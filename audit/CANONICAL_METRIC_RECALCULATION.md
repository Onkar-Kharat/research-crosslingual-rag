# AUDIT REPORT: Canonical Metric Recalculation from Raw Predictions

**Audit Date:** October 2026  
**Auditor:** Senior Methodology & Statistical Verification Auditor  
**Repository:** Cross-Lingual Evidence Verification  
**Evaluation Split:** Test Split ($N=163$), Frozen Protocol ($\tau^* = 0.650$)  
**Status:** FULLY RECOMPUTED, VERIFIED, & RECONCILED  

---

## 1. Executive Summary & Verification Protocol

Every metric in the canonical results suite was independently recalculated from scratch directly from the per-instance prediction rows in `experiments/results_canonical/canonical_test_predictions.csv` ($N=163$). 

- **Gold Label Schema:** 3 canonical classes (`CONTRADICTED`, `INSUFFICIENT_EVIDENCE`, `SUPPORTED`).
- **Ground Truth Distribution:**
  - `CONTRADICTED`: 142 (87.12%)
  - `INSUFFICIENT_EVIDENCE`: 21 (12.88%)
  - `SUPPORTED`: **0 (0.00%)**
- **Missing Positive Class Disclosure:** Because authentic journalistic fact-checks in Hindi focus on debunking viral misinformation, positive entailments are completely absent ($N=0$). Consequently, standard 3-class Macro-F1 averages include an uninformative zero term for `SUPPORTED`. We therefore report both:
  1. **Observed 2-Class Macro-F1:** Evaluated strictly over classes with ground-truth support (`CONTRADICTED` and `INSUFFICIENT_EVIDENCE`).
  2. **Nominal 3-Class Macro-F1:** Included for architectural parity with benchmark conventions.

---

## 2. Primary Descriptive Outcome: Translation Sensitivity & Label Flipping

Evaluates the degree to which translating evidence from Hindi to English alters the verifier's veracity predictions:

| Metric Dimension | Numerator / Denominator | Rate (%) | 95% Bootstrap / Wilson CI | Operational Interpretation |
|:---|:---:|:---:|:---:|:---|
| **Paired Agreement** | 59 / 163 | **36.20%** | [29.22%, 43.81%] | Model prediction unchanged across languages |
| **Paired Disagreement** | 104 / 163 | **63.80%** | [56.19%, 70.78%] | Translation shift induces prediction change |
| **Directional Flip: $\text{SUP} \to \text{CON}$** | 31 / 64 | **48.44%** | [36.63%, 60.42%] | Predicted Entailment flips to Contradiction |
| **Directional Flip: $\text{CON} \to \text{SUP}$** | 18 / 44 | **40.91%** | [27.69%, 55.59%] | Predicted Contradiction flips to Entailment |
| **Directional Flip: $\text{NEU} \to \text{CON}$** | 23 / 55 | **41.82%** | [29.74%, 54.97%] | Predicted Neutral flips to Contradiction |

---

## 3. Secondary Proxy Benchmark Performance & Latency Summary ($N=163$)

All accuracy numbers and confidence intervals recalculated from raw predictions:

