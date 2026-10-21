# Step-by-Step Reproduction from Clean Extraction

**Protocol Version:** `v1.0-observational`  
**Package:** `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip`  
**Certification Status:** `COMPUTATIONAL RESULTS FROZEN — EXPLORATORY; HUMAN ANNOTATION PENDING`  
**Date:** 2026-10-22  

---

## 1. Prerequisites and Environment Setup

This research package is portable and self-contained. It can be verified on Windows 10/11, macOS, and Linux (Ubuntu 22.04+).

### 1.1 Python Environment
- Python 3.10 to 3.14 (Verified on Python 3.14.7, 64-bit AMD64).
- Virtual environment creation:
```bash
# Extract the archive into a clean directory
unzip CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip -d research_clean
cd research_clean

# Create and activate virtual environment
python -m venv .venv

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Windows (Command Prompt):
.venv\Scripts\activate.bat
# On Linux / macOS:
source .venv/bin/activate
```

### 1.2 Dependencies
Install the required lightweight statistical, scientific, and testing packages:
```bash
pip install -r requirements.txt
```
*Note: Full model re-inference requires PyTorch (`torch>=2.0`) and Hugging Face Transformers (`transformers>=4.30`). All raw, per-instance model predictions from the canonical run are included in `experiments/results_canonical/` so the full statistical reproduction, metric recomputation, and test suite do NOT require downloading multi-gigabyte neural checkpoints.*

---

## 2. Integrity and Checksum Verification

Verify file integrity against the SHA-256 manifest:

### On Linux / macOS:
```bash
sha256sum -c FINAL_PASS/SHA256SUMS.txt
```

### On Windows (PowerShell):
```powershell
Get-Content FINAL_PASS/SHA256SUMS.txt | ForEach-Object {
    $hash, $file = $_ -split '\s+', 2
    if ($file -and (Test-Path $file)) {
        $actual = (Get-FileHash -Algorithm SHA256 $file).Hash.ToLower()
        if ($actual -eq $hash.ToLower()) {
            Write-Host "OK: $file" -ForegroundColor Green
        } else {
            Write-Host "FAILED: $file (Expected $hash, got $actual)" -ForegroundColor Red
        }
    }
}
```

---

## 3. Comprehensive Test Suite Execution

Run the consolidated automated verification test suite (8 test modules covering 42 tests):
```bash
python tests/run_all_tests.py
```
**Expected Output:**
```text
Ran 42 tests in < 1.0s
OK
Wrote test reports to tests/TEST_REPORT.md and reproducibility/TEST_REPORT.md
```

### Coverage of the 42 Tests:
1. `TestDataIntegrity` (5 tests): Dataset splits, zero data leakage across train/dev/test, label mapping, sample sizes (dev=103, test=163), missing positive class audit.
2. `TestMethodLogic` (4 tests): Numeral extraction (Arabic & Devanagari), true Jaccard similarity, risk score bounds $[0, 1]$, routing logic.
3. `TestLogicHelpers` (8 tests): McNemar symmetry, Benjamini-Hochberg FDR monotonicity, exact matched-count random routing draw.
4. `TestCorrectedPipeline` (4 tests): Verification of canonical prediction files, real measured latency schema, token-based truncation metadata, dev-only tuning artifacts.
5. `TestAnnotationIntegrity` (5 tests): Quarantine of legacy synthetic annotations, absence of filled submissions in handoff packets, guard asserting non-execution of synthetic annotation.
6. `TestAnnotationWorkflow` (5 tests): Packet file existence, zero prediction leakage, submission validator rejection of invalid files, acceptance of valid QA fixture, Cohen's kappa calculation accuracy.
7. `TestMetricsAndPartitions` (3 tests): Disjoint error partitioning ($S_{\text{trans}} \cap S_{\text{verif}} = \emptyset$), observed accuracy calculations, exact binomial McNemar properties.
8. `TestReproducedArtifactsV4` (8 tests): Benchmark table reconciliation, probability simplex compliance ($\sum p_i = 1.0$), multi-seed random control properties, latency arithmetic.

---

## 4. Recomputing Canonical Metrics and Generating Figures

To independently re-derive all canonical tables and figures directly from the raw per-instance model predictions:

### 4.1 Recompute Metrics Table and Sensitivity Statistics:
```bash
python scripts/compute_evaluation_metrics_corrected.py
```
Outputs regenerated:
- `experiments/results_canonical/test_metrics.json`
- `experiments/results_canonical/test_metrics_table.csv`
- `experiments/results_canonical/paired_comparison_tests.json`
- `experiments/results_canonical/random_routing_control_summary.json`

