# Bilingual Annotator Completion Checklist

Before submitting your completed evaluation file, please verify the following:

- [ ] **Independent Completion:** You completed all judgments independently without consulting the other annotator.
- [ ] **All 50 Items Completed:** Every item from 1 to 50 has an assigned `fidelity_label`.
- [ ] **Label Rules Respected:**
  - If marked `PRESERVED`: Distortion type `NONE` is selected.
  - If marked `ALTERED`: At least one substantive distortion type (e.g., `NUM_DATE`, `NEGATION`, `ENTITY`, `OMISSION`, `HALLUCINATION`, `QUALIFIER`, `TIME`, `OTHER`) is checked, and a concise rationale pointing to the semantic difference is provided.
  - If marked `AMBIGUOUS_SOURCE` or `UNABLE_TO_DECIDE`: A brief explanatory rationale is provided.
- [ ] **Zero Truth Bias:** Your judgments assess *translation fidelity* between Hindi source and English target, NOT whether the underlying claim is factually true in the real world.
- [ ] **File Exported:** Clicked "Validate & Export Submission" and downloaded `submission_{annotator_code}_{packet_id}.json` (or `.csv`).
- [ ] **Returned:** Sent the unmodified submission file back to the research coordinator.
