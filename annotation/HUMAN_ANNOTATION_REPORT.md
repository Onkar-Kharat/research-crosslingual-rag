# Bilingual Human Annotation Status and Audit Report

## Status: Gate C BLOCKED (Pending Authentic Human Annotations)

- **Authentic Annotators Completed:** 0 / 2
- **Adjudicator Decisions:** 0 / 50
- **Admissible Agreement / Kappa:** N/A (Awaiting real bilingual annotators)
- **Gate C State:** **BLOCKED**

## Audit Notice: Invalidation of Synthetic Data
Prior versions of this report cited:
- 96.0% raw percentage agreement
- Cohen's Kappa $\kappa = 0.911$
- 70.0% $E_{trans}$ validation rate

**All of the above figures have been formally INVALIDATED as scientific evidence.** An independent code audit revealed that `scripts/perform_bilingual_annotation.py` hard-coded both annotator responses and adjudications within a Python dictionary and simulated the human process.

In accordance with strict scientific integrity rules:
1. The synthetic data, script, and old reports have been quarantined in `audit/invalidated_synthetic_annotations/` with SHA256 checksums for forensic audit history.
2. The active annotation datasets (`annotation/blinded_annotation_sample.csv` and `annotation_handoff/annotation_sample_blinded.csv`) have been stripped of all pre-filled judgments, notes, and rationales, leaving only the blinded stimulus items (Claim, Original Hindi Evidence, MarianMT English Translation).
3. The clean annotator package (`annotation_handoff/ANNOTATOR_PACKET.zip`) is prepared for recruitment of genuine bilingual human evaluators.
4. Gate C State: Under Option C (the adopted observational scope), bilingual human verification is **NOT APPLICABLE / NOT PERFORMED (Future Work)** because all causal claims have been eliminated from the project. For any future causal claims regarding translation error attribution, Gate C remains strictly **Gate C BLOCKED** until authentic native bilingual annotators complete the study with verifiable provenance.
5. Active Human Annotation Workflow: A complete, zero-friction offline annotation interface (`annotation_tool/app/index.html`), blinded handoff packets (`annotation_tool/packets/PACKET_A_HANDOFF.zip` and `PACKET_B_HANDOFF.zip`), and automated validator scripts (`annotation_tool/scripts/validate_submissions.py`) have been constructed for deploying to external bilingual evaluators.
