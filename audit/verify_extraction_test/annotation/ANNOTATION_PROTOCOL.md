# BILINGUAL HUMAN ANNOTATION PROTOCOL

**Date:** 2026-10-19  
**Protocol Version:** 1.0  
**Status:** Awaiting Human Execution (Required Gate C Blocker)

---

## 1. Study Design and Sampling Scheme

To scientifically validate whether the 41 items operationally classified as $E_{\text{trans}}$ genuinely suffered from meaning-altering translation corruptions (rather than model flakiness), a stratified sample of **50 items** from the held-out test set ($N=163$) is prepared for independent bilingual human review:

- **Stratum 1 (Operational $E_{\text{trans}}$, $N=20$):** Randomly sampled from the 41 items where translated prediction failed but original prediction was correct.
- **Stratum 2 (Operational $E_{\text{verif}}$, $N=20$):** Randomly sampled from the 61 items where both translated and original predictions failed.
- **Stratum 3 (Control / Both Correct, $N=10$):** Randomly sampled from items where both translated and original predictions were correct.

All 50 items are presented in a randomized order and blinded so that annotators cannot deduce the stratum or model outcome.

---

## 2. Annotator Qualifications & Independence

1. **Qualifications:** Minimum 2 independent bilingual annotators fluent in both Hindi and English with professional or native language proficiency.
2. **Independence:** Annotators must work independently without consulting each other during initial labeling.
3. **Strict Integrity Rule:** Antigravity and any automated LLM are strictly prohibited from generating synthetic annotations or simulating human adjudications. Annotations must be supplied by real human annotators.

---

## 3. Adjudication Procedure and Agreement Metrics

1. **Primary Agreement Statistic:**  
   Cohen’s Kappa ($\kappa$) will be computed on the binary agreement of `PRESERVED` vs. `ALTERED` across the two annotators.
2. **Disagreement Resolution:**  
   Where Annotator 1 and Annotator 2 disagree, a third expert adjudicator will review the item to produce the final consensus label.
3. **Validation Threshold:**  
   To confirm the operational classification of $E_{\text{trans}}$, at least 70% of sampled $E_{\text{trans}}$ instances must be confirmed as `ALTERED` by consensus human adjudication.

---

## 4. Current Research Freeze Status

- **Status:** **BLOCKED ON HUMAN ANNOTATION (NOT FROZEN)**
- **Explanation:** As mandated by the Antigravity Research Improvement and Freeze Specification, because causal claims regarding translation-fidelity vs verifier-reasoning failures require genuine human verification, the research cannot be marked `FROZEN FOR MANUSCRIPT PHASE` until these 50 rows are annotated by human annotators.
- **Handoff Packet:** The template sheet `annotation/blinded_annotation_sample.csv` and analysis script `scripts/analyze_human_annotations.py` are provided in the reproducibility package for the user.
