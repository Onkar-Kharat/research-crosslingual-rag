# ANTIGRAVITY MASTER PROMPT — RESEARCH IMPROVEMENT, REPRODUCTION, AND RESEARCH FREEZE

## Mission and priority

Act as a rigorous NLP research scientist, experimental-methodology auditor, multilingual fact-verification specialist, and reproducibility engineer. Your task is to **repair and complete the research itself, then freeze the research** for a future TACL submission. The manuscript-writing phase is explicitly out of scope for now.

The user will provide these three files created for this project:

1. `research-crosslingual-rag-main_AUDIT_FIRST.zip` — the existing research project and artifacts.
2. `ANTIGRAVITY_AUDIT_AND_RECOVERY_PROMPT.md` — the previous audit/recovery instructions.
3. `MANUSCRIPT_REVIEW_AND_TACL_READINESS.md` — the initial review report with suspected problems and recommendations.

These filenames may vary slightly depending on the downloaded copy. Find the actual files supplied, record their names and hashes, and confirm what is present. Do not assume an artifact exists merely because a prior message mentioned it. If the original research PDF or other needed files are inside the ZIP, inspect them there. If something essential is missing, continue all work possible and list the precise missing input instead of stopping at the first obstacle.

**Treat the review report and prior prompts as leads to verify, not as unquestionable truth.** Independently reproduce or refute every material allegation using the actual data, source code, logs, paper, and authoritative dataset documentation.

## Absolute scope boundary: research first, manuscript later

Do NOT draft, rewrite, polish, or format the paper/manuscript during this phase. Do not produce a new submission-ready PDF, rewrite the abstract/introduction/conclusion, or spend time on TACL page formatting. Preserve the existing manuscript files unchanged. You may create technical research documents needed to define the task, protocol, annotation guide, experiments, results, and freeze decision, but they are not a manuscript.

The priority order is:

1. Establish that the dataset and task are valid.
2. Verify scientific claims, implementation, data lineage, and evaluation correctness.
3. Reassess related work and whether a defensible research contribution remains.
4. Correct experimental design and run reproducible experiments.
5. Perform required annotation/robustness/error analysis without inventing human judgments.
6. Decide, with evidence, whether the research meets the freeze criteria.
7. Package the frozen research and all reproducibility artifacts into a ZIP for external review by the user’s ChatGPT reviewer.

Do not equate a “freeze” with forcing a positive result. A valid, well-executed negative or inconclusive result is preferable to a misleading positive claim. If required evidence is missing, say **NOT FROZEN** and provide actionable blockers. Never mark the research frozen merely to finish the task.

## Core topic — provisional only

The current draft studies English–Hindi cross-lingual claim verification, focusing on the effect of translating Hindi evidence into English, distinguishing translation-fidelity problems from verifier-reasoning failures, and selectively checking original-language evidence.

Treat this as a hypothesis, not a commitment. First conduct the audit and literature review. If the current task definition, labels, data, or novelty cannot support it, narrow, redesign, or replace the topic based on evidence. Do not preserve an invalid research question simply because a draft already exists. Do not claim “first,” “novel,” “unexplored,” or “causal” unless the evidence warrants that exact language.

## Working rules

- Work autonomously on routine, reversible local tasks. Use explicit checkpoints at the gates below.
- Use free/local tools, open models, and datasets whose license and terms permit the planned use. No paid APIs, paid services, subscriptions, or cloud compute without asking first. Ask before large downloads/runs, destructive actions, external submissions, or any action that could overwrite the original project.
- Keep the original project immutable. Work in a new folder or a version-control branch. Never silently overwrite input data, original predictions, the original PDF, or original code. Record changes in a change log.
- Never fabricate data, labels, human annotations, outputs, citations, DOIs, statistical significance, execution logs, or completion status. Never infer an experiment ran from the existence of a result file alone.
- Clearly label claims as **verified**, **partially verified**, **not verified**, or **contradicted** and support them with paths, commands, line numbers, record IDs, or source URLs where available.
- Cite external scholarly/official sources in the literature matrix. Verify title, authors, venue/year, DOI/ACL Anthology/arXiv identifiers, status, and the actual claim being used. Search current literature, not just the references already in the draft. Include close prior work and work published through the date of the audit. Do not rely on abstracts alone when full papers are accessible.
- Keep a dated `DECISION_LOG.md` with each decision, alternatives, evidence, and consequence.
- Use English in all reports and deliverables.
- Do not ask the user to decide routine technical details. Make and document a sensible choice. Ask only when genuine human judgment, user approval, or missing information is required. In particular, do not label translation fidelity solely through automated inference when bilingual human adjudication is required.

