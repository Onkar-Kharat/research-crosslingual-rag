# Environment and Runtime Specifications

## 1. Host System Environment
- **Operating System:** Microsoft Windows 11 Pro / Enterprise (AMD64)
- **CPU Architecture:** x86_64 / AMD64, multi-core workstation
- **GPU Acceleration:** None (All inference pipelines and tokenization run on CPU)
- **Memory:** Minimum 16 GB RAM recommended for local model loading

## 2. Python Runtime & Core Dependencies
- **Python Version:** 3.14.7 (64-bit)
- **Virtual Environment:** Python venv located in `.venv/`
- **Core Packages:**
  - `torch`: CPU build
  - `transformers`: Sequence classification and sequence-to-sequence translation
  - `scipy`: Statistical tests (exact binomial, chi-square)
  - `scikit-learn`: Classification metrics (Accuracy, Macro-F1, Confusion Matrices)
  - `pandas`: Data manipulation and tabular results storage
  - `numpy`: Numerical processing and random number generation (`np.random.default_rng`)

## 3. Determinism and Seeding Policy
- **Primary Random Seed:** `42`
- **Permutation Tests:** $B=5,000$ paired permutations initialized with `seed=42`
- **Bootstrap Confidence Intervals:** $B=2,000$ resamples initialized with `seed=42`
- **Multi-Seed Random Control:** Deterministically looped across seeds $s \in \{0, \dots, 99\}$
- **Machine Translation Decoding:** Greedy / beam size 2 deterministic generation with temperature 0.0

## 4. Execution Guidance
To activate the virtual environment and verify runtime parity:
```powershell
.\.venv\Scripts\Activate.ps1
python tests/run_all_tests.py
```
Expected output: 47 tests passed in $< 1.0\text{s}$.
