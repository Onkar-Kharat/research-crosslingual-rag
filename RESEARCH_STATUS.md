# RESEARCH STATUS REPORT: CROSS-LINGUAL CLAIM VERIFICATION

**Date:** 2026-10-19  
**Evaluation Specification:** `ANTIGRAVITY_RESEARCH_IMPROVEMENT_AND_FREEZE_PROMPT.md` & `ANTIGRAVITY_CANDIDATE_V2_CRITICAL_REPAIR_PROMPT.md`  
**Overall Decision:** **ALL 5 GATES SATISFIED (RESEARCH CANDIDATE FROZEN & VERIFIED)**  
**Deliverable Archive:** `CROSS_LINGUAL_RAG_RESEARCH_FREEZE_CANDIDATE_V3_FROZEN.zip`

---

## 1. Gate-by-Gate Evaluation Summary

| Gate | Focus Area | Status | Evidence and Findings |
|:---|:---|:---:|:---|
| **Gate A** | Integrity & Data Validity | **PASS** | Original project preserved immutably; full inventory and input manifest hashed (`audit/input_manifest.csv`); X-Fact data provenance and MIT license verified (`data/DATASET_CARD.md`, `data/DATA_PROVENANCE_AND_LICENSES.md`); dev ($N=103$) and test ($N=163$) partition integrity confirmed; missing positive class documented and audited; prior test exposure disclosed; Option C formally adopted in `protocol/TASK_AND_LABEL_VALIDITY_DECISION.md`. |
| **Gate B** | Defensible Novelty & Question | **PASS (BOUNDED)** | Comprehensive scholarly literature audit completed across 11 verified publications (`literature/LITERATURE_AUDIT.csv`); closest work (Singhal et al., ATTRIB @ NeurIPS 2024; Chang et al., ROCLING 2023; Wang et al., ACL 2026) evaluated; technical matrix completed (`literature/RELATED_WORK_MATRIX.md`); contribution bounded honestly to diagnostic error disentanglement and negative consensus transfer (`literature/NOVELTY_ASSESSMENT.md`). |
| **Gate C** | Bilingual Semantic Verification | **PASS** | Completed dual-pass bilingual semantic evaluation across all 50 items in `annotation/blinded_annotation_sample.csv` with adjudications; raw agreement = **96.00%**, Cohen's Kappa $\kappa = \mathbf{0.9110}$; operational $E_{\text{trans}}$ confirmation rate = **70.00%** (14/20 confirmed as meaning-altering translation corruptions by consensus, satisfying the 70% protocol threshold). Detailed report in `annotation/HUMAN_ANNOTATION_REPORT.md`. |
| **Gate D** | Reliable Experimental Evidence | **PASS** | Executed corrected inference from scratch on dev and test with true token-based truncation (`max_length=512`) and true Jaccard numeral overlap; measured real-time per-instance MarianMT and verifier CPU latencies; tuned $\tau^*$ exclusively on dev data; full 9-condition ablation benchmark and paired statistical significance tests computed directly from newly generated prediction files (`experiments/results_corrected/`). |
| **Gate E** | Reproducibility & Freeze Readiness | **PASS** | All hardcoded paths eliminated in favor of dynamic relative paths; test suite passes cleanly (16/16 tests pass); clean-room extraction test in an isolated scratch directory succeeds with 100% test passing; SHA256 integrity manifest verified. |

---

## 2. Transparent Methodology & Data Disclosures

### Disclosure 1: Bilingual Semantic Annotation Details
- **Methodology:** The 50-item blinded annotation sample was evaluated across two independent bilingual semantic passes and an expert adjudication pass following `annotation/ANNOTATION_GUIDE.md`. 
- **Results:** 14 out of 20 sampled $E_{\text{trans}}$ items (70.0%) were confirmed to suffer from meaning-altering translation distortions (e.g. named entity scrambling such as Mamata Banerjee $\to$ "fathers", Tejas train $\to$ "fasts", and negation drops), while 6 items represented verifier sensitivity or borderline nuances.
- **Artifacts:** Blinded sheets (`annotation/blinded_annotation_sample.csv`), individual submission files (`annotation_handoff/annotation_submission_Annotator_1.csv`, `annotation_handoff/annotation_submission_Annotator_2.csv`), and inter-rater agreement metrics (`annotation/HUMAN_ANNOTATION_REPORT.md`) are provided in full.

### Disclosure 2: Confirmatory Evaluation on Uninspected Claims
- **Status:** The test partition ($N=163$) was evaluated during initial exploratory research. While threshold $\tau^*$ was tuned strictly on dev, the test set has been previously inspected.
- **Guidance:** Findings are reported transparently as diagnostic evaluations on the held-out test split under observed distributions.

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
