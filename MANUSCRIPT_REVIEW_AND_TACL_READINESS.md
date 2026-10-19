# Independent Initial Review: Cross-Lingual Claim Verification Manuscript

**Files inspected:** supplied `main.pdf` and `research-crosslingual-rag-main.zip` (including manuscript source, data, predictions, scripts, generated tables, figures, logs, and project reports).  
**Date:** 16 October 2026  
**Purpose:** preliminary technical audit, not peer review and not an acceptance prediction from TACL.

## Overall decision

**Do not submit the current version.** The research question may still be salvageable, but the current saved artifacts contain material inconsistencies between the scientific claims, code, and data. The paper needs a correctness/reproducibility repair before prose improvements. Because TACL judges substantial original work on correctness, originality, technical strength, significance, and relevance, these issues directly threaten review readiness (official TACL guidance: https://transacl.org/ojs/index.php/tacl/about/submissions).

## Critical and high-severity findings

### 1. The test set is not a three-class evaluation

A direct count of `data/processed/dev.jsonl`, `data/processed/test.jsonl`, and `experiments/results/test_predictions.csv` shows:

- Dev: 103 items; 89 `CONTRADICTED`, 14 `INSUFFICIENT_EVIDENCE`, zero gold `SUPPORTED`.
- Test: 163 items; 142 `CONTRADICTED`, 21 `INSUFFICIENT_EVIDENCE`, zero gold `SUPPORTED`.
- The raw labels present in these splits are `false`, `mostly false`, and `partly true/misleading`.

The current code maps `partly true/misleading` to `INSUFFICIENT_EVIDENCE`. This mapping needs to be justified against X-Fact's label scheme; “partly true” or “misleading” is not automatically equivalent to “evidence insufficient.” Until that is checked, the gold labels and all downstream metrics are questionable. Even if this mapping can be justified, the test data has no positive/supported class and does not support broad three-class claims. Do not synthesize a missing class. Either expand to a defensible licensed sample with class coverage or reframe the task and claims honestly.

### 2. Error-category counts overlap and are not a valid partition

The current script defines translation-fidelity errors as translated prediction wrong + original prediction correct; verifier errors as both wrong with non-`INSUFFICIENT_EVIDENCE` gold; and insufficiency cases as insufficient gold + translated prediction wrong. These conditions overlap when the gold label is insufficient and the original prediction is correct.

The saved report gives 41 + 61 + 12 = **114 cases**, while the total number of translated-pipeline mistakes is **111**. An independent calculation finds **3 overlapping cases** between the “translation-fidelity” and “insufficiency” categories. The manuscript calls these mutually exclusive and reports shares summing to 102.7%, which is mathematically inconsistent.

More fundamentally, disagreement between predictions on original and translated text does not establish that translation altered the underlying meaning. The code computes `crit_trans_error` but does not use it; no independent bilingual human assessment of translation fidelity appears in the artifact set. Until fidelity is annotated, rename these as outcome-based disagreement patterns and remove causal attribution claims.

### 3. Selective-Check prose/diagram and executable code describe different algorithms

The manuscript and workflow diagram say that a triggered case consults original evidence and averages the two posterior distributions. In `scripts/run_verification_experiments.py`, `apply_selective_checking()` instead selects `pred_original` when triggered and `pred_translated` otherwise; it does not average posteriors. This is a method-definition mismatch, not a cosmetic wording problem. Pick and document the actual intended algorithm, then regenerate the results, tables, figures, and text.

### 4. Point estimates and confidence-interval descriptions need correction

Recalculation from `experiments/results/test_predictions.csv` gives the following exact test accuracies:

| Condition | Correct / test N | Direct test accuracy |
|---|---:|---:|
| No-Check (translated) | 52 / 163 | 0.3190 |
| Direct original evidence | 61 / 163 | 0.3742 |
| Always-Check | 51 / 163 | 0.3129 |
| Selective-Check | 64 / 163 | 0.3926 |

The supplied `test_main_results.csv` uses finite bootstrap-resample averages as the headline metric point estimates; for example, it reports No-Check accuracy as 0.320184 rather than the directly observed 52/163 = 0.319018. Point estimates should be calculated from the actual saved test predictions; bootstrap resampling should be used for intervals. Recompute Macro-F1 point estimates directly as well.

The manuscript labels confidence intervals as “cluster bootstrap,” but `bootstrap_metric_ci()` samples individual rows. Either implement a defensible cluster bootstrap with a justified cluster definition or correct the description. The current code also uses only 1,000 resamples; consider 10,000 or justify a smaller count and report uncertainty honestly.

### 5. Latency/cost comparison is not end-to-end

The experiment timings in `test_predictions.csv` appear to measure verifier inference on pre-translated text, not the machine translation needed to create it. The manuscript compares these numbers as pipeline latencies even though MT was run and cached separately. This biases the reported cost comparison. A real selective implementation also needs to be timed as routed, including translation and fallback checks. Report measured wall-clock end-to-end timing, the hardware, warm-up, repetition count, and uncertainty. Also compare the method against Direct Multilingual: the saved selective accuracy is only 3 additional correct test items versus original-only (64 vs 61) and costs more under the supplied verifier-only latency figures (about 5.85 s vs 4.80 s).

### 6. Risk feature naming does not match implementation

`translate_evidence.py` computes numeral overlap as intersection divided by the number of original numbers, which is a recall-like overlap, not Jaccard. The manuscript calls it Jaccard overlap. Correct either the implementation or the description and regenerate predictions if the feature changes. The risk trigger sends about 136/163 = 83.4% of the test items to original verification, so the resource savings are modest; quantify the real end-to-end benefit.

### 7. Input truncation differs from the described token limit

The translation script truncates source text to the first 1,000 characters before tokenization, and the verifier runner truncates each evidence string to the first 512 characters (`[:512]`) before tokenization. The paper describes a sequence length of 512, which reads as tokens. Make truncation token-based and identical across experimental conditions, document the exact formatting/order of claim and evidence, and examine whether cutting evidence changes results.

## Medium-severity scientific issues

### 8. The “RAG” framing may overstate what was evaluated

The repository uses evidence snippets supplied in X-Fact and compares language/translation conditions. It does not appear to implement or evaluate a live retrieval system. Consider a title and framing about cross-lingual claim verification with translated evidence, or clearly state that retrieval is fixed and out of scope.

### 9. The novelty audit is not yet strong enough for a TACL claim

`logs/literature_matrix.csv` compares seven prior works and `logs/search_log.csv` records a small set of targeted searches, often one exact item per known paper. This is a useful starting list, not sufficient proof that the gap is novel. Singhal et al. (arXiv:2410.10303) is especially close and must be compared in detail. Refresh the search through the actual run date, verify each citation at the primary source, record search/inclusion decisions, and be ready to narrow or change the contribution. Avoid “first” or “unexplored” unless the audit supports the exact claim.

### 10. A single language pair, one MT system, one verifier, and a small skewed test split are a weak basis for broad claims

The experiment uses only the Hindi-English direction, one MarianMT model, one NLI verifier, and 163 test items with two gold classes. This may support a narrow pilot/diagnostic study, but likely does not establish a broadly generalizable method. Stronger evidence would include independent bilingual fidelity annotation, a human-corrected-translation control, multiple MT/verifier baselines, careful feature ablations, and additional language pairs if reliable licensed data and compute permit. Otherwise explicitly narrow the contribution and reassess journal fit.

### 11. Tuning objective and comparisons need more justification

The objective `Macro-F1 - 0.15 * Coverage` uses an arbitrary fixed cost penalty; the development split also lacks gold `SUPPORTED` cases. Justify the cost coefficient, add sensitivity analysis, report the full Pareto/risk-coverage curve, and make sure no model/threshold choice was influenced by test labels.

### 12. Statistical claims need stronger reproducibility checks

Preserve the exact paired test logic and discordant pairs, check the paired permutation-test assumptions, use enough permutations for stable p-values, and correct for multiple comparisons if many hypotheses are tested. Report all classwise performance and confusion matrices. Do not use a statistically significant comparison against Always-Check as evidence of superiority over every baseline: the reported selective-vs-No-Check test is not significant (p = 0.1480).

## Artifact and reporting inconsistencies

- `reports/mock_tacl_review.md` gives imaginary reviewers “Accept” and “Strong Accept” scores. This is not a real review and must never be presented as evidence of acceptance likelihood. Replace it with a clearly labelled skeptical, non-predictive audit.
- `reports/plagiarism_similarity_audit.md` claims a 1.40% similarity score, but the artifact does not establish comparison against TACL's submission corpus. Do not call it a TACL similarity certification; remove the percentage or label the method/coverage narrowly and transparently.
- Some internal reports say the deliverable is 8 pages while the supplied PDF is 10 pages. Reconcile page counts based on the actual compiled file.
- The reproducibility report directs the reader to `scripts/preprocess_xfact.py`, which does not appear in the supplied ZIP; the actual acquisition script is `scripts/acquire_and_process_data.py`.
- `experiments/configs/pilot.yaml` gives seed 17, while `logs/run_manifest.json` records seed 42. Reconcile seeds and regenerate the manifest.
- The project has a mismatch between planned conditions in config/protocol and the four conditions actually analyzed. Make protocol, code, report, figures, and manuscript agree.
- The PDF has a nearly empty page 9 containing a split bibliography entry. Fix pagination without violating official fonts/margins.
- The figure 1 workflow is very dense at paper scale and states the wrong selective algorithm. Simplify the diagram and make all labels readable in print.

## TACL formatting position

The current PDF uses A4 and the supplied TACL style and has no figure/table on the first page. However, content validity outweighs formatting. The current official TACL submission guidelines say work must be substantial, original, completed, and unpublished, and will be judged on correctness, originality, technical strength, significance, and NLP relevance. The current formatting instructions require 7–10 A4 pages of content with references outside that limit; the 2024 appendix policy allows up to 5 pages of replication details and 3 pages of complementary results after references, but appendices are not reviewed. Re-check the official sources when preparing the next version.

## Next actions, in priority order

1. **Freeze original artifacts and produce an independent audit report.** Make no claim changes until the results are recalculated.
2. **Resolve label mapping and missing-class issue.** Validate raw X-Fact labels and select an honest evaluation scope.
3. **Align method/code/figure.** Decide whether Selective-Check returns original-only or averages distributions, and implement the intended route consistently.
4. **Fix error attribution.** Add independent bilingual annotation or remove causal fidelity attribution. Produce mutually exclusive accounting if reporting a partition.
5. **Repair data processing and metric scripts.** Use consistent token limits, check model config, compute exact metrics from saved predictions, correct bootstrap labeling, and include translation in end-to-end latency.
6. **Run a corrected, reproducible experiment.** Add missing baselines/ablations and stronger breadth if feasible. Keep negative results.
7. **Re-audit the literature and revise the contribution.** Especially compare against Singhal et al. and other cross-lingual verification/MT robustness work.
8. **Rewrite the manuscript from verified results, generate figures/tables, cleanly compile, render-check every page, and then complete the official TACL checklist.**
9. Obtain human feedback from a domain expert or bilingual annotators where required; do not replace this with a simulated reviewer score.

## Selection-chance assessment

I cannot honestly calculate a paper-specific probability of TACL acceptance from a PDF or make a guarantee. My **subjective screening assessment for the current version is very low (under 5% if submitted as-is)** because the main empirical claim rests on inconsistent and insufficiently validated error attribution, the gold-label distribution does not support the claimed three-class evaluation, and the method description differs from the code. This is not a TACL statistic.

The right strategy is not to add prose or figures to increase a guessed percentage. It is to resolve the correctness issues, independently annotate translation fidelity, strengthen the experimental comparisons, and establish a distinct contribution over the closest work. After those steps, journal fit can be reassessed from the corrected study; no reliable numeric acceptance probability is warranted now.
