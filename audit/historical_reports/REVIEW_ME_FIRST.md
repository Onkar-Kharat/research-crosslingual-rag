# REVIEW ME FIRST: INDEPENDENT REVIEWER HANDOFF GUIDE

**Target Reviewer:** Independent Peer Reviewer (ChatGPT / TACL Reviewer)  
**Research Subject:** Cross-Lingual Evidence-Grounded Claim Verification (Hindi $\rightarrow$ English)  
**Dataset:** X-Fact Hindi Subset ($N=266$ authentic fact-checks: 103 dev, 163 held-out exploratory test)  
**Current Research Status:** **FROZEN — EXPLORATORY COMPUTATIONAL STUDY**  
**Canonical Status Ledger:** `FREEZE_GATE_REPORT.md` (Single Authoritative Source of Truth)  
**Delivered Research Archive:** `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip`  

---

## 1. Executive Summary of the Project

This research investigates automated claim verification when non-English evidence (Hindi) is translated into English before being evaluated by a multilingual natural language inference verifier (`mDeBERTa-v3-base-xnli`). 

The central objectives are:
1. **Primary Descriptive Outcomes (Translation Sensitivity):** Quantifying paired prediction agreement (36.20%) and label-flip disagreement (63.80% on test instances) across original-Hindi and translated-English evidence representations.
2. **Selective Evidence Routing:** Evaluating whether an automated risk trigger can selectively route uncertain claims back to original Hindi evidence (`Selective-Check`, $\tau^*=0.650$ tuned on dev data) and analyzing the resulting accuracy, Macro-F1, and CPU latency trade-offs against key baselines (`Translated-Only`, `Original-Only`, `Always-Check`, and a 100-seed matched-coverage `Random-Control`).
3. **Utility Optimality on Dev:** Honest disclosure that No-Check achieves higher development utility ($J = 0.2104$) than the cascade ($J = 0.2023$). Selective cascade routing is not Pareto-optimal on development data.
4. **Authentic Human Workflow:** Built a friction-free, offline annotation interface (`annotation_tool/app/index.html`) with two randomized, blinded packets (`annotation_tool/packets/PACKET_A_HANDOFF.zip` and `PACKET_B_HANDOFF.zip`), automated validators, and agreement analysis scripts. Zero synthetic human data is active; human annotation is pending external bilingual evaluation.

---

## 2. Research Freeze Decision & Gate Status

In strict accordance with scientific integrity guidelines, this package is certified as **FROZEN — EXPLORATORY COMPUTATIONAL STUDY**:

- **Gate A (Data Validity & Integrity):** **PASS** — Source data preserved immutably; dev ($N=103$) and test ($N=163$) partition integrity confirmed (zero leakage); absent positive class documented (0 gold `SUPPORTED`); Option C adopted; test set designated as exploratory.
- **Gate B (Defensible Novelty & Bounded Question):** **PASS** — Scholarly literature audit across 11 verified publications (`literature/LITERATURE_AUDIT.csv`); nearest neighbors compared; contribution bounded honestly (`literature/NOVELTY_ASSESSMENT.md`).
- **Gate C (Authentic Human Verification):** **PENDING / NOT PERFORMED** — Scripted annotations and fake reports quarantined in `audit/invalidated_synthetic_annotations/`. Full real-human workflow, offline tool, and blinded packets prepared in `annotation_tool/`. Because all causal translation claims are excluded under Option C, this gate does not block the computational freeze. For future causal claims, Gate C remains pending until real human submissions are received.
- **Gate D (Experimental Evidence & Tests):** **PASS** — Direct MT-verifier coupled inference rerun from scratch on CPU; dev-tuned threshold $\tau^*=0.650$; 100-seed matched-coverage random control; McNemar exact tests, permutation tests, bootstrap CIs, and FDR-corrected p-values (`experiments/results_canonical/`).
- **Gate E (Clean-Room Reproducibility):** **PASS** — 47 automated tests pass across 9 modules in $<1.0$s; clean-room extraction test in an isolated scratch directory succeeds.

---

## 3. Key Canonical Empirical Findings ($N=163$)

1. **Primary Descriptive Outcomes:**
   - Paired Prediction Agreement: **36.20%** (59/163) [95% Wilson CI: 29.22%, 43.81%]
   - Paired Prediction Disagreement: **63.80%** (104/163) [95% Wilson CI: 56.19%, 70.78%]
   - Of 64 translated predictions of `SUPPORTED`, 31 (48.44%) flipped to `CONTRADICTED` when verifying original Hindi evidence.
2. **Benchmark Accuracies and F1:**
   - **No-Check (Translated Only):** 46 / 163 = 28.22% Accuracy [21.47%, 35.58%], Observed 2-cl Macro-F1 = 0.3018, Mean Latency = 3,650.4 ms.
   - **Selective-Check ($\tau^*=0.650$):** 46 / 163 = 28.22% Accuracy [21.47%, 35.58%], Observed 2-cl Macro-F1 = 0.2950, Coverage = 8.0% (13/163), Mean Latency = 4,613.8 ms.
   - **Direct Multilingual (Original Only):** 70 / 163 = 42.94% Accuracy [35.57%, 50.92%], Observed 2-cl Macro-F1 = 0.3700, Mean Latency = 11,295.6 ms.
   - **Always-Check (Dual Consensus):** 60 / 163 = 36.81% Accuracy [29.45%, 44.17%], Observed 2-cl Macro-F1 = 0.3657, Mean Latency = 14,945.9 ms ($p = 0.0201$ vs Selective-Check).
   - **Random Routing (100 Seeds, Matched Cov 8.0%):** Mean Accuracy = 29.24% [26.38%, 31.90%], Macro-F1 = 0.2054 ($p = 0.2669$ vs Selective-Check).
3. **Statistical Significance Realities:**
   - Selective-Check vs No-Check: Identical accuracy (46 vs 46, $b=4, c=4$, McNemar $p = 1.0000$, Permutation $p = 0.7572$). Four beneficial routing interventions were exactly offset by four adverse routing interventions.
   - Direct Multilingual vs Selective-Check: Discordant $b=23, c=47$, continuity-corrected $\chi^2 = 7.5571$, exact two-sided $p = 0.005583$.
   - Direct Multilingual vs No-Check: Discordant $b=27, c=51$, continuity-corrected $\chi^2 = 6.7821$, exact two-sided $p = 0.008772$.

---

## 4. Key Files for the Reviewer to Inspect

| Priority | File Path | Content and Purpose |
|:---:|:---|:---|
| **1** | `FREEZE_GATE_REPORT.md` | Canonical gate ledger and single authoritative source of truth |
| **2** | `FINAL_PASS/FINAL_RESEARCH_FREEZE_DECISION.md` | Final one-pass freeze decision and evidence summary |
| **3** | `FINAL_PASS/CANONICAL_VALUES_TABLE.csv` | Exact canonical numbers, definitions, and producing scripts |
| **4** | `protocol/FINAL_SCOPE_AND_CLAIMS.md` | Protocol bounding, paired descriptive outcomes, and claim boundaries |
| **5** | `annotation_tool/README.md` | Architecture and manual for the real-human annotation system |
| **6** | `annotation/ANNOTATION_ANALYSIS_PLAN.md` | Pre-specified analysis plan, metrics, and stratification formulas |
| **7** | `experiments/results_canonical/RUN_MANIFEST.json` | Complete cryptographic and environmental provenance manifest |
| **8** | `TACL_READINESS_ASSESSMENT.md` | Candid evaluation of venue readiness and required future extensions |
