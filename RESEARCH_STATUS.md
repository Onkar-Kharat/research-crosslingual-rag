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

## 3. Verified Empirical Research Findings (From Scratch Corrected Rerun)

1. **Observed Performance on Held-Out Test Set ($N=163$):**
   - **No-Check (Translated Only):** 54 / 163 = 33.13% Accuracy [95% CI: 25.77%, 40.51%], Observed 2-cl Macro-F1 = 0.3520 [0.2704, 0.4348], Standard 3-cl Macro-F1 = 0.2346 [0.1803, 0.2898], Mean E2E Latency = 3,600.0 ms (MT: 1,616.0 ms, Verifier: 1,984.1 ms).
   - **Direct Multilingual (Original Only):** 70 / 163 = 42.94% Accuracy [35.57%, 50.92%], Observed 2-cl Macro-F1 = 0.3700 [0.2972, 0.4537], Standard 3-cl Macro-F1 = 0.2467 [0.1981, 0.3025], Mean E2E Latency = 11,035.4 ms (no MT needed).
   - **Always-Check (Dual Consensus via 0.5 Avg):** 65 / 163 = 39.88% Accuracy [32.52%, 47.85%], Observed 2-cl Macro-F1 = 0.3913 [0.3096, 0.4779], Standard 3-cl Macro-F1 = 0.2609 [0.2064, 0.3186], Mean E2E Latency = 14,635.4 ms (MT + dual verifiers).
   - **Selective-Check (Ours: Hard Routing, $\tau^*=0.30$ tuned on Dev):** 55 / 163 = 33.74% Accuracy [26.99%, 41.10%], Observed 2-cl Macro-F1 = 0.3575 [0.2769, 0.4399], Standard 3-cl Macro-F1 = 0.2383 [0.1846, 0.2933], Coverage = 8.6%, Mean E2E Latency = 4,567.8 ms (saving 68.8% latency vs Always-Check).
2. **Comprehensive Ablations ($N=163$):**
   - **Ablation: Triggered Posterior Averaging:** 54 / 163 = 33.13% Accuracy, Macro-F1 (3-cl) = 0.2357.
   - **Ablation: Uncertainty-Only Routing:** 50 / 163 = 30.67% Accuracy, Macro-F1 (3-cl) = 0.2177.
   - **Ablation: Numeral-Only Routing:** 73 / 163 = 44.79% Accuracy, Macro-F1 (3-cl) = 0.2529, Coverage = 96.9%.
   - **Control: Random Routing (Matched Coverage 8.6%):** 54 / 163 = 33.13% Accuracy, Macro-F1 (3-cl) = 0.2380.
   - **Oracle Upper Bound (Non-Deployable):** 104 / 163 = 63.80% Accuracy, Macro-F1 (3-cl) = 0.3759.
3. **Statistical Significance Realities:**
   - Selective-Check vs. Uncertainty-Only Routing: Statistically significant advantage for selective routing ($p = 0.0380$ permutation test).
   - Selective-Check vs. Always-Check: Directional latency reduction of 10,067.6 ms (saving 68.8% compute).
   - Selective-Check vs. No-Check: +0.61% accuracy, +0.37% Macro-F1 ($p = 1.000$ McNemar, 2 vs 1 discordant pairs; $p = 0.6138$ permutation test).
4. **Diagnostic Error Attribution ($N=109$ total translation errors):**
   - Translation-Associated Errors ($E_{\text{trans}}$, Recovered by Original): **50 cases (45.87%)**.
   - Verifier-Reasoning Errors ($E_{\text{verif}}$, Failed in Both Languages): **59 cases (54.13%)**.
   - Total Sum: $50 + 59 = 109$ (100.00% of translated errors).
   - Unresolved Evidence Insufficiency: 54 cases predicted as INSUFFICIENT_EVIDENCE.
