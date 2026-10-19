# Antigravity Master Prompt: Audit, Repair, Reproduce, and Reassess the Existing Cross-Lingual Verification Paper

## Mission

You are taking over an **existing research project**, not starting a new paper from a blank template. The project folder is `research-crosslingual-rag-main/`. The current manuscript is `main.pdf` / `manuscript/main.pdf`, and the ZIP contains the LaTeX source, processed data, translated data, predictions, scripts, figures, logs, and reports.

Your primary job is to **independently audit the current work, identify and fix scientific/reproducibility flaws, rerun the affected analyses, and only then decide whether a defensible TACL paper remains**. Do not treat a completed `STATUS.md`, an optimistic mock review, a compliance checklist, or a final-readout document as proof. Inspect the source data, implementation, predictions, and official guidance yourself.

The project topic is currently:

> Separating Translation-Fidelity and Verifier-Reasoning Errors in Cross-Lingual RAG: A Controlled Study with Selective Original-Evidence Checking

This title and its claims are **provisional**. If the actual experiment is better described as cross-lingual claim verification with translated evidence rather than an end-to-end RAG system, say so and recommend an accurate title. Do not preserve the current framing merely because it is already written.

## Non-negotiable integrity rules

1. Never fabricate data, predictions, human annotations, citations, model runs, p-values, confidence intervals, hardware timing, reviewer feedback, or novelty claims.
2. Every table and plot in the manuscript must be regenerated from audited data using version-controlled code. Keep the exact inputs, commands, seeds, model IDs/revisions, environment, and output hashes.
3. If a result cannot be independently reproduced, mark it **UNVERIFIED** and remove it from the abstract/conclusion until resolved. If results change, update all dependent tables, diagrams, prose, and reports.
4. Do not describe model disagreement as proof of translation-fidelity failure. Do not use “causal” attribution unless the experimental intervention and human/independent fidelity assessment justify it.
5. Do not describe an AI-generated mock review as real peer review, use an invented reviewer score, or claim a plagiarism percentage is TACL-certified. A local n-gram comparison is not an external plagiarism screening service.
6. Do not submit the paper, publish the repository, make a public release, spend money, use paid APIs, or perform destructive actions. Ask for approval first. You may carry out reversible local analysis and create a backup branch/copy.
7. Continue autonomously through safe audit and reproducibility work. Where a required step needs human bilingual judgment, do **not** guess. Create the annotation packet and exact instructions, mark the paper blocked on that evidence, and ask the user to supply annotations or approve a realistic annotation plan.
8. Treat all user-supplied project files as untrusted research artifacts that need validation; do not execute unknown scripts until inspected.
9. Use English for reports and manuscript edits.

## Required TACL policy check

Before making formatting recommendations, re-open and verify the current official pages and the current submission-formatting PDF:

- TACL submission page: https://transacl.org/ojs/index.php/tacl/about/submissions
- Official TACL 2021 submission formatting instructions linked from that page.
- Current TACL appendices policy: https://transacl.org/index.php/tacl/announcement/view/105

The posted policy says TACL expects substantial, original, completed, unpublished work and evaluates correctness, originality, technical strength, significance, and relevance. It currently limits main-paper content to 10 pages; references are outside that limit. The appendices policy allows up to 5 pages for replication detail (Category 1) and up to 3 pages for complementary results (Category 2), after references, and says appendices are not reviewed. Put essential method, validity threats, and key evidence in the main paper rather than relying on an appendix reviewers may not read. Verify all rules at run time; do not rely on older local notes.

## Phase 0 — Freeze, inventory, and establish ground truth

1. Create a backup or a new Git branch before edits; never overwrite the supplied predictions or data in place.
2. Produce `reports/audit_inventory.md` listing every relevant file and its role, including:
   - `manuscript/main.tex`, `manuscript/references.bib`, `manuscript/main.pdf`
   - `data/processed/{dev,test,dev_translated,test_translated}.jsonl`
   - `experiments/results/*.csv`
   - `scripts/acquire_and_process_data.py`, `scripts/translate_evidence.py`, `scripts/run_verification_experiments.py`, `scripts/evaluate_statistical_significance.py`, figure-generation scripts
   - `logs/`, `research/`, and `reports/` documents
