# FINAL SCOPE AND SCIENTIFIC CLAIMS SPECIFICATION

**Document Identifier:** `protocol/FINAL_SCOPE_AND_CLAIMS.md`  
**Status:** CANONICAL & FROZEN  
**Study Formulation:** Option C (Observational Translation Shift and Verifier Sensitivity)  
**Governance Standard:** Antigravity Master Research Protocol (V6)  

---

## 1. Fixed Research Scope and Boundaries

### Formal Study Scope:
> **"An observational study of model prediction sensitivity and routing behavior when claim evidence is represented in original Hindi versus machine-translated English."**

### Explicit System Boundaries:
- **What is evaluated:** A multilingual Natural Language Inference (NLI) verifier (`MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`) evaluating paired claim and evidence snippets under two representation conditions:
  1. *Translated-English Condition:* Hindi evidence translated to English using `Helsinki-NLP/opus-mt-hi-en` (MarianMT).
  2. *Original-Hindi Condition:* Hindi evidence verified directly in Hindi by mDeBERTa.
  3. *Selective Cascade Condition:* Hard routing back to original Hindi evidence when a risk heuristic (predictive entropy and Devanagari/Arabic numeral Jaccard mismatch) exceeds threshold $\tau^* = 0.650$.
- **What is NOT evaluated:**
  1. *No End-to-End RAG:* The evaluated system consumes pre-retrieved evidence snippets from the X-Fact benchmark. It does **not** implement end-to-end information retrieval (dense/sparse retriever), query reformulation, or generative language model answer synthesis. It is **not** an end-to-end RAG system.
  2. *No Broad Multilingual Generalization:* The empirical evaluation is strictly confined to the Hindi $\rightarrow$ English language pair.
  3. *No Causal Translation Attribution:* Without authentic bilingual human annotation, the computational study does **not** claim that translation errors caused particular verifier failures, nor does it claim verified translation error percentages.
  4. *No Confirmatory Test Generalization:* Because the $N=163$ test partition was inspected during earlier research debugging iterations, all test set evaluations are strictly designated as **EXPLORATORY / PREVIOUSLY INSPECTED**.

---

## 2. Primary Descriptive Outcomes: Paired Prediction Agreement and Transition Patterns

The primary scientific objective of this observational study is to quantify the extent and nature of verifier prediction sensitivity induced by translation shift, independent of ground truth labels.

### 2.1 Paired Prediction Agreement and Disagreement
When presented with translated English evidence versus original Hindi evidence, the verifier exhibits substantial prediction divergence:

| Split | Sample Size ($N$) | Identical Predictions ($k / N$) | Paired Agreement Rate [95% Wilson CI] | Disagreement / Flip Count | Disagreement Rate [95% Wilson CI] |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Development** | 103 | 41 / 103 | **39.81%** [30.88%, 49.46%] | 62 / 103 | **60.19%** [50.54%, 69.12%] |
| **Test (Exploratory)** | 163 | 59 / 163 | **36.20%** [29.22%, 43.81%] | 104 / 163 | **63.80%** [56.19%, 70.78%] |

### 2.2 Paired Label-Flip Transition Matrices

#### Test Split ($N=163$):
Rows represent predictions on Translated-English evidence; Columns represent predictions on Original-Hindi evidence:

| Translated $\downarrow$ \ Original $\rightarrow$ | `CONTRADICTED` | `INSUFFICIENT_EVIDENCE` | `SUPPORTED` | Total Translated |
|:---|:---:|:---:|:---:|:---:|
| **`CONTRADICTED`** | **21** (Preserved) | 5 | 18 | 44 |
| **`INSUFFICIENT_EVIDENCE`** | 23 | **14** (Preserved) | 18 | 55 |
| **`SUPPORTED`** | 31 | 9 | **24** (Preserved) | 64 |
| **Total Original** | 75 | 28 | 60 | **163** |

*Key Transition Observation:* Of the 64 instances where the verifier predicted `SUPPORTED` on translated English evidence, 31 (48.4%) flipped to `CONTRADICTED` when the verifier read the original Hindi text directly.

#### Development Split ($N=103$):
| Translated $\downarrow$ \ Original $\rightarrow$ | `CONTRADICTED` | `INSUFFICIENT_EVIDENCE` | `SUPPORTED` | Total Translated |
|:---|:---:|:---:|:---:|:---:|
| **`CONTRADICTED`** | **22** (Preserved) | 3 | 8 | 33 |
| **`INSUFFICIENT_EVIDENCE`** | 22 | **5** (Preserved) | 12 | 39 |
| **`SUPPORTED`** | 13 | 4 | **14** (Preserved) | 31 |
| **Total Original** | 57 | 12 | 34 | **103** |

---

## 3. Secondary Outcomes: Benchmark Performance, Latency, and Route Trade-Offs

Secondary evaluations assess system performance against the projected X-Fact dataset labels.