# PHASE 0 — SAFE INTAKE AND PROJECT INVENTORY

1. Identify the actual three supplied files and any additional project/PDF files. Record their paths, sizes, timestamps where available, and SHA-256 hashes in `audit/input_manifest.csv`.
2. Inspect the ZIP contents before extraction; reject path traversal or unsafe archive paths. Extract into a fresh working directory, never into the source directory.
3. Inventory code, configuration, data, prediction files, experiment logs, plots, figures, generated reports, environment files, manuscript source, and binary artifacts. Record file paths and purpose in `audit/PROJECT_INVENTORY.md`.
4. Check whether the repository has Git history, uncommitted changes, or missing dependencies. Preserve the original state as a read-only snapshot or immutable commit.
5. Detect OS, Python, CPU, RAM, GPU, free disk, package manager, and relevant model cache. Prefer Python 3.11, fall back to 3.12 if necessary, and use a project `.venv`. Do not force incompatible package upgrades. Save a machine-readable environment report.
6. Produce `audit/INITIAL_AUDIT_PLAN.md` listing the order of checks and the files to be inspected. Then start the audit immediately; do not stop after creating a plan.

# PHASE 1 — INDEPENDENT REPRODUCTION OF THE CURRENT RESULTS

Run a careful forensic audit before designing replacements.

## 1A. Reconcile the paper with artifacts

Build a table for every primary quantitative claim in the current PDF: paper page/section/table/figure, exact claim, corresponding source code, corresponding input artifact, independent recomputation, status, and required correction. Include at least accuracy, Macro-F1, class-wise metrics, label-flip rate, error-category counts, coverage, threshold and utility, confidence intervals, latency, p-values, sample sizes, and all baseline comparisons.

Do not trust a report or screenshot. Recompute from raw labels and per-example prediction records. Check item-ID alignment and missing/duplicate IDs. Derive point estimates directly from the specified held-out predictions; report bootstrap distributions and intervals separately instead of silently using a bootstrap mean as the point estimate.

## 1B. Validate X-Fact provenance, labels, and splits

- Retrieve and inspect the authoritative X-Fact paper, data repository, label schema, official split definitions, and license/usage terms.
- Verify every source label and its mapping to the task. Do not assume that mapping “partly true,” “misleading,” “unproven,” or any source category to `INSUFFICIENT_EVIDENCE` is correct. Record the exact source labels, official meaning, selected mapping, rationale, and alternatives.
- Recompute label distributions for every split and condition. Check for missing classes, collapsed labels, invalid values, and class imbalance. Determine whether the current task definition truly supports three-way (SUPPORTED / CONTRADICTED / INSUFFICIENT_EVIDENCE) verification. If it does not, redesign the task or select a more suitable licensed dataset before reporting three-class scores.
- Check train/dev/test leakage, duplicate or near-duplicate claims, shared evidence/documents, same-event overlap, claim IDs and source overlap. Determine whether the currently called “test” set has already been used repeatedly for threshold selection or research decisions. If it has, treat it as exploratory and create a new independent held-out evaluation or choose an untouched public evaluation set with defensible splits. Do not call a repeatedly inspected test set pristine.
- Verify that all data used can legally be redistributed. If not, include download/setup scripts, dataset references, accepted terms, checksums, and instructions rather than redistributing prohibited files.

Write `audit/DATA_AND_LABEL_AUDIT.md`, `data/DATASET_CARD.md`, and `data/DATA_PROVENANCE_AND_LICENSES.md`.

## 1C. Reconcile code and declared method

Trace each baseline and the proposed selective method end-to-end. Compare the equations, pseudocode, configuration, actual implementation, saved predictions, figure labels, and reported outcome.

Specifically verify, without assuming the initial review is correct:

