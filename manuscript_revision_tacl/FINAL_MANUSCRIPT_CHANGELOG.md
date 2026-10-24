# Final Manuscript Revision Changelog

**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Date:** 2026-10-24  
**Authoritative Revision Workspace:** `manuscript_revision_tacl/`  
**Authors:** Onkar Kharat (Lead Researcher & Author), Himanshu Jadhav (Co-Author & Contributor)  

---

## 1. Structural and Workspace Organization
- **Workspace Isolation:** Created dedicated `manuscript_revision_tacl/` workspace with modular subdirectories (`sections/`, `tables/`, `figures/final/`, `figures/source/`, `supplementary/`, `build/`, `audits/`).
- **Original Manuscript Preservation:** Hashed all 40 files in `docs/manuscript/` into `original_manuscript_hashes.json` prior to edits; automated validation verified 40/40 files remain bitwise identical at completion.
- **Master Entry Point:** Configured `manuscript_revision_tacl/main.tex` with TACL 2021v1 guidelines, `\graphicspath`, and documented toggles for anonymous peer review (`submission`) vs. camera-ready author block (`acceptedWithA`).

---

## 2. Textual Revisions Across Sections
- **`sections/abstract.tex`:**
  - Formulated the core empirical trade-off: pivot representation leverage vs. semantic distortion.
  - Reported exact canonical metrics: 63.80\% disagreement (104/163), 48.44\% SUP $\to$ CON flips (31/64), Direct Multilingual 42.94\% vs No-Check 28.22\% ($p=0.008772$, $b=27, c=51$).
  - Clarified non-significant permutation test on Macro-F1 ($p=0.1898$ and $p=0.1180$) and severe class skew (0.0\% gold \textsc{Supported}).
- **`sections/introduction.tex`:**
  - Grounded cross-lingual verification within RAG architectures and cited primary literature (XRAG, CrossRAG, All Languages Matter).
  - Explicitly established four empirical guardrails: pre-retrieved evidence (not end-to-end RAG), observational sensitivity (not translation causality), exploratory diagnostic status (not blind confirmatory holdout), and benchmark imbalance disclosure.
- **`sections/related_work.tex`:**
  - Structured into four thematic subsections: Multilingual RAG, Cross-lingual fact verification, Translation shift distortion, and Selective prediction cascades.
  - Integrated Table~\ref{tab:prior_work_matrix} comparing present study against 6 prior works across task, language setting, architecture, evaluation design, and key empirical distinctions.
- **`sections/task_and_formulation.tex`:**
  - Formulated claim verification as a 3-class NLI mapping.
  - Mathematically formalized the four paired conditions: No-Check ($\hat{y}_{\text{nc}}$), Direct Multilingual ($\hat{y}_{\text{dm}}$), Always-Check ($\hat{y}_{\text{ac}}$), and Selective-Check ($\hat{y}_{\text{sc}}$).
  - Specified hard routing in Selective-Check with triggered posterior averaging evaluated as an explicit ablation.
- **`sections/methodology.tex`:**
  - Documented X-Fact Hindi data provenance, pre-retrieved evidence grounding, MT MarianMT pipeline, and \texttt{mDeBERTa-v3-base} verifier configuration.
  - Integrated Figure 1 (`fig1_study_workflow.pdf`) and Figure 2 (`fig2_risk_coverage_tradeoff.pdf`).
  - Transparently disclosed that zero-check baseline utility ($J=0.2104$) exceeded peak cascade utility ($J=0.2023$) on dev data prior to test evaluation.
- **`sections/experimental_setup.tex`:**
  - Formulated the mathematical impact of the missing gold \textsc{Supported} class ($TP \equiv 0$).
  - Defined 2-class observed Macro-F1 ($\frac{3}{2}\text{Macro-F1}_3$) alongside nominal 3-class Macro-F1.
  - Rigorously detailed McNemar paired 2x2 contingency test with continuity correction and the non-parametric paired prediction-swap permutation test ($B=5,000$, seed 42).
- **`sections/results.tex`:**
  - Structured around the four pre-registered research questions (RQ1--RQ4).
  - Integrated Figure 3 (`fig3_condition_comparison.pdf`), Figure 4 (`fig4_error_attribution_breakdown.pdf`), and Figure 5 (`fig5_transition_heatmap.pdf`).
  - Resolved historical McNemar contingency cell attributions ($b=27, c=51$ for No-Check vs Direct Multi; $b=23, c=47$ for Selective vs Direct Multi).
  - Provided deep statistical analysis explaining metric divergence between McNemar accuracy significance ($p < 0.01$) and Macro-F1 permutation non-significance ($p > 0.10$).
- **`sections/discussion.tex`:**
  - Analyzed spurious entailment and lexical refutation recovery.
  - Detailed three qualitative case studies illustrating recovery, degradation, and dual-failure modes.
  - Explained why unconditional consensus fails (high-confidence corrupted posteriors overpower calibrated predictions) and why surface risk triggers struggle (MSP miscalibration under distribution shift).
- **`sections/limitations.tex`:**
  - Comprehensively articulated ten distinct limitation dimensions: single language pair, sample size ($N=163$), extreme class skew, exploratory status, single verifier backbone, single MT model, pre-retrieved evidence scope, pending bilingual human validation, observational vs causal sensitivity, and heuristic risk gating scope.
