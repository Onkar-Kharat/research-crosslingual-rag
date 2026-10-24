"""
Comprehensive Numerical Recomputation and Audit Script.
Independently verifies every metric, contingency count, statistical test,
confidence interval, and error partition against canonical files.
"""
import json
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support, confusion_matrix

def wilson_ci(k, n, conf=0.95):
    if n == 0:
        return 0.0, 0.0
    z = stats.norm.ppf(1 - (1 - conf) / 2)
    p = k / n
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    diff = z * np.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denom
    return float(max(0.0, centre - diff)), float(min(1.0, centre + diff))

def mcnemar_calc(y_true, pred_a, pred_b):
    corr_a = (pred_a == y_true)
    corr_b = (pred_b == y_true)
    b = int(np.sum(corr_a & ~corr_b))  # A correct, B wrong
    c = int(np.sum(~corr_a & corr_b))  # A wrong, B correct
    n_disc = b + c
    if n_disc == 0:
        return 0.0, 1.0, 1.0, b, c
    stat = float((abs(b - c) - 1.0)**2 / n_disc)
    p_asymp = float(stats.chi2.sf(stat, df=1))
    p_exact = float(min(1.0, 2.0 * stats.binom.cdf(min(b, c), n_disc, 0.5)))
    return stat, p_asymp, p_exact, b, c

def paired_permutation_f1(y_true, pred_a, pred_b, labels, n_perm=5000, seed=42):
    rng = np.random.default_rng(seed)
    f1_a = f1_score(y_true, pred_a, labels=labels, average="macro", zero_division=0)
    f1_b = f1_score(y_true, pred_b, labels=labels, average="macro", zero_division=0)
    diff_obs = f1_a - f1_b
    n = len(y_true)
    diffs = []
    for _ in range(n_perm):
        swap = rng.choice([True, False], size=n)
        s_a = np.where(swap, pred_b, pred_a)
        s_b = np.where(swap, pred_a, pred_b)
        f1_sa = f1_score(y_true, s_a, labels=labels, average="macro", zero_division=0)
        f1_sb = f1_score(y_true, s_b, labels=labels, average="macro", zero_division=0)
        diffs.append(f1_sa - f1_sb)
    diffs = np.array(diffs)
    p_val = float(np.mean(np.abs(diffs) >= np.abs(diff_obs)))
    return float(diff_obs), p_val

def bootstrap_percentile_ci(y_true, pred, metric_fn, n_resamples=2000, seed=42, alpha=0.05):
    rng = np.random.default_rng(seed)
    n = len(y_true)
    scores = []
    for _ in range(n_resamples):
        idx = rng.choice(n, size=n, replace=True)
        scores.append(metric_fn(y_true[idx], pred[idx]))
    lo = float(np.percentile(scores, 100 * (alpha / 2)))
    hi = float(np.percentile(scores, 100 * (1 - alpha / 2)))
    return lo, hi

def bh_fdr_correction(p_values):
    p_vals = np.asarray(p_values, dtype=float)
    n = len(p_vals)
    order = np.argsort(p_vals)
    sorted_p = p_vals[order]
    fdr = np.zeros(n)
    running_min = 1.0
    for i in range(n - 1, -1, -1):
        rank = i + 1
        adj = (sorted_p[i] * n) / rank
        running_min = min(running_min, adj)
        fdr[i] = min(1.0, running_min)
    orig_order_fdr = np.zeros(n)
    orig_order_fdr[order] = fdr
    return orig_order_fdr.tolist()

