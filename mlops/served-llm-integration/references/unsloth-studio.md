# Unsloth Studio — serving & control-plane notes

Unsloth Studio is a desktop app that wraps `llama-server` and exposes an
OpenAI-compatible endpoint, normally reached through a Cloudflare tunnel. Two
generations of deployment have been seen:

| Deployment | URL shape | Stability |
|---|---|---|
| Throwaway quick tunnel | `https://<slug>.trycloudflare.com` | dies when the process stops |
| Named tunnel | `https://<name>.<domain>` (e.g. `pharma-llm.thefirstonly.com`) | durable, survives restarts |

Auth: `Authorization: Bearer sk-unsloth-<key>`. `GET /v1/models` needs the key —
without it you get `{"error":{"message":"Not authenticated",...}}`.

### Do not guess where the origin box is — a named tunnel hides it

A named tunnel is an **outbound** connection *from* the origin host to
Cloudflare. Nothing about the public URL tells you which machine is behind it,
and the origin is frequently a box on a different network from the one you are
sitting on.

**Do not infer the origin from a port you find open on a machine you can reach.**
Real mistake made once: a Studio-like service was found listening on
`18888` on a LAN machine, and the endpoint was assumed to be that machine — it
was not. The two were unrelated; the endpoint was a separate Windows box on a
separate network. Everything built on that assumption had to be thrown away,
plus a needless detour through the wrong host's SSH.

Ask the endpoint where it lives instead of guessing:

| Signal | What it tells you |
|---|---|
| `GET /api/system` → `platform`, `cpu_count`, `gpu` | the real origin OS, CPU, GPU, VRAM |
| the `llama-server output` block in a failed `POST /v1/load` | full **server-side log path**, which leaks the origin's username and drive layout (e.g. `C:\Users\<user>\.unsloth\studio\logs\...`) |

There is generally no SSH into the origin, so treat everything as
API-only: you can load/unload/poll but not inspect the filesystem. Say so
rather than planning work that needs shell access.

---

## 1. The control plane exists — use it instead of guessing

**Unsloth Studio exposes a full FastAPI management API alongside the
OpenAI-compatible one.** It is documented, and the spec is the source of truth:

```
GET /openapi.json     -> full spec   (seen: 516 endpoints)
GET /docs             -> Swagger UI
GET /redoc            -> ReDoc
```

Do not hand-roll load/switch logic from inference responses. Read the spec:

```python
import json, urllib.request
spec = json.load(urllib.request.urlopen(BASE + "/openapi.json"))
for p, ops in spec["paths"].items():
    if any(k in p.lower() for k in ("load", "unload", "model", "serve")):
        print(p, [m.upper() for m in ops])
```

Note `/openapi.json` intermittently times out through Cloudflare — retry once
before concluding it is absent. `/api/openapi.json` and `/docs/openapi.json` are
404; the spec lives at the root only.

### Endpoints worth knowing

| Endpoint | Method | Purpose |
|---|---|---|
| `/v1/load` | POST | Load (or switch to) a model |
| `/v1/load-progress` | GET | `phase` / `bytes_loaded` / `bytes_total` / `fraction` |
| `/v1/unload` | POST | Unload a model — **body required**, see below |
| `/api/inference/loaded-models` | GET | What is actually resident |
| `/api/system` | GET | Host CPU / RAM / GPU + VRAM, live |
| `/api/health` | GET | Backend version, `desktop_manageability_version` |
| `/api/settings/model-memory` | GET/PUT | `keep_resident`, `no_ram_reserve` |
| `/api/models/gguf-variants` | GET | Available quants + sizes (`?repo_id=`, **not** `model_name`) |
| `/props` | GET | llama.cpp native: loaded alias, ftype, slots, ctx, `is_sleeping` |
| `/slots`, `/metrics` | GET | llama.cpp native slot list and Prometheus metrics |

`/api/system` is the fastest way to learn what the box actually is — RAM, GPU
model, VRAM free, and CPU count, all live:

```json
{"platform": "Windows-11-10.0.26200-SP0", "cpu_count": 20,
 "memory": {"total_gb": 31.75, "available_gb": 16.22, "percent_used": 48.9},
 "gpu": {"devices": [{"name": "NVIDIA GeForce GTX 1660 SUPER",
                      "memory_total_gb": 6.0, "vram_used_gb": 4.56,
                      "vram_free_gb": 1.44, "gpu_utilization_pct": 0.0}]}}
```

Cross-check with `/props` before trusting `/v1/models` about what is loaded —
`/props` reports `model_alias` from llama.cpp itself. In one session
`/v1/models` and the process list disagreed about which model was live.

---

## 2. `POST /v1/load` — the parameters that actually matter

The body is `LoadRequest`. The full field list is long; these are the ones that
change behaviour:

