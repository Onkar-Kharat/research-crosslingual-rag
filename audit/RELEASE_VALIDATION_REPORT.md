# Release Packaging and Verification Report

**Release Archive:** `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip`  
**Research Freeze Status:** `FROZEN — EXPLORATORY COMPUTATIONAL STUDY`  
**Protocol Version:** `v1.0-observational`  
**Evaluation Split:** Test split ($N=163$), Development split ($N=103$)  
**Automated Test Suite Status:** `PASSED (47 / 47 Tests OK)`  
**Manifest Hash Parity:** `100.0% (0 mismatches, 0 missing files)`  

---

## 1. Executive Summary & Verification Overview

This report provides the formal validation record for the research freeze release archive `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip`.

The research investigates cross-lingual evidence verification under Hindi-to-English translation shift using the mDeBERTa-v3-base NLI verifier on the X-Fact benchmark.

All experimental pipelines, unit tests, regression tests, and statistical derivations have been fully executed, validated, and verified from clean-room extractions.

---

## 2. Recomputed 3×3 Directional Transition Matrix & Flip Rates

Direction of transition: **Translated-Evidence Prediction (`pred_translated`) $\to$ Original-Hindi-Evidence Prediction (`pred_original`)**.

### Complete 3×3 Contingency Matrix ($N=163$):

| Translated Prediction (`pred_translated`) | Original CONTRADICTED | Original INSUFFICIENT_EVIDENCE | Original SUPPORTED | Total Translated |
|---|:---:|:---:|:---:|:---:|
| **CONTRADICTED** | 21 | 5 | 18 | **44** |
| **INSUFFICIENT_EVIDENCE** | 23 | 14 | 18 | **55** |
| **SUPPORTED** | 31 | 9 | 24 | **64** |
| **Total Original** | **75** | **28** | **60** | **163** |

### Derived Primary Sensitivity Metrics:
- **Overall Paired Prediction Agreement:** $59 / 163 = \mathbf{36.20\%}$ [95% Wilson CI: 29.22%, 43.81%]
- **Overall Paired Prediction Disagreement:** $104 / 163 = \mathbf{63.80\%}$ [95% Wilson CI: 56.19%, 70.78%]
- **Directional Flip ($\text{SUP} \to \text{CON}$):** $31 / 64 = \mathbf{48.44\%}$ [95% Wilson CI: 36.63%, 60.42%]
- **Directional Flip ($\text{CON} \to \text{SUP}$):** $18 / 44 = \mathbf{40.91\%}$ [95% Wilson CI: 27.69%, 55.59%]
- **Directional Flip ($\text{NEU} \to \text{CON}$):** $23 / 55 = \mathbf{41.82\%}$ [95% Wilson CI: 29.74%, 54.97%]

*(Audit note: Corrects previous reporting artifacts of 12/85 and 7/14, which arose from legacy subset denominators. Per-instance predictions were preserved without modification.)*

---

## 3. Automated Test Suite Verification

The automated test suite (`tests/run_all_tests.py`) covers 9 distinct verification modules:
1. `test_annotation_integrity.py`: Quarantined synthetic data, checksum guards, blinded stimulus columns.
2. `test_annotation_workflow.py`: Blinded packet generation, submission schema validator, Cohen's kappa.
3. `test_corrected_pipeline.py`: Per-instance inference outputs (103 dev, 163 test), token truncation bounds.
4. `test_data_integrity.py`: X-Fact raw data provenance, disjoint dev/test partitions, zero label leakage.
5. `test_directional_flips.py`: Exact derivation of the 3x3 transition matrix, flip rates, and paired McNemar exact and chi2 contingency test (No-Check: b=27, c=51, chi2=6.7821, p=0.008772; Selective: b=23, c=47, chi2=7.5571, p=0.005583).
6. `test_logic_helpers.py`: Devanagari/Arabic numeral extraction, Jaccard similarity, risk score bounds.
7. `test_method_logic.py`: Selective cascade routing behavior, Devanagari normalization.
8. `test_metrics_and_partitions.py`: Disjoint error partition, exact McNemar tests.
9. `test_reproduced_artifacts_v4.py`: Split integrity, softmax probabilities sum to 1.0, 100-seed random control.

**Test Execution Outcome:**
```
Ran 47 tests in 0.526s
OK
```

---

## 4. Cryptographic Integrity & Reviewer Verification Commands

### 4.1 Internal File Manifest Integrity:
Every file inside the release archive is indexed with its SHA-256 hash in `audit/RELEASE_MANIFEST_SHA256.txt` and verified with 100.0% hash parity.

### 4.2 External Archive Checksum Verification:
The authoritative external SHA-256 hash for `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip` is recorded in `audit/RELEASE_CHECKSUM.txt` and `FINAL_PASS/ZIP_RELEASE_CHECKSUM.txt`.

Reviewers can verify the release archive using:

#### Windows PowerShell:
```powershell
Get-FileHash -Path ./CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip -Algorithm SHA256
```

#### Linux / macOS:
```bash
sha256sum CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip
```
