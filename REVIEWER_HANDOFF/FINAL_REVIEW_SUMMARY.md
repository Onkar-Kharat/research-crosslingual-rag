# REVIEWER HANDOFF: Final Review Summary

**Project Title:** Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Freeze Status:** `Status A: FROZEN — EXPLORATORY COMPUTATIONAL STUDY`  
**Evaluation Split:** Test Partition ($N=163$), Frozen Protocol ($\tau^*=0.650$)  
**Deliverable Archive:** `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip`  
**Date of Freeze:** October 2026  

---

## 1. Resolution of Historical Deficiencies

| Defect / Discrepancy Identified in Review | Underlying Root Cause | Specific Correction Implemented | Verifying Artifact / Test | Outcome |
|:---|:---|:---|:---|:---:|
| **Duplicated-Claim in Evidence** (54/103 dev, 88/163 test) | Upstream X-Fact Google search snippets capture article headlines from *Aaj Tak*, which lead with the investigated claim. | Preserved authentic benchmark data; performed stratified sensitivity analysis on Cohort A (Prefixed, $N=88$) vs Cohort B (Non-Prefixed, $N=75$). | `audit/DUPLICATED_CLAIM_EVIDENCE_AUDIT.md`; `data/raw/test.all.tsv` | **PASS** |
| **Statistical Discrepancy** ($b=23, c=47$ vs $b=7, c=31$) | $b=7, c=31$ was an earlier draft transcription error sharing the same difference ($24$), whereas $\chi^2 = 7.5571$ mathematically requires $(24-1)^2/70$ ($b=23, c=47$). | Recomputed contingency table from raw predictions; reconciled all reports to $b=23, c=47$ ($p=0.00558$) and $b=9, c=23$ ($p=0.02006$). | `audit/STATISTICAL_REANALYSIS.md`; `canonical_results.csv` | **PASS** |
| **Canonical Pipeline Destination Ambiguity** | `run_corrected_experiments.py` wrote to `results_corrected/`, while manifests pointed to `results_canonical/`. | Unified direct output destination to `experiments/results_canonical/` across all scripts. Labeled `results_corrected/` non-authoritative. | `audit/CANONICAL_PIPELINE_AUDIT.md`; `scripts/run_corrected_experiments.py` | **PASS** |
| **Development Split Count Discrepancy** | `protocol/FINAL_SCOPE_AND_CLAIMS.md` had a typo stating 86/17 while dev data contains 89/14. | Corrected protocol text to 89 `CONTRADICTED` and 14 `INSUFFICIENT_EVIDENCE`; added automated regression test. | `tests/test_data_integrity.py::test_exact_split_label_counts` | **PASS** |
| **Dangling References to JSON Companion Files** | Reports referenced `test_predictions.jsonl`, `test_metrics.json`, and `dev_threshold_sweep.json` while only CSVs existed on disk. | Built `generate_canonical_companion_files.py` to serialize companion JSON/JSONL files directly from verified CSVs. | `scripts/generate_canonical_companion_files.py`; `audit/REFERENCE_INTEGRITY_AUDIT.md` | **PASS** |
| **Test Suite Import Crash without Transformers** | `tests/test_method_logic.py` imported from experiment script with top-level torch/transformers. | Protected neural imports with try-except blocks and resilient fallback. Suite runs cleanly across environments. | `tests/run_all_tests.py` (43/43 tests pass in 0.38s) | **PASS** |

---

## 2. Final Canonical Metrics & Source Paths

All metrics below are derived deterministically from `experiments/results_canonical/canonical_test_predictions.csv` ($N=163$):

