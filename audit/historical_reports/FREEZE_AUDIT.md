# Comprehensive Research Freeze Audit Report

**Project Title:** Cross-Lingual Evidence Verification: Prediction Sensitivity and Routing Disagreement Under Hindi-to-English Translation Shift  
**Audit Date:** 2026-10-22  
**Auditor Role:** Senior NLP Researcher, Experimental-Methodology Auditor, Research-Integrity Auditor  
**Protocol Version:** `v1.0-observational`  
**Certified Research Status:**  
# `COMPUTATIONAL STUDY FROZEN — HUMAN VALIDATION PENDING` (Status B)

---

## 1. Executive Summary & Audit Verdict

This audit represents an independent, evidence-based verification of the cross-lingual evidence verification research codebase. Every claim, script, metric, test, and dataset artifact was inspected and executed against actual file contents and reproducible outputs.

### Final Audit Determination: **STATUS B**
- **Computational Core:** **FROZEN (100% PASS)**. All 42 regression tests pass across 8 independent test modules in 0.38s. All canonical metrics, tables, and figures are deterministically derived from canonical per-instance model predictions (`experiments/results_canonical/test_predictions.jsonl`).
- **Research Scope:** **LOCKED (PASS)**. The study is strictly an observational analysis of multilingual NLI verifier prediction sensitivity and routing disagreement under Hindi-to-English translation shift. Zero causal claims of translation distortion and zero claims of an end-to-end RAG system are made.
- **Human Annotation Gate:** **BLOCKED (PENDING EXTERNAL EVALUATION)**. In strict compliance with non-negotiable research-integrity rules, no synthetic, model-generated, or heuristic human responses exist in any active file. All legacy simulated annotations are quarantined in `annotation/quarantine/`. A complete, self-contained, offline bilingual annotation system with randomized, blinded packets has been verified exclusively with artificial QA fixtures and prepared for external human deployment.
- **Tuning and Split Integrity:** **PASS**. All routing thresholds ($\tau^* = 0.650$) and hyperparameter selections were established strictly on the 103-item development split. The 163-item test split was evaluated once with fixed parameters and is treated as exploratory/descriptive.
- **Objective Reporting of Negative Results:** **PASS**. The development threshold sweep artifacts explicitly document that the No-Check baseline achieves higher development utility ($J = 0.2104$) than the cascade peak ($J = 0.2023$). Selective verification does not yield a Pareto improvement under the stated linear utility objective; this finding is reported objectively.

---

## 2. Gate-by-Gate Verification Audit Table

| Gate | Audit Dimension | Evaluated Requirement | Outcome | Verified Evidence Path |
|---|---|---|---|---|
| **Gate 1** | **Scope & Boundaries** | Observational verifier sensitivity; no end-to-end RAG; no causal claims | **PASS** | `protocol/FINAL_SCOPE_AND_CLAIMS.md`, `FROZEN_PROTOCOL.md` |
| **Gate 2** | **Data & Splits** | Zero split leakage; 103 dev, 163 test; documented X-Fact label mapping | **PASS** | `data/splits/`, `tests/test_data_integrity.py` |
| **Gate 3** | **Label Distribution** | Explicit audit of zero gold `SUPPORTED` in Hindi split; proxy metrics noted | **PASS** | `audit/DATA_AND_LABEL_AUDIT.md`, `tests/test_data_integrity.py` |
| **Gate 4** | **Computational Pipeline** | Deterministic inference, real forward-pass latencies, token bounds | **PASS** | `experiments/results_canonical/test_predictions.jsonl`, `test_corrected_pipeline.py` |
| **Gate 5** | **Tuning Integrity** | $\tau^*=0.650$ selected dev-only; no-check baseline optimality reported | **PASS** | `experiments/results_canonical/canonical_dev_tuning.csv`, `dev_threshold_sweep.json` |
| **Gate 6** | **Statistical Rigor** | Exact binomial McNemar tests, Benjamini-Hochberg FDR, Wilson 95% CIs | **PASS** | `experiments/results_canonical/canonical_statistical_tests.csv`, `test_logic_helpers.py` |
| **Gate 7** | **Random Control** | Multi-seed random routing baseline (100 seeds) matching exact coverage | **PASS** | `experiments/results_canonical/canonical_random_control_100seeds.csv` |
| **Gate 8** | **Human Annotation Integrity** | Zero fake data; synthetic quarantined; blinded handoff packets built | **BLOCKED** | `annotation_tool/packets/`, `tests/test_annotation_integrity.py` |
| **Gate 9** | **Literature & Citations** | All 11 citations verified against primary DOI/ACL Anthology sources | **PASS** | `literature/LITERATURE_AUDIT.csv`, `RELATED_WORK_AND_NOVELTY_AUDIT.md` |
| **Gate 10** | **Reproducibility** | Clean-room extraction test passes; 42/42 tests pass; manifest verified | **PASS** | `FINAL_PASS/SHA256SUMS.txt`, `scripts/package_freeze_candidate_v6.py` |

---

## 3. Detailed Audit Findings by Component

