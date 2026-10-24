# Simulated Mock TACL Reviews

**Document ID:** `MOCK_TACL_REVIEWS.md`  
**Review Date:** 2026-10-24  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Manuscript Title:** Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Disclaimer:** These are rigorous adversarial mock reviews simulating the critical perspective of expert TACL reviewers and an Action Editor. They are used internally to evaluate scientific strengths and vulnerabilities and do not represent actual TACL decisions.

---

## Reviewer 1: Novelty, Literature Grounding, and Scientific Significance

### 1. Summary of Contribution
This paper investigates the sensitivity of an automated evidence verification model (`mDeBERTa-v3`) when assessing Hindi claims against pre-retrieved evidence represented either in original Hindi ($e_{\text{orig}}$) or translated into English ($e_{\text{trans}}$) via MarianMT. The authors report that the verifier switches its prediction in $63.80\%$ of cases, with $48.44\%$ of claims supported in Hindi flipping to contradictory in translated English. Direct multilingual verification outperforms translation pivot verification ($42.94\%$ vs. $28.22\%$, McNemar $p = 0.0088$). An unconditional dual-representation ensemble (*Always-Check*) underperforms direct verification ($36.81\%$), which the authors attribute to "error contamination." A selective risk-gated cascade (*Selective-Check*) triggers on $8.0\%$ of queries but fails to statistically outperform the translation baseline on Macro-F1 ($p = 0.118$).

### 2. Strengths
- **Clear, Narrow Empirical Problem:** The paper isolates the verification step in cross-lingual factuality pipelines, avoiding the confounding effects of retrieval recall present in end-to-end RAG papers.
- **Strong Diagnostic Value:** The high disagreement rate ($63.80\%$) and the finding that unconditional consensus fails due to error contamination provide valuable empirical warnings against naive multi-representation ensembling.
- **Methodological Transparency:** The paper is unusually candid about negative results: it openly discloses that the selective cascade failed to beat the baseline on development tuning and that Macro-F1 differences are statistically non-significant.

### 3. Major Concerns
1. **Narrow Scope & Generalizability:** The study evaluates only a single language pair (Hindi–English), a single MT model (MarianMT), and a single verifier (`mDeBERTa-v3-base`). Without testing other language families (e.g., Arabic, Swahili, Chinese) or modern LLMs (e.g., LLaMA-3, GPT-4), it is unclear whether this sensitivity is a fundamental property of cross-lingual NLI or merely an artifact of this specific MT-verifier pairing.
2. **Novelty of the Translation Shift Phenomenon:** Machine translation error propagation is well known in multilingual NLP. The paper needs to better articulate what theoretical or generalizable insight emerges beyond confirming that translation degrades downstream NLI predictions.
3. **Overclaiming Potential:** Any suggestion that this work evaluates "RAG systems" in general must be strongly curtailed, as the experiments evaluate classification over pre-retrieved snippets, not interactive or end-to-end retrieval-generation pipelines.

### 4. Minor Concerns
- The literature review should more explicitly contrast this work with CrossRAG (Zhang et al., 2024) and XRAG (Wang et al., 2024).
- The distinction between observational sensitivity and causal attribution should be sharpened in the discussion.

### 5. Questions for Authors
- Would the same directional flip rate (Supported $\to$ Contradicted) be observed if a stronger commercial MT system (e.g., Google Translate) were used?
- Why did the authors choose MarianMT rather than a modern multilingual LLM for translation?

### 6. Required Revisions
- Restrict all claims strictly to an exploratory observational characterization of pre-retrieved evidence verification under Hindi-to-English translation shift.
- Expand the limitations section to explicitly emphasize the single-language, single-model boundary.

### 7. Final Recommendation
**Score:** Borderline (Tend toward Rejection / Encouragement to Revise as an Empirical Diagnosis).

---

## Reviewer 2: Technical Soundness, Methodology, and Statistics

### 1. Summary of Contribution
The paper provides a paired empirical evaluation of four verification conditions (No-Check, Direct Multilingual, Always-Check, and Selective-Check) on the X-Fact Hindi partition ($N=163$ test, $N=103$ dev). It conducts paired McNemar tests on accuracy and non-parametric prediction-swap permutation tests on Macro-F1.

### 2. Strengths
- **Reproducibility & Rigor:** The experimental pipeline is deterministic, with fixed seeds ($B=5,000$, seed 42) and verified statistical test implementations.
- **Paired Experimental Design:** Evaluating identical claims and retrieved snippets across conditions eliminates query selection bias.
- **Disjoint Diagnostic Partitioning:** The 4-way stratification ($S_{\text{trans}}=51, S_{\text{verif}}=66, S_{\text{degraded}}=27, \text{Concordant}=19$) provides a clean accounting of instances.

