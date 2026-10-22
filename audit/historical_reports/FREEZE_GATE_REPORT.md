# Research Freeze Gate Report (Canonical Source of Truth)

**Document Identifier:** `FREEZE_GATE_REPORT.md`  
**Evaluation Prompt:** `ANTIGRAVITY_FINAL_VALUES_AND_HUMAN_ANNOTATION_WORKFLOW_PROMPT.md`  
**Date:** 2026-10-22  
**Adopted Scope:** Option C (Cross-Lingual Verifier Prediction Sensitivity and Routing Disagreement Under Translation Shift)  
**Overall Freeze Decision:** **COMPUTATIONAL RESULTS FROZEN — EXPLORATORY; HUMAN ANNOTATION PENDING**  
**Versioned Research Package:** `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip`  

---

## 1. Executive Summary

This report establishes the authoritative gate decision for the research project in accordance with `ANTIGRAVITY_FINAL_VALUES_AND_HUMAN_ANNOTATION_WORKFLOW_PROMPT.md`. The research scope is formally locked to **Option C: Cross-lingual verifier prediction sensitivity and routing disagreement under Hindi-to-English translation shift**. 

All prior causal and human-validation claims have been eliminated, and synthetic annotation artifacts remain quarantined in `audit/invalidated_synthetic_annotations/`. A complete, reusable, friction-free real-human annotation system has been engineered in `annotation_tool/` (including an offline browser interface, two randomized and blinded independent packets, an automated schema validator, and pre-registered inter-rater agreement scripts). Because real human evaluation requires external participants, bilingual human verification (Gate C) is designated as **PENDING / NOT PERFORMED**.

All computational, algorithmic, and methodological requirements have been independently audited, repaired, and recomputed from scratch:
1. **Primary Descriptive Outcomes Defined:** Paired prediction agreement between translated-English and original-Hindi evidence is **36.20%** (59/163) [95% Wilson CI: 29.22%, 43.81%]; paired prediction disagreement (label flips) is **63.80%** (104/163) [95% Wilson CI: 56.19%, 70.78%].
2. **Direct Translation-Inference Coupling:** MarianMT translations are decoded and passed directly to mDeBERTa under true token truncation ($\le 512$). End-to-end latency is measured on the exact pipeline used for inference.
3. **Threshold Selection & Baseline Fairness:** Threshold selection on development data ($N=103$) includes the zero-check operating point. Recomputation reveals that No-Check ($J=0.2104$) achieves higher development utility than any cascade threshold ($\tau=0.650, J=0.2023$), proving that selective cascade routing is not Pareto-optimal on development data. $\tau^*=0.650$ is retained strictly as the optimal point *conditional on cascade activation*.
4. **Rigorous Baselines & Controls:** Includes a 100-seed random routing control with exact item count matching ($K = \text{round}(N \cdot \text{Coverage}) = 13$), exact McNemar paired tests, 5,000-permutation paired F1 tests, and Benjamini-Hochberg FDR correction.
5. **Honest Negative Empirical Finding:** Selective-Check ($\tau^*=0.650$) achieves identical accuracy ($28.22\%$, 46/163) to No-Check ($28.22\%$, 46/163, $p=1.0000$), while Direct Multilingual on original Hindi evidence achieves $42.94\%$ ($p=0.0056$ vs Selective-Check). No superiority claims are made.
6. **Verified Reproducibility:** 42 automated unit and regression tests pass in $< 1.0$s across 8 verification modules. Clean-room extraction test succeeds.

With all computational requirements fully satisfied and limitations transparently recorded, the project is certified as **COMPUTATIONAL RESULTS FROZEN — EXPLORATORY; HUMAN ANNOTATION PENDING**.

---

## 2. Gate-by-Gate Evaluation Ledger

