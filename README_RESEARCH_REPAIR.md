# RESEARCH REPAIR AND VALIDITY REPORT (CANDIDATE V3)

**Project:** Evidence-Grounded Cross-Lingual Claim Verification Diagnostic Study (Hindi $\rightarrow$ English)  
**Date:** 2026-10-19  
**Version:** Freeze Candidate V3 (`NOT_FROZEN`)  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Status:** **NOT FROZEN** (Gate C BLOCKED awaiting genuine bilingual human annotation)

---

## 1. Executive Summary & Audit Response

Following the submission of Freeze Candidate V2, an independent critical audit (`audit/INDEPENDENT_REVIEW_FREEZE_CANDIDATE_V2.md`) identified 9 methodological and reproducibility vulnerabilities. In response, we initiated a ground-up critical repair workflow adhering strictly to `ANTIGRAVITY_CANDIDATE_V2_CRITICAL_REPAIR_PROMPT.md`.

This package delivers:
1. **Zero Path Assumptions (100% Portable):** All hardcoded paths (e.g., `C:\Users\...`) have been completely eliminated from all scripts and test suites.
2. **Methodological Validity & Task Scoping:** Formally addressed the absence of positive (`SUPPORTED`) claims in the evaluated Hindi X-Fact split (Dev: 89 refutations, 14 unverified; Test: 142 refutations, 21 unverified). Formally adopted **Option C** in `protocol/TASK_AND_LABEL_VALIDITY_DECISION.md`, bounding all findings to refutation and nuance detection under observed distributions, and reporting both 3-class and 2-class Macro F1.
3. **Genuine Inference Rerun from Scratch:** Completely re-executed the inference pipeline from scratch using true tokenizer-level truncation (`max_length=512`, `truncation=True`) and true Jaccard numeral overlap ($|A \cap B| / |A \cup B|$).
4. **Fair, Per-Instance Latency Accounting:** Replaced static constant MT latency with actual per-instance MarianMT generation times and verifier forward passes on CPU, reporting raw verifier and end-to-end latencies with full variance metrics (mean, median, std, p95).
5. **Rigorously Bounded Literature Audit:** Replaced placeholder IDs with verified citations (e.g., Wang et al., ACL 2026 / `arXiv:2604.20199`; Chang et al., ROCLING 2023 / `2023.rocling-1.1`), and removed all unvetted priority ("first") assertions.
6. **Blinded Annotator Packet Hygiene:** Isolated `annotation_handoff/ANNOTATOR_PACKET.zip` containing strictly blinded data and protocols, completely segregated from internal keys. Kept Gate C **BLOCKED**.
7. **Clean-Room Verification:** Verified that the packaged archive extracts and passes all automated tests in a temporary isolated environment.

---

## 2. Gate-by-Gate Verification Status

| Gate | Focus Area | Status | Evidence / Artifact |
|:---:|:---|:---:|:---|
| **Gate A** | Task & Label Validity | **REPAIRED** | `protocol/TASK_AND_LABEL_VALIDITY_DECISION.md` (Scoped to observed 2-class veracity; dual-F1 reporting) |
| **Gate B** | Literature Audit & Novelty | **PASS (BOUNDED)** | `literature/LITERATURE_AUDIT.csv`, `literature/NOVELTY_ASSESSMENT.md` (Verified IDs, removed "first" claims) |
| **Gate C** | Bilingual Human Verification | **BLOCKED** | `annotation_handoff/ANNOTATOR_PACKET.zip` (Requires genuine human annotators; 0/50 complete) |
| **Gate D** | Inference, Tuning & Ablations | **PASS** | `experiments/results_corrected/` (Scratch inference, dev-only tuning, real latency, 9 ablations) |
| **Gate E** | Portability & Reproduction | **PASS** | `scripts/package_freeze_candidate_v3.py` (Clean-room extraction test passes completely) |

