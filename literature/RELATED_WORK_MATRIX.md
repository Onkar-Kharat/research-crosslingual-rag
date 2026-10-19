# RELATED WORK COMPARISON MATRIX

**Date:** 2026-10-19  
**Auditor:** Autonomous Methodology & Verification Specialist

---

## 1. Feature-by-Feature Comparison Matrix

| Study | Target Task | Data Authenticity | Target Language Pair | Paired Original vs. Translated Pass | Error Attribution ($E_{\text{trans}}$ vs. $E_{\text{verif}}$) | Selective Escalation Cascade | Key Finding / Limitation Regarding Our Scope |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **Gupta & Srikumar (2021, X-Fact)** | Claim Verification | Authentic News Fact-Checks | 25 languages (inc. Hindi) | No | No | No | Established benchmark and raw data; evaluated monolingual & zero-shot transfer, but did not study translation pipelines. |
| **Thorne et al. (2018, FEVER)** | Claim Verification | Synthetic (Wikipedia) | English only | N/A | No | No | Foundational 3-class claim verification benchmark; purely monolingual English. |
| **Chang et al. (2023, XFEVER)** | Claim Verification | Synthetic (Wikipedia) | 6 languages (no Hindi) | Partial | No | No | Machine-translated FEVER claims; observed English-pivot calibration, but lacks authentic news noise and error decomposition. |
| **Shcharbakova et al. (2025)** | Claim Verification | Authentic News Fact-Checks | 25 languages (inc. Hindi) | No | No | No | Benchmarked encoders vs LLMs on X-Fact; showed encoders excel, but evaluated strictly direct multilingual text without translation. |
| **Singhal et al. (2024, arXiv:2410.10303)** | Claim Verification | Authentic News Fact-Checks | 15 languages (inc. Hindi) | **Yes** | **No** | **No** | **Closest prior work.** Evaluated pre-translation vs self-translation on X-Fact; showed accuracy drops, but treated error as monolithic and proposed no mitigation cascade. |
| **Liu et al. (2025, XRAG)** | Generative QA | News Articles | Multilingual | Partial (QA) | No | No | Benchmarked cross-lingual QA in RAG; identified language drift and reasoning bottlenecks in generative text, not veracity classification. |
| **Ranaldi et al. (2026, CrossRAG)** | Generative QA | Knowledge QA | Multilingual | No | No | No | Showed translating retrieved passages to English aids generative QA; assumed translation is universally positive, ignoring factual distortion. |
| **Our Study** | **Claim Verification** | **Authentic News Fact-Checks** | **Hindi $\rightarrow$ English** | **Yes** | **Yes (Disentangled)** | **Yes (Risk-Calibrated Cascade)** | **Quantifies operational error attribution separating translation-correlated flips from verifier reasoning failures, and evaluates a risk-calibrated fallback cascade to original source evidence under observed fact-checking distributions.** |

---

## 2. Key Synthesis of the Research Landscape

1. **The Generative QA vs. Discrete Verification Divide:**  
   Recent multilingual RAG studies (XRAG, CrossRAG, LAURA) focus exclusively on generative question answering. In generative QA, minor linguistic variations in translation are easily smoothed over by the decoder. In contrast, in discrete claim verification, a single flipped negation marker, mis-transliterated entity, or altered quantity completely inverts the ground-truth veracity verdict.
2. **The Monolithic Error Blindspot:**  
   Prior cross-lingual fact-checking work (Singhal et al., 2024; Chang et al., 2023) observed performance drops when using translation, but treated accuracy as a monolithic number. They did not answer: *when a pipeline fails, did the translation alter the facts, or did the model fail to reason?*
3. **The Unconditional Translation Fallacy:**  
   Engineering practices often assume translating non-English evidence into English is either universally beneficial (CrossRAG) or that naive dual-language averaging (Always-Check) solves ambiguity. Our study demonstrates that naive averaging degrades accuracy (to 31.29%), and that selective checking is required to avoid negative transfer.
