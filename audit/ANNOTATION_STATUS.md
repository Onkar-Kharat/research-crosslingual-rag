# AUDIT REPORT: Bilingual Human Annotation Status

**Audit Date:** October 2026  
**Auditor:** Senior Research-Integrity & Methodology Auditor  
**Repository:** Cross-Lingual Evidence Verification  
**Gate C Status:** **PENDING / UNEXECUTED (Future Work)**  
**Computational Freeze Compatibility:** **COMPATIBLE (Scope strictly restricted to observational computational evidence)**  

---

## 1. Current Evidentiary Status of Gate C

1. **Zero Human Annotations Received:**
   As of this research freeze, **zero authentic human annotations have been received**. The submission directory `annotation_tool/submissions/` contains exactly zero filled submission records.
2. **Complete Invalidation of Legacy Synthetic Data:**
   In earlier iterations (v2/v3), an automated script generated simulated annotations. Those synthetic outputs were **permanently invalidated, purged from active analysis, and quarantined in `audit/invalidated_synthetic_annotations/`**.
3. **Execution Guard Active:**
   The generation script `scripts/perform_bilingual_annotation.py` is permanently locked with a runtime exception (`raise RuntimeError(...)`) to prevent accidental execution. Automated unit test `tests/test_annotation_integrity.py::test_perform_bilingual_annotation_guard` confirms this guard is active.
4. **No Synthetic Replacement:**
   In strict compliance with research-integrity guidelines, no synthetic, LLM-generated, or heuristic annotations were created as substitutes.

---

## 2. Research Claims Boundary Enforcement

Because authentic human evaluation is pending, the following scientific boundaries are strictly enforced across all repository documentation:

| Prohibited Claim (Requires Gate C) | Allowed Empirical Finding (Supported by Data) | Enforcement Status |
|:---|:---|:---:|
| "Human annotators confirmed that MT errors caused verifier failures." | "Cross-lingual evidence translation induces a 63.80% prediction disagreement rate in the NLI verifier." | **ENFORCED** |
| "Translation infidelity is the root cause of 36.9% of verifier errors." | "On 36.9% of errors (41/111), the verifier correctly predicts the claim when given original Hindi, but misclassifies when given English translation." | **ENFORCED** |
| Reporting human Cohen's $\kappa$ or inter-annotator agreement. | Stating clearly: "Human validation is pending; zero human agreement statistics are reported." | **ENFORCED** |
| Claiming causal validation of semantic fidelity. | Framing all findings strictly as observational computational prediction sensitivity under language shift. | **ENFORCED** |

---

## 3. Preservation of Blinded Protocol for Future Validation

The complete, independent, double-blind human annotation infrastructure is fully prepared, tested, and ready for future external bilingual evaluators:

- **Annotation Interface:** Standalone, zero-dependency HTML5/CSS/JavaScript web application located at `annotation_tool/app/index.html`. Runs 100% locally in any browser with zero telemetry.
- **Blinded Packets:**
  - `annotation_tool/packets/PACKET_A_HANDOFF.zip` (Annotator 1)
  - `annotation_tool/packets/PACKET_B_HANDOFF.zip` (Annotator 2)
  - Each packet contains exactly 50 opaque items (`ITEM_0001` to `ITEM_0050`) drawn across 3 stratified cohorts (Translation-Sensitive Flips, Verifier Reasoning Failures, Agreement Controls).
  - All gold labels, model predictions, confidences, and strata indicators are completely stripped.
- **Automated Validation:** `annotation_tool/scripts/validate_submissions.py` programmatically validates incoming JSON submissions against `annotation_tool/templates/submission_schema.json`.
- **Test Suite Verification:** All 5 unit tests in `tests/test_annotation_workflow.py` pass cleanly.
