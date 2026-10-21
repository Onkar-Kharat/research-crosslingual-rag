"""
Comprehensive packaging, manifest generation, and clean-room verification script for V6:
CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip
"""

import hashlib
import os
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ZIP_NAME = "CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip"
OUTPUT_ZIP = PROJECT_ROOT / ZIP_NAME

EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".idea",
    ".vscode",
    "verify_extraction_test",
    "verify_extraction_v5",
    "verify_extraction_v6",
    "extracted_original",
    "scratch_extraction_v6",
    "test_qa_analysis",
    "scratch",
}

EXCLUDE_EXTS = {
    ".pyc",
}

def should_exclude(rel_path: Path) -> bool:
    # Check directory components
    for part in rel_path.parts:
        if part in EXCLUDE_DIRS:
            return True
            
    # Check file extensions
    if rel_path.suffix.lower() in EXCLUDE_EXTS:
        return True
        
    # Check root-level zip archives (keep handoff zips inside annotation_tool/packets/)
    if len(rel_path.parts) == 1 and rel_path.suffix.lower() == ".zip":
        return True
        
    return False

def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def gather_files():
    files = []
    for p in PROJECT_ROOT.rglob("*"):
        if p.is_file():
            rel_path = p.relative_to(PROJECT_ROOT)
            if not should_exclude(rel_path):
                files.append(rel_path)
    files.sort(key=lambda p: str(p).replace("\\", "/"))
    return files

def generate_checksum_manifest(files):
    manifest_path = PROJECT_ROOT / "FINAL_PASS" / "SHA256SUMS.txt"
    print(f"Generating checksum manifest: {manifest_path.relative_to(PROJECT_ROOT)}")
    lines = []
    for rel_path in files:
        if rel_path == Path("FINAL_PASS/SHA256SUMS.txt"):
            continue
        full_path = PROJECT_ROOT / rel_path
        h = compute_sha256(full_path)
        normalized_path = str(rel_path).replace("\\", "/")
        lines.append(f"{h}  {normalized_path}\n")
        
    manifest_path.write_text("".join(lines), encoding="utf-8")
    print(f"Manifest written with {len(lines)} file hashes.")
    return manifest_path

def build_zip(files):
    print(f"\nBuilding versioned deliverable archive: {OUTPUT_ZIP.name}")
    start_time = time.time()
    count = 0
    total_bytes = 0

    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel_path in files:
            full_path = PROJECT_ROOT / rel_path
            normalized_path = str(rel_path).replace("\\", "/")
            zf.write(full_path, arcname=normalized_path)
            count += 1
            total_bytes += full_path.stat().st_size

    duration = time.time() - start_time
    zip_size = OUTPUT_ZIP.stat().st_size
    sha256_hash = compute_sha256(OUTPUT_ZIP)

    print(f"Archive created successfully in {duration:.2f}s:")
    print(f"  Files included:      {count}")
    print(f"  Uncompressed size:   {total_bytes / (1024*1024):.2f} MB")
    print(f"  Compressed size:     {zip_size / (1024*1024):.2f} MB")
    print(f"  SHA-256 Checksum:    {sha256_hash}")

    # Record checksum to external audit files
    audit_txt = PROJECT_ROOT / "audit" / "v6_archive_sha256.txt"
    audit_txt.write_text(f"{sha256_hash}  {ZIP_NAME}\n", encoding="utf-8")
    
    release_txt = PROJECT_ROOT / "FINAL_PASS_RELEASE_MANIFEST.txt"
    release_txt.write_text(
        f"Archive: {ZIP_NAME}\n"
        f"SHA-256: {sha256_hash}\n"
        f"Status:  COMPUTATIONAL RESULTS FROZEN — EXPLORATORY; HUMAN ANNOTATION PENDING\n"
        f"Date:    {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n"
        f"Files:   {count}\n"
        f"Bytes:   {zip_size}\n",
        encoding="utf-8"
    )
    print(f"Recorded release info to {release_txt.name} and {audit_txt.name}")
    return sha256_hash

def clean_room_verification():
    scratch_dir = PROJECT_ROOT / "scratch_extraction_v6"
    print(f"\n--- Clean-Room Extraction Test in {scratch_dir.name} ---")
    if scratch_dir.exists():
        shutil.rmtree(scratch_dir)
    scratch_dir.mkdir(parents=True, exist_ok=True)

    print(f"Extracting {OUTPUT_ZIP.name}...")
    with zipfile.ZipFile(OUTPUT_ZIP, "r") as zf:
        zf.extractall(scratch_dir)

    print("Verifying extracted files against FINAL_PASS/SHA256SUMS.txt...")
    manifest_file = scratch_dir / "FINAL_PASS" / "SHA256SUMS.txt"
    if not manifest_file.exists():
        raise RuntimeError("FINAL_PASS/SHA256SUMS.txt not found in extracted archive!")

    lines = manifest_file.read_text(encoding="utf-8").strip().splitlines()
    checked = 0
    mismatches = 0
    for line in lines:
        if not line.strip():
            continue
        expected_hash, rel_path_str = line.split(None, 1)
        target = scratch_dir / rel_path_str
        if not target.exists():
            print(f"ERROR: Missing file {rel_path_str}")
            mismatches += 1
            continue
        actual_hash = compute_sha256(target)
        if actual_hash != expected_hash:
            print(f"ERROR: Hash mismatch for {rel_path_str}")
            mismatches += 1
        checked += 1

    print(f"Verified {checked} files from manifest. Mismatches: {mismatches}")
    if mismatches > 0:
        raise RuntimeError(f"Clean-room manifest verification FAILED with {mismatches} mismatches!")

    print("\nRunning automated test suite in clean-room extraction environment...")
    python_bin = sys.executable
    cmd = [python_bin, str(scratch_dir / "tests" / "run_all_tests.py")]
    res = subprocess.run(cmd, cwd=str(scratch_dir), capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print(res.stderr)

    if res.returncode != 0:
        raise RuntimeError(f"Test suite FAILED in clean-room extraction (exit code {res.returncode})!")
    print("SUCCESS: All tests passed inside clean-room extraction!")

    # Clean up scratch folder after successful run
    shutil.rmtree(scratch_dir)
    print(f"Cleaned up scratch extraction directory: {scratch_dir.name}")

def main():
    print("=================================================================")
    print("PACKAGING & REPRODUCIBILITY VERIFICATION: MASTER V6 FREEZE")
    print("=================================================================")

    # Step 1: Gather files (excluding manifest initially to ensure fresh generation)
    files = gather_files()
    
    # Step 2: Generate fresh FINAL_PASS/SHA256SUMS.txt
    manifest_path = generate_checksum_manifest(files)
    
    # Step 3: Re-gather files so manifest is included in the package
    files = gather_files()
    assert Path("FINAL_PASS/SHA256SUMS.txt") in files, "Manifest must be included in package"

    # Step 4: Build zip archive
    sha256 = build_zip(files)

    # Step 5: Clean-room extraction verification
    clean_room_verification()

    print("\n=================================================================")
    print("FREEZE PACKAGING COMPLETED AND VERIFIED")
    print(f"Archive: {ZIP_NAME}")
    print(f"SHA-256: {sha256}")
    print("Status:  COMPUTATIONAL RESULTS FROZEN — EXPLORATORY; HUMAN ANNOTATION PENDING")
    print("=================================================================")

if __name__ == "__main__":
    main()
