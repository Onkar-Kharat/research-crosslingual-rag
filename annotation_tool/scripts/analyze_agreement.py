"""
Inter-Rater Agreement and Stratified Error Attribution Analysis.
Processes two independently completed, validated human submissions.
Aligns items via internal_analysis_key.csv, computes raw agreement, Cohen's kappa,
prevalence, multi-label distortion overlap, and exports a clean adjudication queue.
"""
import json
import csv
import sys
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
KEY_PATH = PROJECT_ROOT / "annotation_tool" / "internal_analysis_key.csv"
ANALYSIS_DIR = PROJECT_ROOT / "annotation_tool" / "analysis"

def load_records(filepath: Path) -> Dict[str, Dict]:
    records = {}
    if filepath.suffix.lower() == ".json":
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        for r in data.get("annotations", []):
            records[r["opaque_item_id"]] = r
    elif filepath.suffix.lower() == ".csv":
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                dt = r.get("distortion_types", "")
                r["distortion_types"] = [x.strip() for x in dt.split(";") if x.strip()] if isinstance(dt, str) else dt
                records[r["opaque_item_id"]] = r
    return records

def compute_cohens_kappa(labels1: List[str], labels2: List[str], categories: List[str]) -> Tuple[float, float, Tuple[float, float]]:
    n = len(labels1)
    if n == 0:
        return 0.0, 0.0, (0.0, 0.0)
    
    cat_to_idx = {c: i for i, c in enumerate(categories)}
    k = len(categories)
    cm = np.zeros((k, k), dtype=int)
    for l1, l2 in zip(labels1, labels2):
        if l1 in cat_to_idx and l2 in cat_to_idx:
            cm[cat_to_idx[l1], cat_to_idx[l2]] += 1

    po = np.trace(cm) / n
    row_sums = cm.sum(axis=1) / n
    col_sums = cm.sum(axis=0) / n
    pe = np.sum(row_sums * col_sums)

    if pe >= 1.0:
        kappa = 1.0
    else:
        kappa = (po - pe) / (1.0 - pe)

    # Standard error of kappa (Fleiss et al., 1969)
    se = np.sqrt((po * (1.0 - po)) / (n * ((1.0 - pe) ** 2))) if pe < 1.0 and po < 1.0 else 0.0
    ci_lower = max(-1.0, kappa - 1.959964 * se)
    ci_upper = min(1.0, kappa + 1.959964 * se)
    return float(kappa), float(se), (float(ci_lower), float(ci_upper))

