# FORMAL DECISION LOG: RESEARCH IMPROVEMENT AND AUDIT

**Target Repository:** `research-crosslingual-rag`  
**Auditor / Specialist:** Autonomous Methodology & Verification Specialist  
**Specification:** `ANTIGRAVITY_RESEARCH_IMPROVEMENT_AND_FREEZE_PROMPT.md`

---

## Decision 1 (2026-10-19): Safe Intake and Branch Isolation
- **Context:** The original research project contained committed LaTeX manuscripts, PDF figures, experiment logs, and raw prediction files on branch `main`.
- **Decision:** Isolate all improvement, audit, and recomputation work on a dedicated Git branch `research-improvement-v2` derived from `30b489a`. Keep original artifacts strictly immutable.
- **Alternatives Considered:** Directly overwriting files on `main` (rejected: violates reproducibility and audit preservation rules).
- **Consequence:** Full auditability is preserved; all original files remain intact in `audit/extracted_original/` for side-by-side comparison.

---

## Decision 2 (2026-10-19): Point Estimate Reporting Standard
- **Context:** The previous result table (`test_main_results.csv`) reported bootstrap sample means (e.g., 0.320184) under the `Accuracy` column header instead of direct observed sample accuracy ($52/163 = 0.319018$).
- **Decision:** All point estimates in official audit reports and tables must reflect the exact observed sample proportion $k / N$. Bootstrap resampling must be restricted strictly to confidence interval estimation ($B = 2,000$).
- **Alternatives Considered:** Retaining bootstrap mean as a Bayesian posterior proxy (rejected: contradicts empirical reporting standards and confuses readers).
- **Consequence:** Recomputed tables now reflect exact observed values (0.3190, 0.3742, 0.3129, 0.3926).

---

## Decision 3 (2026-10-19): Handling Missing Positive Class in Ground Truth
- **Context:** An independent audit of raw X-Fact Hindi partitions revealed that authentic fact-checks in India exclusively target false/misleading rumors (`false`, `mostly false`, `partly true/misleading`). Validated positive claims (`true`, `mostly true`) are 0.0% in both Dev ($0/103$) and Test ($0/163$).
- **Decision:** Report both:
  1. Standard 3-class Macro-F1 (with explicit disclosure that $F_1(\textsc{Supported}) = 0.0$ due to null support), and
  2. Observed 2-class Macro-F1 (evaluating only the classes actually present: `CONTRADICTED` and `INSUFFICIENT_EVIDENCE`).
- **Alternatives Considered:** Synthesizing true claims by scraping Wikipedia or using LLM generation (rejected: destroys data authenticity and introduces synthetic artifacts).
- **Consequence:** Eliminates misleading 3-class reporting without corrupting the authentic journalistic nature of the benchmark.

---

## Decision 4 (2026-10-19): Resolving Error Attribution Overlap (114 vs. 111 Errors)
- **Context:** The prior report claimed $41 + 61 + 12 = 114$ errors out of 111 total errors. A case-by-case audit revealed that 3 items (`xfact-hi-test-0009`, `0023`, `0036`) with $y^* = \textsc{Insufficient}$ were double-counted in both $E_{\text{trans}}$ (because original fixed translation) and $E_{\text{insuff}}$ (because gold was insufficient).
- **Decision:** Formalize a strictly disjoint and exhaustive 3-part partition of the 111 errors:
  - $E_{\text{trans}}$ (Recovered by original): **41 cases** (38 contradicted, 3 insufficient)
  - $E_{\text{verif}}$ (Reasoner error on contradicted): **61 cases**
  - $E_{\text{insuff}}$ (Unresolved insufficiency where both fail): **9 cases**
  - Disjoint sum: $41 + 61 + 9 = 111$ (100.0%).
- **Alternatives Considered:** Arbitrarily dropping the 3 items (rejected: unscientific deletion of valid data).
- **Consequence:** Error taxonomy sums to 100% of failures with complete mathematical integrity.

---

## Decision 5 (2026-10-19): Method Reconciliation (Hard Routing vs. Posterior Averaging)
- **Context:** Manuscript text in Section 4.3 claimed that Selective-Check "averages the posterior distributions" upon trigger. The code actually executed hard routing (`np.where(triggered, pred_original, pred_translated)`).
- **Decision:** Formally define the primary method as **Risk-Calibrated Hard Routing** and preserve **Triggered Posterior Averaging** as an explicit ablation.
- **Evidence:** We proved empirically that triggered posterior averaging reduces accuracy to **30.67%** (worse than No-Check), whereas hard routing achieves **39.26%**.
- **Consequence:** Method description in technical documentation matches code execution, and the failure of posterior averaging is highlighted as a scientific finding (negative transfer).

---

## Decision 6 (2026-10-19): True Jaccard Numeral Overlap Implementation
- **Context:** The code implemented directional recall $|A \cap B| / |A|$, whereas the paper described Jaccard similarity $|A \cap B| / |A \cup B|$.
- **Decision:** Upgrade the feature extraction to True Jaccard similarity.
- **Evidence:** Evaluation showed that while 10 items had altered overlap scores due to extraneous translated numbers, at $\tau^* = 0.30$, exactly zero routing decisions flipped on the test set, proving the cascade's robustness to the metric formulation.
- **Consequence:** Methodological alignment restored.

---

## Decision 7 (2026-10-19): Fair End-to-End Latency Accounting
- **Context:** Prior latency figures only reported verifier forward pass time, omitting the neural machine translation step (MarianMT on CPU).
- **Decision:** Report both verifier inference latency and end-to-end pipeline latency (including estimated 1,120 ms MT generation time per translated claim).
- **Consequence:** Full computational transparency.

