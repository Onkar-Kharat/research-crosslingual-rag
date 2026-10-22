# Research Scope Specification

**Title:** Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Status:** `FROZEN — EXPLORATORY COMPUTATIONAL STUDY`  

---

## 1. Core Research Question

In retrieval-augmented verification pipelines operating across languages, practitioners must choose how to represent retrieved foreign-language evidence before scoring:
1. Translate foreign evidence into an English pivot representation (*No-Check / Translated-Only*), or
2. Evaluate foreign evidence directly in its native representation (*Direct Multilingual*).

This study investigates:
> **Primary Question:** To what extent do veracity predictions from a multilingual natural language inference verifier disagree when evaluating identical real-world claims against original Hindi evidence versus machine-translated English evidence?
>
> **Secondary Diagnostic Question:** Can a lightweight risk trigger (combining verifier predictive uncertainty and numeral overlap) selectively identify disagreement-prone instances, and how does this selective policy compare to unconditional dual-evidence checking?

---

## 2. In-Scope Boundaries

- **Language Pair:** Hindi (`hi`) source evidence $\to$ English (`en`) machine translation.
- **Task:** 3-class claim verification (Supported, Contradicted, Insufficient Evidence).
- **Benchmark:** X-Fact Hindi partition (Gupta & Srikumar, 2021).
  - Development Split: $N=103$ (calibration and threshold tuning).
  - Test Split: $N=163$ (diagnostic evaluation of sensitivity).
- **Models:**
  - Machine Translation: `Helsinki-NLP/opus-mt-hi-en` (MarianMT, 74M params).
  - Cross-Lingual Verifier: `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7` (278M params).
- **Experimental Conditions:**
  1. *No-Check (Translated Only)*: Evaluates machine-translated evidence $e_{\text{trans}}$.
  2. *Direct Multilingual (Original Only)*: Evaluates original Hindi evidence $e_{\text{orig}}$.
  3. *Always-Check (Dual Consensus)*: Averages class posterior distributions from both representations.
  4. *Selective-Check*: Cascades to original evidence if risk score $R(e_{\text{trans}}, c) \ge \tau^* = 0.650$.
  5. *Controls & Ablations*: 100-seed random routing control, numeral-only trigger, uncertainty-only trigger.

---

## 3. Explicit Out-of-Scope Boundaries

1. **End-to-End RAG Systems:** Upstream dense/sparse retrieval and downstream generative answer synthesis are not evaluated. Evidence snippets are evaluated as pre-retrieved pairs.
2. **Causal Translation Quality Claims:** Without bilingual human annotation, prediction shifts cannot be definitively attributed to semantic distortion or translation bugs. They are analyzed strictly as observational model prediction sensitivity.
3. **Multilingual Generalizability:** Claims of universality across other languages, models, or domains are excluded.
4. **Confirmatory Holdout Testing:** The test set was inspected during exploratory computational work; findings are reported transparently as descriptive and diagnostic.