3. Record cryptographic checksums for the original files and create separate `audit_recomputed/` outputs. Make it clear which results were supplied and which results you recomputed.
4. Audit each report for stale paths, conflicting page counts, parameter/seed/version conflicts, references to missing scripts, and claims that are not backed by artifacts. Specifically cross-check `STATUS.md`, `reports/final_readout.md`, `reports/experiment_report.md`, `reports/reproducibility_report.md`, `reports/tacl_compliance_checklist.md`, `reports/mock_tacl_review.md`, and `reports/plagiarism_similarity_audit.md`.
5. Do not accept the existing “100% compliant”, “ready for submission”, “accept with minor revision”, or “1.4% plagiarism” declarations without independent evidence. Correct or clearly relabel inaccurate internal reports.

## Phase 1 — Mandatory data, label, and split audit

Write and run a standalone audit that loads every JSONL/CSV and reports counts, schema validity, source IDs, duplicate claims, duplicate evidence, split overlap, raw labels, mapped labels, empty/truncated evidence, translation cache status, and output/model prediction consistency.

### Issues already indicated by the supplied artifacts — independently verify them

- In `data/processed/test.jsonl` and `experiments/results/test_predictions.csv`, the test labels appear to be only `CONTRADICTED` (142 items) and `INSUFFICIENT_EVIDENCE` (21 items), with **no gold `SUPPORTED` examples**. The dev set appears similarly to have only 89 `CONTRADICTED` and 14 `INSUFFICIENT_EVIDENCE` labels. Confirm these counts from raw and processed benchmark files. Do not call this a representative three-class evaluation without addressing the missing gold class.
- The raw labels appear to be only `false`, `mostly false`, and `partly true/misleading`. The code maps `partly true/misleading` to `INSUFFICIENT_EVIDENCE`. Verify this mapping against the original X-Fact task, paper, annotations, and relevant prior practice. Do not assume that “partly true” or “misleading” means evidence-insufficient. Add a label-mapping table and justify every mapping. Fail loudly on an unknown source label instead of silently mapping it to `INSUFFICIENT_EVIDENCE`.
- Verify that the official split is appropriate for the scientific question, that there is no overlap across dev and test, and that the source-level/claim-level grouping assumptions are true in the actual code (not only mentioned in YAML).
- The NLI model’s real `config.json` labels and premise/hypothesis convention must be checked at run time. Confirm the output mapping from `entailment/neutral/contradiction` to task labels rather than trusting a hand-written mapping.
- Verify exactly what text the verifier and translator receive. The present scripts appear to slice evidence using character counts (`[:1000]` and `[:512]`) before tokenization, while the manuscript describes a 512-token limit. Make preprocessing token-based, explicit, consistent, and saved so the exact input strings can be inspected.
- Verify that the original evidence actually corresponds to the intended source snippets; document how five evidence fields are combined and whether the resulting bundle includes repeated claim text, source headlines, or explicit verdict cues.

**Required decision:** If no supported examples are available, either find and license an appropriate broader sample, redesign the experiment honestly as a two-class/subset study with a defensible mapping, or stop claiming a general three-class study. Do not synthesize fake supported examples. Do not tune or select the test set to improve results.

## Phase 2 — Mandatory code/results consistency audit

Independently reproduce all metrics directly from `experiments/results/test_predictions.csv`. Create `scripts/audit_current_results.py` (or equivalent) that asserts:

- Every split has the expected unique item count.
- Each `correct_*` field equals `(prediction == gold_label)` row by row.
- Flip, helpful-flip, harmful-flip, trigger, coverage, and latency fields equal what their definitions say.
- Every table value equals a metric recalculated from the saved predictions, using clear definitions and stable rounding.
- Every figure’s source data equals the table/source predictions from the same run.

### Numerical checks already indicated by the supplied prediction CSV — reproduce them

For 163 held-out items, the saved predictions imply:

- No-Check translated: 52 correct / 163 = **0.3190 accuracy**.
- Direct original evidence: 61 / 163 = **0.3742 accuracy**.
- Always-Check: 51 / 163 = **0.3129 accuracy**.
- Selective-Check: 64 / 163 = **0.3926 accuracy**.

