# NOVELTY ASSESSMENT AND CONTRIBUTION BOUNDING

**Date:** 2026-10-19  
**Auditor:** Autonomous Methodology & Verification Specialist  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)

---

## 1. Executive Novelty Determination

### Gate B Assessment: **PASS WITH STRICT BOUNDING (GO)**

The core contribution of this work is **scientifically defensible and distinct from prior literature**, provided that its empirical boundaries are stated with rigorous scientific honesty. Prior work in multilingual RAG has either addressed open-domain generative QA (XRAG, CrossRAG) or treated cross-lingual verification error as an undifferentiated, monolithic failure rate (Singhal et al., 2024; Chang et al., 2023). 

However, several claims made in the initial project draft must be narrowed to avoid overstatement or rejection by peer reviewers:

---

## 2. Rigorous Breakdown: What Is Defensible vs. What Must Be Reframed

### A. Genuinely Defensible Contributions:
1. **First Controlled Error Disentanglement in Cross-Lingual Verification:**  
   Decoupling verification failures into:
   - Translation-induced semantic corruption ($E_{\text{trans}}$, 36.9% of failures), and
   - Verifier reasoning shortcomings on preserved semantics ($E_{\text{verif}}$, 55.0% of failures).
   This provides the NLP community with the first quantitative measurement of the "translation error tax" in automated misinformation detection.
2. **Empirical Demonstration of Negative Transfer in Naive Consensus:**  
   Proving that naive dual-language consensus (averaging translated and original posterior probabilities, `Always-Check`) degrades accuracy (to 31.29%), and that risk-calibrated selective routing significantly outperforms it ($p = 0.0294$ McNemar test; $p = 0.0420$ permutation test).
3. **Risk-Calibrated Selective Fallback Mechanism:**  
   Showing that an automated risk trigger combining predictive uncertainty (entropy / max probability) and lexical/numeral preservation can gate expensive original-evidence consultation.

### B. Overstatements and Necessary Boundary Corrections:
1. **Task Framing ("RAG" vs. "Claim Verification"):**  
   - *Draft Claim:* "Cross-Lingual Retrieval-Augmented Generation (RAG)".
   - *Audited Reality:* The experiments evaluate claim verification over **static, pre-retrieved web snippets** from the X-Fact corpus; there is no live neural retriever or generative decoder in the loop.
   - *Required Framing:* The paper must accurately define the task as **Evidence-Grounded Cross-Lingual Claim Verification** (or *Cross-Lingual Verifier Decisions in RAG Pipelines*), not live RAG system development.
2. **Claim of Superiority over Native Multilingual Models:**  
   - *Draft Claim:* Implied that Selective-Check is a breakthrough over evaluating original evidence directly.
   - *Audited Reality:* Selective-Check achieves 39.26% accuracy vs. Direct Multilingual's 37.42% accuracy (a difference of only 3 items out of 163, McNemar $p = 0.6072$, completely non-significant).
   - *Required Framing:* Selective-Check is an **efficiency and fallback safeguard for English-centric pipelines**, proving that pipelines can maintain translated throughput while selectively recovering accuracy on high-risk items, rather than claiming dominance over full multilingual processing.
3. **Operational Surrogate vs. True Causal Ground Truth:**  
   - *Draft Claim:* The 41 cases in $E_{\text{trans}}$ were described as "causally proven translation corruptions".
   - *Audited Reality:* $E_{\text{trans}}$ is defined operationally by model agreement ($\hat{y}_{\text{trans}} \ne y^*$ and $\hat{y}_{\text{orig}} = y^*$). Without bilingual human inspection, some flips may reflect verifier brittleness rather than pure translation errors.
   - *Required Framing:* Explicitly acknowledge that operational error attribution serves as an algorithmic diagnostic surrogate, and supply an audited human annotation protocol.

---

## 3. Ranked Defensible Contribution Alternatives

| Option | Formulation Title | Contribution Stated | Feasibility & Defensibility | Recommendation |
|:---:|:---|:---|:---:|:---:|
| **Option 1** | **Diagnostic Decoupling of Translation Fragility in Cross-Lingual Claim Verification** | Decouples $E_{\text{trans}}$ from $E_{\text{verif}}$ on authentic Hindi news; demonstrates negative transfer in dual consensus; evaluates selective cascade. | **Highest.** Grounded in exact verified experimental data; robust to peer scrutiny; answers an unresolved question left open by Singhal et al. (2024). | **RECOMMENDED** |
| **Option 2** | **When Does Translation Hurt? Failure Modes of Translate-then-Verify Pipelines** | Focuses purely on error taxonomy, cataloging semantic primitives (negation, numbers, entities) that break under MarianMT. | High, but narrower scope (descriptive rather than algorithmic). | Alternative |
| **Option 3** | **Selective Multilingual Verification Cascades** | Focuses on optimal routing and threshold selection algorithms for cross-lingual NLP. | Moderate, weakened by the non-significant gap between Selective and Direct Multilingual ($p=0.6072$). | Deprioritized |

### Decision:
Proceed with **Option 1**, framing the research as a rigorous diagnostic and methodological study isolating translation-fidelity corruption from verifier reasoning failures, with selective original-evidence fallback as a principled safeguard against negative consensus transfer.
