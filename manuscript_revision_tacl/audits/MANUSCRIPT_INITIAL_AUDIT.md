# Initial Manuscript and Repository Audit (TACL Submission Track)

**Audit Date:** 2026-10-24  
**Auditor:** Senior NLP Researcher & Scientific Editor Agent  
**Authoritative Project Root:** `c:\Users\Onkar\OneDrive\Desktop\Research_crosslingual_rag_research`  
**Original Manuscript Baseline:** `docs/manuscript/` (Frozen & Bitwise Preserved)  
**Revised Manuscript Target:** `manuscript_revision_tacl/`  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Authors:** Onkar Kharat (Lead Researcher & Author), Himanshu Jadhav (Co-Author & Contributor)  

---

## 1. Project and Manuscript Locations

- **Workspace Root:** `c:\Users\Onkar\OneDrive\Desktop\Research_crosslingual_rag_research`
- **Original Manuscript Entry Point:** `docs/manuscript/main.tex`
- **Revised Manuscript Entry Point:** `manuscript_revision_tacl/main.tex`
- **Git HEAD Commit:** `90ab224` (Branch: `main`)
- **Python Virtual Environment:** `.venv\Scripts\python.exe` (Python 3.14.7 AMD64)
- **Primary Canonical Outputs:**
  - `canonical_results.csv` (SHA-256 verified)
  - `experiments/results_canonical/canonical_test_predictions.csv` ($N=163$)
  - `experiments/results_canonical/canonical_benchmark_table.csv`
  - `results/canonical/test_metrics.json`
  - `results/statistical_tests/canonical_statistical_tests.csv`

---

## 2. Original Manuscript Inventory

The original manuscript package in `docs/manuscript/` comprises 40 distinct files across 3 directories:
- **Root Files (14 files):**
  - `main.tex`: Master entry point
  - `tacl2021v1.sty`: Official TACL style macro package
  - `acl_natbib.bst`: Official ACL/TACL BibTeX bibliography style
  - `references.bib`: BibTeX citations (24 entries)
  - `supplementary_material.tex`: Detailed appendices and operational profiles
  - Audit logs and reports: `BUILD_AUDIT.md`, `CITATION_AUDIT.md`, `CLAIM_EVIDENCE_MATRIX.csv`, `FIGURE_TABLE_INVENTORY.md`, `FINAL_HANDOFF_REPORT.md`, `MANUSCRIPT_FACT_CHECK.md`, `MANUSCRIPT_VALIDATION_REPORT.md`, `REPOSITORY_MIGRATION_LOG.md`, `build_instructions.md`
- **Sections (`sections/` - 10 files):**
  - `abstract.tex` (2,198 bytes)
  - `introduction.tex` (6,567 bytes)
  - `related_work.tex` (8,127 bytes)
  - `task_and_formulation.tex` (5,685 bytes)
  - `methodology.tex` (6,018 bytes)
  - `experimental_setup.tex` (5,836 bytes)
  - `results.tex` (9,346 bytes)
  - `discussion.tex` (7,224 bytes)
  - `limitations.tex` (4,761 bytes)
  - `conclusion.tex` (1,730 bytes)
- **Tables (`tables/` - 6 files):**
  - `dataset_distribution.tex`: Gold split counts ($N=163$ test, $N=103$ dev)
  - `transition_matrix.tex`: 3x3 label transition matrix between translated En and original Hi
  - `main_results.tex`: Benchmark accuracy, macro-F1, coverage, and latencies
  - `statistical_tests.tex`: McNemar and permutation test comparisons
  - `error_attribution.tex`: Diagnostic error partition
  - `case_studies.tex`: Qualitative example pairs
- **Figures (`figures/` - 10 files):**
  - `figures/pdf/`: 5 vector PDF figures (`fig1_study_workflow.pdf`, `fig2_risk_coverage_tradeoff.pdf`, `fig3_condition_comparison.pdf`, `fig4_error_attribution_breakdown.pdf`, `fig5_transition_heatmap.pdf`)
  - `figures/src/`: 5 matching high-resolution PNG renders

