import json
import csv
import unittest
from pathlib import Path

import sys
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

class TestDataIntegrity(unittest.TestCase):
    def setUp(self):
        self.dev_path = PROJECT_ROOT / "data" / "processed" / "dev.jsonl"
        self.test_path = PROJECT_ROOT / "data" / "processed" / "test.jsonl"
        self.raw_dev = PROJECT_ROOT / "data" / "raw" / "dev.all.tsv"
        self.raw_test = PROJECT_ROOT / "data" / "raw" / "test.all.tsv"
        
    def test_files_exist(self):
        self.assertTrue(self.dev_path.exists(), "dev.jsonl must exist")
        self.assertTrue(self.test_path.exists(), "test.jsonl must exist")
        self.assertTrue(self.raw_dev.exists(), "dev.all.tsv must exist")
        self.assertTrue(self.raw_test.exists(), "test.all.tsv must exist")
        
    def test_sample_sizes(self):
        dev_rows = [json.loads(line) for line in open(self.dev_path, encoding="utf-8")]
        test_rows = [json.loads(line) for line in open(self.test_path, encoding="utf-8")]
        self.assertEqual(len(dev_rows), 103, "Dev must contain exactly 103 Hindi instances")
        self.assertEqual(len(test_rows), 163, "Test must contain exactly 163 Hindi instances")
        
    def test_no_split_leakage(self):
        dev_rows = [json.loads(line) for line in open(self.dev_path, encoding="utf-8")]
        test_rows = [json.loads(line) for line in open(self.test_path, encoding="utf-8")]
        
        dev_ids = {r["item_id"] for r in dev_rows}
        test_ids = {r["item_id"] for r in test_rows}
        self.assertEqual(len(dev_ids & test_ids), 0, "Item IDs must be completely disjoint between dev and test")
        
        dev_claims = {r["claim"].strip() for r in dev_rows}
        test_claims = {r["claim"].strip() for r in test_rows}
        self.assertEqual(len(dev_claims & test_claims), 0, "Claim texts must be completely disjoint between dev and test")
        
    def test_label_mappings(self):
        test_rows = [json.loads(line) for line in open(self.test_path, encoding="utf-8")]
        valid_gold_labels = {"CONTRADICTED", "INSUFFICIENT_EVIDENCE", "SUPPORTED"}
        for r in test_rows:
            self.assertIn(r["gold_label"], valid_gold_labels, f"Invalid label {r['gold_label']}")
            if r["raw_gold_label"] in ["false", "mostly false"]:
                self.assertEqual(r["gold_label"], "CONTRADICTED")
            elif r["raw_gold_label"] in ["partly true/misleading", "unproven"]:
                self.assertEqual(r["gold_label"], "INSUFFICIENT_EVIDENCE")
                
    def test_missing_positive_class_audited(self):
        test_rows = [json.loads(line) for line in open(self.test_path, encoding="utf-8")]
        supported_count = sum(1 for r in test_rows if r["gold_label"] == "SUPPORTED")
        self.assertEqual(supported_count, 0, "Confirmed: SUPPORTED class is completely absent in ground truth")

    def test_exact_split_label_counts(self):
        dev_rows = [json.loads(line) for line in open(self.dev_path, encoding="utf-8")]
        test_rows = [json.loads(line) for line in open(self.test_path, encoding="utf-8")]
        
        dev_counts = {lbl: 0 for lbl in ["CONTRADICTED", "INSUFFICIENT_EVIDENCE", "SUPPORTED"]}
        for r in dev_rows:
            dev_counts[r["gold_label"]] += 1
            
        test_counts = {lbl: 0 for lbl in ["CONTRADICTED", "INSUFFICIENT_EVIDENCE", "SUPPORTED"]}
        for r in test_rows:
            test_counts[r["gold_label"]] += 1
            
        self.assertEqual(dev_counts["CONTRADICTED"], 89, "Dev must contain exactly 89 CONTRADICTED")
        self.assertEqual(dev_counts["INSUFFICIENT_EVIDENCE"], 14, "Dev must contain exactly 14 INSUFFICIENT_EVIDENCE")
        self.assertEqual(dev_counts["SUPPORTED"], 0, "Dev must contain exactly 0 SUPPORTED")
        
        self.assertEqual(test_counts["CONTRADICTED"], 142, "Test must contain exactly 142 CONTRADICTED")
        self.assertEqual(test_counts["INSUFFICIENT_EVIDENCE"], 21, "Test must contain exactly 21 INSUFFICIENT_EVIDENCE")
        self.assertEqual(test_counts["SUPPORTED"], 0, "Test must contain exactly 0 SUPPORTED")

if __name__ == "__main__":
    unittest.main()
