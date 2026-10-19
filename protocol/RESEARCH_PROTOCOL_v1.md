# RESEARCH PROTOCOL v1.0: CROSS-LINGUAL CLAIM VERIFICATION

**Protocol Version:** 1.0  
**Effective Date:** 2026-10-19  
**Specification:** `ANTIGRAVITY_RESEARCH_IMPROVEMENT_AND_FREEZE_PROMPT.md` (Phase 3)  
**Task Domain:** Evidence-Grounded Cross-Lingual Claim Verification (Hindi $\rightarrow$ English)

---

## 1. Research Questions and Falsifiable Hypotheses

### Primary Research Question (RQ1):
- **RQ1 (Translation Sensitivity & Error Disentanglement):** In a cross-lingual claim verification pipeline where non-English evidence is translated into English, what proportion of downstream verification errors are attributable to translation-fidelity corruptions ($E_{\text{trans}}$) versus verifier-reasoning shortcomings on faithfully preserved semantics ($E_{\text{verif}}$)?
  - *Hypothesis $H_{1}$:* A substantial fraction ($\ge 25\%$) of verification failures in translated evidence are recoverable when the verifier is presented with the original untranslated evidence, indicating that translation fidelity is a primary error driver rather than verifier capacity alone.
  - *Refutation Criterion:* If $E_{\text{trans}} < 10\%$ of total verification failures, hypothesis $H_{1}$ is refuted.

### Secondary Research Questions (RQ2 & RQ3):
- **RQ2 (Consensus Failure & Negative Transfer):** Does unconditional dual-language consensus (averaging translated and original posterior probabilities, `Always-Check`) improve verification performance over single-language passes?
  - *Hypothesis $H_{2}$:* Naive consensus averaging dilutes verifier certainty when translations contain subtle semantic corruptions, resulting in performance equal to or worse than evaluating original evidence alone.
  - *Support Criterion:* Supported if `Always-Check` accuracy is lower than `Direct Multilingual` accuracy with statistically significant difference ($p < 0.05$).
- **RQ3 (Risk-Calibrated Selective Safeguards):** Can an automated risk trigger based on predictive uncertainty and lexical/numeral preservation selectively route ambiguous claims to original evidence, achieving significantly higher accuracy than unconditional consensus while maintaining throughput?
  - *Hypothesis $H_{3}$:* A risk-calibrated cascade ($\tau^*$) tuned strictly on development data outperforms `Always-Check` with statistical significance ($p < 0.05$, exact McNemar test).

---

## 2. Dataset and Task Formulation

### Task Definition:
Given a factual claim $c$ in language $L_c$ (Hindi) and retrieved evidence passage $e_{\text{orig}}$ in source language $L_s$ (Hindi), determine the veracity of $c$ relative to $e_{\text{orig}}$. In translated pipelines, $e_{\text{trans}} = M(e_{\text{orig}})$ is produced via neural machine translation.

### Label Space and Observed Empirical Distribution:
- **Formal Verification Space:** $\mathcal{Y} = \{\textsc{Supported}, \textsc{Contradicted}, \textsc{Insufficient\_Evidence}\}$.
- **Authentic Dataset Constraint:** As demonstrated in `audit/DATA_AND_LABEL_AUDIT.md`, authentic fact-checked claims from Indian fact-checking organizations exclusively target debunked rumors. Validated positive claims (`SUPPORTED`) are absent (0.0% in both dev and test).
- **Evaluation Mandate:** Systems must be evaluated and reported on both:
  1. **Observed 2-Class Metrics:** Evaluating the classes actually populated in ground truth (`CONTRADICTED` and `INSUFFICIENT_EVIDENCE`).
  2. **Standard 3-Class Metrics:** Preserving the standard NLI 3-class space with explicit disclosure that $F_1(\textsc{Supported}) = 0.0$ due to null support.

