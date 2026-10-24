# Automated Test Suite Execution Report

- **Execution Time:** 2026-10-24T09:48:53Z
- **Overall Status:** PASS
- **Tests Executed:** 47
- **Failures:** 0
- **Errors:** 0
- **Duration:** 0.624s

## Test Suite Coverage Across 9 Verification Modules
1. `test_annotation_integrity.py`: Verifies that synthetic annotations are quarantined with checksums, active blinded samples contain only stimulus columns, no filled submissions exist in handoffs, and execution of synthetic generators is blocked.
2. `test_annotation_workflow.py`: Verifies packet generation integrity (50 unique items, no prediction leakage), empty response fields in packets, submission validator enforcement (schema, enums, required rationales), and inter-rater agreement computation on an artificial QA fixture.
3. `test_corrected_pipeline.py`: Verifies that real end-to-end inference outputs exist with proper counts (103 dev, 163 test), non-zero measured latencies, token-based truncation ($\le 512$), and tuning artifacts.
4. `test_data_integrity.py`: Verifies X-Fact raw data provenance, dev/test partition integrity (103 dev, 163 test), disjoint claim texts and item IDs (zero split leakage), label mappings, and absence of gold positive class.
5. `test_directional_flips.py`: Directly recomputes the 3x3 transition matrix from per-instance test predictions and strictly verifies exact parity for every directional flip numerator, denominator, and rate against all summary artifacts.
6. `test_logic_helpers.py`: Decoupled tests for Devanagari and Arabic numeral extraction, numeral Jaccard similarity, risk score bounds, exact-count random draw matching, McNemar test symmetry, and Benjamini-Hochberg FDR monotonicity.
7. `test_method_logic.py`: Verifies Devanagari numeral normalization, true Jaccard similarity, risk score bounds, and selective cascade routing behavior.
8. `test_metrics_and_partitions.py`: Verifies observed point estimates, exact disjoint error attribution, and exact McNemar test calculations on legacy reference splits.
9. `test_reproduced_artifacts_v4.py`: Verifies split integrity, direct MT generation string existence, token length bounds, softmax probability sum to 1.0, threshold selection and trigger consistency (`selective_triggered == (risk_score >= tau_star)`), latency arithmetic, 100-seed random control properties, and benchmark metric reconciliation.

**Result:** All 47 unit and regression tests passed successfully.