**Overall Research Status:** **NOT FROZEN** (Blocked on Gate C). The archive is intentionally designated `CROSS_LINGUAL_RAG_RESEARCH_FREEZE_CANDIDATE_V3_NOT_FROZEN.zip`.

---

## 3. Directory Layout and Key Artifacts

```
.
├── BLOCKER_LEDGER.csv                     # Ledger tracking all 9 audit issues and resolutions
├── README_RESEARCH_REPAIR.md              # This document
├── RESEARCH_STATUS.md                     # Gate-by-gate verification report
├── requirements.txt                       # Locked dependencies
├── protocol/
│   ├── TASK_AND_LABEL_VALIDITY_DECISION.md# Formulation options, bounds, and runtime id2label verification
│   ├── analysis_plan.yaml                 # Reconciled protocol, tuning grid, and seeds
│   └── RESEARCH_PROTOCOL_v1.md            # Formal research protocol
├── literature/
│   ├── LITERATURE_AUDIT.csv               # 11 audited and verified literature entries
│   ├── RELATED_WORK_MATRIX.md             # Feature-by-feature comparison matrix
│   └── NOVELTY_ASSESSMENT.md              # Bounded contribution and defensibility analysis
├── data/
│   ├── raw/                               # Raw X-Fact TSVs (dev.all.tsv, test.all.tsv)
│   ├── processed/                         # Filtered Hindi subsets (dev.jsonl, test.jsonl)
│   ├── DATA_USE_AND_LICENSE_NOTES.md      # Multi-tier IP, dataset, model, and code licenses
│   ├── DATASET_CARD.md                    # Dataset card
│   └── DATA_PROVENANCE_AND_LICENSES.md    # Provenance details
├── experiments/
│   ├── results_corrected/                 # CANONICAL OUTPUTS FROM SCRATCH RERUN
│   │   ├── corrected_dev_predictions.csv
│   │   ├── corrected_test_predictions.csv
│   │   ├── corrected_dev_tuning.csv
│   │   ├── corrected_full_benchmark_and_ablations.csv
│   │   ├── corrected_statistical_tests.csv
│   │   ├── corrected_error_attribution.json
│   │   └── corrected_latency_summary.json
│   └── results/                           # Legacy results (preserved for provenance)
├── legacy/                                # Quarantined exploratory files
│   └── README_LEGACY.md                   # Explicit quarantine disclaimer
├── annotation_handoff/
│   ├── ANNOTATOR_PACKET.zip               # Clean annotator packet (NO leaked keys)
│   ├── README_ANNOTATOR.md
│   ├── HUMAN_ANNOTATION_GUIDELINES.md
│   ├── ANNOTATION_PROTOCOL.md
│   ├── annotation_sample_blinded.csv
│   └── annotation_submission_template.csv
├── annotation/
│   └── internal_audit_sampling_key.csv    # Private key for post-hoc unblinding
├── scripts/                               # Portable reproduction scripts
│   ├── run_corrected_experiments.py       # Full scratch inference and ablation pipeline
│   ├── package_freeze_candidate_v3.py     # Packaging and clean-room test script
│   └── ...
└── tests/                                 # Automated test suite
    ├── run_all_tests.py                   # Master test runner
    ├── test_data_integrity.py             # Data schema and partition tests
    ├── test_method_logic.py               # Numeral Jaccard and routing tests
    ├── test_metrics_and_partitions.py     # Partition and McNemar tests
    └── test_corrected_pipeline.py         # Corrected output verification tests
```

---

## 4. Autonomous Reproduction Instructions

To reproduce all findings from scratch in a fresh Python virtual environment:

```bash
# 1. Activate environment and install dependencies
pip install -r requirements.txt

# 2. Run test suite to verify baseline integrity
python tests/run_all_tests.py

# 3. Run corrected inference, dev threshold tuning, and ablations from scratch
python scripts/run_corrected_experiments.py

# 4. Package candidate and verify clean-room extraction
python scripts/package_freeze_candidate_v3.py
```
