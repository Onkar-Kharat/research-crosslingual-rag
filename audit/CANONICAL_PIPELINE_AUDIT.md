# AUDIT REPORT: Canonical Results Pipeline and Directory Architecture

**Audit Date:** October 2026  
**Auditor:** Senior Methodology & Computational Reproducibility Auditor  
**Repository:** Cross-Lingual Evidence Verification  
**Status:** UNIFIED, VALIDATED, & VERIFIED  

---

## 1. Issue Description & Historical Context

A previous audit identified an architectural ambiguity in the experimental workflow:
- The main experimental pipeline `scripts/run_corrected_experiments.py` wrote its outputs to `experiments/results_corrected/`.
- Meanwhile, documentation, manifests, and freeze protocols treated `experiments/results_canonical/` as the authoritative source of truth.
- A promotion script `scripts/build_canonical_manifest.py` copied files from `results_corrected/` to `results_canonical/`, creating redundant file copies and potential risk of stale file drift.

---

## 2. Definitive Single Pipeline Architecture

We have eliminated all pipeline ambiguity by establishing **one clear, authoritative canonical pipeline**:

```
[Processed Data] 
  ├── data/processed/dev.jsonl (N=103)
  └── data/processed/test.jsonl (N=163)
        │
        ▼
[Execution Script] ──> scripts/run_corrected_experiments.py
        │
        ├── Step 1: Run Dev Inference & Extract Risk Features
        ├── Step 2: Tune Tau exclusively on Dev (J = MacroF1 - 0.15 * Cov => tau* = 0.650)
        ├── Step 3: Single-Pass Exploratory Evaluation on Test (tau* frozen)
        └── Step 4: Write Outputs DIRECTLY to Canonical Destination
        │
        ▼
[Authoritative Destination] ──> experiments/results_canonical/
        ├── canonical_dev_predictions.csv
        ├── canonical_dev_tuning.csv
        ├── canonical_test_predictions.csv
        ├── test_predictions.jsonl (companion format)
        ├── dev_threshold_sweep.json (companion format)
        ├── test_metrics.json (companion format)
        ├── canonical_benchmark_table.csv
        ├── canonical_statistical_tests.csv
        ├── canonical_random_control_100seeds.csv
        ├── canonical_latency_summary.json
        ├── canonical_error_attribution.json
        ├── RUN_MANIFEST.json (input/output hashes & environment)
        └── figures/ (vector PDF and PNG visualizations)
```

---

## 3. Script Modifications & Refactorings

1. **`scripts/run_corrected_experiments.py`:**
   - Modified `RES_DIR` from `WORKSPACE / "experiments" / "results_corrected"` to:
     ```python
     RES_DIR = WORKSPACE / "experiments" / "results_canonical"
     ```
   - All predictions, benchmark tables, and significance tests write directly to `experiments/results_canonical/`.

2. **`scripts/generate_publication_figures.py`:**
   - Modified to read directly from `experiments/results_canonical/`:
     ```python
     tuning_csv = WORKSPACE / "experiments" / "results_canonical" / "canonical_dev_tuning.csv"
     benchmark_csv = WORKSPACE / "experiments" / "results_canonical" / "canonical_benchmark_table.csv"
     attr_json = WORKSPACE / "experiments" / "results_canonical" / "canonical_error_attribution.json"
     ```

3. **`scripts/build_canonical_manifest.py`:**
   - Refactored to operate directly within `experiments/results_canonical/`.
   - Programmatically asserts the presence and non-emptiness of all expected files.
   - Computes SHA-256 hashes of all inputs, models, environment parameters, and canonical outputs in place.
   - Saves the cryptographic audit trail to `experiments/results_canonical/RUN_MANIFEST.json`.

4. **`scripts/generate_canonical_companion_files.py`:**
   - Dedicated serialization script ensuring 100% schema consistency between CSV and JSON/JSONL artifacts.
   - Generates `test_predictions.jsonl`, `test_metrics.json`, and `dev_threshold_sweep.json` directly in `experiments/results_canonical/`.

---

## 4. Designation of Alternative Output Folders

| Directory Path | Role | Status | Retention Policy |
|:---|:---|:---:|:---|
| **`experiments/results_canonical/`** | **Primary Canonical Truth** | **AUTHORITATIVE** | Packaged in Release ZIP; referenced by all papers & reports |
| `experiments/results_corrected/` | Historical Staging Directory | SUPERSEDED | Labeled non-authoritative; retained for lineage transparency |
| `experiments/results/` | Initial Exploratory Outputs (v1 $\tau=0.30$) | SUPERSEDED / HISTORICAL | Preserved strictly for audit history; never referenced in final results |

---

## 5. Input Provenance, Configurations, and Hashes

All outputs in `experiments/results_canonical/` are deterministically reproducible from the following frozen inputs:

| Artifact Name | Path | SHA-256 Hash |
|:---|:---|:---|
| Raw Dev TSV | `data/raw/dev.all.tsv` | `b49f99ea0fc0a9e7eaae584f27a6e700a0ca97ef05c754d929424c803ce5fc7b` |
| Raw Test TSV | `data/raw/test.all.tsv` | `d120967396696dbf5c2e171dc6f82fcddfa143c4c9ff2ca43ba4c7b80a13bc49` |
| Processed Dev JSONL | `data/processed/dev.jsonl` | `8c474f32997aa77e2ff8d99ea56e18f27306db3a726ea7247348981f337fa595` |
| Processed Test JSONL | `data/processed/test.jsonl` | `9d554a9fcbe48b7837775591c28c6eebef057e9545dc67e0e2bb398ebcbfa7d5` |
| Analysis Plan YAML | `protocol/analysis_plan.yaml` | `a65cf2a4efea58d4a4608c0ef0be18b08d4beea60ff0d27ce6c0397ae17c98e1` |

Every canonical file hash is recorded in `experiments/results_canonical/RUN_MANIFEST.json` and validated by automated tests in `tests/test_reproduced_artifacts_v4.py`.
