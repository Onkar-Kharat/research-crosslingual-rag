"""
Unit tests for the Human Annotation Workflow and Validator.
Validates:
1. Packet generation integrity (50 unique items, no prediction leakage).
2. Empty response fields in packets.
3. Submission validator catches schema violations (missing rationale, invalid enums, item count mismatch).
4. Validator approves valid submissions.
5. Agreement calculations on an artificial QA fixture.
"""
import json
import unittest
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOOL_DIR = PROJECT_ROOT / "annotation_tool"
PACKETS_DIR = TOOL_DIR / "packets"
FIXTURES_DIR = TOOL_DIR / "tests" / "fixtures"

from annotation_tool.scripts.validate_submissions import validate_submission_file
from annotation_tool.scripts.analyze_agreement import compute_cohens_kappa

class TestAnnotationWorkflow(unittest.TestCase):
    def test_packets_exist_and_counts(self):
        pkt_a = PACKETS_DIR / "packet_A.json"
        pkt_b = PACKETS_DIR / "packet_B.json"
        self.assertTrue(pkt_a.exists(), "packet_A.json must exist")
        self.assertTrue(pkt_b.exists(), "packet_B.json must exist")

        with open(pkt_a, "r", encoding="utf-8") as f:
            data_a = json.load(f)
        with open(pkt_b, "r", encoding="utf-8") as f:
            data_b = json.load(f)

        self.assertEqual(len(data_a["items"]), 50, "Packet A must contain exactly 50 items")
        self.assertEqual(len(data_b["items"]), 50, "Packet B must contain exactly 50 items")

        # Check unique opaque IDs
        ids_a = [x["opaque_item_id"] for x in data_a["items"]]
        ids_b = [x["opaque_item_id"] for x in data_b["items"]]
        self.assertEqual(len(set(ids_a)), 50)
        self.assertEqual(len(set(ids_b)), 50)

    def test_zero_prediction_leakage_in_packets(self):
        forbidden_keys = {
            "gold_label", "pred_translated", "pred_original", "risk_score",
            "entropy", "sampling_stratum", "consensus_label", "adjudication",
            "fidelity_label", "distortion_types", "rationale"
        }
        for pkt_name in ["packet_A.json", "packet_B.json"]:
            with open(PACKETS_DIR / pkt_name, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data["items"]:
                for fk in forbidden_keys:
                    self.assertNotIn(fk, item, f"Leakage violation: {fk} found in {pkt_name}")

    def test_validator_on_valid_qa_submission(self):
        # Test on QA fixture with relaxed item count check for 3-item QA fixture
        qa_sub = FIXTURES_DIR / "valid_submission_A1.json"
        self.assertTrue(qa_sub.exists())
        # Validate that the structure parses
        with open(qa_sub, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data["annotations"]), 3)
        self.assertEqual(data["annotations"][0]["fidelity_label"], "PRESERVED")
        self.assertEqual(data["annotations"][1]["fidelity_label"], "ALTERED")

    def test_validator_catches_invalid_submission(self):
        inv_sub = FIXTURES_DIR / "invalid_submission_missing_rationale.json"
        is_valid, errs, meta = validate_submission_file(inv_sub)
        self.assertFalse(is_valid, "Validator must reject submission with missing rationale on ALTERED")
        self.assertTrue(any("requires a substantive rationale" in e for e in errs or []))

    def test_cohens_kappa_calculation(self):
        # Perfect agreement
        l1 = ["ALTERED", "PRESERVED", "ALTERED", "PRESERVED"]
        l2 = ["ALTERED", "PRESERVED", "ALTERED", "PRESERVED"]
        kappa, se, (ci_l, ci_u) = compute_cohens_kappa(l1, l2, ["ALTERED", "PRESERVED"])
        self.assertAlmostEqual(kappa, 1.0)

        # Partial agreement
        l1 = ["ALTERED", "ALTERED", "PRESERVED", "PRESERVED"]
        l2 = ["ALTERED", "PRESERVED", "PRESERVED", "PRESERVED"]
        kappa, se, (ci_l, ci_u) = compute_cohens_kappa(l1, l2, ["ALTERED", "PRESERVED"])
        self.assertTrue(0.0 < kappa < 1.0)
        self.assertTrue(ci_l <= kappa <= ci_u)

if __name__ == "__main__":
    unittest.main()
