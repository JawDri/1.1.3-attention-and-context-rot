# Lesson 1.1.3 — Attention & Context Rot

Demo code for **Lesson 1.1.3** of *AI Automation: From Scratch* (Module 1).

<!-- links:start -->
<!-- links:end -->

<!-- files:start -->
| File | What it shows | Needs |
|---|---|---|
| [`attention_budget.py`](code/attention_budget.py) | Softmax adds up to 100%, and the same rule's share shrinks as the prompt grows (slides 04-05). | nothing (no packages) |
| [`prompt_sandwich_template.xml`](code/prompt_sandwich_template.xml) | The prompt sandwich template (slide 08). Copy it, don't run it. | - |
| [`lost_in_the_middle_test.py`](code/lost_in_the_middle_test.py) | Optional experiment: one fact hidden at 5%, 50% and 95% of a long prompt. `--dry-run` sends nothing. | API key, about $0.01 per run (Claude Haiku 5.5) |
<!-- files:end -->

## Get the code
- **Download:** the green **Code** button → **Download ZIP**, then unzip it.
- **Or clone:** `git clone https://github.com/JawDri/1.1.3-attention-and-context-rot.git`

Keep the folder's name as it is: `setup.ps1` and `run.ps1` read the lesson number (1.1.3) from it.

## Run it
Everything is in [`code/README.md`](code/README.md): set up once (`setup.ps1` on Windows, a virtual environment on
Mac / Linux), then run the demos from the `code` folder.

## Your API key stays on your computer
The scripts that call the API read your key from your own key file, outside this folder:
`%USERPROFILE%\.ai-automation-from-scratch\.env` on Windows, `~/.ai-automation-from-scratch/.env` on Mac / Linux.
`code/.env.example` is only the template: never put a real key in it. `.gitignore` keeps `.env` files out of git,
so a fork or a pull request can't carry a key by mistake.
