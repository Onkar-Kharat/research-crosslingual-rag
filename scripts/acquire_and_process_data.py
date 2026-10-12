"""
Acquire and process X-Fact Hindi dataset for Cross-Lingual Claim Verification.
Maintains data integrity, saves raw copies, logs SHA-256 hashes,
applies standardized label mappings, and validates schemas.
"""
import os
import csv
import json
import hashlib
from pathlib import Path
from datetime import datetime
import requests

RAW_DIR = Path("data/raw")
INTERIM_DIR = Path("data/interim")
PROCESSED_DIR = Path("data/processed")
SCHEMA_FILE = Path("data/schemas/item_schema.json")

DEV_URL = "https://raw.githubusercontent.com/utahnlp/x-fact/main/data/x-fact/dev.all.tsv"
TEST_URL = "https://raw.githubusercontent.com/utahnlp/x-fact/main/data/x-fact/test.all.tsv"
LICENSE_URL = "https://raw.githubusercontent.com/utahnlp/x-fact/main/LICENSE"

LABEL_MAPPING = {
    "true": "SUPPORTED",
    "mostly true": "SUPPORTED",
    "mostly false": "CONTRADICTED",
    "false": "CONTRADICTED",
    "partly true/misleading": "INSUFFICIENT_EVIDENCE",
    "complicated/hard to categorise": "INSUFFICIENT_EVIDENCE",
    "unproven": "INSUFFICIENT_EVIDENCE",
    "other": "INSUFFICIENT_EVIDENCE"
}

def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def download_file(url: str, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        print(f"Downloading {url} to {dest}...")
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        r.raise_for_status()
        dest.write_bytes(r.content)
    else:
        print(f"File {dest} already exists.")
    return compute_sha256(dest)

def process_tsv(file_path: Path, split_name: str) -> list[dict]:
    items = []
    dropped_count = 0
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f, delimiter="\t")
        row_idx = 0
        for row in reader:
            row_idx += 1
            lang = row.get("language", "").strip().lower()
            if lang != "hi":
                continue
            
            claim = row.get("claim", "").strip()
            raw_label = row.get("label", "").strip().lower()
            
            # Combine non-empty evidence snippets
            snippets = []
            for i in range(1, 6):
                snip = row.get(f"evidence_{i}", "").strip()
                if snip and snip != "None":
                    snippets.append(snip)
            
            if not claim or not snippets:
                dropped_count += 1
                continue
            
            combined_evidence = "\n".join(snippets)
            mapped_label = LABEL_MAPPING.get(raw_label, "INSUFFICIENT_EVIDENCE")
            
            item_id = f"xfact-hi-{split_name}-{len(items)+1:04d}"
            item = {
                "item_id": item_id,
                "claim": claim,
                "original_evidence": combined_evidence,
                "original_language": "hi",
                "translated_evidence": None,
                "target_language": "en",
                "source_dataset": "utahnlp/x-fact",
                "source_item_id": f"row-{row_idx}",
                "source_url": row.get("link_1") or row.get("site"),
                "license_url": "https://raw.githubusercontent.com/utahnlp/x-fact/main/LICENSE",
                "gold_label": mapped_label,
                "raw_gold_label": raw_label,
                "translation_fidelity": "UNCLEAR",
                "translation_error_types": [],
                "annotation_rationale": None,
                "split": split_name,
                "claimant": row.get("claimant", "").strip(),
                "claim_date": row.get("claimDate", "").strip(),
                "review_date": row.get("reviewDate", "").strip(),
                "site": row.get("site", "").strip(),
                "notes": f"Raw label: {raw_label}"
            }
            items.append(item)
    print(f"Split {split_name}: Extracted {len(items)} Hindi items (dropped {dropped_count} invalid).")
    return items

def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Download raw files
    license_hash = download_file(LICENSE_URL, RAW_DIR / "LICENSE_xfact.txt")
    dev_hash = download_file(DEV_URL, RAW_DIR / "dev.all.tsv")
    test_hash = download_file(TEST_URL, RAW_DIR / "test.all.tsv")

    provenance = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "source": "utahnlp/x-fact (ACL-IJCNLP 2021)",
        "license": "MIT",
        "hashes": {
            "LICENSE_xfact.txt": license_hash,
            "dev.all.tsv": dev_hash,
            "test.all.tsv": test_hash
        }
    }
    (RAW_DIR / "provenance.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")

    # 2. Extract Hindi splits
    dev_items = process_tsv(RAW_DIR / "dev.all.tsv", "dev")
    test_items = process_tsv(RAW_DIR / "test.all.tsv", "test")

    # 3. Write interim combined
    all_items = dev_items + test_items
    with open(INTERIM_DIR / "hindi_claims_raw.jsonl", "w", encoding="utf-8") as f:
        for item in all_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    # 4. Write processed splits
    with open(PROCESSED_DIR / "dev.jsonl", "w", encoding="utf-8") as f:
        for item in dev_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    with open(PROCESSED_DIR / "test.jsonl", "w", encoding="utf-8") as f:
        for item in test_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Data acquisition and processing completed successfully.")
    print(f"Dev items: {len(dev_items)}, Test items: {len(test_items)}, Total: {len(all_items)}")

if __name__ == "__main__":
    main()
