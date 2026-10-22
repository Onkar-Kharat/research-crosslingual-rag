# RESEARCH STATUS REPORT: CROSS-LINGUAL CLAIM VERIFICATION

**Document Identifier:** `RESEARCH_STATUS.md`  
**Date:** 2026-10-22  
**Canonical Gate Ledger:** `FREEZE_GATE_REPORT.md` (Single Authoritative Source of Truth)  
**Adopted Scope:** Option C (Cross-Lingual Verifier Prediction Sensitivity and Routing Disagreement Under Translation Shift)  
**Overall Decision:** **COMPUTATIONAL RESULTS FROZEN — EXPLORATORY; HUMAN ANNOTATION PENDING**  
**Deliverable Archive:** `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip`  

---

## 1. Authoritative Gate Status Summary

| Gate | Focus Area | Status | Evidence Path | Canonical Summary |
|:---|:---|:---:|:---|:---|
| **Gate A** | Integrity & Data Validity | **PASS** | `protocol/FINAL_SCOPE_AND_CLAIMS.md` | Data provenance verified (MIT license); zero split leakage (103 dev, 163 test); absent positive class audited (0 `SUPPORTED` claims); primary descriptive metric is paired agreement/disagreement; secondary descriptive metric is 2-class observed Macro-F1; test set designated as exploratory. |
| **Gate B** | Literature-Backed Novelty | **PASS** | `literature/LITERATURE_AUDIT.csv` | Primary citations audited across 11 peer-reviewed papers; nearest neighbors compared; novelty bounded to cross-lingual verification sensitivity diagnostics under translation shift. |
| **Gate C** | Bilingual Semantic Verification | **PENDING / NOT PERFORMED** | `annotation_tool/` | Synthetic annotations quarantined with checksums; full offline annotation tool (`annotation_tool/app/index.html`) and randomized, blinded independent packets (`annotation_tool/packets/`) engineered. Authentic human evaluations are pending external recruitment. |
| **Gate D** | Reliable Experimental Evidence | **PASS** | `experiments/results_canonical/` | Direct MarianMT translation passed to mDeBERTa; true token truncation ($\le 512$); dev grid includes zero-check baseline; 100-seed matched-count random control; exact McNemar and permutation tests with FDR correction. |
| **Gate E** | Reproducibility & Packaging | **PASS** | `reproducibility/REPRODUCE.md` | 42/42 automated tests passing in $<1.0$s across 8 modules; clean-room extraction test passes; `RUN_MANIFEST.json` generated; versioned v6 freeze archive packaged. |

---

## 2. Methodology and Boundary Disclosures

### Disclosure 1: Invalidation of Synthetic Human Data & Real Annotation Tool
- Prior synthetic scripts (`scripts/perform_bilingual_annotation.py`) and simulated human reports (96% agreement, $\kappa=0.911$, 70% error validation) have been **formally invalidated and quarantined** in `audit/invalidated_synthetic_annotations/`.
- Under the adopted observational scope (Option C), human annotation is **pending external participant recruitment**. A complete, reproducible offline annotation interface and validator have been built in `annotation_tool/`. All causal claims regarding translation distortion remain excluded from active research outputs.

### Disclosure 2: Exploratory Status of Test Partition
- The test split ($N=163$) was evaluated during prior debugging and repair iterations.
- Consequently, all test set evaluations are designated as **EXPLORATORY / PREVIOUSLY INSPECTED**. They provide empirical diagnostics of effect size and sensitivity, not confirmatory out-of-sample hypothesis testing.
- Hyperparameter selection ($\tau^* = 0.650$) was performed strictly on the development partition ($N=103$).

### Disclosure 3: Development Utility and Baseline Fairness
- On development data, evaluating the zero-check baseline against the selective cascade under $J = \text{Macro\_F1}_{3cl} - 0.15 \cdot \text{Coverage}$ reveals that **No-Check achieves higher utility ($J = 0.2104$) than the best cascade operating point ($\tau^* = 0.650, J = 0.2023$)**.
- Selective cascade routing is therefore **not Pareto-optimal** on development data; $\tau^* = 0.650$ is optimal strictly conditional on activating the cascade.

