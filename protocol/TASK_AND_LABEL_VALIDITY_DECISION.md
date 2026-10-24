# Protocol Decision: Task and Label Semantics Formulation

**Document Identifier:** `protocol/TASK_AND_LABEL_VALIDITY_DECISION.md`  
**Date:** 2026-10-19  
**Status:** APPROVED AND ADOPTED (Option C with Dual-F1 Reporting)  
**Related Audit:** `audit/DATA_AND_LABEL_AUDIT.md`, `audit/INDEPENDENT_REVIEW_FREEZE_CANDIDATE_V2.md`

---

## 1. Context and Problem Statement

The research project investigates cross-lingual retrieval-augmented claim verification for low-to-medium resource languages (specifically Hindi $\to$ English). Evidence is retrieved in Hindi, optionally machine-translated into English using MarianMT (`Helsinki-NLP/opus-mt-hi-en`), and verified against the claim using multilingual NLI (`MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`).

An independent audit (`audit/INDEPENDENT_REVIEW_FREEZE_CANDIDATE_V2.md`, Issue 1 [P0]) identified two critical semantic validity issues in the legacy evaluation setup:
1. **Semantic Incongruence in Label Mapping:** The dataset (derived from X-Fact, Gupta & Srikumar 2021) contains fact-checking veracity ratings (`false`, `mostly false`, `partly true/misleading`). Legacy code mapped `mostly false` and `false` to `CONTRADICTED`, but mapped `partly true/misleading` to `INSUFFICIENT_EVIDENCE`. In natural language inference (NLI) and fact verification (e.g., FEVER), "Insufficient Evidence" indicates that the retrieved evidence lacks the necessary factual assertions to confirm or refute the claim. In contrast, "partly true/misleading" indicates that evidence exists but presents a nuanced, mixed, or contextually altered truth value.
2. **Absence of Positive (`SUPPORTED`) Claims:** In the filtered Hindi evaluation split ($N_{\text{dev}}=103$, $N_{\text{test}}=163$), there are zero claims labelled `true` or `mostly true` by the fact-checkers. As a result:
   - **Dev set:** 89 `CONTRADICTED` (86.4%), 14 `INSUFFICIENT_EVIDENCE` (13.6%), 0 `SUPPORTED` (0.0%).
   - **Test set:** 142 `CONTRADICTED` (87.1%), 21 `INSUFFICIENT_EVIDENCE` (12.9%), 0 `SUPPORTED` (0.0%).

Claiming general "fact verification across all truth values" when evaluating exclusively on refutations and unverified claims is scientifically invalid without explicit scoping.

---

## 2. Examination of Raw X-Fact Data Schema

We inspected the raw dataset files (`data/raw/dev.all.tsv` and `data/raw/test.all.tsv`).
- **Data Source:** X-Fact (Gupta & Srikumar, ACL 2021), a multilingual fact-checking benchmark scraped from fact-checking websites (e.g., Aaj Tak, Vishwas News, Factly).
- **Raw Columns:** `language`, `site`, `claim`, `claim_date`, `review_date`, `label`, `url`, `evidence_1` ... `evidence_5`.
- **Observed Hindi Labels in Raw Data:**
  - `false`: Claim is demonstrably fabricated or false.
  - `mostly false`: Claim has a minor grain of truth but is substantially inaccurate.
  - `partly true/misleading`: Claim takes real facts out of context or conflates real and false claims.
- **Why Did Legacy Mapping Occur?**
  The original pipeline sought to project the task into a standard 3-class FEVER-style schema (`SUPPORTED`, `INSUFFICIENT_EVIDENCE`, `CONTRADICTED`) to interface with off-the-shelf NLI models. Because X-Fact does not contain explicit sentence-level entailment annotations, the legacy pipeline collapsed `false` / `mostly false` into `CONTRADICTED` and `partly true/misleading` into `INSUFFICIENT_EVIDENCE`.

---

## 3. Evaluation of Candidate Formulation Options

We evaluated three potential remedies:

### Option A: Retrain / Fine-tune Native Fact-Checking Veracity Head
- **Mechanism:** Train a lightweight linear classification head on top of mDeBERTa representations directly predicting the native X-Fact classes (`false`, `mostly false`, `partly true/misleading`).
- **Pros:** Preserves native fact-checking taxonomy without artificial NLI projection.
- **Cons:** Violates the zero-shot/few-shot research objective of the study; requires substantial training data; Hindi split has very small sample counts, leading to severe overfitting; shifts the research question from cross-lingual RAG routing to supervised classifier training.
- **Verdict:** REJECTED for the current scope.

