import os
import sys
import platform
import shutil
import json
import psutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = PROJECT_ROOT / "audit"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

def generate_environment_report():
    import torch
    import transformers
    
    mem = psutil.virtual_memory()
    disk = shutil.disk_usage(PROJECT_ROOT)
    
    # Packages
    try:
        import importlib.metadata as im
        installed_packages = {dist.metadata["Name"]: dist.version for dist in im.distributions()}
    except Exception as e:
        installed_packages = {"error": str(e)}

    # Redact personal paths
    py_exec_redacted = f"python-{platform.python_version()}-amd64"
    
    env_info = {
        "os_platform": platform.platform(),
        "os_release": platform.release(),
        "system_architecture": platform.machine(),
        "cpu_processor": platform.processor(),
        "cpu_cores_logical": os.cpu_count(),
        "cpu_cores_physical": psutil.cpu_count(logical=False),
        "physical_memory_ram": {
            "total_gb": round(mem.total / (1024**3), 2),
            "available_gb": round(mem.available / (1024**3), 2),
            "percent_used": mem.percent
        },
        "disk_storage": {
            "total_capacity_gb": round(disk.total / (1024**3), 2),
            "free_space_gb": round(disk.free / (1024**3), 2),
            "used_space_gb": round(disk.used / (1024**3), 2)
        },
        "python_runtime": {
            "version": sys.version.split()[0],
            "executable_type": py_exec_redacted
        },
        "pytorch": {
            "version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "cuda_device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
            "device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
        },
        "transformers": {
            "version": transformers.__version__
        },
        "key_dependencies": {
            k: installed_packages.get(k, "NOT_INSTALLED")
            for k in ["torch", "transformers", "scikit-learn", "scipy", "numpy", "pandas", "statsmodels", "matplotlib", "seaborn", "nltk", "sacrebleu", "psutil", "pyyaml"]
        }
    }
    
    env_file = AUDIT_DIR / "environment_report.json"
    with open(env_file, "w", encoding="utf-8") as f:
        json.dump(env_info, f, indent=2)
    print(f"Wrote clean, portable environment report to {env_file}")
    print(f"RAM: {env_info['physical_memory_ram']['total_gb']} GB total | Disk: {env_info['disk_storage']['free_space_gb']} GB free | CPU cores: {env_info['cpu_cores_logical']}")

if __name__ == "__main__":
    generate_environment_report()
