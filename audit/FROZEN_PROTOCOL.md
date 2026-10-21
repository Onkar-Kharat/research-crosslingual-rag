# Frozen Experimental Protocol: Cross-Lingual Evidence Verification

**Working Title:** Cross-Lingual Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Protocol Version:** `v1.0-observational`  
**Status:** **FROZEN (COMPUTATIONAL STUDY FROZEN — HUMAN VALIDATION PENDING)**  
**Date:** 2026-10-24  

---

## 1. Central Research Question and Hypotheses

### 1.1 Central Research Question
How do evidence-language conditions (original Hindi vs. machine-translated English) affect the prediction sensitivity and routing behavior of a multilingual NLI verifier on pre-retrieved evidence snippets, and does a prespecified uncertainty-based verification routing strategy improve the quality–latency trade-off compared with appropriate computational baselines?

### 1.2 Prespecified Hypotheses & Acceptance Criteria

- **Hypothesis 1 (Translation Sensitivity):** Presenting evidence in machine-translated English rather than original Hindi induces substantial prediction disagreement ($\text{Disagreement} > 20\%$) and systematic directional label flipping.
  - *Acceptance Criterion:* Two-sided Wilson 95% confidence interval for paired disagreement rate strictly exceeds 20.0%.
  - *Outcome:* **ACCEPTED**. Observed disagreement is 63.80% [95% CI: 56.19%, 70.78%].
- **Hypothesis 2 (Cascade Utility Superiority):** An uncertainty-routed selective cascade ($\tau^*$) achieves superior development utility compared to a Translated-Only (No-Check) baseline under the prespecified linear objective $J(\tau) = \text{MacroF1}_{\text{dev}}(\tau) - \lambda \cdot \text{Coverage}_{\text{dev}}(\tau)$.
  - *Acceptance Criterion:* $\Delta J = J(\tau^*) - J(\text{No-Check}) > 0.0$ on the development split.
  - *Outcome:* **REJECTED (Negative Result)**. Dev No-Check achieves $J = 0.2104$, while Cascade peak achieves $J = 0.2023$ ($\Delta J = -0.0081$). The cascade does not Pareto-dominate the No-Check baseline.
- **Hypothesis 3 (Selective vs. Full Verification Latency):** Selective-Check achieves statistically significant latency reduction compared to Always-Check and Direct Multilingual verification while preserving accuracy.
  - *Acceptance Criterion:* Paired latency reduction $> 50\%$ with no significant degradation in accuracy ($p > 0.05$ on McNemar test).
  - *Outcome:* **PARTIALLY SUPPORTED**. Mean latency is reduced from 11,295.6 ms (Direct Multi) to 4,613.8 ms (Selective-Check) (59.2% reduction). However, Direct Multilingual achieves significantly higher proxy accuracy (42.94% vs. 28.22%, McNemar $p = 0.0056$).
- **Hypothesis 4 (Causal Translation Distortion):** Verifier prediction flips are predominantly caused by semantic distortion introduced by machine translation rather than intrinsic multilingual verifier sensitivity.
  - *Acceptance Criterion:* Authentic independent bilingual human annotations confirm that $\ge 70\%$ of discordant cases exhibit substantive translation fidelity distortion (`ALTERED`).
  - *Outcome:* **BLOCKED / PENDING**. Authentic human annotations have not yet been collected. Zero causal error claims may be made until Gate C is executed.

---

## 2. Experimental Data & Unit of Analysis

- **Dataset Source:** X-Fact multilingual fact verification dataset (`hi` partition) (Gupta & Srikumar, 2021).
- **Unit of Analysis:** Individual Claim-Evidence Snippet pair $(C_i^{\text{hi}}, E_i^{\text{hi}})$.
- **Splits:**
  - Development Split: 103 instances (used exclusively for threshold tuning and objective evaluation).
  - Test Split: 163 instances (evaluated once with fixed parameters as an exploratory benchmark).
- **Inclusion / Exclusion Rules:** All instances in the official X-Fact Hindi partition with non-empty claim and evidence fields are included. Zero synthetic examples are introduced.
- **Label Mapping Definition:**
  - Real-world veracity ratings (`mostly false`, `false`) map to `CONTRADICTED`.
  - Ratings (`partly true/misleading`) map to `INSUFFICIENT_EVIDENCE`.
  - Gold `SUPPORTED` is entirely absent in the Hindi partition ($N=0$). Consequently, all classification accuracy and macro-F1 metrics are secondary proxy measures of task alignment.

---

## 3. Models and Pipelines

1. **Multilingual NLI Verifier:**
   - Model: `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`.
   - Classes: `SUPPORTED` (0), `INSUFFICIENT_EVIDENCE` / `NEUTRAL` (1), `CONTRADICTED` (2).
   - Sequence Length: Strict maximum of 512 tokens with native tokenizer truncation.
