# One-time setup for this lesson's demos (Windows). Safe to run again: it repairs a broken setup.
#   1. creates this lesson's Python virtual environment from requirements.txt
#   2. creates your API key file (only for lessons that call an API)
# Both live OUTSIDE this folder, in your user folders on this computer:
#   venv:      %LOCALAPPDATA%\ai-automation-from-scratch\venvs\M1_<lesson>
#   key file:  %USERPROFILE%\.ai-automation-from-scratch\.env
# Why not a .venv inside this folder? It would add ~100 MB per lesson, and the folder path plus the
# SDK's deep file names can go over Windows' 260-character path limit, which makes pip fail.
# And with your key outside this folder, you can zip or share the folder safely.
#
# Run it from PowerShell in this folder:
#   powershell -ExecutionPolicy Bypass -File .\setup.ps1
# On Mac / Linux, follow the "Mac / Linux" steps in README.md instead.

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$lesson = [regex]::Match((Split-Path -Leaf (Split-Path -Parent $PSScriptRoot)), '^\d+\.\d+\.\d+').Value
if (-not $lesson) { throw 'Run this from a lesson''s code folder (for example "1.1.1 - How Models Read\code").' }
$venv = Join-Path $env:LOCALAPPDATA "ai-automation-from-scratch\venvs\M1_$lesson"
$venvPython = Join-Path $venv 'Scripts\python.exe'

# A venv whose Python was moved or uninstalled no longer starts: rebuild it.
if (Test-Path $venvPython) {
  & $venvPython -c "import sys" 2>$null
  if ($LASTEXITCODE -ne 0) {
    Write-Host 'The existing environment does not work any more. Rebuilding it...'
    Remove-Item -Recurse -Force $venv
  }
}

if (-not (Test-Path $venvPython)) {
  Write-Host "Creating the Python environment for lesson $lesson ..."
  New-Item -ItemType Directory -Force (Split-Path $venv) | Out-Null
  # Prefer the Windows "py" launcher; fall back to "python" on PATH. Python 3.10+ is required.
  $made = $false
  if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 -m venv $venv
    $made = ($LASTEXITCODE -eq 0)
  }
  if (-not $made) {
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
      throw 'Python was not found. Install Python 3.12 or 3.13 from https://www.python.org/downloads/ (tick "Add python.exe to PATH"), then run this again.'
    }
    & python -m venv $venv
    if ($LASTEXITCODE -ne 0) { throw 'Could not create the virtual environment.' }
  }
}

& $venvPython -c "import sys; assert sys.version_info >= (3, 10), sys.version" 2>$null
if ($LASTEXITCODE -ne 0) {
  Remove-Item -Recurse -Force $venv
  throw 'This course needs Python 3.10 or newer. Install Python 3.12 or 3.13, then run this again.'
}

Write-Host 'Installing packages (the first run takes a minute)...'
& $venvPython -m pip install --disable-pip-version-check --quiet -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'pip install failed (see the message above).' }

# API key file: one per computer, shared by every lesson, kept out of the lesson folders.
$needsKey = Select-String -Path (Join-Path $PSScriptRoot 'requirements.txt') -Pattern '^anthropic' -Quiet
if ($needsKey) {
  $keyDir = Join-Path $env:USERPROFILE '.ai-automation-from-scratch'
  $keyFile = Join-Path $keyDir '.env'
  if (-not (Test-Path $keyFile)) {
    New-Item -ItemType Directory -Force $keyDir | Out-Null
    Copy-Item (Join-Path $PSScriptRoot '.env.example') $keyFile
    Write-Host "Created your key file: $keyFile"
    Write-Host '  Open it (notepad $env:USERPROFILE\.ai-automation-from-scratch\.env), paste your key after ANTHROPIC_API_KEY= and save.'
  } else {
    Write-Host "Key file found: $keyFile"
  }
}

Write-Host ''
Write-Host 'Ready. Run a demo like this (from this folder):'
Get-ChildItem -Filter '*.py' | Where-Object { $_.Name -ne 'course_env.py' } | ForEach-Object {
  Write-Host "  .\run.ps1 $($_.Name)"
}
