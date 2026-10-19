"""
Phase 0 V2 Intake Script: Portable audit, archive hashing, and legacy quarantine.
Ensures zero hardcoded paths by resolving PROJECT_ROOT relative to __file__.
"""
import os
import sys
import hashlib
import zipfile
import csv
import shutil
from pathlib import Path

# Resolve project root dynamically
PROJECT_ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = PROJECT_ROOT / "audit"
LEGACY_DIR = PROJECT_ROOT / "legacy"
LOGS_DIR = PROJECT_ROOT / "logs"

AUDIT_DIR.mkdir(parents=True, exist_ok=True)
LEGACY_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

def sha256_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def inspect_v2_archive():
    zip_path = PROJECT_ROOT / "CROSS_LINGUAL_RAG_RESEARCH_FREEZE_CANDIDATE_NOT_FROZEN.zip"
    if not zip_path.exists():
        print(f"Error: {zip_path} not found.")
        return
        
    print(f"Inspecting archive: {zip_path.name} ({zip_path.stat().st_size:,} bytes)")
    manifest_rows = []
    
    with zipfile.ZipFile(zip_path, "r") as zf:
        infolist = zf.infolist()
        print(f"Archive contains {len(infolist)} member entries.")
        for info in infolist:
            if info.is_dir():
                continue
            data = zf.read(info.filename)
            h = sha256_bytes(data)
            manifest_rows.append({
                "archive_member": info.filename,
                "file_size_bytes": info.file_size,
                "compress_size_bytes": info.compress_size,
                "sha256": h
            })
            
    manifest_csv = AUDIT_DIR / "v2_archive_manifest.csv"
    with open(manifest_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["archive_member", "file_size_bytes", "compress_size_bytes", "sha256"])
        writer.writeheader()
        writer.writerows(manifest_rows)
    print(f"Wrote archive member manifest ({len(manifest_rows)} files) to {manifest_csv}")

def quarantine_legacy_artifacts():
    print("\n--- Quarantining Legacy / Exploratory Predictions ---")
    legacy_files = [
        PROJECT_ROOT / "experiments" / "results" / "test_predictions.csv",
        PROJECT_ROOT / "experiments" / "results" / "dev_predictions.csv",
        PROJECT_ROOT / "experiments" / "results" / "test_main_results.csv",
        PROJECT_ROOT / "experiments" / "results" / "test_statistical_tests.csv",
        PROJECT_ROOT / "experiments" / "results" / "test_error_attribution.csv",
        PROJECT_ROOT / "experiments" / "results_corrected" / "full_benchmark_and_ablations.csv"
    ]
    
    for f in legacy_files:
        if f.exists():
            dest = LEGACY_DIR / f.name
            shutil.copy2(f, dest)
            print(f"Quarantined to legacy/: {f.name}")
            
    readme_legacy = LEGACY_DIR / "README_LEGACY.md"
    readme_legacy.write_text(
        "# LEGACY AND EXPLORATORY ARTIFACTS\n\n"
        "**STATUS: LEGACY_EXPLORATORY_NOT_CONFIRMATORY**\n\n"
        "The files in this directory represent the pre-critical-repair predictions and tables.\n"
        "These artifacts:\n"
        "1. Used character slicing `[:512]` instead of BPE token truncation.\n"
        "2. Evaluated an unvalidated mapping of `partly true/misleading` -> `INSUFFICIENT_EVIDENCE`.\n"
        "3. Lacked confirmatory separation from exploratory development.\n"
        "4. Derived ablation latencies using an estimated constant rather than per-instance measurements.\n\n"
        "These files are preserved for forensic provenance and must NOT be used for confirmatory claims.\n",
        encoding="utf-8"
    )
    print(f"Wrote {readme_legacy}")