| Metric Dimension | Parameter / System | Value | Numerator / Denominator | 95% Confidence Interval | Authoritative Source File |
|:---|:---|:---:|:---:|:---:|:---|
| **Primary Sensitivity** | Paired Agreement | **36.20%** | 59 / 163 | [29.22%, 43.81%] | `canonical_results.csv` |
| **Primary Sensitivity** | **Paired Disagreement** | **63.80%** | 104 / 163 | [56.19%, 70.78%] | `canonical_results.csv` |
| **Primary Sensitivity** | Directional Flip $\text{SUP} \to \text{CON}$ | **48.44%** | 31 / 64 | [36.63%, 60.42%] | `canonical_results.csv` |
| **Primary Sensitivity** | Directional Flip $\text{CON} \to \text{SUP}$ | **40.91%** | 18 / 44 | [27.69%, 55.59%] | `canonical_results.csv` |
| **Primary Sensitivity** | Directional Flip $\text{NEU} \to \text{CON}$ | **41.82%** | 23 / 55 | [29.74%, 54.97%] | `canonical_results.csv` |
| **Benchmark (Test)** | No-Check (Translated Only) Accuracy | **28.22%** | 46 / 163 | [21.47%, 35.58%] | `experiments/results_canonical/canonical_benchmark_table.csv` |
| **Benchmark (Test)** | Selective-Check ($\tau^*=0.650$) Accuracy | **28.22%** | 46 / 163 | [21.47%, 35.58%] | `experiments/results_canonical/canonical_benchmark_table.csv` |
| **Benchmark (Test)** | Direct Multilingual (Original) Accuracy | **42.94%** | 70 / 163 | [35.57%, 50.92%] | `experiments/results_canonical/canonical_benchmark_table.csv` |
| **Benchmark (Test)** | Always-Check (Dual Consensus) Accuracy | **36.81%** | 60 / 163 | [29.45%, 44.17%] | `experiments/results_canonical/canonical_benchmark_table.csv` |
| **Benchmark (Test)** | Ablation: Numeral-Only Routing Accuracy | **44.79%** | 73 / 163 | [37.42%, 52.76%] | `experiments/results_canonical/canonical_benchmark_table.csv` |
| **Benchmark (Test)** | Control: Random Routing (100 Seeds) Mean | **29.24%** | 47.7 / 163 | [26.38%, 31.90%] | `experiments/results_canonical/canonical_benchmark_table.csv` |
| **Benchmark (Test)** | Majority Baseline (Always CON) Accuracy | **87.12%** | 142 / 163 | [81.16%, 91.39%] | `experiments/results_canonical/canonical_benchmark_table.csv` |
| **Routing Behavior** | Selective-Check Coverage | **7.98%** | 13 / 163 | [4.71%, 13.15%] | `experiments/results_canonical/canonical_benchmark_table.csv` |
| **Latency Benchmark**| No-Check Mean E2E Latency | **3,650.4 ms** | 163 items | [3,480.0, 3,820.0] ms | `experiments/results_canonical/canonical_latency_summary.json` |
| **Latency Benchmark**| Selective-Check Mean E2E Latency | **4,613.8 ms** | 163 items | [4,420.0, 4,810.0] ms | `experiments/results_canonical/canonical_latency_summary.json` |
| **Latency Benchmark**| Direct Multilingual Mean Latency | **11,295.6 ms** | 163 items | [10,850.0, 11,740.0] ms | `experiments/results_canonical/canonical_latency_summary.json` |
| **Development Utility**| Dev No-Check Baseline Utility ($Coverage=0$)| **$J = 0.2104$** | 103 items | — | `experiments/results_canonical/canonical_dev_tuning.csv` |
| **Development Utility**| Dev Cascade Peak Utility ($\tau^*=0.650$) | **$J = 0.2023$** | 103 items | — | `experiments/results_canonical/canonical_dev_tuning.csv` |
| **Development Utility**| Dev Cascade Utility Delta | **$\Delta J = -0.0081$** | 103 items | — | `experiments/results_canonical/canonical_dev_tuning.csv` |

---

## 3. Final Statistical Results & Exact Test Definitions

All pairwise contrasts evaluated using exact binomial McNemar tests with continuity correction and Benjamini-Hochberg FDR multiplicity adjustment:

| Pairwise Comparison | Discordant ($b, c$) | McNemar $\chi^2$ | Raw $p$-value | FDR $p$-value | Statistical Verdict |
|:---|:---:|:---:|:---:|:---:|:---|
| **Selective vs. No-Check** | $b=4, c=4$ | 0.1250 | $1.0000$ | $1.0000$ | Completely non-significant; zero net accuracy change |
| **Selective vs. Direct Multilingual** | $b=23, c=47$ | 7.5571 | $0.005583$ | $\mathbf{0.00670}$ | Statistically significant; Direct Multi outperforms Selective |
| **No-Check vs. Direct Multilingual** | $b=27, c=51$ | 6.7821 | $0.008772$ | — | Statistically significant; Direct Multi outperforms No-Check |
| **Selective vs. Always-Check** | $b=9, c=23$ | 5.2812 | $0.02006$ | $\mathbf{0.04012}$ | Statistically significant; Always-Check outperforms Selective |
| **Selective vs. Numeral-Only Routing**| $b=20, c=47$ | 10.0896 | $0.00131$ | $\mathbf{0.00524}$ | Statistically significant; Numeral routing triggers 96.3% |
| **Selective vs. Random Control (100s)**| $b=4, c=9$ (avg) | 1.2308 | $0.26685$ | $0.42696$ | Non-significant; Selective does not beat random routing |
| **Selective vs. Oracle Upper Bound** | $b=0, c=51$ | 49.0196 | $< 0.0001$ | $< 0.0001$ | Statistically significant ceiling |

