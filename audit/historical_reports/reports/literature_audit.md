# Literature Audit and Novelty Gate Report

**Date of Audit:** October 15, 2026  
**Auditor:** Autonomous NLP Research Assistant (Google DeepMind Antigravity)  
**Status:** Gate A Passed — Defensible Gap Confirmed (Go Decision)  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)

---

## 1. Executive Summary & Gate Decision

A systematic, reproducible literature audit was conducted across the ACL Anthology, arXiv, and web indexing engines to evaluate the state of the art in multilingual retrieval-augmented generation (RAG), cross-lingual claim verification, machine translation error propagation, and selective verification mechanisms. 

### Gate A Recommendation: **GO / PROCEED**
The proposed topic—**Separating Translation-Fidelity and Verifier-Reasoning Errors in Cross-Lingual RAG: A Controlled Study with Selective Original-Evidence Checking**—addresses an authentic, unresolved research gap that is scientifically defensible. Prior work either treats cross-lingual claim verification as a monolithic end-to-end classification task without disentangling whether failures arise in the evidence translation or in the verifier's reasoning (e.g., Singhal et al., 2024; Shcharbakova et al., 2025), or investigates multilingual RAG solely for open-domain QA generation rather than discrete veracity verification and selective checking (e.g., Liu et al., 2025; Ranaldi et al., 2026; Wang et al., 2026).

---

## 2. Audit Methodology and Search Protocol

Searches were conducted on October 15, 2026 across primary bibliographic databases. All queries, filters, and yield statistics were recorded in `logs/search_log.csv` and synthesized in `logs/literature_matrix.csv`.

### Search Queries Executed:
1. `XRAG: Cross-lingual Retrieval-Augmented Generation` (ACL Anthology: EMNLP Findings 2025)
2. `Multilingual Retrieval-Augmented Generation for Knowledge-Intensive Question Answering Task` (ACL Anthology: EACL Findings 2026)
3. `All Languages Matter: Understanding and Mitigating Language Bias in Multilingual RAG` (ACL Anthology: ACL 2026 Long Papers)
4. `A Comparative Study of Translation Bias and Accuracy in Multilingual Large Language Models for Cross-Language Claim Verification` (arXiv:2410.10303)
5. `When Scale Meets Diversity: Evaluating Language Models on Fine-Grained Multilingual Claim Verification` (ACL Anthology: FEVER 2025)
6. `XFEVER: Exploring Fact Verification across Languages` (arXiv:2310.16278)
7. `X-FACT: A New Benchmark Dataset for Multilingual Fact Checking` (ACL Anthology: ACL-IJCNLP 2021)
8. Multi-term exploratory queries:
   - `"cross-lingual" "claim verification" OR "fact verification" "translation" "error"`
   - `"selective verification" OR "verification cascade" "fact checking" OR "claim verification"`

---

## 3. Systematic Nearest-Neighbor Overlap Analysis

We evaluated each closely related paper against the three core components of our proposed study:
- **Component 1 (Controlled Paired Evidence):** Exact same claim and evidence item evaluated in original source language vs. translated form.
- **Component 2 (Error Disentanglement):** Systematic taxonomy-based error attribution distinguishing meaning-altering translation flaws (negation, numerical, entity) from verifier reasoning errors on meaning-preserved evidence.
- **Component 3 (Selective Checking):** Confidence/risk-triggered verification cascade to original evidence with empirical coverage-cost-accuracy trade-offs against no-check and always-check baselines.