2. **Machine Translation Engine:**
   - Model: `Helsinki-NLP/opus-mt-hi-en` (MarianMT).
   - Direct Coupling: The exact generated translation is fed to the translated-condition verifier.

---

## 4. Evaluated Verification Baselines

1. **No-Check (Translated-Only):**
   - Translate Hindi evidence $E_i^{\text{hi}} \to E_i^{\text{en}}$.
   - Predict veracity using verifier $(C_i^{\text{hi}}, E_i^{\text{en}})$.
   - Consultation Coverage: 0.0%.
2. **Direct Multilingual (Original-Only):**
   - Directly verify claim and evidence in Hindi $(C_i^{\text{hi}}, E_i^{\text{hi}})$.
   - Consultation Coverage: 100.0%.
3. **Always-Check Cascade:**
   - Run Translated-Only verification; always consult Original Hindi verifier for all instances.
   - Consultation Coverage: 100.0%.
4. **Selective-Check Cascade ($\tau^*$):**
   - Run Translated-Only verification; compute verifier predictive risk $R(x) = 1.0 - \max_c P(c \mid x)$.
   - If $R(x) > \tau^*$, route instance to Original Hindi verifier; otherwise retain Translated prediction.
5. **Random Routing Control:**
   - Randomly route instances to the Original Hindi verifier matching the exact consultation count ($k=13$, 7.98%) across 100 random seeds.

---

## 5. Development Threshold Tuning Protocol

- **Objective Function:**
  $$J(\tau) = \text{MacroF1}_{\text{dev}}(\tau) - \lambda \cdot \text{Coverage}_{\text{dev}}(\tau)$$
  where $\lambda = 0.20$ represents the latency penalty coefficient.
- **Search Grid:** $\tau \in \{0.30, 0.35, 0.40, \dots, 0.90\}$.
- **Tuning Constraints:** Evaluated strictly on the 103-item development split. Test set data was completely inaccessible during threshold search.
- **Optimal Selection:** $\tau^* = 0.650$.

---

## 6. Primary and Secondary Evaluation Metrics

### 6.1 Primary Descriptive Sensitivity Metrics
- **Paired Agreement Rate:** Proportion of instances where $\hat{y}_{\text{trans}} = \hat{y}_{\text{orig}}$.
- **Paired Disagreement Rate:** Proportion of instances where $\hat{y}_{\text{trans}} \ne \hat{y}_{\text{orig}}$.
- **Directional Flip Proportions:** Specific state transition probabilities between NLI classes.

### 6.2 Secondary Benchmark Metrics
- **Observed Accuracy:** Correct classifications over observed split size ($N=163$).
- **Observed 2-Class Macro-F1:** Unweighted mean of F1 scores across `CONTRADICTED` and `INSUFFICIENT_EVIDENCE`.
- **Nominal 3-Class Macro-F1:** Reported for historical continuity ($F_{1,\text{SUP}} = 0.0$).
- **Consultation Coverage:** Fraction of test instances routed to the secondary verifier ($k / N$).
- **End-to-End Latency:** Mean wall-clock time (ms) per instance measured during active execution.
- **Paired Statistical Significance:** Exact binomial McNemar tests on discordant classification pairs $(b, c)$ with Benjamini-Hochberg FDR adjustments.

---

## 7. Blinded Human Annotation Protocol (Pending Execution)

- **Annotation Target:** Translation Fidelity (not real-world factuality).
- **Evaluators:** 2 qualified, independent Hindi–English bilingual evaluators.
- **Blinding:** Evaluators receive opaque identifiers (`ITEM_xxxx`) without access to model predictions, gold labels, or error strata.
- **Packets:** 50 items sampled deterministically across 3 strata ($S_{\text{trans}}=20$, $S_{\text{verif}}=20$, $S_{\text{agree}}=10$).
- **Labels:** `PRESERVED`, `ALTERED` (requires $\ge 1$ distortion type and written rationale), `AMBIGUOUS_SOURCE`, `UNABLE_TO_DECIDE`.
- **Inter-Annotator Agreement:** Multi-class and binary Cohen's $\kappa$ with Wilson 95% confidence intervals and stratum-weighted population prevalence estimation.
- **Adjudication:** Documented third-reviewer adjudication for discordant pairs.

---

## 8. Known Methodological Limitations

1. **Pre-Retrieved Evidence:** Study evaluates verifier behavior on pre-retrieved snippets; does not evaluate retriever or generative LLM components.
2. **Class Imbalance:** Zero gold `SUPPORTED` instances in Hindi partition bounds accuracy and makes 3-class F1 a proxy metric.
3. **Exploratory Test Set:** The 163-item test split was inspected in previous project iterations and cannot serve as an untouched confirmatory test set.
4. **Single Language Pair:** Empirical findings are currently restricted to Hindi–English.
