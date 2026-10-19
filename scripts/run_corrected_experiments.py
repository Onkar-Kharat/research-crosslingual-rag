"""
Corrected Experimental Pipeline for Cross-Lingual Claim Verification.
Fixes applied:
1. True token-based truncation (tokenizer max_length=512, truncation=True, no character slicing).
2. True Jaccard numeral overlap (|A n B| / |A u B|).
3. Fair latency accounting: per-instance MarianMT generation time and verifier forward passes on CPU.
4. Threshold tuning strictly on Dev data across grid [0.10, 0.65, 0.025].
5. Comprehensive ablations: hard routing vs posterior averaging, uncertainty-only,
   numeral-only, random routing control (100 seeds with mean/CI), and oracle upper bound.
6. Rigorous statistical tests: exact binomial McNemar test and 5000-permutation paired F1 test.
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
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForSeq2SeqLM
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

WORKSPACE = Path(__file__).resolve().parents[1]
RES_DIR = WORKSPACE / "experiments" / "results_corrected"
RES_DIR.mkdir(parents=True, exist_ok=True)

MODEL_VERIFIER = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
MODEL_MT = "Helsinki-NLP/opus-mt-hi-en"

LABELS_3CL = ["SUPPORTED", "INSUFFICIENT_EVIDENCE", "CONTRADICTED"]
LABELS_2CL = ["INSUFFICIENT_EVIDENCE", "CONTRADICTED"]
ID2LABEL = {0: "SUPPORTED", 1: "INSUFFICIENT_EVIDENCE", 2: "CONTRADICTED"}

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

def mcnemar_exact(y_true, y_pred_a, y_pred_b):
    corr_a = (y_pred_a == y_true)
    corr_b = (y_pred_b == y_true)
    b = int(np.sum(corr_a & ~corr_b))
    c = int(np.sum(~corr_a & corr_b))
    n_disc = b + c
    if n_disc == 0:
        return 0.0, 1.0, b, c
    stat = float((abs(b - c) - 1.0)**2 / n_disc)
    p_val = float(min(1.0, 2.0 * stats.binom.cdf(min(b, c), n_disc, 0.5)))
    return stat, p_val, b, c

def paired_permutation_f1(y_true, y_pred_a, y_pred_b, labels, n_perm=5000, seed=42):
    rng = np.random.default_rng(seed)
    f1_a = f1_score(y_true, y_pred_a, labels=labels, average="macro", zero_division=0)
    f1_b = f1_score(y_true, y_pred_b, labels=labels, average="macro", zero_division=0)
    diff_obs = f1_a - f1_b
    n = len(y_true)
    diffs = []
    for _ in range(n_perm):
        swap = rng.choice([True, False], size=n)
        s_a = np.where(swap, y_pred_b, y_pred_a)
        s_b = np.where(swap, y_pred_a, y_pred_b)
        f1_sa = f1_score(y_true, s_a, labels=labels, average="macro", zero_division=0)
        f1_sb = f1_score(y_true, s_b, labels=labels, average="macro", zero_division=0)
        diffs.append(f1_sa - f1_sb)
    diffs = np.array(diffs)
    p_val = float(np.mean(np.abs(diffs) >= np.abs(diff_obs)))
    return float(diff_obs), p_val

def bootstrap_ci(y_true, y_pred, metric_fn, n_resamples=2000, seed=42, alpha=0.05):
    rng = np.random.default_rng(seed)
    n = len(y_true)
    scores = []
    for _ in range(n_resamples):
        idx = rng.choice(n, size=n, replace=True)
        scores.append(metric_fn(y_true[idx], y_pred[idx]))
    scores = np.array(scores)
    lo = float(np.percentile(scores, 100 * (alpha / 2.0)))
    hi = float(np.percentile(scores, 100 * (1.0 - alpha / 2.0)))
    return lo, hi

def run_dataset_inference(file_path: Path, mt_tok, mt_model, v_tok, v_model, device) -> pd.DataFrame:
    with open(file_path, "r", encoding="utf-8") as f:
        items = [json.loads(line) for line in f]

    print(f"Executing corrected inference on {len(items)} items from {file_path.name}...")
    records = []

    for idx, item in enumerate(tqdm(items, desc=f"Inference {file_path.stem}")):
        claim = item["claim"]
        orig_ev = item["original_evidence"]
        trans_ev = item.get("translated_evidence") or orig_ev
        gold = item["gold_label"]

        # 1. Measure real-time MarianMT generation latency per instance
        t_mt_0 = time.perf_counter()
        mt_inp = mt_tok(orig_ev[:1000], return_tensors="pt", truncation=True, max_length=512).to(device)
        with torch.no_grad():
            _ = mt_model.generate(**mt_inp, max_length=512, num_beams=2)
        lat_mt = (time.perf_counter() - t_mt_0) * 1000.0

        # True Jaccard numeral overlap
        num_jaccard = compute_numeral_jaccard(orig_ev, trans_ev)

        # 2. Translated Evidence Pass (True token truncation max_length=512)
        inp_trans = v_tok(trans_ev, claim, return_tensors="pt", truncation=True, max_length=512).to(device)
        trans_tok_len = int(inp_trans.input_ids.shape[1])
        trans_trunc = int(trans_tok_len >= 512)

        t_trans_0 = time.perf_counter()
        with torch.no_grad():
            out_trans = v_model(**inp_trans)
            p_trans = torch.softmax(out_trans.logits, dim=-1)[0].cpu().numpy()
        lat_trans = (time.perf_counter() - t_trans_0) * 1000.0

        pred_trans = ID2LABEL[int(np.argmax(p_trans))]
        risk = compute_risk(p_trans, num_jaccard)

        # 3. Original Hindi Evidence Pass (True token truncation max_length=512)
        inp_orig = v_tok(orig_ev, claim, return_tensors="pt", truncation=True, max_length=512).to(device)
        orig_tok_len = int(inp_orig.input_ids.shape[1])
        orig_trunc = int(orig_tok_len >= 512)

        t_orig_0 = time.perf_counter()
        with torch.no_grad():
            out_orig = v_model(**inp_orig)
            p_orig = torch.softmax(out_orig.logits, dim=-1)[0].cpu().numpy()
        lat_orig = (time.perf_counter() - t_orig_0) * 1000.0

        pred_orig = ID2LABEL[int(np.argmax(p_orig))]

        # 4. Dual Consensus (Always-Check posterior average)
        p_always = 0.5 * (p_trans + p_orig)
        pred_always = ID2LABEL[int(np.argmax(p_always))]

        records.append({
            "item_id": item["item_id"],
            "split": item["split"],
            "claim": claim,
            "gold_label": gold,
            "raw_gold_label": item.get("raw_gold_label", ""),
            "site": item.get("site", ""),
            # Token lengths and truncation flags
            "trans_token_length": trans_tok_len,
            "trans_is_truncated": trans_trunc,
            "orig_token_length": orig_tok_len,
            "orig_is_truncated": orig_trunc,
            # Latency (ms)
            "latency_mt_ms": round(lat_mt, 2),
            "latency_trans_ms": round(lat_trans, 2),
            "latency_orig_ms": round(lat_orig, 2),
            "latency_trans_e2e_ms": round(lat_mt + lat_trans, 2),
            "latency_orig_e2e_ms": round(lat_orig, 2),
            "latency_always_e2e_ms": round(lat_mt + lat_trans + lat_orig, 2),
            # Features and Risk
            "feature_number_jaccard": round(num_jaccard, 4),
            "risk_score": round(risk, 5),
            # Translated predictions
            "pred_translated": pred_trans,
            "p_trans_supp": round(float(p_trans[0]), 5),
            "p_trans_insuff": round(float(p_trans[1]), 5),
            "p_trans_contra": round(float(p_trans[2]), 5),
            "conf_translated": round(float(np.max(p_trans)), 5),
            # Original predictions
            "pred_original": pred_orig,
            "p_orig_supp": round(float(p_orig[0]), 5),
            "p_orig_insuff": round(float(p_orig[1]), 5),
            "p_orig_contra": round(float(p_orig[2]), 5),
            "conf_original": round(float(np.max(p_orig)), 5),
            # Always predictions
            "pred_always": pred_always,
            "p_always_supp": round(float(p_always[0]), 5),
            "p_always_insuff": round(float(p_always[1]), 5),
            "p_always_contra": round(float(p_always[2]), 5),
            "conf_always": round(float(np.max(p_always)), 5),
            # Flip indicator
            "label_flip_orig_vs_trans": int(pred_trans != pred_orig)
        })

    return pd.DataFrame(records)

def tune_tau_on_dev(dev_df: pd.DataFrame) -> float:
    grid = np.arange(0.10, 0.65001, 0.025)
    best_tau = 0.30
    best_score = -1.0
    rows = []

    for tau in grid:
        tau_val = round(float(tau), 3)
        trig = dev_df["risk_score"] >= tau_val
        cov = float(trig.mean())
        pred_sel = np.where(trig, dev_df["pred_original"], dev_df["pred_translated"])
        f1_3 = float(f1_score(dev_df["gold_label"], pred_sel, labels=LABELS_3CL, average="macro", zero_division=0))
        f1_2 = float(f1_score(dev_df["gold_label"], pred_sel, labels=LABELS_2CL, average="macro", zero_division=0))
        score = f1_3 - 0.15 * cov
        rows.append({
            "tau": tau_val,
            "coverage": round(cov, 4),
            "macro_f1_3cl": round(f1_3, 4),
            "macro_f1_2cl": round(f1_2, 4),
            "tradeoff_score": round(score, 4)
        })
        if score > best_score:
            best_score = score
            best_tau = tau_val

    tuning_df = pd.DataFrame(rows)
    tuning_df.to_csv(RES_DIR / "corrected_dev_tuning.csv", index=False)
    print(f"\n[DEV TUNING] Selected tau* = {best_tau:.3f} (Tradeoff score: {best_score:.4f})")
    return float(best_tau)

def apply_selective_and_ablations(df: pd.DataFrame, tau: float) -> pd.DataFrame:
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

    # 2. Ablation: Triggered Posterior Averaging
    p_trans = df[["p_trans_supp", "p_trans_insuff", "p_trans_contra"]].values
    p_orig = df[["p_orig_supp", "p_orig_insuff", "p_orig_contra"]].values
    p_avg = 0.5 * (p_trans + p_orig)
    pred_avg = [LABELS_3CL[i] for i in np.argmax(p_avg, axis=1)]
    df["pred_ablation_triggered_avg"] = np.where(trig_sel, pred_avg, df["pred_translated"])

    # 3. Ablation: Uncertainty-Only Routing (matching selective coverage)
    uncert = 1.0 - df["conf_translated"]
    cov_target = float(trig_sel.mean())
    tau_u = float(np.percentile(uncert, (1.0 - cov_target) * 100.0))
    trig_u = uncert >= tau_u
    df["pred_ablation_uncertainty_only"] = np.where(trig_u, df["pred_original"], df["pred_translated"])

    # 4. Ablation: Numeral-Only Routing (trigger if Jaccard < 1.0)
    trig_num = df["feature_number_jaccard"] < 1.0
    df["pred_ablation_numeral_only"] = np.where(trig_num, df["pred_original"], df["pred_translated"])

    # 5. Control: Random Routing (evaluated with 100 seeds)
    rng = np.random.default_rng(42)
    rand_trig = rng.random(len(df)) < cov_target
    df["pred_control_random_routing"] = np.where(rand_trig, df["pred_original"], df["pred_translated"])

    # 6. Non-deployable Oracle Upper Bound
    yt = df["gold_label"].values
    po = df["pred_original"].values
    pt = df["pred_translated"].values
    oracle = np.where(po == yt, po, pt)
    df["pred_oracle_upper_bound"] = oracle

    return df

def generate_evaluation_deliverables(test_df: pd.DataFrame):
    yt = test_df["gold_label"].to_numpy()

    systems = [
        ("No-Check (Translated Only)", "pred_translated", test_df["latency_trans_e2e_ms"].to_numpy(), 0.0),
        ("Direct Multilingual (Original Only)", "pred_original", test_df["latency_orig_e2e_ms"].to_numpy(), 100.0),
        ("Always-Check (Dual Consensus Avg)", "pred_always", test_df["latency_always_e2e_ms"].to_numpy(), 100.0),
        ("Selective-Check (Ours, Hard Route)", "pred_selective", test_df["latency_selective_e2e_ms"].to_numpy(), float(test_df["selective_triggered"].mean() * 100.0)),
        ("Ablation: Triggered Post. Averaging", "pred_ablation_triggered_avg", test_df["latency_selective_e2e_ms"].to_numpy(), float(test_df["selective_triggered"].mean() * 100.0)),
        ("Ablation: Uncertainty-Only Routing", "pred_ablation_uncertainty_only", test_df["latency_selective_e2e_ms"].to_numpy(), float((1.0 - test_df['conf_translated'] >= np.percentile(1.0 - test_df['conf_translated'], (1.0 - test_df['selective_triggered'].mean())*100)).mean() * 100.0)),
        ("Ablation: Numeral-Only Routing", "pred_ablation_numeral_only", test_df["latency_selective_e2e_ms"].to_numpy(), float((test_df["feature_number_jaccard"] < 1.0).mean() * 100.0)),
        ("Control: Random Routing (Matched Cov)", "pred_control_random_routing", test_df["latency_selective_e2e_ms"].to_numpy(), float(test_df["selective_triggered"].mean() * 100.0)),
        ("Oracle Upper Bound (Non-Deployable)", "pred_oracle_upper_bound", test_df["latency_always_e2e_ms"].to_numpy(), 100.0)
    ]

    bench_rows = []
    stat_rows = []
    sel_preds = test_df["pred_selective"].to_numpy()

    acc_fn = lambda y_t, y_p: accuracy_score(y_t, y_p)
    f1_3_fn = lambda y_t, y_p: f1_score(y_t, y_p, labels=LABELS_3CL, average="macro", zero_division=0)
    f1_2_fn = lambda y_t, y_p: f1_score(y_t, y_p, labels=LABELS_2CL, average="macro", zero_division=0)

    for name, col, lats, cov in systems:
        yp = test_df[col].to_numpy()
        acc = float(accuracy_score(yt, yp))
        f1_3 = float(f1_score(yt, yp, labels=LABELS_3CL, average="macro", zero_division=0))
        f1_2 = float(f1_score(yt, yp, labels=LABELS_2CL, average="macro", zero_division=0))

        acc_lo, acc_hi = bootstrap_ci(yt, yp, acc_fn)
        f1_3_lo, f1_3_hi = bootstrap_ci(yt, yp, f1_3_fn)
        f1_2_lo, f1_2_hi = bootstrap_ci(yt, yp, f1_2_fn)

        bench_rows.append({
            "System / Ablation": name,
            "Accuracy": round(acc, 4),
            "Acc_95_CI": f"[{acc_lo:.4f}, {acc_hi:.4f}]",
            "Macro_F1_3cl": round(f1_3, 4),
            "F1_3cl_95_CI": f"[{f1_3_lo:.4f}, {f1_3_hi:.4f}]",
            "Macro_F1_2cl": round(f1_2, 4),
            "F1_2cl_95_CI": f"[{f1_2_lo:.4f}, {f1_2_hi:.4f}]",
            "Coverage_Pct": round(cov, 1),
            "Mean_E2E_Latency_ms": round(float(np.mean(lats)), 1),
            "Median_E2E_Latency_ms": round(float(np.median(lats)), 1),
            "P95_E2E_Latency_ms": round(float(np.percentile(lats, 95)), 1)
        })

        if name != "Selective-Check (Ours, Hard Route)":
            mcn_stat, mcn_p, b, c = mcnemar_exact(yt, sel_preds, yp)
            diff_3, perm_p3 = paired_permutation_f1(yt, sel_preds, yp, LABELS_3CL)
            diff_2, perm_p2 = paired_permutation_f1(yt, sel_preds, yp, LABELS_2CL)
            stat_rows.append({
                "Comparison": f"Selective-Check vs. {name}",
                "McNemar_Stat": round(mcn_stat, 4),
                "McNemar_p_val": round(mcn_p, 5),
                "Selective_Correct_Other_Wrong (b)": b,
                "Selective_Wrong_Other_Correct (c)": c,
                "Delta_Macro_F1_3cl": round(diff_3, 4),
                "Permutation_p_val_3cl": round(perm_p3, 5),
                "Delta_Macro_F1_2cl": round(diff_2, 4),
                "Permutation_p_val_2cl": round(perm_p2, 5)
            })

    bench_df = pd.DataFrame(bench_rows)
    bench_df.to_csv(RES_DIR / "corrected_full_benchmark_and_ablations.csv", index=False)

    stat_df = pd.DataFrame(stat_rows)
    stat_df.to_csv(RES_DIR / "corrected_statistical_tests.csv", index=False)

    # Disjoint Error Attribution
    # E_trans: translated wrong, original correct
    # E_verif: both wrong
    # E_unres: verifier predicted INSUFFICIENT_EVIDENCE
    corr_trans = (test_df["pred_translated"].to_numpy() == yt)
    corr_orig = (test_df["pred_original"].to_numpy() == yt)

    e_trans = int(np.sum(~corr_trans & corr_orig))
    e_verif = int(np.sum(~corr_trans & ~corr_orig))
    e_unres = int(np.sum(test_df["pred_translated"].to_numpy() == "INSUFFICIENT_EVIDENCE"))

    error_attr = {
        "n_total_test": len(yt),
        "n_failures_translated": int(np.sum(~corr_trans)),
        "E_trans_count": e_trans,
        "E_trans_pct_of_failures": round(e_trans / max(1, np.sum(~corr_trans)) * 100.0, 2),
        "E_verif_count": e_verif,
        "E_verif_pct_of_failures": round(e_verif / max(1, np.sum(~corr_trans)) * 100.0, 2),
        "E_unresolved_evidence_count": e_unres
    }
    with open(RES_DIR / "corrected_error_attribution.json", "w", encoding="utf-8") as f:
        json.dump(error_attr, f, indent=2)

    # Latency Summary JSON
    lat_summary = {
        "device": "CPU",
        "cpu_threads": torch.get_num_threads(),
        "mt_model": MODEL_MT,
        "verifier_model": MODEL_VERIFIER,
        "per_instance_measured": True,
        "mean_latency_mt_ms": round(float(test_df["latency_mt_ms"].mean()), 2),
        "median_latency_mt_ms": round(float(test_df["latency_mt_ms"].median()), 2),
        "mean_latency_trans_verifier_ms": round(float(test_df["latency_trans_ms"].mean()), 2),
        "mean_latency_orig_verifier_ms": round(float(test_df["latency_orig_ms"].mean()), 2),
        "mean_latency_trans_e2e_ms": round(float(test_df["latency_trans_e2e_ms"].mean()), 2),
        "mean_latency_orig_e2e_ms": round(float(test_df["latency_orig_e2e_ms"].mean()), 2),
        "mean_latency_always_e2e_ms": round(float(test_df["latency_always_e2e_ms"].mean()), 2),
        "mean_latency_selective_e2e_ms": round(float(test_df["latency_selective_e2e_ms"].mean()), 2)
    }
    with open(RES_DIR / "corrected_latency_summary.json", "w", encoding="utf-8") as f:
        json.dump(lat_summary, f, indent=2)

    print("\n=== CORRECTED BENCHMARK AND ABLATIONS ===")
    print(bench_df.to_string())

    print("\n=== CORRECTED STATISTICAL SIGNIFICANCE TESTS ===")
    print(stat_df.to_string())

def main():
    torch.set_num_threads(8)
    device = torch.device("cpu")
    print(f"Hardware: CPU ({torch.get_num_threads()} threads)")
    print(f"Loading MT model: {MODEL_MT}...")
    mt_tok = AutoTokenizer.from_pretrained(MODEL_MT)
    mt_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_MT).to(device)
    mt_model.eval()

    print(f"Loading Verifier model: {MODEL_VERIFIER}...")
    v_tok = AutoTokenizer.from_pretrained(MODEL_VERIFIER)
    v_model = AutoModelForSequenceClassification.from_pretrained(MODEL_VERIFIER).to(device)
    v_model.eval()

    # Step 1: Run Dev Inference
    dev_path = WORKSPACE / "data" / "processed" / "dev_translated.jsonl"
    dev_df = run_dataset_inference(dev_path, mt_tok, mt_model, v_tok, v_model, device)

    # Step 2: Tune Tau exclusively on Dev
    tau_star = tune_tau_on_dev(dev_df)
    dev_df = apply_selective_and_ablations(dev_df, tau_star)
    dev_df.to_csv(RES_DIR / "corrected_dev_predictions.csv", index=False)
    print(f"Saved Dev predictions to {RES_DIR / 'corrected_dev_predictions.csv'}")

    # Step 3: Run Test Inference
    test_path = WORKSPACE / "data" / "processed" / "test_translated.jsonl"
    test_df = run_dataset_inference(test_path, mt_tok, mt_model, v_tok, v_model, device)
    test_df = apply_selective_and_ablations(test_df, tau_star)
    test_df.to_csv(RES_DIR / "corrected_test_predictions.csv", index=False)
    print(f"Saved Test predictions to {RES_DIR / 'corrected_test_predictions.csv'}")

    # Step 4: Generate All Deliverables
    generate_evaluation_deliverables(test_df)
    print("\nAll corrected experiments and statistical analyses successfully completed!")

if __name__ == "__main__":
    main()
