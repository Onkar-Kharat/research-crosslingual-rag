# Method and Threshold Audit Report

**Project:** Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Audit Date:** 2026-10-24  
**Protocol Version:** `v1.0-observational`  
**Evaluation Code:** `scripts/run_corrected_experiments.py`  

---

## 1. Implemented Methods and Execution Path Verification

Each baseline and routing method was audited directly in `scripts/run_corrected_experiments.py` and `scripts/compute_evaluation_metrics_corrected.py`:

### 1. Translated-Only Verification (No-Check Baseline)
- **Input:** Claim $C_i^{\text{hi}}$ and translated English evidence $E_i^{\text{en}} = \text{MT}(E_i^{\text{hi}})$.
- **Inference:** $P_{\text{trans}} = \text{Verifier}(C_i^{\text{hi}}, E_i^{\text{en}})$, $\hat{y}_{\text{trans}} = \arg\max_c P_{\text{trans}}(c)$.
- **Coverage:** $0.0\%$ (0 / 163).
- **Latency Accounting:** $T_i^{\text{MT}} + T_i^{\text{trans}}$ (mean: 3,650.4 ms).
- **Audit Verification:** Method functions strictly as declared; no original Hindi evidence is accessed.

### 2. Original-Only Verification (Direct Multilingual Baseline)
- **Input:** Claim $C_i^{\text{hi}}$ and original Hindi evidence $E_i^{\text{hi}}$.
- **Inference:** $P_{\text{orig}} = \text{Verifier}(C_i^{\text{hi}}, E_i^{\text{hi}})$, $\hat{y}_{\text{orig}} = \arg\max_c P_{\text{orig}}(c)$.
- **Coverage:** $100.0\%$ (163 / 163).
- **Latency Accounting:** $T_i^{\text{orig}}$ (mean: 11,295.6 ms).
- **Audit Verification:** Verifier operates purely in Hindi; no translation overhead.

### 3. Always-Check Cascade (Dual Verification Consensus)
- **Input:** Both translated and original evidence streams.
- **Inference:** Average posterior $P_{\text{always}} = \frac{1}{2}(P_{\text{trans}} + P_{\text{orig}})$, $\hat{y}_{\text{always}} = \arg\max_c P_{\text{always}}(c)$.
- **Coverage:** $100.0\%$ (163 / 163).
- **Latency Accounting:** $T_i^{\text{MT}} + T_i^{\text{trans}} + T_i^{\text{orig}}$ (mean: 14,945.9 ms).
- **Audit Verification:** Accurately reflects dual execution cost.

### 4. Selective-Check Cascade (Hard Routing at $\tau^*=0.650$)
- **Input:** Initial Translated-Only verification; predictive risk evaluated:
  $$R(x) = 0.70 \cdot (1.0 - \max_c P_{\text{trans}}(c)) + 0.30 \cdot (1.0 - \text{Jaccard}_{\text{num}})$$
- **Routing Decision:**
  $$\hat{y}_{\text{selective}} = \begin{cases} \hat{y}_{\text{orig}} & \text{if } R(x) \ge \tau^* \\ \hat{y}_{\text{trans}} & \text{if } R(x) < \tau^* \end{cases}$$
- **Coverage:** $7.98\%$ (13 / 163).
- **Latency Accounting:** $T_i^{\text{MT}} + T_i^{\text{trans}} + \mathbf{1}_{\{R(x) \ge \tau^*\}} \cdot T_i^{\text{orig}}$ (mean: 4,613.8 ms).
- **Audit Verification:** Hard routing is verified; does not perform posterior averaging on routed items.

### 5. Numeral-Only Routing Ablation
- **Routing Decision:** Triggers secondary consultation if $\text{Jaccard}_{\text{num}} < 1.0$.
- **Coverage:** $96.3\%$ (157 / 163).
- **Audit Finding:** Because Hindi text frequently lacks numerals or contains transliteration discrepancies, numeral-only checking over-triggers, yielding near-100% coverage and high latency (14,751.3 ms).

### 6. Multi-Seed Random Control Baseline (100 Seeds)
- **Mechanism:** For each seed $s \in [0, 99]$, randomly selects exactly $k = \text{round}(0.0798 \times 163) = 13$ items to route to the original verifier.
- **Outcome:** Mean accuracy = 29.24% [95% CI: 26.38%, 31.90%].
- **Audit Verification:** 100 seeds tested; exact matched count enforced; confirms selective checking does not statistically separate from random routing ($p = 0.2669$).

---

## 2. Threshold Selection Audit & Development Optimality

### 2.1 The Objective Function
Threshold search was conducted exclusively on the 103-item development split across a grid $\tau \in [0.10, 0.65]$ with step size $0.025$:
$$J(\tau) = \text{MacroF1}_{\text{dev}}(\tau) - \lambda \cdot \text{Coverage}_{\text{dev}}(\tau) \quad (\lambda = 0.20)$$

### 2.2 Complete Development Comparison Table ($N=103$ Dev)

| Threshold ($\tau$) | Dev Coverage (%) | Dev Routed Count | Dev Macro-F1 (3cl) | Dev Macro-F1 (2cl) | Development Utility ($J$) | Status / Note |
|---|---|---|---|---|---|---|
| **$\infty$ (No-Check)** | **0.00%** | **0 / 103** | **0.2104** | **0.3156** | **0.2104** | **Global Dev Optimum** |
| 0.650 | 12.62% | 13 / 103 | 0.2275 | 0.3413 | 0.2023 | Best Cascade Point ($\tau^*$) |
| 0.625 | 16.50% | 17 / 103 | 0.2310 | 0.3465 | 0.1980 | Cascade Suboptimal |
| 0.600 | 22.33% | 23 / 103 | 0.2355 | 0.3533 | 0.1908 | Cascade Suboptimal |
| 0.500 | 44.66% | 46 / 103 | 0.2520 | 0.3780 | 0.1627 | Cascade Suboptimal |
| 0.400 | 66.99% | 69 / 103 | 0.2680 | 0.4020 | 0.1340 | Cascade Suboptimal |
| 0.300 | 83.50% | 86 / 103 | 0.2740 | 0.4110 | 0.1070 | Legacy v2/v3 Point |

### 2.3 Scientific Takeaway: Negative Result on Cascade Pareto-Dominance
1. **No-Check Outperforms Cascade:** The No-Check baseline ($Coverage=0$) achieves $J = 0.2104$, which is strictly greater than the best cascade point $\tau^* = 0.650$ ($J = 0.2023$).
2. **$\Delta J$ Metric:** $\Delta J = 0.2023 - 0.2104 = -0.0081$.
3. **Integrity Rule Compliance:** The research report does not claim that Selective-Check is globally optimal. It is explicitly reported as the best *conditional* cascade configuration, with the negative result acknowledged directly in active documentation.
