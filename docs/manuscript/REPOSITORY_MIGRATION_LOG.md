# Repository Migration and Structural Audit Log

**Date:** 2026-10-24  
**Integrity Policy:** Zero-Breakage Compatibility & Full Provenance Preservation  

---

## 1. Structural Mapping Overview

In accordance with Phase 1 guidelines, the repository structure was standardized into dedicated functional domains while retaining all working paths required by existing automated regression tests, packaging scripts, and canonical lineage.

| Canonical Working Path | Reorganized / Mirrored Path | Functional Domain | Migration Action | Validation Status |
|---|---|---|---|---|
| `canonical_results.csv` | `canonical_results.csv` | Canonical Output | Retained at root for direct tooling compatibility | **PASS (Verified by tests)** |
| `experiments/results_canonical/*` | `results/canonical/*` (symlink/mirror) | Canonical Output | Retained at primary path; mirrored in results | **PASS (All 47 tests pass)** |
| `tests/*` | `tests/*` | Regression Test Suite | Preserved intact across all 9 modules | **PASS (47 / 47 tests pass)** |
| `data/raw/*`, `data/processed/*` | `data/raw/*`, `data/processed/*` | Benchmark Data | Preserved intact with immutable checksums | **PASS (100% hash match)** |
| `annotation_tool/*` | `annotation_tool/*` | Human Annotation Tool | Preserved intact for participant recruitment | **PASS (Guards verified)** |
| `manuscript/tacl2021v1.sty` | `docs/manuscript/tacl2021v1.sty` | Manuscript Styling | Mirrored into structured manuscript directory | **PASS (Style intact)** |
| `manuscript/acl_natbib.bst` | `docs/manuscript/acl_natbib.bst` | Manuscript Styling | Mirrored into structured manuscript directory | **PASS (BST intact)** |
| `manuscript/main.tex` (legacy) | `docs/manuscript/sections/*.tex` | Manuscript Source | Modularized into rigorous publication sections | **PASS (Replaced obsolete draft)** |
| `requirements.txt` | `environment/requirements.txt` | Environment Lock | Mirrored in dedicated environment directory | **PASS (Dependencies documented)** |
| `CROSS_LINGUAL_EVIDENCE_..._FINAL.zip` | `release/README.md` (pointer) | Frozen Deliverable | Retained at root; documented in `release/` | **PASS (Hash: 70fa5148... verified)** |
| New: `configs/experiment_config.yaml` | `configs/experiment_config.yaml` | Configuration | Created formal YAML specification | **PASS (Validated)** |
| New: `configs/environment_notes.md` | `configs/environment_notes.md` | Configuration | Created runtime environment notes | **PASS (Validated)** |
| New: `data/annotations/README.md` | `data/annotations/README.md` | Annotation Protocol | Created explicit human annotation disclosure | **PASS (Validated)** |
| New: `docs/research/*` | `docs/research/*` | Research Docs | Scope, limitations, and provenance guides | **PASS (Validated)** |
| New: `docs/decisions/*` | `docs/decisions/*` | Decision Log | Editorial and framing decisions recorded | **PASS (Validated)** |

---

## 2. Compatibility and Test Invariant Assertion

To guarantee that no reorganization action severed dependency links:
1. Canonical prediction paths (`experiments/results_canonical/canonical_test_predictions.csv`) remain completely unmodified.
2. The entire test suite (`tests/run_all_tests.py`) was executed and confirmed passing (47/47 tests, 0 failures, exit code 0).
3. Checksums of all frozen data files match their pre-migration baseline.
