# Artifact and Data Provenance

---

## 1. Upstream Data Sources

### Primary Benchmark: X-Fact
- **Publication:** *X-FACT: A New Benchmark Dataset for Multilingual Fact Checking* (Gupta & Srikumar, ACL-IJCNLP 2021)
- **Repository:** `https://github.com/utahnlp/x-fact`
- **License:** MIT License (archived locally in `data/raw/LICENSE_xfact.txt`)
- **Language Extracted:** Hindi (`hi`)
- **Raw Files & Checksums (SHA-256):**
  - `data/raw/dev.all.tsv`: `faed99c2ee9e7ea505a1bae88c06bd2c686804b5e1e786551e589b5f89df8199`
  - `data/raw/test.all.tsv`: `b126a4f7e16ec72f554a79e1fffaef8d71ba03ec9e07072ff7484a502cf37cbb`

---

## 2. Upstream Model Weights

### Machine Translation Model
- **Identifier:** `Helsinki-NLP/opus-mt-hi-en` (Tiedemann & Thottingal, 2020)
- **Framework:** MarianMT via HuggingFace Transformers
- **Parameters:** ~74 Million
- **Decoding Configuration:** Deterministic greedy/beam search (beam size = 2, max length = 512)

### Multilingual NLI Verifier Model
- **Identifier:** `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7` (Laurer et al., 2022)
- **Base Architecture:** mDeBERTa-v3-base (He et al., 2021)
- **Parameters:** ~278 Million
- **Fine-Tuning:** Multilingual NLI (MNLI + XNLI across 100 languages)
- **Input Representation:** Premise-Hypothesis pairs structured as `[CLS] Evidence [SEP] Claim [SEP]`

---

## 3. Canonical Output Provenance

All canonical experimental results are archived deterministically in `experiments/results_canonical/`:
- `canonical_test_predictions.csv`: 163 rows, containing raw text, generated translations, token counts, model probabilities, and individual system predictions.
- `canonical_dev_predictions.csv`: 103 rows, containing development split predictions and risk score distributions.
- `canonical_benchmark_table.csv`: Authoritative benchmark performance across all conditions and baselines.
- `canonical_dev_tuning.csv`: Complete grid search evaluation across candidate thresholds $\tau \in [0.10, 0.65]$.
- `canonical_statistical_tests.csv`: Paired McNemar tests, binomial exact calculations, permutation tests, and FDR-corrected $p$-values.
- `canonical_random_control_100seeds.csv`: 100-seed simulation evaluation of the matched-coverage random baseline.
- `test_metrics.json`: Hierarchical JSON serialization of all canonical sensitivity metrics.
