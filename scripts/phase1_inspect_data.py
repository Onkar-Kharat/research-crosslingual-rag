import os
import json
import csv
import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter

WORKSPACE = Path(__file__).resolve().parents[1]

def audit_raw_xfact():
    print("=== AUDIT RAW X-FACT DATA ===")
    dev_path = WORKSPACE / "data" / "raw" / "dev.all.tsv"
    test_path = WORKSPACE / "data" / "raw" / "test.all.tsv"
    
    # Read TSVs
    # X-Fact columns usually: language, site, claim, claim_date, review_date, label, url, evidence_1, ...
    dev_df = pd.read_csv(dev_path, sep="\t", quoting=csv.QUOTE_MINIMAL, on_bad_lines="skip")
    test_df = pd.read_csv(test_path, sep="\t", quoting=csv.QUOTE_MINIMAL, on_bad_lines="skip")
    
    print(f"dev.all.tsv shape: {dev_df.shape}, columns: {list(dev_df.columns[:8])}")
    print(f"test.all.tsv shape: {test_df.shape}, columns: {list(test_df.columns[:8])}")
    
    # Check languages
    lang_col = "language" if "language" in dev_df.columns else dev_df.columns[0]
    label_col = "label" if "label" in dev_df.columns else dev_df.columns[5]
    
    dev_hi = dev_df[dev_df[lang_col] == "hi"]
    test_hi = test_df[test_df[lang_col] == "hi"]
    
    print(f"dev Hindi rows: {len(dev_hi)}, labels: {Counter(dev_hi[label_col])}")
    print(f"test Hindi rows: {len(test_hi)}, labels: {Counter(test_hi[label_col])}")
    
    return dev_hi, test_hi

def audit_processed_data():
    print("\n=== AUDIT PROCESSED DATA ===")
    dev_proc = WORKSPACE / "data" / "processed" / "dev.jsonl"
    test_proc = WORKSPACE / "data" / "processed" / "test.jsonl"
    
    dev_rows = [json.loads(line) for line in open(dev_proc, encoding="utf-8")]
    test_rows = [json.loads(line) for line in open(test_proc, encoding="utf-8")]
    
    print(f"dev.jsonl rows: {len(dev_rows)}")
    dev_labels = Counter(r.get("label") or r.get("veracity_label") or r.get("gold_label") for r in dev_rows)
    print(f"dev.jsonl labels: {dev_labels}")
    
    print(f"test.jsonl rows: {len(test_rows)}")
    test_labels = Counter(r.get("label") or r.get("veracity_label") or r.get("gold_label") for r in test_rows)
    print(f"test.jsonl labels: {test_labels}")
    
    print(f"Sample test row keys: {list(test_rows[0].keys())}")
    print(f"Sample test row labels: raw='{test_rows[0].get('raw_label')}', mapped='{test_rows[0].get('label')}'")

def audit_predictions_and_metrics():
    print("\n=== AUDIT TEST PREDICTIONS ===")
    preds_path = WORKSPACE / "experiments" / "results" / "test_predictions.csv"
    df = pd.read_csv(preds_path)
    print(f"test_predictions.csv shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    print(f"Gold label counts: {Counter(df['gold_label'])}")
    
    # Systems to evaluate:
    systems = {
        "No-Check (Trans)": "pred_trans",
        "Original-Only": "pred_orig",
        "Always-Check": "pred_orig", # wait, what was Always-Check in code?
        "Selective Checking": "pred_selective"
    }
    
    for name, col in [("Trans (No-Check)", "pred_trans"), ("Original", "pred_orig"), ("Selective", "pred_selective")]:
        acc = (df[col] == df['gold_label']).mean()
        corr_cnt = (df[col] == df['gold_label']).sum()
        print(f"{name} Observed Accuracy: {corr_cnt}/{len(df)} = {acc:.6f}")
        
    # Check reported results in test_main_results.csv
    rep_path = WORKSPACE / "experiments" / "results" / "test_main_results.csv"
    rep_df = pd.read_csv(rep_path)
    print("\nReported in test_main_results.csv:")
    print(rep_df[["system", "accuracy", "ci_acc_lower", "ci_acc_upper", "macro_f1", "coverage", "latency_ms"]])
    
    # Error attribution audit
    err_path = WORKSPACE / "experiments" / "results" / "test_error_attribution.csv"
    err_df = pd.read_csv(err_path)
    print("\nReported in test_error_attribution.csv:")
    print(err_df)
    
    # Trace error attribution logic:
    # An example is an error for Trans if pred_trans != gold_label
    trans_errors = df[df["pred_trans"] != df["gold_label"]]
    print(f"Total Trans errors: {len(trans_errors)} / {len(df)}")
    
    # How did analyze_predictions.py classify them?
    # Let's inspect how analyze_predictions defines E_trans, E_verif, E_insuff
    return df

if __name__ == "__main__":
    audit_raw_xfact()
    audit_processed_data()
    audit_predictions_and_metrics()
