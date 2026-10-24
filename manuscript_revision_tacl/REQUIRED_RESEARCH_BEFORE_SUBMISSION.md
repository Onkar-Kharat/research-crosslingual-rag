# Required Research and Author Decision Plan Before External Submission

**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Document Status:** Actionable Author Decision & Research Roadmap  
**Date:** 2026-10-24  

---

## Category 1: Must Fix / Verify Before Submission (Within Frozen Scope)

These items require zero changes to the frozen research and can be completed or verified by the authors immediately:

| Item ID | Task & Requirement | Why It Matters | Status in Revised Manuscript | Author Action Needed |
| :--- | :--- | :--- | :---: | :---: |
| **REQ-01** | **Select Submission PDF File** | TACL requires double-blind anonymous submission with running line numbers. Submitting the author preview PDF would cause desk rejection. | Handled: Both `submission.pdf` (anonymous with line numbers) and `main.pdf` (author preview) are built and ready. | Verify that `submission.pdf` is uploaded to the Open Journal Systems (OJS) portal. |
| **REQ-02** | **Verify Anonymous Review Metadata** | PDF document metadata and title page must not contain names or affiliations. | Handled: Audited via binary search; zero author occurrences in `submission.pdf`. | None; verified compliant. |
| **REQ-03** | **Confirm Editorial Framing** | Paper must be framed as an *Exploratory Computational Diagnostic Study* rather than a confirmatory benchmark. | Handled: Updated across Abstract, Intro, Limitations, and Conclusion. | Approve the transparent scope framing. |
| **REQ-04** | **Multiple Testing Terminology** | Must state that Benjamini-Hochberg controls False Discovery Rate (FDR), not Family-Wise Error Rate (FWER). | Handled: Corrected in Table 5 caption and Section 5.3. | None; verified compliant. |

---

## Category 2: Strongly Recommended (Substantive Research Extensions)

These items would substantially elevate the paper from a Borderline exploratory diagnosis to a High-Acceptance TACL submission, but require executing new research beyond the frozen boundary:

| Item ID | Research Item | Why It Matters | Evidence Currently Missing | Feasible Without Changing Frozen Data? | Action / Approval Required |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **EXT-01** | **Execute Bilingual Human Annotation Protocol** | Answering *why* predictions flip ($48.44\%$ Supported $\to$ Contradicted) requires human ratings of translation fidelity and semantic shift. | Verified human annotations of the $N=104$ discordant claim-evidence pairs. | **No** (Requires recruiting 2+ native Hindi/English raters). | Author decision: Recruit bilingual linguists to execute Appendix A.4 protocol, or retain current observational scope. |
| **EXT-02** | **Multi-Language Family Expansion** | TACL reviewers expect multilingual contributions to span multiple language families (e.g., Arabic, Turkish, Tamil). | Empirical verification on non-Hindi language pairs. | **No** (Requires running pipeline on Arabic/Turkish X-Fact splits). | Author decision: Expand to 2 additional language families in a follow-up phase, or submit as a focused Hindi-to-English case study. |
| **EXT-03** | **Uninspected Confirmatory Split Evaluation** | Evaluating on a strictly uninspected holdout split eliminates any potential alpha inflation from prior test-set inspection. | Uninspected holdout partition. | **No** (Requires downloading and freezing a new holdout split). | Author decision: Retain exploratory classification in TACL, or prepare a fresh split. |

---

## Category 3: Optional Future Work (Long-Term Extensions)

These items represent natural avenues for post-publication or future project phases:

1. **End-to-End Multilingual RAG Integration:** Evaluating upstream dense document retrieval (e.g., mContriever, BGE-M3) jointly with evidence verification and downstream generative LLM answer synthesis.
2. **Learned Neural Arbitration Cascade:** Replacing the surface-level heuristic risk trigger ($r = 0.70(1-p_{\max}) + 0.30(1-\text{Jaccard})$) with a parameterized meta-classifier or small cross-lingual routing network trained to predict verifier disagreement.
3. **Alternative Translation Backbones:** Benchmarking commercial MT APIs (e.g., Google Cloud Translation, DeepL) and massive multilingual foundation translation models (e.g., NLLB-200) to isolate engine-specific translation quirks from cross-lingual representation alignment.

---

## Summary Author Decision Matrix

- **Option A (Submit Now to TACL as an Exploratory Diagnostic Paper):**  
  Submit [`submission.pdf`](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/manuscript_revision_tacl/submission.pdf). Rely on the paper's immaculate statistical reporting, transparent self-critical guardrails, and cautionary architectural findings. Expected outcome: Borderline review; possible Category (c) *Revise and Resubmit* inviting human annotations or second language.
- **Option B (Target EMNLP Findings, EACL, or TALLIP):**  
  Submit the current revised manuscript to a conference findings or regional language journal. The manuscript is already camera-ready, exceeds typical conference rigor, and has a very high acceptance probability in these venues without executing Category 2 research.
- **Option C (Execute Human Annotation Before Submission):**  
  Pause external submission, recruit two bilingual raters to annotate the 104 discordant items according to Appendix A.4, and incorporate inter-annotator agreement ($\kappa$) and causal error attribution into the manuscript.
