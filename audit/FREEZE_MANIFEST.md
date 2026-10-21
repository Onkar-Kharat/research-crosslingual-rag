# Research Freeze Manifest

**Project Title:** Cross-Lingual Evidence Verification: Prediction Sensitivity and Routing Disagreement Under Hindi-to-English Translation Shift  
**Protocol Version:** `v1.0-observational`  
**Certified Status:** `COMPUTATIONAL STUDY FROZEN — HUMAN VALIDATION PENDING` (Status B)  
**Deliverable Archive:** `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip`  
**Date:** 2026-10-24  

---

## 1. What Is Frozen

The following research assets are formally and permanently **FROZEN**:

1. **Experimental Scope and Task Definition:**
   - Scope is locked to observational prediction sensitivity and routing disagreement under Hindi-to-English translation shift.
   - Prohibited from manuscript: End-to-end RAG claims, causal translation error claims, and confirmatory test-set generalization.

2. **Data Splits and Preprocessing:**
   - Development split (103 instances) in `data/splits/hindi_dev.jsonl`.
   - Test split (163 instances) in `data/splits/hindi_test.jsonl`.
   - Mapped veracity labels: `CONTRADICTED`, `INSUFFICIENT_EVIDENCE`.

3. **Inference Pipeline & Threshold Selection:**
   - Verifier checkpoint: `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`.
   - MT checkpoint: `Helsinki-NLP/opus-mt-hi-en`.
   - Selected routing threshold: $\tau^* = 0.650$ (selected dev-only).
   - Per-instance canonical predictions in `experiments/results_canonical/test_predictions.jsonl`.

4. **Canonical Metrics and Statistical Tests:**
   - All values recorded in `canonical_results.csv` and `FINAL_PASS/CANONICAL_VALUES_TABLE.csv`.
   - Paired prediction agreement (36.20%), disagreement (63.80%), $\text{SUP} \to \text{CON}$ flip rate (48.44%).
   - McNemar significance tests, Benjamini-Hochberg FDR corrections, and 100-seed random routing control.

5. **Human Annotation Infrastructure:**
   - Self-contained offline tool in `annotation_tool/app/index.html`.
   - Blinded handoff bundles: `PACKET_A_HANDOFF.zip` and `PACKET_B_HANDOFF.zip`.
   - Automated validator (`validate_submissions.py`) and agreement analyzer (`analyze_agreement.py`).
   - Human annotation status: **BLOCKED (PENDING EXTERNAL EVALUATION)**.

---

## 2. Core File Hashes (SHA-256)

| File Path | SHA-256 Hash |
|---|---|
| `audit/FROZEN_PROTOCOL.md` | `b2149e6f3eb129ef9f79883ea545089e02316e626e64115fc3a23a8ff0f81d18` |
| `audit/FREEZE_AUDIT.md` | `9b139031efb7cebb1ae1b359c1ee9542a4dfd60e7f910be306cfc25c60205dfb` |
| `canonical_results.csv` | `0370d061730d0fb9023faeb595e33d26508f7db0102b3769941a318e8d893452` |
| `experiments/results_canonical/canonical_benchmark_table.csv` | `75dbb1a8d0092c423e200155b4104051bf73c0bc5e56e01ce4cbfe7da3c52a55` |
| `experiments/results_canonical/canonical_statistical_tests.csv` | `d720eb07662abebc3fb357a7d4a04fc9ea76c0e9b9c9f69796ff07742da5302d` |
| `experiments/results_canonical/canonical_dev_tuning.csv` | `88880629532675d31dca21d0061e86055d7b5b5c9071066d5cf5d7cbf0d8c035` |
| `data/splits/hindi_dev.jsonl` | `b9991206103632fc6132cb0a5638c4b92b6a5a22c5478eb04a377b0eb811fb2d` |
| `data/splits/hindi_test.jsonl` | `1ff62a74c49df5d2334969248235e16541334c9c614532a82fa2001c3bf7e231` |
| `scripts/run_corrected_experiments.py` | `d9e03d98c257b9e38f99e3a35b1c8c88f918e7e17c093e0b82f87a810f69a538` |
| `scripts/compute_evaluation_metrics_corrected.py` | `0ca0be0ec5d0ff97c27771ae2ce2ee388a1be5ca278f24419ad24f61b7fcf773` |
| `annotation_tool/packets/PACKET_A_HANDOFF.zip` | `1eb9d5926ec2f68894459f6323c2fa3f20f01c876b6b7daae63510c4fa77ef86` |
| `annotation_tool/packets/PACKET_B_HANDOFF.zip` | `bf4052ca133efb276b5c65449755d9d71398867a05eb2c92bfad5e82b7eb6443` |

*(Complete 368-file SHA-256 manifest is permanently preserved in `FINAL_PASS/SHA256SUMS.txt`)*

---

## 3. Canonical Reproduction Commands

To reproduce the research validation from a clean extraction:

```bash
# 1. Run all 42 automated regression tests
python tests/run_all_tests.py

# 2. Recompute canonical metrics and benchmark tables from predictions
python scripts/compute_evaluation_metrics_corrected.py

# 3. Regenerate publication figures
python scripts/generate_publication_figures.py

# 4. Verify annotation tool submission validator
python annotation_tool/scripts/validate_submissions.py \
  --file1 annotation_tool/tests/fixtures/valid_submission_A1.json \
  --file2 annotation_tool/tests/fixtures/valid_submission_A2.json
```

---

## 4. Final Certification

**Official Status:** `COMPUTATIONAL STUDY FROZEN — HUMAN VALIDATION PENDING` (Status B)  
All computational gates have passed; research values are verified against raw predictions; the repository is frozen.
