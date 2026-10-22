---
name: paperbanana
description: "Use when generating paper figures: diagrams, plots."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [paperbanana, papervizagent, academic-figures, diagrams, multi-agent, google-research]
    related_skills: [diagram-design, architecture-diagram, research-reporting]
---

# PaperBanana (generates academic paper figures from method text)

## Overview

Two public repos hold the same codebase. Know which is which before you touch either.

| Repo | What it is | State |
|---|---|---|
| `dwzhu-pku/PaperBanana` | The maintained one. Google's agent core **plus** a multi-provider layer and UIs. | Active, 7.3k stars, Apache-2.0 |
| `google-research/papervizagent` | The upstream Google release. Agent core only, Gemini-only, 37 files. | Frozen, 560 stars |

The agent core is **Google's code nearly verbatim**. Diff against upstream: `prompts/diagram_eval_prompts.py` = **0 lines different**; `agents/retriever_agent.py` and `agents/critic_agent.py` = **4 lines each** (renames `call_gemini_with_retry_async` → `call_model_with_retry_async`, `model_name` → `main_model_name`). Everything the fork adds lives in `utils/generation_utils.py` (464 → 1189 lines, the provider layer), `demo.py` / `app.py` (UIs), and `tests/`.

Practical consequence: **do not expect different research from the fork.** Use the fork because it runs on any provider. Use upstream only if you want the pristine reference.

Full provenance, the diff method, and upstream-getting steps: `references/repo-provenance.md`.

Pipeline, 5 agents: Retriever (finds similar diagrams from the reference set) → Planner (writes a detailed textual description) → Stylist (applies a style guide auto-mined from NeurIPS 2025 diagrams) → Visualizer (renders via image-gen model) → Critic (loops back to Visualizer, default 3 rounds).

## When to Use

- Generating a methodology diagram, pipeline figure, or architecture figure from a paper's method section
- Generating statistical plots from raw data + a visual intent
- Working on, debugging, or self-hosting the PaperBanana / PaperVizAgent repo
- Evaluating whether PaperBananaBench or the PaperBanana claims hold up

**Don't use for:**
- Hand-built diagrams where you control every element → `architecture-diagram`, `diagram-design`, `excalidraw`
- Charts inside an HTML deliverable → `inline-svg-charts`
- Reading or summarising a paper → `paper-mechanism-map`, `arxiv`

## Install

Clone location used in this setup:

```
C:\Users\NTQUANG_DELL\research-lab\repos\PaperBanana
```

Fresh setup:

```bash
git clone https://github.com/dwzhu-pku/PaperBanana.git
cd PaperBanana
uv venv --python 3.12 .venv
uv pip install --python .venv -r requirements.txt pytest
```

Python **3.12 required** (requirements floors assume it; pyarrow 14 needs 3.12 wheels).

Verified 2026-10-21: venv builds, `pytest tests/ -q` → **135 passed, 21 subtests, ~26s**.

### Windows invocation trap

Hermes' terminal guard throws `ValueError: open: embedded null character in path` when a command contains the literal `.venv/Scripts/python.exe`. Workaround — put it in a variable:

```bash
cd ~/research-lab/repos/PaperBanana && unset PYTHONPATH && P=".venv/Scripts/python.exe" && $P skill/run.py --help
```

Always `unset PYTHONPATH`. Hermes' own venv leaks `pydantic` into the child process and every test collection fails with `ModuleNotFoundError: pydantic_core._pydantic_core`.

## API keys

Read from env var **or** `configs/model_config.yaml` (config wins). `run.py` copies the template to `model_config.yaml` on first run.

