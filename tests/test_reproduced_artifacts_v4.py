"""
Comprehensive verification test suite for V4 canonical research artifacts.
Validates:
1. Exact split counts, unique item IDs, zero train/dev/test leakage.
2. Direct MT generation presence, token truncation bounds (max 512).
3. Softmax probabilities sum to 1.0.
4. Mathematical consistency of threshold: selective_triggered == (risk_score >= tau_star).
5. Exact latency arithmetic across stages.
6. Multi-seed random control properties (100 seeds, exact matched item count).
7. Benchmark table reconciliation against raw per-instance test predictions.
8. Benjamini-Hochberg FDR correction validity.
"""
import sys
import unittest
import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score, f1_score

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class TestReproducedArtifactsV4(unittest.TestCase):
    def setUp(self):
        self.res_dir = PROJECT_ROOT / "experiments" / "results_corrected"
        self.dev_preds_path = self.res_dir / "canonical_dev_predictions.csv"
        self.test_preds_path = self.res_dir / "canonical_test_predictions.csv"
        self.tuning_path = self.res_dir / "canonical_dev_tuning.csv"
        self.benchmark_path = self.res_dir / "canonical_benchmark_table.csv"
        self.stat_path = self.res_dir / "canonical_statistical_tests.csv"
        self.random_path = self.res_dir / "canonical_random_control_100seeds.csv"
        self.strata_path = self.res_dir / "canonical_error_attribution.json"
        self.latency_path = self.res_dir / "canonical_latency_summary.json"

    def test_file_existence_and_split_integrity(self):
        self.assertTrue(self.dev_preds_path.exists(), "canonical_dev_predictions.csv must exist")
        self.assertTrue(self.test_preds_path.exists(), "canonical_test_predictions.csv must exist")

        dev_df = pd.read_csv(self.dev_preds_path)
        test_df = pd.read_csv(self.test_preds_path)

        self.assertEqual(len(dev_df), 103, "Dev split must contain exactly 103 items")
        self.assertEqual(len(test_df), 163, "Test split must contain exactly 163 items")

        # Item ID uniqueness and zero split overlap
        self.assertEqual(len(dev_df["item_id"].unique()), 103)
        self.assertEqual(len(test_df["item_id"].unique()), 163)
        dev_ids = set(dev_df["item_id"])
        test_ids = set(test_df["item_id"])
        self.assertEqual(len(dev_ids.intersection(test_ids)), 0, "Zero item leakage between dev and test")

    def test_mt_generation_and_token_bounds(self):
        test_df = pd.read_csv(self.test_preds_path)
        self.assertIn("gen_translated_evidence", test_df.columns, "Generated translation text must be saved")
        self.assertTrue((test_df["gen_translated_evidence"].str.len() > 0).all(), "Translations cannot be empty")

        # Token bounds
        self.assertTrue((test_df["trans_token_length"] <= 512).all())
        self.assertTrue((test_df["orig_token_length"] <= 512).all())
        self.assertTrue(set(test_df["trans_is_truncated"].unique()).issubset({0, 1}))
        self.assertTrue(set(test_df["orig_is_truncated"].unique()).issubset({0, 1}))

    def test_probabilities_sum_to_one(self):
        test_df = pd.read_csv(self.test_preds_path)
        p_trans_sum = test_df["p_trans_supp"] + test_df["p_trans_insuff"] + test_df["p_trans_contra"]
        p_orig_sum = test_df["p_orig_supp"] + test_df["p_orig_insuff"] + test_df["p_orig_contra"]
        p_always_sum = test_df["p_always_supp"] + test_df["p_always_insuff"] + test_df["p_always_contra"]

        np.testing.assert_allclose(p_trans_sum.values, 1.0, atol=1e-3, err_msg="p_trans must sum to 1.0")
        np.testing.assert_allclose(p_orig_sum.values, 1.0, atol=1e-3, err_msg="p_orig must sum to 1.0")
        np.testing.assert_allclose(p_always_sum.values, 1.0, atol=1e-3, err_msg="p_always must sum to 1.0")

    def test_threshold_selection_and_trigger_consistency(self):
        self.assertTrue(self.tuning_path.exists())
        tuning_df = pd.read_csv(self.tuning_path)

        # Derive tau* mechanically
        best_row = tuning_df.sort_values(by=["tradeoff_score", "coverage"], ascending=[False, True]).iloc[0]
        tau_star = round(float(best_row["tau"]), 3)

        test_df = pd.read_csv(self.test_preds_path)
        expected_trig = (test_df["risk_score"] >= tau_star).astype(int)
        self.assertTrue(
            (test_df["selective_triggered"] == expected_trig).all(),
            f"Every test row selective_triggered must equal (risk_score >= {tau_star})"
        )

    def test_latency_arithmetic_consistency(self):
        test_df = pd.read_csv(self.test_preds_path)
        # Trans E2E = MT + Trans verifier
        np.testing.assert_allclose(
            test_df["latency_trans_e2e_ms"].values,
            test_df["latency_mt_ms"].values + test_df["latency_trans_ms"].values,
            atol=1e-1
        )
        # Always E2E = MT + Trans verifier + Orig verifier
        np.testing.assert_allclose(
            test_df["latency_always_e2e_ms"].values,
            test_df["latency_mt_ms"].values + test_df["latency_trans_ms"].values + test_df["latency_orig_ms"].values,
            atol=1e-1
        )
        # Selective E2E matches routing
        sel_lat_expected = np.where(
            test_df["selective_triggered"] == 1,
            test_df["latency_always_e2e_ms"],
            test_df["latency_trans_e2e_ms"]
        )
        np.testing.assert_allclose(test_df["latency_selective_e2e_ms"].values, sel_lat_expected, atol=1e-1)

    def test_multiseed_random_control_properties(self):
        self.assertTrue(self.random_path.exists())
        r_df = pd.read_csv(self.random_path)
        self.assertEqual(len(r_df), 100, "Random control must be evaluated across exactly 100 seeds")
        self.assertEqual(list(r_df["seed"]), list(range(100)))

        # All seeds must trigger the EXACT same matched count
        k_expected = r_df["k_triggered"].iloc[0]
        self.assertTrue((r_df["k_triggered"] == k_expected).all(), "Exact matched count must hold across all seeds")

    def test_benchmark_reconciliation(self):
        self.assertTrue(self.benchmark_path.exists())
        bench_df = pd.read_csv(self.benchmark_path)
        test_df = pd.read_csv(self.test_preds_path)
        yt = test_df["gold_label"].values

        # Check No-Check
        no_check_row = bench_df[bench_df["System / Ablation"].str.contains("No-Check")].iloc[0]
        acc_recomp = accuracy_score(yt, test_df["pred_translated"].values)
        self.assertAlmostEqual(float(no_check_row["Accuracy"]), round(acc_recomp, 4))

        # Check Selective-Check
        sel_row = bench_df[bench_df["System / Ablation"].str.contains("Selective-Check")].iloc[0]
        acc_sel_recomp = accuracy_score(yt, test_df["pred_selective"].values)
        self.assertAlmostEqual(float(sel_row["Accuracy"]), round(acc_sel_recomp, 4))

    def test_fdr_adjusted_p_values(self):
        self.assertTrue(self.stat_path.exists())
        stat_df = pd.read_csv(self.stat_path)
        self.assertIn("McNemar_p_val_fdr", stat_df.columns)
        self.assertIn("Permutation_p_val_3cl_fdr", stat_df.columns)
        self.assertTrue((stat_df["McNemar_p_val_fdr"] >= stat_df["McNemar_p_val_raw"]).all())
        self.assertTrue((stat_df["Permutation_p_val_3cl_fdr"] >= stat_df["Permutation_p_val_3cl_raw"]).all())

if __name__ == "__main__":
    unittest.main()
