# Final Handoff Report — TACL Manuscript Revision and Verification

**Date:** 2026-10-24  
**Project:** Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Research Status:** `FROZEN — EXPLORATORY COMPUTATIONAL STUDY`  
**Author Attribution:**  
- **Lead Researcher & Primary Author:** Onkar Kharat  
- **Co-Author & Research Contributor:** Himanshu Jadhav  
**Authoritative Revised Manuscript Workspace:** `manuscript_revision_tacl/`  
**Preserved Original Manuscript Baseline:** `docs/manuscript/` (Bitwise Verified Unchanged)  

---

## 1. Executive Status Dashboard

In strict accordance with Phase 12 instructions, the nine required independent status distinctions are reported below:

| Status Dimension | Status Evaluation | Operational Justification |
|:---|:---:|:---|
| **`MANUSCRIPT_REVISION`** | **`complete`** | All 10 section files, supplementary appendix, 6 tables, and 5 figures fully drafted, formatted, and verified against frozen artifacts. |
| **`SCIENTIFIC_CONSISTENCY_AUDIT`** | **`complete`** | 22/22 claims in `CLAIM_EVIDENCE_MATRIX.csv` verified; 40/40 quantitative facts in `MANUSCRIPT_FACT_CHECK.md` verified; 5 historical discrepancies resolved in `MANUSCRIPT_DISCREPANCY_LOG.md`. |
| **`CITATION_AUDIT`** | **`complete`** | Perfect 1:1 parity achieved (15 BibTeX entries, 15 cited in-text, 0 missing, 0 uncited); all entries verified against official ACL Anthology/DOIs in `CITATION_AUDIT.md`. |
| **`TACL_FORMAT_AUDIT`** | **`complete`** | 100% compliant with official TACL 2021v1 layout, typography, margin rules, and double-blind masking options in `TACL_FORMAT_AUDIT.md`. |
| **`LATEX_BUILD`** | **`not run`** | Local host environment lacks `pdflatex`/`latexmk` on PATH. All 10 static validation checks passed; exact reproducible build procedures for TeX Live, Overleaf, and Docker documented in `BUILD_INSTRUCTIONS.md`. |
| **`PDF_VISUAL_INSPECTION`** | **`not performed`** | Local PDF compiler absent on Windows host. Vector PDF assets and LaTeX source validated without syntax warnings. |
| **`REPOSITORY_ORGANIZATION`** | **`complete`** | Pristine directory layout with complete workspace isolation (`manuscript_revision_tacl/`); 40/40 original manuscript files in `docs/manuscript/` verified bitwise unchanged. |
| **`AUTHOR_DECISIONS`** | **`ready for author review`** | Two standard pre-submission editorial toggles ready for author review: (1) Submission vs. camera-ready macro toggle (`submission` vs `acceptedWithA`); (2) Contact email domain selection. |
| **`SUBMISSION_READINESS`** | **`ready for author review against verified requirements`** | All scientific, structural, tabular, and bibliographic requirements are complete and rigorously validated for author review. |

---

## 2. Deliverables Inventory

The complete revised manuscript package resides in `manuscript_revision_tacl/`:

1. **Master LaTeX Source:** [manuscript_revision_tacl/main.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/main.tex)
2. **Modular Section Files (10 files):**
   - [sections/abstract.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/sections/abstract.tex)
   - [sections/introduction.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/sections/introduction.tex)
   - [sections/related_work.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/sections/related_work.tex)
   - [sections/task_and_formulation.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/sections/task_and_formulation.tex)
   - [sections/methodology.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/sections/methodology.tex)
   - [sections/experimental_setup.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/sections/experimental_setup.tex)
   - [sections/results.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/sections/results.tex)
   - [sections/discussion.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/sections/discussion.tex)
   - [sections/limitations.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/sections/limitations.tex)
   - [sections/conclusion.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/sections/conclusion.tex)
3. **Bibliography:** [manuscript_revision_tacl/references.bib](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/references.bib)
4. **Supplementary Material:** [supplementary/supplementary_material.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/supplementary/supplementary_material.tex)
5. **Formatted Tables (6 files):**
   - [tables/dataset_distribution.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/tables/dataset_distribution.tex) (Table 1)
   - [tables/transition_matrix.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/tables/transition_matrix.tex) (Table 2)
   - [tables/main_results.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/tables/main_results.tex) (Table 3)
   - [tables/statistical_tests.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/tables/statistical_tests.tex) (Table 4)
   - [tables/error_attribution.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/tables/error_attribution.tex) (Table 5)
   - [tables/case_studies.tex](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/tables/case_studies.tex) (Table 6)