def analyze(sub_a_path: Path, sub_b_path: Path, output_dir: Path = None):
    out_dir = output_dir or ANALYSIS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    assert KEY_PATH.exists(), f"Secret analysis key missing: {KEY_PATH}"
    key_df = pd.read_csv(KEY_PATH)

    recs_a = load_records(sub_a_path)
    recs_b = load_records(sub_b_path)

    assert len(recs_a) == 50, f"Submission A must contain 50 items, got {len(recs_a)}"
    assert len(recs_b) == 50, f"Submission B must contain 50 items, got {len(recs_b)}"

    aligned = []
    for _, krow in key_df.iterrows():
        iid = krow["item_id"]
        opq_a = krow["opaque_item_id_A"]
        opq_b = krow["opaque_item_id_B"]

        assert opq_a in recs_a, f"Item {opq_a} missing from Submission A"
        assert opq_b in recs_b, f"Item {opq_b} missing from Submission B"

        a_data = recs_a[opq_a]
        b_data = recs_b[opq_b]

        aligned.append({
            "item_id": iid,
            "sampling_stratum": krow["sampling_stratum"],
            "gold_label": krow["gold_label"],
            "pred_translated": krow["pred_translated"],
            "pred_original": krow["pred_original"],
            "opaque_id_A": opq_a,
            "fidelity_A": a_data["fidelity_label"],
            "distortions_A": a_data.get("distortion_types", []),
            "rationale_A": a_data.get("rationale", ""),
            "opaque_id_B": opq_b,
            "fidelity_B": b_data["fidelity_label"],
            "distortions_B": b_data.get("distortion_types", []),
            "rationale_B": b_data.get("rationale", ""),
            "is_agreement": a_data["fidelity_label"] == b_data["fidelity_label"]
        })

    aligned_df = pd.DataFrame(aligned)
    aligned_csv = out_dir / "aligned_two_annotator_evaluations.csv"
    aligned_df.to_csv(aligned_csv, index=False)
    print(f"Saved aligned evaluations to {aligned_csv}")

    # Metrics computation
    n = len(aligned_df)
    n_agree = aligned_df["is_agreement"].sum()
    raw_agree = n_agree / n

    categories = ["PRESERVED", "ALTERED", "AMBIGUOUS_SOURCE", "UNABLE_TO_DECIDE"]
    kappa_multi, se_multi, ci_multi = compute_cohens_kappa(
        aligned_df["fidelity_A"].tolist(),
        aligned_df["fidelity_B"].tolist(),
        categories
    )

    # Binary kappa: ALTERED vs NOT_ALTERED
    bin_a = ["ALTERED" if x == "ALTERED" else "NOT_ALTERED" for x in aligned_df["fidelity_A"]]
    bin_b = ["ALTERED" if x == "ALTERED" else "NOT_ALTERED" for x in aligned_df["fidelity_B"]]
    kappa_bin, se_bin, ci_bin = compute_cohens_kappa(bin_a, bin_b, ["ALTERED", "NOT_ALTERED"])

    # Disagreement queue
    disagreements = aligned_df[~aligned_df["is_agreement"]].copy()
    disagree_csv = out_dir / "disagreement_queue_for_adjudication.csv"
    disagreements.to_csv(disagree_csv, index=False)
    print(f"Identified {len(disagreements)} disagreements. Saved queue to {disagree_csv}")

    # Stratum breakdowns
    stratum_summary = []
    for stratum, grp in aligned_df.groupby("sampling_stratum"):
        agreed_altered = grp[(grp["fidelity_A"] == "ALTERED") & (grp["fidelity_B"] == "ALTERED")]
        stratum_summary.append({
            "stratum": stratum,
            "sample_size": len(grp),
            "annotator_A_altered": (grp["fidelity_A"] == "ALTERED").sum(),
            "annotator_B_altered": (grp["fidelity_B"] == "ALTERED").sum(),
            "both_agreed_altered": len(agreed_altered),
            "agreed_rate": len(agreed_altered) / len(grp)
        })
    stratum_df = pd.DataFrame(stratum_summary)
    stratum_csv = out_dir / "stratum_breakdown_summary.csv"
    stratum_df.to_csv(stratum_csv, index=False)

    # Markdown report
    report_lines = [
        "# Authentic Bilingual Human Annotation Analysis Report",
        "",
        f"- **Items Evaluated:** {n}",
        f"- **Annotators:** {recs_a[list(recs_a.keys())[0]].get('annotator_code', 'A1')} and {recs_b[list(recs_b.keys())[0]].get('annotator_code', 'A2')}",
        f"- **Raw Percentage Agreement:** {raw_agree*100:.2f}% ({n_agree}/{n})",
        f"- **4-Way Cohen's Kappa:** {kappa_multi:.4f} [95% CI: {ci_multi[0]:.4f}, {ci_multi[1]:.4f}] (SE: {se_multi:.4f})",
        f"- **Binary Cohen's Kappa (ALTERED vs Other):** {kappa_bin:.4f} [95% CI: {ci_bin[0]:.4f}, {ci_bin[1]:.4f}]",
        f"- **Disagreements Requiring Adjudication:** {len(disagreements)} / {n}",
        "",
        "## Label Prevalence",
        f"- **Annotator A:** {pd.Series(aligned_df['fidelity_A']).value_counts().to_dict()}",
        f"- **Annotator B:** {pd.Series(aligned_df['fidelity_B']).value_counts().to_dict()}",
        "",
        "## Stratum Breakdown",
        stratum_df.to_markdown(index=False),
        "",
        "## Next Actions",
        "1. For any item in `disagreement_queue_for_adjudication.csv`, have a third expert adjudicator assign consensus.",
        "2. Compute post-stratification weighted population prevalence of translation errors."
    ]
    report_path = out_dir / "HUMAN_ANNOTATION_AGREEMENT_REPORT.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Generated agreement report at {report_path}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python analyze_agreement.py <submission_A> <submission_B> [output_dir]")
        sys.exit(1)
    sub_a = Path(sys.argv[1])
    sub_b = Path(sys.argv[2])
    out_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    analyze(sub_a, sub_b, out_dir)

if __name__ == "__main__":
    main()
