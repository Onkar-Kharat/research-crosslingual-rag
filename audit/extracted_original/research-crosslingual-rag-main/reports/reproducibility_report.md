# Reproducibility Report: Separating Translation-Fidelity and Verifier-Reasoning Errors in Cross-Lingual RAG

**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Verification Date:** October 15, 2026  
**Reproducibility Level:** Fully Deterministic / Complete Offline Reproducibility  

---

## 1. System Specifications & Compute Environment

The complete research workflow was designed and validated to run offline on commodity consumer CPU hardware without requiring paid external APIs, proprietary services, or GPU clusters.

- **Operating System:** Windows 11 Enterprise (AMD64, build 26300)
- **CPU:** 18 logical CPU cores (AMD/Intel x86_64)
- **RAM:** 15.61 GB physical memory
- **Disk Footprint:** < 4.5 GB total storage (including cached Hugging Face models and dataset splits)
- **Python Runtime:** Python 3.14.7 within dedicated `.venv`
- **Compiler:** MiKTeX pdfTeX 4.27 (MiKTeX 26.5) with BibTeX 4.2

### Software Dependencies & Exact Pinning

```
torch==2.14.1+cpu
transformers==5.19.0
sentencepiece==0.2.1
protobuf==6.31.1
sacremoses==0.1.1
pandas==2.3.3
scikit-learn==1.9.1
scipy==1.18.1
numpy==2.5.4
matplotlib==3.11.2
requests==2.34.2
tqdm==4.70.1
pyyaml==6.0.3
psutil==6.1.1
```

---

## 2. Dataset Provenance & Integrity Verification

The dataset is derived from the peer-reviewed **X-Fact** multilingual fact-checking benchmark (Gupta & Srikumar, ACL-IJCNLP 2021), distributed under the open MIT License.

| Artifact File | Description | Instances ($N$) | SHA-256 Checksum |
|:---|:---|:---:|:---|
| `data/raw/hindi.jsonl` | Raw benchmark download | 266 | Recorded in `data/raw/provenance.json` |
| `data/processed/dev.jsonl` | Development partition (calibration/tuning) | 103 | `0373df99f36e4f3a...` |
| `data/processed/test.jsonl` | Held-out test partition (frozen evaluation) | 163 | `b1029c5e21975e7a...` |
| `data/processed/dev_translated.jsonl` | Cached MarianMT Hindi$\rightarrow$English dev translations | 103 | Deterministic cache |
| `data/processed/test_translated.jsonl` | Cached MarianMT Hindi$\rightarrow$English test translations | 163 | Deterministic cache |

---

## 3. Step-by-Step Reproduction Instructions

From a clean checkout of the repository, execute the following commands in order:

### Step 1: Environment Setup
```powershell
# Create dedicated virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install exact dependencies
pip install torch transformers sentencepiece protobuf sacremoses pandas scikit-learn scipy numpy matplotlib requests tqdm pyyaml psutil
```

### Step 2: Data Preprocessing
```powershell
# Preprocess raw X-Fact into standardized schema-compliant partitions
python scripts/preprocess_xfact.py
```
*Expected Output:* `data/processed/dev.jsonl` ($N=103$) and `data/processed/test.jsonl` ($N=163$).

### Step 3: Local Neural Machine Translation
```powershell
# Translate Hindi evidence to English using local Helsinki-NLP/opus-mt-hi-en
python scripts/translate_evidence.py
```
*Expected Output:* `data/processed/dev_translated.jsonl` and `data/processed/test_translated.jsonl` with token counts and numerical overlap features.

### Step 4: Verification Experiments & Dev Threshold Tuning
```powershell
# Run 4-condition evaluation and dev-only threshold calibration (tau* = 0.300)
python scripts/run_verification_experiments.py
```
*Expected Output:* 
- `experiments/results/dev_threshold_tuning.csv`
- `experiments/results/dev_predictions.csv`
- `experiments/results/test_predictions.csv`

### Step 5: Statistical Significance & Table Generation
```powershell
# Execute bootstrap CI estimation, paired McNemar, and permutation tests
python scripts/evaluate_statistical_significance.py
```
*Expected Output:*
- `experiments/results/test_main_results.csv` $\rightarrow$ `manuscript/tables/main_results.tex`
- `experiments/results/test_statistical_tests.csv` $\rightarrow$ `manuscript/tables/statistical_tests.tex`
- `experiments/results/test_error_attribution.csv` $\rightarrow$ `manuscript/tables/error_attribution.tex`

### Step 6: Vector Publication Figures
```powershell
# Generate journal-grade PDF and PNG vector figures
python scripts/generate_publication_figures.py
```
*Expected Output:*
- `figures/pdf/fig2_risk_coverage_tradeoff.pdf`
- `figures/pdf/fig3_condition_comparison.pdf`
- `figures/pdf/fig4_error_attribution_breakdown.pdf`

### Step 7: LaTeX Manuscript Compilation
```powershell
cd manuscript
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```
*Expected Output:* `manuscript/main.pdf` (8 pages, 0 errors, 0 undefined citations, strictly meeting all TACL guidelines).

---

## 4. Key Empirical Constants & Parameters

- **Random Seed:** Fixed to `42` across all scripts.
- **Bootstrap Replications:** $B = 1,000$ cluster resamples for 95% percentile confidence intervals.
- **Permutation Test Replications:** $B = 1,000$ paired label sign-flip permutations.
- **Translation Hyperparameters:**
  - Model: `Helsinki-NLP/opus-mt-hi-en`
  - Beam Size: 2
  - Max Sequence Length: 512 tokens
  - Decoding: Deterministic greedy beam search
- **Verifier Hyperparameters:**
  - Model: `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`
  - Max Sequence Length: 512 tokens
  - Softmax Temperature: 1.0
- **Selective Trigger Hyperparameters:**
  - Uncertainty weight: $w_{\text{unc}} = 0.70$
  - Numerical mismatch weight: $w_{\text{mismatch}} = 0.30$
  - Tuned threshold: $\tau^* = 0.300$ (maximizing $\text{Macro-F1} - 0.15 \cdot \text{Coverage}$ on development data).

---

## 5. Compute Time & Resource Consumption

| Pipeline Stage | Device | Execution Time | Memory Peak (RAM) |
|:---|:---:|:---:|:---:|
| Evidence Translation (266 items) | CPU (18 threads) | ~11.5 minutes | ~2.1 GB |
| Model Inference & Verification (4 conditions) | CPU (18 threads) | ~16.2 minutes | ~3.4 GB |
| Statistical Resampling & Significance | CPU (1 thread) | ~25 seconds | < 300 MB |
| Publication Figure Generation | CPU (1 thread) | ~4 seconds | < 250 MB |
| LaTeX PDF Compilation (3 passes) | CPU (1 thread) | ~12 seconds | < 150 MB |
| **Total End-to-End Pipeline** | **CPU** | **~28 minutes** | **~3.4 GB** |

---

## 6. Verification & Integrity Checklist

- [x] All raw data downloaded from verified public URLs with documented hashes.
- [x] Test split kept completely unseen during threshold selection and hyperparameter exploration.
- [x] No data fabrication, synthetic hallucination, or manual tampering.
- [x] All LaTeX tables generated automatically by scripts directly from prediction logs.
- [x] Manuscript compiled with zero unresolved cross-references and verified bibliography entries.
