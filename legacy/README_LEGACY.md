# LEGACY AND EXPLORATORY ARTIFACTS

**STATUS: LEGACY_EXPLORATORY_NOT_CONFIRMATORY**

The files in this directory represent the pre-critical-repair predictions and tables.
These artifacts:
1. Used character slicing `[:512]` instead of BPE token truncation.
2. Evaluated an unvalidated mapping of `partly true/misleading` -> `INSUFFICIENT_EVIDENCE`.
3. Lacked confirmatory separation from exploratory development.
4. Derived ablation latencies using an estimated constant rather than per-instance measurements.

These files are preserved for forensic provenance and must NOT be used for confirmatory claims.
