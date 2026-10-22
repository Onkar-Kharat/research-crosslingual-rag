# Research Status

**Current Phase:** Final Research Freeze  
**Adopted Scope:** Option C: Cross-Lingual Verifier Prediction Sensitivity and Routing Disagreement Under Translation Shift (Hindi $\rightarrow$ English)  
**Deliverable Archive:** [`CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip`](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip)  
**Gate Status:** Gate A (PASS), Gate B (PASS), Gate C (PENDING / NOT PERFORMED), Gate D (PASS), Gate E (PASS).  
**Overall Decision:** **FROZEN — EXPLORATORY COMPUTATIONAL STUDY**  
**Canonical Gate Ledger:** [`FREEZE_GATE_REPORT.md`](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/FREEZE_GATE_REPORT.md) (Single Authoritative Source of Truth)  
**Environment:** Windows 11 AMD64; 18 logical cores; local `.venv` (Python 3.14.7, PyTorch 2.14.1 CPU, Transformers 5.19.0)  
**Budget:** Strictly free open-source tools and public benchmark data; $0 spend; zero paid APIs  
**Language Pair:** English--Hindi ($L_t = \text{en}$, $L_s = \text{hi}$) on X-Fact benchmark ($N_{\text{dev}}=103$, $N_{\text{test}}=163$)  

---

## Critical Freeze Verifications
- [x] **Option C Scope Adoption:** Fixed scope to cross-lingual verifier prediction sensitivity and routing disagreement under translation shift. Pre-retrieved evidence verification only; no end-to-end RAG claim.
- [x] **Primary Descriptive Sensitivity Metrics:** Paired agreement is 36.20% (59/163), and paired disagreement is 63.80% (104/163).
- [x] **Real Human Annotation Workflow Built:** Engineered `annotation_tool/` with offline HTML5 app, blinded Packets A and B, schema validator, and pre-registered agreement scripts. Synthetic data quarantined. Real human submissions are pending external participant recruitment.
- [x] **Direct Translation-Verifier Coupling:** Pipeline decodes MarianMT generated translations directly into mDeBERTa under true token truncation ($\le 512$). End-to-end latency is measured on the exact pipeline used for inference.
- [x] **Dev Threshold Tuning with No-Check Baseline:** Evaluated complete dev grid including zero-check baseline. Confirmed No-Check ($J=0.2104$) achieves higher development utility than any cascade threshold ($\tau=0.650, J=0.2023$). Selective cascade routing is not Pareto-optimal on development data.
- [x] **Multi-Seed Random Control (100 Seeds):** Evaluated 100 seeds ($s \in 0..99$) with exact matched item counts ($K = \text{round}(N \cdot \text{Coverage}) = 13$). Mean accuracy: 29.24% [26.38%, 31.90%].
- [x] **Honest Empirical Results:** Selective-Check achieves identical accuracy (28.22%, 46/163) to No-Check (28.22%, $p=1.0000$) and trails Direct Multilingual (42.94%, $p=0.0056$). No-Check vs Direct Multilingual is $b=27, c=51$ ($p=0.0088$). No superiority claims are made.
- [x] **Exploratory Test Partition:** Test set ($N=163$) is designated as EXPLORATORY / PREVIOUSLY INSPECTED.
- [x] **Unified Source of Truth:** `FREEZE_GATE_REPORT.md` is the canonical gate ledger; all status files, manifests, and reports agree 100%.
- [x] **Test Suite & Reproducibility:** 47/47 automated tests passing in ~0.5s across 9 modules. Clean-room extraction verified.
