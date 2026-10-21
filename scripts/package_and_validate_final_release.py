"""
Final Research Packaging and Independent Extraction Validation Script.
1. Re-builds full manifest and inventory.
2. Creates CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip.
3. Computes archive SHA-256 hash and writes audit/RELEASE_CHECKSUM.txt.
4. Performs clean-room extraction in scratch directory.
5. Verifies every file against RELEASE_MANIFEST_SHA256.txt.
6. Executes test suite inside clean extracted folder.
7. Generates audit/RELEASE_VALIDATION_REPORT.md.
"""
import os
import sys
import csv
import json
import shutil
import zipfile
import hashlib
import time
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ZIP_NAME = "CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip"
ZIP_PATH = PROJECT_ROOT / ZIP_NAME
CHECKSUM_FILE = PROJECT_ROOT / "audit" / "RELEASE_CHECKSUM.txt"
VALIDATION_REPORT = PROJECT_ROOT / "audit" / "RELEASE_VALIDATION_REPORT.md"
MANIFEST_FILE = PROJECT_ROOT / "audit" / "RELEASE_MANIFEST_SHA256.txt"

EXCLUDE_DIRS = {
    ".venv", ".git", "__pycache__", ".idea", ".vscode", 
    "verify_extraction_test", "extracted_original", "verify_clean_room"
}
EXCLUDE_EXTS = {".pyc", ".pyd", ".pyo"}

def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def package_release():
    print(f"\n--- STEP 1: Packaging {ZIP_NAME} ---")
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()

    file_count = 0
    total_uncompressed_bytes = 0

    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for item in sorted(PROJECT_ROOT.rglob("*")):
            if not item.is_file():
                continue
            rel = item.relative_to(PROJECT_ROOT)
            parts = rel.parts

            if any(part in EXCLUDE_DIRS for part in parts):
                continue
            if item.suffix in EXCLUDE_EXTS:
                continue
            if item.name.endswith(".zip") and item.name != "PACKET_A_HANDOFF.zip" and item.name != "PACKET_B_HANDOFF.zip":
                # Do not package archive zips inside the release zip
                continue
            if item.name in {"RELEASE_CHECKSUM.txt", "ZIP_RELEASE_CHECKSUM.txt", "FINAL_PASS_RELEASE_MANIFEST.txt", "v6_archive_sha256.txt"}:
                # External archive checksums accompanying the release zip
                continue

            zf.write(item, arcname=str(rel))
            file_count += 1
            total_uncompressed_bytes += item.stat().st_size

    archive_size = ZIP_PATH.stat().st_size
    archive_hash = compute_sha256(ZIP_PATH)
    timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

    print(f"Packaged {file_count} files into {ZIP_NAME}")
    print(f"Uncompressed size: {total_uncompressed_bytes / (1024*1024):.2f} MB")
    print(f"Archive size:      {archive_size / (1024*1024):.2f} MB")
    print(f"Archive SHA-256:   {archive_hash}")

    # Write audit/RELEASE_CHECKSUM.txt and FINAL_PASS/ZIP_RELEASE_CHECKSUM.txt
    checksum_content = f"{archive_hash}  {ZIP_NAME}\n"
    with open(CHECKSUM_FILE, "w", encoding="utf-8") as f:
        f.write(checksum_content)
    final_pass_checksum = PROJECT_ROOT / "FINAL_PASS" / "ZIP_RELEASE_CHECKSUM.txt"
    if final_pass_checksum.parent.exists():
        with open(final_pass_checksum, "w", encoding="utf-8") as f:
            f.write(checksum_content)
    print(f"Wrote release checksum to {CHECKSUM_FILE} and {final_pass_checksum}")

    # Write FINAL_PASS_RELEASE_MANIFEST.txt
    release_manifest = PROJECT_ROOT / "FINAL_PASS_RELEASE_MANIFEST.txt"
    release_manifest.write_text(
        f"Archive: {ZIP_NAME}\n"
        f"SHA-256: {archive_hash}\n"
        f"Status:  FROZEN — EXPLORATORY COMPUTATIONAL STUDY\n"
        f"Date:    {timestamp_str}\n"
        f"Files:   {file_count}\n"
        f"Bytes:   {archive_size}\n",
        encoding="utf-8"
    )

    # Sync bitwise copy for v6 name so neither archive is stale
    v6_copy = PROJECT_ROOT / "CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip"
    shutil.copyfile(ZIP_PATH, v6_copy)
    v6_txt = PROJECT_ROOT / "audit" / "v6_archive_sha256.txt"
    v6_txt.write_text(f"{archive_hash}  CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip\n", encoding="utf-8")

    return archive_hash, archive_size, file_count, timestamp_str

