# Experiment Lineage and Data Traceability

**Project Title:** Cross-Lingual Evidence Verification: Prediction Sensitivity and Routing Disagreement Under Hindi-to-English Translation Shift  
**Audit Date:** 2026-10-22  
**Protocol Version:** `v1.0-observational`  

---

## 1. End-to-End Pipeline Lineage Diagram

```
[Raw X-Fact Corpus (Hindi Partition)]
        │
        ▼
[Acquisition & Partitioning] ──> scripts/acquire_and_process_data.py
        │
        ├──> data/splits/hindi_dev.jsonl (N=103)
        └──> data/splits/hindi_test.jsonl (N=163)
        │
        ▼
[Paired Inference Execution] ──> scripts/run_corrected_experiments.py
        │
        ├── Model: MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7 (86M)
        ├── MT Engine: Helsinki-NLP/opus-mt-hi-en (MarianMT)
        ├── Tokenizer Policy: Max length 512 tokens (strict truncation)
        └── Latency Logging: High-precision wall-clock timing (ms)
        │
        ▼
[Raw Per-Instance Predictions]
        ├── experiments/results_canonical/canonical_dev_predictions.csv (103 rows)
        └── experiments/results_canonical/canonical_test_predictions.csv (163 rows)
        │
        ▼
[Development Threshold Tuning] ──> scripts/run_corrected_experiments.py
        │
        ├── Grid: tau in [0.30, 0.90] in steps of 0.05
        ├── Objective: J(tau) = MacroF1_dev(tau) - 0.20 * Coverage_dev(tau)
        ├── Baseline Utility: Dev No-Check J = 0.2104
        ├── Cascade Peak: tau* = 0.650, J = 0.2023 (Delta J = -0.0081)
        └── Output: experiments/results_canonical/canonical_dev_tuning.csv
        │
        ▼
[Canonical Metric Recomputation] ──> scripts/compute_evaluation_metrics_corrected.py
        │
        ├── Primary Descriptive Metrics: Paired Agreement (36.20%), Disagreement (63.80%), Flip SUP->CON (48.44%)
        ├── Secondary Proxy Benchmarks: Accuracy, 2-class observed F1, 3-class nominal F1, Coverage, Latency
        ├── Statistical Tests: Exact binomial McNemar (b=4, c=4, p=1.0000 vs No-Check; b=23, c=47, p=0.0056 vs Direct Multi; b=9, c=23, p=0.0201 vs Always-Check)
        ├── Multi-Seed Random Control: 100 seeds matched count (13/163), Mean Acc = 29.24% [26.38%, 31.90%]
        └── Outputs:
             ├── experiments/results_canonical/canonical_benchmark_table.csv
             ├── experiments/results_canonical/canonical_statistical_tests.csv
             ├── experiments/results_canonical/canonical_random_control_100seeds.csv
             └── FINAL_PASS/CANONICAL_VALUES_TABLE.csv
        │
        ▼
[Figure Generation] ──> scripts/generate_publication_figures.py
        └── figures/ (Fig 1: Arch, Fig 2: Pareto, Fig 3: Risk Dist, Fig 4: Confusion Matrices, Fig 5: Overlap, Fig 6: Disagreement)
```

---

## 2. Step-by-Step Data Transformations and File Traceability

### Stage 1: Raw Data Acquisition and Preprocessing
- **Source Artifact:** X-Fact multilingual fact verification dataset (`hi` partition).
- **Processing Script:** `scripts/acquire_and_process_data.py`.
- **Validation Rule:** Strips non-standard formatting, standardizes JSONL keys (`claim_id`, `claim`, `evidence`, `label`).
- **Splits Generated:**
  - `data/splits/hindi_dev.jsonl`: 103 items (MD5: audited in `input_manifest.csv`).
  - `data/splits/hindi_test.jsonl`: 163 items (MD5: audited in `input_manifest.csv`).
- **Integrity Assertion:** Zero overlapping claims or evidence snippets across splits verified by `tests/test_data_integrity.py`.

