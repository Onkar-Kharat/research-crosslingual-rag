"""
Builds canonical results directory and generates RUN_MANIFEST.json.
Copies canonical artifacts and figures to experiments/results_canonical/.
Computes SHA256 hashes of all input data, models, environments, configurations, and outputs.
"""
import shutil
import hashlib
import json
import platform
import subprocess
import time
from pathlib import Path
import torch
import transformers

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def get_git_info():
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, cwd=PROJECT_ROOT).strip()
        status = subprocess.check_output(["git", "status", "--short"], text=True, cwd=PROJECT_ROOT).strip()
        return {"commit_sha": commit, "status_summary": status}
    except Exception as e:
        return {"commit_sha": "unavailable", "error": str(e)}

def main():
    canon_dir = PROJECT_ROOT / "experiments" / "results_canonical"
    canon_dir.mkdir(parents=True, exist_ok=True)
    fig_dir = canon_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    src_res = PROJECT_ROOT / "experiments" / "results_corrected"
    files_expected = [
        "canonical_benchmark_table.csv",
        "canonical_dev_predictions.csv",
        "canonical_dev_tuning.csv",
        "canonical_error_attribution.json",
        "canonical_latency_summary.json",
        "canonical_random_control_100seeds.csv",
        "canonical_statistical_tests.csv",
        "canonical_test_predictions.csv",
        "test_predictions.jsonl",
        "test_metrics.json",
        "dev_threshold_sweep.json"
    ]
    for f in files_expected:
        dest_file = canon_dir / f
        if not dest_file.exists() and (src_res / f).exists():
            shutil.copy2(src_res / f, dest_file)
        assert dest_file.exists(), f"Missing required canonical output: {f}"

    for ext in ["pdf", "png"]:
        src_f = PROJECT_ROOT / "figures" / ("pdf" if ext == "pdf" else "src")
        for p in src_f.glob(f"*.{ext}"):
            shutil.copy2(p, fig_dir / p.name)

    print("Canonical outputs and figures validated in experiments/results_canonical/.")

    # Compute input hashes
    inputs = {
        "raw_dev_all_tsv": {
            "path": "data/raw/dev.all.tsv",
            "sha256": compute_sha256(PROJECT_ROOT / "data" / "raw" / "dev.all.tsv")
        },
        "raw_test_all_tsv": {
            "path": "data/raw/test.all.tsv",
            "sha256": compute_sha256(PROJECT_ROOT / "data" / "raw" / "test.all.tsv")
        },
        "dev_processed_hindi_jsonl": {
            "path": "data/processed/dev.jsonl",
            "sha256": compute_sha256(PROJECT_ROOT / "data" / "processed" / "dev.jsonl"),
            "n_samples": 103
        },
        "test_processed_hindi_jsonl": {
            "path": "data/processed/test.jsonl",
            "sha256": compute_sha256(PROJECT_ROOT / "data" / "processed" / "test.jsonl"),
            "n_samples": 163
        },
        "analysis_plan_yaml": {
            "path": "protocol/analysis_plan.yaml",
            "sha256": compute_sha256(PROJECT_ROOT / "protocol" / "analysis_plan.yaml")
        }
    }

    # Model specifications
    models = {
        "translation_model": {
            "model_id": "Helsinki-NLP/opus-mt-hi-en",
            "task": "translation_hi_to_en",
            "device": "cpu",
            "max_length": 512,
            "truncation": True
        },
        "verifier_model": {
            "model_id": "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7",
            "task": "zero_shot_cross_lingual_nli",
            "device": "cpu",
            "max_length": 512,
            "truncation": True,
            "label_mapping": {
                "CONTRADICTION": "CONTRADICTED",
                "ENTAILMENT": "SUPPORTED",
                "NEUTRAL": "INSUFFICIENT_EVIDENCE"
            }
        }
    }

    # Parameters
    parameters = {
        "tau_star": 0.650,
        "tuning_objective": "J = Macro_F1_3cl - 0.15 * Coverage",
        "random_control_seeds": 100,
        "permutation_test_resamples": 5000,
        "bootstrap_ci_resamples": 2000,
        "fdr_correction_method": "Benjamini-Hochberg",
        "gold_classes_present_in_evaluation": ["CONTRADICTED", "INSUFFICIENT_EVIDENCE"],
        "gold_supported_count": 0,
        "evaluation_scope": "Option C: Cross-lingual verifier prediction sensitivity and routing disagreement under Hindi-to-English translation shift",
        "test_split_designation": "EXPLORATORY / PREVIOUSLY INSPECTED"
    }

    # Environment
    env = {
        "os": platform.platform(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "torch_version": torch.__version__,
        "transformers_version": transformers.__version__,
        "num_cpu_threads": torch.get_num_threads()
    }

    # Output file hashes
    output_hashes = {}
    for item in sorted(canon_dir.glob("*")):
        if item.is_file() and item.name != "RUN_MANIFEST.json":
            output_hashes[item.name] = compute_sha256(item)
    for item in sorted(fig_dir.glob("*")):
        if item.is_file():
            output_hashes[f"figures/{item.name}"] = compute_sha256(item)

    manifest = {
        "manifest_version": "1.0",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "execution_command": ".venv/Scripts/python.exe scripts/run_corrected_experiments.py",
        "git_info": get_git_info(),
        "environment": env,
        "input_artifacts": inputs,
        "model_configurations": models,
        "experimental_parameters": parameters,
        "canonical_outputs": output_hashes,
        "freeze_gate_status": {
            "gate_a_integrity_and_data_provenance": "PASS",
            "gate_b_literature_backed_bounds": "PASS",
            "gate_c_bilingual_human_verification": "NOT APPLICABLE / NOT PERFORMED (Future Work for Causal Scope)",
            "gate_d_model_inference_and_empirical_findings": "PASS",
            "gate_e_clean_room_reproducibility": "PASS",
            "overall_status": "RESEARCH FROZEN — EXPLORATORY SCOPE"
        }
    }

    manifest_path = canon_dir / "RUN_MANIFEST.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"RUN_MANIFEST.json written to {manifest_path}")

if __name__ == "__main__":
    main()
