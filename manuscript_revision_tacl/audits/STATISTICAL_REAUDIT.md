# Comprehensive Statistical Re-Audit and Numerical Verification Report

**Workspace:** `manuscript_revision_tacl/`  
**Master Evaluator:** Senior NLP Statistical Auditor & Scientific Editor  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Audit Date:** 2026-10-24  
**Source of Truth:** `experiments/results_corrected/canonical_test_predictions.csv` ($N=163$) and `canonical_dev_predictions.csv` ($N=103$)  

---

## 1. Executive Summary of Audit Findings

Every numerical claim, contingency table count, confidence interval, McNemar test statistic, and permutation test p-value reported across the revised manuscript has been independently recomputed from first principles using Python 3.14, NumPy, SciPy, and Scikit-Learn.

### Summary Status Table
| Audit Area | Claimed in Prior Notes | Independently Recomputed | Audit Verdict |
| :--- | :--- | :--- | :---: |
| **Dataset Splits** | Dev: 103, Test: 163 | Dev: 103, Test: 163 | **VERIFIED** |
| **Test Class Imbalance** | 142 CON, 21 NEU, 0 SUP | 142 CON, 21 NEU, 0 SUP | **VERIFIED** |
| **Pairwise Disagreement** | 104 / 163 (63.80%) | 104 / 163 (63.80%) [56.19%, 70.78%] | **VERIFIED** |
| **No-Check Accuracy** | 46 / 163 (28.22%) | 46 / 163 (28.22%) [21.87%, 35.57%] | **VERIFIED** |
| **Direct Multi Accuracy** | 70 / 163 (42.94%) | 70 / 163 (42.94%) [35.59%, 50.62%] | **VERIFIED** |
| **Always-Check Accuracy** | 60 / 163 (36.81%) | 60 / 163 (36.81%) [29.79%, 44.44%] | **VERIFIED** |
| **Selective-Check Accuracy**| 46 / 163 (28.22%) | 46 / 163 (28.22%) [21.87%, 35.57%] | **VERIFIED** |
| **Supported $\to$ Contra Flip**| 31 / 64 (48.44%) | 31 / 64 (48.44%) [36.63%, 60.42%] | **VERIFIED** |
| **Contra $\to$ Supported Flip**| 18 / 44 (40.91%) | 18 / 44 (40.91%) [27.69%, 55.59%] | **VERIFIED** |
| **McNemar Test (NC vs DM)**| $\chi^2=6.7821, p=0.00877$| $\chi^2=6.7821, p_{\text{exact}}=0.008772$ | **VERIFIED** |
| **Macro-F1 Permutation Test**| $\Delta = -0.0455, p=0.1898$| $\Delta = -0.0455, p=0.18980$ | **VERIFIED WITH QUALIFICATION** |
| **Permutation Citation** | Benjamini & Hochberg (1995) | Erroneous citation for permutation test | **INCORRECT — CORRECTION REQUIRED** |
| **Multiple Testing Terminology** | "Family-wise error" | Conflated with False Discovery Rate (FDR) | **INCORRECT — CORRECTION REQUIRED** |

---

## 2. Dataset Composition and Ground-Truth Class Imbalance

### Recomputed Class Distributions
```text
Partition       CONTRADICTED    INSUFFICIENT_EVIDENCE    SUPPORTED    Total (N)
-------------  --------------  -----------------------  -----------  -----------
Development    89 (86.41%)     14 (13.59%)              0 (0.00%)    103
Held-Out Test  142 (87.12%)    21 (12.88%)              0 (0.00%)    163
Combined       231 (86.84%)    35 (13.16%)              0 (0.00%)    266
```

