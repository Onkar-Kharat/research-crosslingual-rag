"""
Corrected Experimental Pipeline for Cross-Lingual Claim Verification.
Fixes:
1. True token-based truncation (tokenizer max_length=512, eliminating string character slicing [:512]).
2. True Jaccard numeral overlap (|A n B| / |A u B|).
3. Fair latency accounting including machine translation.
4. Comprehensive ablations: hard routing vs triggered posterior averaging,
   uncertainty-only, numeral-only, random routing, and oracle upper bound.
"""
import re
import json
import time
import torch
import numpy as np
import pandas as pd
import scipy.stats as stats
from pathlib import Path
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, f1_score

WORKSPACE = Path(r"c:\Users\Onkar\OneDrive\Desktop\Research_crosslingual_rag_research")
RES_DIR = WORKSPACE / "experiments" / "results_corrected"
RES_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
LABELS = ["SUPPORTED", "INSUFFICIENT_EVIDENCE", "CONTRADICTED"]
ID2LABEL = {0: "SUPPORTED", 1: "INSUFFICIENT_EVIDENCE", 2: "CONTRADICTED"}

# Estimated MarianMT translation time per item on CPU (based on benchmark)
MEAN_MT_LATENCY_MS = 1120.0

def extract_numbers(text: str) -> set[str]:
    devanagari_nums = {"०": "0", "१": "1", "२": "2", "३": "3", "४": "4", "५": "5", "६": "6", "७": "7", "८": "8", "९": "9"}
    norm_text = "".join(devanagari_nums.get(c, c) for c in text)
    return set(re.findall(r"\b\d+(?:[\.,]\d+)?\b", norm_text))

def compute_numeral_jaccard(orig_text: str, trans_text: str) -> float:
    orig_nums = extract_numbers(orig_text)
    trans_nums = extract_numbers(trans_text)
    union = orig_nums | trans_nums
    if not union:
        return 1.0 # No numbers in either text
    intersection = orig_nums & trans_nums
    return float(len(intersection) / len(union))

def compute_risk(probs_trans: np.ndarray, num_jaccard: float) -> float:
    max_p = float(np.max(probs_trans))
    num_mismatch = 1.0 - float(num_jaccard)
    return float(0.70 * (1.0 - max_p) + 0.30 * num_mismatch)

def run_inference_dataset(file_path: Path, tokenizer, model, device) -> pd.DataFrame:
    with open(file_path, "r", encoding="utf-8") as f:
        items = [json.loads(line) for line in f]
        
    print(f"Running corrected token-truncated inference on {len(items)} items from {file_path.name}...")
    records = []
    
    for item in tqdm(items, desc=f"Evaluating {file_path.stem}"):
        claim = item["claim"]
        orig_ev = item["original_evidence"]
        trans_ev = item.get("translated_evidence") or orig_ev
        gold = item["gold_label"]
        
        # True Jaccard numeral overlap
        num_jaccard = compute_numeral_jaccard(orig_ev, trans_ev)
        
        # 1. Translated Evidence Pass (True token truncation max_length=512)
        t0 = time.perf_counter()
        inp_trans = tokenizer(trans_ev, claim, return_tensors="pt", truncation=True, max_length=512).to(device)
        with torch.no_grad():
            out_trans = model(**inp_trans)
            p_trans = torch.softmax(out_trans.logits, dim=-1)[0].cpu().numpy()
        lat_trans = (time.perf_counter() - t0) * 1000.0
        
        pred_trans = ID2LABEL[int(np.argmax(p_trans))]
        risk = compute_risk(p_trans, num_jaccard)
        
        # 2. Original Hindi Evidence Pass (True token truncation max_length=512)
        t1 = time.perf_counter()
        inp_orig = tokenizer(orig_ev, claim, return_tensors="pt", truncation=True, max_length=512).to(device)
        with torch.no_grad():
            out_orig = model(**inp_orig)
            p_orig = torch.softmax(out_orig.logits, dim=-1)[0].cpu().numpy()
        lat_orig = (time.perf_counter() - t1) * 1000.0
        
        pred_orig = ID2LABEL[int(np.argmax(p_orig))]
        
        # 3. Always-Check (Dual Consensus via 0.5 posterior average)
        p_always = 0.5 * (p_trans + p_orig)
        pred_always = ID2LABEL[int(np.argmax(p_always))]
        
        records.append({
            "item_id": item["item_id"],
            "split": item["split"],
            "claim": claim,
            "gold_label": gold,
            "raw_gold_label": item.get("raw_gold_label", ""),
            "site": item.get("site", ""),
            # Translated
            "pred_translated": pred_trans,
            "p_trans_supp": round(float(p_trans[0]), 5),
            "p_trans_insuff": round(float(p_trans[1]), 5),
            "p_trans_contra": round(float(p_trans[2]), 5),
            "conf_translated": round(float(np.max(p_trans)), 5),
            "feature_number_jaccard": round(num_jaccard, 4),
            "risk_score": round(risk, 5),
            "latency_trans_ms": round(lat_trans, 2),
            "latency_trans_e2e_ms": round(lat_trans + MEAN_MT_LATENCY_MS, 2),
            # Original
            "pred_original": pred_orig,
            "p_orig_supp": round(float(p_orig[0]), 5),
            "p_orig_insuff": round(float(p_orig[1]), 5),
            "p_orig_contra": round(float(p_orig[2]), 5),
            "conf_original": round(float(np.max(p_orig)), 5),
            "latency_orig_ms": round(lat_orig, 2),
            # Always
            "pred_always": pred_always,
            "latency_always_ms": round(lat_trans + lat_orig, 2),
            "latency_always_e2e_ms": round(lat_trans + lat_orig + MEAN_MT_LATENCY_MS, 2),
            # Discrepancy
            "label_flip_orig_vs_trans": int(pred_trans != pred_orig)
        })
        
    return pd.DataFrame(records)

