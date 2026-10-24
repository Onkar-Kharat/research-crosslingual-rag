# Independent Adversarial Mock TACL Reviews

**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Paper Title:** Cross-Lingual Evidence Verification: Verifier Prediction Sensitivity Under Hindi-to-English Translation Shift  
**Evaluation Standard:** TACL Acceptance Criteria (Correctness, Originality, Technical Strength, Significance, Presentation)  
**Date:** 2026-10-24  

---

## Reviewer A: Novelty, Literature Positioning, and Significance

### Overall Assessment: Borderline (Score: 3 / 5)
*"An empirically rigorous and honest diagnosis of prediction instability under translation shift in claim verification, but constrained in scientific scope by evaluating a single language pair and a single verifier backbone."*

### Summary of Contribution
The paper evaluates the sensitivity of an mDeBERTa-v3 NLI claim verifier when evidence is presented in original Hindi versus machine-translated English (via OPUS-MT) on 163 claims from the X-Fact benchmark. It documents a large paired disagreement rate of 63.80%, shows that 48.44% of translated-supported predictions flip to contradicted under original Hindi evidence, and reveals that an uncertainty/numeral-gated cascade fails to beat the unverified baseline (28.22%).

### Major Concerns
1. **Narrow Language Scope for a Journal Paper:** TACL typically expects multilingual findings to demonstrate cross-typological breadth (e.g., across multiple language families such as Indo-Aryan, Afroasiatic, Sinitic, and Romance). Confining the empirical study exclusively to Hindi-to-English makes it read more like a focused conference short paper or empirical case study rather than a generalizable journal contribution.
2. **Predictable Finding vs. Novel Insight:** That translation introduces noise into downstream inference is well established in cross-lingual QA literature (e.g., XRAG, CrossRAG). The authors attempt to distinguish their work by focusing on 3-class NLI veracity flips, but skeptical reviewers may question whether 63.8% disagreement is simply the expected noise floor of MarianMT coupled with zero-shot DeBERTa transfer.
3. **Negative Result for the Proposed Cascade:** The selective cascade achieves 28.22% accuracy, exactly matching the No-Check baseline ($p = 1.0000$). While reporting negative results is scientifically valuable, TACL papers typically pair empirical diagnoses with a positive algorithmic solution.

### Minor Concerns
- The literature review would benefit from discussing quality estimation (QE) literature more deeply (e.g., WMT shared tasks), as the risk trigger formula resembles a simple sentence-level QE heuristic.
- The title specifies "Hindi-to-English Translation Shift", which is commendably accurate, but highlights the paper's limited scope.

### Required Revisions
- **Writing / Auditing (No New Data):** Clarify that the central novelty lies not in claiming translation adds noise, but in uncovering the **severe directional asymmetry** (false-support generation vs. refutation recovery) that challenges the common architectural assumption that evidence translation preserves verification fidelity.
- **Requires New Research (Future Phase):** Extend the evaluation to at least two additional language families (e.g., Arabic, Turkish, or Tamil) to establish cross-lingual generality.

---

## Reviewer B: Methodology, Statistics, and Experimental Validity

### Overall Assessment: Weak Accept / Borderline (Score: 3.5 / 5)
*"Methodologically meticulous and statistically exemplary, but severely challenged by benchmark class imbalance and the lack of human validation."*

### Summary of Contribution
The authors conduct a thoroughly audited paired evaluation, reporting continuity-corrected McNemar tests, exact binomial p-values, paired prediction-swap permutation tests on Macro-F1, Wilson score intervals, and Benjamini-Hochberg FDR adjustments.

### Strengths
- **Statistical Rigor:** The mathematical treatment of paired correctness and discordant pairs ($b=27, c=51, p=0.008772$) is flawless.
- **Metric Discordance Insight:** The discussion of why McNemar's test is significant ($p < 0.01$) while the permutation test on Macro-F1 is non-significant ($p = 0.1898$) provides a valuable methodological lesson for NLP researchers evaluating imbalanced benchmarks.
- **Ablation Controls:** The inclusion of 100-seed random routing controls and component ablations gives high confidence in the negative result for the selective cascade.

### Major Concerns
1. **Extreme Benchmark Class Skew ($TP_{\text{sup}} \equiv 0$):** The test set has 142 Contradicted, 21 Neutral, and 0 Supported instances. While the authors disclose this prominently, it means the entire positive prediction space ($y = \text{SUPPORTED}$) cannot be validated for recall or true positives. Accuracy is heavily dominated by Contradicted instances.
2. **Exploratory Status of Test Split:** The authors candidly disclose that the test split ($N=163$) was inspected during prior computational experiments. In strict confirmatory testing, this inflates alpha error. The authors correctly designate the work as an exploratory computational study, but a holdout evaluation on an uninspected split would be much stronger.
3. **Absence of Completed Human Validation:** The paper decomposes errors into $S_{\text{trans}}=51$ and $S_{\text{degraded}}=27$, but without completed human bilingual evaluation, we cannot ascertain whether these flips represent genuine semantic shifts in MarianMT or represent representational quirks in the mDeBERTa embedding space.

### Minor Concerns
- The original draft cited Benjamini-Hochberg for the permutation test; this has now been properly corrected to Yeh (2000), while retaining BH strictly for FDR control.

### Required Revisions
- **Writing / Auditing (No New Data):** Emphasize that all error partitions ($S_{\text{trans}}$, $S_{\text{verif}}$, $S_{\text{degraded}}$) are observational operational strata, not proven causal categories.
- **Requires New Research (Future Phase):** Execute the proposed bilingual human annotation protocol (Appendix A.4) with trained annotators on the 104 discordant instances to establish inter-annotator agreement ($\kappa$) and causal error attribution.

---

## Reviewer C: Clarity, Transparency, and Scientific Integrity

### Overall Assessment: Accept with Minor Revisions (Score: 4 / 5)
*"A refreshingly honest, self-critical, and transparent paper that sets a high benchmark for reproducible scientific reporting in NLP."*

### Summary of Contribution
The paper provides an unvarnished characterization of verifier prediction sensitivity under evidence translation, refusing to overclaim or hide negative cascade results.

### Strengths
- **Exemplary Epistemological Restraint:** The authors explicitly distinguish observational prediction disagreement from verified translation error, avoid claiming causality without human data, and report negative cascade results with complete transparency.
- **Open Science & Reproducibility:** Every metric is backed by deterministic random seeds (42), frozen prediction CSVs, and an automated regression test suite passing 47/47 checks.
- **Presentation Excellence:** The five publication figures and modular tables are clean, legible, and completely free of overlapping text or cluttered legends.

### Major Concerns
- None regarding scientific integrity or clarity. The authors have proactively addressed the standard pitfalls of cross-lingual claim verification papers (overclaiming generalization, conflating disagreement with error, hiding class imbalance).
- The primary limitation remains the inherent scientific boundary of the frozen dataset (single language pair, zero gold supported instances).

### Minor Concerns
- Ensure that the anonymous review version (`submission.pdf`) completely removes the GitHub URL, author contributions section, and funding statements. (Audit confirms this has been implemented).

### Final Recommendation
The manuscript is in the upper quartile of scientific transparency. If TACL editors appreciate rigorous negative findings and honest empirical diagnoses of common architectural assumptions in RAG, the paper deserves serious consideration.
