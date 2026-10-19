import os
import sys
import shutil
import hashlib
import zipfile
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = PROJECT_ROOT / "research_freeze_candidate"
ZIP_NAME = "CROSS_LINGUAL_RAG_RESEARCH_FREEZE_CANDIDATE_V3_NOT_FROZEN.zip"
ZIP_PATH = PROJECT_ROOT / ZIP_NAME
VERIFY_DIR = PROJECT_ROOT / "audit" / "verify_extraction_test"

def sha256_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def assemble_candidate_directory():
    print(f"--- Assembling {CANDIDATE_DIR.name} ---")
    if CANDIDATE_DIR.exists():
        shutil.rmtree(CANDIDATE_DIR)
    CANDIDATE_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Top-level documentation
    top_files = [
        "REVIEW_ME_FIRST.md",
        "RESEARCH_STATUS.md",
        "DECISION_LOG.md",
        "README_RESEARCH_FREEZE.md",
        "requirements.txt"
    ]
    for fn in top_files:
        src = WORKSPACE / fn
        if src.exists():
            shutil.copy2(src, CANDIDATE_DIR / fn)
            print(f"Copied: {fn}")
            
    # 2. Specific directories to copy
    dirs_to_copy = [
        ("audit", ["input_manifest.csv", "PROJECT_INVENTORY.md", "INITIAL_AUDIT_PLAN.md", "environment_report.json", "DATA_AND_LABEL_AUDIT.md", "PAPER_CODE_RECONCILIATION.csv", "RESULTS_REPRODUCTION_REPORT.md"]),
        ("literature", ["SEARCH_PROTOCOL.md", "LITERATURE_AUDIT.csv", "RELATED_WORK_MATRIX.md", "NOVELTY_ASSESSMENT.md"]),
        ("protocol", ["RESEARCH_PROTOCOL_v1.md", "analysis_plan.yaml"]),
        ("annotation", ["ANNOTATION_GUIDE.md", "ANNOTATION_PROTOCOL.md", "blinded_annotation_sample.csv", "internal_audit_sampling_key.csv", "HUMAN_ANNOTATION_REPORT.md"]),
        ("data", ["DATASET_CARD.md", "DATA_PROVENANCE_AND_LICENSES.md", "raw", "processed"]),
        ("experiments", ["experiment_ledger.csv", "results", "results_corrected"]),
        ("results", ["audit_recomputed"]),
        ("figures", ["pdf", "src"]),
        ("scripts", ["phase0_intake.py", "phase1_recompute_all.py", "evaluate_true_jaccard.py", "generate_full_ablations.py", "run_corrected_experiments.py", "create_annotation_sample.py", "analyze_human_annotations.py", "acquire_and_process_data.py", "translate_evidence.py", "generate_publication_figures.py"]),
        ("tests", ["test_data_integrity.py", "test_method_logic.py", "test_metrics_and_partitions.py", "run_all_tests.py", "test_report.json", "TEST_REPORT.md"]),
        ("logs", ["decision_log.md", "preflight_report.json", "run_manifest.json", "source_registry.csv"])
    ]
    
    for dir_name, items in dirs_to_copy:
        dest_dir = CANDIDATE_DIR / dir_name
        dest_dir.mkdir(parents=True, exist_ok=True)
        src_dir = WORKSPACE / dir_name
        
        for item in items:
            src_item = src_dir / item
            dest_item = dest_dir / item
            if src_item.is_dir():
                if dest_item.exists():
                    shutil.rmtree(dest_item)
                shutil.copytree(src_item, dest_item)
            elif src_item.exists():
                shutil.copy2(src_item, dest_item)
        print(f"Copied directory: {dir_name}")

    # Generate MANIFEST_SHA256.txt
    print("\n--- Generating MANIFEST_SHA256.txt ---")
    manifest_rows = []
    for root, _, files in os.walk(CANDIDATE_DIR):
        for f in files:
            fp = Path(root) / f
            rel = fp.relative_to(CANDIDATE_DIR).as_posix()
            h = sha256_file(fp)
            manifest_rows.append(f"{h}  {rel}")
            
    manifest_rows.sort(key=lambda x: x.split("  ")[1])
    manifest_file = CANDIDATE_DIR / "MANIFEST_SHA256.txt"
    manifest_file.write_text("\n".join(manifest_rows) + "\n", encoding="utf-8")
    print(f"Wrote checksums for {len(manifest_rows)} files to {manifest_file}")

def create_freeze_zip():
    print(f"\n--- Creating ZIP Archive: {ZIP_NAME} ---")
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
        
    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(CANDIDATE_DIR):
            for f in files:
                fp = Path(root) / f
                arcname = fp.relative_to(CANDIDATE_DIR).as_posix()
                zf.write(fp, arcname)
                
    stat = ZIP_PATH.stat()
    h = sha256_file(ZIP_PATH)
    print(f"Created ZIP: {ZIP_PATH} ({stat.st_size:,} bytes, SHA256: {h})")
    return stat.st_size, h

def verify_zip_extraction():
    print(f"\n--- Testing Clean Extraction in {VERIFY_DIR} ---")
    if VERIFY_DIR.exists():
        shutil.rmtree(VERIFY_DIR)
    VERIFY_DIR.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
        zf.extractall(VERIFY_DIR)
        
    print(f"Extracted {len(zf.namelist())} files safely to {VERIFY_DIR}")
    
    # Run tests inside extracted directory
    print("Running automated regression test suite on extracted files...")
    python_exe = sys.executable
    test_runner = VERIFY_DIR / "tests" / "run_all_tests.py"
    
    env = dict(os.environ)
    env["PYTHONPATH"] = str(VERIFY_DIR)
    
    res = subprocess.run([python_exe, str(test_runner)], cwd=str(VERIFY_DIR), env=env, capture_output=True, text=True)
    print("Test Runner Output:\n" + res.stdout)
    if res.returncode == 0:
        print("ALL TESTS PASSED ON EXTRACTED ARCHIVE! Verification SUCCESSFUL.")
    else:
        print("TEST RUNNER ERROR:\n" + res.stderr)
        raise RuntimeError("Verification tests failed on extracted package!")

if __name__ == "__main__":
    assemble_candidate_directory()
    size, z_hash = create_freeze_zip()
    verify_zip_extraction()
    print("\nPackage and verification complete!")