| Env var | Route | Notes |
|---|---|---|
| `OPENROUTER_API_KEY` | `openrouter/<model>` | One key for text **and** image. Recommended. |
| `GOOGLE_API_KEY` | Gemini direct | Text + image |
| `ORCAROUTER_API_KEY` | `orcarouter/<model>` | Text + image |
| `ATLASCLOUD_API_KEY` | `atlas/<model>` | Text + image |
| `OPENAI_API_KEY` | `openai/<model>` | |
| `ANTHROPIC_API_KEY` | — | Key is read; no `anthropic/` prefix routing in the fork |
| `LOCAL_OPENAI_API_KEY` | `local/<model>` | **Text only** |
| any OpenAI-compatible endpoint (ByteDance Ark, vLLM, …) | `local/<model>` + `LOCAL_OPENAI_BASE_URL` | **Text only** for the client, but the endpoint's own model must be a VLM — see pitfall 10 |
| `OLLAMA_API_KEY` | `ollama/<model>` | **Text only** |

### Is an image API mandatory? Depends on the task

The branch is `agents/visualizer_agent.py:38` — `"plot" in task_name`:

| `--task` | `use_image_generation` | Who renders | Image API needed |
|---|---|---|---|
| `plot` | **`False`** | `main_model_name` writes matplotlib code -> `execute_plot_code_worker` runs it locally | **No** |
| `diagram` | `True` | `image_gen_model_name` via `dispatch_image_generation` | **Yes** |

Statistical plots cost nothing on the image side: every agent on that path is text, and the renderer is local matplotlib. Methodology diagrams need one of exactly four image routes (`gpt-image` / OpenRouter / OrcaRouter / Gemini) — there is no local route.

Four things to know before running:

- **`--task plot` on `skill/run.py` is broken in the repo as shipped.** `task_name` never reaches `ExpConfig`, so it silently takes the diagram branch and then dies asking for a Gemini key. Two one-line patches fix it — see `references/image-routes-and-run-py-bugs.md` for the exact diffs and the verified evidence.
- **`run.py` exits 0 even when no image was produced.** The visualizer swallows exec errors, the critic finds no image and degrades to text-only critique, which always answers "no changes needed" and stops the loop. Never trust the exit code — check the output file exists.
- **`local/<model>` does not mean "on this machine".** It is just an OpenAI-compatible text endpoint that you name via `LOCAL_OPENAI_BASE_URL`. Point it at any strong coder model. Plot quality tracks how well that model writes matplotlib.
- **Check your existing Google key first.** A standard AI Studio key exposes this repo's defaults (`gemini-3.1-pro-preview`, `gemini-3.1-flash-image-preview`), so no new signup is needed for the diagram path.

### Running a real bench case: `scripts/run_case.py`

`skill/run.py` takes `--content` inline, which is painful for a full paper section. This driver pulls a real case out of the bench, stages its `content` into a temp file, injects API keys from the Hermes `.env` (secrets never land in the repo), and verifies the output file exists.

```bash
cd ~/research-lab/repos/PaperBanana && unset PYTHONPATH && P=".venv/Scripts/python.exe"
S="C:/Users/NTQUANG_DELL/AppData/Local/hermes/skills/creative/paperbanana/scripts/run_case.py"
$P "$S" --task diagram --case-index 0 --out diagram_case0.png --dry-run   # inspect first
$P "$S" --task diagram --case-index 0 --out diagram_case0.png
```

ByteDance Ark, no OpenRouter and no Google quota. `--ark` reads `base_url` + `api_key` from the
Hermes `config.yaml` `custom_providers` entry named `ark-v3` and routes every text agent there:

```bash
$P "$S" --task plot --case-index 0 --ark --out plot_ark_case0.png --dry-run
$P "$S" --task plot --case-index 0 --ark --out plot_ark_case0.png
```

Verified 2026-10-22: `--dry-run` prints `main model = local/deepseek-v4-pro-ga-260813`, Ark client
initialises, OpenRouter is withheld. Text latency on Ark: ~1-2 s short prompt, ~15 s for a 30k-char
prompt with 1.2k output tokens.

It prints the ground-truth image path so you can compare against the paper's own figure. Run it with the repo's venv python (it re-uses `sys.executable`). Keys read from `%LOCALAPPDATA%\hermes\.env`, override with `HERMES_ENV`; repo path via `PAPERBANANA_REPO`.
## Usage

