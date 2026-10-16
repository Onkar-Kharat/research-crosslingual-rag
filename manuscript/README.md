# Manuscript Compilation & Review Package

**Manuscript Title:** *Separating Translation-Fidelity and Verifier-Reasoning Errors in Cross-Lingual RAG: A Controlled Study with Selective Original-Evidence Checking*  
**Target Journal:** Transactions of the Association for Computational Linguistics (TACL)  
**Submission Format:** Double-blind review format (anonymous author block, line numbered)  

---

## 1. Review Candidate PDF

- **Primary Submission PDF:** [`main.pdf`](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript/main.pdf)
- **Page Count:** 9 pages total
  - Pages 1--7: Main text, figures, and tables (compliant with TACL 10-page maximum content ceiling).
  - Page 8: References (unlimited length under TACL guidelines).
  - Page 9: Appendix A (Reproducibility details, hyperparameters, and compute profile; compliant with TACL Category 1 appendix policy effective March 1, 2024).
- **Anonymization:** 100% anonymized. The author block is empty; no institutional names, acknowledgments, or self-identifying grant links appear in the document.

---

## 2. Prerequisites & Software Requirements

Compilation requires a standard TeX distribution equipped with `pdflatex` and `bibtex`. The document has been tested and verified under:
- **TeX Engine:** pdfTeX 3.141592653-2.6-1.40.29 (MiKTeX 26.5 / TeX Live 2024+)
- **BibTeX Engine:** BibTeX 0.99d (MiKTeX 26.5)
- **Standard LaTeX Packages:** `times`, `latexsym`, `url`, `fontenc` (T1), `booktabs`, `tabularx`, `amsmath`, `amssymb`, `graphicx`.

---

## 3. Official TACL Template Assets

The manuscript uses the official TACL 2021 template files:
- `tacl2021v1.sty` — Official TACL style macro (submission format with review line numbers enabled).
- `acl_natbib.bst` — Official ACL/TACL Natbib bibliography style file.
- `references.bib` — Verified bibliography entries with complete DOIs and ACL Anthology identifiers.

---

## 4. Compilation Instructions

From the `manuscript/` directory, execute:

```powershell
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

This 4-step sequence resolves all cross-references, compiles the `.bbl` bibliography, and generates the final publication PDF (`main.pdf`) with 0 errors and 0 undefined references.

---

## 5. File Manifest

| File Name | Purpose |
|:---|:---|
| `main.tex` | Master LaTeX source document |
| `references.bib` | BibTeX bibliography containing 11 verified references |
| `tacl2021v1.sty` | Official TACL style file |
| `acl_natbib.bst` | Official Natbib citation styling |
| `main.pdf` | Ready-to-submit compiled publication PDF |
| `tables/main_results.tex` | Table 1: Primary 4-condition evaluation metrics |
| `tables/statistical_tests.tex` | Table 2: Paired McNemar and permutation test results |
| `tables/error_attribution.tex` | Table 3: Systematic causal error attribution breakdown |
| `tables/case_studies.tex` | Table 4: Qualitative case studies demonstrating error categories |
| `figures/pdf/fig1_study_workflow.pdf` | Figure 1: System architecture and evaluation pipeline |
| `figures/pdf/fig2_risk_coverage_tradeoff.pdf` | Figure 2: Operating curve and dev threshold tuning ($\tau^*=0.300$) |
| `figures/pdf/fig3_condition_comparison.pdf` | Figure 3: Held-out test performance across conditions |
| `figures/pdf/fig4_error_attribution_breakdown.pdf` | Figure 4: Diagnostic decomposition of verification failures |