| Paper | Venue / Year | Comp 1 (Paired Evidence) | Comp 2 (Error Attribution) | Comp 3 (Selective Checking) | Overlap Assessment & Limitations |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Liu et al. (XRAG)** | EMNLP Findings 2025 | Partial (QA) | No | No | Benchmarks QA generation across languages; uncovers language confusion and cross-lingual reasoning issues in QA, but does not address fact verification, label flips, or selective checking. |
| **Ranaldi et al. (CrossRAG)** | EACL Findings 2026 | Partial (QA) | No | No | Evaluates translating retrieved documents to English for multilingual QA; finds English translation improves QA, but treats translation as universally positive and does not analyze translation-induced factual distortions or verification cascades. |
| **Wang et al. (LAURA)** | ACL 2026 | No | No | No | Identifies language bias at the *retrieval/reranking* stage of multilingual RAG; addresses retriever alignment, not downstream evidence translation or verifier reasoning. |
| **Singhal et al.** | arXiv:2410.10303 (2024) | Yes (Claims) | **No** | **No** | **Closest prior work.** Evaluates pre-translation and self-translation on X-Fact (15 languages). Demonstrates accuracy drops in low-resource languages, but treats verification accuracy as monolithic: does not isolate whether wrong predictions stem from MT fidelity errors or model reasoning failures; no selective verification mechanism proposed. |
| **Shcharbakova et al.** | FEVER 2025 | No | No | No | Comprehensive benchmark comparing XLM-R and LLMs on X-Fact; finds encoder models excel and LLMs suffer from evidence utilization issues, but does not study cross-lingual evidence translation or error attribution. |
| **Yamagishi Lab (XFEVER)** | arXiv:2310.16278 (2023) | Yes (FEVER) | No | No | Evaluates cross-lingual transfer on translated synthetic FEVER claims and Wikipedia evidence; lacks authentic real-world news noise and does not provide selective checking cascades. |
| **Gupta & Srikumar (X-Fact)** | ACL-IJCNLP 2021 | Baseline data | No | No | Establishes the multilingual benchmark dataset (25 languages) with authentic claims and search snippets; does not perform controlled translation fidelity experiments or verification cascades. |

---

## 4. Defensible Research Gap and Formulation

### The Identified Gap:
In cross-lingual retrieval-augmented claim verification, practitioners frequently translate retrieved foreign evidence into a shared pivot language (e.g., English) before submitting it to a high-capacity verifier model. While this pipeline leverages powerful English reasoning capabilities, it introduces two distinct, competing sources of failure:
1. **Translation-Fidelity Failure ($E_{\text{trans}}$):** The machine translation system distorts claim-critical factual information (such as flipping negation, altering numbers/quantities, confusing named entities, or omitting vital qualifiers).
2. **Verifier-Reasoning Failure ($E_{\text{verif}}$):** The machine translation accurately preserves the claim-relevant semantics, but the verifier model fails to correctly reason over the premises, suffering from hallucination, prior bias, or contextual confusion.

**Critical Problem in Existing Literature:** Prior studies observe performance drops in translated pipelines but conflate $E_{\text{trans}}$ and $E_{\text{verif}}$ into an undifferentiated error rate. Consequently, it remains unknown:
- What percentage of verification errors are truly caused by translation corruption versus verifier reasoning shortcomings?
- Can an automated risk/uncertainty trigger detect high-risk translated evidence and selectively consult the original source evidence to recover accuracy without incurring the latency and cost of always checking original text?

### Refined Research Questions (RQs):
- **RQ1 (Label Sensitivity under Translation):** How frequently does a verifier's veracity decision flip when provided with original evidence versus machine-translated evidence across identical claim-evidence pairs?
- **RQ2 (Disentangled Error Attribution):** What proportion of observed verification errors are attributable to (a) meaning-altering translation distortions, (b) verifier reasoning failures despite faithful translation, or (c) ambiguous/insufficient original evidence? Which semantic error categories (e.g., polarity, quantities, entities) are most detrimental?
- **RQ3 (Selective Original-Evidence Verification):** Does a selective verification cascade—which inspects the translated evidence and routes only uncertain or high-risk cases to original-evidence checking—achieve a superior accuracy-cost trade-off compared to static `No-Check` and `Always-Check` baselines?

---

## 5. Dataset Selection and Feasibility Checks

To ground the empirical investigation in verified, non-synthetic evidence, we examine candidate benchmarks:

1. **X-Fact (Gupta & Srikumar, ACL-IJCNLP 2021):**
   - **Status:** Recommended and Selected.
   - **License:** Open MIT License (`utahnlp/x-fact`).
   - **Language Support:** Includes English and Hindi (our primary target language pair), along with 23 other languages.
   - **Authenticity:** Contains naturally occurring claims investigated by professional fact-checkers, paired with actual retrieved search snippets and multi-class veracity ratings.
   - **License & Ethics:** Fully permissible for non-commercial and commercial research, reproducible, and verifiable.

2. **XFEVER (2023):**
   - Synthetic entity mutations derived from Wikipedia; rejected as primary data because it lacks real-world journalistic nuance and search snippet noise.

---

## 6. Novelty Gate Conclusion

The research questions are verified to be distinct from prior work. We conclude that Gate A is successfully passed with an evidence-backed **GO** decision. The project will now proceed to Phase 2: Experimental Design, Dataset Acquisition, and Protocol Formalization.