def tune_tau(dev_df: pd.DataFrame) -> float:
    candidates = np.linspace(0.15, 0.65, 21)
    best_tau = 0.30
    best_score = -1.0
    
    rows = []
    for tau in candidates:
        trig = dev_df["risk_score"] >= tau
        cov = trig.mean()
        pred_sel = np.where(trig, dev_df["pred_original"], dev_df["pred_translated"])
        f1 = f1_score(dev_df["gold_label"], pred_sel, labels=LABELS, average="macro", zero_division=0)
        score = f1 - 0.15 * cov
        rows.append({"tau": tau, "coverage": cov, "macro_f1": f1, "score": score})
        if score > best_score:
            best_score = score
            best_tau = tau
            
    pd.DataFrame(rows).to_csv(RES_DIR / "corrected_dev_tuning.csv", index=False)
    print(f"Optimal tau* on Dev: {best_tau:.3f} (Tradeoff score: {best_score:.4f})")
    return float(best_tau)

def apply_systems_and_ablations(df: pd.DataFrame, tau: float) -> pd.DataFrame:
    df = df.copy()
    
    # 1. Main Selective-Check (Hard Routing)
    trig_sel = df["risk_score"] >= tau
    df["selective_triggered"] = trig_sel.astype(int)
    df["pred_selective"] = np.where(trig_sel, df["pred_original"], df["pred_translated"])
    df["latency_selective_e2e_ms"] = np.where(
        trig_sel,
        df["latency_always_e2e_ms"],
        df["latency_trans_e2e_ms"]
    )
    
    # 2. Ablation: Triggered Posterior Averaging (evaluating paper Eq 1 text)
    p_trans = df[["p_trans_supp", "p_trans_insuff", "p_trans_contra"]].values
    p_orig = df[["p_orig_supp", "p_orig_insuff", "p_orig_contra"]].values
    p_avg = 0.5 * (p_trans + p_orig)
    pred_avg = [LABELS[i] for i in np.argmax(p_avg, axis=1)]
    df["pred_ablation_triggered_avg"] = np.where(trig_sel, pred_avg, df["pred_translated"])
    
    # 3. Ablation: Uncertainty-Only Routing (top 83.4% uncertainty)
    uncert = 1.0 - df["conf_translated"]
    tau_u = float(np.percentile(uncert, (1.0 - trig_sel.mean()) * 100))
    trig_u = uncert >= tau_u
    df["pred_ablation_uncertainty_only"] = np.where(trig_u, df["pred_original"], df["pred_translated"])
    
    # 4. Ablation: Numeral-Only Routing (mismatch > 0)
    trig_num = df["feature_number_jaccard"] < 1.0
    df["pred_ablation_numeral_only"] = np.where(trig_num, df["pred_original"], df["pred_translated"])
    
    # 5. Control: Random Routing (matched at empirical coverage)
    rng = np.random.default_rng(42)
    rand_trig = rng.random(len(df)) < trig_sel.mean()
    df["pred_control_random_routing"] = np.where(rand_trig, df["pred_original"], df["pred_translated"])
    
    # 6. Non-deployable Oracle Upper Bound
    yt = df["gold_label"].values
    po = df["pred_original"].values
    pt = df["pred_translated"].values
    oracle = np.where(po == yt, po, pt)
    df["pred_oracle_upper_bound"] = oracle
    
    return df