def main():
    test_df = pd.read_csv("experiments/results_corrected/canonical_test_predictions.csv")
    dev_df = pd.read_csv("experiments/results_corrected/canonical_dev_predictions.csv")
    
    print("=== 1. DATASET PARTITION AUDIT ===")
    print(f"Dev instances: {len(dev_df)}")
    print(f"Dev gold counts: {dev_df['gold_label'].value_counts().to_dict()}")
    print(f"Test instances: {len(test_df)}")
    print(f"Test gold counts: {test_df['gold_label'].value_counts().to_dict()}")
    
    y_true = test_df["gold_label"].to_numpy()
    p_trans = test_df["pred_translated"].to_numpy()
    p_orig = test_df["pred_original"].to_numpy()
    p_always = test_df["pred_always"].to_numpy()
    p_sel = test_df["pred_selective"].to_numpy()
    
    print("\n=== 2. AGREEMENT AND TRANSITION MATRIX AUDIT ===")
    agr_mask = (p_trans == p_orig)
    agr_count = int(np.sum(agr_mask))
    disagr_count = int(np.sum(~agr_mask))
    print(f"Agreement count: {agr_count}/{len(y_true)} ({agr_count/len(y_true)*100:.2f}%)")
    print(f"Disagreement count: {disagr_count}/{len(y_true)} ({disagr_count/len(y_true)*100:.2f}%)")
    w_lo, w_hi = wilson_ci(disagr_count, len(y_true))
    print(f"Disagreement 95% Wilson CI: [{w_lo*100:.2f}%, {w_hi*100:.2f}%]")
    
    labels_3cl = ["CONTRADICTED", "INSUFFICIENT_EVIDENCE", "SUPPORTED"]
    cm = confusion_matrix(p_trans, p_orig, labels=labels_3cl)
    print("\n3x3 Transition Matrix (Rows: Translated, Cols: Original Hindi):")
    print("             " + "  ".join([f"{l[:7]:>7}" for l in labels_3cl]) + "  RowTotal")
    for idx, row_l in enumerate(labels_3cl):
        row_str = f"{row_l[:12]:<12} " + "  ".join([f"{cm[idx, j]:>7}" for j in range(3)])
        row_total = np.sum(cm[idx, :])
        row_str += f"  {row_total:>8}"
        print(row_str)
    col_totals = np.sum(cm, axis=0)
    print(f"{'ColTotal':<12} " + "  ".join([f"{col_totals[j]:>7}" for j in range(3)]) + f"  {np.sum(cm):>8}")
    
    # Supported flips
    supp_idx = labels_3cl.index("SUPPORTED")
    contra_idx = labels_3cl.index("CONTRADICTED")
    n_supp_trans = np.sum(cm[supp_idx, :])
    n_supp_to_contra = cm[supp_idx, contra_idx]
    pct_supp_to_contra = n_supp_to_contra / n_supp_trans
    sw_lo, sw_hi = wilson_ci(n_supp_to_contra, n_supp_trans)
    print(f"\nSupported -> Contradicted flip: {n_supp_to_contra}/{n_supp_trans} ({pct_supp_to_contra*100:.2f}%), Wilson 95% CI: [{sw_lo*100:.2f}%, {sw_hi*100:.2f}%]")
    
    # Contradicted flips
    n_contra_trans = np.sum(cm[contra_idx, :])
    n_contra_to_supp = cm[contra_idx, supp_idx]
    pct_contra_to_supp = n_contra_to_supp / n_contra_trans
    cw_lo, cw_hi = wilson_ci(n_contra_to_supp, n_contra_trans)
    print(f"Contradicted -> Supported flip: {n_contra_to_supp}/{n_contra_trans} ({pct_contra_to_supp*100:.2f}%), Wilson 95% CI: [{cw_lo*100:.2f}%, {cw_hi*100:.2f}%]")
    
    print("\n=== 3. SYSTEM PERFORMANCE METRICS ===")
    systems = {
        "No-Check (Translated)": p_trans,
        "Direct Multilingual (Original)": p_orig,
        "Always-Check (Dual Consensus)": p_always,
        "Selective-Check (Hard Route)": p_sel,
        "Ablation: Triggered Post. Avg": test_df["pred_ablation_triggered_avg"].to_numpy(),
        "Ablation: Uncertainty-Only": test_df["pred_ablation_uncertainty_only"].to_numpy(),
        "Ablation: Numeral-Only": test_df["pred_ablation_numeral_only"].to_numpy(),
        "Control: Random Routing": test_df["pred_control_random_routing"].to_numpy(),
        "Oracle Upper Bound": test_df["pred_oracle_upper_bound"].to_numpy()
    }
    
    results = []
    labels_2cl = ["CONTRADICTED", "INSUFFICIENT_EVIDENCE"]
    for name, pred in systems.items():
        k = int(np.sum(pred == y_true))
        n = len(y_true)
        acc = k / n
        w_lo, w_hi = wilson_ci(k, n)
        f1_3 = f1_score(y_true, pred, labels=labels_3cl, average="macro", zero_division=0)
        f1_2 = f1_score(y_true, pred, labels=labels_2cl, average="macro", zero_division=0)
        
        # Per class F1
        p_c, r_c, f_c, _ = precision_recall_fscore_support(y_true, pred, labels=labels_3cl, zero_division=0)
        
        results.append({
            "System": name,
            "Accuracy": acc,
            "Correct": k,
            "Total": n,
            "Acc_Wilson_95": f"[{w_lo:.4f}, {w_hi:.4f}]",
            "Macro_F1_3cl": f1_3,
            "Macro_F1_2cl": f1_2,
            "F1_Contra": f_c[0],
            "F1_Neutral": f_c[1],
            "F1_Support": f_c[2],
            "Prec_Contra": p_c[0],
            "Rec_Contra": r_c[0]
        })
    res_df = pd.DataFrame(results)
    print(res_df[["System", "Accuracy", "Correct", "Acc_Wilson_95", "Macro_F1_3cl", "Macro_F1_2cl", "F1_Contra", "F1_Neutral", "F1_Support"]].to_string(index=False))
    
    print("\n=== 4. PAIRED MCNEMAR AND PERMUTATION TESTS ===")
    comparisons = [
        ("No-Check (Translated)", "Direct Multilingual (Original)", p_trans, p_orig),
        ("Selective-Check (Hard Route)", "Direct Multilingual (Original)", p_sel, p_orig),
        ("Selective-Check (Hard Route)", "Always-Check (Dual Consensus)", p_sel, p_always),
        ("Selective-Check (Hard Route)", "No-Check (Translated)", p_sel, p_trans),
        ("Selective-Check (Hard Route)", "Control: Random Routing", p_sel, test_df["pred_control_random_routing"].to_numpy()),
        ("Selective-Check (Hard Route)", "Ablation: Numeral-Only", p_sel, test_df["pred_ablation_numeral_only"].to_numpy())
    ]
    
    stat_results = []
    for name_a, name_b, pr_a, pr_b in comparisons:
        stat, p_asymp, p_exact, b, c = mcnemar_calc(y_true, pr_a, pr_b)
        delta_f1_3, perm_p_3 = paired_permutation_f1(y_true, pr_a, pr_b, labels=labels_3cl, n_perm=5000, seed=42)
        delta_f1_2, perm_p_2 = paired_permutation_f1(y_true, pr_a, pr_b, labels=labels_2cl, n_perm=5000, seed=42)
        stat_results.append({
            "Comparison": f"{name_a} vs {name_b}",
            "b": b,
            "c": c,
            "Total_Disc": b + c,
            "McNemar_Stat": stat,
            "McNemar_p_asymp": p_asymp,
            "McNemar_p_exact": p_exact,
            "Delta_F1_3cl": delta_f1_3,
            "Perm_p_3cl": perm_p_3,
            "Delta_F1_2cl": delta_f1_2,
            "Perm_p_2cl": perm_p_2
        })
    stat_df = pd.DataFrame(stat_results)
    stat_df["McNemar_FDR"] = bh_fdr_correction(stat_df["McNemar_p_exact"].tolist())
    stat_df["Perm_3cl_FDR"] = bh_fdr_correction(stat_df["Perm_p_3cl"].tolist())
    
    print(stat_df[["Comparison", "b", "c", "Total_Disc", "McNemar_Stat", "McNemar_p_exact", "McNemar_FDR", "Delta_F1_3cl", "Perm_p_3cl", "Perm_3cl_FDR"]].to_string(index=False))
    
    print("\n=== 5. ERROR ATTRIBUTION DECOMPOSITION ===")
    corr_trans = (p_trans == y_true)
    corr_orig = (p_orig == y_true)
    
    n_fail_trans = int(np.sum(~corr_trans))
    n_succ_trans = int(np.sum(corr_trans))
    s_trans = int(np.sum(~corr_trans & corr_orig))
    s_verif = int(np.sum(~corr_trans & ~corr_orig))
    s_control = int(np.sum(corr_trans & corr_orig))
    s_degraded = int(np.sum(corr_trans & ~corr_orig))
    
    print(f"Total translation failures: {n_fail_trans}/{len(y_true)} ({n_fail_trans/len(y_true)*100:.1f}%)")
    print(f"  Recovered by Hindi (S_trans): {s_trans} ({s_trans/n_fail_trans*100:.1f}% of failures, {s_trans/len(y_true)*100:.1f}% of test)")
    print(f"  Both representations wrong (S_verif): {s_verif} ({s_verif/n_fail_trans*100:.1f}% of failures, {s_verif/len(y_true)*100:.1f}% of test)")
    print(f"Total translation successes: {n_succ_trans}/{len(y_true)} ({n_succ_trans/len(y_true)*100:.1f}%)")
    print(f"  Both representations correct (Control): {s_control} ({s_control/n_succ_trans*100:.1f}% of successes, {s_control/len(y_true)*100:.1f}% of test)")
    print(f"  Degraded by Hindi (S_degraded): {s_degraded} ({s_degraded/n_succ_trans*100:.1f}% of successes, {s_degraded/len(y_true)*100:.1f}% of test)")
    print(f"Net gain for Direct Multilingual: {s_trans} - {s_degraded} = {s_trans - s_degraded} correct instances")

if __name__ == "__main__":
    main()
