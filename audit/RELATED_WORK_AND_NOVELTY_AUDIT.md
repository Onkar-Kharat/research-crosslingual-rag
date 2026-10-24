# Related Work and Novelty Audit

**Project Title:** Cross-Lingual Evidence Verification: Prediction Sensitivity and Routing Disagreement Under Hindi-to-English Translation Shift  
**Audit Date:** 2026-10-24  
**Protocol Version:** `v1.0-observational`  

---

## 1. Domain-by-Domain Literature Analysis

This literature audit examines the boundaries of prior work across six relevant research areas, establishing the exact comparative contribution of this observational study.

### 1.1 Cross-Lingual Fact Verification
- **Foundational Works:**
  - *Gupta & Srikumar (ACL 2021)* introduced X-Fact, benchmarking mBERT and XLM-R on real-world fact-checking claims across 25 languages. Their findings established severe performance degradation in non-English languages but did not examine machine-translation evidence pipelines.
  - *Shcharbakova et al. (FEVER @ ACL 2025)* compared encoder-based verifiers (XLM-R) with large decoder-only models (Llama 3, Mistral) on X-Fact, finding that specialized encoders consistently outperform decoder LLMs on evidence utilization. However, they evaluated models strictly within native language inputs.
  - *Chang et al. (ROCLING 2023, XFEVER)* translated synthetic FEVER claims into six languages, focusing on prediction consistency between translated claims and English. Their claims were synthetic Wikipedia mutations rather than noisy real-world journalistic evidence.
- **Closest Direct Comparison:**
  - *Singhal et al. (ATTRIB @ NeurIPS 2024)* evaluated translation strategies (pre-translation vs. self-translation) on X-Fact across 15 languages using LLMs. While closest to our inquiry, they treated accuracy drops as monolithic black-box errors, did not measure verifier predictive uncertainty, did not decouple translation from verifier reasoning, and did not evaluate a selective consultation cascade.

### 1.2 Cross-Lingual and Multilingual RAG
- **Current Paradigms:**
  - *Liu et al. (Findings of EMNLP 2025, XRAG)* and *Ranaldi et al. (Findings of EACL 2026, CrossRAG)* demonstrated that translating non-English retrieved evidence into English significantly boosts downstream question answering by leveraging high-capacity English generators.
  - *Wang et al. (ACL 2026, LAURA)* identified severe English-favoring language bias in dense rerankers, addressing evidence retrieval distortion.
- **The Gap:** These studies focus strictly on open-domain generative QA, assuming translation is universally beneficial or evaluating retrieval recall. None evaluate veracity classification on pre-retrieved evidence snippets, and none analyze the prediction flip dynamics of NLI verifiers under translation shift.

### 1.3 Machine Translation Effects on Factuality and NLI
- *Karpinska & Iyyer (2023)* and *Zhou et al. (2022)* documented that standard neural machine translation (e.g., MarianMT / OPUS-MT) frequently introduces hallucinated entities, dropped numerical qualifiers, and negated clauses.
- **Our Distinction:** Rather than studying translation quality in isolation (BLEU/COMET), this project observes how MT transformations specifically alter downstream multilingual NLI verifier prediction states.

### 1.4 Selective Prediction and Verification Routing
- *Geifman & El-Yaniv (NeurIPS 2017)* and *Xin et al. (ACL 2021)* developed selective classification and early-exit cascades based on softmax predictive entropy.
- **Our Evaluation:** This study tests whether an uncertainty-gated cascade ($R(x) = 1.0 - \max_c P(c \mid x)$) can Pareto-dominate a Translated-Only verification baseline under Hindi-to-English translation shift. Our empirical finding is negative: under the linear utility objective, No-Check achieves higher development utility ($J=0.2104$) than the cascade peak ($J=0.2023$).

---

## 2. Comparison Table: Prior Art vs. This Study

| Dimension | X-Fact (Gupta 2021) | XFEVER (Chang 2023) | LLM Bias (Singhal 2024) | CrossRAG (Ranaldi 2026) | **This Study (2026)** |
|---|---|---|---|---|---|
| **Task** | Fact Checking | Synthetic Claim NLI | Claim Verification | Generative QA | **Paired Evidence Verification** |
| **Evidence Language** | Native Monolingual | Native Monolingual | Translated / Native | Translated into En | **Paired (Hi vs. Translated En)** |
| **Evaluation Focus** | Benchmark Accuracy | Cross-lingual Transfer | LLM Translation Bias | Generation BLEU/F1 | **Prediction Sensitivity & Disagreement** |
| **Noise Profile** | Journalistic Web Snippets | Synthetic Wikipedia | Journalistic Web Snippets | Clean QA Passages | **Authentic Journalistic Snippets** |
| **Cascade Routing** | No | No | No | No | **Evaluated (Selective vs. No-Check)** |
| **Error Decomposition**| None | None | Monolithic Accuracy | Generation Drift | **Formal Protocol & Tooling Built** |
| **Causal Claim** | None | None | Assumed Translation Bias | None | **Strictly Blocked Pending Human Data** |

---

## 3. Disentangling Prior Art, Contribution, and Unsupported Claims

### 3.1 Established Prior Work (What We Did Not Invent)
1. Multilingual fact verification on X-Fact (Gupta & Srikumar, 2021).
2. The finding that translating into English is common in multilingual retrieval systems (Liu et al., 2025; Ranaldi et al., 2026).
3. Softmax risk routing and selective classification (Geifman & El-Yaniv, 2017).
4. MarianMT translation models (`opus-mt-hi-en`) and mDeBERTa-v3 NLI checkpoints (`mDeBERTa-v3-base-xnli`).

### 3.2 The Specific Empirical Contribution
1. **Paired Sensitivity Quantification:** A controlled, paired evaluation demonstrating that presenting identical evidence snippets in machine-translated English versus original Hindi causes a 63.80% prediction disagreement rate in a modern multilingual verifier, including a 48.44% flip from `SUPPORTED` to `CONTRADICTED`.
2. **Negative Result on Cascade Pareto-Optimality:** An honest, reproducible demonstration that selective risk routing fails to achieve Pareto dominance over the Translated-Only (No-Check) baseline under the standard linear utility objective ($J_{\text{No-Check}} = 0.2104 > J_{\text{Cascade}} = 0.2023$).
3. **Rigorous Tooling for Human Verification:** Construction of a friction-free, offline, blinded human evaluation pipeline to enable genuine external bilingual evaluation without synthetic simulation.

### 3.3 Explicitly Unsupported Claims
1. **No "End-to-End RAG" Claim:** We evaluate pre-retrieved snippets paired with claims; no retriever or generative LLM was varied.
2. **No "Causal Translation Distortion" Claim:** We do not claim translation errors caused verifier errors because authentic bilingual human annotations are pending.
3. **No "First Cross-Lingual Cascade" Claim:** Cascaded routing is an established paradigm; our contribution is an empirical sensitivity and routing evaluation under Hindi–English translation shift.
