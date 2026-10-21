# Remaining External Actions Before Human-Validated Diagnostic Freeze

**Current Project Status:** `COMPUTATIONAL RESULTS FROZEN — EXPLORATORY; HUMAN ANNOTATION PENDING`  
**Protocol Version:** `v1.0-observational`  
**Date:** 2026-10-22  

---

## 1. Overview of Remaining Actions

All computational analysis, statistical calculations, data splits, verification pipelines, baseline evaluations, literature audits, regression test suites (42/42 tests passing), and blinded annotation tooling have been completed and frozen.

The **sole remaining unresolved task** for this research program is **Gate C: Bilingual Human Verification**. Per the non-negotiable integrity rules, human judgment cannot be automated, synthesized, or simulated. Authentic bilingual human evaluation is strictly required before any causal claim attributing model prediction flips to translation-fidelity corruption can be made.

Until the actions below are executed by real external bilingual annotators and adjudicators, the project remains at:
`COMPUTATIONAL RESULTS FROZEN — EXPLORATORY; HUMAN ANNOTATION PENDING`.

---

## 2. Action Items: Human Annotation Workflow Execution

### Action 1: External Annotator Recruitment
- **Role:** 2 independent bilingual evaluators (Annotator A1 and Annotator A2) with demonstrable proficiency in reading standard Hindi and English.
- **Independence:** Evaluators must work independently and must not communicate with each other during annotation.
- **Blinding:** Evaluators must remain blinded to model predictions, gold labels, error strata, and each other's responses.
- **Estimated Effort:** Approximately 45–60 minutes per annotator (50 items × ~1.0 minute/item).

### Action 2: Packet Distribution
- Deliver `annotation_tool/packets/PACKET_A_HANDOFF.zip` to Annotator A1.
- Deliver `annotation_tool/packets/PACKET_B_HANDOFF.zip` to Annotator A2.
- Each ZIP contains:
  1. `INSTRUCTIONS.txt` (Clear, jargon-free task instructions)
  2. `annotation_app.html` (Self-contained offline browser UI with pre-embedded packet)
  3. `packet.json` & `packet.csv` (Raw data files for optional spreadsheet annotation)
  4. `COMPLETION_CHECKLIST.md`

### Action 3: Packet Completion & Export
- Annotators open `annotation_app.html` in Chrome, Firefox, Safari, or Edge (no server, no internet, no extensions needed).
- Annotators read the Claim (for context), Original Hindi Evidence, and Machine-Translated English Evidence.
- Annotators provide:
  - `fidelity_label`: `PRESERVED` | `ALTERED` | `AMBIGUOUS_SOURCE` | `UNABLE_TO_DECIDE`
  - `distortion_types`: If `ALTERED`, at least one of `NUM_DATE`, `NEGATION`, `ENTITY`, `OMISSION`, `HALLUCINATION`, `QUALIFIER`, `TIME`, `OTHER`. (If `PRESERVED`, must be `NONE`).
  - `rationale`: Required for `ALTERED`, `AMBIGUOUS_SOURCE`, `UNABLE_TO_DECIDE`.
  - `confidence`: `HIGH` | `MEDIUM` | `LOW`.
- Annotators click **Export Submission (JSON)** and return the exported `.json` file to the research coordinator.

### Action 4: Automated Submission Ingestion & Validation
Place the returned JSON files into `annotation_tool/submissions/` (e.g., `annotator_A1.json` and `annotator_A2.json`).
Run the validation script to verify schema compliance, completeness, and non-empty rationale rules without altering data:
```bash
python annotation_tool/scripts/validate_submissions.py \
  --file1 annotation_tool/submissions/annotator_A1.json \
  --file2 annotation_tool/submissions/annotator_A2.json
```
If validation passes, both submissions are confirmed as genuine and complete.

### Action 5: Inter-Annotator Agreement Calculation
Compute raw agreement, unweighted & multi-class Cohen's kappa, Wilson 95% confidence intervals, and stratum-weighted population prevalence:
```bash
python annotation_tool/scripts/analyze_agreement.py \
  --file1 annotation_tool/submissions/annotator_A1.json \
  --file2 annotation_tool/submissions/annotator_A2.json \
  --key annotation_tool/internal_analysis_key.csv \
  --out_dir annotation_tool/analysis/
```
Outputs produced:
- `annotation_tool/analysis/agreement_report.json`
- `annotation_tool/analysis/agreement_summary.md`
- `annotation_tool/analysis/disagreement_queue_for_adjudication.csv`

### Action 6: Independent Adjudication (if required)
- If Cohen's $\kappa < 0.60$ or disagreement items exist, recruit a qualified 3rd reviewer (Adjudicator A3).
- Provide A3 only with `annotation_tool/analysis/disagreement_queue_for_adjudication.csv` (stripped of model predictions).
- A3 provides authoritative resolution for disagreed items.

### Action 7: Gate C Sign-Off and Freeze Promotion
Once authentic submissions and adjudication are completed:
1. Move validated files to `annotation/results/`.
2. Update `FREEZE_GATE_REPORT.md` to certify Gate C.
3. Promote project freeze status to:
   `STATUS B: HUMAN-VALIDATED DIAGNOSTIC STUDY FROZEN`.
4. Archive the final human-validated research package as `v7`.

---

## 3. Downstream Manuscript Actions (Out of Current Scope)

- **Manuscript Writing:** The TACL manuscript draft (`manuscript/`) is deliberately locked in this computational freeze pass.
- **Post-Gate C Manuscript Updates:** Once Gate C produces authentic human error rates, the manuscript may be updated with verified human attribution data. If Gate C is never executed, the manuscript must be drafted strictly as an observational study of model sensitivity under cross-lingual translation shift.
