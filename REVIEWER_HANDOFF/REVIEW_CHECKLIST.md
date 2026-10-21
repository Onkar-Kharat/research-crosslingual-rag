# REVIEWER CHECKLIST: Verification Protocol for Independent Review

**Intended Auditor:** Independent LLM / Peer Reviewer (e.g., ChatGPT)  
**Package:** `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip`  
**Purpose:** Actionable checklist to independently verify the research freeze claims against actual repository files.  

---

## 1. Core Verification Checklist

Please verify the following 8 items directly against the extracted files:

- [ ] **1. Test Suite Passes (43 Tests):**
  - *How to verify:* Run `python tests/run_all_tests.py` in the activated virtual environment.
  - *Expected:* Exactly 43 tests pass across 8 test modules in `< 1.0 second` with exit code `0`.

- [ ] **2. Primary Sensitivity Metrics Recompute Exactly:**
  - *File to inspect:* `experiments/results_canonical/canonical_test_predictions.csv` ($N=163$).
  - *How to verify:*
    ```python
    import pandas as pd
    df = pd.read_csv('experiments/results_canonical/canonical_test_predictions.csv')
    assert (df['pred_translated'] != df['pred_original']).sum() == 104  # 63.80%
    assert (df['pred_translated'] == df['pred_original']).sum() == 59   # 36.20%
    sup_con = ((df['pred_translated'] == 'SUPPORTED') & (df['pred_original'] == 'CONTRADICTED')).sum()
    assert sup_con == 31  # 31 / 64 = 48.44%
    ```
  - *Expected:* All assertions pass.

- [ ] **3. Statistical Tests Reconciled ($b=23, c=47$):**
  - *Files to inspect:* `experiments/results_canonical/canonical_statistical_tests.csv` and `canonical_results.csv`.
  - *How to verify:* Check row for Selective vs Direct Multilingual. Verify that $b=23, c=47$ is reported, yielding $\chi^2 = (24-1)^2/70 = 7.5571$ ($p = 0.00558$). Confirm that stale $b=7, c=31$ does not appear in active files.

- [ ] **4. Duplicated-Claim Issue Traced to Raw Benchmark:**
  - *Files to inspect:* `data/raw/dev.all.tsv` and `data/raw/test.all.tsv`.
  - *How to verify:*
    ```python
    import csv
    for fn, count, total in [('data/raw/dev.all.tsv', 54, 103), ('data/raw/test.all.tsv', 88, 163)]:
        rows = [r for r in csv.DictReader(open(fn, encoding='utf-8'), delimiter='\t') if r.get('language') == 'hi']
        pref = sum(1 for r in rows if r.get('evidence_1','').startswith(r.get('claim','')))
        assert pref == count and len(rows) == total
    ```
  - *Expected:* Confirmed as an intrinsic property of X-Fact Google search snippets from news outlets (e.g., *Aaj Tak*). Review `audit/DUPLICATED_CLAIM_EVIDENCE_AUDIT.md`.

- [ ] **5. Development Split Label Counts Reconciled:**
  - *File to inspect:* `data/processed/dev.jsonl` ($N=103$).
  - *How to verify:*
    ```python
    import json
    dev = [json.loads(line)['gold_label'] for line in open('data/processed/dev.jsonl', encoding='utf-8')]
    assert dev.count('CONTRADICTED') == 89
    assert dev.count('INSUFFICIENT_EVIDENCE') == 14
    assert dev.count('SUPPORTED') == 0
    ```
  - *Expected:* Exactly 89 / 14 / 0. Verify that `protocol/FINAL_SCOPE_AND_CLAIMS.md` reports 89 / 14.

- [ ] **6. Development-Only Threshold Selection ($J_{\text{No-Check}} > J_{\text{Cascade}}$):**
  - *File to inspect:* `experiments/results_canonical/canonical_dev_tuning.csv`.
  - *How to verify:* Check row $\tau=0.650$ ($J = 0.2023$). Compare against No-Check baseline ($J = 0.2104$). Confirm that the negative result ($\Delta J = -0.0081$) is reported transparently and not concealed by post-hoc objective tweaking.

- [ ] **7. Human Annotation Integrity (Gate C Blocked):**
  - *Directory to inspect:* `annotation_tool/submissions/`.
  - *How to verify:* Verify that `submissions/` contains zero completed annotations. Verify that `scripts/perform_bilingual_annotation.py` raises `RuntimeError`. Confirm that zero synthetic annotations are reported as real human data.

- [ ] **8. Release Manifest and File Hashes Match:**
  - *Files to inspect:* `experiments/results_canonical/RUN_MANIFEST.json` and `audit/RELEASE_MANIFEST_SHA256.txt`.
  - *How to verify:* Run `python scripts/build_canonical_manifest.py`. Confirm that all SHA-256 hashes match.

---

## 2. Potential Audit Risks & How This Release Mitigates Them

| Potential Risk | Reviewer Concern | Where to Inspect Mitigation in This Archive |
|:---|:---|:---|
| **P-Hacking or Label Cherry-Picking** | Did authors cherry-pick $b=23, c=47$ or $b=7, c=31$? | `audit/STATISTICAL_REANALYSIS.md` provides the exact mathematical proof that $\chi^2=7.5571$ mathematically requires $(24-1)^2/70$ ($b=23, c=47$). |
| **Data Leakage into Threshold Tuning** | Was $\tau^*=0.650$ tuned on test data? | `audit/THRESHOLD_AND_TEST_CONTAMINATION_AUDIT.md` verifies that the sweep was conducted exclusively on 103 dev items, and `tests/test_reproduced_artifacts_v4.py` enforces trigger consistency. |
| **Synthetic Annotations Presented as Human** | Are any human claims simulated? | `audit/ANNOTATION_STATUS.md` explicitly declares Gate C pending/unexecuted. All simulated annotations are quarantined in `audit/invalidated_synthetic_annotations/`. |
| **Pipeline Destination Confusion** | Is it `results_corrected` or `results_canonical`? | `audit/CANONICAL_PIPELINE_AUDIT.md` confirms `experiments/results_canonical/` is the sole direct output destination. |