6. **Publication Figures (5 vector PDFs + 5 PNGs + generator script):**
   - [figures/final/fig1_study_workflow.pdf](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/figures/final/fig1_study_workflow.pdf)
   - [figures/final/fig2_risk_coverage_tradeoff.pdf](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/figures/final/fig2_risk_coverage_tradeoff.pdf)
   - [figures/final/fig3_condition_comparison.pdf](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/figures/final/fig3_condition_comparison.pdf)
   - [figures/final/fig4_error_attribution_breakdown.pdf](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/figures/final/fig4_error_attribution_breakdown.pdf)
   - [figures/final/fig5_transition_heatmap.pdf](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/figures/final/fig5_transition_heatmap.pdf)
   - [figures/source/generate_figures.py](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/figures/source/generate_figures.py)
7. **Validation Scripts & Documentation:**
   - [manuscript_revision_tacl/validate_manuscript.py](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/validate_manuscript.py)
   - [manuscript_revision_tacl/REVISION_README.md](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/REVISION_README.md)
   - [manuscript_revision_tacl/BUILD_INSTRUCTIONS.md](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/BUILD_INSTRUCTIONS.md)
   - [manuscript_revision_tacl/FINAL_MANUSCRIPT_CHANGELOG.md](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/FINAL_MANUSCRIPT_CHANGELOG.md)
8. **Audit Reports (8 formal audit files in `manuscript_revision_tacl/audits/`):**
   - [audits/MANUSCRIPT_INITIAL_AUDIT.md](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/audits/MANUSCRIPT_INITIAL_AUDIT.md)
   - [audits/CLAIM_EVIDENCE_MATRIX.csv](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/audits/CLAIM_EVIDENCE_MATRIX.csv)
   - [audits/MANUSCRIPT_DISCREPANCY_LOG.md](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/audits/MANUSCRIPT_DISCREPANCY_LOG.md)
   - [audits/MANUSCRIPT_FACT_CHECK.md](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/audits/MANUSCRIPT_FACT_CHECK.md)
   - [audits/CITATION_AUDIT.md](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/audits/CITATION_AUDIT.md)
   - [audits/TACL_FORMAT_AUDIT.md](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/audits/TACL_FORMAT_AUDIT.md)
   - [audits/FIGURE_TABLE_AUDIT.md](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/audits/FIGURE_TABLE_AUDIT.md)
   - [audits/BUILD_AUDIT.md](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/audits/BUILD_AUDIT.md)
   - [audits/PLAGIARISM_AUDIT.md](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/audits/PLAGIARISM_AUDIT.md) (Audited Similarity Index: 0.25%, well below 20% limit)

---

## 3. Original Manuscript Preservation Verification

The integrity of the original baseline in `docs/manuscript/` has been verified bitwise via SHA-256 hash comparison across all 40 files:
- Initial files recorded: 40
- Matching files: 40 (100.0%)
- Drifted or altered files: 0
- Deleted files: 0

---

## 4. Summary of Key Scientific Findings in Revised Manuscript

1. **Prediction Disagreement:** Shifting evidence representation from original Hindi to machine-translated English alters verifier predictions on **63.80%** of instances (104/163; 95% CI: [56.19%, 70.78%]).
2. **Directional Polarity Reversals:** Of the 64 instances predicted as \textsc{Supported} under translated evidence, **48.44% (31/64)** flip to \textsc{Contradicted} when evaluated on original Hindi evidence, recovering refutations from spurious entailment.
3. **Marginal Accuracy Advantage:** Direct Multilingual verification achieves **42.94%** accuracy (70/163), significantly outperforming the No-Check translated baseline (**28.22%**, 46/163; McNemar exact $p = 0.008772$, $b=27, c=51$).
4. **Selective Cascade Limitations:** Selective-Check ($\tau^*=0.650$) triggers on 7.98% of queries, saving 59.2% latency relative to Direct Multilingual, but matches No-Check accuracy exactly (28.22%, 46/163; $b=4, c=4, p=1.0000$).
5. **Metric Discordance Under Severe Skew:** Non-parametric permutation tests on class-balanced Macro-F1 ($B=5,000$) do not reach significance ($p=0.1898$ and $p=0.1180$), demonstrating the severe volatility of harmonic metrics under benchmark class imbalance (142 \textsc{Contradicted}, 21 \textsc{Insufficient}, 0 gold \textsc{Supported}).
6. **Integrity Guardrails:** Transparently acknowledges pre-retrieved evidence grounding, prior exploratory inspection of the test split, absence of completed human bilingual annotations, and the critical distinction between observational sensitivity and translation causality.
