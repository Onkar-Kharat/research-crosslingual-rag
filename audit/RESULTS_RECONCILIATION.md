# Results Reconciliation and Historical Metrics Audit

**Project:** Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Audit Date:** 2026-10-24  
**Protocol Version:** `v1.0-observational`  
**Authoritative Location:** `experiments/results_canonical/` and `canonical_results.csv`  

---

## 1. Executive Summary of Reconciled Conflict

A previous independent audit identified a critical numerical conflict across project documentation:
1. **Canonical Benchmark Table:** Selective-Check Accuracy of **28.22% (46/163)** at threshold $\tau^* = 0.650$ with **7.98% (13/163)** consultation coverage.
2. **Historical Reproduction Report:** Selective-Check Accuracy of **39.26% (64/163)** at threshold $\tau = 0.30$ with **83.4% (136/163)** consultation coverage.

This forensic audit traced both numbers to their raw execution scripts, prediction files, parameter configurations, and evaluation logic.

---

## 2. Technical Lineage and Forensic Traceability

### 2.1 The Historical v2/v3 Configuration (39.26% Accuracy)
- **Source Artifact:** `experiments/results/test_predictions.csv` and `scripts/evaluate_statistical_significance.py` (legacy v2/v3 runs).
- **Configuration:** Threshold $\tau = 0.30$.
- **Mechanism:**
  - In this early implementation, predictive risk was computed as $R(x) = 0.70 \cdot (1.0 - \max_c P(c \mid x)) + 0.30 \cdot (1.0 - \text{Jaccard})$.
  - Setting $\tau = 0.30$ caused **83.4% (136 / 163)** of all test instances to trigger routing to the original Hindi verifier.
  - Of these 136 routed instances, the original Hindi verifier was correct on 57 items, while Translated-Only was correct on 7 unrouted items:
    $$\text{Total Correct} = 57 + 7 = 64 / 163 = 39.2638\% \approx 39.26\%$$
- **Why This Configuration Was Superseded:**
  1. *Dev/Test Contamination:* In early candidate versions, $\tau=0.30$ was either selected directly on the test set or chosen under an unpenalized objective.
  2. *Excessive Consultation:* A consultation coverage of 83.4% violates the operational premise of a selective cascade, effectively becoming an expensive dual-verification model (mean latency: 6,968.8 ms).
  3. *Statistical Insignificance:* Compared to Direct Multilingual verification (37.42% accuracy in v2), Selective-Check at 39.26% differed by only 3 items out of 163 (McNemar $p = 0.6072$, completely non-significant).

### 2.2 The Canonical v4/v5/v6 Configuration (28.22% Accuracy)
- **Source Artifact:** `experiments/results_canonical/canonical_test_predictions.csv`, `experiments/results_canonical/canonical_dev_tuning.csv`, and `scripts/run_corrected_experiments.py`.
- **Configuration:** Threshold $\tau^* = 0.650$, selected strictly on the 103-item development split.
- **Objective Function:**
  $$J(\tau) = \text{MacroF1}_{\text{dev}}(\tau) - 0.20 \cdot \text{Coverage}_{\text{dev}}(\tau)$$
  - Sweeping $\tau \in [0.10, 0.65]$ on the 103 dev items identified $\tau^* = 0.650$ as the best cascade trade-off point (Dev Macro-F1: 0.2275, Dev Coverage: 12.62%, $J = 0.2023$).
  - Crucially, the Dev No-Check baseline achieved $J = 0.2104$ ($\text{Coverage} = 0.0\%$), establishing that No-Check outperforms the selective cascade on development data ($\Delta J = -0.0081$).
- **Test-Set Execution:**
  - Evaluated on the 163 test items with fixed $\tau^* = 0.650$.
  - Routed Count: 13 / 163 instances (7.98% coverage).
  - Translated-Only Correct: 46 / 163 (28.22%).
  - Selective-Check Correct: 46 / 163 (28.22%).
  - McNemar Paired Comparison: $b = 4, c = 4, p = 1.0000$ (exactly zero net accuracy change).

---

## 3. Side-by-Side Comparison

| Feature / Dimension | Historical v2/v3 (Superseded) | Canonical v4/v5/v6 (Authoritative) |
|---|---|---|
| **Threshold ($\tau$)** | $\tau = 0.30$ | $\tau^* = 0.650$ |
| **Threshold Tuning Split** | Uncontrolled / Test Exposed | Development Split Only ($N=103$) |
| **Consultation Coverage** | 83.44% (136 / 163) | 7.98% (13 / 163) |
| **Test Accuracy** | 39.26% (64 / 163) | 28.22% (46 / 163) |
| **Observed 2-Class Macro-F1** | 0.4067 | 0.2950 |
| **Mean End-to-End Latency** | 6,968.8 ms | 4,613.8 ms |
| **McNemar vs. No-Check** | $p = 0.043$ | $p = 1.0000$ ($b=4, c=4$) |
| **McNemar vs. Direct Multi** | $p = 0.6072$ | $p = 0.0056$ ($b=23, c=47$) |
| **Development Utility $\Delta J$** | Not Evaluated on Dev | $\Delta J = -0.0081$ (No-Check beats Cascade) |
| **Protocol Status** | **SUPERSEDED — DO NOT USE** | **AUTHORITATIVE CANONICAL TRUTH** |

---

## 4. Reconciled Status and Active File Enforcement

1. **Which Result Corresponds to the Frozen Protocol:**
   - **28.22% at $\tau^* = 0.650$ is the sole authoritative canonical result.** It adheres strictly to methodological best practices: zero dev/test contamination, prespecified linear penalty objective, and fixed single-pass test evaluation.
2. **Designation of Prior Outputs:**
   - All reports and spreadsheets referencing 39.26% at $\tau=0.30$ (including `audit/RESULTS_REPRODUCTION_REPORT.md`, `research_freeze_candidate/`, and `experiments/results/`) are permanently designated **HISTORICAL / SUPERSEDED**.
3. **Active Reports Consistency:**
   - All active root and `FINAL_PASS/` documents (`canonical_results.csv`, `FREEZE_AUDIT.md`, `FROZEN_PROTOCOL.md`, `README.md`, `CANONICAL_VALUES_TABLE.csv`, `FINAL_RESEARCH_FREEZE_DECISION.md`) report 28.22% at $\tau^*=0.650$.
   - Zero active documents present the superseded 39.26% figure as current truth.
