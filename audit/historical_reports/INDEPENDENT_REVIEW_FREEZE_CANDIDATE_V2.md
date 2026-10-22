# Independent Review: Cross-Lingual RAG Research Freeze Candidate

**Reviewed artifact:** `CROSS_LINGUAL_RAG_RESEARCH_FREEZE_CANDIDATE_NOT_FROZEN.zip`  
**Review date:** 2026-10-19  
**Decision:** **NOT FROZEN — material methodological and reproducibility blockers remain**

## Executive summary

The archive is much more audit-oriented than the earlier project version. It includes a gate-based status report, processed and raw data, code, prediction records, statistical outputs, a literature audit, annotation materials, figures, and tests. It also correctly discloses that human annotations are missing and that the former test set has already been examined.

However, several reports declare Gates A, B, and D as PASS too confidently. The package has not yet demonstrated that the *corrected experiment* was actually run end-to-end from the included code, its tests are not relocatable, the task-label mapping is scientifically questionable, and the literature audit contains at least one visibly placeholder identifier while omitting a highly relevant cross-lingual fact-verification study. Human annotation remains unperformed.

**Recommendation:** continue research repair. Do not freeze and do not rewrite the manuscript yet. Treat current numerical results as exploratory until a corrected clean rerun and valid task formulation have been established.

---

## Findings, ordered by severity

### P0 — The research task and gold-label mapping need to be re-validated

**Evidence in the ZIP**
- `audit/DATA_AND_LABEL_AUDIT.md` and `protocol/RESEARCH_PROTOCOL_v1.md` map `false`/`mostly false` to `CONTRADICTED`, `true`/`mostly true` to `SUPPORTED`, and `partly true/misleading` to `INSUFFICIENT_EVIDENCE`.
- The audited Hindi subset contains no gold `SUPPORTED` cases: development has 89 `CONTRADICTED` and 14 `INSUFFICIENT_EVIDENCE`; test has 142 and 21 respectively.
- `scripts/run_corrected_experiments.py` uses a three-way NLI verifier and maps its three output labels to those claim-level fact-check labels.

**Why it matters**
`partly true/misleading` describes a mixed or misleading veracity judgment; it is not necessarily equivalent to NLI `neutral` / `insufficient evidence`, which means the premise neither establishes nor contradicts the hypothesis. X-Fact is a multilingual *fact-checking* dataset with fact-checker labels, metadata, and evidence from retrieved news stories; the official paper/repository description does not establish that every fact-checker class can be mechanically converted into FEVER-style evidence-entailment labels. The absent positive class also means the current subset cannot evaluate recall for `SUPPORTED` on the held-out set.

**Required repair**
1. Inspect the official X-Fact paper, data schema, source-specific label maps, and record-level examples.
2. Compare at least three defensible formulations: (a) preserve original X-Fact veracity labels and model claim-veracity classification; (b) independently annotate claim–evidence relation labels for a valid NLI task; (c) use an evidence-verification dataset with appropriate gold support/refute/NEI labels. Do not silently map mixed truth to insufficient evidence.
3. Choose the formulation that actually answers the research question. Document rejected alternatives and remap the data only once the decision is recorded.
4. If no valid gold evidence-relation labels can be obtained, narrow the project to *prediction disagreement / translation sensitivity* and remove causal accuracy/error-attribution claims that require those labels.

**Gate impact:** Gate A is not a full PASS for the intended scientific task until this is resolved.

### P0 — The “corrected ablation results” are not evidence of a corrected inference rerun

**Evidence in the ZIP**
- `experiments/results_corrected/full_benchmark_and_ablations.csv` reports the corrected-looking benchmark and ablation values.
- `scripts/generate_full_ablations.py` reads the older `experiments/results/test_predictions.csv`, recomputes a numeral Jaccard feature on those predictions, and sets `MEAN_MT_LATENCY_MS = 1120.0` as a constant.
- The code that actually reruns the verifier with token-based truncation is `scripts/run_corrected_experiments.py`, which would create `corrected_dev_predictions.csv` and `corrected_test_predictions.csv`; these files are **not present** in the submitted archive.
- The existing `experiments/results/test_predictions.csv` contains the old predictions and old latency columns.

**Why it matters**
The corrected table is a post-hoc recomputation using old model predictions, not proof that the corrected model-input pipeline was run. It cannot support claims that token-based truncation corrected the reported model results. The translation latency value is estimated/fixed, not a per-instance latency measurement from the included run.

