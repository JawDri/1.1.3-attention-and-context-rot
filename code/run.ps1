# Runs one of this lesson's demos with the lesson's Python environment (made by setup.ps1). Windows.
#   .\run.ps1 <script.py> [options]      e.g.  .\run.ps1 cost_calculator.py --runs-per-day 800
# On Mac / Linux: activate the environment (see README.md), then  python <script.py> [options]

$lesson = [regex]::Match((Split-Path -Leaf (Split-Path -Parent $PSScriptRoot)), '^\d+\.\d+\.\d+').Value
$venvPython = Join-Path $env:LOCALAPPDATA "ai-automation-from-scratch\venvs\M1_$lesson\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
  Write-Host 'This lesson is not set up on this computer yet. Run this first:'
  Write-Host '  powershell -ExecutionPolicy Bypass -File .\setup.ps1'
  exit 1
}
if ($args.Count -eq 0) {
  Write-Host 'Usage: .\run.ps1 <script.py> [options]   Scripts in this folder:'
  Get-ChildItem $PSScriptRoot -Filter '*.py' | Where-Object { $_.Name -ne 'course_env.py' } | ForEach-Object { Write-Host "  $($_.Name)" }
  exit 1
}
$script = Join-Path $PSScriptRoot $args[0]
$rest = @($args | Select-Object -Skip 1)
$env:PYTHONDONTWRITEBYTECODE = '1'   # keep __pycache__ folders out of this folder
& $venvPython $script @rest
exit $LASTEXITCODE
