# Bibliography and In-Text Citation Audit

**Audit Date:** 2026-10-24  
**Audit Scope:** 100% verification of all in-text citations and BibTeX entries in `manuscript_revision_tacl/`  
**Verification Sources:** ACL Anthology, NeurIPS Proceedings, IEEE/ACM Digital Library, Springer, Political Analysis, arXiv  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  

---

## 1. Citation Audit Summary

- **Total BibTeX Entries in `references.bib`:** 15
- **Total In-Text Cited Keys in `.tex` Files:** 15
- **Missing Keys (Cited but absent in BibTeX):** 0
- **Uncited Keys (In BibTeX but unreferenced):** 0
- **Citation Parity Ratio:** 100.0% (15 / 15)
- **Status:** `100% VERIFIED & RESOLVED`

---

## 2. Itemized Citation Verification Registry

| Citation Key | Full Title | Authors | Venue & Year | Verification Source / URL / DOI | Manuscript Claim Supported | Audit Status |
|:---|:---|:---|:---|:---|:---|:---:|
| `liu-etal-2025-xrag` | XRAG: Cross-lingual Retrieval-Augmented Generation | W. Liu, S. Trenous, L. F. R. Ribeiro, B. Byrne, F. Hieber | Findings of EMNLP 2025 | ACL Anthology (`2025.findings-emnlp.849`) | Multilingual RAG formulation and generative language drift | `VERIFIED` |
| `ranaldi-etal-2026-multilingual` | Multilingual Retrieval-Augmented Generation for Knowledge-Intensive Question Answering Task | L. Ranaldi, B. Haddow, A. Birch | Findings of EACL 2026 | ACL Anthology (`2026.findings-eacl.35`) | CrossRAG translate-then-generate pipeline assumption | `VERIFIED` |
| `wang-etal-2026-languages` | All Languages Matter: Understanding and Mitigating Language Bias in Multilingual RAG | D. Wang, G. Mo, Y. Shi, C. Zhang, B. Zheng, et al. | ACL 2026 | ACL Anthology (`2026.acl-long.338`) | Language bias in dense multilingual retrievers/rerankers | `VERIFIED` |
| `gupta-srikumar-2021-xfact` | X-FACT: A New Benchmark Dataset for Multilingual Fact Checking | A. Gupta, V. Srikumar | ACL-IJCNLP 2021 | ACL Anthology (`2021.acl-short.86`, DOI: 10.18653/v1/2021.acl-short.86) | Authentic multilingual fact-checking dataset provenance | `VERIFIED` |
| `shcharbakova-etal-2025-scale` | When Scale Meets Diversity: Evaluating Language Models on Fine-Grained Multilingual Claim Verification | H. Shcharbakova, T. Anikina, N. Skachkova, J. van Genabith | FEVER Workshop 2025 | ACL Anthology (`2025.fever-1.1`) | Encoder NLI verifiers outperforming 7B-12B LLMs on X-Fact | `VERIFIED` |
| `singhal-etal-2024-comparative` | Multilingual Fact-Checking using LLMs | A. Singhal, T. Law, C. Kassner, A. Gupta, E. Duan, et al. | NLP4PI Workshop 2024 | ACL Anthology (`2024.nlp4pi-1.2`) | Monolithic translation accuracy degradation observations | `VERIFIED` |
| `tiedemann-thottingal-2020-opus` | OPUS-MT — Building open translation services for the World | J. Tiedemann, S. Thottingal | EAMT 2020 | ACL Anthology (`2020.eamt-1.61`) | MarianMT Hindi-to-English translation backbone specification | `VERIFIED` |
| `he-etal-2021-deberta` | DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing | P. He, J. Gao, W. Chen | arXiv 2021 | arXiv:2111.09543 | Disentangled attention encoder backbone architecture | `VERIFIED` |
| `laurer-etal-2024-less` | Less Annotating, More Classifying — Addressing the Data Scarcity Problem with Zero-Shot Classification and NLI | M. Laurer, W. van Atteveldt, A. Salleras Casas, K. Welbers | Political Analysis 2024 | Cambridge Univ Press (DOI: 10.1017/pan.2023.20) | Fine-tuned 2.7M composite NLI verifier checkpoint | `VERIFIED` |
| `thorne-etal-2018-fever` | FEVER: a large-scale dataset for Fact Extraction and VERification | J. Thorne, A. Vlachos, C. Christodoulopoulos, A. Mittal | NAACL-HLT 2018 | ACL Anthology (`N18-1074`, DOI: 10.18653/v1/N18-1074) | Canonical 3-way fact verification task formulation | `VERIFIED` |
| `lewis-etal-2020-rag` | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, et al. | NeurIPS 2020 | NeurIPS Proceedings (Vol 33, pp. 9459-9474) | Foundational retrieval-augmented generation framework | `VERIFIED` |
| `conneau-etal-2020-unsupervised` | Unsupervised Cross-lingual Representation Learning at Scale | A. Conneau, K. Khandelwal, N. Goyal, V. Chaudhary, et al. | ACL 2020 | ACL Anthology (`2020.acl-main.747`, DOI: 10.18653/v1/2020.acl-main.747) | Multilingual masked pre-training and XNLI evaluation | `VERIFIED` |
| `geifman-elyaniv-2017-selective` | Selective Classification for Deep Neural Networks | Y. Geifman, R. El-Yaniv | NeurIPS 2017 | NeurIPS Proceedings (Vol 30, pp. 4878-4887) | Selective prediction risk-coverage tradeoff theory | `VERIFIED` |
| `benjamini-hochberg-1995` | Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing | Y. Benjamini, Y. Hochberg | JRSS Series B 1995 | Wiley / JSTOR (DOI: 10.1111/j.2517-6161.1995.tb02031.x) | False Discovery Rate (FDR) Benjamini-Hochberg procedure | `VERIFIED` |
| `mcnemar-1947` | Note on the sampling error of the difference between correlated proportions or percentages | Q. McNemar | Psychometrika 1947 | Springer (DOI: 10.1007/BF02295996) | McNemar paired 2x2 contingency test for correlated binary data | `VERIFIED` |

---

## 3. Formatting and Quality Verification

1. **Title Capitalization:** Proper nouns and acronyms (e.g., `{XRAG}`, `{RAG}`, `{FEVER}`, `{X-FACT}`, `{LLM}s`, `{OPUS-MT}`, `{DeBERTaV3}`, `{ELECTRA}`) are protected with braces `{...}` to prevent unwanted down-casing by BibTeX style files.
2. **Special Characters:** Diacritics and accented characters (e.g., J{\"o}rg, Guzm{\'a}n, K{\"u}ttler) use standard TeX escape sequences.
3. **DOIs and URLs:** All entries provide verified open-access URLs to ACL Anthology or official DOI resolvers.