**Required repair**
1. Mark old test predictions and all tables derived from them as `LEGACY/EXPLORATORY`.
2. Fix paths and run the actual corrected inference pipeline on development data, tune the trigger only on dev, freeze the rule, and then run the designated evaluation split.
3. Save per-example token lengths, truncation indicators, all logits/probabilities, predictions, risk scores, trigger decisions, and per-stage times.
4. Generate every corrected aggregate table from the corresponding newly produced raw per-example prediction file. Add tests that verify that provenance chain.
5. Do not reuse the fixed `1120 ms` value as measured latency. Measure translation time and pipeline end-to-end latency directly; if only a proxy is available, label it as an estimate and do not call it measured.

**Gate impact:** Gate D is BLOCKED until corrected inference is run and all reported results trace to its outputs.

### P0 — The repository is not portable/reproducible from a fresh extraction

**Observed execution**
I extracted the ZIP into `/mnt/data/crosslingual_freeze_candidate_review` and ran:

```bash
python tests/run_all_tests.py
```

The command failed *before executing any tests* because `tests/run_all_tests.py` points to `C:\Users\Onkar\OneDrive\Desktop\Research_crosslingual_rag_research\tests`. Multiple other scripts use the same machine-specific path. The archive's `TEST_REPORT.md` says 12/12 tests passed, but that result was not reproducible from the ZIP at a new path.

**Affected files include**
- `tests/run_all_tests.py`
- `tests/test_data_integrity.py`
- `tests/test_metrics_and_partitions.py`
- `scripts/phase0_intake.py`
- `scripts/phase1_recompute_all.py`
- `scripts/run_corrected_experiments.py`
- `scripts/generate_full_ablations.py`
- `scripts/create_annotation_sample.py`
- `scripts/evaluate_true_jaccard.py`

The environment reports also expose an absolute Windows user path. `audit/environment_report.json` uses a `ram_disk` field showing 463.36 GB total / 131.62 GB free, which appears to be disk capacity/free space rather than RAM; the field name and measurement should be checked.

**Required repair**
1. Resolve project root from `Path(__file__).resolve().parents[1]` or a documented `--project-root` argument. No script may depend on a named user's home/Desktop path.
2. Run tests from a fresh temporary extraction whose path differs from the original development path. Test both Windows PowerShell and, where feasible, Linux/macOS path handling.
3. Write a clean-run log recording command, commit/hash, Python version, dependency versions, start/end status, and exit code.
4. Correct the environment report fields, remove or redact personal machine paths from public artifacts, and regenerate checksums after edits.
5. Do not claim a passing test suite unless the run log from the packaged project demonstrates it.

**Gate impact:** Gate E is BLOCKED.

### P0 — The held-out test set is no longer untouched

**Evidence in the ZIP**
- `audit/DATA_AND_LABEL_AUDIT.md` discloses that the full 163-item test split was previously evaluated, inspected, and used for exploratory analysis.
- The annotation plan stratifies a sample from that same previously inspected test split based on known prediction-outcome strata.

**Why it matters**
Even though the original threshold is said to have been tuned on development data, repeated test-set inspection and subsequent method/feature changes mean this test set should not be described as a virgin confirmatory evaluation. Reusing it for corrected method selection further weakens confirmatory claims.

**Required repair**
1. Investigate whether the official X-Fact OOD/zero-shot partitions or another public dataset contain suitable examples and valid labels for this task. The official X-Fact repository lists in-domain test, OOD, and zero-shot files; verify actual Hindi sample sizes and label suitability rather than assuming fit.
2. If a valid independent confirmation set exists, pre-register how it will be used before inspecting results. Keep the current 163-item test only as exploratory/legacy analysis.
3. If no valid external data can be used, use a clearly specified nested/repeated validation design to assess sensitivity and label the result as exploratory; do not call re-splitting already-inspected examples a virgin test.
4. Any final claim must accurately state which data were seen during method development.

**Gate impact:** Gate D remains blocked for confirmatory claims until the evaluation design is repaired or claims are formally downgraded.

### P1 — The novelty assessment is premature and misses relevant work

**Evidence in the ZIP**
- `literature/LITERATURE_AUDIT.csv` lists `arXiv:2407.xxxxx` for *All Languages Matter* while marking the record `VERIFIED`.
- The search protocol lists only a small set of searches and broad source filters.
- The literature inventory does not include *XFEVER: Exploring Fact Verification across Languages* (Chang et al., 2023), a directly relevant multilingual fact-verification benchmark paper.
- `literature/NOVELTY_ASSESSMENT.md` still calls the work the “first” controlled error disentanglement / first quantitative measurement, although human causal attribution is pending and the prior-work coverage needs expansion.

