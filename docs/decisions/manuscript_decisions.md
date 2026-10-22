# Manuscript Editorial and Scientific Decisions

**Date:** 2026-10-24  
**Primary Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Status:** `DRAFT PREPARATION — INTERNAL REVIEW READY`  

---

## 1. Title Decision
- **Authoritative Working Title:**  
  *Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift*
- **Alternative Evaluated:**  
  *Separating Translation-Fidelity and Verifier-Reasoning Errors in Cross-Lingual RAG* (Rejected: overclaims causal error attribution without human annotations and implies full end-to-end RAG evaluation).
- **Decision:** Retain the working title, which precisely communicates the empirical subject, model mechanism, language pair, and diagnostic character.

---

## 2. Venue Alignment: TACL
- **Format Requirements:** TACL style sheet (`tacl2021v1.sty`), line-numbered anonymous submission format, maximum 12 pages content (excluding references and appendices).
- **Scope Fit:** TACL values thorough, reproducible empirical investigations of fundamental NLP phenomena (multilingual models, translation shift, NLI evaluation methodology). Framing the paper as a disciplined diagnostic characterization of evidence translation effects aligns with TACL's evaluation standards.

---

## 3. Framing Decisions

| Dimension | Previous (Invalidated) Framing | Adopted (Authoritative) Framing | Rationale |
|---|---|---|---|
| **Pipeline Scope** | "End-to-End Multilingual RAG" | "Cross-Lingual Evidence Verification" | Evidence passages are pre-retrieved; retrieval was not varied. |
| **Error Attribution** | "Causal Translation Errors" | "Observational Prediction Sensitivity & Stratified Disagreement" | Causal semantic distortion cannot be claimed without completed human annotation. |
| **Test Set Status** | "Untouched Confirmatory Holdout" | "Previously Inspected Exploratory Test Split" | The split was analyzed in previous iterations; honesty requires exploratory framing. |
| **Statistical Tests** | Equated McNemar and Permutation Tests | Separated Accuracy (McNemar) from Class-Balanced F1 (Permutation) | Evaluates distinct mathematical properties under severe class skew. |
| **Cascade Evaluation** | "Global Pareto Dominance" | "Optimal Conditional Cascade Configuration" | Development baseline utility ($J=0.2104$) exceeds cascade peak ($J=0.2023$). |
