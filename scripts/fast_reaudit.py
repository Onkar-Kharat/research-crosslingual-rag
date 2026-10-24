"""
Vectorized Fast Reaudit Script.
Instantly computes all metrics, Wilson CIs, McNemar tests, exact binomial p-values,
vectorized 5,000-resample paired permutation tests, and error partitions.
"""
import sys
import json
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import confusion_matrix

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
    b = int(np.sum(corr_a & ~corr_b))
    c = int(np.sum(~corr_a & corr_b))
    n_disc = b + c
    if n_disc == 0:
        return 0.0, 1.0, 1.0, b, c
    stat = float((abs(b - c) - 1.0)**2 / n_disc)
    p_asymp = float(stats.chi2.sf(stat, df=1))
    p_exact = float(min(1.0, 2.0 * stats.binom.cdf(min(b, c), n_disc, 0.5)))
    return stat, p_asymp, p_exact, b, c

def compute_macro_f1_vectorized(y_true_int, pred_matrix, num_classes=3):
    # pred_matrix: shape (B, N)
    # y_true_int: shape (N,)
    f1_list = []
    for c in range(num_classes):
        tp = np.sum((pred_matrix == c) & (y_true_int == c), axis=1)
        fp = np.sum((pred_matrix == c) & (y_true_int != c), axis=1)
        fn = np.sum((pred_matrix != c) & (y_true_int == c), axis=1)
        denom = 2 * tp + fp + fn
        f1_c = np.where(denom > 0, 2 * tp / np.maximum(denom, 1), 0.0)
        f1_list.append(f1_c)
    # Average across classes
    macro_f1 = np.mean(f1_list, axis=0) # shape (B,)
    return macro_f1

