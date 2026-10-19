# LITERATURE SEARCH PROTOCOL

**Date of Execution:** 2026-10-19  
**Auditor:** Autonomous Methodology & Verification Specialist  
**Topic Scope:** Cross-lingual claim verification, multilingual retrieval-augmented generation, machine translation fidelity in NLI, and selective verification cascades.

---

## 1. Primary Databases and Indexes Queried
1. **ACL Anthology** (`aclanthology.org`): Primary venue for computational linguistics (ACL, EMNLP, EACL, NAACL, Findings, and Workshops).
2. **arXiv.org** (`cs.CL`, `cs.AI`, `cs.LG`): Preprints and workshop submissions.
3. **Crossref & Semantic Scholar**: DOI resolution and citation graphs.
4. **Google Scholar & Web Indexing**: Verified authoritative bibliographic records.

---

## 2. Formal Query Strings Executed

| Query ID | Search String | Primary Target Database | Objective |
|:---|:---|:---|:---|
| **Q1** | `"A Comparative Study of Translation Bias and Accuracy in Multilingual Large Language Models for Cross-Language Claim Verification"` | arXiv, Google Scholar | Verify exact metadata, authorship, and findings of Singhal et al. (arXiv:2410.10303) |
| **Q2** | `"XFEVER: Exploring Fact Verification across Languages"` | ACL Anthology, arXiv | Verify Chang et al. (arXiv:2310.16278), dataset structure, and cross-lingual baselines |
| **Q3** | `"XRAG: Cross-lingual Retrieval-Augmented Generation"` | ACL Anthology, arXiv | Verify Liu et al. (arXiv:2505.10089, Findings of EMNLP 2025) benchmark |
| **Q4** | `"All Languages Matter: Understanding and Mitigating Language Bias in Multilingual RAG"` | ACL Anthology, arXiv | Verify Wang et al. (ACL 2026) reranker debiasing |
| **Q5** | `"Multilingual Retrieval-Augmented Generation for Knowledge-Intensive Question Answering Task"` OR `"CrossRAG"` | ACL Anthology | Verify Ranaldi et al. (Findings of EACL 2026) translation approach |
| **Q6** | `"When Scale Meets Diversity: Evaluating Language Models on Fine-Grained Multilingual Claim Verification"` | ACL Anthology | Verify Shcharbakova et al. (FEVER Workshop 2025) X-Fact evaluation |
| **Q7** | `"selective verification" OR "selective prediction" "claim verification" OR "fact checking"` | ACL Anthology, arXiv | Assess prior work on confidence-gated cascades in fact verification |
| **Q8** | `"translation fidelity" "natural language inference" OR "claim verification"` | ACL Anthology, arXiv | Assess prior work on separating MT corruption from NLI reasoning failures |

---

## 3. Inclusion and Exclusion Criteria

### Inclusion Criteria:
- Papers addressing cross-lingual or multilingual claim verification, fact-checking, or evidence-grounded NLI.
- Papers analyzing the impact of machine translation on downstream semantic reasoning or retrieval-augmented generation.
- Papers formalizing selective inference, cascades, or routing between multiple evidence languages or model representations.
- Papers published in peer-reviewed venues (ACL, EMNLP, EACL, NAACL, NeurIPS) or released on arXiv through October 2026.

### Exclusion Criteria:
- Monolingual English-only RAG pipelines with no cross-lingual component.
- Fact-checking studies focusing strictly on political analysis without algorithmic or empirical NLP evaluation.
- Pure machine translation papers with no downstream task evaluation.

---

## 4. Search Coverage Limits & Disclosures
Searches were conducted up to October 19, 2026. Full papers and proceedings were reviewed for all primary nearest neighbors. No automated claims of "first" or "novel" are made without explicit nearest-neighbor bounding.
