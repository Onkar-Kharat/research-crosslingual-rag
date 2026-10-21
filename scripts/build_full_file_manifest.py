"""
Recursively scans all active release files, computes SHA-256 hashes,
and generates:
1. audit/FILE_INVENTORY.csv
2. REVIEWER_HANDOFF/FINAL_FILE_MANIFEST.csv
3. audit/RELEASE_MANIFEST_SHA256.txt
Excludes local environment (.venv), git metadata, pycache, temporary extraction tests, and release zip itself.
"""
import hashlib
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = {
    ".venv", ".git", "__pycache__", ".idea", ".vscode", 
    "verify_extraction_test", "extracted_original", "verify_clean_room"
}
EXCLUDE_EXTS = {".pyc", ".pyd", ".pyo"}
EXCLUDE_REL_PATHS = {
    "CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip",
    "CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip",
    "audit/RELEASE_MANIFEST_SHA256.txt",
    "audit/RELEASE_CHECKSUM.txt",
    "FINAL_PASS/ZIP_RELEASE_CHECKSUM.txt",
    "FINAL_PASS_RELEASE_MANIFEST.txt",
    "audit/v6_archive_sha256.txt",
    "audit/FILE_INVENTORY.csv",
    "REVIEWER_HANDOFF/FINAL_FILE_MANIFEST.csv",
}

def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def classify_file(rel_path: str) -> str:
    p = rel_path.replace("\\", "/")
    if p.startswith("experiments/results_canonical/"):
        return "Authoritative_Canonical_Output"
    elif p.startswith("data/raw/") or p.startswith("data/processed/"):
        return "Data_Provenance_Split"
    elif p.startswith("protocol/"):
        return "Frozen_Protocol_Specification"
    elif p.startswith("tests/"):
        return "Automated_Regression_Test"
    elif p.startswith("annotation_tool/"):
        return "Annotation_Tool_Infrastructure"
    elif p.startswith("audit/"):
        return "Forensic_Audit_Report"
    elif p.startswith("literature/"):
        return "Literature_Audit"
    elif p.startswith("figures/"):
        return "Publication_Figure"
    elif p.startswith("scripts/"):
        return "Execution_Script"
    elif p.startswith("REVIEWER_HANDOFF/"):
        return "Reviewer_Handoff_Document"
    elif p.startswith("experiments/results_corrected/") or p.startswith("experiments/results/"):
        return "Historical_Superseded_Artifact"
    elif p.startswith("FINAL_PASS/"):
        return "Navigation_Pointer"
    else:
        return "General_Project_File"

def build_manifests():
    print("Scanning repository files recursively...")
    records = []
    manifest_lines = []

    for item in sorted(PROJECT_ROOT.rglob("*")):
        if not item.is_file():
            continue
        rel = item.relative_to(PROJECT_ROOT)
        parts = rel.parts

        # Check exclusion directories
        if any(part in EXCLUDE_DIRS for part in parts):
            continue
        if item.suffix in EXCLUDE_EXTS:
            continue
        rel_str = str(rel).replace("\\", "/")
        if rel_str in EXCLUDE_REL_PATHS:
            continue
        if item.name.endswith(".zip") and item.name != "PACKET_A_HANDOFF.zip" and item.name != "PACKET_B_HANDOFF.zip":
            continue
        file_size = item.stat().st_size
        sha = compute_sha256(item)
        category = classify_file(rel_str)

        records.append({
            "Path": rel_str,
            "Size_Bytes": file_size,
            "SHA256": sha,
            "Category": category
        })
        manifest_lines.append(f"{sha}  {rel_str}")

    # 1. Write audit/FILE_INVENTORY.csv
    inv_path = PROJECT_ROOT / "audit" / "FILE_INVENTORY.csv"
    with open(inv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Path", "Size_Bytes", "SHA256", "Category"])
        writer.writeheader()
        writer.writerows(records)

    # 2. Write REVIEWER_HANDOFF/FINAL_FILE_MANIFEST.csv
    handoff_manifest = PROJECT_ROOT / "REVIEWER_HANDOFF" / "FINAL_FILE_MANIFEST.csv"
    with open(handoff_manifest, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Path", "Size_Bytes", "SHA256", "Category"])
        writer.writeheader()
        writer.writerows(records)

    # Compute actual hashes of newly written inventory files and append to manifest
    for extra_file, rel_name, cat in [
        (inv_path, "audit/FILE_INVENTORY.csv", "Forensic_Audit_Report"),
        (handoff_manifest, "REVIEWER_HANDOFF/FINAL_FILE_MANIFEST.csv", "Reviewer_Handoff_Document")
    ]:
        extra_sha = compute_sha256(extra_file)
        manifest_lines.append(f"{extra_sha}  {rel_name}")
        records.append({
            "Path": rel_name,
            "Size_Bytes": extra_file.stat().st_size,
            "SHA256": extra_sha,
            "Category": cat
        })

    # Sort manifest lines alphabetically by path
    manifest_lines.sort(key=lambda l: l.split("  ", 1)[1])

    # 3. Write audit/RELEASE_MANIFEST_SHA256.txt
    release_txt = PROJECT_ROOT / "audit" / "RELEASE_MANIFEST_SHA256.txt"
    with open(release_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(manifest_lines) + "\n")

    print(f"Total release files inventoried and manifested: {len(manifest_lines)}")
    print(f"Wrote {inv_path}")
    print(f"Wrote {handoff_manifest}")
    print(f"Wrote {release_txt}")

if __name__ == "__main__":
    build_manifests()
