# Human Annotation Status and Protocol Specification

**Status:** `PENDING EXTERNAL PARTICIPANT RECRUITMENT`  
**Observational Scope:** Option C (Diagnostic Verifier Sensitivity Study)  

---

## 1. Protocol Overview

In this exploratory computational study, bilingual human verification remains pending external human subject recruitment. 

Prior synthetic simulation scripts (`scripts/perform_bilingual_annotation.py`) and simulated human agreement reports have been formally invalidated and quarantined in `audit/invalidated_synthetic_annotations/`. Under no circumstances are automated LLMs or synthetic heuristics represented as genuine human judgments.

## 2. Infrastructure Provided

A complete, validated, offline-capable double-blind human annotation workflow is prepared for subsequent human subject studies:
- Interface & Packet Infrastructure: Located in `annotation_tool/`
- Blinded Stimulus Packets: `annotation_tool/packets/PACKET_A_HANDOFF.zip` and `annotation_tool/packets/PACKET_B_HANDOFF.zip`
- Submission Validator: `annotation_tool/validator.py`
- Test Suite: `tests/test_annotation_integrity.py` and `tests/test_annotation_workflow.py`

## 3. Scientific Guidance for Manuscript

The manuscript strictly refrains from claiming:
1. That human annotation has been completed.
2. That model prediction disagreement causally proves machine translation distortion.
3. That semantic fidelity has been human-adjudicated.

All claims are rigorously framed as empirical model sensitivity and routing disagreement under translation shift.
