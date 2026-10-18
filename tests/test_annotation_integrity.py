"""
Unit tests for human annotation integrity and synthetic data invalidation.
Enforces non-negotiable scientific integrity protocols:
1. Synthetic annotation scripts and outputs must be quarantined.
2. Production blinded samples must NOT contain pre-filled annotations or adjudications.
3. Gate C must remain strictly BLOCKED until authentic human data is ingested.
"""
import sys
import unittest
import pandas as pd
from pathlib import Path
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class TestAnnotationIntegrity(unittest.TestCase):
    def test_quarantine_directory_and_checksums(self):
        q_dir = PROJECT_ROOT / "audit" / "invalidated_synthetic_annotations"
        self.assertTrue(q_dir.exists(), "Quarantine directory must exist")
        self.assertTrue((q_dir / "README_INVALIDATION.md").exists())
        self.assertTrue((q_dir / "perform_bilingual_annotation.py").exists())
        self.assertTrue((q_dir / "HUMAN_ANNOTATION_REPORT.md").exists())
        self.assertTrue((q_dir / "annotation_submission_Annotator_1.csv").exists())
        self.assertTrue((q_dir / "annotation_submission_Annotator_2.csv").exists())

    def test_perform_bilingual_annotation_guard(self):
        """Active script must raise an error to prevent accidental synthetic generation."""
        script_path = PROJECT_ROOT / "scripts" / "perform_bilingual_annotation.py"
        self.assertTrue(script_path.exists())
        res = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True
        )
        self.assertNotEqual(res.returncode, 0, "Quarantined script must exit with error")
        self.assertIn("CRITICAL RESEARCH INTEGRITY VIOLATION", res.stderr)

    def test_blinded_sample_csv_clean(self):
        """Active blinded sample CSVs must contain ONLY blinded columns."""
        blinded_paths = [
            PROJECT_ROOT / "annotation" / "blinded_annotation_sample.csv",
            PROJECT_ROOT / "annotation_handoff" / "annotation_sample_blinded.csv"
        ]
        allowed_cols = {'Sample_ID', 'Item_ID', 'Claim_Hindi', 'Original_Evidence_Hindi', 'Machine_Translation_English'}
        prohibited_substrings = ['Annotator', 'Consensus', 'Fidelity', 'Distortion', 'Adjudication', 'Rationale']

        for bp in blinded_paths:
            self.assertTrue(bp.exists(), f"{bp.name} must exist")
            df = pd.read_csv(bp)
            self.assertEqual(len(df), 50, f"{bp.name} must contain exactly 50 items")
            self.assertEqual(set(df.columns), allowed_cols, f"{bp.name} must have only stimulus columns")
            for col in df.columns:
                for bad in prohibited_substrings:
                    self.assertNotIn(bad, col, f"Prohibited column {col} found in {bp.name}")

    def test_gate_c_blocked_in_report(self):
        rep_path = PROJECT_ROOT / "annotation" / "HUMAN_ANNOTATION_REPORT.md"
        self.assertTrue(rep_path.exists())
        content = rep_path.read_text(encoding="utf-8")
        self.assertIn("Gate C BLOCKED", content)
        self.assertIn("INVALIDATED", content)
        # Must not report 96% or kappa 0.911 as current valid agreement
        self.assertNotIn("Raw Percentage Agreement: 96", content)

    def test_no_filled_submissions_in_handoff_folder(self):
        handoff_dir = PROJECT_ROOT / "annotation_handoff"
        self.assertFalse((handoff_dir / "annotation_submission_Annotator_1.csv").exists(),
                         "Filled submissions must NOT exist in annotator handoff folder")
        self.assertFalse((handoff_dir / "annotation_submission_Annotator_2.csv").exists(),
                         "Filled submissions must NOT exist in annotator handoff folder")

if __name__ == "__main__":
    unittest.main()
