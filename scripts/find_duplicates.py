"""
Scans the repository to identify duplicate files by file size and SHA-256 content hash.
"""
import hashlib
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = {".git", ".venv", "__pycache__"}

def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

files_by_size = defaultdict(list)
for p in PROJECT_ROOT.rglob("*"):
    if p.is_file():
        parts = p.relative_to(PROJECT_ROOT).parts
        if any(ex in parts for ex in EXCLUDE_DIRS):
            continue
        files_by_size[p.stat().st_size].append(p)

duplicate_groups = []
for size, path_list in files_by_size.items():
    if len(path_list) > 1 and size > 0:
        hashes = defaultdict(list)
        for p in path_list:
            h = get_file_hash(p)
            hashes[h].append(p)
        for h, dups in hashes.items():
            if len(dups) > 1:
                duplicate_groups.append((size, h, dups))

print(f"Total duplicate content groups found: {len(duplicate_groups)}")
for size, h, dups in sorted(duplicate_groups, key=lambda x: -x[0]):
    rel_paths = [str(p.relative_to(PROJECT_ROOT)) for p in dups]
    print(f"\nSize: {size:,} bytes | Hash: {h[:12]}...")
    for rp in rel_paths:
        print(f"  - {rp}")
