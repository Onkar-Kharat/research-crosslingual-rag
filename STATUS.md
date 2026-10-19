# Research Status

**Current Phase:** Candidate V3 Critical Repair Completed — Package Verified (NOT FROZEN)  
**Working Topic:** Evidence-Grounded Cross-Lingual Claim Verification Diagnostic Study: Separating Translation-Fidelity and Verifier-Reasoning Errors (Hindi $\rightarrow$ English)  
**Target Venue:** Transactions of the Association for Computational Linguistics (TACL)  
**Deliverable Archive:** [`CROSS_LINGUAL_RAG_RESEARCH_FREEZE_CANDIDATE_V3_NOT_FROZEN.zip`](file:///c:/Users/Onkar/OneDrive/Desktop/Research_crosslingual_rag_research/CROSS_LINGUAL_RAG_RESEARCH_FREEZE_CANDIDATE_V3_NOT_FROZEN.zip)  
**Gate Status:** Gate A (REPAIRED), Gate B (PASS), Gate C (BLOCKED), Gate D (PASS), Gate E (PASS). Overall: **NOT FROZEN**  
**Environment:** Windows 11 AMD64; 18 logical cores; local `.venv` (Python 3.14.7, PyTorch 2.14.1 CPU, Transformers 5.19.0)  
**Budget:** Strictly free open-source tools and public benchmark data; $0 spend; zero paid APIs  
**Language Pair:** English--Hindi ($L_t = \text{en}$, $L_s = \text{hi}$) on X-Fact benchmark  

---

## Critical Repair Checkpoints (Candidate V3)
- [x] **Phase 0: Intake & Legacy Quarantine:** Hashed 82 legacy entries in `audit/v2_archive_manifest.csv`; quarantined legacy prediction files into `legacy/` under `legacy/README_LEGACY.md`; logged all 9 issues in `BLOCKER_LEDGER.csv`.
- [x] **Phase 1: Code Portability & Environment Hygiene:** Eliminated all hardcoded paths (`C:\Users\...`) across scripts and tests in favor of dynamic relative paths; corrected `audit/environment_report.json` using `psutil`, properly distinguishing physical RAM (15.61 GB) from storage capacity (463.36 GB).
- [x] **Phase 2: Task & Label Semantics Decision:** Authored `protocol/TASK_AND_LABEL_VALIDITY_DECISION.md`, detailing 3 formulation options and adopting Option C. Formally bounded study to observed 2-class veracity space (`CONTRADICTED` and `INSUFFICIENT_EVIDENCE`), mandating dual-F1 reporting. Verified model runtime logit mapping (`0: entailment`, `1: neutral`, `2: contradiction`). Reconciled tuning grid `[0.10, 0.65, 0.025]` in `protocol/analysis_plan.yaml`.
- [x] **Phase 3: Literature Audit & Novelty Bounding:** Replaced placeholder citations in `literature/LITERATURE_AUDIT.csv` with verified entries (Wang et al., ACL 2026 / `arXiv:2604.20199`; Chang et al., ROCLING 2023 / `2023.rocling-1.1`). Removed unvetted "first" priority claims in `literature/RELATED_WORK_MATRIX.md` and `literature/NOVELTY_ASSESSMENT.md`.
- [x] **Phase 4 & 6: Scratch Inference Rerun & Real Latency Measurement:** Executed end-to-end inference from scratch with true token truncation (`max_length=512`, `truncation=True`) and true Jaccard numeral overlap ($|A \cap B| / |A \cup B|$). Measured actual per-instance MarianMT generation time and verifier forward passes on CPU, saving canonical prediction files in `experiments/results_corrected/`.
- [x] **Phase 5: Re-evaluation & Comprehensive Ablations:** Generated full benchmark covering 9 conditions with exact 95% bootstrap CIs, paired exact McNemar tests, 5000-permutation F1 tests, and diagnostic error attribution.
- [x] **Phase 7: Blinded Annotator Packet Hygiene:** Created `annotation_handoff/ANNOTATOR_PACKET.zip` containing strictly blinded data, guidelines, protocol, and template, completely segregated from internal keys. Kept Gate C **BLOCKED** awaiting genuine human annotators.
- [x] **Phase 8: Packaging & Clean-Room Verification:** Authored `data/DATA_USE_AND_LICENSE_NOTES.md` and `README_RESEARCH_REPAIR.md`. Verified clean-room extraction and 100% test suite execution (16/16 tests pass).
