# REVIEWER HANDOFF: Remaining Scientific Limitations

**Project:** Cross-Lingual Evidence Verification  
**Audit Date:** October 2026  
**Document Purpose:** Explicit disclosure of what this study cannot and does not establish.  

---

Even after comprehensive data cleaning, code refactoring, statistical reconciliation, and test verification, the following boundaries strictly define what this study **cannot** claim:

## 1. No Causal Claim of Translation Error Attribution
- **Limitation:** While the verifier predictions change on 63.80% of test instances under translation, and while 36.9% of errors (41/111) can be recovered by consulting the original Hindi, **we cannot causally assert that translation infidelity caused the verifier's errors**.
- **Reason:** Model predictions may flip due to cross-lingual embedding space misalignments, tokenizer artifacts, or intrinsic verifier sensitivity, rather than factual errors in machine translation.
- **Evidentiary Boundary:** Authentic bilingual human validation (Gate C) is required to establish causal error attribution. Gate C remains pending. All findings are strictly framed as observational computational prediction sensitivity.

---

## 2. No Confirmatory Virgin Test Set Claim
- **Limitation:** The 163-item Hindi test set from X-Fact was evaluated and inspected in earlier exploratory rounds (v1-v3) before the final $\tau^* = 0.650$ protocol was locked.
- **Reason:** Even though $\tau^* = 0.650$ was tuned strictly on the 103 development items without exposure to test labels, the test set cannot be presented as an uninspected, clean-room confirmatory benchmark.
- **Evidentiary Boundary:** The test set evaluation is explicitly designated as **EXPLORATORY / PREVIOUSLY INSPECTED**.

---

## 3. Absence of Gold `SUPPORTED` Class in the Benchmark
- **Limitation:** In the official X-Fact Hindi partition, there are **0 gold `SUPPORTED` instances** (Dev: 89 `CONTRADICTED`, 14 `INSUFFICIENT`; Test: 142 `CONTRADICTED`, 21 `INSUFFICIENT`).
- **Reason:** Authentic Indian journalistic fact-checking organizations exclusively publish articles debunking false rumors and viral misinformation; verified factual truths are not published as debunking articles.
- **Evidentiary Boundary:** True 3-class classification performance cannot be fully evaluated. A trivial majority predictor achieves 87.12% accuracy. Macro-F1 across 3 classes contains an uninformative $F_1(\text{SUPPORTED}) = 0.0$ penalty. Accuracy and Macro-F1 must be treated as secondary proxy metrics.

---

## 4. Single Language Pair and Model Scope
- **Limitation:** The empirical experiments are restricted to **Hindi-to-English translation** using MarianMT (`Helsinki-NLP/opus-mt-hi-en`) and mDeBERTa-v3 (`MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`).
- **Reason:** Hindi represents an Indo-Aryan language with moderate resource availability in MT.
- **Evidentiary Boundary:** Results cannot be assumed to generalize directly to low-resource languages, typologically distant families (e.g., Dravidian, East Asian, or Semitic), or decoder-only frontier LLMs (e.g., GPT-4, Llama 3) without independent experimental replication.

---

## 5. Evidence-Grounded Verification vs. Full-Pipeline RAG
- **Limitation:** This research evaluates pre-retrieved Google search snippets from X-Fact.
- **Reason:** Neither the dense/sparse passage retriever nor open-ended generation was varied or evaluated in this study.
- **Evidentiary Boundary:** This study evaluates **Evidence-Grounded Cross-Lingual Claim Verification**, not end-to-end Retrieval-Augmented Generation (RAG).