def validate_extraction(archive_hash, archive_size, file_count, timestamp_str):
    print(f"\n--- STEP 2: Clean-Room Extraction Validation ---")
    extract_dir = PROJECT_ROOT / "verify_clean_room"
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        zf.extractall(extract_dir)

    print(f"Extracted archive to {extract_dir}")

    # Verify every file against audit/RELEASE_MANIFEST_SHA256.txt
    manifest_lines = [l.strip() for l in open(MANIFEST_FILE, encoding="utf-8") if l.strip()]
    matched = 0
    mismatched = []
    missing = []

    for line in manifest_lines:
        parts = line.split("  ", 1)
        if len(parts) != 2:
            continue
        expected_sha, rel_path = parts
        extracted_file = extract_dir / rel_path
        if not extracted_file.exists():
            missing.append(rel_path)
            continue
        actual_sha = compute_sha256(extracted_file)
        if actual_sha == expected_sha:
            matched += 1
        else:
            mismatched.append((rel_path, expected_sha, actual_sha))

    print(f"Verification Results: {matched} matched, {len(mismatched)} mismatched, {len(missing)} missing.")

    # Confirm that ONLY the manifest itself is intentionally excluded from its own hash list
    extracted_all_files = set()
    for f in extract_dir.rglob("*"):
        if f.is_file():
            extracted_all_files.add(str(f.relative_to(extract_dir)).replace("\\", "/"))
    
    manifest_files = {line.split("  ", 1)[1] for line in manifest_lines if "  " in line}
    unmanifested = extracted_all_files - manifest_files
    print(f"Extracted files not in manifest hash list: {unmanifested}")
    if unmanifested != {"audit/RELEASE_MANIFEST_SHA256.txt"}:
        raise RuntimeError(f"Expected ONLY audit/RELEASE_MANIFEST_SHA256.txt to be unlisted, but found: {unmanifested}")
    print("CONFIRMED: Exactly and only audit/RELEASE_MANIFEST_SHA256.txt is intentionally excluded from its own hash list.")

    # Run tests inside the extracted tree
    print(f"\n--- STEP 3: Executing Test Suite Inside Extracted Clean-Room ---")
    test_runner = extract_dir / "tests" / "run_all_tests.py"
    test_res = subprocess.run(
        [sys.executable, str(test_runner)],
        cwd=str(extract_dir),
        capture_output=True,
        text=True
    )
    test_success = (test_res.returncode == 0)
    print(f"Clean-Room Test Run Exit Code: {test_res.returncode}")
    print(f"Clean-Room Test Output:\n{test_res.stdout[-350:] if test_res.stdout else ''}")

    # Assert clean-room integrity
    if mismatched or missing:
        raise RuntimeError(f"Clean-room extraction validation FAILED: {len(mismatched)} mismatched, {len(missing)} missing.")
    if not test_success:
        raise RuntimeError(f"Clean-room test execution FAILED with exit code {test_res.returncode}.")

    # Cleanup verification directory
    shutil.rmtree(extract_dir)
    print(f"Cleaned up scratch verification directory.")
    print(f"\n=================================================================")
    print(f"RELEASE VALIDATION SUCCESSFUL: 100% HASH PARITY & ALL TESTS PASS")
    print(f"Archive:       {ZIP_NAME}")
    print(f"SHA-256:       {archive_hash}")
    print(f"Files in Zip:  {file_count}")
    print(f"Manifest Match:{matched}/{len(manifest_lines)} files verified")
    print(f"=================================================================\n")

def main():
    # First sync manifests
    import build_full_file_manifest
    build_full_file_manifest.build_manifests()

    # Package
    archive_hash, archive_size, file_count, timestamp_str = package_release()

    # Validate
    validate_extraction(archive_hash, archive_size, file_count, timestamp_str)

if __name__ == "__main__":
    main()
