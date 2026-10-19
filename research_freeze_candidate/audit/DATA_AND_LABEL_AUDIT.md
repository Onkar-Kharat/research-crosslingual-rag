# DATA AND LABEL AUDIT REPORT: X-FACT HINDI

**Date:** 2026-10-19  
**Auditor:** Autonomous Methodology & Verification Specialist  
**Dataset:** X-Fact Hindi Subset (`utahnlp/x-fact`)  
**Raw Files Audited:** `data/raw/dev.all.tsv` (SHA256: `78e34...`), `data/raw/test.all.tsv` (SHA256: `a93b4...`)  
**Processed Files Audited:** `data/processed/dev.jsonl`, `data/processed/test.jsonl`

---

## 1. Provenance and Upstream Benchmark Integrity

The raw data originates from the official X-Fact benchmark created by Ashkan Gupta and Vivek Srikumar (ACL-IJCNLP 2021), hosted at `https://github.com/utahnlp/x-fact`.
- **License:** Open MIT License (`data/raw/LICENSE_xfact.txt`).
- **Nature of Data:** Real-world rumors and public claims collected from professional fact-checking organizations operating in India (e.g., *Aaj Tak Fact Check*, *Newschecker Hindi*, *Dainik Bhaskar*).
- **Evidence Structure:** Each claim was queried against Google Search by the X-Fact authors at dataset creation time; the top search result snippets were captured into `evidence_1` through `evidence_5`.
- **Architecture Caveat:** The current project does not perform live dense/sparse passage retrieval; it evaluates claim verification over pre-existing search snippets. Thus, the task is accurately defined as **Evidence-Grounded Cross-Lingual Claim Verification**, rather than full-pipeline Retrieval-Augmented Generation.

---

## 2. Raw Split Inventory and Extraction Verification

Using standard TSV parsing adhering to X-Fact formatting:
- **`dev.all.tsv`:** Total rows across 25 languages: 2,406.
  - Filtered Hindi (`language == 'hi'`): Exactly **103 items**.
  - Dropped / Empty: 0 items.
- **`test.all.tsv`:** Total rows across 25 languages: 3,657.
  - Filtered Hindi (`language == 'hi'`): Exactly **163 items**.
  - Dropped / Empty: 0 items.

Total authentic Hindi claim-evidence instances: **266 items** ($103 \text{ dev} + 163 \text{ test}$).

---

## 3. Label Schema Analysis and The Missing Positive Class

### Raw Veracity Labels in X-Fact Hindi:
| Split | Raw Label | Count | Percentage |
|:---|:---|:---:|:---:|
| **Dev ($N=103$)** | `false` | 45 | 43.69% |
| | `mostly false` | 44 | 42.72% |
| | `partly true/misleading` | 14 | 13.59% |
| | `true` / `mostly true` | **0** | **0.00%** |
| **Test ($N=163$)** | `mostly false` | 76 | 46.63% |
| | `false` | 66 | 40.49% |
| | `partly true/misleading` | 21 | 12.88% |
| | `true` / `mostly true` | **0** | **0.00%** |
| **Combined ($N=266$)** | `mostly false` | 120 | 45.11% |
| | `false` | 111 | 41.73% |
| | `partly true/misleading` | 35 | 13.16% |
| | `true` / `mostly true` | **0** | **0.00%** |

### Mapping to Verification Classes:
In `scripts/acquire_and_process_data.py`, the mapping logic was:
- `true`, `mostly true` $\rightarrow$ `SUPPORTED`
- `false`, `mostly false` $\rightarrow$ `CONTRADICTED`
- `partly true/misleading`, `unproven`, `complicated/hard to categorise`, `other` $\rightarrow$ `INSUFFICIENT_EVIDENCE`

Under this mapping:
- **Dev Ground Truth:** 89 `CONTRADICTED` (86.41%), 14 `INSUFFICIENT_EVIDENCE` (13.59%), **0 `SUPPORTED` (0.00%)**.
- **Test Ground Truth:** 142 `CONTRADICTED` (87.12%), 21 `INSUFFICIENT_EVIDENCE` (12.88%), **0 `SUPPORTED` (0.00%)**.

### Critical Scientific Findings:
1. **Absence of True Claims in Source Fact-Checks:**  
   In India, professional fact-checking organizations almost exclusively investigate viral social media misinformation, political disinformation, and manipulated media. Verified factual truths rarely warrant published debunking articles. Consequently, the Hindi subset of X-Fact contains **zero positive assertions validated as true**.
2. **Impact on 3-Class Macro-F1 Metric:**  
   The prior paper reported "Macro-F1" across 3 classes ($\textsc{Supported}, \textsc{Insufficient}, \textsc{Contradicted}$). Because the gold support for `SUPPORTED` is 0:
   - True Positives for `SUPPORTED` $= 0$.
   - False Negatives for `SUPPORTED` $= 0$.
   - Recall is undefined ($0/0$), treated as $0.0$ by convention.
   - Precision is $0.0$ whenever the model erroneously predicts `SUPPORTED` (which occurred on 57 test items for No-Check and 68 test items for Original).
   - Thus, $F_1(\textsc{Supported}) = 0.0$.
   - The reported 3-class Macro-F1:
     $$\text{Macro-F1}_{3\text{-class}} = \frac{F_1(\textsc{Contradicted}) + F_1(\textsc{Insufficient}) + 0.0}{3}$$
   This artificially deflated all reported Macro-F1 scores by exactly one-third!
3. **Correct Reporting Requirement:**
   - Both **3-class Macro-F1** (standard NLI space) and **observed 2-class Macro-F1** (evaluating only the classes actually present: `CONTRADICTED` and `INSUFFICIENT_EVIDENCE`) must be transparently reported side-by-side.
   - The paper and documentation must explicitly state: *“Authentic journalistic fact-checks in the Hindi X-Fact partition consist exclusively of debunked claims (87.1% refuted, 12.9% misleading/insufficient), containing no validated positive claims.”*

---

## 4. Leakage, Partition Integrity, and Test Set History

1. **Item ID & Event Leakage:**
   - Dev items (`xfact-hi-dev-0001` to `0103`) and Test items (`xfact-hi-test-0001` to `0163`) were inspected for claim textual overlap and URL overlap.
   - No duplicate claims or shared URLs were found between Dev and Test.
   - Partition separation conforms to the official X-Fact benchmark splits.
2. **Prior Test Set Exposure (Audit Finding):**
   - In the prior development iteration (`EXP-001`), threshold $\tau^* = 0.30$ was tuned strictly on the development split (`dev_threshold_tuning.csv`). Test set labels were NOT used to optimize $\tau^*$.
   - However, the full test set was evaluated, and its predictions were saved in `test_predictions.csv` and analyzed.
   - In accordance with Phase 3 instructions, because the test set has been previously inspected, it cannot be claimed as an untouched virgin evaluation set. All confirmatory conclusions must be clearly documented with this history, or accompanied by cross-validation / perturbation controls.

---

## 5. Redistribution and Licensing Compliance

- Upstream X-Fact code and annotations are licensed under the MIT License.
- Processed JSONL files (`dev.jsonl`, `test.jsonl`, `dev_translated.jsonl`, `test_translated.jsonl`) contain public news claim snippets and can legally be redistributed for scientific research under the MIT License and Fair Use provisions for fact-checking research.
- Full provenance metadata, source URLs, and original claimant attribution are preserved in every record.
