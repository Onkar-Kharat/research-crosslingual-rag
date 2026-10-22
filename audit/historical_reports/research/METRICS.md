# Metrics

Choose one primary outcome after pilot and document it before full test evaluation.
- Accuracy and macro-F1.
- Per-class precision/recall.
- Label-flip rate = items whose predictions differ between original and translated conditions / items with valid predictions in both.
- False-support rate: among gold labels not SUPPORTED, proportion predicted SUPPORTED; report denominator.
- Error attribution: translation-fidelity, verifier reasoning, mixed, ambiguous/unresolved.
- Selective-check coverage: fraction of items triggering a check.
- Error reduction versus no-check; also compare always-check.
- Cost proxies: runtime, memory, fraction checked, tokens if locally available; never invent monetary costs.
- Confidence intervals, effect sizes, appropriate paired tests, multiple-comparison handling.
Report negative results and avoid broad claims from a small pilot.
