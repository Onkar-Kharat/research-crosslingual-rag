# REVIEWER REPRODUCTION COMMANDS: Step-by-Step Execution Guide

**Project:** Cross-Lingual Evidence Verification  
**Evaluation Target:** Test Set ($N=163$), Frozen Parameters ($\tau^*=0.650$)  
**Supported Environments:** Windows PowerShell / CMD, Linux / macOS bash  
**Python Version:** Python 3.10+ (Tested on Python 3.14.7 AMD64)  

---

## 1. Environment Setup

### Option A: Standard Virtual Environment (Recommended)
```bash
# 1. Create a clean virtual environment
python -m venv .venv

# 2. Activate environment
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On Linux/macOS bash:
source .venv/bin/activate

# 3. Install core dependencies
pip install --upgrade pip
pip install -r requirements.txt
```
- **Requirements File:** `requirements.txt` includes `numpy`, `pandas`, `scipy`, `scikit-learn`, `matplotlib`, `requests`, `torch>=2.1`, `transformers>=4.40`.
- **Expected Exit Code:** `0`

---

## 2. Reproduction Steps in Execution Order

### Step 1: Run Automated Regression Test Suite (Fast Verification)
Verifies data integrity, split isolation, missing positive class, numerical normalization, McNemar test symmetry, and schema validation:
```bash
python tests/run_all_tests.py
```
- **Expected Exit Code:** `0`
- **Expected Runtime:** `~0.4 seconds`
- **Expected Output:**
  ```
  Ran 43 tests in 0.375s
  OK
  Wrote test reports to tests/TEST_REPORT.md
  ```

---

### Step 2: Metric Recalculation from Raw Test Predictions
Recalculates all primary sensitivity metrics (agreement, disagreement, flip rates) and secondary proxy benchmark metrics (accuracy, CIs) directly from per-instance model predictions:
```bash
python -c "
import pandas as pd
df = pd.read_csv('experiments/results_canonical/canonical_test_predictions.csv')
total = len(df)
agreed = (df['pred_translated'] == df['pred_original']).sum()
disagreed = (df['pred_translated'] != df['pred_original']).sum()
print(f'Test Items: {total}')
print(f'Paired Agreement:    {agreed}/{total} ({agreed/total*100:.2f}%)')
print(f'Paired Disagreement: {disagreed}/{total} ({disagreed/total*100:.2f}%)')
print(f'No-Check Accuracy:   {(df[\"pred_translated\"] == df[\"gold_label\"]).sum()}/{total} ({(df[\"pred_translated\"] == df[\"gold_label\"]).mean()*100:.2f}%)')
print(f'Selective Accuracy:  {(df[\"pred_selective\"] == df[\"gold_label\"]).sum()}/{total} ({(df[\"pred_selective\"] == df[\"gold_label\"]).mean()*100:.2f}%)')
print(f'Direct Multi Acc:    {(df[\"pred_original\"] == df[\"gold_label\"]).sum()}/{total} ({(df[\"pred_original\"] == df[\"gold_label\"]).mean()*100:.2f}%)')
"
```
- **Expected Exit Code:** `0`
- **Expected Runtime:** `~1.0 second`

---

### Step 3: Run Duplicated-Claim Stratified Sensitivity Analysis
Inspects the claim repetition in raw evidence and computes metrics separately for Claim-Prefixed ($N=88$) vs Non-Prefixed ($N=75$) cohorts:
```bash
python -c "
import pandas as pd
from sklearn.metrics import accuracy_score
df = pd.read_csv('experiments/results_canonical/canonical_test_predictions.csv')
pref = df.apply(lambda r: r['original_evidence'].strip().startswith(r['claim'].strip()), axis=1)
for mask, name in [(pref, 'Cohort A: Claim-Prefixed (N=88)'), (~pref, 'Cohort B: Non-Prefixed (N=75)')]:
    sub = df[mask]
    dis = (sub['pred_translated'] != sub['pred_original']).mean()
    acc_no = accuracy_score(sub['gold_label'], sub['pred_translated'])
    acc_sel = accuracy_score(sub['gold_label'], sub['pred_selective'])
    acc_dir = accuracy_score(sub['gold_label'], sub['pred_original'])
    print(f'=== {name} ===')
    print(f'Disagreement Rate: {dis*100:.2f}% | No-Check: {acc_no*100:.2f}% | Selective: {acc_sel*100:.2f}% | DirectMulti: {acc_dir*100:.2f}%')
"
```
- **Expected Exit Code:** `0`
- **Expected Runtime:** `~1.0 second`

---

### Step 4: Recompute Paired Statistical Tests & Contingency Tables
Recomputes exact McNemar tests ($b=23, c=47$ for Selective vs Direct Multilingual, and $b=9, c=23$ for Selective vs Always-Check):
```bash
python -c "
import pandas as pd, numpy as np, scipy.stats as stats
df = pd.read_csv('experiments/results_canonical/canonical_test_predictions.csv')
yt = df['gold_label'].values
yp_sel = df['pred_selective'].values
yp_dir = df['pred_original'].values
corr_sel = (yp_sel == yt)
corr_dir = (yp_dir == yt)
b = int(np.sum(corr_sel & ~corr_dir))
c = int(np.sum(~corr_sel & corr_dir))
stat = float((abs(b - c) - 1.0)**2 / (b + c))
p_val = float(min(1.0, 2.0 * stats.binom.cdf(min(b, c), b + c, 0.5)))
print(f'Selective vs Direct Multi: b={b}, c={c}, Chi2={stat:.4f}, Exact p={p_val:.5f}')
assert b == 23 and c == 47, 'Counts mismatch!'
"
```
- **Expected Exit Code:** `0`
- **Expected Runtime:** `~0.5 seconds`

---

### Step 5: Regenerate Canonical Companion Files & Build Cryptographic Manifest
Validates and regenerates JSON and JSONL companion formats (`test_predictions.jsonl`, `test_metrics.json`, `dev_threshold_sweep.json`) and calculates SHA-256 hashes:
```bash
python scripts/generate_canonical_companion_files.py
python scripts/build_canonical_manifest.py
```
- **Expected Exit Code:** `0`
- **Expected Runtime:** `~2.5 seconds`

---

### Step 6: Regenerate Publication Figures
Regenerates vector PDF and high-resolution PNG figures from canonical results into `figures/`:
```bash
python scripts/generate_publication_figures.py
```
- **Expected Exit Code:** `0`
- **Expected Runtime:** `~2.0 seconds`
- **Generated Figures:**
  - `figures/pdf/fig2_risk_coverage_tradeoff.pdf`
  - `figures/pdf/fig3_condition_comparison.pdf`
  - `figures/pdf/fig4_error_attribution_breakdown.pdf`

---

### Step 7: Full Neural Inference Rerun (Optional)
Executes MarianMT translation (`Helsinki-NLP/opus-mt-hi-en`) and mDeBERTa-v3 verification (`MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`) on CPU hardware:
```bash
python scripts/run_corrected_experiments.py
```
- **Required Hardware/Time:** Single-thread or multi-thread CPU takes ~12-18 minutes; GPU takes ~1.5 minutes.
- **External Resources:** HuggingFace model weights downloaded on first run (cached in `~/.cache/huggingface/`).
- **Expected Exit Code:** `0`