---

## Decision 8 (2026-10-19): Candidate V2 Critical Repairs
- **Context:** Resolving initial audit findings on path portability, label mapping construct validity, and 16 passing tests.
- **Decision:** Repaired paths, documented label mapping limitations, and verified literature citations.

## Decision 9 (2026-10-19): Invalidation and Quarantine of Synthetic Human Annotations (P0)
- **Context:** An independent code audit revealed that `scripts/perform_bilingual_annotation.py` simulated two bilingual annotators with a hardcoded Python dictionary of 50 item judgments and adjudicated consensus, falsely reporting 96.0% raw agreement and Cohen's kappa 0.911.
- **Decision:** Invalidate all simulated annotation outputs as scientific evidence. Quarantine the script, submissions, and report under `audit/invalidated_synthetic_annotations/` with SHA256 checksums. Strip all active blinded sheets to stimulus columns only. Keep Gate C strictly **BLOCKED** and the project **NOT FROZEN** until genuine human evaluators complete the protocol.
- **Alternatives Considered:** Fabricating replacement labels or accepting simulated data (strictly prohibited by scientific integrity rules).
- **Consequence:** Research validity restored; Gate C remains blocked awaiting real human provenance.

## Decision 10 (2026-10-19): Direct MT-Verifier Coupling, Mechanical Dev Tuning, and Honest Scope Bounding
- **Context:** The inference script timed MarianMT into `_` but verified cached JSONL text; reports stated $\tau^*=0.300$ while dev tuning chose $\tau^*=0.650$; random routing used a single seed; the title claimed "RAG" without a retriever.
- **Decision:** 
  1. Rebuild inference: decode exact MarianMT output, verify that exact string with mDeBERTa, and compute numeral Jaccard on generated text.
  2. Tune $\tau^*$ strictly on dev data under objective $J(\tau) = \text{Macro\_F1}_{3cl} - 0.15 \cdot \text{Coverage}$ and assert `selective_triggered == (risk_score >= tau_star)`.
  3. Implement 100-seed random routing control with exact matched item counts.
  4. Classify test split as exploratory/previously inspected and bound claims: Selective-Check is not superior to Translated-Only ($p=1.000$) and trails Original-Only and Always-Check.
  5. Remove "RAG" from title/scope; classify system as Cross-Lingual Evidence Verification Under Translation Shift.
  6. Deliver versioned archive `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_V4_NOT_FROZEN.zip` with clean-room extraction test.

---

## Decision 11 (2026-10-19): Final One-Pass Research Freeze under Option C (Observational Scope)
- **Specification:** `FINAL_ONE_PASS_RESEARCH_FREEZE_PROMPT.md`
- **Context:** To eliminate recursive status report rewrites and scope drift, the research scope was formally locked to Option C: "Cross-lingual verifier prediction sensitivity and routing disagreement under Hindi-to-English translation shift."
- **Key Actions & Findings:**
  1. **Option C Adoption:** Quarantined synthetic data remains strictly excluded. Human annotation is marked as "not performed / future work" and is not required for this computational scope. All causal claims ("translation caused X errors") are excluded.
  2. **Baseline Fairness on Dev Utility:** Recomputation of development tuning under $J = \text{Macro\_F1}_{3cl} - 0.15 \cdot \text{Coverage}$ demonstrated that the No-Check baseline ($Coverage=0, J=0.2104$) outperforms all cascade thresholds ($\tau=0.650, J=0.2023$). Selective cascade routing is honestly reported as not Pareto-optimal on development data.
  3. **Canonical Results Directory:** Created `experiments/results_canonical/` with full predictions, metrics, 100-seed controls, statistical tests, publication figures, and `RUN_MANIFEST.json`.
  4. **Status Harmonization:** Unified `FREEZE_GATE_REPORT.md` as the single authoritative source of truth, eliminating all contradictory status claims.
  5. **Final Freeze Certification:** Labeled project `RESEARCH FROZEN — EXPLORATORY SCOPE`. Packaged final versioned archive `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_V5_FROZEN_EXPLORATORY.zip`.

---

## Decision 12 (2026-10-22): Real Human Annotation Workflow and Master Freeze Refinement
- **Specification:** `ANTIGRAVITY_FINAL_VALUES_AND_HUMAN_ANNOTATION_WORKFLOW_PROMPT.md`
- **Context:** While the computational study was frozen, a practical, zero-friction workflow was required for qualified bilingual human evaluators to independently annotate the 50-item sample without synthetic data, telemetry, or external dependencies.
- **Key Actions & Findings:**
  1. **Primary Descriptive Outcomes Formalized:** Quantified paired prediction agreement (36.20% [29.22%, 43.81%]) and label-flip disagreement (63.80% [56.19%, 70.78%]) on test instances as primary descriptive outcomes.
  2. **Human Annotation Workflow Engineered:** Created `annotation_tool/` containing an offline single-page HTML5/JS interface (`index.html`), two randomized independent blinded packets (`packet_A.json` and `packet_B.json` with opaque IDs `OPQ-A-01..50` and `OPQ-B-01..50`), automated submission validator (`validate_submissions.py`), and pre-specified agreement script (`analyze_agreement.py`).
  3. **Strict Integrity Maintained:** Zero synthetic human judgments created. Synthetic data remains quarantined. Real human evaluation is marked pending external recruitment.
  4. **Status Certification:** Certified project as `COMPUTATIONAL RESULTS FROZEN — EXPLORATORY; HUMAN ANNOTATION PENDING`. Packaged deliverable archive `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip`.


