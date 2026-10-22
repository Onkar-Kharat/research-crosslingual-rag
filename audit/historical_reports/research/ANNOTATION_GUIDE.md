# Annotation Guide

## Translation fidelity
`PRESERVED`: claim-relevant meaning retained.
`MINOR_VARIATION`: wording differs but relevant meaning retained.
`CRITICAL_ERROR`: claim-relevant meaning changed/omitted.
`UNCLEAR`: cannot confidently decide.

## Error types
Negation/polarity; entity/name; date/time; number/quantity/unit; modality; uncertainty; qualifier/scope; relation/roles; omission; addition; coreference; other.

## Verification labels
`SUPPORTED`: evidence supports the claim under the operational definition.
`CONTRADICTED`: evidence directly conflicts.
`INSUFFICIENT_EVIDENCE`: evidence neither adequately supports nor contradicts.
`UNRESOLVED`: annotation workflow only.

## Procedure
1. Establish gold label from original evidence and available context.
2. Compare translation with original without seeing model output where feasible.
3. Mark fidelity and error spans/rationale.
4. Reveal model predictions only after translation annotation.
5. Attribute to translation only when a relevant meaning change is independently supported.
6. Attribute to verifier reasoning only when translation is meaning-preserving and prediction is wrong.
7. Use mixed/unresolved where needed; do not infer causality from a label flip alone.
8. Use a second annotator on a subset if feasible; report agreement and adjudication. Disclose single-annotator limits.
