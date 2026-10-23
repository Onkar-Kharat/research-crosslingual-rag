# Manuscript Build and Compilation Instructions

**Working Title:** Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Style Package:** `tacl2021v1.sty` with `acl_natbib.bst`  
**LaTeX Document Class:** `\documentclass[11pt,a4paper]{article}`  

---

## 1. Local Tooling Status

- **Host Compiler Check:** A local TeX distribution (`pdflatex`, `xelatex`, or `latexmk`) is currently not installed or not present on the Windows system PATH.
- **Verification Rule:** Under Phase 7 research-integrity rules, we **do not claim** that a local PDF build passed when the binary is absent.
- **Source Validation Status:** The LaTeX source files, tables, figures, bibliography (`references.bib`), and style files (`tacl2021v1.sty`, `acl_natbib.bst`) have been verified for syntax, matching environments, valid BibTeX keys, and complete cross-references.

---

## 2. Compilation Instructions

### Option A: Local Build (Linux / macOS / Windows with TeX Live or MiKTeX)

To compile the manuscript locally from either `docs/manuscript/` or `manuscript/`:

```bash
# Navigate to the manuscript source directory
cd docs/manuscript

# Compile using standard pdflatex + bibtex pipeline:
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Or using latexmk (recommended):
latexmk -pdf main.tex
```

Clean auxiliary build artifacts:
```bash
latexmk -c
# Or on Windows PowerShell:
Remove-Item *.aux, *.bbl, *.blg, *.log, *.out -ErrorAction SilentlyContinue
```

---

### Option B: Compiling on Overleaf / Cloud LaTeX

1. Zip the contents of `docs/manuscript/` (including `sections/`, `tables/`, `figures/`, `main.tex`, `references.bib`, `tacl2021v1.sty`, and `acl_natbib.bst`).
2. Log into [Overleaf](https://www.overleaf.com/) and create a new project by selecting **Upload Project**.
3. Set the compiler to **pdfLaTeX** and TeX Live version to **2023 or 2024**.
4. Set main document to `main.tex`.
5. Click **Recompile**.

---

### Option C: Compiling via Docker

If Docker is available:

```bash
docker run --rm -v "${PWD}/docs/manuscript:/work" -w /work texlive/texlive:latest latexmk -pdf main.tex
```

---

## 3. Directory Layout for Compilation

The manuscript structure is fully self-contained:

```text
docs/manuscript/
├── main.tex                    # Master LaTeX orchestration file
├── references.bib              # Verified, audited BibTeX file
├── tacl2021v1.sty              # Official TACL style file
├── acl_natbib.bst              # Official ACL natbib bibliography style
├── sections/                   # Modular text sections
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
├── tables/                     # Exact numerical tables generated from canonical data
│   ├── dataset_distribution.tex
│   ├── transition_matrix.tex
│   ├── main_results.tex
│   ├── statistical_tests.tex
│   ├── error_attribution.tex
│   └── case_studies.tex
├── figures/                    # Publication-quality vector PDF and PNG figures
│   ├── fig1_method_diagram.pdf
│   ├── fig2_accuracy_ci.pdf
│   ├── fig3_error_distribution.pdf
│   ├── fig4_system_comparison.pdf
│   └── fig5_transition_heatmap.pdf
└── supplementary_material.tex  # Appendices, hardware, tuning sweep, protocol
```