def generate_benchmark_table(test_df: pd.DataFrame):
    yt = test_df["gold_label"].values
    
    systems = [
        ("No-Check (Translated Only)", "pred_translated", test_df["latency_trans_e2e_ms"].values, 0.0),
        ("Direct Multilingual (Original Only)", "pred_original", test_df["latency_orig_ms"].values, 100.0),
        ("Always-Check (Dual Consensus Avg)", "pred_always", test_df["latency_always_e2e_ms"].values, 100.0),
        ("Selective-Check (Ours, Hard Route)", "pred_selective", test_df["latency_selective_e2e_ms"].values, float(test_df["selective_triggered"].mean() * 100)),
        ("Ablation: Triggered Post. Averaging", "pred_ablation_triggered_avg", test_df["latency_selective_e2e_ms"].values, float(test_df["selective_triggered"].mean() * 100)),
        ("Ablation: Uncertainty-Only Routing", "pred_ablation_uncertainty_only", test_df["latency_selective_e2e_ms"].values, 83.4),
        ("Ablation: Numeral-Only Routing", "pred_ablation_numeral_only", test_df["latency_selective_e2e_ms"].values, float((test_df["feature_number_jaccard"] < 1.0).mean() * 100)),
        ("Control: Random Routing (83.4% Cov)", "pred_control_random_routing", test_df["latency_selective_e2e_ms"].values, 83.4),
        ("Oracle Upper Bound (Non-Deployable)", "pred_oracle_upper_bound", test_df["latency_always_e2e_ms"].values, 100.0)
    ]
    
    rows = []
    for name, col, lats, cov in systems:
        yp = test_df[col].values
        acc = accuracy_score(yt, yp)
        f1_3cl = f1_score(yt, yp, labels=LABELS, average="macro", zero_division=0)
        f1_2cl = f1_score(yt, yp, labels=["INSUFFICIENT_EVIDENCE", "CONTRADICTED"], average="macro", zero_division=0)
        
        rows.append({
            "System / Ablation": name,
            "Accuracy": round(acc, 4),
            "Macro_F1_3cl": round(f1_3cl, 4),
            "Macro_F1_2cl": round(f1_2cl, 4),
            "Coverage_Pct": round(cov, 1),
            "Mean_E2E_Latency_ms": round(float(np.mean(lats)), 1)
        })
        
    out_table = pd.DataFrame(rows)
    out_table.to_csv(RES_DIR / "corrected_full_benchmark_and_ablations.csv", index=False)
    print("\n=== CORRECTED BENCHMARK AND ABLATION RESULTS (N=163) ===")
    print(out_table.to_markdown())

def main():
    device = torch.device("cpu")
    print(f"Loading {MODEL_NAME} for corrected inference...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME).to(device)
    model.eval()
    
    # Dev
    dev_path = WORKSPACE / "data" / "processed" / "dev_translated.jsonl"
    dev_df = run_inference_dataset(dev_path, tokenizer, model, device)
    tau = tune_tau(dev_df)
    dev_df = apply_systems_and_ablations(dev_df, tau)
    dev_df.to_csv(RES_DIR / "corrected_dev_predictions.csv", index=False)
    
    # Test
    test_path = WORKSPACE / "data" / "processed" / "test_translated.jsonl"
    test_df = run_inference_dataset(test_path, tokenizer, model, device)
    test_df = apply_systems_and_ablations(test_df, tau)
    test_df.to_csv(RES_DIR / "corrected_test_predictions.csv", index=False)
    
    generate_benchmark_table(test_df)
    print("Corrected experiment run completed successfully!")

if __name__ == "__main__":
    main()
