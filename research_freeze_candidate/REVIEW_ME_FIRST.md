# REVIEW ME FIRST: INDEPENDENT REVIEWER HANDOFF GUIDE

**Target Reviewer:** Independent Peer Reviewer (ChatGPT / TACL Reviewer)  
**Research Subject:** Cross-Lingual Evidence-Grounded Claim Verification (Hindi $\rightarrow$ English)  
**Dataset:** X-Fact Hindi Subset ($N=266$ authentic fact-checks: 103 dev, 163 held-out test)  
**Current Research Status:** **NOT FROZEN — BLOCKED ON HUMAN ANNOTATION (GATE C)**

---

## 1. Executive Summary of the Project

This research investigates automated claim verification when non-English evidence (Hindi) is translated into English before being evaluated by a high-capacity cross-lingual natural language inference verifier (`mDeBERTa-v3-base-xnli`). 

The central objectives are:
1. **Diagnostic Error Attribution:** Measuring what proportion of pipeline failures stem from **translation-fidelity corruptions** ($E_{\text{trans}}$, where MT distorts factual primitives like numbers, entities, or negation) versus **verifier-reasoning failures** ($E_{\text{verif}}$, where MT preserves meaning but the model deduces the wrong stance).
2. **Consensus & Cascade Dynamics:** Evaluating whether unconditional dual-language consensus (`Always-Check`, averaging translated and original posterior probabilities) helps or hurts, and whether an automated risk trigger can selectively route uncertain claims back to original Hindi evidence (`Selective-Check`).

---

## 2. Research Freeze Decision & Gate Status

In strict accordance with scientific integrity guidelines, this package is explicitly marked **NOT FROZEN**:

- **Gate A (Data Validity & Integrity):** **PASS**
- **Gate B (Defensible Novelty & Bounded Question):** **PASS**
- **Gate C (Protocol & Annotation Readiness):** **BLOCKED** — Operational classification of 41 translation errors requires bilingual human validation. Synthetic or AI-generated human labels were strictly prohibited. The blinded 50-item annotation sheet is delivered in `annotation/blinded_annotation_sample.csv`.
- **Gate D (Experimental Evidence & Tests):** **PASS** — All 12 unit and regression tests pass; metrics derive directly from raw predictions.
- **Gate E (Reproducibility):** **BLOCKED** — Dependent on Gate C.

---

## 3. Five Critical Findings from the Independent Audit

When reviewing this package, please note the key corrections made during the independent audit:

1. **The Missing Positive Class in Authentic Fact-Checks:**  
   Authentic Hindi news claims in X-Fact exclusively debunk misinformation (87.1% `CONTRADICTED`, 12.9% `INSUFFICIENT_EVIDENCE`). There are **zero (0) gold `SUPPORTED` claims** in the entire benchmark. The initial project draft reported a 3-class Macro-F1 which artificially penalized scores due to a constant 0.0 score for the missing class. Both observed 2-class and standard 3-class metrics are now reported side-by-side.
2. **Point Estimate Recomputations:**  
   The prior report exported bootstrap sample means (e.g., 0.320184) under the `Accuracy` header. Recomputations establish the exact observed sample accuracies:
   - No-Check (Translated): **31.90%** (52/163)
   - Direct Multilingual (Original): **37.42%** (61/163)
   - Always-Check (Dual Consensus): **31.29%** (51/163)
   - Selective-Check (Cascade): **39.26%** (64/163)
3. **Disentangling the Error Attribution Overlap (114 vs. 111):**  
   The prior claim of $41 + 61 + 12 = 114$ errors out of 111 total failures was caused by double-counting 3 items (`xfact-hi-test-0009`, `0023`, `0036`) where gold was `INSUFFICIENT_EVIDENCE` and original evidence fixed the translation error. The clean, mutually exclusive partition is **41 translation-recovered + 61 verifier reasoning + 9 unrecovered insufficient = 111 total errors (100.0%)**.
4. **Declared Method vs. Code Execution:**  
   The initial manuscript text stated that Selective-Check "averages posterior distributions" upon trigger. The code executed hard routing to original evidence. Our ablations proved that posterior averaging on triggered claims drops accuracy to **30.67%**, whereas hard routing achieves **39.26%**. The paper text was reconciled to declare hard routing.
5. **Statistical Significance Realities:**  
   Selective-Check is statistically significantly better than naive consensus `Always-Check` ($p = 0.0294$, McNemar test), proving that naive consensus causes negative transfer. However, Selective-Check is **not** statistically significantly better than `Direct Multilingual` alone ($p = 0.6072$, gaining only 3 items out of 163). Selective-Check should be framed as an **efficiency and fallback safeguard for English-centric pipelines**, not a replacement for native multilingual processing.

---

## 4. Key Files for the Reviewer to Inspect

| Priority | File Path | Content and Purpose |
|:---:|:---|:---|
| **1** | `RESEARCH_STATUS.md` | Full gate-by-gate pass/fail determination and blockers |
| **2** | `DECISION_LOG.md` | Chronological record of all 8 methodological and audit decisions |
| **3** | `audit/PAPER_CODE_RECONCILIATION.csv` | Line-by-line audit of 15 claims in the paper against code and raw data |
| **4** | `audit/RESULTS_REPRODUCTION_REPORT.md` | Complete recomputed tables, confusion matrices, and statistical tests |
| **5** | `audit/DATA_AND_LABEL_AUDIT.md` | Forensic analysis of X-Fact Hindi, provenance, and label distributions |
| **6** | `literature/NOVELTY_ASSESSMENT.md` | Defensible contribution boundaries vs. Singhal et al. (arXiv:2410.10303) |
| **7** | `protocol/RESEARCH_PROTOCOL_v1.md` | Formal experimental protocol, hypotheses, and stopping rules |
| **8** | `annotation/blinded_annotation_sample.csv` | 50-item blinded sample awaiting human adjudication |
| **9** | `tests/TEST_REPORT.md` | Verification report of the automated test suite (12/12 passing) |

---

## 5. What Remains Needed Before the Manuscript Phase
1. Supply annotations from two bilingual Hindi-English annotators for the 50 items in `annotation/blinded_annotation_sample.csv`.
2. Run `python scripts/analyze_human_annotations.py` to verify whether $\ge 70\%$ of operational $E_{\text{trans}}$ cases represent true meaning-altering translation corruptions.
3. Once Gate C passes, proceed to the official manuscript revision and TACL formatting phase.
