"""
Analyze bilingual human annotations for translation fidelity.
Computes raw agreement, Cohen's Kappa, Krippendorff's alpha (if available),
adjudication rates, and cross-tabulation against operational error strata.
"""
import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import cohen_kappa_score, confusion_matrix

def analyze_annotations(csv_path: Path, key_path: Path, out_report: Path):
    df = pd.read_csv(csv_path)
    
    # Check if annotator columns are filled
    a1_filled = [x for x in df["Annotator_1_Fidelity"].fillna("").astype(str).str.strip() if x]
    a2_filled = [x for x in df["Annotator_2_Fidelity"].fillna("").astype(str).str.strip() if x]
    
    if len(a1_filled) < len(df) or len(a2_filled) < len(df):
        print(f"STATUS: Annotation sheet contains {len(a1_filled)}/{len(df)} entries for A1 and {len(a2_filled)}/{len(df)} for A2.")
        print("Awaiting full human completion. Cannot compute agreement until completed.")
        report_text = (
            "# Human Annotation Audit Status: INCOMPLETE\n\n"
            f"- Total items in sample: {len(df)}\n"
            f"- Annotator 1 completed: {len(a1_filled)}\n"
            f"- Annotator 2 completed: {len(a2_filled)}\n"
            "- Status: BLOCKED ON HUMAN ANNOTATION (NOT FROZEN)\n\n"
            "Please complete all 50 items in `annotation/blinded_annotation_sample.csv` "
            "following `annotation/ANNOTATION_GUIDE.md`.\n"
        )
        out_report.write_text(report_text, encoding="utf-8")
        return False
        
    print("Computing inter-rater agreement statistics...")
    a1 = a1_filled.to_numpy()
    a2 = a2_filled.to_numpy()
    
    raw_agreement = np.mean(a1 == a2)
    kappa = cohen_kappa_score(a1, a2)
    
    # Adjudication consensus
    consensus = df["Adjudication_Consensus"].fillna(df["Annotator_1_Fidelity"]).to_numpy()
    
    key_df = pd.read_csv(key_path)
    merged = df.merge(key_df, on="Sample_ID")
    
    # Stratum validation
    e_trans_subset = merged[merged["Sampling_Stratum"].str.contains("E_trans")]
    e_trans_altered_rate = (e_trans_subset["Adjudication_Consensus"] == "ALTERED").mean()
    
    report_lines = [
        "# Human Annotation Inter-Rater Agreement and Validation Report",
        "",
        f"- **Sample Size:** {len(df)} items",
        f"- **Raw Percentage Agreement:** {raw_agreement*100:.2f}%",
        f"- **Cohen's Kappa (κ):** {kappa:.4f}",
        f"- **Operational E_trans Validation Rate (Marked ALTERED):** {e_trans_altered_rate*100:.2f}%",
        "",
        "## Cross-Tabulation: Human Consensus vs. Operational Strata",
        "",
        pd.crosstab(merged["Sampling_Stratum"], merged["Adjudication_Consensus"]).to_markdown(),
        ""
    ]
    
    out_report.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Wrote agreement report to {out_report}")
    return True

if __name__ == "__main__":
    csv_file = Path("annotation/blinded_annotation_sample.csv")
    key_file = Path("annotation/internal_audit_sampling_key.csv")
    report_file = Path("annotation/HUMAN_ANNOTATION_REPORT.md")
    analyze_annotations(csv_file, key_file, report_file)
