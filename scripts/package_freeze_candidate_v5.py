"""
Packaging script for candidate V5:
CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_V5_FROZEN_EXPLORATORY.zip
"""
import zipfile
import hashlib
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ZIP_NAME = "CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_V5_FROZEN_EXPLORATORY.zip"
OUTPUT_ZIP = PROJECT_ROOT / ZIP_NAME

EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".idea",
    ".vscode",
    "verify_extraction_test",
    "verify_extraction_v5",
    "extracted_original"
}

EXCLUDE_EXTS = {
    ".pyc",
    ".zip"
}

def should_exclude(path: Path) -> bool:
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    if path.suffix.lower() in EXCLUDE_EXTS:
        return True
    return False

def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def package():
    print(f"Creating versioned archive: {OUTPUT_ZIP.name}")
    start_time = time.time()
    count = 0
    total_bytes = 0

    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in PROJECT_ROOT.rglob("*"):
            if p.is_file():
                if should_exclude(p.relative_to(PROJECT_ROOT)):
                    continue
                rel_path = p.relative_to(PROJECT_ROOT)
                zf.write(p, arcname=str(rel_path))
                count += 1
                total_bytes += p.stat().st_size

    duration = time.time() - start_time
    zip_size = OUTPUT_ZIP.stat().st_size
    sha256_hash = compute_sha256(OUTPUT_ZIP)

    print(f"Archive created successfully in {duration:.2f}s:")
    print(f"  Files included: {count}")
    print(f"  Uncompressed size: {total_bytes / (1024*1024):.2f} MB")
    print(f"  Compressed size:   {zip_size / (1024*1024):.2f} MB")
    print(f"  SHA256:            {sha256_hash}")

    manifest_line = f"{sha256_hash}  {ZIP_NAME}\n"
    manifest_path = PROJECT_ROOT / "audit" / "v5_archive_sha256.txt"
    manifest_path.write_text(manifest_line, encoding="utf-8")
    print(f"Saved checksum to {manifest_path}")

if __name__ == "__main__":
    package()