**Relevant external records verified during this review**
- Singhal et al., *A Comparative Study of Translation Bias and Accuracy in Multilingual Large Language Models for Cross-Language Claim Verification*, arXiv:2410.10303 / ATTRIB workshop. It evaluates translation approaches and cross-language claim verification across 15 languages using X-Fact. https://arxiv.org/abs/2410.10303
- Chang et al., *XFEVER: Exploring Fact Verification across Languages*, ROCLING 2023; uses translated FEVER data in six languages and discusses cross-lingual verification and prediction-similarity calibration. https://aclanthology.org/2023.rocling-1.1/
- Official X-Fact benchmark description: https://aclanthology.org/2021.acl-short.86/ and https://github.com/utahnlp/x-fact/
- Current Hugging Face model config for mDeBERTa lists `id2label`: 0 entailment, 1 neutral, 2 contradiction. The current numerical mapping appears consistent, but code should verify `model.config.id2label` at runtime rather than relying on an implicit constant. https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7/blob/main/config.json

**Required repair**
1. Re-run the literature audit through ACL Anthology, arXiv, Semantic Scholar/OpenAlex or Crossref, cited-by chains, and relevant workshops; log exact query strings and run date.
2. Replace placeholder IDs with exact primary-source IDs/DOIs/URLs, independently open every source, and remove any record that cannot be verified.
3. Add XFEVER and other close neighbors on cross-lingual verification, translation bias/fidelity, NLI miscalibration, multilingual evidence attribution, and selective prediction/cascades.
4. Build an evidence-based matrix comparing dataset/task, language direction, translated evidence vs translated claims, human fidelity annotation, causal error attribution, selection/fallback, cost accounting, metrics, and limitations.
5. Remove “first” claims by default. Use a bounded statement of the specific gap unless the systematic audit actually establishes priority.

**Gate impact:** Gate B should be marked `INCOMPLETE/PROVISIONAL`, not PASS, until the literature audit is complete and traceable.

### P1 — The routing results do not yet establish a useful efficiency advantage

**Evidence in the ZIP**
- The existing ablation table shows hard-route Selective-Check at 39.26% accuracy and 83.4% original-evidence consultation; direct original-only is 37.42%; the difference is not statistically significant in the current report.
- Numeral-mismatch-only routing is reported at 39.88% accuracy, but consults original evidence on 96.9% of examples.
- Selective average end-to-end latency is reported as about 6.97 seconds versus about 4.80 seconds for direct original-only and 7.74 seconds for Always-Check; however, the end-to-end numbers use a fixed MT-time addition rather than per-run measurement.
- `scripts/generate_full_ablations.py` uses a random Bernoulli mask for routing and reports a rounded mean accuracy as `Correct_Count`, despite not being an actual integer number of correct claims.
- `scripts/run_corrected_experiments.py` sets uncertainty-only threshold percentiles using test-set trigger coverage; the ablation should instead define target coverage from development data and freeze it.

**Required repair**
1. Tune all learnable thresholds and matched-coverage baselines on dev only. Freeze them before confirmatory evaluation.
2. For random routing, choose exactly the development-defined number of items per replicate (or use a precisely specified matching procedure), evaluate many seeds, and report a distribution/CI. Do not call rounded mean correctness a count.
3. Report risk–coverage and accuracy/F1–latency/compute Pareto curves, plus coverage, fallback frequency, median/p95 latency, and cost saved relative to a proper baseline.
4. Compare Selective-Check to translated-only, original-only, always-check, uncertainty-only, numeral-only, matched-coverage random routing, and a clearly labeled oracle upper bound.
5. Pre-register the primary comparison and correct multiple-comparison testing where appropriate. Report paired effect estimates and confidence intervals, not just p-values.
6. If the method does not beat original-only or fails to save measurable cost, frame it as a diagnostic result rather than a superior deployed method.

### P1 — Human annotation is still completely unperformed

**Evidence in the ZIP**
- `annotation/HUMAN_ANNOTATION_REPORT.md`: 50 sampled items; Annotator 1 completed 0; Annotator 2 completed 0.
- `annotation/ANNOTATION_PROTOCOL.md` requires two independent bilingual annotators, third-party adjudication for disagreement, Cohen's kappa, and a 70% confirmation threshold for operational translation-fidelity errors.
- `annotation/internal_audit_sampling_key.csv` exposes which item belongs to which outcome stratum; this key must not be shared with annotators.

**Required repair**
1. Create a separate annotator handoff directory/ZIP containing only the blinded annotation sheet, instructions, and response template—never the internal sampling key, prediction file, or analysis report.
2. Review whether 20 sampled operational translation-recovered examples is enough for a meaningful precision estimate. Justify the validation threshold and sample design before seeing annotations.
3. Obtain actual independent labels from two qualified Hindi–English bilingual annotators and a third adjudicator where needed. AI must not fill those columns or simulate annotators.
4. Report Cohen's kappa and raw agreement, class-specific agreement and a prevalence-robust statistic, plus a confidence interval for the share judged materially `ALTERED`. If sampling is stratified, use appropriate sampling weights for any population-level totals.
5. If annotations cannot be obtained, remove causal statements about translation fidelity and keep the research explicitly exploratory/blocked for those claims.

