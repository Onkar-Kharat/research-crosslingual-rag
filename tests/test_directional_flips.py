import json
import unittest
from pathlib import Path
import pandas as pd
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

class TestDirectionalFlips(unittest.TestCase):
    """
    Automated regression and integrity test that derives directional transition counts
    and rates directly from per-instance model predictions on the canonical test split (N=163)
    and strictly asserts exact parity with all canonical summary tables.
    """
    def setUp(self):
        self.preds_path = PROJECT_ROOT / "experiments" / "results_canonical" / "canonical_test_predictions.csv"
        self.canonical_results_path = PROJECT_ROOT / "canonical_results.csv"
        self.metrics_json_path = PROJECT_ROOT / "experiments" / "results_canonical" / "test_metrics.json"
        self.results_index_path = PROJECT_ROOT / "REVIEWER_HANDOFF" / "FINAL_RESULTS_INDEX.csv"
        
        self.assertTrue(self.preds_path.exists(), f"Missing {self.preds_path}")
        self.assertTrue(self.canonical_results_path.exists(), f"Missing {self.canonical_results_path}")
        self.assertTrue(self.metrics_json_path.exists(), f"Missing {self.metrics_json_path}")
        self.assertTrue(self.results_index_path.exists(), f"Missing {self.results_index_path}")
        
        self.df_preds = pd.read_csv(self.preds_path)
        self.df_canonical = pd.read_csv(self.canonical_results_path)
        with open(self.metrics_json_path, encoding="utf-8") as f:
            self.metrics_json = json.load(f)
        self.df_index = pd.read_csv(self.results_index_path)

    def test_per_instance_transition_matrix_derivation(self):
        """Recomputes complete 3x3 transition matrix directly from test predictions."""
        n_total = len(self.df_preds)
        self.assertEqual(n_total, 163, "Test set size must be exactly 163")
        
        trans_counts = self.df_preds["pred_translated"].value_counts().to_dict()
        self.assertEqual(trans_counts.get("SUPPORTED", 0), 64)
        self.assertEqual(trans_counts.get("INSUFFICIENT_EVIDENCE", 0), 55)
        self.assertEqual(trans_counts.get("CONTRADICTED", 0), 44)
        
        orig_counts = self.df_preds["pred_original"].value_counts().to_dict()
        self.assertEqual(orig_counts.get("CONTRADICTED", 0), 75)
        self.assertEqual(orig_counts.get("SUPPORTED", 0), 60)
        self.assertEqual(orig_counts.get("INSUFFICIENT_EVIDENCE", 0), 28)
        
        # Complete 3x3 contingency matrix (Row: translated, Col: original)
        crosstab = pd.crosstab(self.df_preds["pred_translated"], self.df_preds["pred_original"])
        self.assertEqual(crosstab.loc["CONTRADICTED", "CONTRADICTED"], 21)
        self.assertEqual(crosstab.loc["CONTRADICTED", "INSUFFICIENT_EVIDENCE"], 5)
        self.assertEqual(crosstab.loc["CONTRADICTED", "SUPPORTED"], 18)
        
        self.assertEqual(crosstab.loc["INSUFFICIENT_EVIDENCE", "CONTRADICTED"], 23)
        self.assertEqual(crosstab.loc["INSUFFICIENT_EVIDENCE", "INSUFFICIENT_EVIDENCE"], 14)
        self.assertEqual(crosstab.loc["INSUFFICIENT_EVIDENCE", "SUPPORTED"], 18)
        
        self.assertEqual(crosstab.loc["SUPPORTED", "CONTRADICTED"], 31)
        self.assertEqual(crosstab.loc["SUPPORTED", "INSUFFICIENT_EVIDENCE"], 9)
        self.assertEqual(crosstab.loc["SUPPORTED", "SUPPORTED"], 24)

    def test_directional_flips_derived_vs_canonical_results(self):
        """Verifies that every directional flip reported in canonical_results.csv matches per-instance derivations."""
        # 1. SUP -> CON
        trans_sup = self.df_preds["pred_translated"] == "SUPPORTED"
        orig_con = self.df_preds["pred_original"] == "CONTRADICTED"
        sup_to_con_num = int((trans_sup & orig_con).sum())
        sup_to_con_den = int(trans_sup.sum())
        self.assertEqual(sup_to_con_num, 31)
        self.assertEqual(sup_to_con_den, 64)
        sup_to_con_rate = round(sup_to_con_num / sup_to_con_den, 4)
        self.assertEqual(sup_to_con_rate, 0.4844)
        
        row_sup_con = self.df_canonical[self.df_canonical["Metric_or_System"] == "Directional Flip SUP to CON"].iloc[0]
        self.assertEqual(float(row_sup_con["Value"]), 0.4844)
        self.assertEqual(str(row_sup_con["Degrees_of_Freedom_or_Counts"]).strip(), "31 / 64")
        
        # 2. CON -> SUP
        trans_con = self.df_preds["pred_translated"] == "CONTRADICTED"
        orig_sup = self.df_preds["pred_original"] == "SUPPORTED"
        con_to_sup_num = int((trans_con & orig_sup).sum())
        con_to_sup_den = int(trans_con.sum())
        self.assertEqual(con_to_sup_num, 18)
        self.assertEqual(con_to_sup_den, 44)
        con_to_sup_rate = round(con_to_sup_num / con_to_sup_den, 4)
        self.assertEqual(con_to_sup_rate, 0.4091)
        
        row_con_sup = self.df_canonical[self.df_canonical["Metric_or_System"] == "Directional Flip CON to SUP"].iloc[0]
        self.assertEqual(float(row_con_sup["Value"]), 0.4091)
        self.assertEqual(str(row_con_sup["Degrees_of_Freedom_or_Counts"]).strip(), "18 / 44")
        
        # 3. NEU -> CON
        trans_neu = self.df_preds["pred_translated"] == "INSUFFICIENT_EVIDENCE"
        neu_to_con_num = int((trans_neu & orig_con).sum())
        neu_to_con_den = int(trans_neu.sum())
        self.assertEqual(neu_to_con_num, 23)
        self.assertEqual(neu_to_con_den, 55)
        neu_to_con_rate = round(neu_to_con_num / neu_to_con_den, 4)
        self.assertEqual(neu_to_con_rate, 0.4182)
        
        row_neu_con = self.df_canonical[self.df_canonical["Metric_or_System"] == "Directional Flip NEU to CON"].iloc[0]
        self.assertEqual(float(row_neu_con["Value"]), 0.4182)
        self.assertEqual(str(row_neu_con["Degrees_of_Freedom_or_Counts"]).strip(), "23 / 55")

    def test_derived_vs_json_and_index_artifacts(self):
        """Verifies parity across test_metrics.json and FINAL_RESULTS_INDEX.csv."""
        # test_metrics.json
        prim_metrics = self.metrics_json["primary_sensitivity_metrics"]
        self.assertEqual(prim_metrics["directional_flip_sup_to_con"]["numerator"], 31)
        self.assertEqual(prim_metrics["directional_flip_sup_to_con"]["denominator"], 64)
        self.assertEqual(prim_metrics["directional_flip_sup_to_con"]["rate"], 0.4844)
        
        self.assertEqual(prim_metrics["directional_flip_con_to_sup"]["numerator"], 18)
        self.assertEqual(prim_metrics["directional_flip_con_to_sup"]["denominator"], 44)
        self.assertEqual(prim_metrics["directional_flip_con_to_sup"]["rate"], 0.4091)
        
        self.assertEqual(prim_metrics["directional_flip_neu_to_con"]["numerator"], 23)
        self.assertEqual(prim_metrics["directional_flip_neu_to_con"]["denominator"], 55)
        self.assertEqual(prim_metrics["directional_flip_neu_to_con"]["rate"], 0.4182)
        
        # FINAL_RESULTS_INDEX.csv
        idx_con_sup = self.df_index[self.df_index["Metric_Name"] == "Directional Flip CON to SUP"].iloc[0]
        self.assertEqual(int(idx_con_sup["Numerator"]), 18)
        self.assertEqual(int(idx_con_sup["Denominator"]), 44)
        self.assertEqual(float(idx_con_sup["Numerical_Value"]), 0.4091)
        
        idx_neu_con = self.df_index[self.df_index["Metric_Name"] == "Directional Flip NEU to CON"].iloc[0]
        self.assertEqual(int(idx_neu_con["Numerator"]), 23)
        self.assertEqual(int(idx_neu_con["Denominator"]), 55)
        self.assertEqual(float(idx_neu_con["Numerical_Value"]), 0.4182)

    def test_paired_mcnemar_exact_and_chi2_contingency(self):
        """
        Regression test asserting the mathematical distinction between:
        1. No-Check vs. Direct Multilingual: b=27, c=51, n=78, chi2=6.7821, p=0.00877
        2. Selective-Check vs. Direct Multilingual: b=23, c=47, n=70, chi2=7.5571, p=0.00558
        Both have |b - c| = 24 (numerator 529), but differing denominators (78 vs 70).
        """
        import scipy.stats as stats
        y = self.df_preds["gold_label"].values
        pt = self.df_preds["pred_translated"].values
        po = self.df_preds["pred_original"].values
        ps = self.df_preds["pred_selective"].values

        corr_trans = (pt == y)
        corr_orig = (po == y)
        corr_sel = (ps == y)

        # 1. No-Check vs Direct Multilingual (b=27, c=51)
        b_no = int((corr_trans & ~corr_orig).sum())
        c_no = int((~corr_trans & corr_orig).sum())
        self.assertEqual(b_no, 27, "No-Check correct, Direct Multi wrong must be 27 (S_degraded)")
        self.assertEqual(c_no, 51, "No-Check wrong, Direct Multi correct must be 51 (S_trans)")
        n_no = b_no + c_no
        self.assertEqual(n_no, 78)
        diff_no = abs(b_no - c_no)
        self.assertEqual(diff_no, 24)
        chi2_no_cc = (diff_no - 1)**2 / n_no
        self.assertAlmostEqual(chi2_no_cc, 529 / 78, places=4)
        self.assertAlmostEqual(round(chi2_no_cc, 4), 6.7821)
        p_exact_no = stats.binomtest(b_no, n_no, 0.5, alternative="two-sided").pvalue
        self.assertAlmostEqual(round(p_exact_no, 5), 0.00877)

        # 2. Selective-Check vs Direct Multilingual (b=23, c=47)
        b_sel = int((corr_sel & ~corr_orig).sum())
        c_sel = int((~corr_sel & corr_orig).sum())
        self.assertEqual(b_sel, 23, "Selective correct, Direct Multi wrong must be 23")
        self.assertEqual(c_sel, 47, "Selective wrong, Direct Multi correct must be 47")
        n_sel = b_sel + c_sel
        self.assertEqual(n_sel, 70)
        diff_sel = abs(b_sel - c_sel)
        self.assertEqual(diff_sel, 24)
        chi2_sel_cc = (diff_sel - 1)**2 / n_sel
        self.assertAlmostEqual(chi2_sel_cc, 529 / 70, places=4)
        self.assertAlmostEqual(round(chi2_sel_cc, 4), 7.5571)
        p_exact_sel = stats.binomtest(b_sel, n_sel, 0.5, alternative="two-sided").pvalue
        self.assertAlmostEqual(round(p_exact_sel, 5), 0.00558)

        # Assert shared numerator but distinct denominators
        self.assertEqual((diff_no - 1)**2, (diff_sel - 1)**2)
        self.assertNotEqual(n_no, n_sel)
        self.assertNotEqual(chi2_no_cc, chi2_sel_cc)

if __name__ == "__main__":
    unittest.main()
