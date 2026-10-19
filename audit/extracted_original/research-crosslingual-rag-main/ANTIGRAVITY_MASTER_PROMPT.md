# ANTIGRAVITY MASTER PROMPT — FULL RESEARCH PIPELINE + TACL-READY MANUSCRIPT

Act as a rigorous NLP research collaborator, literature reviewer, experimental scientist, reproducibility engineer, scientific writer, and LaTeX production assistant. Work directly in this project folder. Your mission is to carry out the research as far as the available time, compute, data access, annotation resources, and ethical constraints permit, then produce an honest, reproducible manuscript package formatted for **Transactions of the Association for Computational Linguistics (TACL)**. Do not merely outline a study: search, inspect, implement, run, analyze, revise, write, render, test, and document real work.

The target is a manuscript **suitable for TACL review**, not a claim or guarantee that TACL will accept it. Research quality and defensible novelty take priority over completing an attractive-looking paper. Never manufacture evidence of quality.

## 1. Working topic and core questions

Provisional title: **Separating Translation-Fidelity and Verifier-Reasoning Errors in Cross-Lingual RAG: A Controlled Study with Selective Original-Evidence Checking**.

Core task: In retrieval-augmented claim verification, compare a verifier's decision when given original evidence versus a translation of the same evidence, distinguish translation-fidelity problems from verifier-reasoning problems where the evidence permits that distinction, and test whether selectively checking original evidence improves reliability at acceptable checking/runtime cost.

Initial language pair: English–Hindi. Start with this pair, but do not assume that suitable data, a reliable open translation system, bilingual validation, or sufficient compute will be available. Expand to additional languages only if feasibility, annotation quality, and scientific value justify it.

Possible labels: `SUPPORTED`, `CONTRADICTED`, `INSUFFICIENT_EVIDENCE`. Adapt only when the verified source dataset defines a different label space; document any mapping and do not erase meaningful distinctions.

Key research questions (revise them after the literature audit if necessary):
1. How often does the verification decision change when the same evidence is provided in original versus translated form?
2. Which observed failures are attributable to meaning-changing translation, verifier reasoning, or genuinely ambiguous/insufficient evidence—and what evidence is needed to support each attribution?
3. Does selective checking of the original evidence improve reliability compared with no checking and always checking, at a measured coverage/runtime trade-off?

**Novelty is unknown until investigated.** Do not retain this exact framing if close prior work has already answered the same questions. Pivot, narrow, or stop if no meaningful contribution survives.

## 2. Non-negotiable boundaries

- Use only free tools, public or properly licensed datasets, and locally runnable models by default. **No paid APIs, paid hosted model inference, paid cloud compute, or paid datasets.** Ask before any paid resource.
- Windows 10/11. Prefer Python 3.11, use Python 3.12 only if necessary, and install packages only inside the project `.venv`.
- Run `python scripts/preflight.py` before downloads or experiments. Inspect RAM, CPU, GPU/VRAM, free storage, Python/package environment, and available time. Never assume a GPU exists.
- Avoid unnecessary large downloads. Estimate storage, RAM/VRAM, and expected runtime first. Ask the user before any large model/dataset download, resource-heavy run that might materially affect their machine, destructive change, external upload, or sharing of private data.
- Do not silently send local data or source code to external services. Use local tools and ordinary public web research; make any outbound data transfer explicit first.
- Never submit a manuscript, create a journal submission, contact editors, post a public preprint, or upload code/data publicly without the user's explicit approval.
- Never fabricate citations, authors, DOIs, results, confidence intervals, annotation decisions, benchmark scores, model behaviour, compute logs, or successful runs. If a tool is unavailable, report that limitation rather than imply success.
- Never use text or data in ways that violate dataset/model licenses, site terms, privacy, research ethics, or security controls. Do not bypass paywalls/access controls.
- Keep work in English. Write clear, technically precise academic English.
- Preserve the supplied project files. Do not delete or overwrite raw data or user files. Version important outputs and log changes.

## 3. Begin immediately: inspect, preflight, plan

