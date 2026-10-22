"""
Clean up confirmed redundant directories and bitwise identical ZIP duplicate:
1. audit/verify_extraction_test (temporary clean-room extraction test dir)
2. audit/extracted_original (temporary clean-room extraction test dir)
3. CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip
   (exact duplicate of CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip)
4. manuscript/ (exact duplicate mirror of docs/manuscript/)
"""
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 1. Remove duplicate extraction directories in audit/
for dir_name in ["verify_extraction_test", "extracted_original"]:
    target = PROJECT_ROOT / "audit" / dir_name
    if target.exists():
        shutil.rmtree(target)
        print(f"Removed temporary extraction dir: audit/{dir_name}")

# 2. Remove duplicate v6.zip (keep authoritative FREEZE_FINAL.zip)
v6_zip = PROJECT_ROOT / "CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip"
if v6_zip.exists():
    v6_zip.unlink()
    print("Removed duplicate v6 archive (kept CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip)")

# 3. Remove duplicate root manuscript/ folder (docs/manuscript/ is the canonical TACL draft)
manuscript_dir = PROJECT_ROOT / "manuscript"
if manuscript_dir.exists():
    shutil.rmtree(manuscript_dir)
    print("Removed duplicate root manuscript/ directory (docs/manuscript/ is canonical)")

print("Duplicate cleanup complete.")
