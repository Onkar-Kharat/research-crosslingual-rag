import sys
import unittest
import numpy as np
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

class TestCorrectedPipeline(unittest.TestCase):
    def setUp(self):
        self.res_dir = PROJECT_ROOT / "experiments" / "results_corrected"
        self.dev_preds_path = self.res_dir / "corrected_dev_predictions.csv"
        self.test_preds_path = self.res_dir / "corrected_test_predictions.csv"
        self.dev_tuning_path = self.res_dir / "corrected_dev_tuning.csv"
        self.benchmark_path = self.res_dir / "corrected_full_benchmark_and_ablations.csv"
        self.stat_tests_path = self.res_dir / "corrected_statistical_tests.csv"
        self.lat_summary_path = self.res_dir / "corrected_latency_summary.json"

    def test_prediction_files_exist_and_counts(self):
        self.assertTrue(self.dev_preds_path.exists(), "corrected_dev_predictions.csv must exist")
        self.assertTrue(self.test_preds_path.exists(), "corrected_test_predictions.csv must exist")
        
        dev_df = pd.read_csv(self.dev_preds_path)
        test_df = pd.read_csv(self.test_preds_path)
        
        self.assertEqual(len(dev_df), 103, "Dev predictions must contain exactly 103 items")
        self.assertEqual(len(test_df), 163, "Test predictions must contain exactly 163 items")

    def test_token_truncation_schema(self):
        test_df = pd.read_csv(self.test_preds_path)
        self.assertIn("trans_token_length", test_df.columns)
        self.assertIn("trans_is_truncated", test_df.columns)
        self.assertIn("orig_token_length", test_df.columns)
        self.assertIn("orig_is_truncated", test_df.columns)
        
        # Max token length should not exceed 512
        self.assertTrue((test_df["trans_token_length"] <= 512).all())
        self.assertTrue((test_df["orig_token_length"] <= 512).all())

    def test_real_latencies_measured(self):
        test_df = pd.read_csv(self.test_preds_path)
        # Latencies must be strictly positive floats
        self.assertTrue((test_df["latency_mt_ms"] > 0).all())
        self.assertTrue((test_df["latency_trans_ms"] > 0).all())
        self.assertTrue((test_df["latency_orig_ms"] > 0).all())
        
        # Latencies should not be a single constant (they must vary by instance)
        self.assertGreater(test_df["latency_mt_ms"].std(), 0.0, "MT latency must vary by instance")
        self.assertGreater(test_df["latency_trans_ms"].std(), 0.0, "Verifier latency must vary by instance")
        
        # Check E2E addition
        np.testing.assert_allclose(
            test_df["latency_trans_e2e_ms"].values,
            test_df["latency_mt_ms"].values + test_df["latency_trans_ms"].values,
            atol=1e-1
        )

    def test_tuning_and_ablation_artifacts(self):
        self.assertTrue(self.dev_tuning_path.exists(), "corrected_dev_tuning.csv must exist")
        self.assertTrue(self.benchmark_path.exists(), "corrected_full_benchmark_and_ablations.csv must exist")
        self.assertTrue(self.stat_tests_path.exists(), "corrected_statistical_tests.csv must exist")
        self.assertTrue(self.lat_summary_path.exists(), "corrected_latency_summary.json must exist")
        
        bench_df = pd.read_csv(self.benchmark_path)
        self.assertEqual(len(bench_df), 9, "Benchmark table must contain 9 systems/ablations")
        required_cols = [
            "System / Ablation", "Accuracy", "Acc_95_CI",
            "Macro_F1_3cl", "F1_3cl_95_CI", "Macro_F1_2cl", "F1_2cl_95_CI",
            "Coverage_Pct", "Mean_E2E_Latency_ms"
        ]
        for col in required_cols:
            self.assertIn(col, bench_df.columns)

if __name__ == "__main__":
    unittest.main()