The supplied `test_main_results.csv` reports bootstrap-resample means as the point estimates (for example, `0.320184` for No-Check) rather than the direct observed test accuracy. Use direct observed metrics as point estimates and bootstrap only for intervals. Recalculate all Macro-F1 values from raw predictions as well.

The manuscript calls the confidence intervals “cluster bootstrap,” but the current implementation seems to resample individual rows, not clusters. Correct the terminology or implement a defensible cluster bootstrap based on a justified unit (such as source/claim cluster); explain the unit and limits. Consider at least 10,000 resamples or justify another choice. Do not merely change the caption to sound stronger.

## Phase 3 — Fix the error taxonomy before making claims

The current script contains `crit_trans_error` but appears not to use it in the attribution. It labels translation-fidelity errors primarily when a translated prediction is wrong and the original-language prediction is right. That outcome alone does **not** prove that the translation changed factual meaning: the verifier may behave differently across languages for other reasons.

The supplied category counts appear to be:

- Translation-fidelity errors: 41
- Verifier-reasoning failures: 61
- Evidence-insufficiency cases: 12
- Total No-Check errors: 111

The categories sum to 114, not 111. There appear to be **3 overlapping cases**, because a wrong translated prediction with a correct original prediction can also have an `INSUFFICIENT_EVIDENCE` gold label. Recompute the overlap and provide a mutually exclusive accounting or explicitly describe overlapping diagnostic flags. Never present non-mutually-exclusive categories as a partition; their percentages cannot be described as a complete 100% breakdown.

The current method also seems to equate the gold claim-veracity label `INSUFFICIENT_EVIDENCE` with “the retrieved evidence snippet is insufficient.” These are not automatically the same construct. Define and annotate them separately.

### Human/independent fidelity evaluation is required for an error-attribution claim

Build an annotation schema and blind annotation spreadsheet for the Hindi source evidence and English translation. At minimum include:

- semantic fidelity: `PRESERVED`, `MINOR_VARIATION`, `CRITICAL_ERROR`, `UNCLEAR`;
- error types: negation/polarity, entity, number/quantity, date/time, relation, modality/uncertainty, qualifier, omission, addition, coreference, other;
- whether a difference is claim-critical; annotator confidence; evidence span; rationale;
- whether the original evidence itself is enough to support/refute the claim;
- whether the model was correct under each condition (keep these outputs hidden from annotators until the primary labels are completed, where feasible).

Prefer two independent bilingual annotators on the planned evaluation set or a justified, stratified subset; report inter-annotator agreement and adjudication. If no human annotations are provided, the manuscript must report only **prediction-disagreement/outcome patterns** and remove unverified claims of translation-fidelity causality. Never invent annotation labels or agreement statistics.

## Phase 4 — Resolve the selective-check method/code/diagram mismatch

The manuscript/figure text appears to say that Selective-Check consults the original evidence and **averages posterior distributions**; `apply_selective_checking()` in the current code instead chooses the original prediction when triggered and the translated prediction otherwise. These are different algorithms. Decide which method is scientifically intended, document it exactly, implement that method, and rerun everything. If useful, compare them as two separate baselines rather than conflating them.

Additional checks:

- The current `feature_number_overlap` calculation appears to be intersection size divided by the number of original numbers, not Jaccard overlap, while the paper names it Jaccard. Correct the computation or the wording consistently.
- Make sure routing features are available at routing time and do not leak labels or test information. Explicitly define uncertainty, number mismatch, and any entity/lexical features. Ablate uncertainty-only, numeric-only, and combined triggers.
- Tune the threshold on development data only. Freeze it before test. Report threshold-selection objective, why its cost penalty is meaningful, sensitivity to the penalty, and the full risk/coverage/performance curve. Avoid overstating a single tuned point.
- Compare translated-only, original-only, always-check, and selective routing. Any posterior averaging baseline requires a justification or calibration check. A method that costs more and performs no better than direct original verification must not be described as a latency/cost win.
- `latency_trans_ms` appears to time verifier inference on already translated text, not the machine-translation step. Recompute **end-to-end** latency for a real routed implementation, including translation, initial verification, and fallback verification as appropriate. Report warm-up, hardware, batch size, repetitions, and uncertainty. Do not present a proxy as measured whole-pipeline latency.
- The threshold presently appears to route about 136/163 = 83.4% of test items. Report this as consultation coverage and examine whether the saved cost is meaningful.