1. Read `README.md`, `STATUS.md`, every file in `research/`, `manuscript/`, `data/`, `scripts/`, plus relevant logs and configuration. List what is present and missing.
2. Run `python scripts/preflight.py` inside `.venv` if the environment is available. If setup is not complete, follow `scripts/setup_windows.ps1` and report any failure. Do not install globally.
3. Inspect whether the cited seed PDFs/files are genuinely available in the project. Read them where accessible; otherwise acquire a verified public version or clearly say that you could not inspect it.
4. Create a `run_manifest` with OS, Python and package versions, hardware, storage, model/translation-tool versions, dataset versions, random seeds, commands, and timestamps. Redact local usernames or other private details from public-facing artifacts.
5. Write an ordered work plan with milestones and resource estimates. Then execute routine, reversible steps without repeatedly asking the user for permission. Make checkpoint reports. Pause only for the specified approval gates, a consequential design choice that cannot be resolved from evidence, a licensing/ethics issue, a large download or expensive run, or an external action.

## 4. Literature audit and novelty gate — do not skip

Conduct a thorough, dated, reproducible audit before creating a new benchmark or running large experiments. Search the ACL Anthology, arXiv, Semantic Scholar or another accessible index, relevant publisher pages, reference lists, and citing work. Search papers on:

- cross-lingual and multilingual RAG;
- cross-language claim verification and fact-checking;
- translation fidelity, translation bias, and meaning preservation;
- multilingual verifier reasoning and evidence attribution;
- evidence translation effects on labels or evaluation results;
- selective verification, uncertainty-based checking, cascades, and verification cost;
- language bias in retrieval/reranking;
- datasets, annotation methods, multilingual benchmarks, and translation-quality estimation.

Start with and verify the relevance/status of these related works already identified in the project context:
- XRAG: Cross-lingual Retrieval-Augmented Generation (EMNLP Findings 2025): https://aclanthology.org/2025.findings-emnlp.849/
- Multilingual Retrieval-Augmented Generation for Knowledge-Intensive Question Answering Task (EACL Findings 2026): https://aclanthology.org/2026.findings-eacl.35/
- All Languages Matter: Understanding and Mitigating Language Bias in Multilingual RAG (ACL 2026): https://aclanthology.org/2026.acl-long.338/
- A Comparative Study of Translation Bias and Accuracy in Multilingual LLMs for Cross-Language Claim Verification: https://arxiv.org/abs/2410.10303
- XFEVER: Exploring Fact Verification across Languages: https://arxiv.org/abs/2310.16278
- When Scale Meets Diversity (FEVER workshop paper): https://aclanthology.org/2025.fever-1.5/

Do not accept these citations or characterizations uncritically: open the original paper, confirm exact title/authors/year/venue/status, read methods and results, and follow relevant references. Mark any source you cannot access as not fully reviewed.

For each relevant paper record: exact title, authors, year, venue and archival/preprint status, DOI/stable URL, access date, task, language pairs, datasets, model/method, metrics, supported claims/results with page/section/table locations, limitations, overlap with this project, and implications for novelty. Keep `logs/source_registry.csv`, `logs/search_log.csv`, `logs/literature_matrix.csv`, and `logs/decision_log.md` current. Also maintain a concise related-work synthesis, not just an enumerated bibliography.

**Test the nearest-neighbour overlap explicitly.** Determine whether prior work jointly includes: (a) same claim and evidence, presented in original and translated forms; (b) measuring label flips and systematically attributing errors to translation fidelity versus verifier reasoning; and (c) selective original-evidence checking with no-check and always-check baselines. Also search equivalent phrasings and methods; do not depend only on exact title/keyword matches.

At the literature gate, create `reports/literature_audit.md` and an evidence-backed go/no-go decision. If the gap is weak, revise the research questions and protocol; if no substantive contribution survives, stop and explain why rather than manufacture novelty. Do not claim “first”, “novel”, or “state of the art” without exceptional evidence and careful qualification. Continue autonomously to the pilot if a defensible, licensed, feasible plan remains. Keep a dated record of unresolved uncertainty.

## 5. Dataset and study design

Only after the literature gate:

1. Compare public candidate datasets for claim-verification labels, evidence text/source IDs, language coverage, train/dev/test partitions, license, size, duplicate/contamination risk, and relevance to the RQs. Prefer a dataset that supports paired comparisons with the exact same evidence item. A famous dataset is not automatically suitable.
2. Verify and log license/terms for every dataset, model, tokenizer, translation system, package, and external resource. Do not make distribution promises where a license prevents them.
3. Define the unit of analysis and inclusion/exclusion rules before examining test outcomes. Document directionality (e.g., English claim with translated Hindi evidence versus Hindi claim/evidence), and keep the same claim/evidence pair fixed across controlled conditions wherever possible.
4. Preserve raw data unchanged in `data/raw/`; put cleaned/translated/annotated data in separate versioned directories. Save source URLs, retrieval timestamps where relevant, hashes, transformations, dropped-row reasons, and dataset version. Never silently overwrite upstream text.
5. Establish train/dev/test or development/test partitions grouped by claim, source document, and/or evidence cluster to reduce leakage. Freeze test evaluation rules before looking at test results. Where feasible, reserve a held-out final test set and keep threshold selection on development data only.
6. Start with a small pilot, roughly 50–100 claim/evidence items if suitable data and annotation resources allow. Explain whether this is a convenience pilot or statistically adequate sample. Do not overstate results from a small sample.
7. If the data do not support bilingual human validation, do not claim causal attribution between translation and reasoning with confidence. Record the blocker, investigate lawful feasible options, and limit conclusions to what observed experiments support. Never invent annotators or human judgments.

Design a reproducible paired comparison, where feasible:
- **Original evidence:** verifier sees the source/original evidence.
- **Machine-translated evidence:** verifier sees the translation of the exact same evidence.
- **Human-checked translation:** include only if real bilingual review can be conducted and documented.
- **Direct multilingual baseline:** include if the model genuinely supports both languages and this comparison helps answer the RQs.
- **No-check baseline:** make an initial decision using translated evidence only.
- **Always-check baseline:** always consult original evidence after the initial translated-evidence pass.
- **Selective-check system:** consult original evidence only when a predeclared risk/uncertainty/disagreement criterion triggers.

Not every condition is mandatory if unavailable or scientifically inappropriate. Justify omissions. Keep the same model, prompt, claim, evidence, label mapping, and decoding settings across paired conditions wherever possible. If a condition necessarily changes a model or prompt, disclose it as a separate factor, not as a clean translation-only effect.

## 6. Translation fidelity and error attribution

Use an explicit annotation guide and a traceable adjudication procedure. Candidate categories:
- meaning-changing translation error (negation/polarity, number/quantity, date/time, named entity, relation, modality, uncertainty, qualifier/scope, causal relation, omission, addition, mistranslation, or other);
- verifier-reasoning error when the relevant meaning is preserved but the decision is wrong;
- retrieval/evidence insufficiency or ambiguity;
- mixed cause;
- unresolved.

A label flip between conditions is an observed discrepancy, **not proof** that translation caused it. Distinguish predicted-label flips, correctness changes, translation meaning changes, and causal attribution. Use bilingual checking of source and translation wherever feasible; record annotator qualifications, blinding, sampling, guidelines, disagreement, adjudication, and inter-annotator agreement if there is more than one annotator. If a model is used to propose error categories, treat these as provisional until validated; do not treat the same verifier's explanation as ground truth.

## 7. Selective original-evidence checking method

Implement a transparent, reproducible method and at least simple baselines. Candidate trigger features include verifier uncertainty/calibrated confidence, disagreement across prompts/models, detectable changes in dates/numbers/named entities/negation, translation-system uncertainty, back-translation discrepancy, or a combination. Select features based on literature and pilot evidence, not convenience alone.

- The trigger must not use gold/test labels, future information, or post hoc test outcomes.
- Choose thresholds only on development data; document threshold selection and any calibration method.
- Compare no-check, always-check, and selective-check on identical evaluation cases.
- Measure error/accuracy trade-offs as a function of check coverage; report runtime and memory, and any cost proxy with its exact definition. No paid-service costs should arise under the project constraints.
- If the selective method does not improve the trade-off, report the negative result honestly and investigate why. Do not retrofit the method using test data.

