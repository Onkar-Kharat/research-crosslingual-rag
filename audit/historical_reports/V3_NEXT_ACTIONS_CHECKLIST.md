# V3 next actions checklist

**Decision: keep V3 as an audit snapshot; do not freeze for manuscript work yet.**

## First-priority repairs
- [ ] Invalidate scripted/simulated annotations. `scripts/perform_bilingual_annotation.py` hard-codes the two “annotators” and adjudication; the present 96% agreement, kappa and 70% result are not human evidence.
- [ ] Regenerate a clean blinded annotation packet; obtain genuine independent annotators if causal translation-fidelity claims are retained.
- [ ] Resolve the threshold mismatch: the included dev tuning table selects tau=0.650, while status/docs say tau=0.300; saved test routing triggers only 14/163 (8.59%).
- [ ] Fix MT inference: current code times `mt_model.generate()` but discards that output and uses cached `translated_evidence` for predictions. Use the exact timed translation for verification or report a cached-translation experiment honestly.
- [ ] Correct the conclusion: selective hard routing gets 55/163 correct versus 54 translated-only, 70 original-only, 65 always-check, and 73 numeral-only (the latter nearly always checks). No significant gain over translated-only is shown.
- [ ] Run random-routing baseline over many seeds; current corrected code only draws one seeded random route despite saying 100 seeds.
- [ ] Treat the current test split as previously inspected/exploratory, not as a virgin confirmatory test.
- [ ] Decide whether to change the task/labels, obtain real claim-evidence labels, or narrow the project to translation/prediction stability. Avoid unsupported 3-class verification claims because `SUPPORTED` has no gold examples and X-Fact veracity labels are not automatically NLI labels.
- [ ] Rename the project away from “RAG” unless retrieval and generation are actually part of the evaluated system.
- [ ] Make a canonical current-results report; relegate old manuscripts, figures and old 41/61/9, tau=.30, 62.6% flip, and p=.0294 claims to legacy history.
- [ ] Update tests to verify corrected outputs and run from clean extraction with a documented environment.

## Freeze condition
Freeze only after the exact method used, its outputs, threshold, statistical tables, annotations (if needed), and fresh evaluation all reconcile from one reproducible run. If no new untouched test set or authentic human annotations can be obtained, narrow the claims to exploratory diagnostics and document the limitation explicitly.