## Phase 5 — Build a credible experimental design

After the data and method audits pass, propose a preregistered/locked protocol and implement experiments that are feasible on the detected local hardware. At a minimum:

1. Establish baselines with clear input/output definitions and no test-driven method changes.
2. Add a human-corrected translation condition or another independent fidelity control if it is needed to distinguish translation from verifier effects.
3. Use more than one translation system and more than one verifier if feasible, or explain clearly why the study is intentionally limited and reassess whether it reaches the TACL contribution bar.
4. Consider at least one additional language pair only if licensed data and reliable evaluation are available. If it is infeasible, make the narrow scope explicit and do not generalize to multilingual RAG broadly.
5. Run feature ablations, sensitivity analyses, per-label results, confusion matrices, flip direction analysis, translation-error-category analysis, and cost/coverage curves.
6. Choose statistical tests before looking at test results. For paired comparisons, report discordant pairs and suitable paired tests; account for multiple comparisons where needed. Use adequate resampling and report intervals honestly.
7. Check calibration before averaging posterior distributions. Include simple baselines (e.g., original-only, translated-only, uncertainty-only routing) so the proposed cascade must earn its complexity.
8. Calculate an appropriate sample size/precision goal from pilot results. A 163-item test set with no gold examples of one class is not a strong basis for broad three-class conclusions.
9. Keep negative findings. If the selective method does not reliably outperform baselines, report that and reformulate the contribution around the verified diagnostic result rather than manufacturing a success story.

Before any model download above 2 GB, large experiment, or expensive operation, report the estimated disk/RAM/time requirement and get approval. Use free tools and public/licensed data only.

## Phase 6 — Literature audit and novelty reassessment

Perform a fresh, traceable literature search up to the run date using primary sources (ACL Anthology, journal/conference proceedings, arXiv/OpenReview when necessary, and official model/dataset pages). Do not make the literature table by checking only one known URL per known paper. Save queries, dates, result lists, inclusion/exclusion reasons, source URLs, and verified bibliographic metadata.

Pay special attention to:

- Singhal et al., *A Comparative Study of Translation Bias and Accuracy in Multilingual LLMs for Cross-Language Claim Verification* (arXiv:2410.10303 / its current publication status).
- XFEVER and related cross-lingual verification work.
- X-Fact and later fine-grained multilingual claim-verification papers.
- Cross-lingual RAG evidence translation, translation evaluation, NLI errors, translation robustness, abstention/selective prediction/cascades, and factuality verification.

For every nearest neighbor, compare the exact task, unit of analysis, evidence source, languages, model/translation conditions, error labels, use of human annotation, selective policy, metrics, and result. State clearly what is new over the closest work. If the novelty is not sufficiently distinct, propose a narrower or different question before spending time on further experiments. Do not use “first,” “unexplored,” or “causal” unless the documented evidence supports the exact claim.

## Phase 7 — Rewrite manuscript only after the scientific gates pass

Do not simply patch the existing abstract to preserve the old numbers. Rebuild the claims from verified results. Required sections:

- a narrow, evidence-supported problem definition;
- prior-work comparison centering on the closest papers;
- transparent data provenance and correct gold-label construction;
- operational definitions for error types and a clear distinction between model disagreement, translation fidelity, and evidence insufficiency;
- reproducible system description, exact model revisions and input ordering/truncation;
- baselines and fair comparisons;
- result tables built from current outputs;
- qualitative cases selected with stated rules, including counterexamples/negative outcomes;
- statistical uncertainty and threats to validity;
- limitations and ethical considerations;
- anonymous data/code availability statement with only working, non-identifying links when allowed by TACL rules;
- reproducibility details in appendix where appropriate, while keeping essential evidence in the main paper.

Figures must be generated from actual source data. At minimum, create a simple readable pipeline diagram, a condition/performance plot with intervals, a risk-coverage curve, and an error analysis plot only if the error labels are valid. Simplify the crowded existing workflow figure; ensure figure text is readable at print size and not reliant only on color. The current figure and prose saying “consult original evidence and average” must match the implemented algorithm.

