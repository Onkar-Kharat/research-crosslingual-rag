# Cross-Lingual Evidence Verification: Research Freeze Package

**Status:** **FROZEN — EXPLORATORY COMPUTATIONAL STUDY**  
**Version:** Final Reproducible Research Freeze  
**Date:** October 2026  
**Canonical Status Ledger:** `FREEZE_GATE_REPORT.md` (Single Authoritative Source of Truth)  
**Deliverable Archive:** `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip`  
**Adopted Scope:** Option C (Cross-Lingual Verifier Prediction Sensitivity and Routing Disagreement Under Translation Shift)  
**Corpus / Benchmark:** X-Fact (Hindi Subset, $N=266$ authentic fact-checks; $N_{\text{dev}}=103$, $N_{\text{test}}=163$)

---

## 1. Executive Summary

This repository contains the complete experimental artifacts, audit reports, protocols, dataset cards, canonical predictions, and regression test suites for cross-lingual claim evidence verification under translation shift.

The study investigates:
1. **Diagnostic Outcome Strata:** Disentangling prediction behavior between translated evidence and original Hindi evidence under representation shift.
2. **Selective Evidence Routing:** Evaluating a risk-driven gate (`Selective-Check`, $\tau^*=0.650$ tuned on dev data) that routes uncertain or numeral-mismatched claims back to original Hindi evidence, evaluating trade-offs across accuracy, Macro-F1, and end-to-end CPU latency against key baselines (`Translated-Only`, `Original-Only`, `Always-Check`, and a 100-seed matched-coverage `Random-Control`).
3. **Utility Optimality on Dev:** Honest disclosure that No-Check achieves higher development utility ($J = 0.2104$) than the cascade ($J = 0.2023$). Selective cascade routing is not Pareto-optimal on development data.
4. **Authenticity:** Quarantined all simulated human annotations in `audit/invalidated_synthetic_annotations/`. Under Option C, human annotation is marked as future work and causal translation claims are excluded.


---

## 2. Directory Structure and File Map

