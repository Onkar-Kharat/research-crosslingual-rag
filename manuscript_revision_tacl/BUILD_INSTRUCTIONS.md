# Reproducible PDF Build Instructions

**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Workspace:** `manuscript_revision_tacl/`  
**Master Document:** `main.tex`  
**Style Files:** `tacl2021v1.sty`, `acl_natbib.bst`, `references.bib`  

---

## 1. Local TeX Live Compilation (Standard 4-Pass)

Ensure a modern TeX Live distribution (2022 or newer) or MacTeX / MiKTeX is installed.

### Option A: Standard Manual Build Commands

Run the following commands from inside the `manuscript_revision_tacl/` directory:

```bash
# Navigate to the revision workspace
cd manuscript_revision_tacl

# Pass 1: Initial compilation to parse sections and generate aux files
pdflatex -output-directory=build main.tex

# Pass 2: Process bibliography and citation references
bibtex build/main

# Pass 3: Resolve cross-references and citation links
pdflatex -output-directory=build main.tex

# Pass 4: Finalize page numbers and hyperref cross-links
pdflatex -output-directory=build main.tex
```

The resulting publication PDF will be located at:
`manuscript_revision_tacl/build/main.pdf`

---

### Option B: Automated Build with `latexmk`

If `latexmk` is available:

```bash
cd manuscript_revision_tacl
latexmk -pdf -outdir=build main.tex
```

To perform a clean rebuild:
```bash
latexmk -C -outdir=build
latexmk -pdf -outdir=build main.tex
```

---

## 2. Compiling in Overleaf

To compile this manuscript on Overleaf:
1. Create a new blank project in Overleaf.
2. Upload the contents of `manuscript_revision_tacl/` (preserving folder hierarchy: `sections/`, `tables/`, `figures/`, `supplementary/`).
3. Set the root document to `main.tex`.
4. In Overleaf Project Settings, select **Compiler: pdfLaTeX** and **TeX Live version: 2023 or newer**.
5. Click **Recompile**.

---

## 3. Reproducible Containerized Build (Docker)

To compile the manuscript in a hermetic, zero-dependency Docker container:

```bash
docker run --rm -v "${PWD}/manuscript_revision_tacl:/workspace" -w /workspace texlive/texlive:latest \
  bash -c "mkdir -p build && pdflatex -output-directory=build main.tex && bibtex build/main && pdflatex -output-directory=build main.tex && pdflatex -output-directory=build main.tex"
```

The output PDF is saved directly to `manuscript_revision_tacl/build/main.pdf`.

---

## 4. Switching Review vs. Camera-Ready Mode

In `manuscript_revision_tacl/main.tex`:
- **For Anonymous Peer Review (Default):**
  ```latex
  \usepackage[hyperref,submission]{tacl2021v1}
  ```
  Masks the author block for double-blind review.
- **For Camera-Ready / Author-Attributed Archival Draft:**
  ```latex
  \usepackage[hyperref,acceptedWithA]{tacl2021v1}
  ```
  Renders the author block showing **Onkar Kharat** and **Himanshu Jadhav**.

---

## 5. Verification Checklist

- [x] All 10 section files present in `sections/`
- [x] All 6 table files present in `tables/`
- [x] All 5 vector PDF figures present in `figures/final/`
- [x] Style files `tacl2021v1.sty` and `acl_natbib.bst` present in workspace root
- [x] Bibliography file `references.bib` verified with 24 complete entries
- [x] Supplementary materials loaded cleanly via `supplementary/supplementary_material.tex`
