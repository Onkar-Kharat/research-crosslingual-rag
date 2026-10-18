# Pre-Specified Bilingual Human Annotation Analysis Plan

**Document Identifier:** `annotation/ANNOTATION_ANALYSIS_PLAN.md`  
**Protocol Version:** 2.0  
**Date:** 2026-10-22  
**Governance:** Antigravity Research Protocol for Translation Fidelity Validation  

---

## 1. Study Objective and Hypotheses

The goal of the human annotation protocol is to determine whether translation shift introduces meaning-altering semantic corruptions into evidence passages, and to what extent operational error categories ($S_{\text{trans}}$ vs $S_{\text{verif}}$) correspond to genuine translation-induced errors.

### Hypotheses:
- **$H_1$ (Translation Distortion in $S_{\text{trans}}$):** Evidence passages in the operational $S_{\text{trans}}$ stratum (where verifying translated evidence failed, but verifying original Hindi evidence succeeded) exhibit a significantly higher rate of factual alteration (`ALTERED`) than passages in the Control stratum (where both languages succeeded).
- **$H_2$ (Reasoner Error in $S_{\text{verif}}$):** Evidence passages in $S_{\text{verif}}$ (where the verifier failed under both representations) exhibit a lower rate of meaning alteration than $S_{\text{trans}}$, reflecting verifier comprehension or background knowledge limitations.

---

## 2. Sampling Design and Stratification

A stratified random sample of $N=50$ instances is drawn with fixed seed 42 from the canonical test set ($N=163$):
1. **Stratum 1 ($S_{\text{trans}}$, $N_1 = 20$):** Sampled from the population of $M_1 = 51$ translation-recovery cases.
2. **Stratum 2 ($S_{\text{verif}}$, $N_2 = 20$):** Sampled from the population of $M_2 = 66$ joint failure cases.
3. **Stratum 3 (Control, $N_3 = 10$):** Sampled from the population of $M_3 = 19$ joint success cases.

### Blinding Guarantees:
- Both annotators receive the same 50 underlying items in different randomized permutations.
- Items are designated with opaque random identifiers (`OPQ-A-01..50` and `OPQ-B-01..50`).
- Gold veracity labels, verifier predictions, model confidence scores, error strata, and annotator identities are completely hidden.

---

## 3. Evaluation Metrics and Agreement Statistics

### 3.1 Primary Inter-Rater Agreement:
1. **Raw Percentage Agreement ($P_o$):** Proportion of items where Annotator 1 and Annotator 2 assign identical `fidelity_label` categories.
2. **Multi-Class Cohen's Kappa ($\kappa$):** Calculated across the 4-way label space (`PRESERVED`, `ALTERED`, `AMBIGUOUS_SOURCE`, `UNABLE_TO_DECIDE`):
   $$\kappa = \frac{P_o - P_e}{1 - P_e}$$
   with analytical standard error (Fleiss et al., 1969) and 95% confidence intervals.
3. **Binary Kappa ($\kappa_{\text{binary}}$):** Calculated on `ALTERED` vs `NOT_ALTERED` (`PRESERVED`, `AMBIGUOUS_SOURCE`, `UNABLE_TO_DECIDE`).

### 3.2 Small-Sample Caveat & Prevalence Disclosure:
Because Cohen's $\kappa$ is sensitive to skewed marginal prevalence, $\kappa$ will **not** be reported in isolation. It will be accompanied by marginal label prevalence and raw percentage agreement.

### 3.3 Multi-Label Distortion Analysis:
For items agreed as `ALTERED`, agreement on specific distortion types (`NUM_DATE`, `NEGATION`, `ENTITY`, `OMISSION`, `HALLUCINATION`, `QUALIFIER`, `TIME`, `OTHER`) will be evaluated using mean Jaccard overlap:
$$J(D_1, D_2) = \frac{|D_1 \cap D_2|}{|D_1 \cup D_2|}$$

---

## 4. Population Prevalence Estimation

Because sampling is stratified, the raw fraction of `ALTERED` instances in the 50-item sample cannot be interpreted as population prevalence without weighting.
The estimated population proportion of translation failures ($N_{\text{err}} = 117$, comprising $M_1 = 51$ and $M_2 = 66$) attributable to semantic alteration is calculated via stratified post-stratification:
$$\hat{P}_{\text{altered}|N_{\text{err}}} = \frac{M_1}{M_1 + M_2} \hat{p}_1 + \frac{M_2}{M_1 + M_2} \hat{p}_2 = \frac{51}{117} \hat{p}_1 + \frac{66}{117} \hat{p}_2$$
where $\hat{p}_1$ and $\hat{p}_2$ are the consensus alteration rates observed in Stratum 1 and Stratum 2.
Variance and 95% confidence intervals will be estimated using stratified sampling formulas:
$$\widehat{\text{Var}}(\hat{P}) = \left(\frac{51}{117}\right)^2 \frac{\hat{p}_1(1-\hat{p}_1)}{n_1 - 1} \left(1 - \frac{n_1}{M_1}\right) + \left(\frac{66}{117}\right)^2 \frac{\hat{p}_2(1-\hat{p}_2)}{n_2 - 1} \left(1 - \frac{n_2}{M_2}\right)$$

---

## 5. Adjudication Procedure and Project-Specific Criteria

1. **Disagreement Queue:** Where Annotator 1 and Annotator 2 disagree on `fidelity_label`, the item is queued into `disagreement_queue_for_adjudication.csv` for independent review by a third bilingual adjudicator.
2. **Project Validation Criterion (Pre-Analysis Benchmark):**
   - The operational classification of $S_{\text{trans}}$ as genuine translation distortion will be considered supported if the consensus alteration rate in Stratum 1 satisfies:
     $$\hat{p}_1 \ge 0.70 \quad (70\%)$$
   - *Epistemic Status:* This 70% threshold is an internal, project-specific operational target established to distinguish systematic translation failure from random model flakiness. It is **not** a universal natural law. The primary research deliverable will be the point estimate and confidence interval $\hat{p}_1 \pm 1.96 \cdot \text{SE}(\hat{p}_1)$, rather than a binary pass/fail decree.