- Whether triggered selective checking averages the translated/original posterior distributions, selects the original prediction, or performs some other operation.
- Whether the gate and threshold in the paper match the code and saved run.
- Whether the numeral/entity mismatch feature is implemented as described and uses the correct numeral systems and tokenization. Check any potentially inconsistent figure annotation (for example, descriptions of Arabic versus Devanagari numerals).
- Whether inference time includes translation, original-evidence fallback, preprocessing, model loading, and other end-to-end costs; identify warm-up and caching effects.
- Whether the implementation uses token-based truncation or character-based truncation and whether the maximum sequence length is actually honoured.
- Whether development-only threshold selection is faithfully implemented and whether test labels or test metrics influenced it.
- Whether confidence scores are calibrated or merely raw model scores. Do not refer to uncalibrated max probabilities as calibrated uncertainty.
- Whether averaging model probabilities is justified, whether class order is consistent across both routes, and whether logits/probabilities/labels are handled correctly.
- Whether `requirements.txt`, lock files, run commands, referenced scripts, seeds, package versions, and reported runtime match the actual environment and code.

Document each discrepancy in `audit/PAPER_CODE_RECONCILIATION.csv` and explain its scientific consequence. Do not edit the existing manuscript during this phase.

## 1D. Recompute metrics and statistics correctly

Create an independent evaluation script that works from the exported per-example prediction table and ground-truth labels. Verify at minimum:

- Exact accuracy, Macro-F1, per-class precision/recall/F1, balanced accuracy where appropriate, confusion matrices, and class support.
- Coverage/routing rate and the quality-versus-cost/latency trade-off at each threshold.
- Label-flip rate and the direction of changes, using stable paired item IDs.
- Correct confidence intervals, resampling unit, random seed and number of resamples. Explain why that interval method is appropriate for the sample design.
- Correct paired statistical tests for each stated comparison. Check the assumptions and use exact McNemar where applicable for paired correctness on accuracy; use a paired permutation or justified paired bootstrap approach for Macro-F1. Report effect sizes and uncertainty, not only p-values.
- Multiple comparisons and primary-versus-secondary outcomes. Predefine the primary comparison before evaluating a new test set; use a correction or clearly label exploratory comparisons when appropriate.
- Repeated-run variability if the method/model is stochastic. Preserve all seeds and predictions.
- End-to-end latency measured fairly under the same machine/runtime conditions for all systems. Report mean and median and variability, note hardware, and separate translation/verifier/fallback components.

Check all counts in error tables. In particular, determine whether the reported error categories are genuinely mutually exclusive and exhaustive. If their counts sum to more than the number of incorrect No-Check predictions (the initial report raised this as a suspected issue), determine whether cases overlap; change the scheme or count only with a valid defined unit. Never force totals to reconcile by deleting or relabeling observations without evidence.

Save outputs under `results/audit_recomputed/` and summarize them in `audit/RESULTS_REPRODUCTION_REPORT.md`.

# PHASE 2 — LITERATURE AND NOVELTY AUDIT

Conduct a reproducible search of scholarly databases and authoritative sources. Search ACL Anthology, arXiv, Crossref/DOI records, conference proceedings, papers’ official repositories, and relevant broader scholarly search indexes. State the actual search date, search strings, databases, inclusion/exclusion rules, and coverage limits.

Audit at least the following close work, confirming the exact publication details and scope rather than relying on the draft's description:

- “A Comparative Study of Translation Bias and Accuracy in Multilingual LLMs for Cross-Language Claim Verification” (listed in the current draft as arXiv:2410.10303).
- “XFEVER: Exploring Fact Verification across Languages” (listed in the project context as arXiv:2310.16278).
- “XRAG: Cross-lingual Retrieval-Augmented Generation” (EMNLP Findings 2025).
- “Multilingual Retrieval-Augmented Generation for Knowledge-Intensive Question Answering Task” (EACL Findings 2026).
- “All Languages Matter: Understanding and Mitigating Language Bias in Multilingual RAG” (ACL 2026).
- “When Scale Meets Diversity: Evaluating Language Models on Fine-Grained Multilingual Claim Verification” (FEVER workshop, 2025).
- Other more recent and directly relevant work found during search, including machine-translation faithfulness, multilingual NLI, claim verification, selective prediction/cascades, abstention, uncertainty calibration, bilingual human evaluation, and evaluation leakage.

Verify whether the titles, citations, dates, authors and venue-status in the draft are accurate; distinguish peer-reviewed publication from preprint. Add missing close work, including work that weakens the proposed novelty.

Create:
- `literature/SEARCH_PROTOCOL.md`
- `literature/LITERATURE_AUDIT.csv` (one row per paper, with verified metadata, research question, data/languages, method, metrics, key findings, limitations, overlap with the proposed study, stable URL/DOI, and access/check status)
- `literature/RELATED_WORK_MATRIX.md`
- `literature/NOVELTY_ASSESSMENT.md`

