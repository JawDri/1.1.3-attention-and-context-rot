# Lesson 1.1.3 — demo code: Attention & Context Rot

| File | What it shows | Needs |
|---|---|---|
| `attention_budget.py` | Softmax adds up to 100%, and the same rule's share shrinks as the prompt grows (slides 04-05). | nothing (no packages) |
| `prompt_sandwich_template.xml` | The prompt sandwich template (slide 08). Copy it, don't run it. | - |
| `lost_in_the_middle_test.py` | Optional experiment: one fact hidden at 5%, 50% and 95% of a long prompt. `--dry-run` sends nothing. | API key, about $0.01 per run (Claude Haiku 5.5) |

prices.json = Claude prices used to print the cost of the experiment.

## Set up on Windows (once per computer)
PowerShell and Python 3.10 or newer ([python.org](https://www.python.org/downloads/), tick
"Add python.exe to PATH"). Open PowerShell **in this folder** (in Explorer: Shift + right-click →
"Open PowerShell window here", or `cd` to it) and run:
```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```
It creates this lesson's Python environment from `requirements.txt` in
`%LOCALAPPDATA%\ai-automation-from-scratch\venvs\M1_1.1.3` (outside this folder, so the folder stays
small and Windows' path-length limit is never hit). Run it again any time: it repairs a broken setup.

## Run on Windows
```powershell
.\run.ps1 attention_budget.py
.\run.ps1 lost_in_the_middle_test.py
```
If PowerShell refuses to run `.\run.ps1`:

- "running scripts is disabled": allow local scripts once for your user with
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, or run
  `powershell -ExecutionPolicy Bypass -File .\run.ps1 <script.py>` instead.
- "not digitally signed": Windows marked these files as downloaded (from a zip, for example).
  Unblock them once, from this folder: `Get-ChildItem -Recurse | Unblock-File`.

## Mac / Linux
`setup.ps1` and `run.ps1` are for Windows. With Python 3.10 or newer (check: `python3 --version`), open
a terminal in this folder and set up once:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Then run the demos (same options as on Windows):
```bash
python attention_budget.py
python lost_in_the_middle_test.py
```
In a new terminal, run `source .venv/bin/activate` first. On Ubuntu/Debian, if `python3 -m venv` fails:
`sudo apt install python3-venv`.

## API key (only for the scripts marked "API key")
1. Create a key at [platform.claude.com](https://platform.claude.com) (add ~$5 credit and a monthly
   spend limit first: Lesson 1.2.1).
2. Paste it after `ANTHROPIC_API_KEY=` in your key file, which lives **outside this folder** (one file
   for every lesson):
   - Windows: `setup.ps1` already created it. Open it with
     `notepad $env:USERPROFILE\.ai-automation-from-scratch\.env`, paste your key and save.
   - Mac / Linux: create it once (`-n` keeps the file if you already made it), then paste your key:
     ```bash
     mkdir -p ~/.ai-automation-from-scratch
     cp -n .env.example ~/.ai-automation-from-scratch/.env
     nano ~/.ai-automation-from-scratch/.env   # save: Ctrl+O, Enter. Quit: Ctrl+X
     ```
3. `.env.example` in this folder is only the template. Never put a real key in it: anyone you share
   this folder with would see it.
4. Every script that calls the API has `--dry-run`: it prints the exact request and sends nothing.

## Helper files (the demos need them; no need to edit them)
- `course_env.py`: the shared helper every demo imports (finds your API key, sets the download folder,
  loads prices).
- `setup.ps1` and `run.ps1`: set up this lesson once, then run a demo (Windows).
- `.env.example`: the template for your key file.
