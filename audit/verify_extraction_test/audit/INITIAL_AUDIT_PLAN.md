# INITIAL AUDIT PLAN: CROSS-LINGUAL CLAIM VERIFICATION RESEARCH

**Date:** 2026-10-19  
**Auditor:** Antigravity Autonomous Research & Methodology Specialist  
**Target Repository:** `research-crosslingual-rag`  
**Base Commit / Branch:** `research-improvement-v2` (derived from `30b489a`)  
**Specification:** `ANTIGRAVITY_RESEARCH_IMPROVEMENT_AND_FREEZE_PROMPT.md`

---

## 1. Objectives & Scope

The objective of this audit is to conduct an independent, forensic evaluation of the cross-lingual claim verification research project, verifying:
1. **Provenance & Dataset Integrity:** Origin, licensing, and label mappings from the raw X-Fact dataset to the 3-class schema (`SUPPORTED`, `CONTRADICTED`, `INSUFFICIENT_EVIDENCE`).
2. **Label Distribution & Missing Class:** Verify the distribution of veracity labels in dev ($N=103$) and test ($N=163$), specifically investigating whether any gold `SUPPORTED` claims exist.
3. **Paper vs. Artifact Reconciliation:** Systematically audit every quantitative claim in the compiled PDF (`manuscript/main.pdf`), tables, and figures against per-example prediction files (`experiments/results/test_predictions.csv`).
4. **Code vs. Method Discrepancies:** End-to-end trace of baseline and selective checking logic:
   - Posterior averaging vs. direct routing to original evidence.
   - Character slicing (`[:512]`) vs. tokenizer token truncation.
   - Numeral/entity overlap implementation (true Jaccard vs. recall).
   - Latency accounting (verifier inference time vs. end-to-end pipeline including machine translation).
5. **Metric Recomputation & Statistical Validity:**
   - Exact observed point estimates vs. bootstrap mean confusion.
   - Exact paired McNemar test and paired permutation tests for Macro-F1.
   - Disentangling the error attribution taxonomy: resolving the 114 vs. 111 count discrepancy (41 translation + 61 verification + 12 insufficient = 114 vs. 111 errors).
6. **Literature & Novelty Gap:** Independent verification of close prior work (specifically arXiv:2410.10303, XFEVER, XRAG, Multilingual RAG) to determine defensible contributions.

---

## 2. Order of Inspection & Target Artifacts

| Step | Focus Area | Primary Target Files | Output Artifact |
|---|---|---|---|
| **1** | Raw Data & Provenance | `data/raw/dev.all.tsv`, `data/raw/test.all.tsv`, `scripts/acquire_and_process_data.py` | `audit/DATA_AND_LABEL_AUDIT.md`, `data/DATASET_CARD.md`, `data/DATA_PROVENANCE_AND_LICENSES.md` |
| **2** | Per-Example Predictions & Metrics | `experiments/results/test_predictions.csv`, `experiments/results/dev_predictions.csv` | `results/audit_recomputed/`, `audit/RESULTS_REPRODUCTION_REPORT.md` |
| **3** | Error Taxonomy Disentanglement | `scripts/analyze_predictions.py`, `experiments/results/test_error_attribution.csv` | Detailed case-by-case partition in `audit/RESULTS_REPRODUCTION_REPORT.md` |
| **4** | Code vs Declared Method | `scripts/run_verification_experiments.py`, `manuscript/main.tex` | `audit/PAPER_CODE_RECONCILIATION.csv` |
| **5** | Literature & Novelty Audit | Scholarly databases, arXiv, ACL Anthology, arXiv:2410.10303 | `literature/SEARCH_PROTOCOL.md`, `literature/LITERATURE_AUDIT.csv`, `literature/RELATED_WORK_MATRIX.md`, `literature/NOVELTY_ASSESSMENT.md` |
| **6** | Protocol & Annotation Redesign | Redesigning protocol and annotation sheet for bilingual evaluation | `protocol/RESEARCH_PROTOCOL_v1.md`, `protocol/analysis_plan.yaml`, `annotation/` |
| **7** | Corrected Code & Regression Tests | Upgraded scripts with token truncation, true Jaccard, latency accounting | `scripts/`, `tests/` |
| **8** | Research Freeze Gate Evaluation | Assessment of Gates A through E | `RESEARCH_STATUS.md`, `REVIEW_ME_FIRST.md`, Final Package ZIP |

---

## 3. Initial Suspicion Checklist (from `MANUSCRIPT_REVIEW_AND_TACL_READINESS.md`)

- [ ] **S1. Zero Positive (`SUPPORTED`) Examples:** Does the evaluation set lack positive claims entirely? If so, why was 3-class Macro-F1 reported?
- [ ] **S2. Point Estimate vs. Bootstrap Mean:** Did `test_main_results.csv` report bootstrap sample means (e.g., 0.320184) instead of direct observed sample accuracy (52/163 = 0.319018)?
- [ ] **S3. Error Attribution Non-Disjoint Partition:** Why do reported error counts sum to 114 (41 + 61 + 12) when total errors are 111? Are there 3 overlapping cases?
- [ ] **S4. Mathematical Formulation vs. Code:** Does the text claim posterior averaging $\bar{P} = 0.5(P_{\text{trans}} + P_{\text{orig}})$ while the code executes `pred = pred_original`?
- [ ] **S5. Numeral/Entity Overlap Metric:** Does the code compute $|N_{\text{claim}} \cap N_{\text{ev}}| / |N_{\text{claim}}|$ (directional recall) rather than true Jaccard similarity $|N_1 \cap N_2| / |N_1 \cup N_2|$?
- [ ] **S6. Truncation Defect:** Does `[:512]` slice 512 Python string characters rather than 512 BPE tokens?
- [ ] **S7. Latency Underreporting:** Does reported inference latency (e.g., 78.4 ms) omit the machine translation stage (Opus-MT runtime)?
- [ ] **S8. Prior Literature & Novelty:** Is arXiv:2410.10303 an existing paper? What did it prove about translation bias in multilingual LLMs?

Execution begins immediately with Phase 1.
