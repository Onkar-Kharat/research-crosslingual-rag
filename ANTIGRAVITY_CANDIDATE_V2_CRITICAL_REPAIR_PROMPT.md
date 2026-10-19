# ANTIGRAVITY MASTER PROMPT — CRITICAL REPAIR OF RESEARCH FREEZE CANDIDATE V2

## Role and mission

Act as a rigorous NLP research engineer, reproducibility auditor, experimental methodologist, and literature reviewer. Your task is to repair the current **research artifacts and experimental evidence only** for the project on Hindi–English cross-lingual evidence-grounded claim verification.

The supplied archive is:
`CROSS_LINGUAL_RAG_RESEARCH_FREEZE_CANDIDATE_NOT_FROZEN.zip`

The archive currently says `NOT FROZEN`. Keep it that way until the gates at the end of this prompt genuinely pass. A previous independent review identified material issues; this prompt supersedes any prior instruction that prematurely marked Gates A, B, or D as PASS.

If available, also inspect the accompanying prior files:
- `ANTIGRAVITY_AUDIT_AND_RECOVERY_PROMPT.md`
- `MANUSCRIPT_REVIEW_AND_TACL_READINESS.md`
- `ANTIGRAVITY_RESEARCH_IMPROVEMENT_AND_FREEZE_PROMPT.md`

Treat the current candidate archive plus reproducible evidence as authoritative for the current state. Previous reports are hypotheses to verify, not truth to assume.

## Non-negotiable priorities

1. **Research quality and validity come before manuscript writing.** Do not rewrite the abstract, introduction, related work, conclusion, or TACL manuscript. Do not prepare a submission-ready paper in this phase. You may create research figures/tables needed to diagnose the experiments, but do not update the manuscript.
2. Preserve the supplied archive and extracted original files immutably. Work in a new versioned folder or Git branch. Never delete or overwrite legacy results. Clearly label legacy predictions/results as exploratory.
3. Free tools and public data only. No paid model/API calls or paid services. Ask before destructive actions, unusually large downloads/compute jobs, or materially changing the research question/dataset.
4. Do not invent annotations, results, citations, dataset labels, model outputs, hardware measurements, or completed experiment claims.
5. Every result must trace to code, a data version/hash, a command, a model revision, a config, and raw per-example outputs. Recompute summaries from the canonical raw outputs automatically.
6. Work autonomously on safe, reversible audit and code fixes. Ask the user only when a real human judgement/annotation, meaningful scope decision, or approval is necessary. Do not stop merely because a human annotation task is pending; finish every other feasible research repair, but leave the blocked gate open.
7. If a goal cannot be completed, report the blocker honestly. `NOT FROZEN` is an acceptable and required final status when evidence is insufficient.

---

# PHASE 0 — Create a safe, traceable working copy

1. Inspect every file in the candidate archive and generate a complete file inventory, byte size, SHA-256 hashes, and input manifest.
2. Extract to a new folder with a path different from the developer's former Windows Desktop/OneDrive path. Do not use a fixed path such as `C:\Users\Onkar\OneDrive\Desktop\Research_crosslingual_rag_research` anywhere in code.
3. Create a `legacy/` or equivalent immutable area for pre-correction predictions/tables. Mark `experiments/results/test_predictions.csv`, previous tables, and any outputs derived from them as `LEGACY_EXPLORATORY_NOT_CONFIRMATORY`.
4. Create a new repair log, decision log, experiment ledger, blocker ledger, and status file. Each issue must have an ID, severity, evidence path, reproducible check, fix, test, status, and remaining caveat.
5. Start with a concise Phase 0 report. Continue into Phase 1 without waiting for approval for low-risk fixes.

# PHASE 1 — Make the project portable and reproduce the current archive's checks

The earlier automated test report states 12/12 tests passed. However, running `python tests/run_all_tests.py` from a fresh extraction failed before any tests ran because the project uses hard-coded absolute Windows paths. Independently verify this and repair it.

Requirements:

- Resolve project root relative to each script, e.g. `Path(__file__).resolve().parents[1]`, or accept a documented `--project-root` option. Do not embed machine-specific user paths.
- Fix all scripts, including test runner, data integrity tests, corrected inference, recomputation, ablations, annotation-sample generation, intake, and numeral evaluation scripts.
- Use `pathlib.Path` and UTF-8 explicit file handling; ensure path handling works on Windows and does not fail from a Linux clean-extraction test where feasible.
- Correct `audit/environment_report.json`: verify RAM versus disk values. The current `ram_disk` total/free values appear to describe disk storage, not system RAM. Use distinct named fields for physical RAM, disk capacity/free bytes, CPU, GPU and versions.
- Remove/redact personal usernames and home-directory paths in shareable logs while preserving relevant hardware/software facts.
- Pin and record Python/package versions and exact model/tokenizer revisions. Provide a lock file or equivalent reproducible dependency specification. Avoid claiming exact model reproducibility from a moving `main` branch.
- Run the test suite in the new extracted path, log the exact command, environment, exit code, failures, and timestamp. Add a test that verifies project relocation does not break execution.
- Run the data pipeline's integrity tests, not only unit tests of helper functions. Tests must assert that each report's input files and prediction source match the declared experiment run.

**Acceptance criterion:** a new extraction can run tests from its own root and the test report is produced by that actual run. If tests fail, leave the gate open.

# PHASE 2 — Revalidate the research task and label semantics BEFORE new model runs

This phase is a hard gate. The dataset/task formulation may be scientifically invalid even if the code works.

The current mapping is:
- `true` / `mostly true` → `SUPPORTED`
- `false` / `mostly false` → `CONTRADICTED`
- `partly true/misleading` / `unproven` etc. → `INSUFFICIENT_EVIDENCE`

The current Hindi subset contains no gold `SUPPORTED` examples. Do not automatically assume the mapping above is valid. In particular, **`partly true/misleading` does not necessarily mean NLI-neutral or insufficient evidence**; it can signify mixed veracity. The model's outputs are NLI labels, while X-Fact's gold labels are source fact-checker veracity labels. Prove that the target labels are aligned before scoring the model as an evidence verifier.

Complete the following:

1. Read the official X-Fact paper and repository/data schema, including source-specific label maps. Inspect raw rows and examples from every original class and source.
2. Document exactly what each gold field means, what the evidence snippets contain, how the X-Fact authors derived labels, and whether each class can legitimately be mapped into support/refute/NEI.
3. Compare at least three candidate task formulations:
   - **Option A:** Preserve native X-Fact veracity labels and formulate this as claim-veracity prediction with evidence; do not describe the native labels as evidence-entailment labels without validation.
   - **Option B:** Create a valid claim–evidence relation benchmark using genuine human labels for SUPPORTS / CONTRADICTS / NOT ENOUGH INFORMATION, with a clear annotation unit, adjudication rules, and manageable scope.
   - **Option C:** Use another suitable open benchmark with compatible gold evidence-relation labels, after checking language support, split composition, license/terms, and whether its inputs match this question.
4. Choose the option that best supports the research question. Record alternatives, pros/cons, sample sizes, feasibility, risks, and the decision before proceeding.
5. If there is no defensible ground truth for evidence relation, narrow the study to **prediction disagreement / sensitivity to evidence language**, and explicitly remove causal statements that model disagreements prove translation corruption.
6. The current zero-`SUPPORTED` split cannot measure `SUPPORTED` recall. Decide whether to acquire a valid sample with this class or explicitly scope the evaluation to the classes represented. Do not use three-class metrics as the sole decision criterion when a class has zero gold support.
7. Verify the model's label mapping at runtime with `model.config.id2label`. The published config for `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7` currently maps IDs 0/1/2 to entailment/neutral/contradiction. Map labels from that config explicitly; do not rely on an unexplained hardcoded mapping. Save a machine-readable mapping report.

**Acceptance criterion:** a signed-off `protocol/TASK_AND_LABEL_VALIDITY_DECISION.md` states the chosen target, evidence for validity, the exact gold-label mapping, what inferences are and are not supported, and why rejected task formulations were not selected. No new confirmatory inference should begin before this decision is written.

# PHASE 3 — Complete a real, verifiable literature audit and bound novelty

The current literature audit is not a sufficient basis for a PASS. `literature/LITERATURE_AUDIT.csv` contains a visibly placeholder identifier (`arXiv:2407.xxxxx`) while marking the record VERIFIED, and it omits at least one relevant work: **XFEVER: Exploring Fact Verification across Languages (Chang et al., 2023)**. The audit also cites the very close work by Singhal et al. on translation bias and cross-language claim verification.

Search and verify, at minimum:

- Singhal et al., *A Comparative Study of Translation Bias and Accuracy in Multilingual Large Language Models for Cross-Language Claim Verification*, arXiv:2410.10303 / ATTRIB workshop.
- Chang et al., *XFEVER: Exploring Fact Verification across Languages*, ROCLING 2023, https://aclanthology.org/2023.rocling-1.1/.
- The official X-Fact paper and source-specific label mapping documentation.
- XRAG; CrossRAG / multilingual RAG for knowledge-intensive QA; All Languages Matter; multilingual evidence attribution and NLI; translation quality/fidelity effects on downstream decisions; confidence calibration and selective prediction; model cascades/original-evidence fallback; evidence verification work with human error annotation.