| Field | Default | Effect |
|---|---|---|
| `model_path` | — | Repo id or path |
| `gguf_variant` | — | **Which quant to load.** Omit it and you get whatever the server picks — not necessarily what was loaded before (see §5) |
| `gpu_memory_mode` | `auto` | `auto` = Studio picks GPUs and **caps context to fit VRAM**. `manual` = **you own the offload** |
| `gpu_layers` | `-1` | Layers on GPU. **Ignored unless `gpu_memory_mode: "manual"`** |
| `load_mode` | `auto` | `mmap` forces memory-mapping; **`mlock` keeps the model in RAM rather than letting it swap or compress** |
| `cpu_fallback` | `false` | Allow CPU-only execution |
| `n_cpu_moe` | `0` | CPU-resident MoE expert layers |
| `max_seq_length` | `0` | Context to allocate (0 = model default) |
| `n_batch` / `n_ubatch` | — | Batch sizes; smaller = less peak RAM during prefill |
| `cache_type_kv` | — | KV cache dtype: `f16`, `bf16`, `q8_0`, `q4_0`, `q4_1`, `q5_0`, `q5_1`, `iq4_nl`, `f32` |
| `speculative_type` | — | `auto` / `none` / `dflash` / `mtp` / ngram |
| `engine` | `auto` | `auto` / `vllm` / `sglang` |
| `engine_precision` | `auto` | `auto` / `bf16` / `fp16` / `int4` / `int8` / `fp8` |
| `force_reload` | `false` | Reload even if already resident |
| `disable_vision` | `false` | Drop the vision projector (saves memory) |
| `alongside` / `force_alongside` | `false` | Load *in addition to* the current model instead of replacing |
| `llama_extra_args` | — | Escape hatch for raw llama.cpp flags |

### The trap: `gpu_memory_mode` silently overrides `gpu_layers`

Passing `gpu_layers: 0` (the intuitive way to say "CPU only, use system RAM")
has **no effect** while `gpu_memory_mode` is at its default `auto`. Observed side
by side on the same model:

```
gpu_memory_mode unset (auto) + gpu_layers: 0  ->  "offloaded 6/6 layers to GPU"
gpu_memory_mode: "manual"    + gpu_layers: 0  ->  "offloaded 0/6 layers to GPU"
```

So the "force everything into RAM" request is:

```json
{
  "model_path": "<repo>",
  "gpu_memory_mode": "manual",
  "gpu_layers": 0,
  "cpu_fallback": true,
  "load_mode": "mlock",
  "max_seq_length": 16384,
  "load_in_4bit": false,
  "disable_vision": true
}
```

`load_mode: "mlock"` is what the API describes as *"keeps the model in RAM
rather than letting it swap or compress"* — that is the real "pin it in RAM"
switch. Pair it with `keep_resident` (§3) if you want it to stay put.

### Loads are async — trigger, then poll

`POST /v1/load` may return before the model is up. Poll `/api/inference/loaded-models`
or `/v1/load-progress`. Caveat: `/v1/load-progress` returns
`{"phase": null, "bytes_loaded": 0, "bytes_total": 0, "fraction": 0.0}` both
while idle *and* while a load is stuck — an all-zero progress reading is **not**
proof that loading is progressing. `loaded-models` is the reliable signal.

**`POST /v1/load` can hang for minutes without ever returning.** Observed: one
call sat for 345 s with an idle server behind it (loaded-models empty, no load in
progress, VRAM free). Killing it and re-issuing the same load via `curl` worked
immediately. Do not treat a hung load call as "the server is busy" — check
`/api/inference/loaded-models`, and if the server is idle, kill and retry.

---

## 3. Keeping a model resident

```
GET  /api/settings/model-memory
PUT  /api/settings/model-memory   {"keep_resident": true, "no_ram_reserve": true}
```

Response fields: `keep_resident`, `no_ram_reserve`, `default_keep_resident`,
`default_no_ram_reserve`, `mlock_active`, `mlock_applicable`,
`reload_required`, `memlock_limit_bytes`.

`no_ram_reserve: true` lets the model consume available RAM rather than holding
a reserve back. Both settings persist server-side, so **leave a note in your
reply about anything you flip** — the next person reading the box has no other
way to know the defaults were changed.

---

## 4. A failed load — response shape and the log to read

A load that fails returns **HTTP 500** wrapped as a deferred error, and the body
carries the llama-server stderr inline:

```json
{"_deferred_error": {"status_code": 500,
 "detail": "Failed to load model: llama-server failed to start. Check that the GGUF file is valid and you have enough memory.\n\nllama-server output:\n<stderr tail>"}}
```

Read `detail` before doing anything else — it usually names the cause outright.
The message also carries the full server-side log path, e.g.

