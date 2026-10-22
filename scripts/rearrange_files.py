"""
One-time utility to cleanly rearrange historical audit reports and duplicate root files
into audit/historical_reports/ while preserving authoritative canonical files and tests.
"""
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

hist_dir = PROJECT_ROOT / "audit" / "historical_reports"
hist_dir.mkdir(parents=True, exist_ok=True)

files_to_move = [
    "BLOCKER_LEDGER.csv",
    "DECISION_LOG.md",
    "EXPERIMENT_LINEAGE.md",
    "FREEZE_AUDIT.md",
    "FREEZE_GATE_REPORT.md",
    "INDEPENDENT_REVIEW_FREEZE_CANDIDATE_V2.md",
    "MANUSCRIPT_REVIEW_AND_TACL_READINESS.md",
    "README_RESEARCH_FREEZE.md",
    "README_RESEARCH_REPAIR.md",
    "RESEARCH_STATUS.md",
    "REVIEW_ME_FIRST.md",
    "STATUS.md",
    "TACL_READINESS_ASSESSMENT.md",
    "V3_FREEZE_READINESS_REVIEW.md",
    "V3_NEXT_ACTIONS_CHECKLIST.md",
]

for filename in files_to_move:
    src = PROJECT_ROOT / filename
    if src.exists():
        dst = hist_dir / filename
        shutil.move(str(src), str(dst))
        print(f"Moved to audit/historical_reports: {filename}")

duplicate_files_to_remove = [
    "ANNOTATION_HANDOFF.md",
    "FILE_INVENTORY.csv",
    "FREEZE_MANIFEST.md",
    "FROZEN_PROTOCOL.md",
    "ISSUES_AND_FIXES.csv",
    "LIMITATIONS.md",
    "RELATED_WORK_AND_NOVELTY_AUDIT.md",
]

for filename in duplicate_files_to_remove:
    src = PROJECT_ROOT / filename
    if src.exists():
        src.unlink()
        print(f"Removed redundant root duplicate: {filename}")

# Also move legacy reports/ and research/ folders if present into audit/historical_reports/
for dir_name in ["reports", "research"]:
    src_dir = PROJECT_ROOT / dir_name
    if src_dir.exists():
        dst_dir = hist_dir / dir_name
        if dst_dir.exists():
            shutil.rmtree(str(dst_dir))
        shutil.move(str(src_dir), str(dst_dir))
        print(f"Moved directory {dir_name}/ to audit/historical_reports/{dir_name}/")

print("Rearrangement complete.")