```bash
cd ~/research-lab/repos/PaperBanana && unset PYTHONPATH && P=".venv/Scripts/python.exe"

$P skill/run.py \
  --content-file method.md \
  --caption "Figure 1: Overview of the proposed framework" \
  --task diagram \
  --output figure.png
```

Verified: `--help` exits 0 and lists all flags.

| Flag | Default | Meaning |
|---|---|---|
| `--content` / `--content-file` | — | Method text (one required) |
| `--caption` | required | Figure caption / visual intent |
| `--task` | `diagram` | `diagram` or `plot` |
| `--output` | `output.png` | Multi-candidate writes `<stem>_0.png`, `_1.png`, … |
| `--aspect-ratio` | `21:9` | `21:9`, `16:9`, `3:2` |
| `--figure-size` | provider default | `1-3cm` … `14-17cm` → provider image-size tier |
| `--num-candidates` | `10` | Parallel candidates |
| `--max-critic-rounds` | `3` | Visualizer↔Critic loop |
| `--retrieval-setting` | `auto` | `auto`, `manual`, `random`, `none` |
| `--main-model-name` | `gemini-3.1-pro-preview` | VLM for all agents |
| `--image-gen-model-name` | `gemini-3.1-flash-image-preview` | Image model |
| `--exp-mode` | `demo_full` | `demo_full` (with Stylist) or `demo_planner_critic` |

Output: absolute path of each saved image, one per line on stdout.

`main.py` is a **separate** entry point — the benchmark eval harness. It reads `PaperBananaBench` and the model config and runs full evaluation. `skill/run.py` is the one-off "give me a figure" entry. Don't confuse them.

## Dataset

`PaperBananaBench` is **not in the repo** (`.gitignore`d). Actual counts in the public dataset, verified by downloading it 2026-10-21:

| Task | test | ref | images on disk |
|---|---|---|---|
| diagram | 292 | **298** | 590 |
| plot | 240 | 240 | 480 |

Note the discrepancy: the paper states 292 reference cases, the published dataset ships **298**. Quote 298 when citing the dataset, 292 when citing the paper — do not silently reconcile them.

Curated from NeurIPS 2025. Total download ≈ 288 MB.

- Auto: `skill/run.py` calls `scripts/prepare_bench.py` when the task dir is unusable.
- Manual: `$P scripts/prepare_bench.py --tasks diagram plot --data-dir data`
- Source: HuggingFace `dwzhu/PaperBananaBench` (public, ungated — verified HTTP 200). Set `HF_TOKEN` to avoid the unauthenticated rate-limit warning.

Layout it writes:

```
data/PaperBananaBench/{diagram,plot}/{test,ref}.json
data/PaperBananaBench/{diagram,plot}/images/<file>.jpg
```

Without the dataset the Retriever has no reference set and the run degrades toward zero-shot. The Stylist's style guide still ships in-repo (`style_guides/neurips2025_diagram_style_guide.md`), so styling survives.

## Common Pitfalls

