---
name: model-cost-optimization
description: "Use when cutting LLM cost or deploying local models."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [llm-cost, model-routing, local-models, ollama, vllm, telemetry]
    related_skills: [hermes-agent, cron-job]
---

# Model Cost Optimization & Workload Routing

Decide which model tier handles which task to save API tokens, and wire local models into Hermes for the cheap tier.

## When to use
- User complains about token cost, a provider "run out of limit", or that local models generate slowly.
- User downloads local models (Gemma/Qwen GGUF) and wants to offload work to them.
- User asks for an "orchestrator/router" to distribute calls across model providers.

## Step 0 — Check hardware BEFORE promising local inference (critical)
Never assume a local model can run on the host machine. Probe first:
- `nvidia-smi` may be missing; fall back to `wmic path win32_VideoController get name,AdapterRAM` (Windows) to see real GPUs.
- A 6GB VRAM user may have a laptop (Quadro 2GB + Intel HD) on the Hermes host — the real GPU is often on a SEPARATE machine reachable only via Tailscale/WireGuard (100.64.0.0/10 range).
- Model memory needs (Q4): 7B≈5GB, 12B≈7GB, 27B≈16GB. If host VRAM is below that, CPU-only offload gives ~1-3 tok/s — not worth it. Tell the user plainly rather than downloading more huge models.

### CPU-only host (no GPU): prove deployability with a probe, not vibes (verified 2026-09-25)

For any "can I self-host this model repo here?" question on a GPU-less box (e.g. an encoder/classifier repo such as GLiFormer jeff, a reranker, a small BERTheavy pipeline). Steps 1-3 cost minutes and can kill the plan before you download gigabytes.

1. **Wheel-tag audit before installing.** Query PyPI for the exact version's file list and check for `cp3XX-win_amd64`:
   `curl -s https://pypi.org/pypi/<pkg>/json | python -c "import json,sys;d=json.load(sys.stdin);print(d['info']['requires_python']);[print(f['filename'],round(f['size']/1e6,1),'MB') for f in d['urls']]"`
   Read `requires_dist` the same way. A package can ship a `cp314-win_amd64` wheel while its *dependencies* still call removed APIs — see pitfall 5.
2. **Resolve without downloading:** `uv venv --python 3.12 /tmp/probe`, then `uv pip install --dry-run --python "<absolute Windows path to venv python>" <deps...>`. Exit 0 + a `+ pkg==ver` list = resolvable for that interpreter. Pass the **Windows** path (`C:/.../probe/Scripts/python.exe`); uv rejects the MSYS `/tmp/...` form with "no virtual environment found".
3. **An interpreter pin is not a blocker.** A repo pinning `requires-python = ">=3.12,<3.13"` + `.python-version` = 3.12 works fine with `uv python install 3.12` (~15 s — uv downloads CPython itself) then `uv sync`. Don't treat the pin as a wall, and don't run the repo on the system default interpreter just to dodge the download.
4. **CPU-only torch is the default on Windows.** PyPI's Windows torch wheels are already CPU-only (~124 MB for 2.14.0) unlike manylinux (~555 MB, CUDA payload). In containers/Modal add `extra_index_url=https://download.pytorch.org/whl/cpu`.
5. **PITFALL — Hermes' own `PYTHONPATH` poisons every non-3.11 venv.** The agent environment exports `PYTHONPATH=<hermes-agent>;<hermes-agent>\venv\Lib\site-packages` (3.11-based). A 3.12/3.14 venv then imports 3.11 C-extensions and dies with `ImportError: No module named 'numpy._core._multiarray_umath'` (the message listing `*.cp311-win_amd64.pyd` is the tell). **Always `unset PYTHONPATH` before invoking a venv python**, then re-export only what the project needs (`PYTHONPATH=src` for a src-layout repo). This is not a broken venv — do NOT reinstall.
6. **Pitfall — Python 3.14 is an unsupported path for `torch.jit.script`.** torch prints `FutureWarning: torch.jit.script is not supported in Python 3.14+ and may break`; libraries built on it (gliner/gliformer) still ran once in testing, so never present 3.14 as validated — install the pinned interpreter, or state the risk explicitly.
7. **Pitfall — direct script invocation needs the src path.** `python scripts/export_onnx.py ...` fails with `ModuleNotFoundError: No module named '<pkg>'` when the repo only self-registers via its entry point — run `PYTHONPATH=src python scripts/...`.
8. **Measure RAM by system delta, not struct RSS.** `GetProcessMemoryInfo` (psapi) returned all zeros on this host; use `GlobalMemoryStatusEx` before/after load and report the delta. Budget ≈ weights + runtime: a 1.05 GB fp32 checkpoint → ~+2.6 GB resident; a 2.3 GB checkpoint → expect ~4-5 GB.
9. **Run the probe, then extrapolate only with a stated factor.** `scripts/cpu_inference_probe.py` (this skill) loads a checkpoint, times bs=1 / bs=N / long-context, and prints system RAM. Measured on this laptop (i7-4910MQ 4C/8T Haswell, 15.9 GB, torch CPU fp32 eager, 8 threads): 146M encoder → **411 ms @77 tok bs=1**, **4.19 s @797 tok**, bs=8 only 1.6x better (250 ms/text), full 3-question request ≈0.6 s. Scale **x2.6** for a 400M/2.3 GB encoder on x86 (Apple silicon stays ~x1 — bandwidth-bound); a hosted 8-core x86 was 1.3-1.7x faster than this laptop. If a number is extrapolated rather than measured, label it as such — never dress x2.6 arithmetic up as a measurement.
   **The x2.6 factor was later CONFIRMED by direct measurement (2026-09-25)** on the same laptop, same probe: 400M/2.3 GB encoder loaded from local disk → **823 ms @77 tok bs=1** (x2.0 of the 146M figure), **477 ms/text @bs=8**, **9.52 s @797 tok** (x2.3), full 3-question request **1.46 s**, model load **20.8 s**, peak **RSS 11.2 GB**. So the extrapolated ~1.0-1.1 s for 400M was ~25% high but the right order — usable for a go/no-go call, not for quoting as fact. Always replace the estimate with a measurement once the checkpoint actually lands.