```
C:\Users\<user>\.unsloth\studio\logs\llama-server\llama-<epoch>-port-<port>-try0.log
```

The generic text "check that the GGUF file is valid and you have enough memory"
is misleading boilerplate: it is printed for *every* startup failure, including
ones that have nothing to do with memory.

### Architectural load failures are not memory problems

Worst case observed — a GGUF whose architecture the bundled llama.cpp build
cannot instantiate. Four different configurations (all-auto; `speculative_type:
none` + mmap; `speculative_type: none` + 20 GPU layers; `gpu_memory_mode:
manual` + `gpu_layers: 0`) produced the **identical** failure:

```
E llama_init_from_model: failed to initialize the context:
    dflash requires ctx_other to be set (this warning is normal during memory fitting)
E cmn  common_init_: failed to create context with model '...\dflash2-qwen38-27b-Q8_0.gguf'
E srv    load_model: failed to create_context with model '...'
E srv  llama_server: exiting due to model loading error
```

Recognise this shape: the error is raised at **context creation**, before any
weights are placed, and it is identical across every memory configuration. That
means the RAM/VRAM/offload knobs are irrelevant — the model file demands a
feature (`ctx_other`, a companion context for its DFlash2 speculative decoder)
that the server cannot supply. Say so and stop; do not keep re-tuning memory.

**Sanity-check the artefact before blaming the knobs.** In the same episode the
failing file was a self-described 27B quantised at Q2 that reported a **1.95 GB**
buffer and only **6 layers** — a real 27B at Q2 needs roughly 9–15 GB and dozens
of layers. Files like this are pruned or partially downloaded. A repo whose
`display_name` advertises a size its own tensor layout contradicts is not
trustworthy; prefer the upstream publisher's build of the same model.

---

## 5. Unloading is destructive to an empty server — restore deliberately

`POST /v1/unload` takes an `UnloadRequest` body. **An empty body returns HTTP
400.** Include `model_path`, and `force_cancel_active: true` if chats may be
decoding:

```json
{"model_path": "unsloth/Ministral-3-3B-Reasoning-2512-GGUF", "force_cancel_active": true}
```

**Hazard:** if the server holds exactly one model and you unload it to make room
for something that then fails to load, you have left the endpoint with **zero
models** — every subsequent request 404s. That is a self-inflicted outage on
someone else's machine. Before unloading, capture the current state so you can
put it back:

```
GET /api/inference/loaded-models     -> record id + quant + context
GET /api/models/gguf-variants?repo_id=<repo>   -> available quant filenames
```

### Restoring the *same* quant requires `gguf_variant`

Reloading by repo name alone does **not** guarantee the quant you had. Observed:
a repo previously resident as `Q8_0` / context 8192 came back from a bare
`{"model_path": ...}` load as **`UD-Q4_K_XL` / context 10496** — a different
quant and a different context. Pass the variant explicitly:

```json
{"model_path": "<repo>", "gguf_variant": "Q8_0", "load_in_4bit": false}
```

Restored output confirmed the original state, `quant: Q8_0`, `context_length:
8192`. Always re-read `/api/inference/loaded-models` afterwards and **verify the
quant matches what you recorded**, then send one real generation to prove the
model actually serves — `loaded: true` alone does not prove it decodes.

---

## 6. Context length: trust the fitted number, not the headline

`/v1/models` entries carry four different context fields, and the largest is the
least useful:

```json
{"quant": "Q8_0", "loaded": true,
 "context_length":           262144,   <- what /props may report as n_ctx
 "max_context_length":         8192,   <- what actually fits
 "vram_fit_context_length":    8192,   <- what fits given current VRAM
 "native_context_length":   262144}    <- the model's design maximum
```

A model advertising 262144 could be served at an effective **8192**. Size your
prompts and `max_seq_length` against `max_context_length` /
`vram_fit_context_length`. Quoting the headline figure when describing
capability is a real accuracy error.

`gpu_memory_mode: "auto"` is what caps context to fit VRAM — that is the
mechanism behind the gap between `native_context_length` and
`vram_fit_context_length`.

---

## 7. Inference behaviour measured on this deployment

- **A request for a model that is not loaded returns a bare `HTTP 404`**, not the
  descriptive `model_not_found` JSON seen on earlier builds. A 404 on
  `/v1/chat/completions` with a correct-looking model id means *not loaded* —
  check `/api/inference/loaded-models` before suspecting the name. Do not
  conclude the name is wrong and start editing it.
- **`stream: true` is mandatory through the tunnel.** Non-streaming calls to a
  slow model hit **HTTP 524** when the whole body exceeds Cloudflare's ~100 s
  budget. `max_tokens: 2500` reproducibly 524'd on a model that streamed fine.
  At ~14 tok/s the practical non-streaming ceiling is roughly 1400 tokens.
