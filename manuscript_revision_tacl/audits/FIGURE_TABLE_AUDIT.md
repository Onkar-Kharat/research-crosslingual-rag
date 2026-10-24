# Figure and Table Verification and Presentation Audit

**Audit Date:** 2026-10-24  
**Audit Scope:** Verification of all figure assets and LaTeX table environments against canonical frozen data  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Workspace:** `manuscript_revision_tacl/`  

---

## 1. Executive Summary

All figures and tables in the revised manuscript have been systematically verified against canonical data records in `canonical_results.csv`, `experiments/results_canonical/`, and `results/canonical/`. Table environments have been standardized using `booktabs` formatting without vertical gridlines. Cross-reference labels have been normalized (`tab:...` and `fig:...`). All figures are available as publication-quality vector PDFs and high-resolution PNGs.

---

## 2. Table Audit

| Table ID | File Path | Data Source | Canonical Metric / Range | Changes Made in Revision | Status |
|:---|:---|:---|:---|:---|:---:|
| **Table 1** | `tables/dataset_distribution.tex` | `data/processed/dev.jsonl`, `data/processed/test.jsonl` | Dev: 89 CON (86.4%), 14 NEU (13.6%), 0 SUP ($N=103$); Test: 142 CON (87.1%), 21 NEU (12.9%), 0 SUP ($N=163$); Total: 231 CON (86.8%), 35 NEU (13.2%), 0 SUP ($N=266$). | Corrected dev split transcription anomaly from draft; aligned label to `tab:dataset_distribution`. | `VERIFIED` |
| **Table 2** | `tables/transition_matrix.tex` | `experiments/results_canonical/canonical_test_predictions.csv` | Full $3\times 3$ contingency table: Agreement = 59/163 (36.20%), Disagreement = 104/163 (63.80%). Critical flip SUP $\to$ CON = 31/64 (48.44%). | Normalized cross-reference label to `tab:transition_matrix`; verified row and column marginal sums. | `VERIFIED` |
| **Table 3** | `tables/main_results.tex` | `experiments/results_canonical/canonical_benchmark_table.csv` | No-Check: Acc 0.2822, F1 (3cl) 0.2012, F1 (2cl) 0.3018, Latency 3650.4 ms; Direct Multi: Acc 0.4294, F1 (3cl) 0.2467, F1 (2cl) 0.3700, Latency 11295.6 ms; Always-Check: Acc 0.3681, F1 (3cl) 0.2438, F1 (2cl) 0.3657, Latency 14945.9 ms; Selective-Check: Acc 0.2822, F1 (3cl) 0.1967, F1 (2cl) 0.2950, Latency 4613.8 ms, Coverage 8.0%. | Updated table label to `tab:main_results`; added full ablations and controls with exact canonical metrics and Wilson score CIs. | `VERIFIED` |
| **Table 4** | `tables/statistical_tests.tex` | `results/statistical_tests/canonical_statistical_tests.csv` | McNemar tests: No-Check vs Direct Multi ($b=27, c=51, \chi^2=6.7821, p=0.008772$); Selective vs Direct Multi ($b=23, c=47, \chi^2=7.5571, p=0.005583$); Selective vs Always-Check ($b=9, c=23, \chi^2=5.2812, p=0.02006$); Selective vs No-Check ($b=4, c=4, \chi^2=0.1250, p=1.0000$). Permutation tests on Macro-F1: No-Check vs Direct Multi ($p=0.18980$); Selective vs Direct Multi ($p=0.11800$). | Updated label to `tab:statistical_tests`; clearly formatted both raw and FDR-adjusted p-values. | `VERIFIED` |
| **Table 5** | `tables/error_attribution.tex` | `experiments/results_canonical/canonical_test_predictions.csv` | 117 translation failures: 51 recovered by original ($S_{\text{trans}}$, 43.6%), 66 unrecovered ($S_{\text{verif}}$, 56.4%). 46 translation successes: 19 control (41.3%), 27 degraded ($S_{\text{degraded}}$, 58.7%). | Updated label to `tab:error_attribution`; verified disjoint error partition. | `VERIFIED` |
| **Table 6** | `tables/case_studies.tex` | `experiments/results_canonical/canonical_test_predictions.csv` | Concrete examples for $S_{\text{trans}}$ (`xfact-hi-test-0005`), $S_{\text{degraded}}$ (`xfact-hi-test-0003`), and $S_{\text{verif}}$ (`xfact-hi-test-0004`). | Updated label to `tab:case_studies`; cleaned English paraphrases. | `VERIFIED` |