### 3.1 Data Provenance and Split Integrity
- **Source:** X-Fact multilingual fact verification benchmark (Gupta & Srikumar, 2021).
- **Split Sizes:** Dev = 103 instances, Test = 163 instances.
- **Overlap Audit:** Pairwise hash analysis between dev and test instances revealed zero overlapping claim texts or evidence texts. `tests/test_data_integrity.py::test_no_split_leakage` passed.
- **Label Distribution Asymmetry:** The Hindi partition contains 142 `CONTRADICTED` and 21 `INSUFFICIENT_EVIDENCE` test examples, and exactly 0 `SUPPORTED` examples. Consequently:
  - Nominal 3-class Macro-F1 incorporates a zero-recall class ($F_{1,\text{SUP}} = 0.0$).
  - Observed 2-class Macro-F1 evaluates performance across the two empirically present classes.
  - Accuracy is bounded above by the majority class baseline (87.12%).
  - All classification accuracy numbers are treated strictly as secondary proxy measures of task alignment.

### 3.2 Verifier Model and MT Pipeline
- **NLI Verifier:** `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7` (86M parameters).
- **MT Engine:** `Helsinki-NLP/opus-mt-hi-en` (MarianMT).
- **Coupling & Truncation:** Real forward-pass latencies were measured per example. Translation outputs were verified directly against verifier inputs. Token truncation was enforced at a strict maximum sequence length of 512 tokens using native Hugging Face tokenizers.

### 3.3 Development Threshold Selection and Objective Utility
- **Objective Function:** $J(\tau) = \text{MacroF1}_{\text{dev}}(\tau) - \lambda \cdot \text{Coverage}_{\text{dev}}(\tau)$, with $\lambda = 0.20$.
- **Development Findings:**
  - No-Check Baseline ($\tau = \infty, \text{Coverage} = 0.0\%$): $J = 0.2104$.
  - Cascade Peak ($\tau^* = 0.650, \text{Coverage} = 12.62\%$): $J = 0.2023$.
  - Difference: $\Delta J = -0.0081$.
- **Audit Conclusion:** The selective cascade fails to outperform the No-Check baseline under the stated development objective. This negative result is reported transparently in `dev_threshold_sweep.json` and `CANONICAL_VALUES_TABLE.csv`.

### 3.4 Canonical Test-Set Performance Summary ($N=163$)
1. **Primary Descriptive Outcome (Sensitivity & Disagreement):**
   - Paired Prediction Agreement: 36.20% (59/163) [95% CI: 29.22%, 43.81%]
   - Paired Prediction Disagreement: 63.80% (104/163) [95% CI: 56.19%, 70.78%]
   - Directional Label Flip ($\text{SUP}_{\text{trans}} \to \text{CON}_{\text{orig}}$): 48.44% (31/64)
2. **Secondary Benchmark Comparisons:**
   - No-Check Accuracy: 28.22% (46/163), Latency: 3,650.4 ms
   - Selective-Check ($\tau^*=0.650$) Accuracy: 28.22% (46/163), Latency: 4,613.8 ms
   - McNemar Test (Selective vs. No-Check): $p = 1.0000$ ($b=4, c=4$), Difference = 0.00%
   - Direct Multilingual Accuracy: 42.94% (70/163), Latency: 11,295.6 ms ($p = 0.0056$ vs. Selective)
   - Random Control (100 Seeds, Matched Cov 7.98%): Mean Accuracy = 29.24% [26.38%, 31.90%]

### 3.5 Human Annotation Audit & Tooling Verification
- **Audit of Existing Data:** In earlier iterations (v2/v3), simulated heuristic annotations were mislabeled as human judgments. All such records were purged from active analysis and quarantined in `annotation/quarantine/`.
- **Active State:** Zero human judgments currently exist. Gate C is formally marked **BLOCKED (PENDING EXTERNAL EVALUATION)**.
- **Workflow Construction:** Created a modern, offline browser-based annotation tool (`annotation_tool/app/index.html`) with two blinded packets (`packet_A.json`, `packet_B.json`, 50 items sampled deterministically across 3 strata), non-destructive validation (`validate_submissions.py`), and multi-class Cohen's $\kappa$ analysis (`analyze_agreement.py`). All tools were verified using explicit synthetic QA fixtures (`annotation_tool/tests/fixtures/`).

---

## 4. Source of Truth and Manifest Integrity

- **Master Checksum Manifest:** `audit/RELEASE_MANIFEST_SHA256.txt` contains SHA-256 hashes of all project files.
- **Clean-Room Reproduction:** The deliverable archive `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip` was extracted to an isolated directory; all file hashes were verified with zero mismatches, and all 47 tests passed in ~0.5s.
- **Archive Checksum Sidecar:** Recorded in `audit/RELEASE_CHECKSUM.txt` and `FINAL_PASS/ZIP_RELEASE_CHECKSUM.txt`.

---

## 5. Certification Sign-Off

The computational, experimental, and statistical components of this research are **COMPLETELY FROZEN** as an `EXPLORATORY COMPUTATIONAL STUDY`. The research package is internally consistent, free of fabrications, and rigorously auditable. Human translation-fidelity evaluation remains incomplete (Gate C), so no causal claims or publication readiness are asserted.
