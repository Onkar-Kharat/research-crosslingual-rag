# Human Annotation Handoff Guide

**Project Title:** Cross-Lingual Evidence Verification: Prediction Sensitivity and Routing Disagreement Under Hindi-to-English Translation Shift  
**Date:** 2026-10-24  
**Protocol Version:** `v1.0-observational`  
**Current Status:** `HUMAN ANNOTATION PENDING / BLOCKED`  

---

## 1. Overview for Research Coordinators

To finalize **Gate C: Bilingual Human Verification**, authentic independent human judgments from two qualified Hindi–English bilingual evaluators are required. In strict compliance with non-negotiable research-integrity standards, automated, synthetic, or model-generated human labels are prohibited.

This document outlines the precise handoff procedure, packet distribution, submission requirements, and automated validation checks.

---

## 2. Annotator Qualifications & Independence

1. **Language Proficiency:** Evaluators must have demonstrable reading proficiency in standard Hindi (Devanagari script) and standard English.
2. **Independence:** Annotator 1 (A1) and Annotator 2 (A2) must complete their packets independently without discussing items, sharing rationales, or comparing judgments.
3. **Blinding:** Both evaluators are completely blinded to:
   - Model predictions in translated English and original Hindi.
   - Gold veracity labels and source error strata.
   - Confidence and risk scores.
   - Each other's responses.
4. **Estimated Effort:** 45 to 60 minutes per evaluator (50 items $\times$ $\sim 1$ minute/item).

---

## 3. Packet Distribution

Two self-contained handoff ZIP files have been prepared in `annotation_tool/packets/`:

- **For Annotator 1:** Distribute `annotation_tool/packets/PACKET_A_HANDOFF.zip`.
- **For Annotator 2:** Distribute `annotation_tool/packets/PACKET_B_HANDOFF.zip`.

### Contents of each Handoff ZIP:
1. `INSTRUCTIONS.txt`: Clear, non-technical instructions explaining the translation fidelity task.
2. `annotation_app.html`: Self-contained offline single-page application containing pre-embedded items.
3. `packet.json` & `packet.csv`: Raw packet data for evaluators who prefer spreadsheet annotation.
4. `COMPLETION_CHECKLIST.md`: Step-by-step checklist to verify completeness prior to submission.

---

## 4. Evaluator Workflow & Task Instructions

### Step 1: Open the Application
- The evaluator unzips their assigned handoff bundle and double-clicks `annotation_app.html` in any web browser (Chrome, Firefox, Safari, Edge).
- **No internet connection, server, software installation, or user account is required.**

### Step 2: Perform Evaluation
For each of the 50 items, the evaluator reviews:
- **Claim Text:** Provided strictly for factual context.
- **Original Hindi Evidence:** Source evidence snippet.
- **Machine-Translated English Evidence:** Automatically translated evidence snippet.

The evaluator answers:
1. **Translation Fidelity Label:**
   - `PRESERVED`: Claim-relevant factual semantics are preserved.
   - `ALTERED`: Claim-relevant facts have been changed, omitted, added, inverted, or garbled.
   - `AMBIGUOUS_SOURCE`: Hindi source text is too incomplete or ambiguous to judge fidelity.
   - `UNABLE_TO_DECIDE`: Annotator cannot determine due to domain/language ambiguity.
2. **Distortion Types:**
   - If `ALTERED`, select $\ge 1$ of: `NUM_DATE`, `NEGATION`, `ENTITY`, `OMISSION`, `HALLUCINATION`, `QUALIFIER`, `TIME`, `OTHER`.
   - If `PRESERVED`, select `NONE`.
3. **Rationale:**
   - Mandatory for `ALTERED`, `AMBIGUOUS_SOURCE`, and `UNABLE_TO_DECIDE`. (A brief 1-2 sentence note describing the semantic distortion).
4. **Confidence:** `HIGH`, `MEDIUM`, or `LOW`.

### Step 3: Export Submission
- Upon completing all 50 items, the evaluator clicks **Export Submission (JSON)**.
- The browser downloads `annotator_A1.json` (or `annotator_A2.json`).
- The evaluator returns the JSON file to the research coordinator.

---

## 5. Ingestion and Automated Validation Protocol

Upon receiving both authentic submission files, the research coordinator executes the following automated pipeline:

### Step 1: Place Files in Submissions Directory
```bash
cp path/to/returned_A1.json annotation_tool/submissions/annotator_A1.json
cp path/to/returned_A2.json annotation_tool/submissions/annotator_A2.json
```

### Step 2: Validate Schema and Completeness
Run the automated non-destructive validator:
```bash
python annotation_tool/scripts/validate_submissions.py \
  --file1 annotation_tool/submissions/annotator_A1.json \
  --file2 annotation_tool/submissions/annotator_A2.json
```
**Validation Checks Enforced:**
- Exactly 50 unique items matching expected opaque IDs.
- Zero empty or skipped responses.
- `ALTERED` entries possess $\ge 1$ substantive distortion type and non-empty rationale.
- `PRESERVED` entries have `NONE` distortion type.
- Distinct annotator codes (`A1` and `A2`).

### Step 3: Execute Agreement Analysis
```bash
python annotation_tool/scripts/analyze_agreement.py \
  --file1 annotation_tool/submissions/annotator_A1.json \
  --file2 annotation_tool/submissions/annotator_A2.json \
  --key annotation_tool/internal_analysis_key.csv \
  --out_dir annotation_tool/analysis/
```
**Outputs Produced:**
- `annotation_tool/analysis/agreement_report.json`: Multi-class & binary Cohen's $\kappa$, Wilson 95% CIs.
- `annotation_tool/analysis/agreement_summary.md`: Human-readable summary table.
- `annotation_tool/analysis/disagreement_queue_for_adjudication.csv`: Extracted items where A1 and A2 disagreed.

### Step 4: Adjudication (if needed)
- If Cohen's $\kappa < 0.60$ or disagreement items exist, recruit an independent 3rd bilingual reviewer (Adjudicator A3).
- Provide A3 with the disagreement queue. A3 resolves discrepancies without seeing model predictions.

---

## 6. Freeze Status Promotion

Once Gate C validation is completed with authentic human data:
1. Promote project freeze status to:
   `STATUS B: HUMAN-VALIDATED DIAGNOSTIC STUDY FROZEN`.
2. Update `FREEZE_GATE_REPORT.md` and `FREEZE_AUDIT.md`.
3. Package the final validated release archive as `v7`.
