"""
Package Candidate V4 (NOT_FROZEN) with Complete Provenance and Integrity Manifest.
Enforces clean-room extraction test in an isolated scratch directory.
"""
import os
import sys
import zipfile
import hashlib
import tempfile
import subprocess
import pandas as pd
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
ZIP_NAME = "CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_V4_NOT_FROZEN.zip"
ZIP_PATH = WORKSPACE / ZIP_NAME

EXCLUDE_DIRS = {
    ".git", ".venv", "__pycache__", ".pytest_cache", ".idea", ".vscode",
    "research_freeze_candidate", "verify_extraction_test", "scratch",
    "extracted_original", ".system_generated"
}
EXCLUDE_EXTS = {".pyc", ".pyo", ".pyd", ".tmp", ".log"}
EXCLUDE_FILES = {
    ZIP_NAME,
    "CROSS_LINGUAL_RAG_RESEARCH_FREEZE_CANDIDATE_NOT_FROZEN.zip",
    "CROSS_LINGUAL_RAG_RESEARCH_FREEZE_CANDIDATE_V3_NOT_FROZEN.zip",
    "CROSS_LINGUAL_RAG_RESEARCH_FREEZE_CANDIDATE_V3_FROZEN.zip",
    "research-crosslingual-rag-main_AUDIT_FIRST.zip"
}

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def package_candidate():
    print(f"=== PACKAGING {ZIP_NAME} ===")
    manifest_rows = []

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(WORKSPACE):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]

            for file in files:
                if file in EXCLUDE_FILES or any(file.endswith(ext) for ext in EXCLUDE_EXTS):
                    continue
                if file.startswith(".tempmedia") or file.endswith(".png_tmp"):
                    continue

                full_path = Path(root) / file
                rel_path = full_path.relative_to(WORKSPACE)

                # Exclude any zip file at the root or within audit (except ANNOTATOR_PACKET.zip)
                if rel_path.suffix == ".zip" and rel_path.name != "ANNOTATOR_PACKET.zip":
                    continue
                if "verify_extraction_test" in rel_path.parts:
                    continue

                zf.write(full_path, arcname=str(rel_path).replace("\\", "/"))
                f_hash = sha256_file(full_path)
                f_size = full_path.stat().st_size
                manifest_rows.append({
                    "relative_path": str(rel_path).replace("\\", "/"),
                    "size_bytes": f_size,
                    "sha256": f_hash
                })

    manifest_df = pd.DataFrame(manifest_rows)
    manifest_df.to_csv(WORKSPACE / "audit_v4" / "v4_archive_manifest.csv", index=False)

    zip_hash = sha256_file(ZIP_PATH)
    zip_size = ZIP_PATH.stat().st_size
    print(f"Packaged {len(manifest_rows)} files into {ZIP_NAME}")
    print(f"Archive Size: {zip_size / (1024*1024):.2f} MB")
    print(f"Archive SHA256: {zip_hash}")

    with open(WORKSPACE / "audit_v4" / "v4_archive_sha256.txt", "w", encoding="utf-8") as f:
        f.write(f"{zip_hash}  {ZIP_NAME}\n")

    return ZIP_PATH

def verify_clean_room_extraction():
    print("\n=== RUNNING CLEAN-ROOM EXTRACTION VERIFICATION ===")
    with tempfile.TemporaryDirectory(prefix="clean_test_v4_") as tmp_dir:
        tmp_path = Path(tmp_dir)
        print(f"Extracting to isolated scratch directory: {tmp_path}")
        with zipfile.ZipFile(ZIP_PATH, "r") as zf:
            zf.extractall(tmp_path)

        print("Verifying test suite execution in extracted directory...")
        res = subprocess.run(
            [sys.executable, "tests/run_all_tests.py"],
            cwd=str(tmp_path),
            capture_output=True,
            text=True
        )
        print(res.stdout)
        if res.stderr:
            print("STDERR:", res.stderr)

        if res.returncode == 0:
            print("[VERIFICATION SUCCESS] Clean-room extraction test PASSED!")
            return True
        else:
            print(f"[VERIFICATION FAILURE] Test suite returned exit code {res.returncode}")
            return False

if __name__ == "__main__":
    package_candidate()
    verify_clean_room_extraction()