Requirements:
1. Search primary scholarly sources (ACL Anthology, arXiv/OpenReview, publisher/proceedings pages and Crossref/Semantic Scholar/OpenAlex if available) and follow cited-by/reference chains.
2. Record query strings, sources searched, search date, exact canonical URL/DOI/arXiv ID, venue and peer-review status. Distinguish peer-reviewed proceedings, workshop papers, preprints, and blogs.
3. Open every source and verify bibliographic details. No placeholder identifiers, invented venue details or claims of `VERIFIED` without an actual source check.
4. Include a row for every genuinely close neighbor and a detailed nearest-neighbor matrix comparing task, dataset, language pair(s), translated claim versus translated evidence, human translation-fidelity annotation, error-attribution method, selective routing/cascade, latency/cost analysis, and reported limitations.
5. Explicitly distinguish what the close papers already did from what remains unanswered. Do not state “first” unless the systematic evidence supports it. Default to a bounded claim rather than priority language.
6. Do not overstate novelty because a paper uses a different model or dataset. If the current contribution is too incremental, propose a narrower or genuinely new experiment and record that decision before spending substantial compute.

**Acceptance criterion:** all close-neighbor references verified, no placeholder IDs, search process recorded, a novelty memo explains the overlap, and each novelty claim links to evidence. Gate B remains INCOMPLETE until then.

# PHASE 4 — Corrected experiments must actually re-run inference

The file `experiments/results_corrected/full_benchmark_and_ablations.csv` is not a valid corrected-inference result by itself. `scripts/generate_full_ablations.py` reads the legacy `experiments/results/test_predictions.csv`, derives new Jaccard features from it and adds a constant `MEAN_MT_LATENCY_MS = 1120.0`. The corrected inference code `scripts/run_corrected_experiments.py` would create corrected per-example predictions, but those outputs are absent from the archive.

Do not treat `generate_full_ablations.py`'s current output as proof the corrected pipeline ran.

After Phase 2 and protocol freeze:

1. Rerun real inference on development data from the chosen task representation using tokenization exactly as specified. Log input IDs/tokens or sufficient reproducibility evidence, per-input token lengths and whether truncation occurred. Explain how the 512-token limit treats evidence vs claim and keep the rule identical across conditions.
2. Tune all thresholds and choice rules only on development data. The current protocol grid `[0.10, 0.65, 0.025]` conflicts with the script's grid starting at `0.15`. Correct this. The current code tunes using three-class macro-F1 despite the missing positive class; select the primary metric only after Phase 2 resolves the target, and define exactly how zero-support classes are handled.
3. Retune the threshold after any change to risk features, tokenization, MT model, verifier, label mapping, or loss objective. Do not simply reuse `tau=0.30` from the legacy run.
4. Freeze the protocol, threshold, primary comparison, hypotheses, metrics, resampling method and random seeds before evaluation on a fresh confirmation split.
5. Run all key conditions from new predictions:
   - translated evidence only;
   - original-language evidence only;
   - unconditional dual evaluation/consensus with its exact decision rule specified;
   - selective hard routing/fallback;
   - uncertainty-only routing;
   - numeral-only routing;
   - matched-coverage random routing;
   - clearly marked non-deployable oracle upper bound.
6. Tune ablation thresholds/coverage on development data. The current uncertainty-only code derives a percentile from test-set coverage; remove that test-derived tuning. Match random routing by selecting exactly a frozen number of instances based on development-defined coverage. Run many seeds, report mean/SD/intervals; never round a mean accuracy into a fake integer `Correct_Count`.
7. Investigate whether one MT system and one verifier are enough. Prefer a practical robustness check with a second free/open translation system and/or an alternate cross-lingual verifier if license, RAM, and compute allow. First run a small pilot and estimate cost. If not feasible, document the single-model scope and do not generalize beyond it.
8. Check probability calibration because the risk trigger uses maximum class probability. Report calibration/reliability evidence or justify a simpler uncertainty measure. Analyze risk–coverage performance across thresholds.
9. Save per-instance raw output for every system: item ID, gold label, all model probabilities, prediction, input lengths/truncation, risk features, chosen route, and stage timings. Pin model and tokenizer revisions. Keep test gold hidden from all threshold/hyperparameter selection.
10. Generate `corrected_dev_predictions.csv/jsonl`, evaluation predictions, and outputs with unique run IDs. Make result scripts consume only those outputs; assert their run ID and config hash. Do not silently blend old and new records.

