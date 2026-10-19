# Automated Test Suite Execution Report

- **Execution Time:** 2026-10-19T06:46:16Z
- **Overall Status:** PASS
- **Tests Executed:** 16
- **Failures:** 0
- **Errors:** 0
- **Duration:** 0.06s

## Test Suite Coverage
1. `test_data_integrity.py`: Verifies X-Fact raw data provenance, dev/test partition integrity (103 dev, 163 test), disjoint claim texts and item IDs, label mappings, and absence of positive class.
2. `test_method_logic.py`: Verifies Devanagari numeral normalization, true Jaccard similarity, risk score bounds, and selective cascade routing.
3. `test_metrics_and_partitions.py`: Verifies direct observed point estimates, exact disjoint error attribution ($41 + 61 + 9 = 111$), and exact McNemar test calculations.

**Result:** All 16 unit and regression tests passed successfully.