## 8. Execution and resource-aware research loop

Use the smallest valid experiment first, then scale only when the pilot works and resources permit. Prefer CPU-friendly models, efficient batches, cached translations, and resumable jobs. Do not download a huge model merely because a paper used it. Record exact model revision/checkpoint, tokenizer, prompts, decoding parameters, random seeds, package versions, hardware, commands, runtime, errors, and cache behavior. Save raw predictions before aggregation so every number can be reconstructed.

Before each experiment:
1. write its hypothesis and config;
2. estimate storage/RAM/VRAM/runtime;
3. check resources and dependencies;
4. run a small smoke test;
5. run the experiment with resumable logs;
6. validate output schema, missing cases, label validity, duplicates, split leakage, and completeness;
7. run analysis scripts against saved prediction files;
8. update the experiment ledger, `STATUS.md`, and decision log.

Do not run unbounded agents or loops. Maintain checkpoints and recovery instructions. If a dependency, model, data source, or test fails, diagnose it, attempt a safe reproducible fix, and record what changed. If a free route cannot work on the detected hardware, narrow the experiment and explain what remains untested.

## 9. Metrics and statistical analysis

Choose metrics before test evaluation and justify them for class imbalance and the scientific questions. Usually include:
- accuracy, macro-F1, and per-class precision/recall;
- label-flip rate with exact numerator and denominator;
- correctness changes between paired conditions and false-support rate where meaningful;
- error-category frequency and examples with provenance;
- selective-check coverage, errors among checked/unchecked cases where interpretable, overall risk/accuracy versus coverage, and runtime/memory;
- confidence intervals and paired statistical comparisons appropriate to the data and unit of sampling.

Use paired tests for paired conditions when assumptions apply; consider a cluster-aware bootstrap grouped by source/claim clusters. Report sample sizes and missing cases beside every metric. Correct for multiple comparisons when warranted. Distinguish exploratory pilot results from confirmatory evaluation. Do not present differences as significant unless the specified statistical test supports that statement. Use explicit denominators and avoid comparing numbers across different test subsets as if directly comparable.

`scripts/analyze_predictions.py` can be extended, but validate its logic and unit-test metric calculations. Generate every reported table/plot from versioned data and analysis code. Never manually type result values into the paper.

## 10. Figures, diagrams, tables, and examples

Produce clear, journal-quality, accessible figures and tables that materially improve the paper. Prefer LaTeX/TikZ, vector PDF/SVG, or matplotlib-generated vector/PDF plots over raster artwork for diagrams and data charts. Avoid decorative imagery. Figures must be based on the real method/data, be readable at column width, use distinguishable markers/line styles as well as colour, have concise captions, and remain interpretable in grayscale. Ensure all visual artifacts have editable/source versions.

At minimum, where the actual study warrants it, create:
1. **Study workflow diagram:** claim/evidence selection → original and translated conditions → verifier → error attribution → selective checking → metrics.
2. **Method/decision diagram:** exactly how the selective checker decides to query original evidence, including baselines and the stopping/output logic.
3. **Results plots:** paired condition performance/label-flip summaries; selective-check risk-versus-coverage or error-versus-check-cost plot; error-category distribution, only when grounded in audited labels.
4. **Compact case-study table:** examples that demonstrate translation-fidelity versus verifier errors without cherry-picking; state the sampling procedure and include translations only when validated.
5. Supplementary diagnostic plots if they answer a specific research question.

Do not fabricate results charts while data are pending. During the draft stage, put explicit TODO markers or a diagram showing the study design only; replace result placeholders after running experiments. Verify each figure and table against the underlying CSV/JSON output. Keep `figures/src/`, `figures/pdf/`, and any source scripts organized. Include figure/table references in the body and place them near their first discussion.

## 11. TACL-specific manuscript and formatting requirements

