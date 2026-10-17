# Initial Repository State Audit

**Project:** Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Audit Date:** 2026-10-24  
**Auditor Role:** Senior NLP Researcher, Experimental-Methodology Auditor, Reproducibility Reviewer  
**Initial Reference Archive:** `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip`  
**Reference Archive SHA-256:** `c498c6eb27f7ae0dba8a1cd9e7fa725a1f72885bc51dc113d36092aff7db3167`  

---

## 1. Initial State Inventory

Upon initiating this complete final audit and cleanup pass, the repository was inspected across all top-level and recursive directories.

### 1.1 Directory Breakdown and File Counts
- **Total Tracked Files:** 539 files
- **Root Documents:** Active prompt files, master status reports, license/gitignore, and historical ZIP candidates (`v1` through `v6`).
- **Core Computational Folders:**
  - `data/splits/`: Preprocessed, paired Hindi fact verification instances (`hindi_dev.jsonl` $N=103$, `hindi_test.jsonl` $N=163$).
  - `experiments/results_canonical/`: Authoritative canonical outputs (`canonical_dev_predictions.csv`, `canonical_test_predictions.csv`, `canonical_benchmark_table.csv`, `canonical_dev_tuning.csv`, `canonical_statistical_tests.csv`, `canonical_random_control_100seeds.csv`, `RUN_MANIFEST.json`).
  - `scripts/`: Production execution scripts (`run_corrected_experiments.py`, `compute_evaluation_metrics_corrected.py`, `generate_publication_figures.py`, `package_freeze_candidate_v6.py`).
  - `tests/`: Consolidated regression test suite (`run_all_tests.py`, 8 test modules covering 42 tests).
  - `annotation_tool/`: Complete offline human annotation workflow (`app/index.html`, `packets/PACKET_A_HANDOFF.zip`, `packets/PACKET_B_HANDOFF.zip`, `scripts/validate_submissions.py`, `scripts/analyze_agreement.py`).
  - `audit/`: Forensic audit reports, lineage ledgers, and historical issue tracking.
  - `literature/`: Literature audit (`LITERATURE_AUDIT.csv`, 11 peer-reviewed primary citations).

### 1.2 Initial Integrity Verification
1. **Human Annotation State:** Confirmed that `annotation/results/` contains no active synthetic human judgments. The legacy simulated outputs are safely isolated in `annotation/quarantine/` and `audit/invalidated_synthetic_annotations/`.
2. **Computational Reproducibility:** Canonical predictions reproduce the exact reported values:
   - Paired Agreement: 36.20% (59/163)
   - Paired Disagreement: 63.80% (104/163)
   - Translated SUP to Original CON: 48.44% (31/64)
   - No-Check Accuracy: 28.22% (46/163)
   - Selective-Check Accuracy ($\tau^*=0.650$): 28.22% (46/163), Coverage: 7.98% (13/163)
   - Direct Multilingual Accuracy: 42.94% (70/163)
3. **Threshold Selection Lineage:** Dev sweep confirmed $\tau^*=0.650$ is selected dev-only under $J(\tau) = \text{MacroF1}_{\text{dev}} - 0.20 \cdot \text{Coverage}_{\text{dev}}$, and Dev No-Check achieves $J=0.2104 > J=0.2023$ (a documented negative result).

---

## 2. Identified Deficiencies Requiring Finalization

1. **Test Environment Portability:**
   - `tests/test_method_logic.py` imported directly from `scripts/run_corrected_experiments.py`, which had top-level imports of `torch` and `transformers`. In minimal environments lacking these heavy dependencies, the test crashed on import.
   - *Resolution:* Made `torch` and `transformers` graceful at import time in `scripts/run_corrected_experiments.py` and added a resilient fallback in `tests/test_method_logic.py`.
2. **Historical Metrics Discrepancy Documentation:**
   - Previous audit notes reported a discrepancy between 28.22% at $\tau=0.650$ (canonical v4-v6) and 39.26% at $\tau=0.30$ (historical v2/v3). This required formal documentation and reconciliation in `audit/RESULTS_RECONCILIATION.md`.
3. **Consolidation of Audit Artifacts:**
   - The master prompt requests explicit files in the `audit/` subdirectory (`audit/FILE_INVENTORY.csv`, `audit/CHANGELOG.md`, `audit/ISSUES_AND_FIXES.csv`, `audit/FROZEN_PROTOCOL.md`, `audit/DATA_AND_LABEL_AUDIT.md`, `audit/METHOD_AND_THRESHOLD_AUDIT.md`, `audit/METRIC_AND_COST_AUDIT.md`, `audit/RESULTS_RECONCILIATION.md`, `audit/TEST_AND_REPRODUCTION_REPORT.md`, `audit/RELATED_WORK_AND_NOVELTY_AUDIT.md`, `audit/ANNOTATION_AUDIT.md`, `audit/ANNOTATION_HANDOFF.md`, `audit/LIMITATIONS.md`, `audit/FREEZE_DECISION.md`, `audit/FREEZE_MANIFEST.md`).
   - These must be comprehensively authored and reconciled to ensure 100% internal consistency.
