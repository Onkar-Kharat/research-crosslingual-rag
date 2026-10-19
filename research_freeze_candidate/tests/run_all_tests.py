import unittest
import json
import time
from pathlib import Path

WORKSPACE = Path(r"c:\Users\Onkar\OneDrive\Desktop\Research_crosslingual_rag_research")
TESTS_DIR = WORKSPACE / "tests"

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
        "## Test Suite Coverage",
        "1. `test_data_integrity.py`: Verifies X-Fact raw data provenance, dev/test partition integrity (103 dev, 163 test), disjoint claim texts and item IDs, label mappings, and absence of positive class.",
        "2. `test_method_logic.py`: Verifies Devanagari numeral normalization, true Jaccard similarity, risk score bounds, and selective cascade routing.",
        "3. `test_metrics_and_partitions.py`: Verifies direct observed point estimates, exact disjoint error attribution ($41 + 61 + 9 = 111$), and exact McNemar test calculations.",
        "",
        f"**Result:** All {report['total_tests']} unit and regression tests passed successfully." if report['success'] else f"**Result:** Failed tests: {report['failures']}"
    ]
    
    with open(TESTS_DIR / "TEST_REPORT.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        
    print(f"\nWrote test reports to {TESTS_DIR / 'TEST_REPORT.md'} and test_report.json")
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
