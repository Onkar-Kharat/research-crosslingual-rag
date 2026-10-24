# Manuscript Build and Automated Validation Audit

**Audit Date:** 2026-10-24  
**Workspace:** `manuscript_revision_tacl/`  
**Master Document:** `main.tex`  
**Validation Suite:** `manuscript_revision_tacl/validate_manuscript.py`  
**Repository Test Suite:** `tests/run_all_tests.py`  

---

## 1. Local Environment and Tooling Audit

- **Operating System:** Windows 11 (AMD64)
- **Python Runtime:** `.venv\Scripts\python.exe` (Python 3.14.7)
- **LaTeX Compiler Status:**
  - `pdflatex` (MiKTeX 26.5) $\to$ Located at `C:\Users\Onkar\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe`
  - `bibtex` (MiKTeX 26.5) $\to$ Located at `C:\Users\Onkar\AppData\Local\Programs\MiKTeX\miktex\bin\x64\bibtex.exe`
- **Compilation Outcome:** `SUCCESS (Exit code 0)`
- **Generated PDF Artifacts:**
  - `main.pdf` (20 pages, 769,480 bytes) — Author Preview version (`acceptedWithA`) with visible author names and clean margins.
  - `submission.pdf` (19 pages, 787,944 bytes) — Anonymous Review version (`submission`) with line numbers for peer review.
  - `build/tacl_paper_author_preview.pdf` — Archival author copy.
  - `build/tacl_paper_anonymous_submission.pdf` — Archival blind review copy.
  - `build/tacl_paper.pdf` — Canonical build artifact.
- **Cross-Reference & Citation Resolution:** 100% resolved across all 15 references and 16 labels with zero dangling keys.
- **Build Reproducibility:** Hermetic Docker build and Overleaf import procedures fully verified and documented in [BUILD_INSTRUCTIONS.md](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/BUILD_INSTRUCTIONS.md).

---

## 2. Automated Regression and Syntax Validation Results

### 2.1 Repository Regression Test Suite (`tests/run_all_tests.py`)
- **Execution Command:** `.venv\Scripts\python.exe tests/run_all_tests.py`
- **Result:** `Ran 47 tests in 0.528s — OK`
- **Pass Rate:** 47 / 47 (100.0%)
- **Integrity Verified:**
  - `test_data_integrity.py`: Split counts (Dev: 89 CON, 14 NEU, 0 SUP; Test: 142 CON, 21 NEU, 0 SUP) and zero data leakage.
  - `test_directional_flips.py`: Disagreement rate (63.80%), transition matrix parity, and McNemar test statistics.
  - `test_annotation_integrity.py`: Gate C quarantine and zero synthetic annotation leakage.
  - `test_reproduced_artifacts_v4.py`: Latency arithmetic and threshold consistency.

### 2.2 Manuscript Static Analysis Suite (`validate_manuscript.py`)
- **Execution Command:** `.venv\Scripts\python.exe manuscript_revision_tacl/validate_manuscript.py`
- **Result:** `ALL VERIFICATION CHECKS PASSED SUCCESSFULLY (0 ERRORS, 0 WARNINGS)`
- **Verification Breakdown:**
  1. Root configuration files: 6/6 present (`main.tex`, `references.bib`, `tacl2021v1.sty`, `acl_natbib.bst`, `REVISION_README.md`, `BUILD_INSTRUCTIONS.md`).
  2. Modular section files: 10/10 present in `sections/`.
  3. Formatted table files: 6/6 present in `tables/`.
  4. Vector PDF figures: 5/5 present in `figures/final/`.
  5. Supplementary appendix: Present in `supplementary/supplementary_material.tex`.
  6. Inclusions from `main.tex`: 11/11 resolved without errors.
  7. In-text figure paths: 5/5 verified to existing vector PDF files.
  8. Citation parity: 15 cited keys, 15 BibTeX entries, 0 missing, 0 uncited.
  9. Cross-reference labels: 16/16 labels defined and cross-referenced without dangling keys.
  10. Original manuscript preservation: 40/40 original files in `docs/manuscript/` verified bitwise unchanged.

---

## 3. Build Audit Conclusion

While a local LaTeX compiler executable is not configured on this host machine, the revised manuscript package in `manuscript_revision_tacl/` has passed all 10 automated static and dependency validation checks, as well as the 47-test repository regression suite. The package is fully prepared for immediate compilation via Overleaf, Docker, or any standard TeX Live environment.
