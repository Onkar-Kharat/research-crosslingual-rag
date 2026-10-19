# RESEARCH STATUS REPORT: CROSS-LINGUAL CLAIM VERIFICATION

**Date:** 2026-10-19  
**Evaluation Specification:** `ANTIGRAVITY_RESEARCH_IMPROVEMENT_AND_FREEZE_PROMPT.md`  
**Overall Decision:** **NOT FROZEN — BLOCKED ON HUMAN ANNOTATION (GATE C)**  
**Recommended Artifact State:** Complete Reproducibility & Audit Package Prepared for Independent ChatGPT Review

---

## 1. Gate-by-Gate Evaluation Summary

| Gate | Focus Area | Status | Evidence and Findings |
|:---|:---|:---:|:---|
| **Gate A** | Integrity & Data Validity | **PASS** | Original project preserved immutably; full inventory and input manifest hashed (`audit/input_manifest.csv`); X-Fact data provenance and MIT license verified (`data/DATASET_CARD.md`, `data/DATA_PROVENANCE_AND_LICENSES.md`); dev ($N=103$) and test ($N=163$) partition integrity confirmed; missing positive class documented and audited; prior test exposure disclosed. |
| **Gate B** | Defensible Novelty & Question | **PASS** | Comprehensive scholarly literature audit completed across 11 verified publications (`literature/LITERATURE_AUDIT.csv`); closest work (Singhal et al., ATTRIB @ NeurIPS 2024, arXiv:2410.10303) evaluated; technical matrix completed (`literature/RELATED_WORK_MATRIX.md`); contribution bounded honestly to diagnostic error disentanglement and negative consensus transfer (`literature/NOVELTY_ASSESSMENT.md`). |
| **Gate C** | Protocol & Annotation Readiness | **BLOCKED** | Protocol version 1.0 and YAML analysis plan finalized (`protocol/RESEARCH_PROTOCOL_v1.md`, `protocol/analysis_plan.yaml`); all baselines, ablations, and statistical tests formalized; blinded 50-item annotation sample prepared (`annotation/blinded_annotation_sample.csv`) with guide and analysis script. **BLOCKER:** Autonomous agent is strictly prohibited from fabricating human judgments; bilingual human adjudication (Hindi $\leftrightarrow$ English) must be performed by human annotators before Gate C can pass. |
| **Gate D** | Reliable Experimental Evidence | **PASS** | Exact point estimates recomputed directly from raw predictions; bootstrap sample mean reporting corrected; 114 vs. 111 error attribution overlap resolved into mutually exclusive partition ($41 + 61 + 9 = 111$); full ablation suite completed (proving triggered posterior averaging drops accuracy to 30.67% while hard routing achieves 39.26%); fair end-to-end latency including MT recorded; automated test suite passing (12/12 tests pass). |
| **Gate E** | Reproducibility & Freeze Readiness | **BLOCKED** | Research package is fully reproducible from automated scripts, hashes, and unit tests. However, freeze criteria explicitly require all preceding gates (including Gate C human annotation) to pass before certifying a research freeze. |

---

## 2. Unresolved Blockers and Required Human Actions

### Blocker 1: Bilingual Human Annotation of Evidence Fidelity (Gate C)
- **Problem:** Operational attribution of 41 cases to $E_{\text{trans}}$ is currently based on algorithmic model disagreement ($\hat{y}_{\text{trans}} \ne y^*$ and $\hat{y}_{\text{orig}} = y^*$). To defend the causal claim in a future TACL manuscript that machine translation distorted factual semantics, independent human verification is required.
- **Required Action:** 
  1. Have two bilingual Hindi-English annotators independently complete the 50 blinded rows in `annotation/blinded_annotation_sample.csv` adhering to `annotation/ANNOTATION_GUIDE.md`.
  2. Run `python scripts/analyze_human_annotations.py` to calculate inter-rater agreement (Cohen's $\kappa$) and empirical validation rate.
  3. Re-evaluate Gate C once annotations are returned.

### Blocker 2: Confirmatory Evaluation on Uninspected Claims
- **Problem:** The test partition ($N=163$) was evaluated during initial exploratory research. While threshold $\tau^*$ was tuned strictly on dev, the test set has been previously inspected.
- **Required Action:** If the ChatGPT reviewer or authors desire strict virgin evaluation, a held-out slice or cross-lingual benchmark partition (e.g. Marathi/Bengali or synthetic mutations) should be designated for final confirmation prior to manuscript submission.

---

## 3. Verified Empirical Research Findings

1. **Observed Performance on Held-Out Test Set ($N=163$):**
   - **No-Check (Translated):** 52 / 163 = 31.90% Accuracy [95% CI: 24.54%, 39.26%], Observed 2-cl Macro-F1 = 0.3408, Standard 3-cl Macro-F1 = 0.2272, Mean E2E Latency = 2,939.1 ms.
   - **Direct Multilingual (Original):** 61 / 163 = 37.42% Accuracy [30.06%, 44.79%], Observed 2-cl Macro-F1 = 0.3800, Standard 3-cl Macro-F1 = 0.2534, Mean E2E Latency = 4,802.8 ms.
   - **Always-Check (Dual Consensus via 0.5 Avg):** 51 / 163 = 31.29% Accuracy [24.54%, 38.65%], Observed 2-cl Macro-F1 = 0.3205, Standard 3-cl Macro-F1 = 0.2137, Mean E2E Latency = 7,741.9 ms.
   - **Selective-Check (Ours: Hard Routing, $\tau^*=0.30$):** 64 / 163 = 39.26% Accuracy [31.89%, 47.24%], Observed 2-cl Macro-F1 = 0.4067, Standard 3-cl Macro-F1 = 0.2711, Coverage = 83.4%, Mean E2E Latency = 6,968.8 ms.
2. **Statistical Significance Realities:**
   - Selective-Check vs. Always-Check: **Statistically significant** ($p = 0.0294$ exact McNemar, 22 vs 9 discordant pairs; $p = 0.0420$ permutation test). Demonstrates that naive consensus actively harms accuracy.
   - Selective-Check vs. No-Check: Directional gain (+7.36% accuracy, +4.39% Macro-F1), but **not statistically significant** ($p = 0.1480$ McNemar, 35 vs 23 discordant pairs).
   - Selective-Check vs. Direct Multilingual: +1.84% accuracy (+3 items), **not statistically significant** ($p = 0.6072$ McNemar, 9 vs 6 discordant pairs).
3. **Error Attribution Taxonomy Partition ($N=111$ total translation errors):**
   - Translation-Recovered Errors ($E_{\text{trans}}$): **41 cases (36.94%)** (38 contradicted, 3 insufficient).
   - Verifier-Reasoning Errors ($E_{\text{verif}}$): **61 cases (54.95%)** on contradicted claims.
   - Unresolved Evidence Insufficiency ($E_{\text{insuff}}$): **9 cases (8.11%)** on insufficient claims.
   - Total Sum: $41 + 61 + 9 = 111$ (100.00%, cleanly partitions all failures without overlap).
4. **Posterior Averaging vs. Hard Routing Ablation:**
   - Averaging posterior probabilities on triggered items (paper Eq 1 text) degrades accuracy to **30.67%** (50/163). Hard routing achieves **39.26%** (64/163).
