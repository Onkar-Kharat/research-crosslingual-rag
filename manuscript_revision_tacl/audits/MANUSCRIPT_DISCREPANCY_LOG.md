# Manuscript Discrepancy and Audit Log

**Audit Track:** TACL Manuscript Revision  
**Authoritative Directory:** `manuscript_revision_tacl/`  
**Date:** 2026-10-24  

---

## 1. Executive Summary

This log records all identified discrepancies, ambiguities, or historical transcription anomalies between draft manuscript versions, earlier summary reports, and canonical frozen artifacts. Every issue listed below has been formally investigated against instance-level canonical data (`experiments/results_canonical/canonical_test_predictions.csv` and `canonical_results.csv`) and fully resolved in the revised manuscript.

---

## 2. Itemized Discrepancy Audit

### Discrepancy DISC-01: McNemar Paired Contingency Table Misattribution
- **Location in Drafts:** Section 4.3 & Table 4 text descriptions.
- **Previous Draft Statement:** Older draft text reported discordant pairs $b=27, c=51$ while attributing the test statistic $\chi^2 = 7.5571$.
- **Canonical Fact Check:**
  - In `experiments/results_canonical/canonical_test_predictions.csv`:
    - **Selective-Check vs. Direct Multilingual:** $b = 23$ (Selective correct, Direct wrong), $c = 47$ (Selective wrong, Direct correct). Continuity-corrected McNemar $\chi^2 = (|23 - 47| - 1)^2 / (23 + 47) = 23^2 / 70 = 529 / 70 = 7.55714$, yielding $p = 0.005583$.
    - **No-Check vs. Direct Multilingual:** $b = 27$ (No-Check correct, Direct wrong), $c = 51$ (No-Check wrong, Direct correct). Continuity-corrected McNemar $\chi^2 = (|27 - 51| - 1)^2 / (27 + 51) = 23^2 / 78 = 529 / 78 = 6.78205$, yielding $p = 0.008772$.
- **Resolution in Revised Manuscript:** The text and tables now distinctly and accurately report both comparisons:
  - Selective vs Direct Multi: $b=23, c=47, \chi^2=7.5571, p=0.0056$ (FDR $p=0.0149$).
  - No-Check vs Direct Multi: $b=27, c=51, \chi^2=6.7821, p=0.0088$ (FDR $p=0.0175$).
- **Status:** `RESOLVED & VERIFIED`.

---

### Discrepancy DISC-02: Missing Gold Class Formulation in Macro-F1
- **Location in Drafts:** Results section discussing F1 performance.
- **Issue:** In the X-Fact Hindi test set ($N=163$), gold labels are distributed as 142 `CONTRADICTED`, 21 `INSUFFICIENT_EVIDENCE`, and 0 `SUPPORTED`. Evaluating a standard 3-class macro-F1 introduces division-by-zero or zero-support penalties for the `SUPPORTED` class.
- **Canonical Fact Check:**
  - 3-Class Macro-F1: No-Check = 0.2012, Direct Multilingual = 0.2467, Selective-Check = 0.1967.
  - 2-Class Observed Macro-F1 (evaluating only observed gold classes): No-Check = 0.3018, Direct Multilingual = 0.3700, Selective-Check = 0.2950.
- **Resolution in Revised Manuscript:** Both 3-class and 2-class macro-F1 metrics are explicitly defined and reported side-by-side in Table 3. The manuscript text clarifies why both metrics are necessary and emphasizes that the permutation tests on Macro-F1 ($p=0.1898$ and $p=0.1180$) are statistically non-significant due to variance under extreme class skew.
- **Status:** `RESOLVED & VERIFIED`.

---

### Discrepancy DISC-03: Characterization of Test Split Holdout
- **Location in Drafts:** Experimental Setup & Limitations sections.
- **Issue:** Some preliminary working notes referred to the test split as an "unseen confirmatory benchmark."
- **Canonical Fact Check:** Per project provenance logs, the test split was inspected during early exploratory rounds before the computational research freeze was finalized.
- **Resolution in Revised Manuscript:** The manuscript strictly characterizes the evaluation as an *exploratory computational investigation on a previously inspected test split ($N=163$)*. No claims of blind confirmatory trial are made.
- **Status:** `RESOLVED & VERIFIED`.

---

### Discrepancy DISC-04: End-to-End RAG vs. Pre-Retrieved Evidence
- **Location in Drafts:** Introduction and Task Formulation.
- **Issue:** The broader research theme encompasses cross-lingual RAG, which could inadvertently suggest that multi-hop vector retrieval was experimentally evaluated.
- **Canonical Fact Check:** The experimental pipeline evaluates claims paired with pre-retrieved top evidence passages extracted from X-Fact Hindi.
- **Resolution in Revised Manuscript:** Explicitly defined as *cross-lingual evidence verification* isolating the NLI verifier stage under translation shift, rather than full end-to-end information retrieval.
- **Status:** `RESOLVED & VERIFIED`.

---

### Discrepancy DISC-05: Causal Claims Regarding Translation Quality
- **Location in Drafts:** Error attribution and discussion sections.
- **Issue:** Preliminary notes considered attributing prediction flips to specific machine translation errors (e.g., named entity distortion).
- **Canonical Fact Check:** Human bilingual translation annotations were quarantined and intentionally blocked (Gate C) to prevent unvalidated synthetic annotations.
- **Resolution in Revised Manuscript:** The manuscript strictly avoids causal claims. It presents observed surface correlations (e.g., numeral mismatches) as heuristic diagnostic indicators rather than proven causal mechanisms.
- **Status:** `RESOLVED & VERIFIED`.

---

## 3. Audit Verification Conclusion

All five historical discrepancies have been audited against the canonical frozen artifacts. The revised manuscript in `manuscript_revision_tacl/` faithfully adheres to the verified empirical record without exception.
