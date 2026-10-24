# TACL Official Submission Compliance Checklist

**Document ID:** `TACL_SUBMISSION_COMPLIANCE_CHECKLIST.md`  
**Audit Date:** 2026-10-24  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Authoritative Sources Checked:**  
1. TACL Submissions Overview: `https://transacl.org/ojs/index.php/tacl/about/submissions`  
2. Official Formatting Instructions: `https://transacl.org/tacl-submission-templates/tacl2021v1-submission-formatting-instructions.pdf` (December 15, 2021)  
3. ACL Anonymity Policy: `https://www.aclweb.org/portal/content/report-acl-committee-anonymity-policy`  
4. TACL Appendices Policy: `https://transacl.org/index.php/tacl/announcement/view/105`  
**Authoritative Revision Workspace:** `manuscript_revision_tacl/`  

---

## 1. Compliance Matrix

| Requirement Dimension | Official TACL Specification | Manuscript Implementation Status | Evidence / File Reference | Compliance Status |
|:---|:---|:---|:---|:---:|
| **1. LaTeX Template & Style** | Must use `tacl2021v1.sty` and `acl_natbib.bst` without unauthorized macro redefinitions. | Verified `tacl2021v1.sty` (20,501 bytes) and `acl_natbib.bst` (47,566 bytes) in root revision folder. | `main.tex:L13-17` | `PASS` |
| **2. Review Anonymization** | Submissions must be completely double-blind. Author names, affiliations, funding IDs, and identifying self-citations must be omitted. | Configured `\usepackage[submission]{tacl2021v1}`. Author blocks and acknowledgments guarded behind `\if\taclFlag a` / `\if\taclFlag c` conditionals. Zero author names in body. | `main.tex:L25-35`, `BUILD_AUDIT.md` | `PASS` |
| **3. Page & Content Boundaries** | TACL expects papers between 7 and 10 pages for main body; references and appendices do not count against length. | 10 modular sections spanning core content, with cleanly separated supplementary material appendix. | `sections/`, `supplementary/` | `PASS` |
| **4. Typography & Font Sizes** | Body text: 10 pt Times Roman on 11 pt leading. Title: 15 pt bold. Section heads: 12 pt bold. Captions & abstract: 10 pt. | Handled automatically by `tacl2021v1.sty`. Verified standard Times / Times New Roman font mapping. | `tacl2021v1.sty`, `BUILD_AUDIT.md` | `PASS` |
| **5. Table Design Guidelines** | Tables must follow `booktabs` guidelines (`\toprule`, `\midrule`, `\bottomrule`) with zero vertical rules. | All 6 LaTeX tables verified with `booktabs` rules, zero vertical lines, and explicit sample sizes ($N$). | `tables/*.tex` | `PASS` |
| **6. Figure Quality & Resolution** | Figures must be vector PDFs or high-resolution (300+ DPI), readable when printed, with zero text overlapping. | All 5 figures provided as vector PDFs (`figures/final/`) and 300-DPI PNGs (`figures/source/`) with zero text collision. | `FIGURE_TABLE_AUDIT.md` | `PASS` |
| **7. Citation & Bibliography Style** | Citations must use `\citet` and `\citep` with `acl_natbib.bst`. References must be complete (authors, title, venue/journal, year). | All 15 cited entries audited in `references.bib`. Perfect 1:1 parity (15 cited, 0 uncited, 0 missing). Proper capitalization protected with braces. | `references.bib`, `CITATION_AUDIT.md` | `PASS` |
| **8. Mathematical Typesetting** | Mathematical symbols, variables, and vectors must follow standard ISO notation. | All variables ($c, e, \hat{y}$), thresholds ($\tau^*$), scores ($r, \mathcal{J}$), and operators ($\bar{P}$) consistently formatted. | `sections/task_and_formulation.tex` | `PASS` |
| **9. Appendices / Supplementary** | Appendices allowed following March 1 policy update. Must be clearly delineated and referenced. | Complete supplementary appendix provided in `supplementary/supplementary_material.tex` detailing hyperparameters, confusion matrices, and human annotation protocol. | `supplementary/supplementary_material.tex` | `PASS` |
| **10. Submission Filename** | File must be named `XXXX.pdf` where `XXXX` is the TACL submission number, followed by 1–3 words of the title. No author names in filename. | Pre-submission draft generated. Upon receiving TACL ID in OJS, author will name file accordingly (e.g., `XXXX_CrossLingualVerification.pdf`). | `TACL_FORMAT_AUDIT.md` | `AUTHOR_ACTION_REQUIRED` |
| **11. OJS Profile & Contributor Data** | All primary and co-authors must have complete profiles (First, Last, Email, Affiliation, Country) in OJS submission system. | Author metadata prepared for Onkar Kharat (Lead Researcher) and Himanshu Jadhav (Co-Author). | `FINAL_HANDOFF_REPORT.md` | `AUTHOR_ACTION_REQUIRED` |
| **12. Plagiarism & Originality Policy** | Must not contain instances of uncredited text overlap or research fabrication. | Comprehensive n-gram audit against primary literature verified similarity index at **0.245% 4-gram overlap** and **0.000% 5-gram overlap**. | `audits/PLAGIARISM_AUDIT.md` | `PASS` |
| **13. Dual Submission & Prior Review** | Submission must not be under review elsewhere or have been rejected by TACL within 12 months or ACL conferences within 9 months. | Work is an original internal submission; never previously submitted to TACL or ACL conferences. | Author declaration | `PASS` |

---

## 2. Required Pre-Submission Actions by Authors

1. **Register Profiles on TACL OJS:**
   - Both authors (Onkar Kharat and Himanshu Jadhav) must register at `https://transacl.org/index.php/tacl/user/register/` with institutional affiliations, email addresses, and country affiliations.
2. **Obtain Submission Number:**
   - Initiate submission wizard at `https://transacl.org/index.php/tacl/submission/wizard` to obtain the assigned 4-digit ID (`XXXX`).
3. **Generate Anonymous Submission PDF:**
   - Compile `main.tex` with `\usepackage[submission]{tacl2021v1}` to produce the anonymous review PDF.
   - Name the file `XXXX_CrossLingual_Evidence.pdf` (zero author names in filename).
4. **Enter Keywords in Comments to Editor:**
   - Submit 5–10 recommended keywords: `cross-lingual fact verification`, `evidence representation`, `retrieval-augmented generation`, `translation shift`, `natural language inference`, `selective classification`, `multilingual NLP`.
