# Research Protocol

## Aim
Measure how translating retrieved evidence affects claim-level verification; distinguish translation-fidelity errors from verifier-reasoning failures; test selective original-evidence checking at acceptable cost.

## Research questions
RQ1. How often does the label change between original and machine-translated evidence?
RQ2. How are incorrect decisions associated with translation-fidelity errors versus verifier-reasoning failures?
RQ3. Does selective original-evidence checking reduce errors compared with no-check and always-check baselines?

## Tentative hypotheses
H1. Some examples will show label changes, with rates varying by language, model and error type.
H2. Meaning-critical translation errors may be associated with incorrect labels.
H3. Selective checking may reduce errors at lower average cost than always checking if the trigger is reliable.
These are hypotheses, not results.

## Scope and labels
Start English–Hindi. Add languages only if suitable licensed data, reliable bilingual annotation, and compute allow.
Labels: `SUPPORTED`, `CONTRADICTED`, `INSUFFICIENT_EVIDENCE`. Define how multiple/conflicting passages are handled. Allow `UNRESOLVED` in annotation workflow rather than forcing an unreliable gold label.

## Conditions
- Original evidence
- Machine-translated evidence
- Human-corrected translation
- Direct multilingual verification where fair
- Translation-quality-warning baseline if available
- Always-check-original
- Selective-check-original

## Pilot and data
Target 50–100 examples after literature gate. Inspect dataset schema, evidence availability, language coverage and license before selecting it. Pilot size is for feasibility, not broad generalization. Determine full-study size from pilot effect sizes, annotation capacity and desired precision.

## Annotation
Bilingual reviewer(s) compare original and translation, ideally blind to model outputs. Fidelity labels: `PRESERVED`, `MINOR_VARIATION`, `CRITICAL_ERROR`, `UNCLEAR`. Error types: negation, entity, date, number, modality, uncertainty, qualifier, relation, omission, addition, coreference, other. Record rationale/confidence; double-annotate a subset if possible and adjudicate disagreements. A single annotator must be disclosed as a limitation.

## Selective-check method
Define a transparent risk trigger without gold/test leakage. Tune thresholds on development data only. Compare no-check, always-check and selective-check. Report accuracy, error reduction, fraction checked and runtime/cost proxies. If it does not help, report that result.

## Analysis
Accuracy, macro-F1, per-class precision/recall, label-flip rate with denominator, false-support rate, error attribution, confidence intervals, paired comparisons, per-language/model/error-type analysis, ablations and cost/latency. Group splits by claim/source clusters to reduce leakage. Report negative results.

## Reproducibility
Record versions, prompts, model IDs, translation method, seeds, data version/license, splits, hardware, exact commands and preprocessing. Generate tables from saved predictions.

## Go/no-go
Proceed only if literature review finds a defensible contribution, pilot results are measurable/interpretable, annotation is feasible and mitigation can be fairly tested. Otherwise narrow/change the topic.