def fast_paired_permutation_test(y_true_int, pred_a_int, pred_b_int, num_classes=3, n_perm=5000, seed=42):
    rng = np.random.default_rng(seed)
    n = len(y_true_int)
    
    # Observed F1
    f1_a_obs = compute_macro_f1_vectorized(y_true_int, pred_a_int[None, :], num_classes)[0]
    f1_b_obs = compute_macro_f1_vectorized(y_true_int, pred_b_int[None, :], num_classes)[0]
    diff_obs = f1_a_obs - f1_b_obs
    
    # Vectorized permutation: shape (n_perm, n)
    swap = rng.choice([True, False], size=(n_perm, n))
    s_a = np.where(swap, pred_b_int[None, :], pred_a_int[None, :])
    s_b = np.where(swap, pred_a_int[None, :], pred_b_int[None, :])
    
    f1_sa = compute_macro_f1_vectorized(y_true_int, s_a, num_classes)
    f1_sb = compute_macro_f1_vectorized(y_true_int, s_b, num_classes)
    diffs = f1_sa - f1_sb
    
    p_val = float(np.mean(np.abs(diffs) >= np.abs(diff_obs)))
    return float(diff_obs), p_val

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
    
    label2id = {"CONTRADICTED": 0, "INSUFFICIENT_EVIDENCE": 1, "SUPPORTED": 2}
    
    y_true_str = test_df["gold_label"].to_numpy()
    y_true = np.array([label2id[l] for l in y_true_str])
    
    p_trans = np.array([label2id[l] for l in test_df["pred_translated"].to_numpy()])
    p_orig = np.array([label2id[l] for l in test_df["pred_original"].to_numpy()])
    p_always = np.array([label2id[l] for l in test_df["pred_always"].to_numpy()])
    p_sel = np.array([label2id[l] for l in test_df["pred_selective"].to_numpy()])
    p_num = np.array([label2id[l] for l in test_df["pred_ablation_numeral_only"].to_numpy()])
    p_rnd = np.array([label2id[l] for l in test_df["pred_control_random_routing"].to_numpy()])
    
    print("=== DATASET COUNTS ===", flush=True)
    print(f"Dev instances: {len(dev_df)}", flush=True)
    print(f"Dev counts: {dev_df['gold_label'].value_counts().to_dict()}", flush=True)
    print(f"Test instances: {len(test_df)}", flush=True)
    print(f"Test counts: {test_df['gold_label'].value_counts().to_dict()}", flush=True)
    
    print("\n=== AGREEMENT AND DISAGREEMENT ===", flush=True)
    agr = np.sum(p_trans == p_orig)
    disagr = np.sum(p_trans != p_orig)
    w_lo, w_hi = wilson_ci(disagr, 163)
    print(f"Agr: {agr}/163 ({agr/163*100:.2f}%), Disagr: {disagr}/163 ({disagr/163*100:.2f}%)", flush=True)
    print(f"Disagreement 95% Wilson CI: [{w_lo*100:.2f}%, {w_hi*100:.2f}%]", flush=True)
    
    print("\n=== TRANSITION MATRIX ===", flush=True)
    cm = confusion_matrix(p_trans, p_orig, labels=[0, 1, 2])
    # [0: Contra, 1: Insuff, 2: Supp]
    print(cm, flush=True)
    supp_to_contra = cm[2, 0]
    total_supp_trans = np.sum(cm[2, :])
    sw_lo, sw_hi = wilson_ci(supp_to_contra, total_supp_trans)
    print(f"Supp -> Contra: {supp_to_contra}/{total_supp_trans} ({supp_to_contra/total_supp_trans*100:.2f}%), CI: [{sw_lo*100:.2f}%, {sw_hi*100:.2f}%]", flush=True)
    
    contra_to_supp = cm[0, 2]
    total_contra_trans = np.sum(cm[0, :])
    cw_lo, cw_hi = wilson_ci(contra_to_supp, total_contra_trans)
    print(f"Contra -> Supp: {contra_to_supp}/{total_contra_trans} ({contra_to_supp/total_contra_trans*100:.2f}%), CI: [{cw_lo*100:.2f}%, {cw_hi*100:.2f}%]", flush=True)
    
    print("\n=== SYSTEM PERFORMANCE ===", flush=True)
    sys_dict = {
        "No-Check (Translated)": p_trans,
        "Direct Multilingual (Original)": p_orig,
        "Always-Check (Dual Consensus)": p_always,
        "Selective-Check (Hard Route)": p_sel,
        "Ablation: Numeral-Only": p_num,
        "Control: Random Routing": p_rnd
    }
    for name, pred in sys_dict.items():
        corr = int(np.sum(pred == y_true))
        acc = corr / 163
        wlo, whi = wilson_ci(corr, 163)
        f1_3 = compute_macro_f1_vectorized(y_true, pred[None, :], num_classes=3)[0]
        # 2-class Macro F1: evaluate over classes 0 and 1
        tp0 = np.sum((pred == 0) & (y_true == 0))
        fp0 = np.sum((pred == 0) & (y_true != 0))
        fn0 = np.sum((pred != 0) & (y_true == 0))
        f1_c0 = 2 * tp0 / (2 * tp0 + fp0 + fn0) if (2 * tp0 + fp0 + fn0) > 0 else 0.0
        
        tp1 = np.sum((pred == 1) & (y_true == 1))
        fp1 = np.sum((pred == 1) & (y_true != 1))
        fn1 = np.sum((pred != 1) & (y_true == 1))
        f1_c1 = 2 * tp1 / (2 * tp1 + fp1 + fn1) if (2 * tp1 + fp1 + fn1) > 0 else 0.0
        f1_2 = (f1_c0 + f1_c1) / 2.0
        print(f"{name:<32} Acc: {acc:.4f} [{wlo:.4f}, {whi:.4f}] ({corr}/163) | F1_3cl: {f1_3:.4f} | F1_2cl: {f1_2:.4f} | F1_Contra: {f1_c0:.4f} | F1_Neutral: {f1_c1:.4f}", flush=True)
        
    print("\n=== PAIRED TESTS ===", flush=True)
    test_pairs = [
        ("No-Check vs Direct Multilingual", p_trans, p_orig),
        ("Selective-Check vs Direct Multilingual", p_sel, p_orig),
        ("Selective-Check vs Always-Check", p_sel, p_always),
        ("Selective-Check vs No-Check", p_sel, p_trans),
        ("Selective-Check vs Random Routing", p_sel, p_rnd),
        ("Selective-Check vs Numeral-Only", p_sel, p_num),
    ]
    raw_mcnemar_p = []
    raw_perm_3cl_p = []
    
    out_rows = []
    for pair_name, pr_a, pr_b in test_pairs:
        stat, p_asymp, p_exact, b, c = mcnemar_calc(y_true, pr_a, pr_b)
        delta_3, perm_p3 = fast_paired_permutation_test(y_true, pr_a, pr_b, num_classes=3, n_perm=5000, seed=42)
        raw_mcnemar_p.append(p_exact)
        raw_perm_3cl_p.append(perm_p3)
        out_rows.append({
            "Pair": pair_name,
            "b": b,
            "c": c,
            "n_disc": b + c,
            "McNemar_Stat": stat,
            "p_asymp": p_asymp,
            "p_exact": p_exact,
            "delta_3": delta_3,
            "perm_p3": perm_p3
        })
    fdr_mcnemar = bh_fdr_correction(raw_mcnemar_p)
    fdr_perm = bh_fdr_correction(raw_perm_3cl_p)
    
    for idx, row in enumerate(out_rows):
        print(f"{row['Pair']:<40} b={row['b']:<2} c={row['c']:<2} chi2={row['McNemar_Stat']:<7.4f} asymp_p={row['p_asymp']:<8.6f} exact_p={row['p_exact']:<8.6f} (FDR={fdr_mcnemar[idx]:<8.6f}) | DeltaF1={row['delta_3']:<8.4f} perm_p={row['perm_p3']:<8.5f} (FDR={fdr_perm[idx]:<8.5f})", flush=True)

if __name__ == "__main__":
    main()
