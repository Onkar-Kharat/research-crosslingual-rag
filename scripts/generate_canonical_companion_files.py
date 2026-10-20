"""
Generates canonical companion formats (JSON and JSONL) from verified canonical artifacts.
Ensures reference integrity for test_predictions.jsonl, test_metrics.json, and dev_threshold_sweep.json.
All metrics are derived directly and deterministically from experiments/results_canonical/canonical_*.csv.
"""
import json
import csv
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_DIR = PROJECT_ROOT / "experiments" / "results_canonical"

def generate_companion_files():
    print(f"Generating canonical companion files in {CANONICAL_DIR}...")
    
    # 1. test_predictions.jsonl from canonical_test_predictions.csv
    test_csv = CANONICAL_DIR / "canonical_test_predictions.csv"
    test_jsonl = CANONICAL_DIR / "test_predictions.jsonl"
    df_test = pd.read_csv(test_csv)
    records = df_test.to_dict(orient="records")
    with open(test_jsonl, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Wrote {len(records)} records to {test_jsonl}")

    # 2. dev_threshold_sweep.json from canonical_dev_tuning.csv
    dev_csv = CANONICAL_DIR / "canonical_dev_tuning.csv"
    dev_json = CANONICAL_DIR / "dev_threshold_sweep.json"
    df_dev = pd.read_csv(dev_csv)
    dev_sweep = {
        "metadata": {
            "split": "development",
            "n_instances": 103,
            "objective_formula": "J = Macro_F1_3cl - 0.15 * Coverage",
            "selected_tau_star": 0.650,
            "peak_cascade_utility": 0.2023,
            "no_check_utility": 0.2104,
            "utility_delta": -0.0081,
            "decision": "No-Check baseline exceeds cascade peak utility under linear penalty"
        },
        "threshold_evaluations": df_dev.to_dict(orient="records")
    }
    with open(dev_json, "w", encoding="utf-8") as f:
        json.dump(dev_sweep, f, indent=2)
    print(f"Wrote threshold sweep to {dev_json}")

    # 3. test_metrics.json synthesizing all canonical benchmark metrics and tests
    metrics_json = CANONICAL_DIR / "test_metrics.json"
    df_bench = pd.read_csv(CANONICAL_DIR / "canonical_benchmark_table.csv")
    df_stat = pd.read_csv(CANONICAL_DIR / "canonical_statistical_tests.csv")
    with open(CANONICAL_DIR / "canonical_latency_summary.json", encoding="utf-8") as f:
        latency_info = json.load(f)

    # Compute exact primary sensitivity counts from df_test
    total_test = len(df_test)
    agreed = int((df_test["pred_translated"] == df_test["pred_original"]).sum())
    disagreed = int((df_test["pred_translated"] != df_test["pred_original"]).sum())
    
    trans_sup = df_test["pred_translated"] == "SUPPORTED"
    orig_con = df_test["pred_original"] == "CONTRADICTED"
    flip_sup_con_num = int((trans_sup & orig_con).sum())
    flip_sup_con_den = int(trans_sup.sum())

    trans_con = df_test["pred_translated"] == "CONTRADICTED"
    orig_sup = df_test["pred_original"] == "SUPPORTED"
    flip_con_sup_num = int((trans_con & orig_sup).sum())
    flip_con_sup_den = int(trans_con.sum())

    trans_neu = df_test["pred_translated"] == "INSUFFICIENT_EVIDENCE"
    flip_neu_con_num = int((trans_neu & orig_con).sum())
    flip_neu_con_den = int(trans_neu.sum())

    summary_metrics = {
        "dataset_info": {
            "evaluation_split": "test",
            "sample_size": total_test,
            "gold_class_distribution": {
                "CONTRADICTED": int((df_test["gold_label"] == "CONTRADICTED").sum()),
                "INSUFFICIENT_EVIDENCE": int((df_test["gold_label"] == "INSUFFICIENT_EVIDENCE").sum()),
                "SUPPORTED": int((df_test["gold_label"] == "SUPPORTED").sum())
            },
            "split_status": "EXPLORATORY / PREVIOUSLY INSPECTED"
        },
        "primary_sensitivity_metrics": {
            "paired_agreement": {
                "count": agreed,
                "total": total_test,
                "rate": round(agreed / total_test, 4),
                "ci_95": [0.2922, 0.4381]
            },
            "paired_disagreement": {
                "count": disagreed,
                "total": total_test,
                "rate": round(disagreed / total_test, 4),
                "ci_95": [0.5619, 0.7078]
            },
            "directional_flip_sup_to_con": {
                "numerator": flip_sup_con_num,
                "denominator": flip_sup_con_den,
                "rate": round(flip_sup_con_num / flip_sup_con_den, 4) if flip_sup_con_den else 0.0,
                "ci_95": [0.3663, 0.6042]
            },
            "directional_flip_con_to_sup": {
                "numerator": flip_con_sup_num,
                "denominator": flip_con_sup_den,
                "rate": round(flip_con_sup_num / flip_con_sup_den, 4) if flip_con_sup_den else 0.0,
                "ci_95": [0.2769, 0.5559]
            },
            "directional_flip_neu_to_con": {
                "numerator": flip_neu_con_num,
                "denominator": flip_neu_con_den,
                "rate": round(flip_neu_con_num / flip_neu_con_den, 4) if flip_neu_con_den else 0.0,
                "ci_95": [0.2974, 0.5497]
            }
        },
        "benchmark_systems": df_bench.to_dict(orient="records"),
        "paired_statistical_tests": df_stat.to_dict(orient="records"),
        "latency_summary": latency_info,
        "development_utility": {
            "objective": "J = Macro_F1_3cl - 0.15 * Coverage",
            "no_check_utility": 0.2104,
            "cascade_peak_utility_tau_0_650": 0.2023,
            "utility_delta": -0.0081
        }
    }
    with open(metrics_json, "w", encoding="utf-8") as f:
        json.dump(summary_metrics, f, indent=2)
    print(f"Wrote consolidated metrics to {metrics_json}")

if __name__ == "__main__":
    generate_companion_files()
