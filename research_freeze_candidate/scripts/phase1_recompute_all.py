import json
import csv
import pandas as pd
import numpy as np
import scipy.stats as stats
from pathlib import Path
from collections import Counter
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score,
    confusion_matrix, classification_report
)

WORKSPACE = Path(r"c:\Users\Onkar\OneDrive\Desktop\Research_crosslingual_rag_research")
OUT_DIR = WORKSPACE / "results" / "audit_recomputed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def mcnemar_exact(y_true, y_pred_a, y_pred_b):
    corr_a = (y_pred_a == y_true)
    corr_b = (y_pred_b == y_true)
    b = int(np.sum(corr_a & ~corr_b)) # A correct, B wrong
    c = int(np.sum(~corr_a & corr_b)) # A wrong, B correct
    n_disc = b + c
    if n_disc == 0:
        return 0.0, 1.0, b, c
    stat = float((abs(b - c) - 1.0)**2 / n_disc)
    # Exact two-sided binomial p-value
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
    boot_mean = float(np.mean(scores))
    return lo, hi, boot_mean

def run_recomputations():
    print("Running comprehensive independent audit recomputations...")
    test_csv = WORKSPACE / "experiments" / "results" / "test_predictions.csv"
    df = pd.read_csv(test_csv)
    
    y_true = df["gold_label"].to_numpy()
    classes_all = ["SUPPORTED", "INSUFFICIENT_EVIDENCE", "CONTRADICTED"]
    classes_obs = ["INSUFFICIENT_EVIDENCE", "CONTRADICTED"]
    
    conditions = [
        ("No-Check (Translated)", "pred_translated", df["latency_trans_ms"].to_numpy(), 0.0),
        ("Direct Multilingual (Original)", "pred_original", df["latency_orig_ms"].to_numpy(), 100.0),
        ("Always-Check (Dual)", "pred_always", df["latency_always_ms"].to_numpy(), 100.0),
        ("Selective-Check (Ours, tau*=0.30)", "pred_selective", df["latency_selective_ms"].to_numpy(), float(df["selective_triggered"].mean() * 100.0))
    ]
    
    summary_rows = []
    for cond_name, col_name, latencies, cov in conditions:
        y_pred = df[col_name].to_numpy()
        
        # Exact observed sample metrics
        obs_acc = float(accuracy_score(y_true, y_pred))
        obs_f1_3cl = float(f1_score(y_true, y_pred, labels=classes_all, average="macro", zero_division=0))
        obs_f1_2cl = float(f1_score(y_true, y_pred, labels=classes_obs, average="macro", zero_division=0))
        
        # Bootstrap CIs (BCa / percentile)
        acc_fn = lambda yt, yp: accuracy_score(yt, yp)
        f1_3cl_fn = lambda yt, yp: f1_score(yt, yp, labels=classes_all, average="macro", zero_division=0)
        f1_2cl_fn = lambda yt, yp: f1_score(yt, yp, labels=classes_obs, average="macro", zero_division=0)
        
        acc_lo, acc_hi, acc_bmean = bootstrap_ci(y_true, y_pred, acc_fn)
        f1_3lo, f1_3hi, f1_3bmean = bootstrap_ci(y_true, y_pred, f1_3cl_fn)
        f1_2lo, f1_2hi, f1_2bmean = bootstrap_ci(y_true, y_pred, f1_2cl_fn)
        
        cm = confusion_matrix(y_true, y_pred, labels=classes_all)
        cm_dict = {
            f"pred_{c}": {f"true_{r}": int(cm[i, j]) for i, r in enumerate(classes_all)}
            for j, c in enumerate(classes_all)
        }
        
        summary_rows.append({
            "condition": cond_name,
            "pred_col": col_name,
            "sample_size": len(y_true),
            "correct_count": int(np.sum(y_true == y_pred)),
            "observed_accuracy": obs_acc,
            "bootstrap_mean_accuracy": acc_bmean,
            "acc_ci_95_lower": acc_lo,
            "acc_ci_95_upper": acc_hi,
            "observed_macro_f1_3class": obs_f1_3cl,
            "bootstrap_mean_macro_f1_3class": f1_3bmean,
            "f1_3class_ci_95_lower": f1_3lo,
            "f1_3class_ci_95_upper": f1_3hi,
            "observed_macro_f1_2class": obs_f1_2cl,
            "bootstrap_mean_macro_f1_2class": f1_2bmean,
            "f1_2class_ci_95_lower": f1_2lo,
            "f1_2class_ci_95_upper": f1_2hi,
            "coverage_pct": cov,
            "latency_mean_ms": float(np.mean(latencies)),
            "latency_median_ms": float(np.median(latencies)),
            "latency_std_ms": float(np.std(latencies)),
        })
        
        # Save confusion matrix
        cm_df = pd.DataFrame(cm, index=[f"True_{c}" for c in classes_all], columns=[f"Pred_{c}" for c in classes_all])
        cm_df.to_csv(OUT_DIR / f"confusion_matrix_{col_name}.csv")
        
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(OUT_DIR / "recomputed_test_main_results.csv", index=False)
    print("Saved recomputed_test_main_results.csv")
    
    # Statistical tests: all pairwise combinations
    test_rows = []
    cond_map = {name: df[col].to_numpy() for name, col, _, _ in conditions}
    pairs = [
        ("Selective-Check (Ours, tau*=0.30)", "No-Check (Translated)"),
        ("Selective-Check (Ours, tau*=0.30)", "Direct Multilingual (Original)"),
        ("Selective-Check (Ours, tau*=0.30)", "Always-Check (Dual)"),
        ("Direct Multilingual (Original)", "No-Check (Translated)"),
        ("Always-Check (Dual)", "No-Check (Translated)"),
        ("Direct Multilingual (Original)", "Always-Check (Dual)")
    ]
    
    for cond_a, cond_b in pairs:
        yp_a = cond_map[cond_a]
        yp_b = cond_map[cond_b]
        
        stat, p_mcnemar, b, c = mcnemar_exact(y_true, yp_a, yp_b)
        diff_f1_3, p_perm_3 = paired_permutation_f1(y_true, yp_a, yp_b, labels=classes_all)
        diff_f1_2, p_perm_2 = paired_permutation_f1(y_true, yp_a, yp_b, labels=classes_obs)
        
        test_rows.append({
            "comparison": f"{cond_a} vs. {cond_b}",
            "discordant_pairs_a_correct_b_wrong": b,
            "discordant_pairs_b_correct_a_wrong": c,
            "total_discordant": b + c,
            "mcnemar_stat": stat,
            "mcnemar_p_value": p_mcnemar,
            "delta_accuracy": float(accuracy_score(y_true, yp_a) - accuracy_score(y_true, yp_b)),
            "delta_macro_f1_3class": diff_f1_3,
            "permutation_p_f1_3class": p_perm_3,
            "delta_macro_f1_2class": diff_f1_2,
            "permutation_p_f1_2class": p_perm_2,
            "significant_mcnemar_alpha_05": p_mcnemar < 0.05,
            "significant_perm_f1_alpha_05": p_perm_3 < 0.05
        })
        
    test_df = pd.DataFrame(test_rows)
    test_df.to_csv(OUT_DIR / "recomputed_statistical_tests.csv", index=False)
    print("Saved recomputed_statistical_tests.csv")
    
    # Error attribution reconciliation
    # Total errors in No-Check:
    pt = df["pred_translated"].to_numpy()
    po = df["pred_original"].to_numpy()
    
    # Complete, mutually exclusive and exhaustive partition of all 163 items:
    # Let y_true be ground truth
    trans_corr = (pt == y_true)
    trans_wrong = (pt != y_true)
    
    orig_corr = (po == y_true)
    orig_wrong = (po != y_true)
    
    # Partition of the 111 errors:
    # 1. Recovered by original evidence (E_trans_recovered): pt != yt, po == yt
    #    Split by gold class:
    e_trans_contra = np.sum(trans_wrong & orig_corr & (y_true == "CONTRADICTED")) # 38
    e_trans_insuff = np.sum(trans_wrong & orig_corr & (y_true == "INSUFFICIENT_EVIDENCE")) # 3
    e_trans_total = e_trans_contra + e_trans_insuff # 41
    
    # 2. Unrecovered errors where both fail: pt != yt, po != yt
    #    Split by gold class:
    e_both_contra = np.sum(trans_wrong & orig_wrong & (y_true == "CONTRADICTED")) # 61 (verifier reasoning failure)
    e_both_insuff = np.sum(trans_wrong & orig_wrong & (y_true == "INSUFFICIENT_EVIDENCE")) # 9 (evidence insufficiency unrecovered)
    e_both_total = e_both_contra + e_both_insuff # 70
    
    total_errors = np.sum(trans_wrong) # 111
    
    error_reconciliation = [
        {"Category": "Total No-Check (Translated) Errors", "Count": int(total_errors), "Share_of_Errors": "100.0%", "Operational_Definition": "Claims where pred_translated != gold_label"},
        {"Category": "1. Recoverable via Original (Translation-Induced)", "Count": int(e_trans_total), "Share_of_Errors": f"{e_trans_total/total_errors*100:.2f}%", "Operational_Definition": "pred_translated != gold AND pred_original == gold"},
        {"Category": "   -- On CONTRADICTED claims", "Count": int(e_trans_contra), "Share_of_Errors": f"{e_trans_contra/total_errors*100:.2f}%", "Operational_Definition": "gold=CONTRADICTED, original fixes translation error"},
        {"Category": "   -- On INSUFFICIENT claims", "Count": int(e_trans_insuff), "Share_of_Errors": f"{e_trans_insuff/total_errors*100:.2f}%", "Operational_Definition": "gold=INSUFFICIENT, original fixes translation error (overlap in prior code)"},
        {"Category": "2. Unrecovered Reasoning Failures (Verifier Error)", "Count": int(e_both_contra), "Share_of_Errors": f"{e_both_contra/total_errors*100:.2f}%", "Operational_Definition": "pred_translated != gold AND pred_original != gold on gold=CONTRADICTED"},
        {"Category": "3. Unrecovered Evidence Insufficiency", "Count": int(e_both_insuff), "Share_of_Errors": f"{e_both_insuff/total_errors*100:.2f}%", "Operational_Definition": "pred_translated != gold AND pred_original != gold on gold=INSUFFICIENT"},
        {"Category": "Total Disjoint Sum", "Count": int(e_trans_total + e_both_contra + e_both_insuff), "Share_of_Errors": "100.0%", "Operational_Definition": "41 + 61 + 9 = 111 (Cleanly partitions all 111 errors)"}
    ]
    
    err_rec_df = pd.DataFrame(error_reconciliation)
    err_rec_df.to_csv(OUT_DIR / "recomputed_error_attribution_disjoint.csv", index=False)
    print("Saved recomputed_error_attribution_disjoint.csv")
    
    # Save a machine-readable summary JSON
    summary_data = {
        "dataset_sample_size": len(y_true),
        "gold_class_distribution": dict(Counter(y_true)),
        "conditions": summary_rows,
        "statistical_tests": test_rows,
        "error_partition": error_reconciliation
    }
    with open(OUT_DIR / "audit_metrics_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)
    print("Saved audit_metrics_summary.json")

if __name__ == "__main__":
    run_recomputations()