---

## 3. Verified Canonical Empirical Findings ($N=163$)

All numbers recomputed directly from `experiments/results_canonical/canonical_test_predictions.csv`:

1. **Primary Descriptive Sensitivity Outcomes:**
   - **Paired Prediction Agreement:** 59 / 163 = **36.20%** [95% Wilson CI: 29.22%, 43.81%]
   - **Paired Prediction Disagreement:** 104 / 163 = **63.80%** [95% Wilson CI: 56.19%, 70.78%]
   - Transition from translated `SUPPORTED` to original `CONTRADICTED`: 31 / 64 = **48.44%**.

2. **Benchmark Performance Summary:**
   - **No-Check (Translated Only):** Accuracy = 28.22% (46/163), Macro-F1 (3cl nominal) = 0.2012, Macro-F1 (2cl observed) = 0.3018, Mean Latency = 3,650.4 ms.
   - **Direct Multilingual (Original Only):** Accuracy = 42.94% (70/163), Macro-F1 (3cl nominal) = 0.2467, Macro-F1 (2cl observed) = 0.3700, Mean Latency = 11,295.6 ms ($p = 0.005583$ vs Selective-Check).
   - **Always-Check (Dual Consensus):** Accuracy = 36.81% (60/163), Macro-F1 (3cl nominal) = 0.2438, Macro-F1 (2cl observed) = 0.3657, Mean Latency = 14,945.9 ms ($p = 0.0201$ vs Selective-Check).
   - **Selective-Check ($\tau^*=0.650$):** Accuracy = 28.22% (46/163), Macro-F1 (3cl nominal) = 0.1967, Macro-F1 (2cl observed) = 0.2950, Coverage = 8.0% (13/163), Mean Latency = 4,613.8 ms.
   - **Random Routing (100 Seeds, Matched Cov 8.0%):** Accuracy Mean = 29.24% [26.38%, 31.90%], Macro-F1 (3cl) = 0.2054 [0.1874, 0.2217].
   - **Majority Baseline (Always CONTRADICTED):** Accuracy = 87.12% (142/163), Macro-F1 (3cl nominal) = 0.3104, Macro-F1 (2cl observed) = 0.4656.

3. **Statistical Significance Realities:**
   - Selective-Check vs No-Check: Identical accuracy (46 vs 46, $b=4, c=4$), McNemar exact $p = 1.0000$, Permutation $p = 0.7572$ (FDR $p = 0.8236$).
   - Direct Multilingual vs Selective-Check: Direct Multilingual is statistically significantly superior ($p = 0.005583$ raw, $p = 0.0149$ FDR).
   - Always-Check vs Selective-Check: Always-Check is statistically significantly superior ($p = 0.0201$ raw, $p = 0.0401$ FDR).

4. **Diagnostic Outcome Strata & Denominators ($N=163$ Test Split):**
   - **Partition of Translated Failures ($N=117$, 71.78% of test set):**
     - $S_{\text{trans}}$ (Recovered by Original Hindi Evidence): 51 / 117 (43.59% of failures; 31.29% of test set)
     - $S_{\text{verif}}$ (Both Representations Incorrect): 66 / 117 (56.41% of failures; 40.49% of test set)
   - **Partition of Translated Successes ($N=46$, 28.22% of test set):**
     - Control (Both Representations Correct): 19 / 46 (41.30% of successes; 11.66% of test set)
     - $S_{\text{degraded}}$ (Degraded by Original Hindi Evidence): 27 / 46 (58.70% of successes; 16.56% of test set)
   - **McNemar Tests vs. Direct Multilingual:**
     - **No-Check vs. Direct Multilingual:** Discordant $b=27, c=51$ ($n=78$), $\chi^2 = 529/78 = 6.7821$, exact binomial $p = 0.008772$.
     - **Selective-Check vs. Direct Multilingual:** Discordant $b=23, c=47$ ($n=70$), $\chi^2 = 529/70 = 7.5571$, exact binomial $p = 0.005583$.

