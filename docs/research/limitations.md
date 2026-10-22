# Methodological Limitations and Non-Supported Claims

**Project Title:** Cross-Lingual Evidence Verification: Prediction Sensitivity and Routing Disagreement Under Hindi-to-English Translation Shift  
**Protocol Version:** `v1.0-observational`  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  

---

## 1. Explicitly Non-Supported and Prohibited Claims

To uphold scientific integrity and prevent overclaiming, the following statements are explicitly declared **unsupported by the empirical evidence** and must not appear in any manuscript:

1. **NO END-TO-END RAG CLAIM:**
   - *Prohibited Statement:* "We evaluate a full cross-lingual Retrieval-Augmented Generation (RAG) system."
   - *Factual Reality:* This research evaluates pre-retrieved evidence snippets paired with claims. Neither the dense/sparse retriever nor an open-ended generator LLM was varied or evaluated in this study. The study investigates *cross-lingual evidence verification*.

2. **NO CAUSAL TRANSLATION ERROR ATTRIBUTION:**
   - *Prohibited Statement:* "Machine translation errors caused verifier errors," or "Semantic distortion explains 70% of prediction flips."
   - *Factual Reality:* Without authentic bilingual human annotations confirming semantic distortions in translation, all observed flips reflect *model prediction sensitivity* and *cross-lingual disagreement*. Model flips may stem from intrinsic multilingual tokenizer artifacts, cross-lingual representation shifts, or verifier noise rather than translation corruption. Causal claims remain blocked until Gate C is executed.

3. **NO CONFIRMATORY TEST SET GENERALIZATION:**
   - *Prohibited Statement:* "The test set provides an untouched, confirmatory evaluation of the selective cascade."
   - *Factual Reality:* The 163-item test split was inspected in previous project iterations. All test-set metrics must be characterized strictly as *exploratory* and *descriptive*.

4. **NO CLAIM OF CASCADE PARETO DOMINANCE:**
   - *Prohibited Statement:* "Selective verification achieves Pareto-optimal fact-checking performance."
   - *Factual Reality:* Under the prespecified linear development utility objective ($J = \text{MacroF1} - 0.15 \cdot \text{Coverage}$), the Translated-Only (No-Check) baseline achieves a higher development objective ($J = 0.2104$) than the cascade peak ($J = 0.2023$). Selective-Check is strictly the best *conditional* cascade configuration, not an unconstrained global optimum.

---

## 2. Structural and Dataset Limitations

1. **Missing Positive Class in X-Fact Hindi Split:**
   - The official Hindi partition of the X-Fact benchmark contains 142 `CONTRADICTED` and 21 `INSUFFICIENT_EVIDENCE` test examples, and **zero** gold `SUPPORTED` examples.
   - Consequently, true three-class classification cannot be evaluated on this split.
   - Accuracy is bounded above by a simple majority-class predictor (87.12%), and nominal three-class Macro-F1 contains an unavoidable zero-recall penalty ($F_{1,\text{SUP}} = 0.0$).
   - Accuracy and Macro-F1 numbers serve solely as *secondary proxy metrics* of task alignment.

2. **Single Language Pair:**
   - Experiments are currently limited to Hindi-to-English translation using MarianMT (`opus-mt-hi-en`) and mDeBERTa-v3 (`mDeBERTa-v3-base-xnli`).
   - Findings may not generalize to typologically distinct language families (e.g., East Asian or Semitic languages) or frontier LLM verifiers without independent verification.

3. **Pre-Retrieved Search Snippets:**
   - The evidence inputs consist of short, noisy search snippets scraped from professional fact-checking sites rather than full-length source documents.
   - Truncation boundaries and snippet incompleteness may introduce independent ambiguity.

4. **Hardware and Latency Measurement:**
   - Forward-pass latencies were measured on CPU hardware under single-instance batching. While relative latency ratios are informative (Selective-Check achieves a 59.2% reduction relative to Direct Multilingual), absolute latencies will differ on GPU/TPU accelerators or batched production servers.
