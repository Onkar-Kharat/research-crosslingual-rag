"""Summarize predictions from a CSV with gold_label, condition, predicted_label columns."""
import argparse
from pathlib import Path
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, classification_report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("csv_path")
    p.add_argument("--out",default="reports/prediction_summary.txt")
    a=p.parse_args()
    df=pd.read_csv(a.csv_path)
    required={"gold_label","condition","predicted_label"}
    if not required.issubset(df.columns):
        raise SystemExit(f"Missing columns: {sorted(required-set(df.columns))}")
    chunks=[]
    for condition,sub in df.groupby("condition"):
        sub=sub.dropna(subset=["gold_label","predicted_label"])
        chunks += [f"## {condition}\nN={len(sub)}",
          f"Accuracy={accuracy_score(sub.gold_label,sub.predicted_label):.4f}",
          f"Macro-F1={f1_score(sub.gold_label,sub.predicted_label,average='macro',zero_division=0):.4f}",
          classification_report(sub.gold_label,sub.predicted_label,zero_division=0)]
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text("\n\n".join(chunks),encoding="utf-8")
    print(f"Wrote {out}")
if __name__=="__main__": main()
