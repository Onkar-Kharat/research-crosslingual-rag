# TACL Contribution and Readiness Decision

**Document ID:** `CONTRIBUTION_AND_READINESS_DECISION.md`  
**Decision Date:** 2026-10-24  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Evaluator Personas:** TACL Action Editor & Skeptical Review Panel  
**Authoritative Revision Workspace:** `manuscript_revision_tacl/`  
**Current Research Phase:** `FROZEN — EXPLORATORY COMPUTATIONAL STUDY`  

---

## 1. Direct Answers to Core Editorial Questions

### 1. What is the single central contribution?
The single central contribution of this work is an **empirical and diagnostic characterization of verifier prediction sensitivity under Hindi-to-English translation shift in pre-retrieved cross-lingual evidence verification**. The paper establishes that translating non-English evidence to English—a ubiquitous design choice in cross-lingual NLP pipelines—induces massive prediction instability ($63.80\%$ disagreement rate) and asymmetric semantic distortion ($48.44\%$ of claims supported by original Hindi evidence flip to contradictory when translated into English), demonstrating that direct multilingual verification significantly outperforms pivot translation verification ($42.94\%$ vs. $28.22\%$, $p = 0.008772$).

### 2. What is the strongest claim that the existing evidence supports?
> **Strongest Defensible Claim:**  
> On the evaluated X-Fact Hindi fact verification benchmark ($N=163$), cross-lingual evidence verification using fine-tuned `mDeBERTa-v3` exhibits severe observational sensitivity to translation pivot representations, where native Hindi evidence yields statistically superior accuracy over MarianMT translated English ($+14.72\%$, McNemar $p < 0.01$). Furthermore, naive posterior averaging (*Always-Check*) suffers from error contamination (dropping accuracy to $36.81\%$), and surface risk triggers (maximum softmax probability and numeral overlap) fail to reliably calibrate selective routing, causing selective consultation to match the translation baseline ($28.22\%$) without significant Macro-F1 improvement ($p = 0.118$).

### 3. What is the most likely major reviewer objection?
> **Primary Objection:**  
> *"The study is conducted on a single language pair (Hindi–English), on a single moderate-sized benchmark partition ($N=163$), using a single MT engine (MarianMT) and a single verifier (`mDeBERTa-v3`). Most critically, the test partition contains 0.0% gold \textsc{Supported} instances, rendering the evaluation of true positive entailment uninformative. Additionally, the error attribution taxonomy ($S_{\text{trans}}, S_{\text{verif}}, S_{\text{degraded}}$) has not been validated by bilingual human annotators. Therefore, the findings represent an exploratory diagnostic report rather than a comprehensive, generalizable journal contribution."*

### 4. Is the current contribution potentially appropriate for TACL?
**Yes, but strictly as a rigorous, bounded empirical/diagnostic study**, provided the authors:
1. Do not claim universality across all languages or end-to-end RAG systems.
2. Disclose the missing gold \textsc{Supported} class candidly and report both 3-class and 2-class Macro-F1.
3. Explicitly present the cascade evaluation as a diagnostic negative result on surface risk gating.
4. Transparently characterize the study as an observational computational study with pending human validation.

### 5. Which weaknesses can be fixed through better writing, reporting, or citation verification?
- Narrowing all claims to match the exact experimental scope.
- Mathematically formulating the missing positive class and its deflation of Macro-F1.
- Explaining the statistical divergence between significant McNemar accuracy and non-significant permutation Macro-F1.
- Framing the selective cascade as an insightful negative result on calibration under distribution shift.
- Standardizing tables, citations, and figures with zero visual overlaps and full mathematical rigor.

### 6. Which weaknesses cannot be resolved without new data, annotation, or experiments?
- **Absence of Additional Languages:** Evaluating other low/medium-resource language pairs (e.g., Bengali, Tamil, Swahili, Arabic) cannot be done under frozen results.
- **Absence of Additional MT/LLM Verifiers:** Evaluating modern LLMs (e.g., LLaMA-3, GPT-4) or commercial MT APIs cannot be done under frozen results.
- **Completed Bilingual Human Annotation:** Human evaluation packets are prepared, but actual manual ratings cannot be fabricated or completed without authorized human annotators.
- **Absence of Gold \textsc{Supported} Instances:** The missing class is an inherent benchmark artifact of X-Fact Hindi test partition and cannot be changed without collecting new annotated claims.

---

## 2. Authoritative Readiness Decision

Based on the frozen empirical evidence, the formal editorial decision is:

$$\mathbf{BORDERLINE \text{ --- } SUBSTANTIAL\ SCIENTIFIC\ LIMITATIONS}$$

### Editorial Justification
- **Why not "NOT READY FOR TACL"?**  
  The core findings are genuine, surprising, and methodologically sound. A $63.80\%$ disagreement rate and $48.44\%$ directional flip rate under standard MarianMT + mDeBERTa-v3 directly challenge widespread assumptions in multilingual RAG. The statistical testing is paired, non-parametric, and rigorous. All artifacts are 100% reproducible with zero data leakage.
- **Why not "PROMISING — EDITORIAL STRENGTHENING REQUIRED"?**  
  Editorial strengthening alone *cannot* add additional language pairs, generate missing gold positive examples, or substitute for completed bilingual human annotation. A paper with $N=163$ on a single language pair with zero positive examples faces substantial skepticism at TACL as a full archival journal article.
- **Action Editor Recommendation:**  
  The manuscript should be positioned explicitly as an **"Exploratory Computational Study"** and **"Empirical Diagnosis"**. If submitted to TACL with complete candor regarding its scope and limitations, it has a viable path to a Revise & Resubmit (Category C) or Conditional Acceptance (Category B) if the Action Editor values deep, honest empirical investigation of common architectural failures over inflated benchmark claims. Alternatively, if TACL reviewers demand multi-language validation, the paper is exceptionally well-suited for EMNLP/ACL Findings or a specialized venue such as *Transactions on Asian and Low-Resource Language Information Processing (TALLIP)*.
