"""
Submission Validator for Translation Fidelity Annotations.
Enforces non-negotiable data integrity checks without modifying or synthesizing data.
"""
import json
import csv
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any

VALID_FIDELITY_LABELS = {"PRESERVED", "ALTERED", "AMBIGUOUS_SOURCE", "UNABLE_TO_DECIDE"}
VALID_DISTORTION_TYPES = {
    "NUM_DATE", "NEGATION", "ENTITY", "OMISSION", 
    "HALLUCINATION", "QUALIFIER", "TIME", "OTHER", "NONE"
}
FORBIDDEN_COLUMNS = {
    "gold_label", "pred_translated", "pred_original", "risk_score", 
    "entropy", "sampling_stratum", "consensus_label", "adjudication"
}

def validate_submission_file(filepath: Path, expected_packet: str = None) -> Tuple[bool, List[str], Dict[str, Any]]:
    errors = []
    if not filepath.exists():
        return False, [f"File not found: {filepath}"], {}

    records = []
    annotator_code = None
    packet_id = None

    if filepath.suffix.lower() == ".json":
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                return False, ["JSON root must be an object with metadata and 'annotations' array"], {}
            annotator_code = data.get("annotator_code")
            packet_id = data.get("packet_id")
            records = data.get("annotations", [])
        except Exception as e:
            return False, [f"Failed to parse JSON: {e}"], {}
    elif filepath.suffix.lower() == ".csv":
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                header = set(reader.fieldnames or [])
                for forbidden in FORBIDDEN_COLUMNS:
                    if forbidden in header:
                        errors.append(f"Security/Blinding Violation: Forbidden column '{forbidden}' found in CSV header")
                for row in reader:
                    # Convert distortion_types back to list if semicolon separated
                    dt = row.get("distortion_types", "")
                    row["distortion_types"] = [x.strip() for x in dt.split(";") if x.strip()] if isinstance(dt, str) else dt
                    records.append(row)
            if records:
                annotator_code = records[0].get("annotator_code")
                packet_id = records[0].get("packet_id")
        except Exception as e:
            return False, [f"Failed to parse CSV: {e}"], {}
    else:
        return False, [f"Unsupported file format: {filepath.suffix}. Expected .json or .csv"], {}

    if not annotator_code:
        errors.append("Missing annotator_code in submission")
    if not packet_id:
        errors.append("Missing packet_id in submission")
    elif expected_packet and packet_id != expected_packet:
        errors.append(f"Packet mismatch: expected '{expected_packet}', found '{packet_id}'")

    if len(records) != 50:
        errors.append(f"Item count violation: expected exactly 50 items, found {len(records)}")

    seen_ids = set()
    for idx, rec in enumerate(records):
        item_id = rec.get("opaque_item_id")
        if not item_id:
            errors.append(f"Row {idx+1}: Missing opaque_item_id")
            continue
        if item_id in seen_ids:
            errors.append(f"Row {idx+1}: Duplicate opaque_item_id '{item_id}'")
        seen_ids.add(item_id)

        # Check forbidden fields in record
        for k in rec.keys():
            if k in FORBIDDEN_COLUMNS:
                errors.append(f"Row {idx+1} ({item_id}): Blinding violation, contained hidden column '{k}'")

        # Label verification
        label = rec.get("fidelity_label")
        if not label:
            errors.append(f"Row {idx+1} ({item_id}): Missing fidelity_label")
        elif label not in VALID_FIDELITY_LABELS:
            errors.append(f"Row {idx+1} ({item_id}): Invalid fidelity_label '{label}'. Must be one of {sorted(VALID_FIDELITY_LABELS)}")

        # Distortions verification
        distortions = rec.get("distortion_types", [])
        if isinstance(distortions, str):
            distortions = [x.strip() for x in distortions.split(";") if x.strip()]
        
        for d in distortions:
            if d not in VALID_DISTORTION_TYPES:
                errors.append(f"Row {idx+1} ({item_id}): Invalid distortion type '{d}'")

        rationale = rec.get("rationale", "")
        rationale_str = str(rationale).strip() if rationale is not None else ""

        if label == "PRESERVED":
            if "NONE" not in distortions and len(distortions) > 0:
                errors.append(f"Row {idx+1} ({item_id}): PRESERVED label must have distortion_types=['NONE'] or empty, found {distortions}")
        elif label == "ALTERED":
            substantive = [d for d in distortions if d != "NONE"]
            if len(substantive) == 0:
                errors.append(f"Row {idx+1} ({item_id}): ALTERED label requires at least one substantive distortion type")
            if len(rationale_str) < 3:
                errors.append(f"Row {idx+1} ({item_id}): ALTERED label requires a substantive rationale explaining semantic alteration")
        elif label in {"AMBIGUOUS_SOURCE", "UNABLE_TO_DECIDE"}:
            if len(rationale_str) < 3:
                errors.append(f"Row {idx+1} ({item_id}): {label} requires an explanatory rationale")

    is_valid = len(errors) == 0
    metadata = {
        "filepath": str(filepath),
        "annotator_code": annotator_code,
        "packet_id": packet_id,
        "total_items": len(records),
        "valid_items": len(seen_ids),
        "is_valid": is_valid,
        "error_count": len(errors)
    }
    return is_valid, errors, metadata

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_submissions.py <submission_file> [expected_packet]")
        sys.exit(1)

    sub_path = Path(sys.argv[1])
    exp_pkt = sys.argv[2] if len(sys.argv) > 2 else None

    is_valid, errs, meta = validate_submission_file(sub_path, exp_pkt)
    print("=" * 60)
    print(f"Submission Validation Report: {sub_path.name}")
    print(f"Annotator: {meta.get('annotator_code')}")
    print(f"Packet: {meta.get('packet_id')}")
    print(f"Status: {'VALID' if is_valid else 'INVALID'}")
    print("=" * 60)
    if is_valid:
        print("All 50 items passed validation checks with zero integrity errors.")
        sys.exit(0)
    else:
        print(f"Validation failed with {len(errs)} error(s):")
        for e in errs[:20]:
            print(f"  [ERROR] {e}")
        if len(errs) > 20:
            print(f"  ...and {len(errs) - 20} more errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
