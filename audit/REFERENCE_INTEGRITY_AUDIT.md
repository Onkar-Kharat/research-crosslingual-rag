# AUDIT REPORT: Reference Integrity and Freeze Decision Consolidation

**Audit Date:** October 2026  
**Auditor:** Senior Methodology & Integrity Auditor  
**Repository:** Cross-Lingual Evidence Verification  
**Status:** COMPLETE, CONSOLIDATED, & ALL REFERENCES RESOLVED  

---

## 1. Consolidation of Freeze Decisions

### Authoritative Final Freeze File:
- **`audit/FREEZE_DECISION.md`** is designated as the **SOLE AUTHORITATIVE FINAL DECISION FILE** for this research package.
- All other summary documents (`FINAL_PASS/FINAL_RESEARCH_FREEZE_DECISION.md`, `FREEZE_AUDIT.md`, `README.md`) serve as navigational pointers that conform strictly to `audit/FREEZE_DECISION.md`.
- **Frozen Research Scope:** *Cross-Lingual Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift*.
- **Certified Freeze Status:** `Status A: FROZEN — EXPLORATORY COMPUTATIONAL STUDY`.

---

## 2. Audit of Referenced Pipeline Files

A previous review identified several file references in audit reports and markdown documents that risked broken link errors or naming ambiguity. We have audited every referenced file and established canonical resolutions:

| Referenced File Name | Historical Reference Context | Actual File Status & Authoritative Path | Resolution Action |
|:---|:---|:---|:---|
| `test_predictions.jsonl` | Mentioned as per-instance predictions in `FREEZE_MANIFEST.md` | Exists in `experiments/results_canonical/test_predictions.jsonl` | Generated deterministic JSONL companion from `canonical_test_predictions.csv`. Both CSV and JSONL formats provided. |
| `test_metrics.json` | Referenced in `FINAL_PASS/REPRODUCE_FROM_CLEAN_EXTRACTION.md` | Exists in `experiments/results_canonical/test_metrics.json` | Generated machine-readable JSON containing all exact canonical metrics, CIs, and McNemar tests. |
| `dev_threshold_sweep.json` | Referenced in `ISSUES_AND_FIXES.csv` and `FINAL_PASS/FINAL_RESEARCH_FREEZE_DECISION.md` | Exists in `experiments/results_canonical/dev_threshold_sweep.json` | Generated JSON companion from `canonical_dev_tuning.csv` with metadata and utility formulas. Both CSV and JSON formats provided. |
| `paired_comparison_tests.json` | Mentioned in earlier freeze report | Exists in `experiments/results_canonical/canonical_statistical_tests.csv` and `test_metrics.json` | Updated documentation references to point to `experiments/results_canonical/canonical_statistical_tests.csv` and `test_metrics.json`. |
| `test_metrics_table.csv` | Mentioned in earlier freeze draft | Exists in `experiments/results_canonical/canonical_benchmark_table.csv` | Updated references to `experiments/results_canonical/canonical_benchmark_table.csv`. |

---

## 3. Directory Navigation & Link Integrity Table

Every key artifact referenced across the repository maps directly to an active file on disk:

```
[Repository Root]
├── README.md                                          -> Quickstart, core findings, & reproduction commands
├── canonical_results.csv                              -> Authoritative machine-readable summary table
├── protocol/
│   ├── analysis_plan.yaml                             -> Prespecified experimental and tuning protocol
│   └── FINAL_SCOPE_AND_CLAIMS.md                      -> Scoped empirical boundaries & construct validity
├── experiments/
│   ├── configs/verification_pipeline.yaml             -> Model and inference parameters
│   └── results_canonical/
│       ├── canonical_test_predictions.csv             -> 163 per-instance test predictions with all columns
│       ├── test_predictions.jsonl                    -> JSONL format of canonical test predictions
│       ├── canonical_dev_predictions.csv              -> 103 per-instance dev predictions
│       ├── canonical_dev_tuning.csv                   -> Full dev threshold sweep table
│       ├── dev_threshold_sweep.json                   -> JSON format of threshold sweep
│       ├── test_metrics.json                          -> Consolidated machine-readable test metrics
│       ├── canonical_benchmark_table.csv              -> Full benchmark & ablation table
│       ├── canonical_statistical_tests.csv            -> Pairwise McNemar & permutation tests
│       ├── canonical_latency_summary.json             -> Real forward-pass latencies
│       ├── canonical_error_attribution.json           -> Diagnostic error category counts
│       ├── RUN_MANIFEST.json                          -> Input/output cryptographic manifest
│       └── figures/                                   -> Vector PDF and PNG publication figures
├── tests/
│   ├── run_all_tests.py                               -> Master test runner (43 tests pass in ~0.38s)
│   └── TEST_REPORT.md                                 -> Detailed test execution report
└── audit/
    ├── FREEZE_DECISION.md                             -> Single authoritative freeze certification
    ├── DUPLICATED_CLAIM_EVIDENCE_AUDIT.md             -> Audit of claim repetition in evidence
    ├── STATISTICAL_REANALYSIS.md                      -> Mathematical resolution of McNemar counts
    ├── CANONICAL_PIPELINE_AUDIT.md                    -> Pipeline unification audit
    └── CANONICAL_METRIC_RECALCULATION.md              -> Metric recalculation audit
```

No dangling file references remain in any active document.
