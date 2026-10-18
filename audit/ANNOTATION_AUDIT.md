# Human Annotation Audit Report

**Project:** Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Audit Date:** 2026-10-24  
**Protocol Version:** `v1.0-observational`  
**Current Gate C Status:** `BLOCKED / PENDING AUTHENTIC EVALUATION`  

---

## 1. Audit of Human Annotation State

In accordance with Phase Seven of the Master Prompt, all annotation-related files, directories, interfaces, and scripts were thoroughly audited:

### 1.1 Invalidation and Quarantine of Legacy Synthetic Annotations
- **Forensic Finding:** In iterations v2 and v3, a script named `scripts/perform_bilingual_annotation.py` generated simulated "human" annotations using hardcoded heuristics and identical timestamps.
- **Remediation:**
  1. All synthetic annotation outputs (`annotation_submission_Annotator_1.csv`, `annotation_submission_Annotator_2.csv`) were immediately purged from active analysis and quarantined in `audit/invalidated_synthetic_annotations/`.
  2. The active script `scripts/perform_bilingual_annotation.py` was replaced with a hard runtime exception guard (`raise RuntimeError(...)`) preventing accidental synthetic data generation.
  3. `tests/test_annotation_integrity.py` verifies both the quarantine integrity and that invoking the legacy generator raises a `RuntimeError`.

### 1.2 Verification of Annotation Interfaces and Packets
- **Application:** Built a standalone, offline HTML5/CSS/JavaScript single-page application at `annotation_tool/app/index.html`.
- **Offline Self-Containment:** The interface requires zero external server dependencies, zero external APIs, zero telemetry, and zero user accounts. Annotators can launch it by double-clicking the file or via `python launch_app.py`.
- **Blinded Packet Generation:**
  - Script: `annotation_tool/scripts/prepare_blinded_packets.py`.
  - Sample Size: Exactly 50 items drawn deterministically (seed 42) across 3 strata:
    - Translation-Sensitive Flips ($S_{\text{trans}}$, $n=20$)
    - Verifier Error Overlap ($S_{\text{verif}}$, $n=20$)
    - Agreement Control ($S_{\text{agree}}$, $n=10$)
  - Blinding: All model predictions, confidence scores, risk scores, gold labels, and strata are stripped. Items are identified solely by opaque identifiers (`ITEM_xxxx`).
  - Distribution Bundles: Packaged as `annotation_tool/packets/PACKET_A_HANDOFF.zip` (for Annotator 1) and `PACKET_B_HANDOFF.zip` (for Annotator 2), containing identical 50 items under distinct random orderings.

### 1.3 Active Submissions Status
- **Audit Finding:** The submission directory `annotation_tool/submissions/` contains exactly 0 submission files (only a documentation `README.md`).
- **Conclusion:** **ZERO human annotations have been received to date.** Gate C is formally marked **BLOCKED / NOT AVAILABLE**.
- **Non-Negotiable Policy:** No responses have been synthesized, no mock annotator codes have been inserted, and zero inter-annotator agreement statistics are reported as real human data.

---

## 2. Integrity and Claim Enforcements

1. **No Causal Error Attribution:** Without authentic bilingual human judgments confirming semantic distortion, no scientific claim may state that machine translation errors *caused* verifier misclassifications.
2. **Observational Framing:** All observed label flips and disagreements must be reported strictly as *model prediction sensitivity* under cross-lingual translation shift.
3. **Manuscript Invariant:** The manuscript must not state or imply that human evaluation has been completed until real external annotators return completed packets.

---

## 3. Tooling and Validation Verification

The human annotation pipeline was verified end-to-end using explicit, artificial QA fixtures (`annotation_tool/tests/fixtures/`):
- `validate_submissions.py`: Correctly validates 50 unique opaque items, schema compliance, mandatory rationales for `ALTERED`, and distinct annotator codes. Correctly rejects missing rationales and incomplete items.
- `analyze_agreement.py`: Accurately computes raw agreement, multi-class and binary Cohen's $\kappa$, Wilson 95% confidence intervals, and exports a disagreement queue for third-reviewer adjudication.
- All 5 automated unit tests in `tests/test_annotation_workflow.py` pass cleanly.