- **`<think>` blocks are not separated.** `reasoning_tokens: 0` in `usage`, and
  the chain-of-thought arrives inside `message.content` wrapped in
  `<think>...</think>`. A client that does not split on `<｜end▁of▁thinking｜>` shows raw
  chain-of-thought to the user. Split it yourself:
  `answer = buf.split("<｜end▁of▁thinking｜>")[-1].strip()`.
- **Reasoning models can fail to terminate.** Bounded `max_tokens` produces
  `finish_reason: length` with the entire budget spent inside `<think>` and no
  answer emitted. Worse, the failure is **non-deterministic**: the same trivial
  comparison prompt ran 189 s and burned 4000 tokens without answering on one
  attempt, then answered correctly in 46 s on the next. Temperature influences
  it. Any integration needs a token budget generous enough to escape the think
  block *and* a fallback for the non-terminating case.
- **Low quant + reasoning compounds.** Q2 mangles Vietnamese homophones
  ("Kiềm→Kiêm", "gia cầm→giá cam", "bò→bô"). Q4 is the floor for Vietnamese
  content. A small reasoning model also got a unit conversion wrong by 1000×
  ("9000 tấn" for 9000 kg) at temp 0.6 while getting it right at temp 0.3 —
  measure at the temperature you intend to ship.
- **Throughput is set by whether the quant FITS IN VRAM — not by the model or
  the box.** This is the single biggest lever, and it is worth 5×. Measured on
  one GTX 1660 SUPER / 6 GB box, same 3B model, same prompts, same server:

  | Variant | Weights | Placement | Throughput |
  |---|---|---|---|
  | `Q8_0` | ~4.5 GB | **CPU** — does not fit | 9–21 tok/s |
  | `UD-Q4_K_XL` | ~2 GB | **GPU** (`vram_used_gb: 4.64` of 6) | 57–88 tok/s |

  So "a 3B model on a 6 GB card will not run GPU-resident" is **wrong** — it
  depends entirely on the quant. Do not reach for the smaller quant assuming a
  pure quality-for-size trade: above a floor, the smaller quant is *faster by a
  factor of five* because it changes which processor runs the model. Pull
  `vram_used_gb` from `/api/system` after loading to confirm which path you got
  — GPU-resident shows several GB of VRAM in use, a CPU fallback shows near
  zero. Benchmark the variant you intend to ship, not the model name.
- **Small reasoning models are hypersensitive to prompt wording AND to diacritics
  — a "clarification" can turn a passing prompt into an empty reply.** Measured
  on the same model, minutes apart:

  | Prompt | Result |
  |---|---|
  | Short: "120 con lợn, mỗi con ăn 2,5 kg/ngày, 30 ngày, bao nhiêu tấn?" | ✅ **"9 tấn"**, 6.2 s |
  | Same + "Biết 1 tấn = 1000 kg. Trả lời ngắn gọn." | ❌ 2000 tokens burned, **EMPTY** |

  Adding a unit-conversion hint *broke* it. With **unaccented** Vietnamese the
  same model answered a compare-these-two-numbers question by **adding** them
  ("The sum of 9.11 and 9.9 is 19.01"), produced an empty reply on the
  comma-decimal form, and answered a pig-gut pH question about **"a large water
  body"** — a hallucinated context. Re-run with full diacritics and the
  comparison came back correct ("9,9 là số lớn hơn 9,11").

  Consequences for a test protocol: (a) always prompt with **real diacritics**,
  never a stripped-ASCII stand-in, or you are measuring your own typo; (b) test
  the *shipped* wording, not a cleaned-up version of it; (c) a pass on one
  phrasing is not a pass — vary it. Reasoning models also drift to English on a
  Vietnamese question (a Vietnamese livestock question came back in English).

## Remote GPU path (the alternative that avoids the tunnel)

- Size the quant against **VRAM, not model class**. A 1660 Super / 6 GB machine
  cannot run 27B Q4 (~16 GB needed). Working rule of thumb from measurements on
  this box: ~3B Q4 (2 GB) and 7–8B Q4 (~5 GB) fit and run GPU-resident; a 3B at
  Q8 (4.5 GB) does not fit once the KV cache is counted and silently falls back
  to CPU, costing ~5× throughput. Leave ~1.5 GB of VRAM headroom for the KV
  cache — a 4.5 GB file on a 6 GB card looks like it fits and does not.
- Preferred durable route: Ollama (or llama.cpp) bound to `0.0.0.0:11434` on the
  GPU machine, called over LAN/Tailscale → `custom` provider in Hermes. Tailscale
  CGNAT IPs (100.x) need the service bound to all interfaces, not localhost.
