"""
DEPRECATED AND QUARANTINED SCRIPT.

DO NOT RUN THIS SCRIPT FOR RESEARCH CLAIMS OR EXPERIMENTS.

This script previously generated synthetic 'human' annotations via hardcoded dictionaries,
which violates scientific integrity protocols. It has been moved to:
audit/invalidated_synthetic_annotations/perform_bilingual_annotation.py

Gate C remains strictly BLOCKED until authentic, bilingual human annotators
complete the blinded task according to ANNOTATION_PROTOCOL.md.
"""

import sys

def main():
    raise RuntimeError(
        "CRITICAL RESEARCH INTEGRITY VIOLATION: "
        "perform_bilingual_annotation.py contains hardcoded simulated annotations. "
        "It has been quarantined in audit/invalidated_synthetic_annotations/. "
        "Do not run this script to fabricate human annotation data."
    )

if __name__ == "__main__":
    main()