| Gate | Focus Area | Status | Evidence and Audit Findings |
|:---|:---|:---:|:---|
| **Gate A** | Integrity, Data Splits, and Task Formulation | **PASS** | X-Fact raw data provenance, licensing (MIT), and split integrity verified (`data/DATASET_CARD.md`). Dev ($N=103$) and test ($N=163$) partitions have zero item ID or claim text leakage. Total absence of gold `SUPPORTED` claims audited and disclosed. Task formulated under Option C (`protocol/FINAL_SCOPE_AND_CLAIMS.md`). Primary descriptive metric established as paired prediction agreement/disagreement; secondary descriptive metric is observed 2-class Macro-F1; nominal 3-class Macro-F1 retained as secondary reference. Test set formally classified as EXPLORATORY / PREVIOUSLY INSPECTED. |
| **Gate B** | Literature-Backed Contribution & Novelty Bounding | **PASS** | Verified primary-source literature audit across 11 publications (`literature/LITERATURE_AUDIT.csv`). Clarified distinction from nearest neighbors: Chang et al. (ROCLING 2023, cross-lingual NLI bias), Singhal et al. (ATTRIB @ NeurIPS 2024, attribution), and Wang et al. (ACL 2026, multilingual fact-checking). Novelty honestly bounded to cross-lingual verification sensitivity diagnostics and risk-driven routing under translation shift (`literature/NOVELTY_ASSESSMENT.md`). All claims of "novel architecture", "state-of-the-art", or "first end-to-end cross-lingual RAG" eliminated. |
| **Gate C** | Bilingual Semantic Verification | **PENDING / NOT PERFORMED** | **Scope-Conditioned Gate:** Synthetic annotations quarantined in `audit/invalidated_synthetic_annotations/`. Built complete, reusable human annotation workflow in `annotation_tool/` (offline HTML5 app, blinded Packets A and B with opaque item IDs, automated validator, pre-registered analysis plan). Real human evaluations are pending external recruitment. Because all causal translation claims are excluded under Option C, this gate does not block the computational freeze. For any future causal study, Gate C remains pending until real human submissions are received. |
| **Gate D** | Model Inference, Baselines, and Honest Empirical Findings | **PASS** | Complete rerun from scratch on CPU (`scripts/run_corrected_experiments.py`): decoded MarianMT output verified directly by mDeBERTa; true token truncation ($\le 512$); numeral Jaccard overlap computed on generated translation; dev grid tuning includes zero-check baseline; 100-seed matched-count random control; exact McNemar tests, 5,000-permutation tests, bootstrap 95% CIs, and Benjamini-Hochberg FDR correction. Results honestly reported: Selective-Check ($28.22\%$) matches No-Check ($28.22\%$) and trails Direct Multilingual ($42.94\%$) and Always-Check ($36.81\%$). |
| **Gate E** | Clean-Room Reproducibility & Test Provenance | **PASS** | Comprehensive automated test suite in `tests/` (42 tests across 8 verification modules, passing in 0.95s). Clean-room extraction verified in scratch directory without local absolute paths. Canonical output directory `experiments/results_canonical/` populated with predictions, metrics, statistical tests, figures, and verified `RUN_MANIFEST.json`. |

---

## 3. Canonical Benchmark Performance (Exploratory Test Partition, $N=163$)

All metrics recomputed from canonical per-instance predictions (`experiments/results_canonical/canonical_test_predictions.csv`):

| Condition / Strategy | Accuracy (Point & 95% CI) | Macro-F1 (3-Class Nominal) | Macro-F1 (2-Class Observed) | Coverage (%) | Mean E2E Latency (ms) | Paired McNemar Test vs Selective (Raw / FDR) | Paired Permutation Test vs Selective (Raw / FDR) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **No-Check (Translated Only)** | 28.22% [21.47%, 35.58%] | 0.2012 [0.1498, 0.2516] | 0.3018 [0.2248, 0.3774] | 0.0% | 3,650.4 ms | $p = 1.0000$ / $p = 1.0000$ ($b=4, c=4$) | $p = 0.7572$ / $p = 0.8236$ |
| **Direct Multilingual (Original Only)** | 42.94% [35.57%, 50.92%] | 0.2467 [0.1981, 0.3025] | 0.3700 [0.2972, 0.4537] | 100.0% | 11,295.6 ms | $p = 0.005583$ / $p = 0.0149$ ($b=23, c=47$) | $p = 0.1180$ / $p = 0.2360$ |
| **Always-Check (Dual Consensus Avg)** | 36.81% [29.45%, 44.17%] | 0.2438 [0.1901, 0.3023] | 0.3657 [0.2852, 0.4534] | 100.0% | 14,945.9 ms | $p = 0.0201$ / $p = 0.0401$ ($b=9, c=23$) | $p = 0.0196$ / $p = 0.0784$ |
| **Selective-Check (Hard Route, $\tau^*=0.650$)** | 28.22% [21.47%, 35.58%] | 0.1967 [0.1450, 0.2494] | 0.2950 [0.2175, 0.3741] | 8.0% (13/163) | 4,613.8 ms | Reference System | Reference System |
| **Ablation: Triggered Post. Averaging** | 26.99% [20.25%, 34.36%] | 0.1903 [0.1396, 0.2427] | 0.2854 [0.2094, 0.3640] | 8.0% | 4,613.8 ms | $p = 0.6250$ / $p = 0.8333$ ($b=3, c=1$) | $p = 0.3684$ / $p = 0.4912$ |
| **Ablation: Uncertainty-Only Routing** | 28.22% [21.47%, 35.58%] | 0.2012 [0.1500, 0.2570] | 0.3018 [0.2250, 0.3856] | 8.0% | 4,613.8 ms | $p = 1.0000$ / $p = 1.0000$ ($b=2, c=2$) | $p = 0.8236$ / $p = 0.8236$ |
| **Ablation: Numeral-Only Routing** | 44.79% [37.42%, 52.76%] | 0.2529 [0.2050, 0.3076] | 0.3794 [0.3075, 0.4615] | 96.3% | 14,751.3 ms | $p = 0.0013$ / $p = 0.0052$ ($b=20, c=47$) | $p = 0.0744$ / $p = 0.1984$ |
| **Control: Random Routing (100 Seeds, Matched Cov)** | 29.24% [26.38%, 31.90%] | 0.2054 [0.1874, 0.2217] | 0.3082 [0.2810, 0.3326] | 8.0% | 4,613.8 ms | $p = 0.2669$ / $p = 0.4270$ ($b=4, c=9$) | $p = 0.1650$ / $p = 0.2640$ |
| **Majority Baseline (Always CONTRADICTED)** | 87.12% [81.60%, 92.02%] | 0.3104 [0.2907, 0.3279] | 0.4656 [0.4361, 0.4919] | 0.0% | 0.0 ms | Baseline Reference | Baseline Reference |
| **Oracle Upper Bound (Non-Deployable)** | 59.51% [52.15%, 66.87%] | 0.3467 [0.2867, 0.4067] | 0.5200 [0.4300, 0.6100] | 100.0% | 14,945.9 ms | $p < 0.0001$ / $p < 0.0001$ ($b=0, c=51$) | $p < 0.0001$ / $p < 0.0001$ |

