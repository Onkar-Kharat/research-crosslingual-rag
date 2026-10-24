# Clean-Room Reproduction Instructions

**Document Identifier:** `reproducibility/REPRODUCE.md`  
**Package:** `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_V5_FROZEN_EXPLORATORY.zip`  
**Status:** FROZEN & VERIFIED  

---

## 1. System Requirements

- **Operating System:** Windows 10/11, Linux (Ubuntu 20.04+), or macOS
- **Python Version:** Python 3.10 to 3.14 (Verified on Python 3.14.7 AMD64)
- **PyTorch:** 2.1.0+ (CPU execution supported and recommended for exact reproduction)
- **Hugging Face Transformers:** 4.35.0+ (Verified on 5.19.0)
- **Disk Space:** ~5 GB for model caches (MarianMT + mDeBERTa) and virtual environment
- **RAM:** Minimum 8 GB recommended

---

## 2. Step-by-Step Clean-Room Reproduction

### Step 1: Extract Archive
Extract the research archive to a fresh, clean working directory:
```bash
unzip CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_V5_FROZEN_EXPLORATORY.zip -d research_frozen_v5
cd research_frozen_v5
```

### Step 2: Set Up Python Environment
Create and activate an isolated virtual environment:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

Install the pinned dependencies:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Complete Automated Test Suite
Execute the unit and regression test suite to verify data integrity, label mappings, and logic:
```bash
# Windows
.venv\Scripts\python.exe tests/run_all_tests.py

# Linux / macOS
python tests/run_all_tests.py
```
**Expected Output:**
```
Ran 37 tests in ~0.4s
OK
```

### Step 4: Run End-to-End Inference Pipeline
To regenerate all canonical dev and test predictions, tuning tables, benchmark metrics, 100-seed random controls, and statistical tests from scratch:
```bash
# Windows
.venv\Scripts\python.exe scripts/run_corrected_experiments.py

# Linux / macOS
python scripts/run_corrected_experiments.py
```
*Note: This downloads `Helsinki-NLP/opus-mt-hi-en` and `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7` on first run, generates direct translations, evaluates NLI on both languages, and computes paired statistical tests.*

### Step 5: Regenerate Canonical Manifest and Figures
```bash
# Windows
.venv\Scripts\python.exe scripts/generate_publication_figures.py
.venv\Scripts\python.exe scripts/build_canonical_manifest.py

# Linux / macOS
python scripts/generate_publication_figures.py
python scripts/build_canonical_manifest.py
```

---

## 3. Verifying Key Output Metrics

Compare the newly produced metrics in `experiments/results_canonical/canonical_benchmark_table.csv` against the frozen benchmark:
- **No-Check (Translated Only):** Accuracy = 28.22% (46/163), Macro-F1 (3cl) = 0.2012, Macro-F1 (2cl) = 0.3018
- **Direct Multilingual (Original Only):** Accuracy = 42.94% (70/163), Macro-F1 (3cl) = 0.2467, Macro-F1 (2cl) = 0.3700
- **Always-Check (Dual Consensus):** Accuracy = 36.81% (60/163), Macro-F1 (3cl) = 0.2438, Macro-F1 (2cl) = 0.3657
- **Selective-Check ($\tau^*=0.650$):** Accuracy = 28.22% (46/163), Coverage = 8.0% (13/163)
- **Random Control (100 Seeds, Matched Cov 8.0%):** Accuracy Mean = 29.24% [26.38%, 31.90%]
