import json
import pandas as pd
import numpy as np
import sys
from pathlib import Path
WORKSPACE = Path(r"c:\Users\Onkar\OneDrive\Desktop\Research_crosslingual_rag_research")
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))

from scripts.run_corrected_experiments import compute_numeral_jaccard, compute_risk

WORKSPACE = Path(r"c:\Users\Onkar\OneDrive\Desktop\Research_crosslingual_rag_research")

def test_jaccard_impact():
    df = pd.read_csv(WORKSPACE / "experiments" / "results" / "test_predictions.csv")
    test_jsonl = WORKSPACE / "data" / "processed" / "test_translated.jsonl"
    
    items = {d["item_id"]: d for d in [json.loads(line) for line in open(test_jsonl, encoding="utf-8")]}
    
    jaccards = []
    risks_corr = []
    for _, r in df.iterrows():
        d = items[r["item_id"]]
        j = compute_numeral_jaccard(d["original_evidence"], d.get("translated_evidence", ""))
        jaccards.append(j)
        probs = np.array([r["p_trans_supp"], r["p_trans_insuff"], r["p_trans_contra"]])
        risks_corr.append(compute_risk(probs, j))
        
    df["jaccard_true"] = jaccards
    df["risk_corrected"] = risks_corr
    
    diff_jacc = np.abs(df["feature_number_overlap"] - df["jaccard_true"])
    diff_risk = np.abs(df["risk_score"] - df["risk_corrected"])
    
    print("=== NUMERAL FEATURE AUDIT ===")
    print(f"Stored Recall Overlap Mean: {df['feature_number_overlap'].mean():.4f}")
    print(f"True Jaccard Overlap Mean:  {df['jaccard_true'].mean():.4f}")
    print(f"Items with Jaccard != Recall: {np.sum(diff_jacc > 0.001)} / {len(df)}")
    print(f"Max Jaccard discrepancy: {diff_jacc.max():.4f}")
    print(f"Max Risk discrepancy:    {diff_risk.max():.4f}")
    
    tau = 0.30
    trig_old = df["risk_score"] >= tau
    trig_new = df["risk_corrected"] >= tau
    
    print(f"\nTriggered coverage at tau=0.30: Old={trig_old.sum()}/163 ({trig_old.mean()*100:.1f}%), New={trig_new.sum()}/163 ({trig_new.mean()*100:.1f}%)")
    routing_flips = (trig_old != trig_new).sum()
    print(f"Routing decisions flipped by True Jaccard: {routing_flips}")
    
    yt = df["gold_label"].values
    pred_sel_old = np.where(trig_old, df["pred_original"], df["pred_translated"])
    pred_sel_new = np.where(trig_new, df["pred_original"], df["pred_translated"])
    
    acc_old = (pred_sel_old == yt).mean()
    acc_new = (pred_sel_new == yt).mean()
    print(f"Accuracy with stored risk:   {acc_old*100:.2f}% (64/163)")
    print(f"Accuracy with true Jaccard:  {acc_new*100:.2f}% ({(pred_sel_new == yt).sum()}/163)")

if __name__ == "__main__":
    test_jaccard_impact()
