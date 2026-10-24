import unittest
import json
import time
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
TESTS_DIR = PROJECT_ROOT / "tests"

def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(TESTS_DIR), pattern="test_*.py")
    
    start_time = time.time()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    duration = time.time() - start_time
    
    report = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_tests": result.testsRun,
        "success": result.wasSuccessful(),
        "failures_count": len(result.failures),
        "errors_count": len(result.errors),
        "duration_seconds": round(duration, 3),
        "failures": [{"test": str(t), "err": str(e)} for t, e in result.failures],
        "errors": [{"test": str(t), "err": str(e)} for t, e in result.errors]
    }
    
    with open(TESTS_DIR / "test_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    repro_dir = PROJECT_ROOT / "reproducibility"
    repro_dir.mkdir(parents=True, exist_ok=True)

    md_lines = [
        "# Automated Test Suite Execution Report",
        "",
        f"- **Execution Time:** {report['timestamp']}",
        f"- **Overall Status:** {'PASS' if report['success'] else 'FAIL'}",
        f"- **Tests Executed:** {report['total_tests']}",
        f"- **Failures:** {report['failures_count']}",
        f"- **Errors:** {report['errors_count']}",
        f"- **Duration:** {report['duration_seconds']}s",
        "",
        "## Test Suite Coverage Across 9 Verification Modules",
        "1. `test_annotation_integrity.py`: Verifies that synthetic annotations are quarantined with checksums, active blinded samples contain only stimulus columns, no filled submissions exist in handoffs, and execution of synthetic generators is blocked.",
        "2. `test_annotation_workflow.py`: Verifies packet generation integrity (50 unique items, no prediction leakage), empty response fields in packets, submission validator enforcement (schema, enums, required rationales), and inter-rater agreement computation on an artificial QA fixture.",
        r"3. `test_corrected_pipeline.py`: Verifies that real end-to-end inference outputs exist with proper counts (103 dev, 163 test), non-zero measured latencies, token-based truncation ($\le 512$), and tuning artifacts.",
        "4. `test_data_integrity.py`: Verifies X-Fact raw data provenance, dev/test partition integrity (103 dev, 163 test), disjoint claim texts and item IDs (zero split leakage), label mappings, and absence of gold positive class.",
        "5. `test_directional_flips.py`: Directly recomputes the 3x3 transition matrix from per-instance test predictions and strictly verifies exact parity for every directional flip numerator, denominator, and rate against all summary artifacts.",
        "6. `test_logic_helpers.py`: Decoupled tests for Devanagari and Arabic numeral extraction, numeral Jaccard similarity, risk score bounds, exact-count random draw matching, McNemar test symmetry, and Benjamini-Hochberg FDR monotonicity.",
        "7. `test_method_logic.py`: Verifies Devanagari numeral normalization, true Jaccard similarity, risk score bounds, and selective cascade routing behavior.",
        "8. `test_metrics_and_partitions.py`: Verifies observed point estimates, exact disjoint error attribution, and exact McNemar test calculations on legacy reference splits.",
        "9. `test_reproduced_artifacts_v4.py`: Verifies split integrity, direct MT generation string existence, token length bounds, softmax probability sum to 1.0, threshold selection and trigger consistency (`selective_triggered == (risk_score >= tau_star)`), latency arithmetic, 100-seed random control properties, and benchmark metric reconciliation.",
        "",
        f"**Result:** All {report['total_tests']} unit and regression tests passed successfully." if report['success'] else f"**Result:** Failed tests: {report['failures']}"
    ]
    
    content = "\n".join(md_lines) + "\n"
    with open(TESTS_DIR / "TEST_REPORT.md", "w", encoding="utf-8") as f:
        f.write(content)
    with open(repro_dir / "TEST_REPORT.md", "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"\nWrote test reports to {TESTS_DIR / 'TEST_REPORT.md'} and {repro_dir / 'TEST_REPORT.md'}")
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
