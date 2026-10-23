# Phase 0: Build Audit and Authoritative Baseline Record

**Date:** 2026-10-24  
**Project Root:** `c:\Users\Onkar\OneDrive\Desktop\Research_crosslingual_rag_research`  
**Current Status:** `FROZEN — EXPLORATORY COMPUTATIONAL STUDY`  
**Primary Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  

---

## 1. Authoritative Repository & Freeze Baseline

| Attribute | Verified Value |
|---|---|
| **Authoritative Project Directory** | `c:\Users\Onkar\OneDrive\Desktop\Research_crosslingual_rag_research` |
| **Authoritative Freeze Archive** | `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip` |
| **Bitwise Synchronized Archive Alias** | `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip` |
| **Archive SHA-256 Hash** | `70fa5148f69cfed661cedec2990ebb7b9b79bd0a50ecb278b8e55d4eb6f5efa5` |
| **Archive Size** | 17,836,204 bytes (17.01 MB compressed; 42.94 MB uncompressed) |
| **Archive File Count** | 406 files (405 manifest files + self-manifest) |
| **Internal File Manifest** | `audit/RELEASE_MANIFEST_SHA256.txt` (405 entries, 100.0% clean-room match) |
| **External Sidecar Checksums** | `audit/RELEASE_CHECKSUM.txt`, `FINAL_PASS/ZIP_RELEASE_CHECKSUM.txt`, `FINAL_PASS_RELEASE_MANIFEST.txt` |
| **Canonical Prediction Record** | `experiments/results_canonical/canonical_test_predictions.csv` ($N=163$) |
| **Canonical Development Tuning** | `experiments/results_canonical/canonical_dev_predictions.csv` ($N=103$, $\tau^*=0.650$) |
| **Authoritative Results Summary** | `canonical_results.csv`, `REVIEWER_HANDOFF/FINAL_RESULTS_INDEX.csv` |
| **Automated Test Suite** | `tests/run_all_tests.py` (47 / 47 passing across 9 modules) |

---

## 2. Inventory of Inspected Project Documentation

The following authoritative documentation files were inspected prior to manuscript drafting and repository reorganization:
1. `README.md`: Verified high-level project framing, 4-way benchmark table, and explicit freeze disclosures.
2. `STATUS.md`: Confirmed status `FROZEN — EXPLORATORY COMPUTATIONAL STUDY` and 47/47 passing tests.
3. `RESEARCH_STATUS.md`: Audited the failure/success partition ($N=117$ failures: $S_{\text{trans}}=51, S_{\text{verif}}=66$; $N=46$ successes: Control=19, $S_{\text{degraded}}=27$) and paired McNemar tests.
4. `FREEZE_GATE_REPORT.md`: Verified the 4 freeze gates (Gate A: Computational integrity PASS; Gate B: Task validity PASS; Gate C: Human annotation BLOCKED/PENDING; Gate D: Report consistency PASS).
5. `audit/RELEASE_VALIDATION_REPORT.md`: Validated clean-room extraction procedure, test log, and hash alignment.
6. `audit/STATISTICAL_REANALYSIS.md`: Audited exact mathematical proofs for contingency denominators:
   - No-Check vs Direct Multilingual: $b=27, c=51, n_{\text{disc}}=78, \chi^2=6.7821, p=0.008772$.
   - Selective-Check vs Direct Multilingual: $b=23, c=47, n_{\text{disc}}=70, \chi^2=7.5571, p=0.005583$.
   - Paired Permutation Test on Macro-F1 ($B=5,000$, Seed=42): $p=0.1898$ (No-Check) and $p=0.1180$ (Selective-Check).
7. `FINAL_PASS/FINAL_RESEARCH_FREEZE_DECISION.md`: Verified freeze criteria, quarantine of simulated human ratings, and scope boundary.
8. `REVIEWER_HANDOFF/FINAL_REVIEW_SUMMARY.md`: Inspected reviewer checklist, claim matrix cross-checks, and benchmark index.

---

## 3. Discrepancies in Historical Draft Files to be Replaced

Inspection of the historical draft in `manuscript/main.tex` and `manuscript/tables/` revealed critical discrepancies requiring complete replacement:
- **Title & Scope Inflation:** Claimed "causal error attribution" and "end-to-end RAG" rather than observational sensitivity of the verifier under pre-retrieved evidence snippets.
- **Test Set Characterization:** Described test partition as an unseen confirmatory holdout; in reality, the test split was previously inspected during exploratory development.
- **Obsolete Metric Values:**
  - Claimed Selective-Check test accuracy of $0.394$ with $\tau^*=0.300$ (historical invalidated run); canonical test accuracy is **$0.2822$ (46/163)** with **$\tau^*=0.650$** tuned on dev.
  - Claimed 41 $E_{\text{trans}}$ and 61 $E_{\text{verif}}$ cases; canonical failure partition ($N=117$) is **$51$ $S_{\text{trans}}$** and **$66$ $S_{\text{verif}}$**, with **$27$ $S_{\text{degraded}}$** and **$19$ Control** successes.
  - Claimed $b=22, c=9$ for Selective vs Always-Check; canonical values are $b=9, c=23$.
- **Undisclosed Class Imbalance:** Omitted the extreme test set skew: 142 `CONTRADICTED` (87.12%), 21 `INSUFFICIENT_EVIDENCE` (12.88%), and 0 `SUPPORTED` (0.0%).
- **Simulated Human Annotation:** Historical drafts cited 96% human agreement, which has been quarantined as synthetic. Active research protocol designates human annotation as **PENDING EXTERNAL PARTICIPANT RECRUITMENT**.

---

## 4. Integrity and Baseline Decisions for Manuscript Development

1. **Empirical Ground Truth:** All numbers in the manuscript, tables, and figures will derive strictly and reproducibly from `canonical_test_predictions.csv`, `canonical_results.csv`, and `test_metrics.json`.
2. **Modularity:** The manuscript is partitioned into standalone LaTeX sections under `docs/manuscript/sections/` and `manuscript/sections/`.
3. **Reproducibility Preservation:** All 47 existing automated unit and regression tests in `tests/` must continue to pass before and after repository reorganization.
4. **Author/Affiliation Anonymity:** In accordance with TACL double-blind review policies, author names, institutions, acknowledgements, and identifying local filesystem paths are strictly excluded.
