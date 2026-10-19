# Decision log

Append dated decisions, evidence, alternatives and reasons. Never overwrite prior decisions.

## 2026-10-15: Gate A — Literature Audit & Novelty Gate Decision
- **Decision:** PROCEED (GO) to Phase 2 (Study Protocol & Dataset Acquisition) with refined research questions and frozen scope.
- **Evidence:**
  1. Audited 7 key related works (Liu et al. Findings of EMNLP 2025; Ranaldi et al. Findings of EACL 2026; Wang et al. ACL 2026; Singhal et al. 2024; Shcharbakova et al. FEVER 2025; XFEVER 2023; Gupta & Srikumar ACL-IJCNLP 2021).
  2. Closest prior work is Singhal et al. (arXiv:2410.10303), which evaluated pre-translation and self-translation on X-Fact across 15 languages, and Shcharbakova et al. (FEVER 2025), which benchmarked models on X-Fact.
  3. **Identified & Defensible Research Gap:** Prior work evaluates end-to-end classification accuracy under translation or direct inference as a monolithic metric. No prior work jointly establishes:
     - (a) A controlled paired comparison on identical claim-evidence pairs under original vs. machine-translated evidence;
     - (b) A systematic, taxonomy-grounded error attribution separating meaning-altering translation-fidelity errors (e.g. polarity, numerical, entity distortions) from verifier-reasoning failures (where meaning is preserved but the model misreasons);
     - (c) A selective original-evidence verification mechanism (cascading from fast translated evidence to original evidence upon uncertainty/risk trigger) benchmarked against no-check and always-check baselines with empirical coverage-accuracy-latency trade-offs.
  4. **Language Pair:** English-Hindi (as specified in Master Prompt), with potential expansion only if justified.
  5. **Dataset Choice:** X-Fact (Gupta & Srikumar, ACL-IJCNLP 2021), distributed under the open MIT License, providing authentic real-world claims, search evidence snippets, and expert veracity labels in Hindi and English.
- **Alternatives Considered:**
  - *Alternative 1 (Synthetic FEVER translation like XFEVER):* Rejected because synthetic Wikipedia mutations do not reflect realistic web search snippet noise and nuanced translation failures.
  - *Alternative 2 (Abandoning selective checking and only doing error analysis):* Rejected because the master prompt and TACL standards require actionable algorithmic contribution/mitigation alongside diagnostic analysis.
- **Next Step:** Write `reports/literature_audit.md`, freeze protocol, acquire and validate X-Fact Hindi/English subsets under strict license/schema checks, and construct pilot dataset.