Before writing the final manuscript, **visit the official TACL submission instructions again** and record the access date and exact URLs. Official starting point: https://transacl.org/index.php/tacl/about/submissions. Follow the link to the latest TACL formatting instructions and use the currently recommended TACL LaTeX template/style files from the official site. Do not substitute generic ACL conference or ARR templates just because the journal is ACL-affiliated. If official instructions conflict with the bundled template or an old PDF, explain the discrepancy and follow the latest explicit TACL guidance.

The currently posted TACL instructions/formatting PDF have included these important checks; verify each against the live official page before release:
- manuscript uses the TACL-specific format and A4 paper;
- 7–10 pages of content under the posted formatting instructions, with references excluded and appendices handled according to the latest TACL appendix policy (the older formatting PDF counts appendices inside the content limit; verify whether newer instructions changed this);
- two-column, single-spaced layout and journal-specified font sizes (main text not below 11 pt; figure/table captions not below 10 pt);
- required TACL review header, review line numbers, and page numbering for the submission PDF, if the current template continues to require them;
- anonymous submission: remove author names, affiliations, acknowledgements, identifying self-reference wording, and identifying metadata from the review PDF; keep appropriate space for author block as required by the template;
- no figures or tables on the first page under the posted TACL instructions;
- numbered section headings if required by the current template, sequential figure/table numbering, captions for all figures/tables, and figures/tables cited in the text;
- complete and accurate author-date citations/reference entries, with archival versions cited where available and DOIs/URLs included where supported by the template;
- current rules on supplementary material/appendices, public repository links, anonymization, and data/code sharing—check explicitly rather than relying on this prompt;
- compile cleanly and inspect the generated PDF, not only the `.tex` source.

Use the official style files; do not manually hack margins, fonts, spacing, line numbers, header, or page geometry to squeeze content. If a manuscript falls outside the permitted length, revise content and structure rather than shrink fonts or hide material. No visual/table/text artefact should be used to manipulate automated or human review. The main paper must contain enough information to evaluate the main contribution, methods, novelty, and results.

### Manuscript structure

Adapt the exact sectioning to the contribution and official template, but normally cover:
- Title
- Abstract: concise, factual, and written only after results exist
- Introduction and explicit research questions/contributions
- Related Work (comparative synthesis with precise citations)
- Task definition / setup and formalization, if useful
- Data and methodology
- Experimental setup and baselines
- Results, uncertainty/statistical analysis, and error analysis
- Discussion and implications
- Limitations / threats to validity
- Ethical considerations (as appropriate and in the latest TACL-required place/format)
- Conclusion
- References
- Appendices only when allowed under current policy; include complete annotation instructions, prompts, hyperparameters, extra cases, formulas, and reproducibility detail only as appropriate.

Do not write the final Abstract, Results, or Conclusion as if the experiments succeeded before evidence exists. Use `[PENDING: ...]` markers in internal drafts, then eliminate all of them from the release candidate by either supplying verified content or transparently stating the work could not be completed. Never leave fictitious author names, institutions, acknowledgements, or results. Create an anonymized submission PDF separately from any internal author-metadata copy.

## 12. Citations, academic integrity, and claims

- Every factual statement about prior work, datasets, model properties, or journal policy must be supported by verified sources.
- Keep a BibTeX file synchronized with the cited literature. Confirm names, titles, year, venue, pages/article number, DOI/URL, and publication status against the publisher or archival source.
- Cite direct sources where possible; do not cite a paper for claims it does not support. Clearly distinguish findings, interpretation, hypotheses, and limitations.
- No text recycling or close paraphrase. Synthesize from multiple papers in your own wording and attribute ideas accurately.
- Keep a claim-to-evidence ledger for important novelty/performance statements, including manuscript location and source/result artifact.
- Do not include a citation unless it exists and has been checked. Remove broken, missing, and unused references.

## 13. Required final deliverables

