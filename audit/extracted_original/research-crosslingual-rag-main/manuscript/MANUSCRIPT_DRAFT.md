# Separating Translation-Fidelity and Verifier-Reasoning Errors in Cross-Lingual RAG: A Controlled Study with Selective Original-Evidence Checking

**Status:** Scaffold only; not submission-ready. **Never invent results.**

## Abstract
[RESULTS PENDING] Cross-lingual retrieval-augmented generation (RAG) systems may rely on machine-translated retrieved evidence. Translation can alter claim-relevant meaning, while a verifier may also misinterpret faithful evidence. This study investigates these potential sources of error in claim verification. We compare decisions from original, machine-translated and human-corrected evidence; annotate translation-fidelity errors; and evaluate selective original-evidence checking against no-check and always-check baselines. We report verification quality, label changes, error attribution and computational trade-offs across [LANGUAGES/MODELS]. Results and novelty claims will be added only after the literature audit and experiments.

## 1. Introduction
Explain why cross-lingual evidence verification matters. Distinguish meaning-changing translation from verifier reasoning. State RQ1: how often labels change; RQ2: how errors are associated with translation fidelity versus reasoning; RQ3: whether selective original-evidence checking reduces errors at acceptable cost. Finalize contributions only after novelty audit/results.

## 2. Related Work
2.1 Cross-lingual and multilingual RAG
2.2 Multilingual claim verification and cross-language consistency
2.3 Translation quality and translation errors in evaluation
2.4 Evidence attribution and verification-time checking
2.5 Research gap (write only after comparing closest work; cite verified sources)

## 3. Task Definition
Given claim c, original evidence e in source language and translation T(e), predict `SUPPORTED`, `CONTRADICTED` or `INSUFFICIENT_EVIDENCE`. Define evidence bundles, conflicting passages and context rules.

## 4. Data
Dataset versions, URLs, licenses, languages, sampling, exclusions, splits, translation systems, human validation, annotation procedure, agreement and adjudication.

## 5. Experimental Setup
Models and versions; prompts; decoding; baselines; selective-check trigger; dev-only threshold tuning; metrics; statistical analysis; compute environment.

## 6. Results
**[RESULTS PENDING — DO NOT INVENT]**
Main performance; label changes; error attribution; selective-check vs no-check/always-check; robustness and ablations. Generate tables from saved result files.

## 7. Discussion
Interpret results against RQs. Address alternative explanations, language proficiency, annotation uncertainty, retrieval artifacts and whether the method truly improves the accuracy–cost trade-off.

## 8. Limitations and Ethics
Language coverage, representativeness, licenses, annotation, translation systems, compute and generalization.

## 9. Conclusion
Write after results are final; do not claim broader generalization than supported.

## References
Only verified bibliography entries. Check every title, author, year, venue, DOI/URL and citation-to-claim mapping.
