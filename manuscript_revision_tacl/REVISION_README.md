# Manuscript Revision Workspace — TACL Submission Preparation

## 1. Overview and Workspace Separation

This workspace (`manuscript_revision_tacl/`) is the **authoritative directory for all revised manuscript drafts, publication-quality tables, figure assets, and editorial audits** targeted for the *Transactions of the Association for Computational Linguistics (TACL)*.

- **Authoritative Revised Manuscript Workspace:** `manuscript_revision_tacl/`
- **Original Manuscript Baseline (Frozen & Preserved):** `docs/manuscript/`
  - The original manuscript files in `docs/manuscript/` are completely preserved and unmodified, with recorded SHA-256 hashes monitored by regression tests.
- **Author Information:**
  - **Lead Researcher & Primary Author:** Onkar Kharat
  - **Co-Author & Research Contributor:** Himanshu Jadhav

---

## 2. Directory Layout

```text
manuscript_revision_tacl/
├── REVISION_README.md              # This guide and directory authority declaration
├── main.tex                       # Master LaTeX entry point (TACL 2021v1 style)
├── tacl2021v1.sty                 # Official TACL style package
├── acl_natbib.bst                 # Official ACL/TACL BibTeX style
├── references.bib                 # Verified bibliography database
├── sections/                      # Modular LaTeX manuscript sections
│   ├── abstract.tex
│   ├── introduction.tex
│   ├── related_work.tex
│   ├── task_and_formulation.tex
│   ├── methodology.tex
│   ├── experimental_setup.tex
│   ├── results.tex
│   ├── discussion.tex
│   ├── limitations.tex
│   └── conclusion.tex
├── figures/                       # Publication figure assets
│   ├── final/                     # Production vector PDFs for LaTeX inclusion
│   │   ├── fig1_study_workflow.pdf
│   │   ├── fig2_risk_coverage_tradeoff.pdf
│   │   ├── fig3_condition_comparison.pdf
│   │   ├── fig4_error_attribution_breakdown.pdf
│   │   └── fig5_transition_heatmap.pdf
│   └── source/                    # High-resolution PNGs and plotting scripts
├── tables/                        # Formatted LaTeX table environments
│   ├── dataset_distribution.tex   # Split counts and gold label breakdown
│   ├── transition_matrix.tex      # 3x3 label transition matrix
│   ├── main_results.tex           # 4-condition benchmark and ablations
│   ├── statistical_tests.tex      # McNemar and permutation test statistics
│   ├── error_attribution.tex      # Diagnostic error partition
│   └── case_studies.tex           # Concrete cross-lingual prediction shift examples
├── supplementary/                 # Supplementary materials and appendix
│   └── supplementary_material.tex
├── build/                         # Build artifacts directory (keeps source clean)
├── audits/                        # Verification, fact-checking, and audit artifacts
│   ├── MANUSCRIPT_INITIAL_AUDIT.md
│   ├── CLAIM_EVIDENCE_MATRIX.csv
│   ├── MANUSCRIPT_DISCREPANCY_LOG.md
│   ├── MANUSCRIPT_FACT_CHECK.md
│   ├── CITATION_AUDIT.md
│   ├── TACL_FORMAT_AUDIT.md
│   ├── FIGURE_TABLE_AUDIT.md
│   └── BUILD_AUDIT.md
├── BUILD_INSTRUCTIONS.md           # Reproducible PDF compilation guide
├── FINAL_MANUSCRIPT_CHANGELOG.md  # Detailed log of editorial and formatting changes
└── FINAL_HANDOFF_REPORT.md        # Comprehensive handoff report with 9 status dimensions
```

---

## 3. Supporting Frozen Research Artifacts

All numerical claims, percentages, test statistics, and confidence intervals in this manuscript are grounded directly in the frozen research artifacts:

1. `canonical_results.csv`: Master registry of canonical experimental values.
2. `experiments/results_canonical/canonical_test_predictions.csv`: Instance-level test predictions ($N=163$).
3. `experiments/results_canonical/canonical_dev_predictions.csv`: Instance-level dev predictions ($N=103$).
4. `experiments/results_canonical/canonical_benchmark_table.csv`: Condition comparisons and ablations.
5. `results/canonical/test_metrics.json`: Hierarchical JSON serialization of all canonical metrics.
6. `results/statistical_tests/canonical_statistical_tests.csv`: Exact McNemar and permutation test records.

---

## 4. Compilation Instructions

The manuscript uses standard LaTeX tools with `tacl2021v1.sty` and `acl_natbib.bst`.

```bash
cd manuscript_revision_tacl
pdflatex -output-directory=build main.tex
bibtex build/main
pdflatex -output-directory=build main.tex
pdflatex -output-directory=build main.tex
```

For detailed platform-specific commands (including Overleaf and Docker setups), refer to [BUILD_INSTRUCTIONS.md](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/BUILD_INSTRUCTIONS.md).

---

## 5. Unresolved Author Decisions

The manuscript is fully prepared with all verified facts. The following routine toggles are ready for author decision prior to final submission:
1. **Submission vs. Camera-Ready Mode:** `\usepackage[hyperref,submission]{tacl2021v1}` is configured by default to enable double-blind peer review anonymization required by TACL. To render author affiliations (Onkar Kharat and Himanshu Jadhav) for internal archiving or camera-ready preparation, change to `\usepackage[hyperref,acceptedWithA]{tacl2021v1}`.
2. **Contact Email:** A placeholder email domain or direct institutional email address can be inserted into the author block when publishing camera-ready.
