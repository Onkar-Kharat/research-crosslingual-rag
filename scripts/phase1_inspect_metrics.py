import csv
import json
import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter
from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support, confusion_matrix

WORKSPACE = Path(__file__).resolve().parents[1]

def audit_predictions_and_metrics():
    print("=== AUDIT TEST PREDICTIONS AND METRICS ===")
    preds_path = WORKSPACE / "experiments" / "results" / "test_predictions.csv"
    df = pd.read_csv(preds_path)
    print(f"Total rows in test_predictions.csv: {len(df)}")
    print(f"Gold labels: {Counter(df['gold_label'])}")
    
    systems = [
        ("Translated (No-Check)", "pred_translated"),
        ("Original-Only", "pred_original"),
        ("Always-Check", "pred_always"),
        ("Selective Checking", "pred_selective")
    ]
    
    print("\n--- EXACT OBSERVED POINT ESTIMATES (Test N=163) ---")
    recomputed = []
    for name, col in systems:
        y_true = df["gold_label"]
        y_pred = df[col]
        
        acc = accuracy_score(y_true, y_pred)
        correct_count = (y_true == y_pred).sum()
        
        # 3-class Macro F1 (with SUPPORTED included in classes)
        macro_f1_3class = f1_score(y_true, y_pred, labels=["SUPPORTED", "INSUFFICIENT_EVIDENCE", "CONTRADICTED"], average="macro", zero_division=0)
        # 2-class Macro F1 (only observed classes)
        macro_f1_2class = f1_score(y_true, y_pred, labels=["INSUFFICIENT_EVIDENCE", "CONTRADICTED"], average="macro", zero_division=0)
        
        p, r, f1, s = precision_recall_fscore_support(y_true, y_pred, labels=["SUPPORTED", "INSUFFICIENT_EVIDENCE", "CONTRADICTED"], zero_division=0)
        
        print(f"\n[{name}] ({col}):")
        print(f"  Accuracy: {correct_count}/{len(df)} = {acc:.6f} ({acc*100:.2f}%)")
        print(f"  Macro-F1 (3-class): {macro_f1_3class:.6f}")
        print(f"  Macro-F1 (2-class observed): {macro_f1_2class:.6f}")
        print(f"  Per-class metrics (SUPPORTED, INSUFFICIENT, CONTRADICTED):")
        print(f"    Precision: {p}")
        print(f"    Recall:    {r}")
        print(f"    F1:        {f1}")
        print(f"    Support:   {s}")
        print(f"  Prediction distribution: {Counter(y_pred)}")
        
        recomputed.append({
            "system": name,
            "col": col,
            "correct": correct_count,
            "total": len(df),
            "acc": acc,
            "macro_f1_3class": macro_f1_3class,
            "macro_f1_2class": macro_f1_2class,
            "p_contra": p[2], "r_contra": r[2], "f1_contra": f1[2],
            "p_insuff": p[1], "r_insuff": r[1], "f1_insuff": f1[1],
            "p_supp": p[0], "r_supp": r[0], "f1_supp": f1[0],
        })
        
    rep_path = WORKSPACE / "experiments" / "results" / "test_main_results.csv"
    rep_df = pd.read_csv(rep_path)
    print("\n--- COMPARISON WITH REPORTED IN test_main_results.csv ---")
    for r in recomputed:
        row_rep = rep_df[rep_df["system"].str.contains(r["system"].split()[0])]
        if not row_rep.empty:
            rep_acc = row_rep["accuracy"].values[0]
            rep_f1 = row_rep["macro_f1"].values[0]
            print(f"System: {r['system']}")
            print(f"  Observed Acc: {r['acc']:.6f} vs Reported Acc: {rep_acc:.6f} (Diff: {r['acc'] - rep_acc:+.6f})")
            print(f"  Observed 3-cl F1: {r['macro_f1_3class']:.6f} vs Reported F1: {rep_f1:.6f} (Diff: {r['macro_f1_3class'] - rep_f1:+.6f})")

def audit_error_attribution():
    print("\n=== AUDIT ERROR ATTRIBUTION AND TAXONOMY ===")
    preds_path = WORKSPACE / "experiments" / "results" / "test_predictions.csv"
    df = pd.read_csv(preds_path)
    
    # Analyze the definitions from analyze_predictions.py
    # Let's inspect analyze_predictions.py
    code_path = WORKSPACE / "scripts" / "analyze_predictions.py"
    with open(code_path, "r", encoding="utf-8") as f:
        print("--- scripts/analyze_predictions.py ---")
        print(f.read())

if __name__ == "__main__":
    audit_predictions_and_metrics()
    audit_error_attribution()
