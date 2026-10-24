# Manuscript Validation and Audit Report

**Working Title:** Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Research Status:** `FROZEN — EXPLORATORY COMPUTATIONAL STUDY`  
**Overall Validation Verdict:** `INTERNAL REVIEW READY` (Full First Draft Complete, All 47 Regression Tests Passing, 100% Numerical Fact-Check Passed)

---

## 1. Comprehensive Validation Checklist

| Item # | Validation Check | Status | Verification Evidence / Details |
|:---:|:---|:---:|:---|
| 1 | All 10 core manuscript sections present | **PASS** | `abstract.tex`, `introduction.tex`, `related_work.tex`, `task_and_formulation.tex`, `methodology.tex`, `experimental_setup.tex`, `results.tex`, `discussion.tex`, `limitations.tex`, `conclusion.tex`, `supplementary_material.tex` verified. |
| 2 | All numerical claims trace to canonical records | **PASS** | All 37 quantitative entries in `docs/manuscript/MANUSCRIPT_FACT_CHECK.md` match `results/canonical/` bit-for-bit. |
| 3 | Every table matches source data | **PASS** | Tables 1--6 generated directly from canonical CSVs and JSON summaries; zero discrepancies. |
| 4 | Every figure regenerated from declared source | **PASS** | `fig1` through `fig5` generated via `scripts/generate_publication_figures.py`; PDF and PNG outputs available. |
| 5 | All citations resolve in `references.bib` | **PASS** | 15/15 citations verified against ACL Anthology, NeurIPS, and official DOIs; zero unresolved `\cite` keys. |
| 6 | No bibliography entry is fabricated | **PASS** | Audited in `docs/manuscript/CITATION_AUDIT.md`; all authors, titles, years, and URLs verified. |
| 7 | No unresolved placeholders disguised as complete | **PASS** | Human annotation explicitly labeled **PENDING**; test split explicitly labeled **PREVIOUSLY INSPECTED / EXPLORATORY**. |
| 8 | No accidental changes to frozen results | **PASS** | `experiments/results_canonical/` and `results/canonical/` checksums intact; frozen release archive SHA-256 unchanged. |
| 9 | Full existing test suite passes | **PASS** | `python tests/run_all_tests.py` passes 47/47 tests (0 failures, exit code 0). |
| 10 | Existing result files retain checksums | **PASS** | Canonical test predictions SHA-256 matches frozen baseline inventory. |
| 11 | Tables and figures regenerate without model inference | **PASS** | Figure and table scripts operate purely on precomputed canonical CSVs/JSONs in $< 2$ seconds. |
| 12 | LaTeX source syntax validation | **PASS** | Validated matching environments, valid package options (`tacl2021v1.sty`), and verified BibTeX syntax. |
| 13 | Local compiler availability check | **DOCUMENTED** | Local system lacks `pdflatex` binary on PATH; documented in `build_instructions.md` with Overleaf/Docker instructions. |
| 14 | Cross-section narrative consistency | **PASS** | Title, abstract, introduction, results, discussion, and conclusion maintain identical scope, counts, and interpretations. |
| 15 | Limitations prominence | **PASS** | Section 9 contains 10 explicit numbered paragraphs; not hidden in internal documentation. |
| 16 | TACL-specific formatting compliance | **PASS** | Follows TACL 2021v1 formatting guidelines, double-blind author placeholder, and required structure. |
| 17 | Honest readiness designation | **PASS** | Designated as `INTERNAL REVIEW READY`, strictly distinguishing draft completeness from external submission readiness. |

---

## 2. Blockers and Outstanding Items for Future Submission

1. **Host LaTeX Tooling:** Compiling the final camera-ready PDF requires executing `pdflatex` / `latexmk` on an environment with TeX Live or uploading to Overleaf (see `build_instructions.md`).
2. **Author and Affiliation Metadata:** Double-blind placeholders must be replaced with final verified author names, institutional affiliations, and ORCIDs only after formal author approval.
3. **Pending Bilingual Human Annotation:** Prior to making causal claims about translation errors or submitting to venues requiring human gold validation, the planned annotation protocol (`docs/manuscript/supplementary_material.tex`) must be executed.
4. **License Selection:** Final repository license (e.g., MIT / CC-BY-4.0) must be confirmed with primary authors and upstream X-Fact redistribution guidelines.
