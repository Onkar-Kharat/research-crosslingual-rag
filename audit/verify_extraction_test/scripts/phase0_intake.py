import os
import sys
import hashlib
import zipfile
import json
import csv
import time
import platform
import shutil
from pathlib import Path

WORKSPACE = Path(r"c:\Users\Onkar\OneDrive\Desktop\Research_crosslingual_rag_research")
AUDIT_DIR = WORKSPACE / "audit"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

def sha256_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def phase0_manifest():
    print("--- Phase 0.1: Calculating Input Manifest ---")
    files_to_check = [
        WORKSPACE / "research-crosslingual-rag-main_AUDIT_FIRST.zip",
        WORKSPACE / "ANTIGRAVITY_AUDIT_AND_RECOVERY_PROMPT.md",
        WORKSPACE / "MANUSCRIPT_REVIEW_AND_TACL_READINESS.md",
        WORKSPACE / "ANTIGRAVITY_RESEARCH_IMPROVEMENT_AND_FREEZE_PROMPT.md",
        WORKSPACE / "ANTIGRAVITY_MASTER_PROMPT.md",
        WORKSPACE / "manuscript" / "main.pdf",
        WORKSPACE / "manuscript" / "main.tex"
    ]
    
    manifest_rows = []
    for fp in files_to_check:
        if fp.exists():
            stat = fp.stat()
            h = sha256_file(fp)
            manifest_rows.append({
                "filename": fp.name,
                "relative_path": fp.relative_to(WORKSPACE).as_posix(),
                "size_bytes": stat.st_size,
                "mtime_iso": time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(stat.st_mtime)),
                "sha256": h
            })
            print(f"Found: {fp.name} ({stat.st_size} bytes, SHA256: {h[:12]}...)")
        else:
            print(f"MISSING: {fp.name}")

    manifest_csv = AUDIT_DIR / "input_manifest.csv"
    with open(manifest_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "relative_path", "size_bytes", "mtime_iso", "sha256"])
        writer.writeheader()
        writer.writerows(manifest_rows)
    print(f"Wrote input manifest to {manifest_csv}")

def phase0_zip_inspect_and_extract():
    print("\n--- Phase 0.2: Inspecting and Extracting Archive ---")
    zip_path = WORKSPACE / "research-crosslingual-rag-main_AUDIT_FIRST.zip"
    if not zip_path.exists():
        print(f"Error: {zip_path} does not exist.")
        return

    extract_dest = AUDIT_DIR / "extracted_original"
    extract_dest.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        infolist = zf.infolist()
        print(f"Zip contains {len(infolist)} entries.")
        # Check for path traversal or absolute paths
        unsafe_entries = []
        for info in infolist:
            filename = info.filename
            if filename.startswith("/") or filename.startswith("\\") or ".." in filename:
                unsafe_entries.append(filename)
        
        if unsafe_entries:
            raise ValueError(f"UNSAFE ZIP ENTRIES DETECTED: {unsafe_entries}")
        print("Archive safety check: PASSED (no path traversal, no absolute paths).")
        
        zf.extractall(extract_dest)
        print(f"Extracted archive safely to {extract_dest}")

def phase0_environment():
    print("\n--- Phase 0.3: Detecting Environment ---")
    import torch
    import transformers
    
    # Disk space
    total, used, free = shutil.disk_usage(WORKSPACE)
    
    # Packages
    try:
        import importlib.metadata as im
        installed_packages = {dist.metadata["Name"]: dist.version for dist in im.distributions()}
    except Exception as e:
        installed_packages = {"error": str(e)}

    # HF cache
    hf_cache = os.environ.get("HF_HOME", os.path.expanduser("~/.cache/huggingface"))
    
    env_info = {
        "os": platform.platform(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "cpu_count": os.cpu_count(),
        "ram_disk": {
            "total_gb": round(total / (1024**3), 2),
            "free_gb": round(free / (1024**3), 2),
            "used_gb": round(used / (1024**3), 2)
        },
        "torch": {
            "version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "cuda_device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
            "device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
        },
        "transformers": {
            "version": transformers.__version__
        },
        "hf_cache_dir": hf_cache,
        "key_dependencies": {
            k: installed_packages.get(k, "NOT_INSTALLED")
            for k in ["torch", "transformers", "scikit-learn", "scipy", "numpy", "pandas", "statsmodels", "matplotlib", "seaborn", "nltk", "sacrebleu"]
        }
    }
    
    env_file = AUDIT_DIR / "environment_report.json"
    with open(env_file, "w", encoding="utf-8") as f:
        json.dump(env_info, f, indent=2)
    print(f"Wrote environment report to {env_file}")
    print(f"Environment Summary: {env_info['os']} | Python {platform.python_version()} | Torch {torch.__version__} (CUDA: {torch.cuda.is_available()}) | Free Disk: {env_info['ram_disk']['free_gb']} GB")

def phase0_inventory():
    print("\n--- Phase 0.4: Generating Project Inventory ---")
    categories = {
        "source_code": [".py", ".sh", ".ps1"],
        "configuration": [".yaml", ".yml", ".json", ".ini", ".toml"],
        "data": [".tsv", ".jsonl", ".csv"],
        "documentation_reports": [".md", ".txt"],
        "manuscript": [".tex", ".bib", ".sty", ".bst"],
        "figures": [".png", ".pdf", ".svg"],
        "binary_archives": [".zip", ".tar", ".gz"]
    }
    
    file_records = []
    for root, dirs, files in os.walk(WORKSPACE):
        # Exclude .git, .venv, audit/extracted_original
        rel_root = Path(root).relative_to(WORKSPACE)
        parts = rel_root.parts
        if len(parts) > 0 and (parts[0] in [".git", ".venv"] or (len(parts) > 1 and parts[0] == "audit" and parts[1] == "extracted_original")):
            continue
        for f in files:
            fp = Path(root) / f
            rel_fp = fp.relative_to(WORKSPACE).as_posix()
            ext = fp.suffix.lower()
            size = fp.stat().st_size
            
            category = "other"
            for cat, exts in categories.items():
                if ext in exts:
                    category = cat
                    break
            
            file_records.append({
                "path": rel_fp,
                "category": category,
                "size_bytes": size,
                "extension": ext
            })
            
    inventory_md = AUDIT_DIR / "PROJECT_INVENTORY.md"
    with open(inventory_md, "w", encoding="utf-8") as f:
        f.write("# Project Inventory\n\n")
        f.write(f"Total tracked files inventoried: {len(file_records)}\n\n")
        
        # Summary table by category
        cat_counts = {}
        for r in file_records:
            cat_counts[r["category"]] = cat_counts.get(r["category"], 0) + 1
        
        f.write("## File Count by Category\n\n")
        f.write("| Category | Count |\n|---|---|\n")
        for cat, cnt in sorted(cat_counts.items()):
            f.write(f"| {cat} | {cnt} |\n")
        f.write("\n## Detailed Inventory\n\n")
        f.write("| Relative Path | Category | Size (bytes) |\n|---|---|---|\n")
        for r in sorted(file_records, key=lambda x: x["path"]):
            f.write(f"| `{r['path']}` | {r['category']} | {r['size_bytes']} |\n")
            
    print(f"Wrote project inventory to {inventory_md}")

if __name__ == "__main__":
    phase0_manifest()
    phase0_zip_inspect_and_extract()
    phase0_environment()
    phase0_inventory()
    print("\nPhase 0 Complete!")