All 40 original files have been hashed into `original_manuscript_hashes.json` to guarantee zero drift.

---

## 3. Current LaTeX Template and Configuration

- **Document Class:** `\documentclass[11pt,a4paper]{article}`
- **Package:** `\usepackage[hyperref,submission]{tacl2021v1}`
  - Note: In TACL submissions, the `submission` option enforces anonymous review, obscuring the author block. For internal archiving and camera-ready preparation, `acceptedWithA` can be passed to render author affiliations.
- **Font & Formatting Standards:**
  - `times`, `latexsym`, `amsmath`, `amssymb`, `graphicx`, `booktabs`, `multirow`, `microtype`, `url`, `xcolor`, `array`.
  - Margin parameters defined in `tacl2021v1.sty`: standard two-column ACL layout (8.5in x 11in or A4; 2.5cm margins, 10pt/11pt fonts).

---

## 4. Current Figures and Tables

1. **Table 1 (`dataset_distribution.tex`):** X-Fact Hindi subset details. Test set ($N=163$) contains 142 `CONTRADICTED`, 21 `INSUFFICIENT_EVIDENCE`, 0 `SUPPORTED`. Dev set ($N=103$) contains 89 `CONTRADICTED`, 14 `INSUFFICIENT_EVIDENCE`, 0 `SUPPORTED`.
2. **Table 2 (`transition_matrix.tex`):** Full 3x3 prediction transitions between Translated English and Original Hindi conditions.
3. **Table 3 (`main_results.tex`):** 4 evaluation conditions + 4 ablations/controls.
4. **Table 4 (`statistical_tests.tex`):** Exact McNemar paired test statistics, 2-class/3-class permutation test p-values, and FDR Benjamini-Hochberg adjusted values.
5. **Table 5 (`error_attribution.tex`):** Diagnostic error categorization.
6. **Table 6 (`case_studies.tex`):** Concrete claim-evidence instances showing translation-induced prediction divergence.
7. **Figures 1-5:** High-resolution vector diagrams illustrating workflow, risk-coverage trade-off, condition benchmark comparisons, error attribution, and the transition heatmap.

---

## 5. Bibliography and Citation Setup

- **BibTeX File:** `references.bib` containing 24 entries.
- **Style File:** `acl_natbib.bst`.
- **Key References Included:**
  - Thorne et al. (2018) FEVER
  - Gupta and Srikumar (2021) X-Fact
  - He et al. (2021) DeBERTa
  - Conneau et al. (2020) XLM-R
  - Tiedemann and Thottingal (2020) OPUS-MT
  - Lewis et al. (2020) RAG
  - Asai et al. (2021) XOR-QA
  - Kassner et al. (2021) Multilingual QA
  - Wang et al. (2023) Cross-lingual Consistency
  - Benjamini and Hochberg (1995) FDR
  - McNemar (1947) Paired Test
- **Citation Command Style:** Consistent use of `\citet` and `\citep` via `natbib`.

---

## 6. Existing Build Procedure

- Standard 4-pass compilation: `pdflatex` -> `bibtex` -> `pdflatex` -> `pdflatex`.
- Build directory separation (`-output-directory=build`) is recommended to avoid cluttering root source.
- Local execution environment audit: Local Windows environment does not currently have `pdflatex` or `latexmk` on system PATH. A complete cloud/Docker build specification and Overleaf import structure will be documented.

---

## 7. Formatting Defects Identified in Initial Pass

1. Section references in `main.tex` previously pointed directly to `sections/` and `supplementary_material.tex` in root, requiring modular containment.
2. In `figures/`, LaTeX files must reference `figures/final/` to ensure vector PDF files are picked up cleanly.
3. Float placement parameters and table widths in two-column mode: `table*` vs `table` requires strict bounding to prevent overfull hbox warnings in ACL 2-column mode.

