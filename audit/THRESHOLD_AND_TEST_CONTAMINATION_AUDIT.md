# AUDIT REPORT: Threshold Selection, Development Sweeps, and Test-Set Contamination Audit

**Audit Date:** October 2026  
**Auditor:** Senior Methodology & Integrity Auditor  
**Repository:** Cross-Lingual Evidence Verification  
**Status:** AUDITED, TRANSPARENTLY DISCLOSED, & METHODOLOGICALLY FROZEN  

---

## 1. Executive Summary

This audit evaluates the integrity of the risk routing threshold selection process, inspects the development sweep protocol, checks for test-set leakage, and establishes the exact evidentiary status of the test set evaluation.

### Key Audit Verdict:
1. **Zero Test-Set Contamination in Final Protocol:** The canonical routing threshold $\tau^* = 0.650$ was selected **strictly on the 103 development instances** using a prespecified linear utility objective. The 163 test instances were never exposed to parameter sweeps or threshold tuning.
2. **Transparent Historical Disclosure:** Earlier preliminary iterations of this project (v1) explored a threshold of $\tau = 0.30$ and evaluated it on the test set. Because the test set was inspected in earlier exploratory rounds, we **strictly designate the test set as "EXPLORATORY / PREVIOUSLY INSPECTED"**. We do not present the test set results as untouched clean-room confirmation.
3. **Inclusion of Proper Baselines:** The development sweep evaluated the full range of candidate thresholds against the **No-Check baseline ($\text{Coverage}=0.0\%$)** and **Always-Check baseline ($\text{Coverage}=100.0\%$)**, ensuring that the selective cascade was not evaluated against an artificially depressed strawman.

---

## 2. Prespecified Development Optimization Objective

The threshold sweep was conducted across $\tau \in [0.10, 0.65]$ on `data/processed/dev.jsonl` ($N=103$). The decision objective was prespecified in `protocol/analysis_plan.yaml` and `experiments/configs/verification_pipeline.yaml`:

$$J(\tau) = \text{Macro-F1}_{3\text{cl}}(\tau) - 0.15 \times \text{Coverage}(\tau)$$

- **Penalty Coefficient:** $0.15$ per unit coverage, reflecting the computational cost of secondary multilingual model execution.
- **Observed Development Sweep (`experiments/results_canonical/canonical_dev_tuning.csv`):**
  - At $\tau = 0.10$: Coverage = 98.06%, Macro-F1 = 0.2948, $J = 0.1477$.
  - At $\tau = 0.30$: Coverage = 80.58%, Macro-F1 = 0.2605, $J = 0.1397$.
  - At $\tau = 0.50$: Coverage = 34.95%, Macro-F1 = 0.1995, $J = 0.1471$.
  - At $\tau = 0.65$: Coverage = 12.62%, Macro-F1 = 0.2213, $J = \mathbf{0.2023}$ (Peak of Cascade).
- **No-Check Baseline Comparison:**
  - At $\text{Coverage} = 0.0\%$: Macro-F1 = 0.2104, $J = \mathbf{0.2104}$.
  - Utility Delta: $\Delta J = 0.2023 - 0.2104 = \mathbf{-0.0081}$.

### Transparent Scientific Conclusion:
Under the prespecified linear development utility function, the No-Check baseline outperforms the selective cascade ($\Delta J < 0$). Rather than modifying the objective function post-hoc to manufacture an artificial "win" for the selective method, this negative result is preserved and reported as an authentic empirical finding.

---

## 3. Test Set Evaluation Governance & Integrity Controls

1. **Fixed Parameter Freezing:** When evaluating `experiments/results_canonical/canonical_test_predictions.csv`, the parameter $\tau^* = 0.650$ was held completely fixed. No post-hoc sweep was conducted on the test split.
2. **Programmatic Assertion Guard:** In `scripts/run_corrected_experiments.py`, line 563 enforces a runtime assertion verifying that every test row's trigger status strictly obeys the frozen threshold:
   ```python
   assert (test_df["selective_triggered"] == (test_df["risk_score"] >= tau_star)).all()
   ```
3. **Automated Unit Test:** `tests/test_reproduced_artifacts_v4.py::test_threshold_selection_and_trigger_consistency` verifies that the threshold stored in `canonical_dev_tuning.csv` matches the trigger column in `canonical_test_predictions.csv`.

---

## 4. Evidentiary Scoping and Claims Boundaries

- **Claim Permitted:** "Under a prespecified development objective penalizing original consultation latency, the selective routing cascade fails to surpass the simple no-check baseline."
- **Claim Prohibited:** Claiming that $\tau^*=0.650$ was validated on an untouched blind confirmatory test set. All active reports and handoff summaries explicitly label the test set as "EXPLORATORY / PREVIOUSLY INSPECTED".