**Acceptance criterion:** the new prediction files actually exist, came from a logged run of the corrected code, and all corrected aggregate tables are generated directly from those exact files. If the script cannot run in the available environment, record the exception and do not claim corrected results.

# PHASE 5 — Repair evaluation design and statistics

The current test set was already evaluated and inspected. It cannot be described as a virgin test set. The current ablation results also show only a small, non-significant observed improvement over original-only in the old run, and the latency advantage is not established by real end-to-end timings.

1. Investigate official X-Fact OOD and zero-shot splits and other suitable open benchmarks. Verify real language counts, labels, task compatibility and redistribution/terms before selecting one. Do not assume OOD/zero-shot data contain enough relevant Hindi examples until measured.
2. Select a valid independent confirmation set, or explicitly narrow conclusions to exploratory evidence if no independent data are suitable. Do not call a new random split of previously inspected examples a virgin external test.
3. Pre-register one primary contrast. Likely choices include selective vs translated-only or selective vs always-check; decide based on the actual intended claim rather than whichever comparison yields significance. Treat selective vs original-only honestly and do not claim superiority if it is not supported.
4. Recompute exact sample point estimates from the final canonical predictions. Compute confidence intervals and paired differences. Align all statistical code and reports: current files disagree about a permutation p-value (0.0370 vs 0.0420).
5. Use exact paired McNemar tests for accuracy where appropriate; use a documented paired permutation procedure for F1, with a nonzero finite-sample correction (e.g. plus-one p-value), and a fixed seed. Correct for multiple secondary comparisons (e.g. Holm). Report effects and confidence intervals, not only p-values.
6. Consider clustered resampling by underlying article/source/event if multiple instances are dependent; document the chosen resampling unit and assumptions.
7. Report per-class precision/recall/F1 and confusion matrices, class support, observed 2-class metrics when valid, and any standard 3-way diagnostic metric separately. Avoid a performance narrative based only on accuracy.
8. Add sensitivity analysis for metric choice, threshold/coverage, model variation and label uncertainty. A weak or null result is a valid research outcome; do not adjust protocol post hoc to make the proposed method look better.

# PHASE 6 — Correct the latency/cost study

Current outputs use a fixed `1120 ms` MT-time constant in the ablation script, and reports inconsistently mix verifier-only and end-to-end latencies.

- Measure actual translation runtime and inference runtime on the same declared hardware. Include warm-up, number of repeats, batch size, software/model versions, and whether the translator is cached.
- Measure per-instance MT time, translated verification time, original verification time, risk-feature computation and overall pipeline time for each condition. For selective fallback, time both the initial translate+verify stage and the conditional original-language verifier stage.
- Report mean, median, standard deviation and p95 latency; separate model-only from end-to-end latency. Clearly identify whether disk/cache/model loading is included.
- Do not claim throughput benefit merely because fewer original-evidence calls are made. Compare accuracy and cost on a Pareto curve against translated-only and original-only baselines. If selective fallback is slower than direct original-only under the actual setup and does not improve accuracy significantly, say so.

# PHASE 7 — Human annotation workflow (cannot be automated dishonestly)

The package says `0/50` annotations are complete. The prior annotation design samples 20 operational translation-recovered cases, 20 cases where both methods fail, and 10 both-correct controls from a test set whose predictions have already been examined.

1. Do not populate annotation fields yourself and do not ask another AI to fabricate human judgments.
2. Create `annotation_handoff/ANNOTATOR_PACKET.zip` containing only the blinded annotation CSV, annotation guide/protocol, instructions and a blank output template. Do not include `internal_audit_sampling_key.csv`, prediction files, strata names, or internal review reports. Keep the internal key separately.
3. Audit sample size, sampling design and the 70% pass threshold before annotation starts. Explain the estimand: whether the goal is precision of the operational `E_trans` heuristic among sampled cases, overall error rates, or class/stratum comparisons. Use appropriate sample weights if estimating totals from stratified samples.
4. Obtain two genuinely independent qualified Hindi–English bilingual annotators. Third adjudicator resolves disagreements. Record annotator qualifications at an appropriate non-identifying level and annotation dates. Human-provided responses must be stored exactly before analysis.
5. Compute Cohen's kappa and raw agreement, per-class/positive agreement, an additional prevalence-robust statistic such as Gwet AC1 where suitable, and confidence intervals for the `ALTERED` proportion. Predefine treatment of missing/disputed labels.
6. The previously inspected test-based annotation sample validates the operational label only; it does not create a fresh confirmatory test set.
7. If human annotation is not returned, keep Gate C `BLOCKED`. You may continue every other repair, but may not state that translation-fidelity cases are causally validated. An alternative is to narrow the contribution to model prediction disagreement and remove causal wording; document the scientific trade-off for the user's decision.