### 4.2 Regenerate Figures:
```bash
python scripts/generate_corrected_figures.py
```
Outputs regenerated:
- `reports/figures/figure1_architecture.png`
- `reports/figures/figure2_pareto_frontier.png`
- `reports/figures/figure3_risk_distribution.png`
- `reports/figures/figure4_confusion_matrices.png`
- `reports/figures/figure5_error_overlap.png`
- `reports/figures/figure6_disagreement_breakdown.png`

---

## 5. Testing the Annotation Tooling

Verify that the blinded human annotation packets, validator, and agreement analysis scripts function end-to-end using the synthetic QA fixtures:

### 5.1 Test Submission Validator:
```bash
# Test with valid QA fixture submissions:
python annotation_tool/scripts/validate_submissions.py \
  --file1 annotation_tool/tests/fixtures/valid_submission_A1.json \
  --file2 annotation_tool/tests/fixtures/valid_submission_A2.json
```
**Expected Output:**
```text
Validation PASSED: Both submission files are valid and ready for agreement analysis.
```

### 5.2 Test Inter-Annotator Agreement Analysis:
```bash
python annotation_tool/scripts/analyze_agreement.py \
  --file1 annotation_tool/tests/fixtures/valid_submission_A1.json \
  --file2 annotation_tool/tests/fixtures/valid_submission_A2.json \
  --key annotation_tool/internal_analysis_key.csv \
  --out_dir test_qa_analysis/
```
**Expected Output:**
```text
Successfully wrote agreement report and disagreement queue to test_qa_analysis/
```

### 5.3 Launch the Local Annotation App:
```bash
python annotation_tool/app/launch_app.py
```
Opens `http://localhost:8080` in the default browser. Annotators can also double-click `annotation_tool/app/index.html` directly without a server.

---

## 6. Verifying Canonical Results Against Reported Values

Compare the regenerated `experiments/results_canonical/test_metrics.json` against `FINAL_PASS/CANONICAL_VALUES_TABLE.csv`:

| Metric | Condition | Canonical Value | 95% Confidence Interval | Source File |
|---|---|---|---|---|
| **Paired Agreement** | Original Hi vs Translated En | **36.20%** (59/163) | [29.22%, 43.81%] | `experiments/results_canonical/test_metrics.json` |
| **Paired Disagreement** | Original Hi vs Translated En | **63.80%** (104/163) | [56.19%, 70.78%] | `experiments/results_canonical/test_metrics.json` |
| **Observed Accuracy** | No-Check Baseline | **28.22%** (46/163) | [21.90%, 35.53%] | `experiments/results_canonical/test_metrics_table.csv` |
| **Observed Accuracy** | Selective-Check ($\tau^*=0.650$) | **28.22%** (46/163) | [21.90%, 35.53%] | `experiments/results_canonical/test_metrics_table.csv` |
| **Observed Accuracy** | Direct Multilingual | **42.94%** (70/163) | [35.57%, 50.63%] | `experiments/results_canonical/test_metrics_table.csv` |
| **Consultation Coverage** | Selective-Check | **7.98%** (13/163) | [4.71%, 13.15%] | `experiments/results_canonical/test_metrics_table.csv` |
| **End-to-End Latency** | No-Check | **3,650.4 ms** | [3,480.0, 3,820.0] ms | `experiments/results_canonical/test_metrics_table.csv` |
| **End-to-End Latency** | Selective-Check | **4,613.8 ms** | [4,420.0, 4,810.0] ms | `experiments/results_canonical/test_metrics_table.csv` |
| **Development Utility** | No-Check ($Coverage=0$) | **$J = 0.2104$** | — | `experiments/results_canonical/dev_threshold_sweep.json` |
| **Development Utility** | Cascade Peak ($\tau^*=0.650$) | **$J = 0.2023$** | — | `experiments/results_canonical/dev_threshold_sweep.json` |

---

## 7. Troubleshooting and Environment Notes

1. **Path Separators:** All scripts use `pathlib.Path` or `os.path.join` and are cross-platform compatible.
2. **Missing Dependencies:** If `scipy` or `sklearn` are missing, install them via `pip install scipy scikit-learn pandas numpy`.
3. **No GPU Required:** All verification tests and canonical metric recalculations run entirely on CPU in $< 2$ seconds.