```text
├── REVIEW_ME_FIRST.md           <- Comprehensive reviewer handoff guide (Start here!)
├── RESEARCH_STATUS.md           <- Gate-by-gate PASS / BLOCKED assessment
├── DECISION_LOG.md              <- Chronological log of 8 methodological decisions
├── README_RESEARCH_FREEZE.md    <- This reproduction guide and directory map
├── requirements.txt             <- Python dependencies
├── audit/
│   ├── input_manifest.csv       <- Checksums and metadata of all input files
│   ├── PROJECT_INVENTORY.md     <- Categorized inventory of all project files
│   ├── INITIAL_AUDIT_PLAN.md    <- Order of forensic checks
│   ├── environment_report.json  <- Machine environment (CPU, RAM, PyTorch, OS)
│   ├── DATA_AND_LABEL_AUDIT.md  <- Forensic audit of X-Fact raw data & missing class
│   ├── PAPER_CODE_RECONCILIATION.csv <- Line-by-line audit of 15 paper claims vs code
│   └── RESULTS_REPRODUCTION_REPORT.md <- Recomputed tables, CIs, tests, and confusion matrices
├── literature/
│   ├── SEARCH_PROTOCOL.md       <- Database search parameters and queries
│   ├── LITERATURE_AUDIT.csv     <- 11 verified related works with DOIs and findings
│   ├── RELATED_WORK_MATRIX.md   <- Nearest-neighbor comparison across 6 dimensions
│   └── NOVELTY_ASSESSMENT.md    <- Defensible contribution bounding vs. prior art
├── protocol/
│   ├── RESEARCH_PROTOCOL_v1.md  <- Formal experimental protocol and hypotheses
│   └── analysis_plan.yaml       <- Machine-readable configuration of analysis
├── data/
│   ├── DATASET_CARD.md          <- Dataset documentation and class balance
│   ├── DATA_PROVENANCE_AND_LICENSES.md <- Provenance, MIT license, and file hashes
│   ├── raw/                     <- Raw X-Fact TSVs (dev.all.tsv, test.all.tsv)
│   └── processed/               <- Filtered Hindi instances (JSONL) with translations
├── annotation/
│   ├── ANNOTATION_GUIDE.md      <- Guidelines for bilingual human annotators
│   ├── ANNOTATION_PROTOCOL.md   <- Sampling, blinding, and adjudication rules
│   ├── blinded_annotation_sample.csv <- 50 blinded items awaiting human review
│   ├── internal_audit_sampling_key.csv <- Sampling strata key for audit
│   └── HUMAN_ANNOTATION_REPORT.md <- Status of human annotation (Incomplete)
├── experiments/
│   ├── experiment_ledger.csv    <- Record of experimental runs
│   ├── results/                 <- Baseline prediction CSVs (dev, test)
│   └── results_corrected/       <- Corrected benchmark and ablation results
├── results/
│   └── audit_recomputed/        <- Recomputed metrics, confusion matrices, and tests
├── scripts/
│   ├── phase0_intake.py         <- Intake, hashing, and inventory script
│   ├── phase1_recompute_all.py  <- Exact point estimates, CIs, McNemar & permutation tests
│   ├── run_corrected_experiments.py <- Corrected token truncation and True Jaccard pipeline
│   ├── generate_full_ablations.py <- Full benchmark and ablation generator
│   └── analyze_human_annotations.py <- Inter-rater agreement and validation script
└── tests/
    ├── test_data_integrity.py   <- Unit tests for splits, schemas, and missing class
    ├── test_method_logic.py     <- Unit tests for True Jaccard, risk, and routing
    ├── test_metrics_and_partitions.py <- Unit tests for disjoint error partition & McNemar
    ├── run_all_tests.py         <- Test runner
    ├── test_report.json         <- Machine-readable test execution report
    └── TEST_REPORT.md           <- Summary test report (12/12 passing)
```

---

## 3. Quick Reproduction Instructions

### Step 1: Set Up Python Virtual Environment
```bash
python -m venv .venv
# On Windows:
.\.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### Step 2: Run Automated Regression Tests
Verify all data schemas, splits, mathematical formulas, and disjoint partitions:
```bash
python tests/run_all_tests.py
```
*(All 12 unit tests should pass with status OK).*

### Step 3: Reproduce Exact Evaluation Metrics and Statistical Tests
Recompute exact observed point estimates, 95% bootstrap intervals, McNemar tests, permutation tests, and disjoint error partitions:
```bash
python scripts/phase1_recompute_all.py
```
Outputs will be written to `results/audit_recomputed/`.

### Step 4: Reproduce Full Benchmark and Ablation Suite
Generate the full 9-condition benchmark (No-Check, Direct Multilingual, Always-Check, Selective-Check, Triggered Averaging, Uncertainty-Only, Numeral-Only, Random Routing, and Oracle):
```bash
python scripts/generate_full_ablations.py
```
Outputs will be written to `experiments/results_corrected/full_benchmark_and_ablations.csv`.

---

## 4. Known Scientific Limitations
1. **Unrepresented Positive Class:** The dataset contains 0 gold `SUPPORTED` claims. Systems must be evaluated on observed 2-class metrics (`CONTRADICTED` and `INSUFFICIENT_EVIDENCE`) alongside standard 3-class NLI metrics.
2. **Prior Test Set Exposure:** The held-out test set ($N=163$) was evaluated during initial exploration. Although threshold $\tau^* = 0.30$ was tuned strictly on dev data, this test set cannot be claimed as an untouched virgin evaluation set.
3. **Pending Human Adjudication:** Causal attribution of the 41 translation-recovered errors requires completion of the blinded bilingual annotation sheet (`annotation/blinded_annotation_sample.csv`).
