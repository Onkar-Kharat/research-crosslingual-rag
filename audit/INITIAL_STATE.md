# AUDIT REPORT: Initial Repository State and Archive Protection

**Audit Date:** October 2026  
**Auditor:** Senior NLP Researcher, Experimental-Methodology Auditor, & Research-Integrity Auditor  
**Project:** Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Starting Archive:** `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip`  
**Starting Archive SHA-256:** `9e1ef3badfe84ee1c30f70155bc26ca9a797fddec1d50fe3f36cb6928ab47ab8`  

---

## 1. Archive Protection and Baseline Provenance

Before performing any repository modifications, the initial starting state was verified and preserved:
1. **Archive Preservation:** The baseline archive `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip` was verified on disk and its SHA-256 cryptographic checksum recorded:
   ```
   9e1ef3badfe84ee1c30f70155bc26ca9a797fddec1d50fe3f36cb6928ab47ab8
   ```
2. **Untouched Extraction Copy:** An untouched baseline extraction was maintained in `audit/extracted_original/` to ensure full forensic traceability back to the starting state.
3. **Repository Inventory:** A complete recursive file inventory was recorded in `audit/FILE_INVENTORY.csv`, classifying all files into Authoritative, Historical/Superseded, Data Provenance, Environment, or Audit categories.

---

## 2. File Classification and Authority Taxonomy

| Category | Typical Paths | Authority Level | Description & Handling |
|:---|:---|:---:|:---|
| **Authoritative Canonical Outputs** | `experiments/results_canonical/` | **AUTHORITATIVE** | The single source of truth for all final metrics, tables, figures, and manifests. |
| **Authoritative Protocol & Configs** | `protocol/`, `experiments/configs/` | **AUTHORITATIVE** | Frozen analysis plan, scoping documents, and model hyperparameters. |
| **Data Provenance & Splits** | `data/raw/`, `data/processed/` | **AUTHORITATIVE** | Authentic X-Fact raw TSVs, processed Hindi splits ($N=103$ dev, $N=163$ test). |
| **Regression Test Suite** | `tests/` | **AUTHORITATIVE** | 8 test modules covering 43 unit and integrity tests (all passing). |
| **Bilingual Human Annotation Tool** | `annotation_tool/` | **AUTHORITATIVE INFRASTRUCTURE** | Standalone offline application and blinded packets; submissions pending. |
| **Audit and Forensic Documentation** | `audit/` | **AUTHORITATIVE AUDIT** | Complete methodology reports, statistical reanalyses, and lineage ledgers. |
| **Historical & Superseded Artifacts**| `experiments/results/`, `experiments/results_corrected/`, `audit/invalidated_synthetic_annotations/` | **SUPERSEDED / NON-AUTHORITATIVE** | Preserved strictly for lineage history; clearly marked superseded. |

---

## 3. Initial Baseline Audit Findings

1. **Duplicated-Claim in Evidence:** Traced directly to the raw upstream X-Fact dataset (`data/raw/dev.all.tsv` 54/103; `data/raw/test.all.tsv` 88/163) due to Google search snippets capturing fact-checking article headlines. Verified as an intrinsic benchmark property.
2. **Statistical Discrepancy:** Recomputed paired contingency tables from raw predictions, proving mathematically that $b=23, c=47$ is the true underlying count for $\chi^2 = 7.5571, p = 0.00558$, while $b=7, c=31$ was an earlier transcription error.
3. **Pipeline Output Destination:** Resolved ambiguity between `results_corrected/` and `results_canonical/` by making `experiments/results_canonical/` the direct output destination.
4. **Development Label Counts:** Corrected protocol typo from 86/17 to actual verified split counts 89 `CONTRADICTED` and 14 `INSUFFICIENT_EVIDENCE`.
5. **Reference Integrity:** Verified and generated all referenced companion files (`test_predictions.jsonl`, `test_metrics.json`, `dev_threshold_sweep.json`).