### Critical Audit Qualification (Zero Positive Class)
- **Impact on Evaluation:** In the $N=163$ test partition, there are **exactly zero gold `SUPPORTED` claims**.
- **Mathematical Consequences:**
  1. For any system $S$, the number of True Positives for `SUPPORTED` is identically zero ($TP_{\text{sup}} \equiv 0$).
  2. Recall for `SUPPORTED` is undefined or $0.0\%$. Precision is $0.0\%$ whenever the model predicts `SUPPORTED` at least once ($FP_{\text{sup}} > 0$).
  3. Consequently, $F_{1, \text{sup}} \equiv 0.0000$ for all models predicting at least one supported claim.
  4. 3-class Macro-F1 is mathematically bounded at an upper ceiling of $\frac{1}{3}(1.0 + 1.0 + 0.0) = 0.6667$.
  5. The effective 2-class Macro-F1 (evaluating only non-empty gold classes `CONTRADICTED` and `INSUFFICIENT_EVIDENCE`) satisfies the exact identity:
     $$\text{Macro-F1}_{2\text{cl}} = \frac{3}{2} \cdot \text{Macro-F1}_{3\text{cl}}$$
- **Auditor Verdict:** **VERIFIED WITH QUALIFICATION**. The manuscript must prominently state that factuality recall on true assertions cannot be validated on this benchmark.

---

## 3. Pairwise Prediction Sensitivity and 3x3 Transition Matrix

### Recomputed Prediction Counts
- **Total test instances:** $N = 163$
- **Concordant instances ($y_{\text{trans}} = y_{\text{orig}}$):** 59 (36.20%)
- **Discordant instances ($y_{\text{trans}} \ne y_{\text{orig}}$):** 104 (63.80%)
- **95% Wilson Score CI on Disagreement:** $[56.19\%, 70.78\%]$

### Recomputed 3x3 Transition Matrix
```text
Translated Prediction    Original Hindi: CONTRA    Original Hindi: INSUFF    Original Hindi: SUPPORTED    Row Total (N_trans)
---------------------    ----------------------    ----------------------    -------------------------    -------------------
CONTRADICTED             21 (12.88%)               5 (3.07%)                 18 (11.04%)                  44 (26.99%)
INSUFFICIENT             23 (14.11%)               14 (8.59%)                18 (11.04%)                  55 (33.74%)
SUPPORTED                31 (19.02%)               9 (5.52%)                 24 (14.72%)                  64 (39.26%)
---------------------    ----------------------    ----------------------    -------------------------    -------------------
Column Total (N_orig)    75 (46.01%)               28 (17.18%)               60 (36.81%)                  163 (100.00%)
```

### Directional Transition Proportions and CIs
1. **Supported to Refutation Flip ($y_{\text{trans}}=\text{SUPP} \to y_{\text{orig}}=\text{CONTRA}$):**
   - Count: $31 / 64$ instances ($48.44\%$)
   - Wilson 95% CI: $[36.63\%, 60.42\%]$
   - **Audit Finding:** Because gold `SUPPORTED` is 0, all 64 translated predictions were false positives; evaluating original Hindi restored 31 of them to correct refutations.
2. **Refutation to False Support Flip ($y_{\text{trans}}=\text{CONTRA} \to y_{\text{orig}}=\text{SUPP}$):**
   - Count: $18 / 44$ instances ($40.91\%$)
   - Wilson 95% CI: $[27.69\%, 55.59\%]$
   - **Audit Finding:** Demonstrates that original Hindi is not an infallible oracle; it incorrectly degrades 18 instances into false support.
3. **Uncertainty Resolution:**
   - 23 / 55 ($41.82\%$) neutral translated instances resolve to `CONTRADICTED` in Hindi.
   - 18 / 55 ($32.73\%$) neutral translated instances flip to `SUPPORTED` in Hindi.
   - Only 14 / 55 ($25.45\%$) remain stably neutral across both languages.

---

## 4. Benchmark Predictive Performance Metrics

Recomputed over $N=163$ test instances:

```text
System / Condition             Accuracy      95% Wilson CI     Macro-F1 (3cl)  Macro-F1 (2cl)  F1 (Contra)  F1 (Neutral)
-----------------------------  ------------  ----------------  --------------  --------------  -----------  ------------
No-Check (Translated)          0.2822 (46)   [0.2187, 0.3557]  0.2012          0.3018          0.4194       0.1842
Direct Multilingual (Orig)     0.4294 (70)   [0.3559, 0.5062]  0.2467          0.3700          0.6175       0.1224
Always-Check (Dual Consensus)  0.3681 (60)   [0.2979, 0.4444]  0.2438          0.3657          0.5347       0.1967
Selective-Check (Hard Route)   0.2822 (46)   [0.2187, 0.3557]  0.1967          0.2950          0.4278       0.1622
Ablation: Numeral-Only         0.4479 (73)   [0.3736, 0.5245]  0.2529          0.3794          0.6364       0.1224
Control: Random Routing        0.3129 (51)   [0.2467, 0.3877]  0.2175          0.3263          0.4607       0.1918
Majority Baseline (All Contra) 0.8712 (142)  [0.8116, 0.9139]  0.3104          0.4656          0.9311       0.0000
Oracle Upper Bound             0.5951 (97)   [0.5186, 0.6674]  0.3467          0.5200          0.7303       0.3099
```

### Critical Audit Findings on Performance
1. **Direct Multilingual Accuracy Advantage:**
   - $\Delta \text{Acc} = 0.4294 - 0.2822 = +0.1472$ (+14.72 percentage points, 24 additional correct instances).
2. **Selective-Check Performance:**
   - Triggers on exactly 13 / 163 instances ($7.98\%$ coverage).
   - Exactly 4 instances flip from incorrect to correct ($c=4$).
   - Exactly 4 instances flip from correct to incorrect ($b=4$).
   - Net accuracy gain: $0$ ($46/163 = 28.22\%$, identical to No-Check).
   - Macro-F1 actually drops slightly from 0.2012 to 0.1967 due to neutral-class precision penalties.
3. **The Majority-Class Baseline Paradox:**
   - Always predicting `CONTRADICTED` achieves $87.12\%$ accuracy.
   - All complex NLI pipelines (28.22%–42.94%) score lower on accuracy than the trivial majority baseline because they attempt to predict neutral and supported classes.

---

## 5. Paired Statistical Hypothesis Testing Audit

### Recomputed Contingency Statistics ($N=163$)
```text
Comparison Pair                  b   c   Disc  McNemar chi2  p_asymp   p_exact   FDR (q)   Delta_F1_3cl  Perm_p_3cl  Perm_FDR
-------------------------------  --  --  ----  ------------  --------  --------  --------  ------------  ----------  --------
No-Check vs Direct Multilingual  27  51  78    6.7821        0.009208  0.008772  0.017543  -0.04547      0.18980     0.22776
Selective vs Direct Multilingual 23  47  70    7.5571        0.005977  0.005583  0.016748  -0.05000      0.11800     0.22776
Selective vs Always-Check        9   23  32    5.2812        0.021556  0.020062  0.030092  -0.04712      0.01960     0.11760
Selective vs No-Check            4   4   8     0.1250        0.723674  1.000000  1.000000  -0.00450      0.75720     0.75720
Selective vs Random Control      4   9   13    1.2308        0.267257  0.266846  0.320215  -0.02080      0.16500     0.22776
Selective vs Numeral-Only        20  47  67    10.0896       0.001491  0.001307  0.007843  -0.05630      0.07440     0.22320
```

---

## 6. Mandatory Investigation: Macro-F1 Permutation Test & Citations

### 6.1 Code Audit of `paired_permutation_f1`
We inspected `scripts/run_corrected_experiments.py` (lines 82–98) and verified:
1. **Null Hypothesis:** Exchangeability of system predictions conditional on the instance:
   $$H_0: (y_A(i), y_B(i)) \stackrel{d}{=} (y_B(i), y_A(i)) \quad \forall i \in \{1, \dots, N\}$$
2. **Permutation Unit:** For each instance $i$, a Bernoulli(0.5) coin flip determines whether system A and system B swap predictions.
3. **Metric Calculation:** In every permutation $b \in \{1, \dots, B\}$, full $N=163$ prediction vectors $s_A^{(b)}$ and $s_B^{(b)}$ are constructed, and Macro-F1 is recomputed from the complete confusion matrices against the fixed gold vector $y_{\text{true}}$.
4. **Resamples & Seed:** $B=5,000$ permutations, deterministic NumPy seed 42.
5. **Observed Test Statistic & P-Value:**
   - No-Check vs Direct Multilingual: $\Delta \text{Macro-F1}_{3\text{cl}} = -0.04547$, two-sided empirical $p = 0.18980$.
   - Selective vs Direct Multilingual: $\Delta \text{Macro-F1}_{3\text{cl}} = -0.05000$, two-sided empirical $p = 0.11800$.