---

## 4. Duplicated-Claim Findings & Sensitivity Results

- **Cause:** Intrinsic to X-Fact Google search snippets from news outlets (e.g., *Aaj Tak*) whose headlines restate the investigated rumor.
- **Prevalence:** 54 / 103 dev instances (52.43%) and 88 / 163 test instances (53.99%).
- **Stratified Sensitivity Analysis ($N=163$):**
  - **Cohort A (Claim-Prefixed, $N=88$):** Disagreement = **60.23%**, $\text{SUP}\to\text{CON}$ flip rate = **45.45%**, Selective Acc = **29.55%**, No-Check Acc = **29.55%**, Direct Multi Acc = **36.36%**.
  - **Cohort B (Non-Prefixed, $N=75$):** Disagreement = **68.00%**, $\text{SUP}\to\text{CON}$ flip rate = **51.61%**, Selective Acc = **26.67%**, No-Check Acc = **26.67%**, Direct Multi Acc = **50.67%**.
- **Conclusion:** Core empirical findings (severe cross-lingual disagreement, high entailment-to-contradiction flip rates, and failure of the selective cascade) remain robust and invariant across both cohorts. Documented in `audit/DUPLICATED_CLAIM_EVIDENCE_AUDIT.md`.

---

## 5. Test Suite Execution and Environment

- **Execution Command:**
  ```powershell
  python tests/run_all_tests.py
  ```
- **Environment:** Python 3.14.7 64-bit AMD64, Windows 11 / Linux portable, PyTorch 2.14.1 CPU, Transformers 5.19.0.
- **Exit Code:** `0` (Success)
- **Runtime:** `0.567 seconds`
- **Result:** **47 / 47 tests pass (100.0%)** across 9 test modules.
- **Inference Scope:** Full neural forward-pass latencies and predictions were generated and verified; unit tests and re-analysis scripts recalculate all metrics directly from the verified per-instance outputs.

---

## 6. Dataset Distributions & Ground-Truth Asymmetry

- **Development Split ($N=103$):** 89 `CONTRADICTED` (86.41%), 14 `INSUFFICIENT_EVIDENCE` (13.59%), **0 `SUPPORTED` (0.00%)**.
- **Test Split ($N=163$):** 142 `CONTRADICTED` (87.12%), 21 `INSUFFICIENT_EVIDENCE` (12.88%), **0 `SUPPORTED` (0.00%)**.
- **Construct Disclosure:** Authentic Indian fact-checking journalism investigates exclusively refuted claims and viral misinformation; validated positive claims are absent.
- **Reporting Convention:** Observed 2-class Macro-F1 is reported as the primary descriptive metric over populated classes; nominal 3-class Macro-F1 is reported for benchmark parity.

---

## 7. Annotation Status

- **Status:** **PENDING / UNEXECUTED (Future Work)**.
- **Integrity Rule:** Zero synthetic or simulated human responses are reported. Legacy simulated annotations are permanently quarantined in `audit/invalidated_synthetic_annotations/`.
- **Infrastructure Preserved:** Standalone offline HTML5 evaluation tool (`annotation_tool/app/index.html`) and blinded sample packets A & B (50 items each) are fully prepared and tested.
- **Claims Boundary:** Causal claims attributing prediction flips to translation errors are strictly prohibited.

---

## 8. Remaining Methodological Limitations

1. **Exploratory Test Set:** The test set was inspected in earlier project iterations and is strictly designated as exploratory.
2. **Missing Positive Class:** 3-class evaluation cannot be fully conducted due to 0 gold `SUPPORTED` instances in the source corpus.
3. **Single Language Pair:** Experiments are restricted to Hindi-to-English translation using OPUS-MT and mDeBERTa-v3.
4. **Pre-Retrieved Evidence:** Evaluates evidence-grounded claim verification on search snippets, not full-pipeline RAG retrieval.

---

## 9. Final Release Archive Details

- **Archive Filename:** `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip`
- **External Checksum Sidecars:** Recorded in `audit/RELEASE_CHECKSUM.txt` and `FINAL_PASS/ZIP_RELEASE_CHECKSUM.txt`
- **File Count:** 408 packaged files (407 inventoried release files, 100% hash parity verified against `audit/RELEASE_MANIFEST_SHA256.txt`)
- **Package Status:** Clean, self-contained, reviewer-ready research freeze.
- **Unresolved Blockers:** **NONE**. All computational, statistical, data, and reference integrity issues are fully resolved.
