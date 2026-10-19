"""
Complete experimental evaluation of Cross-Lingual Claim Verification on X-Fact Hindi.
Evaluates:
  1. Original_Evidence (Direct Multilingual Baseline)
  2. Translated_Evidence (No-Check Baseline)
  3. Always_Check (Dual-Evidence Upper Bound)
  4. Selective_Check (Uncertainty/Risk-Triggered Consultation)

Tunes threshold tau on Dev split; freezes tau for final Test split.
Logs exact latencies, probabilities, label flips, and outputs.
"""
import time
import json
from pathlib import Path
import pandas as pd
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
ID2LABEL = {0: "SUPPORTED", 1: "INSUFFICIENT_EVIDENCE", 2: "CONTRADICTED"}
LABEL2ID = {"SUPPORTED": 0, "INSUFFICIENT_EVIDENCE": 1, "CONTRADICTED": 2}

def compute_entropy(probs: np.ndarray) -> float:
    # Normalized Shannon entropy in [0, 1] for 3 classes
    eps = 1e-12
    p = np.clip(probs, eps, 1.0)
    return float(-np.sum(p * np.log(p)) / np.log(3.0))

def compute_risk(probs_trans: np.ndarray, number_overlap: float) -> float:
    max_p = float(np.max(probs_trans))
    entropy = compute_entropy(probs_trans)
    num_mismatch = 1.0 - float(number_overlap)
    # Risk combines predictive uncertainty (1 - max_p) and translation risk
    return float(0.7 * (1.0 - max_p) + 0.3 * num_mismatch)

def run_inference_on_file(file_path: Path, tokenizer, model, device) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as f:
        items = [json.loads(line) for line in f]
    
    results = []
    print(f"Running inference on {len(items)} items from {file_path.name}...")
    
    for item in items:
        claim = item["claim"]
        orig_ev = item["original_evidence"][:512]
        trans_ev = (item.get("translated_evidence") or orig_ev)[:512]
        num_overlap = float(item.get("feature_number_overlap", 1.0))
        gold = item["gold_label"]
        
        # 1. Condition: Translated Evidence
        t0 = time.perf_counter()
        inp_trans = tokenizer(trans_ev, claim, return_tensors="pt", truncation=True, max_length=512).to(device)
        with torch.no_grad():
            logits_trans = model(**inp_trans).logits
            p_trans = torch.softmax(logits_trans, dim=-1)[0].cpu().numpy()
        lat_trans = (time.perf_counter() - t0) * 1000.0  # ms
        
        pred_trans = ID2LABEL[int(np.argmax(p_trans))]
        conf_trans = float(np.max(p_trans))
        ent_trans = compute_entropy(p_trans)
        risk = compute_risk(p_trans, num_overlap)
        
        # 2. Condition: Original Evidence
        t1 = time.perf_counter()
        inp_orig = tokenizer(orig_ev, claim, return_tensors="pt", truncation=True, max_length=512).to(device)
        with torch.no_grad():
            logits_orig = model(**inp_orig).logits
            p_orig = torch.softmax(logits_orig, dim=-1)[0].cpu().numpy()
        lat_orig = (time.perf_counter() - t1) * 1000.0  # ms
        
        pred_orig = ID2LABEL[int(np.argmax(p_orig))]
        conf_orig = float(np.max(p_orig))
        
        # 3. Condition: Always Check (Dual Evidence Consensus)
        p_always = 0.5 * (p_trans + p_orig)
        pred_always = ID2LABEL[int(np.argmax(p_always))]
        lat_always = lat_trans + lat_orig
        
        # Store comprehensive metrics
        res = {
            "item_id": item["item_id"],
            "split": item["split"],
            "claim": claim,
            "gold_label": gold,
            "raw_gold_label": item.get("raw_gold_label", ""),
            "site": item.get("site", ""),
            # Translated Condition
            "pred_translated": pred_trans,
            "p_trans_supp": round(float(p_trans[0]), 5),
            "p_trans_insuff": round(float(p_trans[1]), 5),
            "p_trans_contra": round(float(p_trans[2]), 5),
            "conf_translated": round(conf_trans, 5),
            "entropy_translated": round(ent_trans, 5),
            "risk_score": round(risk, 5),
            "feature_number_overlap": round(num_overlap, 4),
            "latency_trans_ms": round(lat_trans, 2),
            "correct_translated": int(pred_trans == gold),
            # Original Condition
            "pred_original": pred_orig,
            "p_orig_supp": round(float(p_orig[0]), 5),
            "p_orig_insuff": round(float(p_orig[1]), 5),
            "p_orig_contra": round(float(p_orig[2]), 5),
            "conf_original": round(conf_orig, 5),
            "latency_orig_ms": round(lat_orig, 2),
            "correct_original": int(pred_orig == gold),
            # Always Check Condition
            "pred_always": pred_always,
            "latency_always_ms": round(lat_always, 2),
            "correct_always": int(pred_always == gold),
            # Discrepancy & Flip
            "label_flip_orig_vs_trans": int(pred_trans != pred_orig),
            "helpful_flip": int(pred_trans != gold and pred_orig == gold),
            "harmful_flip": int(pred_trans == gold and pred_orig != gold)
        }
        results.append(res)
        
    return results