1. **Expecting the fork to be new research.** It isn't. Google's agent core, verbatim. Read the paper, not the diff.
2. **Trying to run image generation on a local model.** Blocked at `generation_utils.py:91`. Only the VLM agents can be local.
3. **Exposing the web UI publicly.** `utils/plot_execution.py:49` does `exec(code_clean, exec_globals)` on **LLM-generated** matplotlib code. It does run inside a `ProcessPoolExecutor` (`visualizer_agent.py:41`), so the process is separate and an infinite loop does not take the parent down — but that is availability isolation, **not a security boundary**: same user, full filesystem, no seccomp, `exec_globals` empty. Combined with the `Dockerfile` (`python:3.12-slim` as root, `EXPOSE 8080`, `chmod -R 777 data`), prompt injection reaches host code execution. Bind to localhost or sandbox the container before exposing.
4. **Forgetting `unset PYTHONPATH`.** Hermes' venv contaminates the child → `pydantic_core` import error, all test modules fail collection.
5. **Forgetting the `$P` variable trick on Windows.** Literal `.venv/Scripts/python.exe` trips the terminal guard.
6. **Underestimating runtime.** One candidate is 3-10 min (Retriever + Planner + Stylist + Visualizer + up to 3 Critic rounds, each several LLM calls). Default 10 candidates in parallel ≈ 10-30 min.
7. **Reading the README as the API surface.** `main.py` and `skill/run.py` are different tools with different flags.
8. **Assuming commercial use is fine.** Google filed patents on the workflow; the repo states no commercial use is planned and that it is not an officially supported Google product.
9. **Trusting the benchmark numbers blindly.** Scoring is VLM-as-a-Judge against human figures, i.e. a model grading model-family output. The paper reports correlation checks with human judgment; read them before quoting the deltas.
10. **Pointing the `local/` route at a text-only model.** `agents/planner_agent.py:98` sends the **10 retrieved reference figures as base64 images** (`{"type": "image", "image_base64": …}`) to `main_model_name`. A text-only model (e.g. Ark `deepseek-v4-pro-ga-260813`) does not refuse — it **hangs**. Worse, `_client_for_local_text` builds `AsyncOpenAI` **without a timeout**, so the SDK default of 600 s applies and the progress bar sits at `Processing concurrently: 0%` with no error and no retry line. Symptom seen: a 218 KB reference JPEG becomes a 291 K-char data URL; the run stalls 4+ min at 0% while a plain text call to the same endpoint answers in 2 s. Fix: use a VLM on that endpoint. Diagnose by checking whether any `python.exe` child is alive (`ps -W | grep -i python`) — if the log is frozen but the process lives, it is this.

## Verification Checklist

Run the bundled health check first — it covers every box below:

```bash
bash "$HOME/AppData/Local/hermes/skills/creative/paperbanana/scripts/health.sh"
# optional arg: path to the repo, default ~/research-lab/repos/PaperBanana
```

It verifies python, imports, the CLI, the test suite, the dataset, and image-provider key presence, and exits non-zero on failure. Sample output when healthy but unconfigured:

```
== tests ==    135 passed, 21 subtests passed in 14.10s
== dataset ==  WARN: no dataset. Retriever has no reference set.
== image key == WARN: no image-capable key. local/ and ollama/ are text-only.
HEALTH: OK
```

Then confirm by hand:

- [ ] `unset PYTHONPATH` and `$P=".venv/Scripts/python.exe"` in the command
- [ ] `$P -m pytest tests/ -q` → 135 passed before trusting any change
- [ ] `$P skill/run.py --help` exits 0
- [ ] API key present for a **non-local** image provider, or the run fails at the Visualizer
- [ ] Dataset present at `data/PaperBananaBench/{diagram,plot}/{test,ref}.json` when few-shot matters
- [ ] UI bound to localhost, not `0.0.0.0`, if you started `demo.py` or `app.py`
- [ ] `data/` and `results/` stay out of git (already in `.gitignore`)

## One-Shot Recipes

**Diagram from a paper's method section**

```bash
cd ~/research-lab/repos/PaperBanana && unset PYTHONPATH && P=".venv/Scripts/python.exe"
$P skill/run.py --content-file method.md \
  --caption "Figure 1: Overview of our framework" \
  --task diagram --num-candidates 4 --output fig.png
```

**Statistical plot, fully local, zero API cost**

```bash
cd ~/research-lab/repos/PaperBanana && unset PYTHONPATH && P=".venv/Scripts/python.exe"
export LOCAL_OPENAI_BASE_URL="http://127.0.0.1:11434/v1"   # or your own server
$P skill/run.py --task plot \
  --main-model-name "ollama/qwen2.5:3b" \
  --content-file data.json \
  --caption "Bar chart: number of publications by year" \
  --output plot.png
```

No image provider required — `--task plot` renders via generated matplotlib code executed locally.

**Check the install is healthy**

```bash
bash "$HOME/AppData/Local/hermes/skills/creative/paperbanana/scripts/health.sh"
```

**Compare fork vs upstream** — see `references/repo-provenance.md`.