Explicitly assess whether the combination of (i) paired original-versus-translated evidence, (ii) translation-fidelity vs verifier-error attribution, and (iii) selective original-evidence consultation is genuinely distinct from the closest prior art. Do not say “no prior work exists” unless you define the search scope and provide adequate evidence. If novelty is weak, propose 2–3 narrower defensible alternatives ranked by feasibility and contribution. Select the most defensible option and record why; do not silently stick to a weak idea.

# PHASE 3 — RESEARCH QUESTION AND PROTOCOL REDESIGN

Once Phases 1 and 2 reveal what is valid, define the actual study. Create a versioned protocol **before accessing any new held-out labels/results for tuning**.

The protocol must state:

- One primary research question and at most three secondary questions.
- Specific, falsifiable hypotheses (or explicitly exploratory questions), and what result would support or refute each one.
- Exact task definition and label semantics, inclusion/exclusion criteria, language direction(s), unit of analysis, dataset provenance/license, sampling, split/cluster logic, and sample-size limitations.
- Primary/secondary metrics, confidence-interval procedure, resampling unit, statistical tests, multiple-testing plan, seeds, hardware/runtime measurement, and failure handling.
- Threshold/parameter tuning procedures restricted to development data.
- Exact baselines and ablations to be run, with fair compute/cost accounting.
- Annotation plan for any claim requiring human judgment.
- Predefined stopping rules and what results permit a “research frozen” decision.

Because the current test set may have been inspected during development, determine the correct clean evaluation strategy. If there is no untouched test set, create a new properly separated evaluation set or use another suitable licensed benchmark. A new random seed alone does not make an already inspected test set untouched.

Possible baselines to evaluate, where valid for the task and feasible, include translated-evidence-only, original-evidence-only, always-consult-original, the defined selective method, random routing at comparable coverage, uncertainty-only routing, mismatch-only routing, and an oracle/upper-bound analysis clearly labelled as non-deployable. Do not run every imaginable model; justify a manageable minimum set that answers the research question fairly.

Use the smallest valid pilot first. Expand beyond Hindi–English or add models only if the pilot, data availability, budget, and compute justify it. More languages/models are not automatically better than valid labels, reliable annotations, strong controls, and sound statistics.

Save the protocol as `protocol/RESEARCH_PROTOCOL_v1.md`, configuration files, and a machine-readable `protocol/analysis_plan.yaml`. Mark the protocol version and SHA-256 before confirmatory evaluation. If the protocol changes later, version it, describe the reason, and label affected results exploratory.

# PHASE 4 — HUMAN ANNOTATION, IF REQUIRED

The research’s central distinction between a semantic mistranslation and a verifier-reasoning failure cannot be validated solely by comparing model predictions. Determine whether bilingual human annotation is necessary; for a strong claim that a translation changed meaning, it normally is.

If required:

1. Prepare an annotation guide with definitions and examples for meaning preserved, meaning altered, omission/addition, negation, entity, number/date, modality/qualifier, source-context loss, ambiguous/insufficient evidence, and unable-to-decide.
2. Create a blinded annotation sheet that does not show gold label, verifier predictions, or the proposed error category where that could bias annotators. Include stable IDs and anonymize unnecessary personal information.
3. Have at least two competent bilingual annotators independently annotate the defined sample, with a documented adjudication procedure. Antigravity must not impersonate annotators or generate synthetic “human” labels. If the user must supply annotations, stop at the annotation gate, deliver the complete sheet and instructions, and clearly mark the research as not yet frozen until the annotations are returned.
4. Report agreement using a suitable statistic (such as Cohen’s kappa for appropriate two-rater categorical labels or Krippendorff’s alpha where appropriate), raw agreement and class counts, uncertainty, adjudication rates, and limitations. Select the statistic based on the design rather than mechanically.
5. Define error categories using observable evidence and report ambiguous cases honestly. Do not force every example into a mutually exclusive category unless the guide and annotations justify that.

Create `annotation/ANNOTATION_GUIDE.md`, `annotation/ANNOTATION_PROTOCOL.md`, an empty/template sheet before annotation, and the analysis script. Protect annotators’ personal data and do not include identifying information in the final ZIP.

# PHASE 5 — IMPLEMENT, RUN, AND TEST THE CORRECTED EXPERIMENTS

