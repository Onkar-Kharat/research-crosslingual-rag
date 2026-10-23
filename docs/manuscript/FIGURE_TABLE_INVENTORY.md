# Manuscript Figure and Table Inventory

**Project Title:** Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Date:** 2026-10-24  
**Audit Standard:** 100% Deterministic Reproducibility from Frozen Canonical Data  

---

## 1. Table Inventory

| Table Label | File Location | Purpose & Scientific Content | Primary Source File | Generation / Extraction Script | Manuscript Section | Validation Status |
|---|---|---|---|---|---|---|
| **Table 1** | `tables/dataset_distribution.tex` | Benchmark class distributions for Dev ($N=103$) and Test ($N=163$), highlighting zero gold \textsc{Supported} instances | `data/processed/dev.jsonl`, `data/processed/test.jsonl` | `tests/test_data_integrity.py` | Section 4 (Experimental Setup) | **VERIFIED** |
| **Table 2** | `tables/transition_matrix.tex` | Complete $3 \times 3$ contingency matrix cross-tabulating translated vs original predictions | `experiments/results_canonical/canonical_test_predictions.csv` | `tests/test_directional_flips.py` | Section 5.1 (Prediction Sensitivity) | **VERIFIED** |
| **Table 3** | `tables/main_results.tex` | Main benchmark performance across 4 conditions + 4 controls/ablations (Accuracy [95% CI], F1, Latency, Coverage) | `experiments/results_canonical/canonical_benchmark_table.csv` | `scripts/run_corrected_experiments.py` | Section 5.2 (Main Benchmark Results) | **VERIFIED** |
| **Table 4** | `tables/statistical_tests.tex` | Paired McNemar tests, exact binomial $p$-values, permutation Macro-F1 tests, and FDR adjustments | `experiments/results_canonical/canonical_statistical_tests.csv` | `scripts/run_corrected_experiments.py` | Section 5.3 (Statistical Significance) | **VERIFIED** |
| **Table 5** | `tables/error_attribution.tex` | Diagnostic outcome strata partitioning 117 translated failures ($S_{\text{trans}}$, $S_{\text{verif}}$) and 46 successes ($S_{\text{degraded}}$, Control) | `experiments/results_canonical/canonical_test_predictions.csv` | `scripts/run_corrected_experiments.py` | Section 6 (Error Attribution & Strata) | **VERIFIED** |
| **Table 6** | `tables/case_studies.tex` | Qualitative case studies from authentic Hindi X-Fact items illustrating recovery, degradation, and double-failure modes | `experiments/results_canonical/canonical_test_predictions.csv` | `tests/test_directional_flips.py` | Section 6.2 (Qualitative Case Studies) | **VERIFIED** |

---

## 2. Figure Inventory

| Figure Label | File Location | Description & Visual Content | Source Data | Generation Script | Section | Accessibility Notes | Validation Status |
|---|---|---|---|---|---|---|---|
| **Figure 1** | `figures/pdf/fig1_study_workflow.pdf` | System architecture and paired evaluation pipeline diagram (No-Check vs Direct Multilingual vs Selective-Check) | System Architecture Specification | TikZ / Vector PDF Source | Section 3 (Methodology) | High-contrast vector graphic with descriptive text callouts | **VERIFIED** |
| **Figure 2** | `figures/pdf/fig2_risk_coverage_tradeoff.pdf` | Risk-coverage tradeoff curve on Dev ($N=103$) showing optimal threshold $\tau^*=0.650$ under penalized utility $\mathcal{J}$ | `experiments/results_canonical/canonical_dev_tuning.csv` | `scripts/generate_publication_figures.py` | Section 3.3 (Threshold Calibration) | Distinct markers, labeled axes, high-contrast red callout box | **VERIFIED** |
| **Figure 3** | `figures/pdf/fig3_condition_comparison.pdf` | Grouped bar chart comparing Accuracy and Macro-F1 with exact 95% bootstrap confidence interval error bars | `experiments/results_canonical/canonical_benchmark_table.csv` | `scripts/generate_publication_figures.py` | Section 5.2 (Main Results) | Colorblind-safe palette (Royal Blue / Forest Green), in-bar values | **VERIFIED** |
| **Figure 4** | `figures/pdf/fig4_error_attribution_breakdown.pdf` | Bar chart decomposing the 117 No-Check verification failures into $S_{\text{trans}}$, $S_{\text{verif}}$, and degraded outcomes | `experiments/results_canonical/canonical_error_attribution.json` | `scripts/generate_publication_figures.py` | Section 6.1 (Failure Decomposition) | Clear subgroup labels, percentages, and case counts | **VERIFIED** |
| **Figure 5** | `figures/pdf/fig5_transition_heatmap.pdf` | $3 \times 3$ confusion heatmap of prediction transitions between translated English and original Hindi evidence | `experiments/results_canonical/canonical_test_predictions.csv` | `scripts/generate_publication_figures.py` | Section 5.1 (Transition Heatmap) | Monochrome Blues colormap with high-contrast text annotations | **VERIFIED** |