10. **Verdict framing for encoder/classifier models:** CPU self-hosting is 6-20x MORE expensive than the API's per-token price and 40-90x worse than the cheapest GPU (L4), and batching barely helps on CPU. Recommend CPU only for privacy, low volume, or a genuinely GPU-less host; recommend a cheap GPU or the hosted API for latency-/QPS-sensitive work.
11. **Large HF downloads throttle per connection.** `resolve/main/<file>` single-stream ran ~0.5-1.1 MB/s; 8 parallel range requests reached ~1.7 MB/s. Use `scripts/hf_parallel_fetch.sh` (resumable `curl -C - -r` chunking + reassembly, verifies total against Content-Length); expect 15-80 min for 2.3 GB.
    **PITFALL — a range-fetch script can report failure while the bytes are actually fine.** Observed 2026-09-25: `fetch.sh` printed `curl: option -r: is badly used here` for some chunks, assembled a 309 MB file against an expected 2.30 GB, then `rm -f part.*` failed with `Device or resource busy`. Verdict should NOT be "download failed" — **check the parts first**: all 8 were exactly 287,841,982 bytes and `cat part.*` summed to 2,302,735,855 = the exact `Content-Length`. The assembly step had run while chunks were still being written. Recovery costs nothing: verify `sum(part sizes) == Content-Length`, then concatenate yourself. Do this BEFORE restarting a multi-GB download.
12. **PITFALL — HF/transformers libraries reject MSYS paths; pass the Windows form.** `GLiFormer.from_pretrained("/d/ai-router-test/models/x")` (git-bash path) dies with:
    `HFValidationError: Repo id must be in the form 'repo_name' or 'namespace/repo_name': '/d/ai-router-test/models/x'`
    — the loader can't tell a local dir from a repo id, so it validates the string and rejects it. Use `D:/ai-router-test/models/x` (forward slashes, drive letter, quotes in bash). Same class of failure as uv's "no virtual environment found" on `/tmp/...` in step 2: **any Windows binary reached from git-bash wants a `C:/`-style path, never `/c/` or `/d/`.**
13. **Prove the code path, not just the install.** Fake-backend unit tests passing under two interpreters (3.12 and 3.14 both: 15 core + 7 server tests) plus one real `Engine.run` returning byte-identical decoded values on both is what turns "deps installed" into "it works".
14. **PITFALL — a probe script's self-reported model name can be hardcoded and WRONG.** The first 400M run printed `"model": "gliformer-base-v1"` inside its answers block, which reads as "you benchmarked the wrong checkpoint". It was not: the label was a literal string passed to the engine constructor in the probe script (`Eng = Engine(b, "gliformer-base-v1")`), while the `info` line separately showed the real load path. **Trust the load line and the physics, not the label:** check `info.model` / the path actually loaded, then sanity-check against expected scaling (823 ms vs 411 ms = x2.0 for a x2.6-parameter model; load 13.2 s vs 7.5 s). If the label disagrees with those, fix the label, not the conclusion. Derive labels from the input (`Path(MODEL).name`) so the trap cannot recur.

## Step 1 — Map tasks to 3 tiers
Classify every recurring job/pipeline by reasoning+direction-strength needed:

> Before reaching for a "router" library, read `references/llm-router-landscape-2026-09.md` — it
> compares jeff / RouteLLM / LLMRouter / semantic-router by what they actually do, with published
> benchmarks and measured CPU numbers. Short version: the savings live in deterministic rules +
> caching (Tier 0), not in a small classifier model, and **none of the off-the-shelf classifiers
> support Vietnamese**.

| Tier | Examples | Model |
|------|----------|-------|
| **Heavy — MUST stay on strong API** | deep research with real citations, legal/contract review, complex code fixes/architecture, multi-agent orchestration | strong API (e.g. deepseek-v4-pro) |
| **Light — can go local or cheap** | summarize transcript, titles/hashtags, rewrite/format, short daily check-ins | local Qwen/Gemma 7-8B if host has the GPU, else cheap API |
| **Mechanical — code, 0 LLM** | watchdogs, health checks, STT (Whisper local), Trello card moves, format docx/xlsx/pdf | plain Python/scripts — biggest token saver |

