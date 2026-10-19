$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
$chosen = $null
if (Test-Path ".venv") {
  Write-Host ".venv exists; skipping version check for environment creation."
} else {
  if (Get-Command py -ErrorAction SilentlyContinue) {
    foreach ($ver in @("-3.11", "-3.12", "-3.14")) {
      try {
        $out = & py $ver --version 2>$null
        if ($LASTEXITCODE -eq 0) { $chosen = @("py", $ver); Write-Host "Selected $out"; break }
      } catch {}
    }
  }
  if (-not $chosen -and (Get-Command python -ErrorAction SilentlyContinue)) {
    $v = (& python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')").Trim()
    if ($v -in @("3.11","3.12","3.14")) { $chosen = @("python") }
  }
  if (-not $chosen) { throw "Python 3.11, 3.12, or 3.14 not found. Install Python 3.11 (recommended) or 3.12." }
}
if (-not (Test-Path ".venv")) {
  if ($chosen[0] -eq "py") { & py $chosen[1] -m venv .venv } else { & python -m venv .venv }
  if ($LASTEXITCODE -ne 0) { throw "Failed to create .venv" }
} else { Write-Host ".venv exists; leaving it unchanged." }
$vp = Join-Path (Get-Location) ".venv\\Scripts\\python.exe"
& $vp -m pip install --upgrade pip
& $vp -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed. Do not install packages globally." }
Write-Host "Ready. Activate with .\\.venv\\Scripts\\Activate.ps1 then run python scripts\\preflight.py"