### 3. Major Concerns
1. **Extreme Class Imbalance (Missing Gold Positive Class):** The test set ($N=163$) contains 142 Contradictions, 21 Neutrals, and **0 Supported** instances. This is a severe limitation:
   - The verifier's ability to correctly verify true positive claims is completely untested in the ground truth.
   - Any prediction of \textsc{Supported} is mathematically penalized as a false positive.
   - 3-class Macro-F1 is inherently depressed because $F_{1,\text{sup}} \equiv 0.0$.
2. **Divergence Between Significance Tests:** McNemar's test on accuracy indicates significance ($p = 0.0088$), whereas the permutation test on Macro-F1 is non-significant ($p = 0.1898$ vs No-Check, $p = 0.1180$ vs Selective). The paper must explain why this divergence occurs without appearing to rely exclusively on the metric that achieved $p < 0.05$.
3. **Absence of Completed Human Bilingual Validation:** The error taxonomy ($S_{\text{trans}}, S_{\text{verif}}, S_{\text{degraded}}$) relies on automated model predictions against gold labels. Without human bilingual verification confirming whether MarianMT actually corrupted semantic entities in each specific instance, the taxonomy remains computational, not causally proven.

### 4. Minor Concerns
- The development set sample size ($N=103$) is relatively small for calibrating a multi-component risk threshold ($\tau, \lambda_{\text{num}}$).
- Table 4 should report both raw and FDR-adjusted p-values for all pairwise comparisons.

### 5. Questions for Authors
- How did the authors handle the zero true-positive class when calculating precision and recall for \textsc{Supported}?
- Is the lack of gold \textsc{Supported} instances a property of the X-Fact Hindi scraping methodology, or an artifact of fact-checking real-world disinformation?

### 6. Required Revisions
- Explicitly disclose the zero-support class in the abstract, methodology, and limitations.
- Report observed 2-class Macro-F1 ($\frac{3}{2}\text{Macro-F1}_3$) alongside 3-class Macro-F1.
- Clearly state that error strata represent computational outcome categories, pending bilingual human verification.

### 7. Final Recommendation
**Score:** Borderline (Acceptance subject to major clarifying revisions regarding class imbalance and statistical divergence).

---

## Reviewer 3: Overall TACL Suitability and Action Editor Perspective

### 1. Summary of Contribution
The paper tackles a timely and relevant question in cross-lingual NLP: whether translating non-English evidence to English for automated verification helps or harms performance. Through rigorous paired evaluation on X-Fact Hindi, it demonstrates that translation pivot verification causes substantial error and that direct native verification is superior.

### 2. Strengths
- **Excellent Writing & Presentation:** The manuscript is exceptionally well structured, with clear math, beautiful collision-free vector figures, and flawless TACL formatting.
- **Intellectual Honesty:** The authors avoid the temptation to overclaim, explicitly highlighting negative results regarding consensus averaging and selective cascades.
- **Relevance to TACL Scope:** Falls squarely within TACL's interest in foundational multilingual NLP, cross-lingual representation, and empirical evaluation methodology.

### 3. Major Concerns
1. **Journal-Level Archival Weight:** TACL typically expects broad, definitive studies with multi-benchmark, multi-lingual, and multi-model evaluations. An $N=163$ study on one language pair and one model family feels closer to an outstanding conference short paper or focused workshop paper than a definitive journal milestone.
2. **Failure of Proposed Method:** The proposed *Selective-Check* method does not beat the baseline. While negative results are valuable, the paper must be carefully framed so that the negative result is viewed as an illuminating empirical finding about calibration failure, rather than an uncompleted method.

### 4. Minor Concerns
- Ensure that the anonymous review version strictly omits all author-identifying details in text, citations, and PDF metadata.

### 5. Final Recommendation
**Action Editor Synthesis:**  
The paper is scientifically sound, reproducible, and addresses a genuine problem with surprising empirical data. However, due to its single-pair scope, missing positive class, and lack of human annotation, it cannot be accepted as-is (Category A) or with minor revisions (Category B).  
**Recommended TACL Decision:** **Category (c) — Rejection with Encouragement to Revise and Resubmit**, OR **Category (b) — Conditional Acceptance** if framed strictly as an *Exploratory Empirical Diagnosis* with full limitation disclosures.