---

## 4. Primary Descriptive Sensitivity Outcomes ($N=163$)

- **Paired Prediction Agreement:** 59 / 163 = **36.20%** [95% Wilson CI: 29.22%, 43.81%]
- **Paired Prediction Disagreement:** 104 / 163 = **63.80%** [95% Wilson CI: 56.19%, 70.78%]
- **Transition Dynamics:**
  - Of 64 translated predictions of `SUPPORTED`, 31 (48.44%) flipped to `CONTRADICTED` when verifying original Hindi evidence.
  - Of 55 translated predictions of `INSUFFICIENT_EVIDENCE`, 23 (41.82%) flipped to `CONTRADICTED`.
- **Diagnostic Outcome Strata & Denominators ($N=163$):**
  - **Translated Failures Partition ($N=117$):**
    - $S_{\text{trans}}$ (Recovered by Original Hindi Evidence): 51 instances (43.59% of failures; 31.29% of test set)
    - $S_{\text{verif}}$ (Both Representations Incorrect): 66 instances (56.41% of failures; 40.49% of test set)
  - **Translated Successes Partition ($N=46$):**
    - Control (Both Representations Correct): 19 instances (41.30% of successes; 11.66% of test set)
    - $S_{\text{degraded}}$ (Degraded by Original Hindi Evidence): 27 instances (58.70% of successes; 16.56% of test set)
  - **Paired McNemar Tests:**
    - No-Check vs. Direct Multilingual: $b=27, c=51$ ($n=78$), $\chi^2 = 529/78 = 6.7821$, exact binomial $p = 0.008772$.
    - Selective-Check vs. Direct Multilingual: $b=23, c=47$ ($n=70$), $\chi^2 = 529/70 = 7.5571$, exact binomial $p = 0.005583$.

---

## 5. Development Threshold Tuning Audit

On the development set ($N=103$), evaluation of the grid $\tau \in \{0.10, \dots, 0.65\}$ alongside the zero-check baseline under utility $J = \text{Macro\_F1}_{3cl} - 0.15 \cdot \text{Coverage}$:
- **No-Check Baseline ($\tau = \infty$, Coverage = 0.0%):** Macro-F1 = 0.2104, Penalty = 0.0000, **$J = 0.2104$**
- **$\tau = 0.650$ (Coverage = 12.62%):** Macro-F1 = 0.2213, Penalty = 0.0189, **$J = 0.2023$**
- **$\tau = 0.500$ (Coverage = 38.83%):** Macro-F1 = 0.2268, Penalty = 0.0583, **$J = 0.1686$**
- **$\tau = 0.100$ (Coverage = 93.20%):** Macro-F1 = 0.2505, Penalty = 0.1398, **$J = 0.1107$**

**Conclusion:** The No-Check baseline achieves the highest global utility on development data ($J=0.2104 > 0.2023$). Selective cascade routing does not achieve Pareto-optimality on development data. $\tau^* = 0.650$ is strictly the optimal threshold *conditional on using the cascade*.

---

## 6. Freeze Certification and Boundaries

### Decision:
**COMPUTATIONAL RESULTS FROZEN — EXPLORATORY; HUMAN ANNOTATION PENDING**

### Certified Boundary Conditions:
1. **Scope Boundary:** Observational study of prediction sensitivity under translation shift; no causal translation fidelity claims.
2. **Data Boundary:** Results on test ($N=163$) are exploratory and descriptive; gold positive class is absent ($N=0$).
3. **Model Boundary:** Pre-retrieved evidence verification only; no retriever or generative LM.
4. **Human Verification Boundary:** Authentic human annotation was not performed; ready-to-use offline tool and blinded packets are built in `annotation_tool/` for future external execution.
5. **Manuscript Status:** `manuscript/` remains locked from edits.
