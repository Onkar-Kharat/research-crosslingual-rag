# TACL Submission Formatting and Anonymity Audit Report

**Workspace:** `manuscript_revision_tacl/`  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Audit Standard:** Official TACL Submission Instructions & Author Formatting Guidelines  
**Audit Date:** 2026-10-24  
**Evaluator:** LaTeX & Publication-Formatting Specialist  

---

## 1. Official TACL Specification Verification

| Guideline Requirement | TACL Specification | Submission State | Status |
| :--- | :--- | :--- | :---: |
| **Document Class & Style** | `\documentclass[11pt,a4paper]{article}` with `tacl2021v1.sty` | Fully matched in `main.tex` and `submission.tex` | **PASS** |
| **Review Version Anonymity** | Author names, institutions, and affiliations omitted; "Anonymous TACL Submission" | `submission.tex` uses `\author{Anonymous TACL Submission}` | **PASS** |
| **Line Numbering** | Continuous margin line numbers required for review version | `tacl2021v1.sty` option `[submission]` renders gray margin line numbers | **PASS** |
| **Author Preview Version** | Camera-ready style with visible author names and clean margins | `main.tex` uses `[acceptedWithA]` displaying Onkar Kharat & Himanshu Jadhav | **PASS** |
| **Repository URL Policy** | Identifying URLs prohibited in review version | Excluded from `submission.tex`; present only in author copy `main.tex` | **PASS** |
| **PDF Metadata Anonymity** | Binary metadata and Creator fields must not leak author names | Binary search confirms zero occurrences of author names in `submission.pdf` | **PASS** |
| **Page Layout & Margins** | A4 paper, two-column layout (3.125 in / 77 mm per column, 0.25 in / 6.5 mm gutter) | Enforced by `tacl2021v1.sty` | **PASS** |
| **Font Specifications** | 11pt Times Roman with microtype character protrusion | Enforced via `times` and `microtype` packages | **PASS** |
| **Table Spanning** | Wide multi-column tables must use `table*` environment | All wide tables (`dataset_distribution`, `transition_matrix`, `error_attribution`, `case_studies`) span both columns cleanly | **PASS** |
| **Bibliography Format** | Citations formatted via `\usepackage{acl_natbib}` and `acl_natbib.bst` | All 16 citations compiled with Natbib and valid DOIs/URLs | **PASS** |
| **Figure Formatting** | Standalone vector PDF figures with readable fonts ($\ge 8$pt) | All 5 figures in `figures/final/` are vector PDFs with 0 text overlap | **PASS** |

---

## 2. Build and Page Allocation Audit

- **Author Preview Build (`main.pdf`):**
  - **Total Pages:** 20 pages
  - **Main Text (Sections 1–9):** 15 pages (includes Section 1 Introduction, Section 2 Related Work, Section 3 Task Formulation, Section 4 Methodology, Section 5 Experimental Setup, Section 6 Results, Section 7 Discussion, Section 8 Limitations, Section 9 Conclusion)
  - **References:** Pages 16–17 (16 verified bibliographic entries)
  - **Supplementary Material (Appendix A):** Pages 18–20 (Tables 8, 9, 10, and Human Annotation Protocol)
- **Review Version Build (`submission.pdf`):**
  - **Total Pages:** 19 pages
  - **Main Text:** 15 pages with continuous margin line numbers for reviewer feedback.
  - **References:** Pages 15–16.
  - **Supplementary Material:** Pages 17–19.

---

## 3. Anonymity and De-Identification Checklist

- [x] Author names removed from review document: Verified in `submission.tex`.
- [x] Institutional affiliations removed: Verified.
- [x] Project and funding acknowledgements removed from review version: Verified (moved to `main.tex` only).
- [x] Author contributions statement removed from review version: Verified.
- [x] GitHub repository link removed from review version: Verified.
- [x] Third-person phrasing used for prior institutional work: Verified.
- [x] PDF document metadata stripped of identifying names: Verified via binary inspection of `submission.pdf`.