### Stage 2: Machine Translation & Evidence Pairing
- **Translation Script:** `scripts/translate_evidence.py` and integrated into `scripts/run_corrected_experiments.py`.
- **MT Checkpoint:** `Helsinki-NLP/opus-mt-hi-en`.
- **Coupling Rule:** For every example $i$, the original Hindi evidence $E_i^{\text{hi}}$ is translated to $E_i^{\text{en}}$. The exact generated string $E_i^{\text{en}}$ is fed directly to the translated-condition verifier, and the wall-clock translation time $T_i^{\text{MT}}$ is recorded alongside the forward-pass time.

### Stage 3: Verifier Forward Pass
- **Verifier Checkpoint:** `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`.
- **Conditions Evaluated:**
  1. `Translated-Only` (No-Check): Pair $(C_i^{\text{hi}}, E_i^{\text{en}})$ with prompt formatting.
  2. `Original-Only` (Direct Multilingual): Pair $(C_i^{\text{hi}}, E_i^{\text{hi}})$ directly in Hindi.
  3. `Always-Check`: Evaluates both $(C_i^{\text{hi}}, E_i^{\text{en}})$ and $(C_i^{\text{hi}}, E_i^{\text{hi}})$ for every instance.
  4. `Selective-Check` ($\tau^*$): Computes risk score $R(x) = 1.0 - \max_{c} P_{\text{trans}}(c \mid x)$. If $R(x) > \tau^*$, routes to original Hindi verifier.
- **Output Record:** `experiments/results_canonical/canonical_test_predictions.csv` containing:
  - `claim_id`, `split`, `claim_text`, `gold_label`, `evidence_hi`, `evidence_en`
  - `pred_trans`, `prob_trans_sup`, `prob_trans_neu`, `prob_trans_con`, `conf_trans`, `risk_trans`, `latency_trans`
  - `pred_orig`, `prob_orig_sup`, `prob_orig_neu`, `prob_orig_con`, `conf_orig`, `risk_orig`, `latency_orig`
  - `route_selective`, `pred_selective`, `latency_selective`

### Stage 4: Threshold Selection (Development Split Only)
- **Script:** `scripts/run_corrected_experiments.py` (tuning module).
- **Sweep Range:** $\tau \in [0.30, 0.90]$ with step size $0.05$.
- **Metric Swept:** $J(\tau) = \text{MacroF1}_{\text{dev}}(\tau) - 0.20 \cdot \text{Coverage}_{\text{dev}}(\tau)$.
- **Dev Optimal Point:** $\tau^* = 0.650$ (Coverage: 12.62%, Dev Macro-F1: 0.2275, $J = 0.2023$).
- **Dev Baseline Point:** No-Check ($\text{Coverage} = 0.0\%$, Dev Macro-F1: 0.2104, $J = 0.2104$).
- **Frozen Output:** `experiments/results_canonical/canonical_dev_tuning.csv`.

### Stage 5: Evaluation and Statistical Aggregation
- **Script:** `scripts/compute_evaluation_metrics_corrected.py`.
- **Dependencies:** NumPy, SciPy, scikit-learn, pandas.
- **Statistical Tests:**
  - McNemar exact paired test (binomial distribution on discordant pairs $b, c$).
  - Benjamini-Hochberg false discovery rate (FDR) adjustment across multiple pairwise comparisons.
  - Wilson score intervals for binomial proportions.
- **Outputs Produced:**
  - `experiments/results_canonical/canonical_benchmark_table.csv`
  - `experiments/results_canonical/canonical_statistical_tests.csv`
  - `experiments/results_canonical/canonical_random_control_100seeds.csv`
  - `FINAL_PASS/CANONICAL_VALUES_TABLE.csv`

---

## 3. Configuration and Environment Provenance

- **Random Seeds:**
  - Data splitting / sampling: Seed 42
  - Multi-seed random routing control: Seeds 0 to 99 (100 runs)
- **Model Checkpoints:**
  - Hugging Face Model ID: `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`
  - Hugging Face Model ID: `Helsinki-NLP/opus-mt-hi-en`
- **Software Stack:**
  - Python: 3.14.7 (AMD64 Windows / Linux compatible)
  - PyTorch: 2.14.1+cpu
  - Hugging Face Transformers: 5.19.0
  - SciPy: 1.15.1
  - scikit-learn: 1.6.1