The single biggest saving: split a heavy job into slices — local does raw summarize/format, API does only ~30% final (write + citations). Cuts 50-60% tokens without losing quality.

## Step 2 — Wire local model into Hermes (no custom orchestrator needed)
Hermes already routes models per-job with two mechanisms:
1. `model_aliases` in config.yaml — give each model a short name (`local-qwen`, `api-pro`) with `provider: custom` + `base_url` pointing at the local OpenAI-compatible endpoint.
2. Each `cronjob` has its own `model` + `provider` + `base_url` fields — assign a tier per job without touching others.
Build a telemetry/log layer to see real cost before scaling. Don't build a custom FastAPI orchestrator (Hướng B) until the Hermes-native path (Hướng A + alias + per-job model) proves insufficient.

## Running an agentic Hermes flow on a local model (verified 2026-08-23)
A local 8B GGUF behind an OpenAI-compatible endpoint (e.g. `unsloth/Ministral-3-8B-Instruct-2512-GGUF` served by llama.cpp, exposed at `pharma.llm.thefirstonly.com/v1`, config alias `unsloth-min`) CAN drive a full multi-step Hermes cron agent-flow end to end: pick topic → research → write draft → save file → run the pipeline's OWN verification script. Real data point: it produced a Vietnamese Threads draft that PASSED the pipeline's unslop gate (0 em dash, 0 emoji, 791 dấu, correct researcher names/years, correct "mình/bạn" voice, verbatim quotes). So do NOT assume local tiers can only do light summarize/rewrite — test the actual flow before locking the tier table.

### Pin a cron job to a local model — edit jobs.json, NOT the cron tool
The `cronjob` tool's create/update does NOT expose per-job `model`/`provider`/`base_url` — a job created there comes back `model: null` and silently runs the session default (e.g. opencode-go / deepseek-v4). To pin a job to a local model:
1. Create the job with cronjob (schedule + prompt).
2. Edit `~/AppData/Local/hermes/cron/jobs.json` directly: set that job's `model` and `provider` fields, copying verbatim from a known-working job of the same provider (e.g. `model: unsloth/Ministral-3-8B-Instruct-2512-GGUF`, `provider: unsloth`, `base_url: null`). The scheduler reloads jobs.json every tick, so the patch is live immediately.
3. `cronjob action=run job_id=<id>` executes it on that model.

### Pitfall — local small models inject non-Latin glyphs into Vietnamese
An 8B local model glitched a Korean hanja char (분야, "field") into the middle of a Vietnamese sentence. The pipeline's unslop/diacritic gate PASSED it: a Korean char is neither em dash nor emoji, and the sentence still has plenty of dấu, so agentic verification says OK while the text is corrupted. When routing Vietnamese content-generation to local models: (a) ADD a prompt rule "self-check for non-Latin characters (Latin alphabet + Vietnamese diacritics only) before saving", (b) still spot-scan the output yourself for non-Latin code ranges (`re.search(r'[가-힣一-龥ぁ-ゔァ-ヺ]', text)`) even when the quality gate passes.

## Wiring checklist when the local model is on a REMOTE machine
- Verify the remote endpoint is actually OPEN: `timeout 2 bash -c "echo > /dev/tcp/IP/PORT"` per port (11434 Ollama / 8080 llama.cpp / 8000 vLLM). A machine that pings but exposes no port = nothing reachable.
- Local framework (Unsloth, etc.) does NOT auto-serve HTTP. The remote must run `ollama serve`, `llama-server`, or `vllm serve` bound to `0.0.0.0` to be reachable over Tailscale.
- Test real speed + latency once (Tailscale relay vs P2P direct matters for token streaming) before committing tasks.

## Setup sequence with the user (manual per-task control)
When the user wants to run tasks by hand first rather than auto-route:
1. Confirm the remote GPU machine's reachability + open endpoint (Step 0-1 above).
2. Get IP + whether Ollama/llama.cpp/vLLM is already running there.
3. B1: set up the model server on the remote. B2: test one light call over LAN/Tailscale for real speed. B3: create `model_aliases` (`local-qwen` / `api-pro`). B4: assign per-job model. B5: scale to remaining jobs only after the first runs well.

See `references/quang-machines.md` for Quang's specific machine topology.

## Diagnosing "input tokens too high" (200k+ per request)

When the user reports input tokens are huge (every request ~200k), DO NOT guess. Two real root causes, in order: (1) `compression.enabled: false` in config.yaml → never compresses session history, so long sessions (300-400 messages) resend the ENTIRE history each turn; fix = `hermes config set compression.enabled true` (threshold 0.5, target 0.2, protect_last_n 20). (2) sessions never reset — `history=290-380` in agent.log is the tell; correct remedy is compression + /new + STATE files, NEVER summary-of-summary (loses detail, hallucinates). Working query code for monthly request/token stats + top fat sessions from `state.db` (ACTIVE copy is on C:, the D: junction copy is stale pre-10/08): see `references/diagnose-input-token-bloat.md`.