- **`sections/conclusion.tex`:**
  - Summarized supported findings without overclaiming.
- **`supplementary/supplementary_material.tex`:**
  - Detailed hardware specifications, development set calibration grid search table, per-system confusion matrices, bilingual human annotation protocol, and reproducibility instructions.

---

## 3. Tables and Figures Revisions
- **`tables/dataset_distribution.tex`:** Updated to exact canonical counts for development split (89 CON, 14 NEU, 0 SUP; $N=103$) and test split (142 CON, 21 NEU, 0 SUP; $N=163$).
- **`tables/transition_matrix.tex`:** Verified complete $3\times 3$ contingency counts (59 agreed, 104 disagreed); normalized cross-reference label.
- **`tables/main_results.tex`:** Standardized 4 main systems and 4 controls/ablations with exact Wilson score 95% CIs and CPU latencies; normalized cross-reference label.
- **`tables/statistical_tests.tex`:** Standardized paired McNemar tests and permutation tests with both raw and FDR Benjamini-Hochberg adjusted p-values; normalized cross-reference label.
- **`tables/error_attribution.tex`:** Verified disjoint error partition ($S_{\text{trans}}=51, S_{\text{verif}}=66, S_{\text{degraded}}=27, \text{Control}=19$); normalized cross-reference label.
- **`tables/case_studies.tex`:** Cleaned and formatted qualitative items with explicit English translations.
- **Figures 1--5:** Sourced from verified deterministic plotting script (`generate_figures.py`) as high-contrast, colorblind-safe vector PDFs in `figures/final/`.

---

## 4. Citation and Bibliography Revisions
- Audited `references.bib` against primary publishers and ACL Anthology.
- Achieved perfect 1:1 citation parity: 15 BibTeX entries, 15 cited in-text, 0 missing, 0 uncited.
- Protected acronyms and proper names with braces (`{XRAG}`, `{FEVER}`, `{X-FACT}`, `{OPUS-MT}`, etc.).

---

## 5. Verification and Auditing
- Produced 9 comprehensive audit artifacts in `manuscript_revision_tacl/audits/`:
  1. `MANUSCRIPT_INITIAL_AUDIT.md`
  2. `CLAIM_EVIDENCE_MATRIX.csv` (22 verified claims)
  3. `MANUSCRIPT_DISCREPANCY_LOG.md` (5 resolved historical items)
  4. `MANUSCRIPT_FACT_CHECK.md` (40 itemized verified facts)
  5. `CITATION_AUDIT.md` (15 verified citations)
  6. `TACL_FORMAT_AUDIT.md` (10 compliance dimensions)
  7. `FIGURE_TABLE_AUDIT.md` (6 tables and 5 figures, updated with zero-collision visual overhaul)
  8. `BUILD_AUDIT.md` (Test results and build verification)
  9. `PLAGIARISM_AUDIT.md` (Similarity index 0.245% 4-grams, 0.000% 5-grams; strictly < 20.0%)
- Automated validation suite `validate_manuscript.py` passed with 0 errors and 0 warnings.
- Repository test suite passed 47/47 tests.

---

## 6. Figure Visual Enhancement and Overlap Elimination
- **Comprehensive Overhaul of Figures 1–5:**
  - **Fig 1 (`fig1_study_workflow`):** Overhauled card layout; updated all numbers to canonical values ($\tau^*=0.650$, Selective-Check $28.22\%$ accuracy and $8.0\%$ coverage, Always-Check $36.81\%$, Diagnostic Error Strata $N=117$, $S_{\text{trans}}=51, S_{\text{verif}}=66, S_{\text{degraded}}=27$); zero overlapping arrows or badges.
  - **Fig 2 (`fig2_risk_coverage_tradeoff`):** Relocated red callout annotation from `(opt_cov - 20)` (which collided with the Y-axis label and tick numbers) to `(opt_cov + 17, opt_f1 + 0.13)`, completely resolving the Y-axis label and tick text overlap; adjusted $y$-limits to $[0.08, 0.60]$.
  - **Fig 3 (`fig3_condition_comparison`):** Enhanced grouped bar chart with Royal Blue (`#1e40af`) and Emerald (`#059669`) bars; added dark rounded pill badges behind in-bar values to guarantee zero whisker collision; added clear baseline dashed line.
  - **Fig 4 (`fig4_error_attribution_breakdown`):** Increased x-axis labelpad to 14; widened layout to avoid multi-line label crowding; color-coded strata ($S_{\text{trans}}=51, S_{\text{verif}}=66, S_{\text{degraded}}=27$); added clean count/percentage annotations.
  - **Fig 5 (`fig5_transition_heatmap`):** Explicitly disabled background grid lines (`ax.grid(False)`) so grid dashes no longer cross through numbers and percentages; set high-contrast white text for dark cells and navy for light cells; added padding to colorbar.
- **Artifact Formats:** Sourced as both vector PDFs in `manuscript_revision_tacl/figures/final/` and 300-DPI high-resolution PNGs in `manuscript_revision_tacl/figures/source/`.