### 6.2 Citation and Methodological Error Discovered
- **The Error in Prior Draft:** The manuscript text cited `Benjamini and Hochberg (1995)` as the methodological citation for the permutation test itself:
  > *"We implement a non-parametric paired permutation test (Benjamini and Hochberg, 1995)..."*
- **Audit Verdict:** **INCORRECT — CORRECTION REQUIRED**.
  - **Reason:** Benjamini and Hochberg (1995) authored the seminal paper on *Controlling the False Discovery Rate (FDR)* for independent multiple tests. They did **not** introduce paired prediction-swap permutation tests for NLP evaluation.
  - **Proper Methodological Sources:**
    - Randomization and permutation testing foundations: Pitman (1937), Good (2000), Dudoit and van der Laan (2008).
    - Permutation testing for paired NLP evaluation metrics: Yeh (2000), *More accurate tests for the statistical significance of result differences*, COLING 2000.
  - **Required Action:** Decouple the permutation test description from Benjamini-Hochberg. Cite Yeh (2000) or Good (2000) for the permutation test, and cite Benjamini and Hochberg (1995) strictly in the subsection on FDR multiple-comparison control.

---

## 7. Multiple Comparisons and FDR Control Audit

### Conflation Discovered in Text
- **Prior Draft Phrasing:** The manuscript stated: *"Benjamini-Hochberg adjustments are reported for family-wise error control."*
- **Audit Verdict:** **INCORRECT — CORRECTION REQUIRED**.
  - **Reason:** The Benjamini-Hochberg (BH) step-up procedure controls the **False Discovery Rate (FDR)**:
    $$\text{FDR} = \mathbb{E}\left[\frac{V}{\max(R, 1)}\right] \le \frac{m_0}{m} q \le q$$
    It does **not** control the Family-Wise Error Rate (FWER = $P(V \ge 1)$). FWER control requires Bonferroni, Holm-Bonferroni, or Hochberg FWER procedures, which are far more conservative.
  - **Adjustment Family Definition:** The family comprises the $m=6$ primary pairwise comparisons between system configurations.
  - **Recomputed Benjamini-Hochberg FDR $q$-values:**
    - No-Check vs Direct Multilingual: Raw $p = 0.008772 \to q = 0.017543$ (Significant at $q < 0.05$).
    - Selective vs Direct Multilingual: Raw $p = 0.005583 \to q = 0.016748$ (Significant at $q < 0.05$).
    - Selective vs Numeral-Only: Raw $p = 0.001307 \to q = 0.007843$ (Significant at $q < 0.01$).
  - **Required Action:** Replace all occurrences of "family-wise error control" with "False Discovery Rate (FDR) control" when referring to Benjamini-Hochberg.

---

## 8. Diagnostic Error Attribution Decomposition

Recomputed from `experiments/results_corrected/canonical_error_attribution.json`:

```text
Outcome Stratum                                           Count    Subgroup %    Test Set %
-------------------------------------------------------  -------  ------------  -----------
Partition of Translated Failures (N_fail = 117):
  Recovered by Hindi (S_trans: Trans Wrong, Orig Right)     51       43.59%        31.29%
  Unrecovered (S_verif: Both Representations Wrong)         66       56.41%        40.49%

Partition of Translated Successes (N_succ = 46):
  Control (Both Representations Correct)                    19       41.30%        11.66%
  Degraded by Hindi (S_degraded: Trans Right, Orig Wrong)   27       58.70%        16.56%
-------------------------------------------------------  -------  ------------  -----------
Total Evaluated Instances                                  163        ---         100.00%
```

### Key Analytical Insights
- **Net Gain:** Original Hindi recovers 51 instances while degrading 27 instances, yielding a net difference of $51 - 27 = +24$ correct instances ($70 - 46 = 24$).
- **Ceiling of Machine Translation Damage:** At most $43.59\%$ of translated-evidence failures can be attributed to translation artifacts, because the remaining $56.41\%$ fail even when evaluated on clean, original Hindi evidence.