## Phase 8 — TACL format, PDF, and package checks

- Use the official TACL template/style linked from the current site, not an improvised or stale format.
- Verify A4, two columns, required line numbers and confidentiality header, title placement, anonymization including PDF document metadata, citations/references, no figures/tables on page one, and readable figure/table text.
- Verify the main content page count and appendix page limits under the current policy. Appendices are not reviewed: move material needed to judge correctness/novelty into the main text.
- The current PDF has 10 pages and appears to leave page 9 almost blank except for a split bibliography entry; fix pagination professionally without altering font or margins improperly.
- Re-render the final PDF and inspect every page at readable resolution for clipping, overlap, broken references, unreadable figures, or accidental identity leaks.
- Run a clean build from documented instructions in a clean environment where feasible. The current reproducibility report references `scripts/preprocess_xfact.py`, but the supplied ZIP appears to contain `scripts/acquire_and_process_data.py` instead; correct commands to real files and verify clean-checkout execution.
- Reconcile conflicting reports: one file says 8 pages while the supplied PDF is 10 pages; the pilot config says seed 17 while the run manifest says 42; the paper/report describe conditions that do not match the code. Recreate reports from current, verified outputs.

## Required deliverables

Place new outputs in `audit/` or `reports/revised/`; preserve all original artifacts in the backup. Deliver:

1. `audit/INITIAL_AUDIT_FINDINGS.md`: severity-ranked findings and evidence paths.
2. `audit/DATA_LABEL_SPLIT_AUDIT.csv` plus a readable summary.
3. `audit/RESULTS_RECOMPUTATION.md` and machine-readable recomputed metric tables.
4. `audit/METHOD_CODE_CROSSWALK.md` mapping every manuscript formula/condition/claim to the code that implements it.
5. `audit/ANNOTATION_GUIDE.md` and an annotation template if human bilingual labels are needed.
6. `audit/LITERATURE_AUDIT.md` and a source matrix with verified citations and search decisions.
7. Updated experiment protocol and script/config versions with exact commands and checksums.
8. Updated manuscript LaTeX, references, generated figures/tables, compiled PDF, and page-by-page PDF inspection checklist **only after the scientific gates pass**.
9. `audit/TACL_READINESS_REPORT.md`: Pass/Fail/Blocked for each criterion, with evidence, no generic “100% compliant” declarations.
10. `audit/DECISION_AND_NEXT_STEPS.md`: whether to proceed, narrow/reframe, or abandon the current hypothesis, and what human input/approvals are needed.

## Checkpoints and stop conditions

### Gate A — Initial audit only
First run the inventory, dataset/label audit, code/results cross-check, and review of official TACL requirements. Produce a concise severity-ranked report. Do not start new large model runs before reporting this checkpoint.

### Gate B — Scientific validity
Proceed only after the label mapping, method/code consistency, error taxonomy, and baseline definitions have been corrected. If human annotation is necessary and unavailable, stop claims that require it and ask for the next input.

### Gate C — Reproducible experiments
Rerun from clean scripts. Require all tables, saved predictions, and figures to agree exactly within stated numerical rounding. If they do not, debug and rerun.

### Gate D — Novelty and journal-fit review
Write a skeptical TACL-style decision memo using the actual corrected paper. Do not assign pretend reviewers or fabricate “accept” scores. Assess correctness, originality, technical strength, significance, and relevance and identify the strongest possible rejection argument.

### Gate E — Submission readiness
Only recommend submission if all critical audit issues are resolved, results are reproducible, the contribution remains distinct after literature review, and current TACL requirements have been checked. Otherwise recommend further work or a better-fit venue, with reasons. Never submit without the user's explicit approval.

## First message to execute

Start Gate A now. Inspect the files, run the independent data/results audit, check the official TACL guidelines, and produce the severity-ranked audit report. Do not rewrite the abstract yet. Do not assume the current results are correct. After Gate A, tell me the critical blockers, which ones you fixed automatically, which ones require human annotation or approval, and the exact recommended next step. Then continue according to the gates above without inventing any evidence.
