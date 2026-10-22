# Novelty Assessment and Literature Positioning

**Title:** Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Status:** `FROZEN — EXPLORATORY COMPUTATIONAL STUDY`  

---

## 1. Prior Work Comparison Matrix

| Prior Work | Task | Language Setting | Method / Architecture | Evaluation Design | Relationship to This Study | Key Remaining Distinction |
|---|---|---|---|---|---|---|
| **Liu et al. (EMNLP 2025 Findings)** [*XRAG*] | Open-domain generative QA | Cross-lingual (ar, zh, de, es, en) | LLM RAG with mono- and multilingual retrieval | QA Accuracy, language drift metrics | Studies cross-lingual retrieval and generation bottlenecks | Focuses on open-ended text generation; does not evaluate discrete veracity classification or directional prediction transitions. |
| **Ranaldi et al. (EACL 2026 Findings)** [*CrossRAG*] | Knowledge-intensive QA | Multilingual (MKQA, MLQA, XOR-TyDi) | CrossRAG: Translate retrieved passages to English pivot | F1, Exact Match on QA spans | Proposes translating foreign passages into English pivot | Treats translation as universally beneficial for generation; omits discrete fact-checking and does not measure verifier sensitivity. |
| **Wang et al. (ACL 2026)** [*All Languages Matter*] | Multilingual document retrieval | Multilingual (mMARCO, MIRACL) | Dense multilingual document reranking | MRR@10, nDCG@10 | Identifies language bias in multilingual retrievers | Investigates upstream retrieval representation bias; does not evaluate downstream evidence verification. |
| **Shcharbakova et al. (FEVER 2025)** | Multilingual claim verification | 25 languages (X-Fact) | XLM-RoBERTa vs. 7B--12B LLMs | Macro-F1 across 25 language splits | Evaluates multilingual encoders on X-Fact claims | Treats evidence language as fixed; does not compare paired original vs. machine-translated evidence representations. |
| **Singhal et al. (NLP4PI 2024)** | Multilingual fact-checking | Multilingual subset of X-Fact | Few-shot prompting of multilingual LLMs | Veracity classification accuracy | Observes that MT translation reduces accuracy in low-resource settings | Treats verification error as monolithic; does not decompose into directional transition matrices or evaluate selective fallback cascades. |
| **Geifman & El-Yaniv (NeurIPS 2017, ICML 2019)** | Selective classification / Abstention | Monolingual vision/text | Softmax thresholding & SelectiveNet | Risk-Coverage tradeoff curves | Theoretical foundation for reject-option inference | Formulates generic rejection; does not study cross-lingual evidence switching or translation risk gating. |

---

## 2. What Is Already Known

1. Multilingual RAG systems experience cross-lingual semantic drift and language inconsistency during open-ended generation (Liu et al., 2025; Ranaldi et al., 2026).
2. Upstream dense retrievers exhibit severe linguistic bias toward high-resource English documents (Wang et al., 2026).
3. Specialized multilingual encoder models (e.g., mDeBERTa, XLM-RoBERTa) consistently outperform 7B--12B parameter autoregressive LLMs on fine-grained multilingual claim verification due to superior evidence grounding (Shcharbakova et al., 2025).
4. Machine translation can silently corrupt factual primitives (negations, numbers, named entities), degrading downstream classification (Singhal et al., 2024).

---

## 3. What This Study Adds (Empirical Diagnostic Contribution)

1. **Controlled Paired Sensitivity Characterization:** Provides an empirical paired evaluation on authentic Hindi claims ($N=163$), holding the claim, evidence snippets, verifier model, and decoding fixed while varying only evidence language representation (original Hindi vs. machine-translated English).
2. **Empirical $3 \times 3$ Transition Matrix:** Documents a 63.80% prediction disagreement rate, revealing that 48.44% of translated `SUPPORTED` predictions flip to `CONTRADICTED` when evaluated on original Hindi evidence.
3. **Disentangled Outcome Strata:** Separates translated failures ($N=117$) into cases recovered by original Hindi evidence ($S_{\text{trans}}=51$, 43.59%) and cases failing across both languages ($S_{\text{verif}}=66$, 56.41%), while showing that original Hindi evidence degrades 27 instances ($S_{\text{degraded}}$) that translated text classified correctly.
4. **Critical Evaluation of Selective Routing:** Demonstrates that while a risk trigger ($\tau^*=0.650$) achieves identical accuracy (28.22%) with 7.98% coverage (saving 59.2% latency vs. Direct Multilingual), it does not achieve global Pareto dominance over the translated baseline on development utility ($J=0.2104$ vs. $0.2023$).
5. **Rigorous Disclosure of Class Imbalance & Statistical Asymmetry:** Transparently documents the total absence of gold `SUPPORTED` instances (87.12% `CONTRADICTED`, 12.88% `INSUFFICIENT`) and demonstrates why accuracy differences reach statistical significance under McNemar's test ($p=0.008772$ and $p=0.005583$) while class-balanced Macro-F1 permutation tests do not ($p=0.1898$ and $p=0.1180$).

---

## 4. What Remains Unproven & Threats to Novelty

- **Causal Attribution:** Without completed bilingual human annotations, prediction flips cannot be proven to result from translation distortion rather than tokenizer/model inductive biases.
- **Limited Scope:** Evaluated on one language pair (Hindi $\to$ English), one MT model (MarianMT), one verifier (mDeBERTa-v3), and pre-retrieved snippets.
- **Modest Algorithmic Complexity:** The selective cascade trigger combines maximum softmax probability and numeral overlap; it is an empirical diagnostic probe rather than a fundamentally new machine learning architecture.
- **Positioning:** This work is positioned strictly as a disciplined, reproducible empirical study providing diagnostic insight into verifier sensitivity and benchmark limitations for cross-lingual verification.
