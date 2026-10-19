import sys
import json
import pandas as pd
import numpy as np
import scipy.stats as stats
from pathlib import Path
from sklearn.metrics import accuracy_score, f1_score

WORKSPACE = Path(r"c:\Users\Onkar\OneDrive\Desktop\Research_crosslingual_rag_research")
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))

WORKSPACE = Path(r"c:\Users\Onkar\OneDrive\Desktop\Research_crosslingual_rag_research")
OUT_DIR = WORKSPACE / "experiments" / "results_corrected"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MEAN_MT_LATENCY_MS = 1120.0

def generate_ablations():
    df = pd.read_csv(WORKSPACE / "experiments" / "results" / "test_predictions.csv")
    test_jsonl = WORKSPACE / "data" / "processed" / "test_translated.jsonl"
    items = {d["item_id"]: d for d in [json.loads(line) for line in open(test_jsonl, encoding="utf-8")]}
    
    # Calculate True Jaccard for all items
    from scripts.run_corrected_experiments import compute_numeral_jaccard, compute_risk
    jaccards = []
    risks_corr = []
    for _, r in df.iterrows():
        d = items[r["item_id"]]
        j = compute_numeral_jaccard(d["original_evidence"], d.get("translated_evidence", ""))
        jaccards.append(j)
        probs = np.array([r["p_trans_supp"], r["p_trans_insuff"], r["p_trans_contra"]])
        risks_corr.append(compute_risk(probs, j))
        
    df["feature_number_jaccard"] = jaccards
    df["risk_corrected"] = risks_corr
    
    yt = df["gold_label"].values
    labels_3cl = ["SUPPORTED", "INSUFFICIENT_EVIDENCE", "CONTRADICTED"]
    labels_2cl = ["INSUFFICIENT_EVIDENCE", "CONTRADICTED"]
    
    # Latencies
    lat_trans_e2e = df["latency_trans_ms"].values + MEAN_MT_LATENCY_MS
    lat_orig = df["latency_orig_ms"].values
    lat_always_e2e = df["latency_always_ms"].values + MEAN_MT_LATENCY_MS
    
    # Selective trigger
    tau = 0.30
    trig_sel = df["risk_corrected"].values >= tau
    cov_sel = float(trig_sel.mean() * 100.0)
    lat_sel_e2e = np.where(trig_sel, lat_always_e2e, lat_trans_e2e)
    
    # 1. No-Check
    pred_no_check = df["pred_translated"].values
    # 2. Direct Multilingual
    pred_direct = df["pred_original"].values
    # 3. Always-Check
    pred_always = df["pred_always"].values
    # 4. Selective-Check (Ours, Hard Routing)
    pred_selective = np.where(trig_sel, pred_direct, pred_no_check)
    
    # 5. Ablation: Triggered Posterior Averaging (paper Eq 1 text)
    p_trans = df[["p_trans_supp", "p_trans_insuff", "p_trans_contra"]].values
    p_orig = df[["p_orig_supp", "p_orig_insuff", "p_orig_contra"]].values
    p_avg = 0.5 * (p_trans + p_orig)
    pred_avg_all = [labels_3cl[i] for i in np.argmax(p_avg, axis=1)]
    pred_ablation_trig_avg = np.where(trig_sel, pred_avg_all, pred_no_check)
    
    # 6. Ablation: Uncertainty-Only Routing (matching coverage 83.4%)
    uncert = 1.0 - df["conf_translated"].values
    tau_u = float(np.percentile(uncert, (1.0 - trig_sel.mean()) * 100))
    trig_u = uncert >= tau_u
    pred_ablation_uncert = np.where(trig_u, pred_direct, pred_no_check)
    lat_uncert = np.where(trig_u, lat_always_e2e, lat_trans_e2e)
    
    # 7. Ablation: Numeral-Only Routing (mismatch > 0)
    trig_num = np.array(jaccards) < 1.0
    pred_ablation_num = np.where(trig_num, pred_direct, pred_no_check)
    cov_num = float(trig_num.mean() * 100.0)
    lat_num = np.where(trig_num, lat_always_e2e, lat_trans_e2e)
    
    # 8. Control: Random Routing (mean across 100 seeds at 83.4% coverage)
    rand_accs = []
    rand_f1_3s = []
    rand_f1_2s = []
    for seed in range(100):
        rng = np.random.default_rng(seed)
        r_trig = rng.random(len(df)) < trig_sel.mean()
        p_rand = np.where(r_trig, pred_direct, pred_no_check)
        rand_accs.append(accuracy_score(yt, p_rand))
        rand_f1_3s.append(f1_score(yt, p_rand, labels=labels_3cl, average="macro", zero_division=0))
        rand_f1_2s.append(f1_score(yt, p_rand, labels=labels_2cl, average="macro", zero_division=0))
        
    # 9. Oracle Upper Bound
    pred_oracle = np.where(pred_direct == yt, pred_direct, pred_no_check)
    
    systems = [
        ("No-Check (Translated Evidence Only)", pred_no_check, 0.0, lat_trans_e2e),
        ("Direct Multilingual (Original Hindi Only)", pred_direct, 100.0, lat_orig),
        ("Always-Check (Dual Consensus via 0.5 Avg)", pred_always, 100.0, lat_always_e2e),
        ("Selective-Check (Ours: Hard Routing, tau*=0.30)", pred_selective, cov_sel, lat_sel_e2e),
        ("Ablation 1: Triggered Posterior Averaging (Paper Eq 1)", pred_ablation_trig_avg, cov_sel, lat_sel_e2e),
        ("Ablation 2: Uncertainty-Only Routing", pred_ablation_uncert, float(trig_u.mean()*100), lat_uncert),
        ("Ablation 3: Numeral-Mismatch-Only Routing", pred_ablation_num, cov_num, lat_num),
        ("Control: Random Routing (83.4% Coverage, 100 seeds)", None, cov_sel, lat_sel_e2e),
        ("Oracle Upper Bound (Non-Deployable Ceiling)", pred_oracle, 100.0, lat_always_e2e)
    ]
    
    out_rows = []
    for name, yp, cov, lats in systems:
        if name.startswith("Control: Random"):
            acc = float(np.mean(rand_accs))
            f1_3 = float(np.mean(rand_f1_3s))
            f1_2 = float(np.mean(rand_f1_2s))
            corr = int(round(acc * len(yt)))
        else:
            acc = float(accuracy_score(yt, yp))
            f1_3 = float(f1_score(yt, yp, labels=labels_3cl, average="macro", zero_division=0))
            f1_2 = float(f1_score(yt, yp, labels=labels_2cl, average="macro", zero_division=0))
            corr = int(np.sum(yp == yt))
            
        out_rows.append({
            "System_or_Ablation": name,
            "Correct_Count": corr,
            "Accuracy": acc,
            "Observed_2cl_Macro_F1": f1_2,
            "Standard_3cl_Macro_F1": f1_3,
            "Coverage_Pct": round(cov, 1),
            "Mean_E2E_Latency_ms": round(float(np.mean(lats)), 1),
            "Median_E2E_Latency_ms": round(float(np.median(lats)), 1)
        })
        
    out_df = pd.DataFrame(out_rows)
    out_csv = OUT_DIR / "full_benchmark_and_ablations.csv"
    out_df.to_csv(out_csv, index=False)
    print(f"Wrote full benchmark and ablations table to {out_csv}")
    
    # Write simple Markdown table
    header = "| " + " | ".join(out_df.columns) + " |"
    sep = "| " + " | ".join(["---"] * len(out_df.columns)) + " |"
    body = "\n".join("| " + " | ".join(str(val) for val in row) + " |" for row in out_df.values)
    md_table = f"{header}\n{sep}\n{body}\n"
    (OUT_DIR / "full_benchmark_and_ablations.md").write_text(md_table, encoding="utf-8")
    print("\n" + md_table)

if __name__ == "__main__":
    generate_ablations()
