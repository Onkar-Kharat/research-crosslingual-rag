# Research Audit and Freeze Changelog

**Project:** Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Protocol Version:** `v1.0-observational`  
**Current Date:** 2026-10-24  

---

## [v7.0-Final-Research-Freeze] - 2026-10-24

### Repaired & Reconciled
- **Duplicated-Claim in Evidence Resolved:** Traced claim repetition in evidence to the upstream X-Fact corpus (`data/raw/dev.all.tsv` 54/103; `data/raw/test.all.tsv` 88/163) where Google snippets capture fact-checking article headlines. Verified as an intrinsic benchmark property. Executed stratified sensitivity analysis demonstrating that high disagreement (60.23% vs 68.00%) and severe $\text{SUP}\to\text{CON}$ flips (45.45% vs 51.61%) persist robustly across both strata. Documented in `audit/DUPLICATED_CLAIM_EVIDENCE_AUDIT.md`.
- **Statistical Discrepancy Mathematically Reconciled:** Proved that McNemar chi-square 7.5571 and p-value 0.00558 correspond exactly to $(24-1)^2/70 = 529/70$ with discordant counts $b=23, c=47$. Erroneous counts $b=7, c=31$ and $b=6, c=20$ from an earlier draft were corrected to $b=23, c=47$ and $b=9, c=23$ across all repository documents. Documented in `audit/STATISTICAL_REANALYSIS.md`.
- **Single Canonical Pipeline Established:** Set `experiments/results_canonical/` as the direct authoritative output destination in `scripts/run_corrected_experiments.py`, `scripts/build_canonical_manifest.py`, and `scripts/generate_publication_figures.py`. Labeled `experiments/results_corrected/` non-authoritative. Documented in `audit/CANONICAL_PIPELINE_AUDIT.md`.
- **Development Split Count Corrected:** Corrected protocol typo from 86/17 to actual verified split counts (89 `CONTRADICTED`, 14 `INSUFFICIENT_EVIDENCE`). Added automated regression test `tests/test_data_integrity.py::test_exact_split_label_counts`. Suite expanded to 43/43 tests passing.
- **Reference Integrity & Companion Formats:** Generated companion files `experiments/results_canonical/test_predictions.jsonl`, `dev_threshold_sweep.json`, and `test_metrics.json` via `scripts/generate_canonical_companion_files.py`. Consolidated authoritative freeze decision into `audit/FREEZE_DECISION.md`. Documented in `audit/REFERENCE_INTEGRITY_AUDIT.md`.
- **Reviewer Handoff Created:** Constructed `REVIEWER_HANDOFF/` containing plain-English onboarding guide, review summary, claims matrix, reproduction commands, and review checklist for independent evaluation.
- **Final Packaging:** Created release ZIP `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip`.

---

## [v6.1-Freeze-Audit] - 2026-10-24

### Repaired & Enhanced
- **Test Environment Portability:**
  - Resolved `ModuleNotFoundError: No module named 'transformers'` issue in `scripts/run_corrected_experiments.py` and `tests/test_method_logic.py`.
  - Added graceful try-except import blocks for `torch` and `transformers` in `scripts/run_corrected_experiments.py`, allowing pure decision logic and string extraction helpers (`extract_numbers`, `compute_numeral_jaccard`, `compute_risk`) to run in lightweight Python environments.
  - Added resilient fallback import in `tests/test_method_logic.py` to ensure unit test suite runs reliably across minimal CPU test environments.
  - Re-executed full automated test suite: 42/42 tests pass in 0.395 seconds.

### Added Core Audit Artifacts in `audit/`
- `audit/INITIAL_REPOSITORY_STATE.md`: Inventory of initial state, directory breakdown, and verification of reference archive `v6`.
- `audit/FILE_INVENTORY.csv`: Machine-readable census of 549 files tracking paths, categories, splits, sizes, and audit statuses.
- `audit/CHANGELOG.md`: Detailed changelog of repository modifications, repairs, and audit outcomes.
- `audit/ISSUES_AND_FIXES.csv`: Exhaustive defect ledger covering 10 audited issues (ISS-01 through ISS-10).
- `audit/FROZEN_PROTOCOL.md`: Explicit specification of the locked scientific scope, hypotheses, models, baselines, metrics, and acceptance criteria.
- `audit/DATA_AND_LABEL_AUDIT.md`: Data provenance, split isolation, and detailed analysis of the zero-gold-SUPPORTED class asymmetry in the X-Fact Hindi partition.
- `audit/METHOD_AND_THRESHOLD_AUDIT.md`: Formal verification of verification pipelines, threshold selection mechanics, and the negative result on selective cascade utility.
- `audit/METRIC_AND_COST_AUDIT.md`: Verification of statistical tests, confidence intervals, and real measured forward-pass latencies.
- `audit/RESULTS_RECONCILIATION.md`: Definitive technical reconciliation resolving the historical 39.26% ($\tau=0.30$, v2/v3) vs. canonical 28.22% ($\tau=0.650$, v4-v6) conflict.
- `audit/TEST_AND_REPRODUCTION_REPORT.md`: Comprehensive test execution log with module breakdown, pass counts, and environment details.
- `audit/RELATED_WORK_AND_NOVELTY_AUDIT.md`: In-depth literature audit across 6 domains, comparison matrix with closest prior work, and novelty boundaries.
- `audit/ANNOTATION_AUDIT.md`: Audit of human annotation state, quarantine of legacy synthetic outputs, and tooling validation.
- `audit/ANNOTATION_HANDOFF.md`: Protocol and handoff guide for external bilingual evaluators.
- `audit/LIMITATIONS.md`: Explicit enumeration of unsupported claims and methodological constraints.
- `audit/FREEZE_DECISION.md`: Formal freeze decision certifying `Status B: COMPUTATIONAL STUDY FROZEN — HUMAN VALIDATION PENDING`.
- `audit/FREEZE_MANIFEST.md`: Release manifest recording SHA-256 hashes of all canonical files and reproduction commands.

### Reconciled & Preserved
- Preserved `experiments/results_canonical/` as the single authoritative source of truth for all numerical values.
- Verified that all active reports read exclusively from canonical predictions (`canonical_results.csv`).
- Preserved historical reports in `audit/` and `legacy/` while explicitly designating them non-authoritative.
- Maintained strict quarantine over legacy synthetic human responses in `annotation/quarantine/`.
