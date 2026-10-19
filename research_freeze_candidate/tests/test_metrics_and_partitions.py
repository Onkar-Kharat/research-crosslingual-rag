import sys
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))

import unittest
import numpy as np
import pandas as pd
from scripts.phase1_recompute_all import mcnemar_exact

WORKSPACE = Path(r"c:\Users\Onkar\OneDrive\Desktop\Research_crosslingual_rag_research")

class TestMetricsAndPartitions(unittest.TestCase):
    def setUp(self):
        self.preds_df = pd.read_csv(WORKSPACE / "experiments" / "results" / "test_predictions.csv")
        self.recomputed_df = pd.read_csv(WORKSPACE / "results" / "audit_recomputed" / "recomputed_test_main_results.csv")
        self.error_part_df = pd.read_csv(WORKSPACE / "results" / "audit_recomputed" / "recomputed_error_attribution_disjoint.csv")
        
    def test_observed_accuracy_calculation(self):
        yt = self.preds_df["gold_label"].values
        pt = self.preds_df["pred_translated"].values
        po = self.preds_df["pred_original"].values
        ps = self.preds_df["pred_selective"].values
        
        # Test exact fraction k / N
        self.assertEqual(np.sum(pt == yt), 52)
        self.assertEqual(np.sum(po == yt), 61)
        self.assertEqual(np.sum(ps == yt), 64)
        
        # Check that recomputed table has exact fractions
        no_check_row = self.recomputed_df[self.recomputed_df["condition"].str.contains("No-Check")]
        self.assertAlmostEqual(no_check_row["observed_accuracy"].values[0], 52/163)
        
    def test_disjoint_error_partition(self):
        yt = self.preds_df["gold_label"].values
        pt = self.preds_df["pred_translated"].values
        po = self.preds_df["pred_original"].values
        
        total_errors = np.sum(pt != yt)
        self.assertEqual(total_errors, 111, "Total translation errors must equal 111")
        
        e_trans = np.sum((pt != yt) & (po == yt))
        e_verif = np.sum((pt != yt) & (po != yt) & (yt == "CONTRADICTED"))
        e_insuff = np.sum((pt != yt) & (po != yt) & (yt == "INSUFFICIENT_EVIDENCE"))
        
        # Check disjoint sum
        self.assertEqual(e_trans + e_verif + e_insuff, total_errors, "Partition must sum to exactly 111")
        self.assertEqual(e_trans, 41)
        self.assertEqual(e_verif, 61)
        self.assertEqual(e_insuff, 9)

    def test_mcnemar_exact_properties(self):
        # Discordant pairs: 22 vs 9
        stat, p_val, b, c = mcnemar_exact(
            self.preds_df["gold_label"].values,
            self.preds_df["pred_selective"].values,
            self.preds_df["pred_always"].values
        )
        self.assertEqual(b, 22)
        self.assertEqual(c, 9)
        self.assertAlmostEqual(p_val, 0.029449, places=5)
        self.assertLess(p_val, 0.05, "Selective vs Always-Check must be statistically significant")

if __name__ == "__main__":
    unittest.main()
