# Revision Baseline and Provenance Specification

**Repository:** `Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift`  
**Revision Workspace:** `manuscript_revision_tacl/`  
**Original Manuscript Baseline:** `docs/manuscript/` (Status: FROZEN | BITWISE UNCHANGED)  
**Date Established:** 2026-10-24  
**Audit Standard:** TACL Evidence-First Submission Readiness  

---

## 1. Baseline Document Hierarchy and Authority

1. **Frozen Original Manuscript Baseline:**
   - **Path:** [`docs/manuscript/`](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/docs/manuscript/)
   - **Status:** Frozen archive. Preserved strictly unchanged across all 40 files (verified via automated SHA-256 regression testing in `validate_manuscript.py`).
   - **Master TeX File:** `docs/manuscript/main.tex`

2. **Authoritative Revision Workspace:**
   - **Path:** [`manuscript_revision_tacl/`](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/)
   - **Role:** Active development and editorial workspace. All structural reorganization, table reformatting, text strengthening, and compilation artifacts belong exclusively here.
   - **Author Preview Source:** `manuscript_revision_tacl/main.tex` (`[hyperref,acceptedWithA]`)
   - **Anonymous Submission Source:** `manuscript_revision_tacl/submission.tex` (`[hyperref,submission]`)

3. **Compiled PDF Versions:**
   - **Author Preview PDF:** [`manuscript_revision_tacl/main.pdf`](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/main.pdf) (20 pages, 769,480 bytes) — Displays lead researcher Onkar Kharat, co-author Himanshu Jadhav, project affiliations, and repository URL.
   - **Anonymous Submission PDF:** [`manuscript_revision_tacl/submission.pdf`](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/submission.pdf) (19 pages, 787,944 bytes) — Fully anonymized with running margin line numbers compliant with TACL blind review policy.
   - **Canonical Build Archive:** `manuscript_revision_tacl/build/tacl_paper.pdf`

---

## 2. Canonical Computational Artifacts (Source of Truth)

All scientific statements, numerical point estimates, and statistical conclusions in the revised manuscript are strictly grounded in the frozen computational outputs under `experiments/results_corrected/` and `data/processed/`:

| Canonical Artifact | Role in Study | Record Count |
| :--- | :--- | :---: |
| `experiments/results_corrected/canonical_test_predictions.csv` | Primary per-instance inference results on held-out test split | 163 instances, 44 attributes |
| `experiments/results_corrected/canonical_dev_predictions.csv` | Primary per-instance inference results on tuning split | 103 instances, 44 attributes |
| `experiments/results_corrected/canonical_benchmark_table.csv` | Canonical benchmark metrics, Wilson CIs, and latencies | 9 conditions / baselines |
| `experiments/results_corrected/canonical_statistical_tests.csv` | Paired McNemar tests, exact binomial p-values, and permutation FDRs | 8 pairwise contrasts |
| `experiments/results_corrected/canonical_error_attribution.json` | Disjoint outcome partition ($S_{\text{trans}}$, $S_{\text{verif}}$, $S_{\text{degraded}}$) | 163 test instances |
| `experiments/results_corrected/canonical_latency_summary.json` | E2E CPU latency profile measured across 8 threads | 4 main pipeline systems |
| `configs/experiment_config.yaml` | Experiment hyperparameter and model provenance manifest | Complete pipeline configuration |
| `data/processed/dev.jsonl` | Processed X-Fact Hindi development partition | 103 claims/evidence pairs |
| `data/processed/test.jsonl` | Processed X-Fact Hindi evaluation partition | 163 claims/evidence pairs |

---

## 3. Cryptographic Baseline Verification (SHA-256 Checksums)

The following SHA-256 cryptographic hashes define the immutable baseline state of the project:

```text
Algorithm   SHA-256 Hash                                                      File Path
---------   ----------------------------------------------------------------  --------------------------------------------------------------
SHA256      B792BE0AF604212B782C1C112BBD92390D5D28395464605AF62FBB997C063CC8  docs/manuscript/main.tex
SHA256      C6EDBABA73479FBD81C02C145309B6DEDDAEC5C8054B07A3373A261A5E145DAF  docs/manuscript/references.bib
SHA256      7C71EDE112CCB3711C7073C4B1C60ABFB076B83945E0E9D14ED79CAA37DCA3B6  docs/manuscript/tacl2021v1.sty
SHA256      27A3B62FDC4211FA56FE4827572FF0524B3BA3FE96C9443FAABA5A683AF83C08  docs/manuscript/acl_natbib.bst
SHA256      1F31665607CF8976F75C427EB379683D038A55C51BB9BD3A70AF9FA1F25B991A  experiments/results_corrected/canonical_test_predictions.csv
SHA256      729958D28E108545F121AC6FD3B0545692E7EC5946DF48E49EC4C64593F7FF18  experiments/results_corrected/canonical_benchmark_table.csv
SHA256      390F7CA090C97DC0D3182A6EECC5CCECFD0EDE699E0E10623998060B19CC1A01  experiments/results_corrected/canonical_statistical_tests.csv
SHA256      1F6819A6525737D3A6D955BEA798CD510BC9D80C948066D60DD55C9D3399A59D  configs/experiment_config.yaml
SHA256      2243C60AF13D1D5E4CE4D5FD40E0AFCB7A4AEA004F8D9615BC5328F8B682A438  data/processed/dev.jsonl
SHA256      B1F7580EEE7AB89E4BEE7B04CB55906243A2DAF36CF7B757B0281FF532E1751D  data/processed/test.jsonl
```

---

## 4. Frozen Scope Boundaries and Known Blockers

The following immutable boundaries govern all revisions:

1. **Exploratory Status:** The test split ($N=163$) was inspected during earlier computational experiments; all reporting must designate this study as an *Exploratory Computational Diagnostic Study*, never a blind confirmatory benchmark.
2. **Extreme Class Skew:** The test split contains 142 `CONTRADICTED`, 21 `INSUFFICIENT_EVIDENCE`, and 0 `SUPPORTED` claims. Validating true positive recall on supported claims ($TP_{\text{sup}} \equiv 0$) is structurally impossible.
3. **Absence of Completed Bilingual Human Annotation:** Gate C quarantine is active. Synthetic annotations are quarantined. All error taxonomy attributions must remain documented as observational diagnostic hypotheses, not human-verified ground truth.
4. **Cascade Negative Result:** The selective cascade ($\tau^* = 0.650$) does not beat the No-Check baseline on test ($28.22\%$, $p=1.0000$), functioning as a diagnostic limitation rather than a deployable contribution.
5. **Single Language Direction:** Evaluations are restricted strictly to Hindi-to-English translation shift (`hi->en`) on `Helsinki-NLP/opus-mt-hi-en` and `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`.