---

## 3. Figure Audit & Visual Overhaul

| Figure ID | File Path | Vector Source | Generation Script | Purpose, Enhancements & Collision Fixes | Status |
|:---|:---|:---|:---|:---|:---:|
| **Figure 1** | `figures/final/fig1_study_workflow.pdf` | Vector PDF (95.9 KB) | `figures/source/generate_figures.py` | Architectural cascade diagram. Overhauled modular card dimensions, unified font families (`DejaVu Serif`), eliminated all crossing arrows and badge collisions, updated card contents strictly to canonical test evaluation values ($\tau^*=0.650$, Selective-Check $28.22\%$ accuracy, Diagnostic strata $N=117$). | `VERIFIED` |
| **Figure 2** | `figures/final/fig2_risk_coverage_tradeoff.pdf` | Vector PDF (71.5 KB) | `figures/source/generate_figures.py` | Dev calibration curve ($N=103$). Relocated optimal operating point callout box from $(opt\_cov - 20)$ (which previously collided with the Y-axis label and tick numbers) to $(opt\_cov + 17, opt\_f1 + 0.13)$, placing it in the open upper quadrant with zero label overlap. | `VERIFIED` |
| **Figure 3** | `figures/final/fig3_condition_comparison.pdf` | Vector PDF (70.1 KB) | `figures/source/generate_figures.py` | Held-out test performance ($N=163$). Styled with Royal Blue (`#1e40af`) and Emerald (`#059669`) bars; placed dark rounded pill badges behind in-bar value labels at $y=0.05$ to completely eliminate whisker and error-bar collisions. | `VERIFIED` |
| **Figure 4** | `figures/final/fig4_error_attribution_breakdown.pdf` | Vector PDF (89.2 KB) | `figures/source/generate_figures.py` | Diagnostic outcome stratification ($N=163$). Increased x-axis labelpad to 14, widened bar separation, color-coded strata ($S_{\text{trans}}=51, S_{\text{verif}}=66, S_{\text{degraded}}=27$), and centered multi-line categorical explanations without crowding. | `VERIFIED` |
| **Figure 5** | `figures/final/fig5_transition_heatmap.pdf` | Vector PDF (56.0 KB) | `figures/source/generate_figures.py` | Directional prediction transition matrix ($N=163$). Explicitly disabled background Cartesian grid lines (`ax.grid(False)`) to prevent dashed grid lines from intersecting in-cell numbers; set high-contrast white text on dark cells and navy text on light cells. | `VERIFIED` |

---

## 4. Accessibility and Typography Compliance

1. **Zero Text Collisions:** Every figure has been audited and rendered at print resolution with verified bounding boxes, ensuring zero text-to-axis, text-to-line, or text-to-whisker collisions.
2. **Colorblind-Safe Palettes:** All color figures utilize blue/teal/orange palettes with distinct line styles and hatch markers to avoid relying on color alone.
3. **Resolution and Vector Rendering:** All final figures included in LaTeX are vector PDFs, ensuring crisp text and vector line rendering at any print resolution. High-resolution 300-DPI raster PNGs are also maintained in `figures/source/`.
4. **Table Formatting:** All tables conform strictly to ACL/TACL style guidelines, utilizing `booktabs` (`\toprule`, `\midrule`, `\bottomrule`) with zero vertical rules and proper mathematical font typesetting.