# PHASE 8 — License, provenance and artifact hygiene

1. Re-check upstream licenses/terms for the X-Fact repo, model weights, translation model, and included source-news snippets. The repository's MIT license does not automatically prove every third-party snippet in derived files is itself MIT-licensed. Do not make blanket legal claims such as “Fair Use” without a defensible basis.
2. If redistribution permission is unclear, exclude third-party text from the public research ZIP and include documented acquisition instructions, original source pointers, schema, hashes and preprocessing scripts instead.
3. Redact personal machine paths, usernames and unnecessary local metadata.
4. Include a `DATA_USE_AND_LICENSE_NOTES.md` that distinguishes code licenses, model licenses, dataset terms, and underlying source-text rights. Do not present legal advice.

# PHASE 9 — Final independent clean-room reproduction

Create a completely new directory from the final candidate ZIP, at a location different from the working directory. Create a clean virtual environment using the documented supported Python version and install pinned dependencies. Run the entire documented pipeline in order without reading hidden local paths or relying on untracked files.

The reproduction run must:
- verify checksums;
- validate the raw/processed dataset mapping;
- recreate translations or verify translation cache hashes/revisions;
- rerun inference from defined models;
- retune the method on dev only;
- generate new prediction records and all tables/figures automatically;
- run tests from the extracted project root;
- reproduce reported metrics and statistical tests within stated deterministic tolerance;
- show every command, exit status and output path in a clean-run log.

Do not accept a prefilled `TEST_REPORT.md` as evidence. Regenerate it during this actual run.

# REQUIRED FINAL DELIVERABLES

Create a new versioned ZIP, e.g. `CROSS_LINGUAL_RAG_RESEARCH_FREEZE_CANDIDATE_V3_NOT_FROZEN.zip` unless every gate truly passes. Include:

1. `README_RESEARCH_REPAIR.md` with a one-command clean reproduction path.
2. `RESEARCH_STATUS.md` and gate evidence table.
3. `BLOCKER_LEDGER.csv` with all open issues and owners (Agent / Human / Approval).
4. `DECISION_LOG.md` and frozen protocol/analysis YAML with version and timestamp.
5. Validated dataset card, provenance, mappings, label analysis and license notes.
6. Full audited literature CSV/matrix/search log and bounded novelty memo.
7. Actual corrected per-example development and evaluation predictions, not only aggregated metrics.
8. Recomputed results, confusion matrices, paired tests, confidence intervals, ablations and latency measurement logs.
9. Figure source files plus generated images/PDFs that directly reflect the latest valid data.
10. Human annotation handoff packet without the internal sampling key, plus annotation analysis script and explicit pending/complete status.
11. Portable source scripts, dependency lock/specification, tests and clean-room run log.
12. `MANIFEST_SHA256.txt` with checksums for the final package contents.
13. No rewritten manuscript. Keep the old manuscript only as a clearly marked legacy input if it is part of the supplied project; do not edit it in this phase.

## FINAL GATES — DO NOT OVERRIDE THEM

- **Gate A: Task/data validity** — raw labels, label mappings, missing classes, sample composition and task semantics are defensible and documented.
- **Gate B: Literature/novelty** — close work verified, no placeholders, bounded and evidence-supported contribution.
- **Gate C: Annotation/claim validity** — genuine human annotation completed for causal translation-fidelity claims, OR the research question is explicitly narrowed to non-causal prediction disagreement and corresponding causal claims are removed.
- **Gate D: Empirical evidence** — corrected inference actually rerun, evaluation plan frozen, valid independent confirmation or explicitly exploratory scope, full ablations/statistics/latency from raw output.
- **Gate E: Reproducibility** — clean ZIP successfully tested from a new path; outputs trace back to run IDs/configs/hashes.

Do not set any Gate to PASS based only on an earlier report. Point to concrete artifact paths, commands, and outputs. If a gate depends on an actual human action or a decision that cannot be automated, label it BLOCKED and state precisely what is needed.

When finished, provide the user a concise but complete status summary: what changed, what was rerun from scratch, what passed/failed, research decisions required from the user, human annotation status, the exact final ZIP filename, and the SHA-256 checksum. The result should be an improved research package, not a polished manuscript.
