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

## Decision 8 (2026-10-19): Research Freeze Decision (NOT FROZEN)
- **Context:** Specifying the freeze status for Gate C and Gate E. Antigravity is prohibited from fabricating human judgments, and true causal claims distinguishing translation-fidelity from verifier reasoning require bilingual human verification.
- **Decision:** Declare the research **NOT FROZEN** at Gate C. Deliver the complete reproducibility package, blinded annotation sheet (`annotation/blinded_annotation_sample.csv`), and analysis script for human completion.
- **Alternatives Considered:** Marking the package frozen to satisfy a routine completion urge (strictly prohibited by Master Prompt).
- **Consequence:** Absolute scientific integrity maintained. Package named `CROSS_LINGUAL_RAG_RESEARCH_FREEZE_CANDIDATE_NOT_FROZEN.zip`.
