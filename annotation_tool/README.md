# Translation Fidelity Annotation Workflow

**Module:** `annotation_tool`  
**Purpose:** Practical, friction-free annotation system for independent bilingual human evaluation of machine-translated evidence.  
**Integrity Rule:** Zero simulated or synthetic human data. This tool is built to collect and process real human judgments only.

---

## 1. Directory Structure

```text
annotation_tool/
├── README.md                          <- System overview and researcher manual
├── ANNOTATOR_INSTRUCTIONS.md          <- Plain-language guidelines for human annotators
├── internal_analysis_key.csv          <- SECRET analysis-only mapping (never sent to annotators)
├── app/
│   ├── index.html                     <- Self-contained offline HTML5/JS browser interface
│   └── launch_app.py                  <- Optional local HTTP server launcher
├── scripts/
│   ├── prepare_blinded_packets.py     <- Stratified deterministic packet generator
│   ├── validate_submissions.py        <- Automated submission validator (schema & completeness)
│   └── analyze_agreement.py           <- Inter-rater agreement (raw %, Cohen's kappa, stratification)
├── templates/
│   ├── submission_schema.json         <- JSON schema for submissions
│   ├── empty_submission_template.csv  <- Empty reference CSV template
│   └── COMPLETION_CHECKLIST.md        <- Pre-submission quality checklist for annotators
├── packets/
│   ├── packet_A.json & .csv           <- Blinded packet for Annotator 1 (50 items)
│   ├── packet_B.json & .csv           <- Blinded packet for Annotator 2 (50 items)
│   ├── PACKET_A_HANDOFF.zip           <- Ready-to-send ZIP packet for Annotator 1
│   └── PACKET_B_HANDOFF.zip           <- Ready-to-send ZIP packet for Annotator 2
├── submissions/
│   └── README.md                      <- Drop directory for returned real submission files (empty)
├── analysis/
│   └── README.md                      <- Output directory for agreement reports (populated after real submissions)
└── tests/
    └── fixtures/                      <- Isolated artificial QA fixtures for automated unit tests
```

---

## 2. Researcher Workflow

### Step 1: Deliver Packets to Real Human Annotators
Send `annotation_tool/packets/PACKET_A_HANDOFF.zip` to Annotator 1 and `PACKET_B_HANDOFF.zip` to Annotator 2.
Each annotator unzips the folder, double-clicks `index.html` in their browser, completes all 50 items, and exports their completed submission.

### Step 2: Ingest and Validate Returned Submissions
Place the returned JSON files into `annotation_tool/submissions/`.
Validate each file:
```bash
python annotation_tool/scripts/validate_submissions.py annotation_tool/submissions/submission_A1_packet_A.json packet_A
python annotation_tool/scripts/validate_submissions.py annotation_tool/submissions/submission_A2_packet_B.json packet_B
```

### Step 3: Run Agreement and Adjudication Analysis
Once both files pass validation:
```bash
python annotation_tool/scripts/analyze_agreement.py \
  annotation_tool/submissions/submission_A1_packet_A.json \
  annotation_tool/submissions/submission_A2_packet_B.json \
  annotation_tool/analysis
```
This produces:
- `aligned_two_annotator_evaluations.csv`
- `disagreement_queue_for_adjudication.csv`
- `stratum_breakdown_summary.csv`
- `HUMAN_ANNOTATION_AGREEMENT_REPORT.md`

---

## 3. Pre-Analysis Protocol and Thresholds
Detailed mathematical formulation and decision criteria are recorded in `annotation/ANNOTATION_ANALYSIS_PLAN.md`.
