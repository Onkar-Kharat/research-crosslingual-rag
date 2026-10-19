from __future__ import annotations
import json, os, platform, shutil, subprocess, sys
from pathlib import Path
from datetime import datetime

def cmd(args):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=10)
        return {"returncode": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()}
    except Exception as e:
        return {"error": str(e)}

def ram():
    if platform.system() == "Windows":
        r = cmd(["powershell","-NoProfile","-Command",
          "$o=Get-CimInstance Win32_OperatingSystem; [PSCustomObject]@{Total=$o.TotalVisibleMemorySize;Free=$o.FreePhysicalMemory} | ConvertTo-Json"])
        try:
            o=json.loads(r["stdout"])
            return {"total_gb":round(int(o["Total"])/1024/1024,2),"free_gb":round(int(o["Free"])/1024/1024,2)}
        except Exception: pass
    try:
        import psutil
        m=psutil.virtual_memory()
        return {"total_gb":round(m.total/1024**3,2),"available_gb":round(m.available/1024**3,2)}
    except Exception: return {"note":"RAM detection unavailable"}

def main():
    root=Path(__file__).resolve().parents[1]
    d=shutil.disk_usage(root)
    r={"timestamp":datetime.now().astimezone().isoformat(),"project_root":str(root),
       "python_executable":sys.executable,"python_version":sys.version,"platform":platform.platform(),
       "cpu_count_logical":os.cpu_count(),"ram":ram(),
       "disk_gb":{"total":round(d.total/1024**3,2),"used":round(d.used/1024**3,2),"free":round(d.free/1024**3,2)},
       "gpu":cmd(["nvidia-smi"]) if shutil.which("nvidia-smi") else {"detected":False,"note":"nvidia-smi not found"},
       "git":cmd(["git","--version"]) if shutil.which("git") else {"detected":False},
       "is_virtual_environment":sys.prefix != sys.base_prefix}
    out=root/"logs"/"preflight_report.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(r,indent=2),encoding="utf-8")
    print(json.dumps(r,indent=2))
    if not r["is_virtual_environment"]: print("WARNING: Activate .venv and rerun.")
if __name__=="__main__": main()
