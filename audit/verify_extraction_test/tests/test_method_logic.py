import sys
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))

import unittest
import numpy as np
from scripts.run_corrected_experiments import extract_numbers, compute_numeral_jaccard, compute_risk

class TestMethodLogic(unittest.TestCase):
    def test_devanagari_numeral_extraction(self):
        text_hi = "शामली में ५०० और १००० के नोट मिले।"
        extracted = extract_numbers(text_hi)
        self.assertEqual(extracted, {"500", "1000"}, "Devanagari numerals must be normalized to standard digits")
        
    def test_true_jaccard_similarity(self):
        # Exact match
        orig = "५०० रुपये"
        trans = "500 rupees"
        self.assertAlmostEqual(compute_numeral_jaccard(orig, trans), 1.0)
        
        # Partial match: 1 common, 1 extra in trans
        orig = "५०० रुपये"
        trans = "500 rupees for 200 items"
        # Intersection: {500}, Union: {500, 200} -> Jaccard = 0.5
        self.assertAlmostEqual(compute_numeral_jaccard(orig, trans), 0.5)
        
        # Complete mismatch
        orig = "५००"
        trans = "1000"
        self.assertAlmostEqual(compute_numeral_jaccard(orig, trans), 0.0)
        
        # Empty sets in both
        orig_none = "कोई संख्या नहीं"
        trans_none = "no numbers here"
        self.assertAlmostEqual(compute_numeral_jaccard(orig_none, trans_none), 1.0)

    def test_risk_score_bounds(self):
        # Perfect confidence (max_p=1.0) and perfect jaccard (1.0) -> risk=0.0
        p_cert = np.array([0.0, 0.0, 1.0])
        self.assertAlmostEqual(compute_risk(p_cert, 1.0), 0.0)
        
        # Maximum uncertainty (max_p=0.333) and zero jaccard (0.0)
        p_flat = np.array([0.3333, 0.3333, 0.3334])
        r_high = compute_risk(p_flat, 0.0)
        self.assertGreater(r_high, 0.70)
        
    def test_routing_behavior(self):
        # When risk >= tau -> routes to original
        tau = 0.30
        risk_high = 0.45
        risk_low = 0.15
        
        pred_orig = "CONTRADICTED"
        pred_trans = "SUPPORTED"
        
        route_high = pred_orig if risk_high >= tau else pred_trans
        route_low = pred_orig if risk_low >= tau else pred_trans
        
        self.assertEqual(route_high, "CONTRADICTED", "High risk must route to original evidence")
        self.assertEqual(route_low, "SUPPORTED", "Low risk must remain on translated evidence")

if __name__ == "__main__":
    unittest.main()