### 3.1 Construct Validity and Missing Positive Class Disclosure
- **Absence of Gold `SUPPORTED`:** In authentic fact-checking reporting in India within X-Fact, the gold label distribution is strictly skewed:
  - Development ($N=103$): 89 `CONTRADICTED` (86.4%), 14 `INSUFFICIENT_EVIDENCE` (13.6%), **0 `SUPPORTED` (0.0%)**.
  - Test ($N=163$): 142 `CONTRADICTED` (87.1%), 21 `INSUFFICIENT_EVIDENCE` (12.9%), **0 `SUPPORTED` (0.0%)**.
- **Label Mismatch:** X-Fact veracity ratings (`false`, `partly true`, `unproven`) represent document-level journalistic judgments, which are projected onto sentence-level NLI categories. Because gold `SUPPORTED` has zero support ($N=0$), all standard 3-class Macro-F1 scores contain an uninformative $F_1(\textsc{Supported}) = 0.0$ term.
- **Reporting Standard:**
  1. *Primary Descriptive F1:* **Observed 2-Class Macro-F1**, calculated strictly over the non-empty gold classes (`CONTRADICTED` and `INSUFFICIENT_EVIDENCE`).
  2. *Secondary Reference F1:* Nominal 3-Class Macro-F1, retained solely for structural comparison with 3-way benchmark definitions.
  3. *Trivial Majority Baseline:* Always predicting `CONTRADICTED` yields **87.12% accuracy**, nominal 3-class Macro-F1 of **0.3104**, and observed 2-class Macro-F1 of **0.4656**.

### 3.2 Canonical Test Results Summary ($N=163$)

| System Condition | Accuracy [95% CI] | Macro-F1 (2-Class Observed) | Macro-F1 (3-Class Nominal) | Coverage (%) | Mean E2E Latency (ms) | Paired McNemar vs Selective |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **No-Check (Translated Only)** | 28.22% [21.47%, 35.58%] | 0.3018 [0.2248, 0.3774] | 0.2012 [0.1498, 0.2516] | 0.0% | 3,650.4 ms | $p = 1.0000$ ($b=4, c=4$) |
| **Direct Multilingual (Original Only)** | 42.94% [35.57%, 50.92%] | 0.3700 [0.2972, 0.4537] | 0.2467 [0.1981, 0.3025] | 100.0% | 11,295.6 ms | $p = 0.0056$ ($b=23, c=47$) |
| **Always-Check (Dual Consensus Avg)** | 36.81% [29.45%, 44.17%] | 0.3657 [0.2852, 0.4534] | 0.2438 [0.1901, 0.3023] | 100.0% | 14,945.9 ms | $p = 0.0201$ ($b=9, c=23$) |
| **Selective-Check ($\tau^*=0.650$)** | 28.22% [21.47%, 35.58%] | 0.2950 [0.2175, 0.3741] | 0.1967 [0.1450, 0.2494] | 8.0% (13/163) | 4,613.8 ms | Reference System |
| **Random Control (100 Seeds, Matched Cov)** | 29.24% [26.38%, 31.90%] | 0.3082 [0.2810, 0.3326] | 0.2054 [0.1874, 0.2217] | 8.0% | 4,613.8 ms | $p = 0.2669$ ($b=4, c=9$) |

### 3.3 Development Utility Optimality Finding
On development data ($N=103$), evaluating the utility function $J = \text{Macro\_F1}_{3cl} - 0.15 \cdot \text{Coverage}$:
- **No-Check ($\tau = \infty$, Coverage = 0.0%):** $J = 0.2104 - 0.0000 = \mathbf{0.2104}$
- **Selective Cascade ($\tau^* = 0.650$, Coverage = 12.62%):** $J = 0.2213 - 0.0189 = \mathbf{0.2023}$

**Empirical Conclusion:** The No-Check baseline achieves the highest global utility on development data. Selective cascade routing is **not Pareto-optimal** relative to zero checking on development data. Threshold $\tau^* = 0.650$ is optimal strictly conditional on activating the cascade.

---

## 4. Prohibited vs. Permitted Scientific Claims

### Strictly Prohibited Claims (Violations of Integrity):
- **PROHIBITED:** Claiming that "translation errors caused $X\%$ of verifier failures."
- **PROHIBITED:** Claiming that "70% of translation errors were validated by bilingual human annotators." (All prior human annotation files were synthetic simulations and have been permanently quarantined in `audit/invalidated_synthetic_annotations/`).
- **PROHIBITED:** Claiming that selective-check routing achieves "superior fact-checking performance" or "outperforms the baseline."
- **PROHIBITED:** Claiming that this system validates an "end-to-end RAG architecture."
- **PROHIBITED:** Claiming that the exploratory test set confirms general out-of-sample validity.

### Permitted Observational Claims:
- Machine-translated evidence and original Hindi evidence produce 63.80% prediction disagreement on test instances.
- Verifying translated evidence alone yields 28.22% accuracy, significantly lower than verifying original Hindi evidence directly (42.94%, $p = 0.0056$).
- Consulting original Hindi evidence when translation risk is elevated ($\tau^* = 0.650$) does not significantly improve accuracy over translated-only verification (identical accuracy 28.22%, $p = 1.0000$).
- End-to-end inference latency on CPU scales from 3,650.4 ms (Translated-Only) to 4,613.8 ms (Selective-Check, 8.0% coverage) and 11,295.6 ms (Direct Multilingual).