**Gate impact:** Gate C remains BLOCKED for causal error-attribution claims.

### P1 — The metric and threshold plan is internally inconsistent

**Evidence in the ZIP**
- `protocol/analysis_plan.yaml` specifies a candidate grid `[0.10, 0.65, 0.025]`.
- `scripts/run_corrected_experiments.py` searches `np.linspace(0.15, 0.65, 21)`, whose lower bound differs.
- The script tunes the trigger using three-class macro-F1 even though the gold data have no `SUPPORTED` examples; the documentation says observed two-class and standard three-class metrics should both be reported.
- The report gives a permutation p-value of 0.0370 in one place and 0.0420 in another.

**Required repair**
1. Choose a primary metric only after the label/task mapping is resolved. State exactly which labels are included, how zero-support classes are handled, and why the metric fits the task.
2. Make the YAML protocol, executed code, logs, and reports share the same grid, seed, resampling counts, confidence interval method, and p-value implementation.
3. Recompute all results from a single canonical raw prediction table and regenerate outputs; no hand-edited result summaries.
4. Report paired differences and intervals. Use a prespecified primary comparison and account for multiple secondary comparisons.

### P1 — Licensing, provenance, and local-path hygiene need work

**Evidence in the ZIP**
- `data/DATA_PROVENANCE_AND_LICENSES.md` makes a broad redistribution claim based on MIT licensing and “Fair Use.” The official X-Fact repository itself is MIT-licensed, but that alone does not prove all third-party news text and snippets in derived files can be re-licensed or redistributed under MIT.
- Machine-specific paths and a username appear in reports and scripts.

**Required repair**
1. Separate the license of the X-Fact repository/code from the rights/terms applying to source news text and snippets. Do not offer legal conclusions such as “Fair Use” without a qualified basis.
2. If rights for bundling evidence snippets are unclear, remove raw copyrighted text from the redistributable research ZIP and provide reproducible acquisition/preprocessing instructions, hashes, provenance, and download pointers instead.
3. Store relative paths and environment metadata without personal usernames or home-directory paths.

---

## Current gate assessment recommended by this review

| Gate | Recommended status | Reason |
|---|---|---|
| A — data integrity and task validity | **PARTIAL / BLOCKED** | Split inventory is useful, but the fact-check-to-NLI label mapping and missing positive class are unresolved for the intended task. |
| B — literature and novelty | **INCOMPLETE / PROVISIONAL** | Placeholder identifier, missing close work, and unsupported “first” claims. |
| C — human annotation | **BLOCKED** | 0/50 items annotated; causality claims need human validation or must be removed. |
| D — corrected empirical evidence | **BLOCKED** | Corrected table derives from legacy predictions; corrected inference outputs are absent; evaluation split was inspected; latency is estimated. |
| E — reproducibility and freeze | **BLOCKED** | Test runner fails on clean extraction due absolute paths, and gates A–D are not met. |

## Exact order of work

1. Keep current package immutable and label its outputs legacy/exploratory.
2. Fix project-relative paths and verify an actual clean-extraction test run.
3. Resolve label/task validity before spending more compute.
4. Re-audit the literature and update the bounded contribution question.
5. Pre-register the corrected protocol, metric, primary comparison, threshold strategy, and new evaluation split.
6. Run actual corrected dev inference, tune on dev only, and execute a confirmatory run on valid independent data if available.
7. Complete independent human annotation for the translation-fidelity claim; otherwise narrow the scientific question to prediction disagreement.
8. Regenerate all tables/figures/reports from canonical raw outputs and rerun clean-room reproduction.
9. Create a new ZIP. Freeze only if all required gates have evidence; otherwise name it `NOT_FROZEN` and list the exact blockers.

## External references checked for this review

- X-Fact paper (ACL Anthology, 2021): https://aclanthology.org/2021.acl-short.86/
- Official X-Fact repository (describes in-domain test, OOD, and zero-shot files): https://github.com/utahnlp/x-fact/
- Singhal et al. (2024), cross-language claim verification across 15 languages: https://arxiv.org/abs/2410.10303
- Chang et al. (2023), XFEVER: Exploring Fact Verification across Languages: https://aclanthology.org/2023.rocling-1.1/
- Current mDeBERTa model config (`id2label`): https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7/blob/main/config.json
