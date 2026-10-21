# Final Research Freeze Decision Report

**Project Title:** Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Protocol Version:** `v1.0-observational`  
**Audit Date:** 2026-10-24  
**Certified Status:**  
# `Status A: FROZEN — EXPLORATORY COMPUTATIONAL STUDY`

---

## 1. Formal Certification and Freeze Scope

Following an exhaustive computational audit, test environment repair, historical metrics reconciliation, and clean-room reproduction pass, the research project is formally certified as:

**`FROZEN — EXPLORATORY COMPUTATIONAL STUDY` (Status A)**

### Explicit Boundaries of This Freeze:
1. **Narrowed Scientific Scope:** This freeze applies strictly to the observational computational study of multilingual NLI verifier prediction sensitivity and routing behavior under Hindi-to-English translation shift.
2. **Computational Reproducibility:** All 43 automated regression tests pass (100.0% pass rate in 0.375s). All canonical results, tables, and figures are deterministically derived from canonical per-instance model predictions (`canonical_results.csv`).
3. **Absence of Real Human Judgments:** The project explicitly documents that genuine human annotation has **not been performed**. Gate C is formally marked **BLOCKED / PENDING EXTERNAL EVALUATION**.
4. **Exclusion of Causal Attribution Claims:** Zero claims attributing prediction flips to translation corruption are made or permitted.
5. **Exclusion of End-to-End RAG Claims:** Zero claims of full retriever-generator evaluation are made.
6. **Exploratory Test Set Designation:** The 163-item test split is formally treated as an exploratory descriptive benchmark rather than an untouched confirmatory sample.

---

## 2. Gate-by-Gate Verification Summary

| Gate | Audit Dimension | Outcome | Justification & Verification Evidence |
|---|---|:---:|---|
| **Gate 1** | **Scientific Scope** | **PASS** | Locked to observational sensitivity; no end-to-end RAG; no causal claims (`audit/FROZEN_PROTOCOL.md`) |
| **Gate 2** | **Data & Splits** | **PASS** | Zero split leakage; exact counts ($N_{\text{dev}}=103, N_{\text{test}}=163$); X-Fact provenance verified |
| **Gate 3** | **Label Semantics** | **PASS** | Documented mapping; zero gold `SUPPORTED` in Hindi split explicitly audited as proxy limitation |
| **Gate 4** | **Authoritative Pipeline**| **PASS** | Single source of truth (`experiments/results_canonical/`); 39.26% vs 28.22% conflict reconciled |
| **Gate 5** | **Tuning Integrity** | **PASS** | $\tau^*=0.650$ chosen dev-only; negative result ($J_{\text{No-Check}} > J_{\text{Cascade}}$) reported transparently |
| **Gate 6** | **Statistical Rigor** | **PASS** | Exact binomial McNemar tests, Benjamini-Hochberg FDR adjustments, 100-seed random control |
| **Gate 7** | **Latency Accounting** | **PASS** | Real forward-pass execution times on CPU hardware; coupled MT and verifier timing windows |
| **Gate 8** | **Human Annotation** | **BLOCKED** | Zero fake data; legacy simulated data quarantined; offline UI & blinded packets A/B verified |
| **Gate 9** | **Environment & Tests**| **PASS** | Portable imports verified; 43/43 tests pass in 0.375s (`audit/TEST_AND_REPRODUCTION_REPORT.md`) |
| **Gate 10** | **Literature & Citations**| **PASS** | 11/11 primary peer-reviewed citations verified via DOI/ACL Anthology (`literature/LITERATURE_AUDIT.csv`) |
| **Gate 11** | **Clean Reproduction** | **PASS** | Verified in isolated extraction; all file hashes match manifest (`audit/FREEZE_MANIFEST.md`) |

---

## 3. Canonical Numerical Values Table

| Evaluation Dimension | Parameter / Metric | Canonical Value | 95% Confidence Interval | Source Artifact |
|---|---|---|---|---|
| **Primary Sensitivity** | Paired Agreement Rate | **36.20% (59/163)** | [29.22%, 43.81%] | `canonical_results.csv` |
| **Primary Sensitivity** | Paired Disagreement Rate | **63.80% (104/163)** | [56.19%, 70.78%] | `canonical_results.csv` |
| **Primary Sensitivity** | Flip: Trans $\text{SUP} \to$ Orig $\text{CON}$ | **48.44% (31/64)** | [36.63%, 60.42%] | `canonical_results.csv` |
| **Primary Sensitivity** | Flip: Trans $\text{CON} \to$ Orig $\text{SUP}$ | **40.91% (18/44)** | [27.69%, 55.59%] | `canonical_results.csv` |
| **Primary Sensitivity** | Flip: Trans $\text{NEU} \to$ Orig $\text{CON}$ | **41.82% (23/55)** | [29.74%, 54.97%] | `canonical_results.csv` |
| **Benchmark (Test)** | No-Check Accuracy | **28.22% (46/163)** | [21.47%, 35.58%] | `canonical_results.csv` |
| **Benchmark (Test)** | Selective-Check Accuracy ($\tau^*=0.650$) | **28.22% (46/163)** | [21.47%, 35.58%] | `canonical_results.csv` |
| **Benchmark (Test)** | Direct Multilingual Accuracy | **42.94% (70/163)** | [35.57%, 50.92%] | `canonical_results.csv` |
| **Benchmark (Test)** | Always-Check Accuracy | **36.81% (60/163)** | [29.45%, 44.17%] | `canonical_results.csv` |
| **Benchmark (Test)** | Majority Baseline (Always CON) | **87.12% (142/163)** | [81.16%, 91.39%] | `canonical_results.csv` |
| **Routing Behavior** | Selective-Check Coverage | **7.98% (13/163)** | [4.71%, 13.15%] | `canonical_results.csv` |
| **Statistical Test** | McNemar: Selective vs No-Check | **$p = 1.0000$ ($b=4, c=4$)** | Difference = 0.00% | `canonical_results.csv` |
| **Statistical Test** | McNemar: Selective vs Direct Multi | **$p = 0.0056$ ($b=23, c=47$)** | Adjusted $p = 0.0067$ | `canonical_results.csv` |
| **Latency Benchmark** | No-Check Mean Latency | **3,650.4 ms** | [3,480.0, 3,820.0] ms | `canonical_results.csv` |
| **Latency Benchmark** | Selective-Check Mean Latency | **4,613.8 ms** | [4,420.0, 4,810.0] ms | `canonical_results.csv` |
| **Latency Benchmark** | Direct Multilingual Latency | **11,295.6 ms** | [10,850.0, 11,740.0] ms | `canonical_results.csv` |
| **Development Utility** | Dev No-Check Baseline Utility | **$J = 0.2104$** | — | `canonical_results.csv` |
| **Development Utility** | Dev Cascade Peak Utility ($\tau^*=0.650$) | **$J = 0.2023$** | — | `canonical_results.csv` |
| **Development Utility** | Dev Cascade Utility Difference | **$\Delta J = -0.0081$** | — | `canonical_results.csv` |

---

## 4. Decision Sign-Off

The computational research artifacts, canonical metrics, statistical comparisons, and test suites are **FROZEN**. Manuscript development may proceed strictly within the narrowed observational scope.
