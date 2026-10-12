# Data Documentation and Provenance

## 1. Primary Dataset: X-Fact (Hindi Subset)
- **Source:** Utah NLP `utahnlp/x-fact` (Gupta & Srikumar, ACL-IJCNLP 2021)
- **Paper:** *X-FACT: A New Benchmark Dataset for Multilingual Fact Checking*
- **License:** MIT License (archived locally in `data/raw/LICENSE_xfact.txt`)
- **Acquisition Date:** 2026-10-15
- **Language:** Hindi (`hi`) with web search evidence passages retrieved from authentic fact-checking outlets (e.g., `hindi.newschecker.in`, `aajtak.in`).

## 2. Integrity and Checksums (SHA-256)
- `data/raw/LICENSE_xfact.txt`: `21c8eb0210067b344db0dc338d3c4fa4d97be9b8a33699018d0c30a744f0af55`
- `data/raw/dev.all.tsv`: `faed99c2ee9e7ea505a1bae88c06bd2c686804b5e1e786551e589b5f89df8199`
- `data/raw/test.all.tsv`: `b126a4f7e16ec72f554a79e1fffaef8d71ba03ec9e07072ff7484a502cf37cbb`

## 3. Directory Structure
- `data/raw/`: Immutable upstream downloads directly from the source repository.
- `data/interim/`: Combined Hindi instances extracted across splits (`hindi_claims_raw.jsonl`).
- `data/processed/`: Normalized, schema-validated partitions:
  - `dev.jsonl`: Development split ($N = 103$). Used strictly for hyperparameter/threshold tuning and pilot evaluation.
  - `test.jsonl`: Final evaluation test split ($N = 163$). Held-out for blind evaluation.

## 4. Label Mapping
To conform to standard 3-way fact verification while preserving source fidelity:
- `true` / `mostly true` $\rightarrow$ `SUPPORTED`
- `false` / `mostly false` $\rightarrow$ `CONTRADICTED`
- `partly true/misleading` / `complicated/hard to categorise` / `unproven` $\rightarrow$ `INSUFFICIENT_EVIDENCE`

Both the original `raw_gold_label` and the standardized `gold_label` are preserved in every record.

## 5. Schema Compliance
All processed records conform to `data/schemas/item_schema.json`.
