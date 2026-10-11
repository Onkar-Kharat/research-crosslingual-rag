# End-to-End Workflow

0. **Environment:** create `.venv`; run preflight; record Python, CPU, RAM, GPU, disk; estimate download requirements.
1. **Literature audit:** document queries, dates, inclusion/exclusion; inspect closest papers, methods, appendices, citations and citing work; update registries.
2. **Gap gate:** compare exact task, unit, labels, attribution, mitigation and evaluation. Write the strongest argument against novelty. Decide go/narrow/stop; checkpoint with user.
3. **Dataset/licensing:** inspect actual schema and language coverage; verify official license; create data manifest and grouped splits.
4. **Pilot protocol:** select 50–100 items; create translations; annotate fidelity and gold labels; smoke-test prompts/parser.
5. **Pilot:** run original/translated/corrected evidence and fair baselines; compute flips, error types and baseline performance. Report resource use.
6. **Pilot checkpoint:** show sample/exclusions, denominators, label-flip rate, annotation uncertainty, preliminary results, resource usage and limitations. Ask before scaling.
7. **Selective method:** specify trigger; tune only on dev; compare no-check, always-check, selective-check; run ablations.
8. **Full experiments:** expand models/languages only if justified; freeze splits/metrics; run confidence intervals, paired tests, leakage checks and error analysis.
9. **Reproducibility:** rerun scripts, regenerate tables, check missing outputs and version records.
10. **Manuscript:** draft abstract last; use verified citations and result outputs; state limitations and negative results.
11. **Venue audit:** verify official scope, peer-review status, mandatory fees, optional APC and repository policies.
12. **Final gate:** produce readiness report. No external submission without explicit user approval.

Every phase must produce a dated report and update `STATUS.md`, source/search/literature logs, decision log and experiment ledger.