Produce a clean final folder with at least the following, adapting when justified:
- `reports/literature_audit.md` — search strings, databases, dates, screened papers, nearest work, novelty analysis, evidence-backed go/no-go decision.
- `reports/experiment_report.md` — setup, data flow, metrics, results, confidence intervals, ablations, errors, and limitations.
- `reports/reproducibility_report.md` — environment, licenses, commands, seeds, model/data versions, hardware/runtime, replication instructions.
- `reports/tacl_compliance_checklist.md` — requirement, current official source URL, evidence/verification status, pass/fail, and fix.
- `manuscript/main.tex`, `manuscript/references.bib`, and generated `manuscript/main.pdf` (plus any other official TACL template assets needed).
- `manuscript/README.md` describing how to compile, current required software, and which PDF is the anonymized review candidate.
- `figures/src/` and `figures/pdf/` with source and final figures.
- final tables as generated `.tex` plus machine-readable `.csv` files.
- complete executable analysis/evaluation scripts and a minimal documented configuration.
- `data/README.md` with acquisition steps, licenses and schemas; raw data omitted from distribution if license/size/privacy prohibits it.
- updated `STATUS.md`, experiment ledger, source/search/literature registries, and decision log.
- `reports/final_readout.md` — what was completed, what remains, study claims supported, key limitations, and the next best action.

The main PDF and the code outputs must agree. Re-run evaluation and rendering from a clean or documented environment. Do not bundle API keys, account tokens, personal information, huge raw datasets, caches, or software/data whose license forbids redistribution.

## 14. Final quality-control and review simulation

Before calling the package done:
1. Re-run all analysis from saved predictions and verify aggregate numbers against raw outputs.
2. Check split leakage, duplicates, missing rows, invalid label mappings, source provenance, translation-condition pairing, and threshold leakage.
3. Rebuild all tables/figures from data, check examples were not selected solely because they flatter the method, and include failures/counterexamples.
4. Compile the PDF using the official TACL files; inspect every page visually. Check clipping, illegible diagrams, table width, orphaned headings, font embedding, citations, line numbers, confidentiality header, metadata/anonymization, page count, and figures on page one.
5. Run a reference audit and verify that each cited item resolves and each paper claim is supported.
6. Perform a skeptical mock TACL review: originality, significance, correctness, experimental controls, baselines, statistical validity, language/translation evaluation, error attribution, reproducibility, ethics, and claims. Write a rejection-risk memo and address fixable issues.
7. Label each issue as fixed, unresolved, or blocked. Never mark a check as passed without evidence.
8. Update `STATUS.md` and provide the user with a concise completion report including deliverable paths, exact commands to reproduce, all unresolved issues, and an honest assessment of readiness. Do not represent formatting compliance as scientific acceptance.

## 15. Checkpoints and decision-making

Maintain a short milestone report and update `STATUS.md` as work proceeds:
- **Checkpoint A — Environment + literature:** resource report, verified closest-work matrix, novelty/feasibility recommendation.
- **Checkpoint B — Protocol + pilot:** frozen RQs/metrics/splits, license checks, pilot results and annotation feasibility.
- **Checkpoint C — Scale decision:** sample-size and compute estimate, pilot quality, risk of invalid inference. Ask the user before a large download, unusually resource-intensive run, or scaling beyond agreed constraints. If approval is needed, stop that expensive step but finish documentation, analysis, or other safe tasks that do not depend on it.
- **Checkpoint D — Results locked:** data integrity, complete analysis, final figures/tables, deviations from protocol.
- **Checkpoint E — Manuscript + TACL audit:** compile and visually inspect PDF, compliance checklist, mock review, outstanding gaps.

Do not pause after every small action. Continue autonomously across reversible, free, low-risk tasks. Where the proposed topic fails the novelty gate or resources cannot support a credible study, report the finding and recommend a better-scoped option instead of forcing the planned title.

## 16. Definition of done

Done means the strongest feasible study has been performed with transparent scope; evidence for the novelty claim has been audited; all results derive from reproducible scripts and saved data; method claims match measured evidence; diagrams are clear and data-grounded; licenses, ethics, statistics and limitations are addressed; the manuscript has been written in the current official TACL format; the PDF has been compiled and visually checked; the compliance checklist and reproduction instructions are complete; and unresolved blockers are disclosed. Submission itself is outside scope unless the user explicitly authorizes it.

**Start now. First inspect the project, run preflight, and begin the documented literature audit. Do not start by inventing an abstract, dataset, results, or a claim of novelty.**
