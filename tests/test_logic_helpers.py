"""
Unit tests for pure decision logic and evaluation metrics.
These tests run fast and isolated without importing heavyweight Transformers models.
"""
import unittest
import numpy as np
import scipy.stats as stats
import re

def extract_numbers(text: str) -> set[str]:
    devanagari_nums = {"०": "0", "१": "1", "२": "2", "३": "3", "४": "4", "५": "5", "६": "6", "७": "7", "८": "8", "९": "9"}
    norm_text = "".join(devanagari_nums.get(c, c) for c in text)
    return set(re.findall(r"\b\d+(?:[\.,]\d+)?\b", norm_text))

def compute_numeral_jaccard(orig_text: str, trans_text: str) -> float:
    orig_nums = extract_numbers(orig_text)
    trans_nums = extract_numbers(trans_text)
    union = orig_nums | trans_nums
    if not union:
        return 1.0
    intersection = orig_nums & trans_nums
    return float(len(intersection) / len(union))

def compute_risk(probs_trans: np.ndarray, num_jaccard: float) -> float:
    max_p = float(np.max(probs_trans))
    num_mismatch = 1.0 - float(num_jaccard)
    return float(0.70 * (1.0 - max_p) + 0.30 * num_mismatch)

def mcnemar_exact(y_true, y_pred_a, y_pred_b):
    corr_a = (y_pred_a == y_true)
    corr_b = (y_pred_b == y_true)
    b = int(np.sum(corr_a & ~corr_b))
    c = int(np.sum(~corr_a & corr_b))
    n_disc = b + c
    if n_disc == 0:
        return 0.0, 1.0, b, c
    stat = float((abs(b - c) - 1.0)**2 / n_disc)
    p_val = float(min(1.0, 2.0 * stats.binom.cdf(min(b, c), n_disc, 0.5)))
    return stat, p_val, b, c

def fdr_bh(p_values: list[float]) -> list[float]:
    n = len(p_values)
    if n == 0:
        return []
    sorted_indices = np.argsort(p_values)
    sorted_p = np.array(p_values)[sorted_indices]
    adjusted = np.zeros(n)
    running_min = 1.0
    for i in range(n - 1, -1, -1):
        rank = i + 1
        adj = min(1.0, sorted_p[i] * n / rank)
        running_min = min(running_min, adj)
        adjusted[i] = running_min
    result = np.zeros(n)
    result[sorted_indices] = adjusted
    return [float(x) for x in result]

class TestLogicHelpers(unittest.TestCase):
    def test_numeral_extraction_devanagari_and_arabic(self):
        text_hi = "२०२६ में ५०० और 1000 के नोट"
        nums = extract_numbers(text_hi)
        self.assertIn("2026", nums)
        self.assertIn("500", nums)
        self.assertIn("1000", nums)

    def test_numeral_jaccard_identical(self):
        t1 = "Cost is 500 dollars in 2026."
        t2 = "५०० डॉलर की लागत २०२६ में।"
        self.assertEqual(compute_numeral_jaccard(t1, t2), 1.0)

    def test_numeral_jaccard_disjoint(self):
        t1 = "Item costs 100."
        t2 = "Item costs 200."
        self.assertEqual(compute_numeral_jaccard(t1, t2), 0.0)

    def test_numeral_jaccard_no_numbers(self):
        t1 = "No numbers here."
        t2 = "Still no numbers."
        self.assertEqual(compute_numeral_jaccard(t1, t2), 1.0)

    def test_risk_score_bounds(self):
        # Perfect confidence, perfect numeral match -> risk = 0
        p_cert = np.array([1.0, 0.0, 0.0])
        self.assertAlmostEqual(compute_risk(p_cert, 1.0), 0.0)

        # Max uncertainty (1/3), complete numeral mismatch (0.0) -> risk = 0.7*(2/3) + 0.3*1.0 = 0.7667
        p_unif = np.array([1/3, 1/3, 1/3])
        risk_unif = compute_risk(p_unif, 0.0)
        self.assertAlmostEqual(risk_unif, 0.7 * (2/3) + 0.3 * 1.0, places=4)

    def test_mcnemar_exact_symmetry(self):
        yt = np.array([1, 1, 1, 0, 0])
        ya = np.array([1, 1, 0, 0, 0])
        yb = np.array([1, 0, 1, 0, 0])
        stat1, p1, b1, c1 = mcnemar_exact(yt, ya, yb)
        stat2, p2, b2, c2 = mcnemar_exact(yt, yb, ya)
        self.assertEqual(b1, c2)
        self.assertEqual(c1, b2)
        self.assertEqual(p1, p2)

    def test_fdr_bh_monotonicity(self):
        raw_p = [0.001, 0.04, 0.05, 0.20, 0.80]
        adj_p = fdr_bh(raw_p)
        self.assertEqual(len(adj_p), len(raw_p))
        for r, a in zip(raw_p, adj_p):
            self.assertGreaterEqual(a, r, "Adjusted p-value must be >= raw p-value")
        for i in range(len(adj_p) - 1):
            self.assertLessEqual(adj_p[i], adj_p[i+1], "FDR adjusted p-values must be monotonic")

    def test_exact_matched_count_random_draw(self):
        n_items = 163
        cov_target = 0.0859
        k_items = int(round(cov_target * n_items))
        self.assertEqual(k_items, 14)

        for s in range(50):
            rng = np.random.default_rng(s)
            idx = rng.choice(n_items, size=k_items, replace=False)
            self.assertEqual(len(idx), 14)
            self.assertEqual(len(set(idx)), 14, "Indices must be unique without replacement")

if __name__ == "__main__":
    unittest.main()