---

## 8. Writing and Organization Assessment

1. **Precision in Terminology:** Distinguish clearly between *prediction disagreement* (sensitivity under translation) and *factual verifier error*. Translation shift induces sensitivity, but without manual gold translation alignment, disagreement does not imply translation error caused inaccuracy.
2. **Class Imbalance Framing:** The test set lacks gold `SUPPORTED` claims (142 CON, 21 NEU, 0 SUP). Raw accuracy must be framed cautiously, and 3-class macro-F1 reflects a degenerate third class. 2-class observed F1 must be reported alongside 3-class F1.
3. **Exploratory Status:** The test set was previously inspected during initial pilot runs. The study must be explicitly framed as an *exploratory computational investigation*, not a blind confirmatory trial.
4. **Pre-Retrieved Evidence:** The verifier evaluates claims against pre-retrieved evidence passages from X-Fact. It does not evaluate end-to-end multi-hop web retrieval.

---

## 9. Potential Scientific or Numerical Inconsistencies (Audited & Clarified)

- **Prior McNemar Confusion:** In older draft notes, $b=27, c=51$ was mistakenly conflated with $\chi^2=7.5571$.
  - Canonical resolution verified:
    - No-Check vs Direct Multilingual: $b=27, c=51 \implies \chi^2 = (|27-51|-1)^2 / (27+51) = 23^2 / 78 = 529 / 78 = 6.7821, p=0.008772$.
    - Selective-Check vs Direct Multilingual: $b=23, c=47 \implies \chi^2 = (|23-47|-1)^2 / (23+47) = 23^2 / 70 = 529 / 70 = 7.55714 = 7.5571, p=0.005583$.
- **Permutation Tests:** Macro-F1 permutation tests ($B=5,000$) demonstrate $p=0.1898$ (No-Check vs Direct Multi) and $p=0.1180$ (Selective vs Direct Multi), which are not statistically significant at $\alpha=0.05$. This must be honestly emphasized: the accuracy difference is statistically significant under McNemar, but macro-F1 is non-significant due to extreme class skew.

---

## 10. Missing Dependencies or Files

- All LaTeX section files, tables, and figures exist in the repository.
- Style files `tacl2021v1.sty` and `acl_natbib.bst` are present and valid.

---

## 11. Official TACL Requirements That Apply

- **Page Limit:** TACL allows up to 10 pages for the main text in submission/review format, with unlimited pages for references and appendices.
- **Double-Blind Review:** Submissions must omit author names and self-identifying citations (`\usepackage[hyperref,submission]{tacl2021v1}`).
- **Two-Column Layout:** A4/US Letter standard formatting, 11pt body font.
- **Ethical Considerations & Limitations:** Mandatory dedicated sections discussing data biases, language limitations, and ethical scope.

---

## 12. Prioritized Revision Plan

1. **Phase 2:** Establish and isolate `manuscript_revision_tacl/` workspace. (Done)
2. **Phase 3:** Construct `CLAIM_EVIDENCE_MATRIX.csv`, `MANUSCRIPT_DISCREPANCY_LOG.md`, and `MANUSCRIPT_FACT_CHECK.md`.
3. **Phase 4:** Thoroughly revise all manuscript section files for tone, scientific rigor, balanced claims, and limitation transparency.
4. **Phase 5 & 6:** Verify TACL formatting compliance, polish tables with booktabs, ensure figure paths and captions are aligned.
5. **Phase 7:** Audit bibliography (`references.bib`) and generate `CITATION_AUDIT.md`.
6. **Phase 8-10:** Package workspace, run regression validation script, and generate `BUILD_AUDIT.md`.
7. **Phase 11-12:** Produce `FINAL_MANUSCRIPT_CHANGELOG.md` and `FINAL_HANDOFF_REPORT.md`.