### Option B: Human Claim-Evidence Entailment Annotation
- **Mechanism:** Collect dense bilingual human annotations judging true sentence-level NLI entailment between the claims and the scraped web snippets.
- **Pros:** Perfectly grounds the NLI formulation.
- **Cons:** Genuine bilingual human judgment cannot be fabricated by an AI agent. While we have prepared the blinded annotation packet, Gate C remains strictly `BLOCKED` until human annotators complete the study. Halting all computational analysis awaiting human completion would prevent resolving reproducible algorithmic fixes.
- **Verdict:** DEFERRED to human annotators (Gate C remains BLOCKED; annotation handoff packet prepared).

### Option C: Explicitly Scoped Cross-Lingual Claim Verification Benchmark (Adopted)
- **Mechanism:** Retain the deterministic inference pipeline but strictly and transparently redefine the benchmark scope:
  1. **Scoping Definition:** The benchmark measures *prediction sensitivity and cross-lingual translation routing disagreement* under the observed real-world distribution of fact-checked claims (predominantly false/misleading claims).
  2. **Dual-F1 Reporting:** All evaluations must report **both**:
     - **3-Class Macro F1:** Computed across all three nominal classes (`SUPPORTED`, `INSUFFICIENT_EVIDENCE`, `CONTRADICTED`). Because ground-truth `SUPPORTED` count is 0, recall for `SUPPORTED` is 0 by definition, penalizing false-positive supported predictions.
     - **2-Class Observed Macro F1:** Computed strictly over the observed non-empty classes (`CONTRADICTED` and `INSUFFICIENT_EVIDENCE`).
  3. **Runtime Model Verification:** Verify that the pretrained model logits strictly correspond to:
     - Logit 0: `entailment` $\to$ `SUPPORTED`
     - Logit 1: `neutral` $\to$ `INSUFFICIENT_EVIDENCE`
     - Logit 2: `contradiction` $\to$ `CONTRADICTED`
  4. **Claim Bounding:** The paper and all reports must explicitly disclaim general 3-class fact verification validity, stating clearly:
     *"The evaluation subset reflects real-world fact-checking intake in Hindi, which consists overwhelmingly of false and disputed claims (87.1% refutations, 12.9% partial/unverified). Consequently, findings quantify cross-lingual routing efficacy specifically for debunking and nuance detection, not affirmation of true claims."*
- **Verdict:** **ADOPTED AS CANONICAL PROTOCOL.**

---

## 4. Runtime Model Configuration Check

At runtime, the model `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7` was inspected directly via HuggingFace transformers:
```python
model = AutoModelForSequenceClassification.from_pretrained('MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7')
print(model.config.id2label)
# Output: {0: 'entailment', 1: 'neutral', 2: 'contradiction'}
print(model.config.label2id)
# Output: {'contradiction': 2, 'entailment': 0, 'neutral': 1}
```

The mapping is therefore verified:
- Index 0: `entailment` $\to$ `SUPPORTED`
- Index 1: `neutral` $\to$ `INSUFFICIENT_EVIDENCE`
- Index 2: `contradiction` $\to$ `CONTRADICTED`

---

5. System Architecture Scoping (Cross-Lingual Evidence Verification vs RAG)
The evaluated system consumes pre-retrieved evidence passages from fact-checking sources and evaluates cross-lingual translation routing alongside NLI verification. Because no dynamic retrieval index (e.g. BM25 / dense vector database) or generative large language model is part of the inference evaluation, the research scope and system are strictly classified as **Cross-Lingual Evidence Verification Under Translation Shift**, and references to full "Retrieval-Augmented Generation (RAG)" are disclaimed as aspirational rather than experimentally validated.

6. Evaluation Split Design: Exploratory Test Partition Status
The $N=163$ Hindi test split was evaluated in prior iterations (V1, V2). Although all threshold selection ($\tau^*$) is performed strictly on the $N=103$ development split without looking at test labels, repeated exposure of the test set across project revisions mandates classifying the current test evaluation as **EXPLORATORY / PREVIOUSLY INSPECTED**. Confirmatory claims of generalization are therefore not asserted.

---

## 7. Summary of Protocol Directives
1. `LABELS = ["SUPPORTED", "INSUFFICIENT_EVIDENCE", "CONTRADICTED"]`
2. All summary tables must include both `Macro_F1_3cl` and `Macro_F1_2cl`.
3. Threshold tuning on development data must optimize a pre-specified objective on development split only.
4. The system is classified as Cross-Lingual Evidence Verification, not end-to-end RAG.
5. The test set is designated as exploratory; selective routing findings are framed honestly as diagnostic rather than superior.
6. Gate A (Task and Label Definition) is marked **PASS** subject to these explicit bounds. Gate C remains **BLOCKED** awaiting human annotation.