After the research protocol is defined, implement the minimum sufficient experiments. Use free, locally runnable models and avoid paid services. Cache raw model outputs with stable item IDs and record model/version/checkpoint, tokenization, max length, decoding settings, seed, package versions, config hash, start/end time, and hardware.

Requirements:

- Every condition must use the same eligible claim/evidence units, with valid pairing and correctly aligned labels.
- Define one clear main selective method and implement exactly the stated behavior. Keep alternate routing or fusion approaches as explicit ablations.
- Make tokenization and truncation reproducible and consistent with the model architecture.
- Record per-example gold labels, predictions and class scores for each condition, routing decisions, trigger features, latency components, and error/audit flags.
- Store raw logs and predictions before aggregation. Derive tables and plots from scripts; do not hand-edit reported numeric values.
- Build automated tests for label mappings, class order, split integrity, item-ID alignment, threshold gating, routing behavior, coverage calculations, metric calculations, and table generation.
- Use deterministic settings where possible. Where exact determinism is unavailable, document it and rerun enough seeds to characterize variance if feasible.
- Record failures and excluded examples with reasons. Never silently drop cases to improve metrics.
- Perform relevant robustness checks and ablations without using test outcomes to change the method. Possible checks include alternative MT system/model if feasible, label-mapping sensitivity, threshold sensitivity on development data, class-specific performance, low-confidence handling, and cost/coverage sensitivity.
- Re-run the final pipeline from a clean environment using documented commands. Compare reproduced outputs with the saved results.

If a corrected experiment yields no advantage, preserve that result and determine whether the research question should be narrowed or the contribution changed. Do not keep tuning on the final test set until it becomes positive.

# PHASE 6 — RESEARCH FREEZE DECISION GATES

Produce an explicit gate report. Do not jump to the next phase when a gate fails.

### Gate A — integrity and data validity
Pass only when the original project is preserved; data provenance and license are recorded; labels and splits are verified; leakage and prior test-set exposure are handled; and the audit of existing claims is complete.

### Gate B — defensible novelty and a clear question
Pass only when the close-prior-work review is complete, the contribution can be stated narrowly and accurately, and the experiment is capable of answering the chosen research question. Otherwise narrow/replace the question and document the decision.

### Gate C — protocol and annotation readiness
Pass only when the versioned protocol, sampling, analysis plan, baselines, statistical tests, tuning boundary, and human-annotation requirements are explicit. Any required human annotation must be completed and quality-checked before a freeze.

### Gate D — reliable experimental evidence
Pass only when the corrected pipeline runs, all key result tables reproduce from raw per-example outputs, tests pass, uncertainty is reported correctly, latency accounting is fair, and the major claims do not exceed evidence. Positive statistical significance is not a gate by itself; a carefully measured null result can pass if the research is still meaningful.

### Gate E — reproducibility and freeze
Pass only when an independent clean run is documented, data/model/source licenses and redistribution restrictions are clear, the frozen protocol and actual code/config hashes are recorded, results are regenerated by scripts, all exclusions and limitations are disclosed, and no critical or major unresolved scientific validity issue remains.

If any gate fails, mark `RESEARCH_STATUS.md` as `NOT FROZEN`, list each blocker with evidence and the exact required action, and package the best current candidate clearly marked **NOT FROZEN** for review. Continue with every autonomous safe task possible before asking for needed human input.

If all gates pass, mark the research **FROZEN FOR MANUSCRIPT PHASE**. This freezes the research design, verified dataset version, analysis plan, experiment artifacts, results, and conclusions—not the manuscript prose. Future deviations must be versioned and justified.

# PHASE 7 — DELIVERABLES AND REQUIRED ZIP

Create a clean, portable final directory, for example:

`research_freeze_candidate/`

It should contain (adapt only when justified and document omissions):

