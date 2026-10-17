# Metric Validity and Computational Cost Audit

**Project:** Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Audit Date:** 2026-10-24  
**Protocol Version:** `v1.0-observational`  

---

## 1. Metric Validity and Distribution Alignment

### 1.1 Primary Metric: Paired Prediction Sensitivity and Disagreement
Because the research is an observational inquiry into verifier sensitivity under translation shift, the primary scientific outcomes evaluate paired behavioral divergence under identical claim inputs:
- **Paired Prediction Disagreement:** $104 / 163 = \mathbf{63.80\%}$ [95% Wilson CI: 56.19%, 70.78%].
- **Paired Prediction Agreement:** $59 / 163 = \mathbf{36.20\%}$ [95% Wilson CI: 29.22%, 43.81%].
- **State Transition Probability ($\text{SUP}_{\text{trans}} \to \text{CON}_{\text{orig}}$):** $31 / 64 = \mathbf{48.44\%}$ [95% Wilson CI: 36.63%, 60.42%].
- **State Transition Probability ($\text{CON}_{\text{trans}} \to \text{SUP}_{\text{orig}}$):** $18 / 44 = \mathbf{40.91\%}$ [95% Wilson CI: 27.69%, 55.59%].
- **State Transition Probability ($\text{NEU}_{\text{trans}} \to \text{CON}_{\text{orig}}$):** $23 / 55 = \mathbf{41.82\%}$ [95% Wilson CI: 29.74%, 54.97%].

### 1.2 Secondary Benchmark Metrics & The Missing Positive Class
As documented in `audit/DATA_AND_LABEL_AUDIT.md`, the Hindi test split contains 142 `CONTRADICTED` and 21 `INSUFFICIENT_EVIDENCE` instances, and 0 `SUPPORTED` instances.
- **Observed 2-Class Macro-F1:** Evaluates the harmonic mean of precision and recall over the two empirically present classes (`CONTRADICTED` and `INSUFFICIENT_EVIDENCE`).
  - No-Check: $0.3018$ [95% CI: 0.2248, 0.3774]
  - Selective-Check ($\tau^*=0.650$): $0.2950$ [95% CI: 0.2175, 0.3741]
  - Direct Multilingual: $0.3700$ [95% CI: 0.2972, 0.4537]
- **Nominal 3-Class Macro-F1:** Retained for continuity with standard NLI benchmarks; penalizes the unobserved `SUPPORTED` class ($F_{1,\text{SUP}} = 0.0$):
  - No-Check: $0.2012$ [95% CI: 0.1498, 0.2516]
  - Selective-Check: $0.1967$ [95% CI: 0.1450, 0.2494]
  - Direct Multilingual: $0.2467$ [95% CI: 0.1981, 0.3025]
- **Observed Accuracy:**
  - Bounded above by the majority-class baseline (predicting `CONTRADICTED` for all instances achieves $142 / 163 = \mathbf{87.12\%}$).
  - All classification accuracy values (28.22% for No-Check and Selective-Check; 42.94% for Direct Multilingual) are explicitly labeled as **secondary proxy measures** of real-world veracity alignment rather than native 3-class NLI accuracy.

---

## 2. Statistical Significance Testing and Multiplicity Control

Paired comparisons were evaluated using exact binomial McNemar tests on discordant classification pairs ($b, c$), with Benjamini-Hochberg FDR adjustments applied across all pairwise contrasts:

| Hypothesis Contrast | Discordant Pairs ($b, c$) | McNemar $\chi^2$ | Raw $p$-value | FDR-Adjusted $p$-value | Statistical Conclusion |
|---|---|---|---|---|---|
| **Selective-Check vs. No-Check** | $b=4, c=4$ | 0.1250 | $1.0000$ | $1.0000$ | Completely non-significant; zero net accuracy change |
| **Selective-Check vs. Direct Multilingual** | $b=23, c=47$ | 7.5571 | $0.00558$ | $\mathbf{0.00670}$ | Statistically significant; Direct Multi outperforms Selective |
| **Selective-Check vs. Always-Check** | $b=9, c=23$ | 5.2812 | $0.02006$ | $\mathbf{0.04012}$ | Statistically significant; Always-Check outperforms Selective |
| **Selective-Check vs. Random Control (100 Seeds)** | $b=4, c=9$ (mean) | 1.2308 | $0.26685$ | $0.42696$ | Non-significant; Selective does not beat random routing |
| **Selective-Check vs. Numeral-Only Routing** | $b=20, c=47$ | 10.0896 | $0.00131$ | $\mathbf{0.00524}$ | Statistically significant; Numeral routing triggers 96.3% |

---

## 3. Computational Cost and Latency Accounting Audit

Every latency metric reported in the benchmark table was audited to verify that it reflects real measured forward-pass execution times rather than synthetic approximations:

### 3.1 Measurement Setup
- **Hardware:** Intel/AMD 64-bit CPU architecture, 8 evaluation threads.
- **Warmup:** Two dummy inference cycles executed prior to timed runs to eliminate JIT and caching skew.
- **Timing Primitive:** High-precision Python `time.perf_counter()`, converted to milliseconds.

### 3.2 Component and End-to-End Latency Values ($N=163$)

| System Configuration | MT Translation Time ($T_{\text{MT}}$) | Translated Verifier ($T_{\text{trans}}$) | Original Verifier ($T_{\text{orig}}$) | Mean End-to-End Latency | Latency Reduction vs. Direct Multi |
|---|---|---|---|---|---|
| **No-Check (Translated Only)** | 1,820.2 ms | 1,830.2 ms | 0.0 ms | **3,650.4 ms** | 67.7% reduction |
| **Selective-Check ($\tau^*=0.650$)** | 1,820.2 ms | 1,830.2 ms | 963.4 ms (on 7.98% routed) | **4,613.8 ms** | **59.2% reduction** |
| **Direct Multilingual (Original)** | 0.0 ms | 0.0 ms | 11,295.6 ms | **11,295.6 ms** | Reference (0.0%) |
| **Always-Check (Dual Consensus)** | 1,820.2 ms | 1,830.2 ms | 11,295.6 ms | **14,945.9 ms** | 32.3% increase |

### 3.3 Latency Takeaways
1. **Coupling Integrity:** For every instance $i$, the exact translation $E_i^{\text{en}}$ generated during the $T_i^{\text{MT}}$ timing window is the string passed to the translated verifier.
2. **Selective-Check Efficiency:** Selective-Check consults Hindi evidence on 7.98% of instances, reducing mean latency by 59.2% relative to Direct Multilingual verification (4,613.8 ms vs. 11,295.6 ms), but at the cost of lower observed accuracy (28.22% vs. 42.94%).