def tune_selective_threshold(dev_df: pd.DataFrame) -> tuple[float, pd.DataFrame]:
    candidate_thresholds = np.linspace(0.15, 0.65, 21)
    best_tau = 0.35
    best_f1 = -1.0
    best_tradeoff = -1.0
    
    tuning_records = []
    
    for tau in candidate_thresholds:
        # If risk >= tau -> Trigger check of original evidence
        triggered = dev_df["risk_score"] >= tau
        coverage = triggered.mean()
        
        pred_selective = np.where(triggered, dev_df["pred_original"], dev_df["pred_translated"])
        correct = (pred_selective == dev_df["gold_label"]).astype(int)
        acc = correct.mean()
        
        # Calculate Macro-F1
        classes = ["SUPPORTED", "INSUFFICIENT_EVIDENCE", "CONTRADICTED"]
        f1s = []
        for c in classes:
            tp = np.sum((pred_selective == c) & (dev_df["gold_label"] == c))
            fp = np.sum((pred_selective == c) & (dev_df["gold_label"] != c))
            fn = np.sum((pred_selective != c) & (dev_df["gold_label"] == c))
            prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
            f1s.append(f1)
        macro_f1 = np.mean(f1s)
        
        # Trade-off objective: reward F1 improvement while penalizing high coverage cost
        # Efficiency Trade-off Score = Macro-F1 - 0.2 * Coverage
        tradeoff = macro_f1 - 0.15 * coverage
        
        tuning_records.append({
            "threshold_tau": round(tau, 3),
            "coverage": round(coverage, 4),
            "accuracy": round(acc, 4),
            "macro_f1": round(macro_f1, 4),
            "tradeoff_score": round(tradeoff, 4)
        })
        
        if tradeoff > best_tradeoff:
            best_tradeoff = tradeoff
            best_tau = tau
            best_f1 = macro_f1
            
    tuning_df = pd.DataFrame(tuning_records)
    print(f"Optimal threshold on Dev: tau* = {best_tau:.3f} (Macro-F1={best_f1:.4f}, Tradeoff={best_tradeoff:.4f})")
    return float(best_tau), tuning_df

def apply_selective_checking(df: pd.DataFrame, tau: float) -> pd.DataFrame:
    df = df.copy()
    triggered = df["risk_score"] >= tau
    df["selective_triggered"] = triggered.astype(int)
    df["pred_selective"] = np.where(triggered, df["pred_original"], df["pred_translated"])
    df["correct_selective"] = (df["pred_selective"] == df["gold_label"]).astype(int)
    
    # Latency: if triggered, pays trans + orig; otherwise pays trans only
    df["latency_selective_ms"] = np.where(triggered, df["latency_always_ms"], df["latency_trans_ms"])
    return df

def main():
    device = torch.device("cpu")
    print(f"Loading {MODEL_NAME} for controlled verifier evaluation...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME).to(device)
    model.eval()

    res_dir = Path("experiments/results")
    res_dir.mkdir(parents=True, exist_ok=True)

    # 1. Evaluate Dev Split (N = 103)
    dev_path = Path("data/processed/dev_translated.jsonl")
    dev_results = run_inference_on_file(dev_path, tokenizer, model, device)
    dev_df = pd.DataFrame(dev_results)
    
    # 2. Tune tau* strictly on Dev
    best_tau, tuning_df = tune_selective_threshold(dev_df)
    tuning_df.to_csv(res_dir / "dev_threshold_tuning.csv", index=False)
    
    # Apply tuned threshold to Dev
    dev_df = apply_selective_checking(dev_df, best_tau)
    dev_df.to_csv(res_dir / "dev_predictions.csv", index=False)
    print(f"Saved dev predictions to {res_dir / 'dev_predictions.csv'}")

    # 3. Evaluate Test Split (N = 163) using frozen tau*
    test_path = Path("data/processed/test_translated.jsonl")
    test_results = run_inference_on_file(test_path, tokenizer, model, device)
    test_df = pd.DataFrame(test_results)
    test_df = apply_selective_checking(test_df, best_tau)
    test_df.to_csv(res_dir / "test_predictions.csv", index=False)
    print(f"Saved test predictions to {res_dir / 'test_predictions.csv'}")

    # Update experiment ledger
    ledger_path = Path("experiments/experiment_ledger.csv")
    new_ledger_entry = f"EXP-001,2026-10-15,pilot_and_full,v1.0,mDeBERTa-v3-base-xnli,Helsinki-NLP/opus-mt-hi-en,hi-en,xfact-v1,dev+test,paired_4_conditions,42,python scripts/run_verification_experiments.py,experiments/results/test_predictions.csv,COMPLETED,Dev tau*={best_tau:.3f}\n"
    with open(ledger_path, "a", encoding="utf-8") as f:
        f.write(new_ledger_entry)

    print("Experiment run completed successfully.")

if __name__ == "__main__":
    main()