### Partitions:
- **Development Partition ($N=103$):** 89 `CONTRADICTED`, 14 `INSUFFICIENT_EVIDENCE`. Reserved strictly for threshold tuning, feature calibration, and ablation exploration.
- **Held-Out Evaluation Partition ($N=163$):** 142 `CONTRADICTED`, 21 `INSUFFICIENT_EVIDENCE`. Reserved strictly for frozen evaluation.

---

## 3. Experimental Conditions and Baselines

| Condition ID | System Name | Evidence Consulted | Decision Mechanism |
|:---:|:---|:---|:---|
| **C1** | **No-Check (Translated)** | Translated English ($e_{\text{trans}}$) only | $\hat{y} = \arg\max_y P_V(y \mid e_{\text{trans}}, c)$ |
| **C2** | **Direct Multilingual (Original)** | Original Hindi ($e_{\text{orig}}$) only | $\hat{y} = \arg\max_y P_V(y \mid e_{\text{orig}}, c)$ |
| **C3** | **Always-Check (Dual Consensus)** | Both $e_{\text{trans}}$ and $e_{\text{orig}}$ unconditionally | $\hat{y} = \arg\max_y [0.5 \cdot P_V(y \mid e_{\text{trans}}, c) + 0.5 \cdot P_V(y \mid e_{\text{orig}}, c)]$ |
| **C4** | **Selective-Check (Cascade)** | $e_{\text{trans}}$ initially; $e_{\text{orig}}$ if $R \ge \tau^*$ | Hard routing: if $R \ge \tau^* \rightarrow \hat{y}_{\text{orig}}$; else $\hat{y}_{\text{trans}}$ |
| **A1** | **Ablation: Uncertainty-Only** | $e_{\text{trans}}$ initially; $e_{\text{orig}}$ if $(1 - \max p) \ge \tau_u$ | Hard routing based purely on verifier entropy |
| **A2** | **Ablation: Numeral-Only** | $e_{\text{trans}}$ initially; $e_{\text{orig}}$ if $(1 - \text{Overlap}_{\text{num}}) \ge \tau_n$ | Hard routing based purely on numeral distortion |
| **A3** | **Ablation: Posterior Averaging** | Both if $R \ge \tau^*$; else $e_{\text{trans}}$ | Posterior averaging on triggered claims (evaluating paper Eq 1 prose) |
| **A4** | **Control: Random Routing** | $e_{\text{orig}}$ routed at random matching coverage | Evaluates whether trigger is superior to random sampling |

---

## 4. Evaluation Metrics and Statistical Plan

1. **Point Estimates:** Computed directly as the exact observed proportion of correct predictions ($k / N$) on held-out test data. Never report a bootstrap mean as the point estimate.
2. **Confidence Intervals:** 95% non-parametric percentile bootstrap intervals computed using $B = 2,000$ resamples with fixed random seed (`seed = 42`).
3. **Paired Statistical Significance Tests:**
   - **Accuracy Differences:** Exact two-sided McNemar paired test with binomial evaluation for discordant pairs ($b, c$).
   - **Macro-F1 Differences:** Paired permutation test with $B = 5,000$ random sign-swaps.
4. **Error Attribution Taxonomy:**
   - $E_{\text{trans\_recov}}$: $\hat{y}_{\text{trans}} \ne y^*$ and $\hat{y}_{\text{orig}} = y^*$ (Translation-recovered).
   - $E_{\text{verif}}$: $\hat{y}_{\text{trans}} \ne y^*$ and $\hat{y}_{\text{orig}} \ne y^*$ on $y^* = \textsc{Contradicted}$ (Verifier reasoning error).
   - $E_{\text{insuff}}$: $\hat{y}_{\text{trans}} \ne y^*$ and $\hat{y}_{\text{orig}} \ne y^*$ on $y^* = \textsc{Insufficient}$ (Evidence insufficiency).
   - Guaranteed disjoint sum: $E_{\text{trans\_recov}} + E_{\text{verif}} + E_{\text{insuff}} = N_{\text{errors}}$.
5. **Fair Latency Accounting:**
   - Report mean, median, and standard deviation of latency per condition.
   - For translated pipelines, record both verifier-only forward pass time and end-to-end pipeline time including MarianMT translation.
