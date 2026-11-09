"""Shared helpers for the Module 1 demos: API keys, caches and prices.

Every lesson's code folder has its own copy of this file, so each folder runs on its own.

API keys are read in this order:
  1. a variable already set in your terminal, e.g.  $env:ANTHROPIC_API_KEY = "sk-ant-..."  (PowerShell)
     or  export ANTHROPIC_API_KEY=sk-ant-...  (Mac / Linux)
  2. the course key file, outside the lesson folders:
       Windows:      %USERPROFILE%\\.ai-automation-from-scratch\\.env
       Mac / Linux:  ~/.ai-automation-from-scratch/.env
The key file lives outside the lesson folders on purpose: zipping or sharing a folder never shares
your key. On Windows, setup.ps1 creates it from .env.example the first time you run it; on
Mac / Linux, copy .env.example there yourself (see README.md).
"""
import json
import os
import sys
from pathlib import Path

HOME = Path(os.environ.get("USERPROFILE") or Path.home())
KEY_FILE = HOME / ".ai-automation-from-scratch" / ".env"
# Downloads (tokenizer files, embedding models) go here, outside the lesson folders, so they stay small
# (Windows: %LOCALAPPDATA%\ai-automation-from-scratch, Mac / Linux: ~/.cache/ai-automation-from-scratch).
CACHE_DIR = Path(os.environ.get("LOCALAPPDATA") or (HOME / ".cache")) / "ai-automation-from-scratch"
HERE = Path(__file__).resolve().parent

# Windows terminals sometimes default to an old code page; force UTF-8 so the bars and arrows print.
for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


def load_key_file():
    """Copy KEY=VALUE lines from the course key file into the environment (terminal values win)."""
    if not KEY_FILE.exists():
        return
    for line in KEY_FILE.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        if value:
            os.environ.setdefault(name.strip(), value)


def require_anthropic_key():
    """Stop with a clear message when no real Anthropic key is set."""
    load_key_file()
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key or "your-key" in key:
        print("No Anthropic API key found.\n"
              f"  1. Create a key at https://platform.claude.com (API keys page).\n"
              f"  2. Paste it into {KEY_FILE}  as  ANTHROPIC_API_KEY=sk-ant-...\n"
              "     (no such file yet? Windows: run .\\setup.ps1 once. Mac / Linux: copy .env.example there.)\n"
              "  Or run this script with --dry-run to see the request without sending it.")
        sys.exit(2)
    return key


def cache_path(name):
    path = CACHE_DIR / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_prices():
    """Prices per 1M tokens, from prices.json next to this file (update it from the pricing page)."""
    return json.loads((HERE / "prices.json").read_text(encoding="utf-8"))


def usd(amount):
    return f"${amount:,.4f}" if amount < 1 else f"${amount:,.2f}"