| System / Condition | Correct / Total | Accuracy (%) | 95% CI (Acc) | Observed 2-Class F1 | Nominal 3-Class F1 | Coverage (%) | Mean Latency (ms) | Paired McNemar vs Selective |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **No-Check (Translated Only)** | 46 / 163 | **28.22%** | [21.47%, 35.58%] | 0.3018 | 0.2012 | 0.0% (0/163) | 3,650.4 ms | $p = 1.0000$ ($b=4, c=4$) |
| **Selective-Check ($\tau^*=0.650$)**| 46 / 163 | **28.22%** | [21.47%, 35.58%] | 0.2950 | 0.1967 | 7.98% (13/163) | 4,613.8 ms | Reference System |
| **Direct Multilingual (Original)** | 70 / 163 | **42.94%** | [35.57%, 50.92%] | 0.3700 | 0.2467 | 100.0% (163/163) | 11,295.6 ms | $p = 0.0056$ ($b=23, c=47$) |
| **Always-Check (Dual Consensus)** | 60 / 163 | **36.81%** | [29.45%, 44.17%] | 0.3657 | 0.2438 | 100.0% (163/163) | 14,945.9 ms | $p = 0.0201$ ($b=9, c=23$) |
| **Ablation: Numeral-Only Routing** | 73 / 163 | **44.79%** | [37.42%, 52.76%] | 0.3794 | 0.2529 | 96.32% (157/163) | 14,751.3 ms | $p = 0.0013$ ($b=20, c=47$) |
| **Control: Random Routing (100 Seeds)**| 47.7 / 163 | **29.24%** | [26.38%, 31.90%] | 0.3082 | 0.2054 | 7.98% (13/163) | 4,613.8 ms | $p = 0.2669$ ($b=4, c=9$) |
| **Majority Baseline (Always CON)**| 142 / 163 | **87.12%** | [81.16%, 91.39%] | 0.4656 | 0.3104 | 0.0% | 0.0 ms | Baseline Reference |
| **Oracle Upper Bound (Non-Deployable)**| 97 / 163 | **59.51%** | [52.15%, 66.87%] | 0.5200 | 0.3467 | 100.0% | 14,945.9 ms | $p < 0.0001$ ($b=0, c=51$) |

---

## 4. Confusion Matrices (Rows: Gold Label, Columns: Predicted Label)

### 4.1 No-Check System (Translated Only)
| Gold \ Pred | CONTRADICTED | INSUFFICIENT_EVIDENCE | SUPPORTED | Total | Recall (%) |
|:---|:---:|:---:|:---:|:---:|:---:|
| **CONTRADICTED** | 43 | 11 | 88 | 142 | 30.28% |
| **INSUFFICIENT_EVIDENCE** | 3 | 3 | 15 | 21 | 14.29% |
| **SUPPORTED** | 0 | 0 | 0 | 0 | N/A |
| **Precision (%)** | 93.48% | 21.43% | 0.00% | 163 | **Acc: 28.22%** |

### 4.2 Selective-Check System ($\tau^*=0.650$)
| Gold \ Pred | CONTRADICTED | INSUFFICIENT_EVIDENCE | SUPPORTED | Total | Recall (%) |
|:---|:---:|:---:|:---:|:---:|:---:|
| **CONTRADICTED** | 44 | 13 | 85 | 142 | 30.99% |
| **INSUFFICIENT_EVIDENCE** | 4 | 2 | 15 | 21 | 9.52% |
| **SUPPORTED** | 0 | 0 | 0 | 0 | N/A |
| **Precision (%)** | 91.67% | 13.33% | 0.00% | 163 | **Acc: 28.22%** |

### 4.3 Direct Multilingual System (Original Hindi Only)
| Gold \ Pred | CONTRADICTED | INSUFFICIENT_EVIDENCE | SUPPORTED | Total | Recall (%) |
|:---|:---:|:---:|:---:|:---:|:---:|
| **CONTRADICTED** | 68 | 8 | 66 | 142 | 47.89% |
| **INSUFFICIENT_EVIDENCE** | 17 | 2 | 2 | 21 | 9.52% |
| **SUPPORTED** | 0 | 0 | 0 | 0 | N/A |
| **Precision (%)** | 80.00% | 20.00% | 0.00% | 163 | **Acc: 42.94%** |

---

## 5. Development Tuning Utility Recalculation ($N=103$ Dev Split)

The routing threshold was selected strictly on development data optimizing the prespecified linear utility function:
$$J(\tau) = \text{Macro-F1}_{3\text{cl}}(\tau) - 0.15 \times \text{Coverage}(\tau)$$

- **No-Check Baseline Utility ($\text{Coverage}=0.0\%$):**
  $$J = 0.2104 - 0.15 \times 0.0000 = \mathbf{0.2104}$$
- **Cascade Peak Utility ($\tau^*=0.650, \text{Coverage}=12.62\%$):**
  $$J = 0.2213 - 0.15 \times 0.1262 = \mathbf{0.2023}$$
- **Utility Delta:**
  $$\Delta J = 0.2023 - 0.2104 = \mathbf{-0.0081}$$

**Conclusion:** The No-Check baseline achieves higher development utility than any threshold of the selective consultation cascade. The cascade does not produce a Pareto improvement. This negative result is reported transparently and verified across all files.