def create_blocker_ledger():
    print("\n--- Creating Blockers Ledger ---")
    blockers = [
        {
            "Issue_ID": "ISSUE-P0-1",
            "Severity": "P0",
            "Category": "Task & Label Validity",
            "Description": "partly true/misleading mapped to INSUFFICIENT_EVIDENCE without grounding; 0 SUPPORTED claims in gold.",
            "Evidence_Path": "audit/DATA_AND_LABEL_AUDIT.md",
            "Fix_Required": "Evaluate native X-Fact veracity vs NLI formulations in TASK_AND_LABEL_VALIDITY_DECISION.md; scope to observed classes.",
            "Owner": "Agent",
            "Gate": "Gate A",
            "Status": "OPEN"
        },
        {
            "Issue_ID": "ISSUE-P0-2",
            "Severity": "P0",
            "Category": "Corrected Inference Rerun",
            "Description": "full_benchmark_and_ablations.csv was post-hoc recomputed on old predictions; corrected prediction CSVs missing.",
            "Evidence_Path": "experiments/results_corrected/full_benchmark_and_ablations.csv",
            "Fix_Required": "Rerun corrected token-truncated inference from scratch on dev and eval splits; save canonical per-example outputs.",
            "Owner": "Agent",
            "Gate": "Gate D",
            "Status": "OPEN"
        },
        {
            "Issue_ID": "ISSUE-P0-3",
            "Severity": "P0",
            "Category": "Portability & Hardcoded Paths",
            "Description": "Scripts and tests hardcode 'C:\\Users\\Onkar\\...'; tests fail upon extraction to clean directory.",
            "Evidence_Path": "tests/run_all_tests.py:6",
            "Fix_Required": "Refactor all scripts to use Path(__file__).resolve().parents[1]; verify clean extraction tests pass.",
            "Owner": "Agent",
            "Gate": "Gate E",
            "Status": "OPEN"
        },
        {
            "Issue_ID": "ISSUE-P0-4",
            "Severity": "P0",
            "Category": "Evaluation Split Exposure",
            "Description": "163-item test split was previously evaluated and inspected; cannot be claimed as virgin confirmatory test.",
            "Evidence_Path": "audit/DATA_AND_LABEL_AUDIT.md:Sec 4",
            "Fix_Required": "Inspect official X-Fact OOD/zero-shot data for Hindi claims; pre-register evaluation design and disclose history.",
            "Owner": "Agent",
            "Gate": "Gate D",
            "Status": "OPEN"
        },
        {
            "Issue_ID": "ISSUE-P1-1",
            "Severity": "P1",
            "Category": "Literature Audit Rigor",
            "Description": "Placeholder 'arXiv:2407.xxxxx' in LITERATURE_AUDIT.csv; omitted XFEVER (Chang et al. 2023); unvetted 'first' claims.",
            "Evidence_Path": "literature/LITERATURE_AUDIT.csv:row P05",
            "Fix_Required": "Verify exact IDs for all 12+ papers; add XFEVER; remove 'first' claims and bound contributions.",
            "Owner": "Agent",
            "Gate": "Gate B",
            "Status": "OPEN"
        },
        {
            "Issue_ID": "ISSUE-P1-2",
            "Severity": "P1",
            "Category": "Latency Measurement",
            "Description": "Fixed constant 1120 ms used for MT latency; mix of model-only and E2E latencies without per-instance measurement.",
            "Evidence_Path": "scripts/generate_full_ablations.py:10",
            "Fix_Required": "Measure per-instance MT generation and verifier forward passes; report mean, median, std, and p95.",
            "Owner": "Agent",
            "Gate": "Gate D",
            "Status": "OPEN"
        },
        {
            "Issue_ID": "ISSUE-P1-3",
            "Severity": "P1",
            "Category": "Human Annotation & Packet Hygiene",
            "Description": "0/50 annotations complete; internal sampling key was co-located with annotation files.",
            "Evidence_Path": "annotation/internal_audit_sampling_key.csv",
            "Fix_Required": "Create isolated ANNOTATOR_PACKET.zip containing only blinded CSV, guide, protocol; keep key private; Gate C remains BLOCKED.",
            "Owner": "Human / Agent",
            "Gate": "Gate C",
            "Status": "BLOCKED (Awaiting Human)"
        },
        {
            "Issue_ID": "ISSUE-P1-4",
            "Severity": "P1",
            "Category": "Protocol Inconsistencies",
            "Description": "Threshold grid in analysis_plan.yaml ([0.10, 0.65]) differed from script ([0.15, 0.65]); permutation p-value mismatch (0.037 vs 0.042).",
            "Evidence_Path": "protocol/analysis_plan.yaml:26",
            "Fix_Required": "Reconcile YAML protocol, code, seeds, permutation count, and reported statistics from single canonical run.",
            "Owner": "Agent",
            "Gate": "Gate D",
            "Status": "OPEN"
        },
        {
            "Issue_ID": "ISSUE-P1-5",
            "Severity": "P1",
            "Category": "Licensing & Local Path Hygiene",
            "Description": "Broad 'Fair Use' claim in license report; environment report confused disk capacity with RAM.",
            "Evidence_Path": "data/DATA_PROVENANCE_AND_LICENSES.md",
            "Fix_Required": "Create DATA_USE_AND_LICENSE_NOTES.md; separate code, model, and dataset terms; fix RAM/disk reporting with psutil.",
            "Owner": "Agent",
            "Gate": "Gate A / E",
            "Status": "OPEN"
        }
    ]
    
    ledger_csv = PROJECT_ROOT / "BLOCKER_LEDGER.csv"
    with open(ledger_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Issue_ID", "Severity", "Category", "Description", "Evidence_Path", "Fix_Required", "Owner", "Gate", "Status"])
        writer.writeheader()
        writer.writerows(blockers)
    print(f"Wrote blocker ledger ({len(blockers)} tracked issues) to {ledger_csv}")

if __name__ == "__main__":
    inspect_v2_archive()
    quarantine_legacy_artifacts()
    create_blocker_ledger()
    print("Phase 0 V2 Intake Complete!")