- `README_RESEARCH_FREEZE.md` — what was studied, exact setup/run instructions, file map, current freeze status, known limitations, and quick reproduction commands.
- `RESEARCH_STATUS.md` — gate-by-gate PASS / FAIL / BLOCKED status and reasons.
- `DECISION_LOG.md` — chronological decisions and alternatives.
- `audit/` — input hashes, inventory, paper–code reconciliation, data/label audit, reproduction report, and resolved/unresolved issue register.
- `literature/` — search protocol, verified literature table, comparison matrix, novelty assessment, and source links.
- `protocol/` — final versioned protocol and machine-readable analysis plan/config.
- `data/` — dataset card, provenance/license record, data hashes, split definitions, acquisition/processing scripts, and only the data files that are legally redistributable. Do not redistribute third-party data contrary to license/terms; provide scripts and hashes instead.
- `annotation/` — guide, protocol, anonymized annotation data/sheet, adjudication and agreement report where annotation was required and completed. If awaiting human work, include templates and status but do not claim completion.
- `src/` or `scripts/` — clean source code for processing, experiments, metrics, statistics, plotting, and tests.
- `configs/` — exact configurations and fixed seeds.
- `predictions/` — per-example predictions and route decisions for each condition, with item IDs and label semantics, subject to data license/privacy constraints.
- `results/` — machine-generated CSV/JSON/Markdown tables, confidence intervals, statistical tests, confusion matrices, figures and plotting source. Each figure must be generated from committed result data and have a source script.
- `logs/` — run logs, environment details, model/version records, clean rerun record, and checksums. Do not store private tokens or secrets.
- `tests/` — automated validity and regression tests with a recorded pass/fail report.
- `REVIEW_ME_FIRST.md` — a concise reviewer handoff: the most important changes, strongest verified findings, unresolved caveats, exact files the reviewer should inspect, and the research freeze status.
- `MANIFEST_SHA256.txt` — SHA-256 checksums for distributable files.
- `requirements.txt` plus lock/environment export if supported.

Do not add a newly rewritten manuscript to this package. The existing manuscript can be retained only as an unmodified source/reference artifact if necessary; clearly state that it is not the new validated research output and has not been revised during this phase. Do not include model weights unnecessarily or any non-redistributable data. Ensure the ZIP does not contain absolute paths, temporary caches, `.venv`, secrets, API keys, Windows user profiles, or unrelated large files.

Run all scripts needed to regenerate final research tables and plots before packaging. Perform a clean extraction test of the ZIP in a new temporary directory and verify that the documented reproduction commands work as far as the available hardware and lawful data access allow. Include any limitation in the report rather than claiming a successful clean run without evidence.

Create a ZIP with a clear name such as:

`CROSS_LINGUAL_RAG_RESEARCH_FREEZE_REVIEW.zip`

If the gates are not all passed, use:

`CROSS_LINGUAL_RAG_RESEARCH_FREEZE_CANDIDATE_NOT_FROZEN.zip`

Save the ZIP in the project root or another clearly documented location. Verify that the file exists, is non-empty, can be opened, and contains the required deliverables. Include the exact full path, file size, SHA-256, and a short inventory in the final report.

# CHECKPOINTS

- **Checkpoint 1:** After intake and initial audit, present a concise evidence-based issue list and chosen plan. Continue safe, reversible work without waiting for approval.
- **Checkpoint 2:** Before a large run, changing the main question/data source, or requesting human annotation, present the proposed experiment/annotation and why it is necessary. Ask for approval only where the user must make a decision or supply human judgment. Do not pay for anything.
- **Checkpoint 3:** Before declaring a freeze, show the gate report, core metrics, novelty conclusion, clean-run status, and unresolved issues. If the evidence does not support a freeze, say so.
- Never wait passively for future work. Complete everything feasible during the current run, record blocked actions, and leave precise continuation instructions.

# FINAL MESSAGE TO THE USER

At completion, provide:

1. The verified path and download link for the final ZIP.
2. A clear statement: `FROZEN FOR MANUSCRIPT PHASE` or `NOT FROZEN`.
3. A brief audit summary: what changed, which original claims were confirmed/refuted, and which results are reproducible.
4. The final literature novelty judgment, with uncertainty and close prior work named.
5. The primary metrics, intervals, statistical tests, and latency/coverage comparisons directly from generated result files; do not cherry-pick.
6. The number and status of human annotations, if any; never imply annotation was performed when it was not.
7. Every unresolved critical/major issue, missing input, and limitation.
8. Exact steps to share the ZIP with ChatGPT for independent review.

Never report an invented acceptance probability for TACL. This phase assesses research validity and strength, not manuscript acceptance. The next phase—only after the research is frozen and reviewed—will be manuscript preparation and official TACL compliance.

## Start now

Inspect the supplied files, preserve the original project, run Phase 0 and Phase 1, and proceed through every safe and feasible phase. Do not stop at a plan, do not merely produce recommendations, and do not start manuscript rewriting. The primary deliverable is a scientifically defensible, reproducible research package and the verified ZIP for external review.
