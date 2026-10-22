---
name: llm-routing-classifier
description: "Use when routing with a pre-LLM classifier (Jeff/Jev pattern)."
---

# LLM Routing Classifier (Jeff/Jev Pattern)

Use a tiny, self-hosted classifier model **before** calling an expensive LLM. Handles structured decisions (routing, classification, scoring, yes/no gates) without burning tokens, so the LLM only fires when real generation is needed.

**Read the measured section before adopting.** The pattern is sound. The "free and instant on CPU" framing that circulates online is wrong on both counts, and no off-the-shelf checkpoint handles Vietnamese.

## When to use

- You have a multi-agent system and need to route incoming tasks to the right agent
- You want to classify user intent, tone, or urgency before deciding which LLM to call
- You need fast, cheap "gating" decisions (is this billing? is this urgent?)
- You're tired of paying 15K tokens to deepseek just to figure out where to route a message

## The Concept

```
Input → classifier (400M params, CPU: ~1s/query, not <100ms)
         ├── choice: pick one option → route to agent / category
         ├── score: rate on ordered scale → urgency, priority
         └── noul: probability of yes → gate check
                   │
                   ▼
         (no LLM needed) → process deterministically
         (LLM needed) → forward with enriched context
```

## What is Jeff/Jev

**Jeff** (github.com/logan-markewich/jeff, MIT, 238★) is a self-hosted implementation of TypeSafe's **Jev System One** API. It runs **GLiFormer** (400M parameters from HuggingFace `knowledgator/gliformer-large-v1`), a multi-label encoder. It does run on CPU, but not fast, and the upstream repo states outright that the CPU arm "is not a cheaper tier".

**Language limit:** GLiFormer is tagged `en` (English only). `knowledgator/gliclass-multilang-ultra` covers 20 languages and does not include Vietnamese. Treat both as English-only for routing until proven otherwise on your own text.

Three modes:

| Mode | What it does | Example |
|------|-------------|---------|
| **choice** | Pick one option from a list | Route: `["research", "sales", "dev", "ceo"]` |
| **score** | Rate on ordered levels | Urgency: `["low", "medium", "high"]` |
| **noul** | Probability of yes/no | Gate: `"Is this about billing?"` |

## Quickstart

```bash
git clone https://github.com/logan-markewich/jeff
cd jeff && uv sync --extra dev
uv run hf download knowledgator/gliformer-large-v1 --local-dir models/gliformer-large-v1
JEFF_API_KEYS=devkey uv run jeff  # http://localhost:8000
```

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient
client = TypeSafeClient(api_key="devkey", base_url="http://localhost:8000")
result = client.system_one(
    "Research EZ80 vs competitors",
    {"agent_route": Choice(instructions="Route to?", criteria={
        "research": "needs web research",
        "sales": "outreach or CRM",
        "dev": "code or deploy",
    })}
)
print(result.choices["agent_route"].choice)  # "research"
```

## Integration into Hermes Multi-Agent 2.0

```
User message → Jeff (localhost:8000, 5ms)
  → choice: agent_route (research|sales|dev|ceo)
  → score: urgency (low|medium|high)
  → noul: needs_llm (probability)
If needs_llm < 0.3 → gửi thẳng vào agent inbox (0 token)
If needs_llm >= 0.3 → forward LLM + enriched context
```

## Measured reality (read before adopting)

Numbers below come from the jeff repo's own benchmarks plus direct measurement on an i7-4910MQ laptop (2013 Haswell, 4C/8T, no GPU usable by modern torch):

| Claim seen online | What was measured |
|---|---|
| "<100ms on CPU" | **823 ms** for the 400M on a 77-token query, measured directly; 411 ms for the 150M base; **9.5 s** on a 797-token input |
| "free, ~0 tokens" | jeff's own docs: CPU costs **17-20x more per token** than the jev cloud API. Only a GPU L4 beats the API, at 5x cheaper |
| "~50 req/s" | repo's own CPU tier: 0.94 s p50, **10.97 s p95** on hard items, 4-thread Ryzen. Measured here: 1.2 texts/s at batch 1, 2.1 texts/s at batch 8 |
| "just start it" | 400M loads in 20.8 s with **11.2 GB peak RAM**; the `gliclass-multilang-ultra` checkpoint took 994 s (16.5 min) to load |

Full per-case numbers and the reproduction recipe: `references/cpu-benchmark-measurements.md`. That file also records which figures were extrapolated before being measured, so you can judge how much to trust the remaining estimates.

**Consequence:** on CPU-only hardware this tier makes every request both slower and more expensive than calling a small LLM API. Self-hosting wins on cost only with a GPU, and wins on privacy/independence when you have none.

## Cost comparison

| Scenario | Without classifier | With classifier (CPU) |
|----------|-------------------|----------------------|
| Route task | ~15K tokens on a cheap model | +1 s latency, no token saving |
| Classify | ~5K tokens | +1 s latency, no token saving |
| Gate (`noul`) | 1 LLM call | **genuinely removes the call** |

The `noul` gate is the one place this pattern pays for itself, because it eliminates a call rather than shrinking one.

## Deployment

| Platform | Command |
|----------|---------|
| Local CPU | `uv run jeff` |
| Modal L4 | `uv run modal deploy deploy/modal_gpu.py` |
| CPU/ONNX int8 | `PYTHONPATH=src python scripts/export_onnx.py <model-dir> --int8` then `JEFF_BACKEND=onnx JEFF_QUANT=int8 uv run jeff` |

The ONNX int8 export is verified working on CPU: 150M base exported `encoder.onnx` (736 MB) in 14.4 s with max abs parity vs torch of **2.48e-05** (repo asserts < 1e-3), then quantized to `encoder.int8.onnx` (645 MB) in 29.2 s, deliberately keeping 24 MatMuls in fp32. The export script needs `PYTHONPATH=src` when run directly, otherwise it dies with `ModuleNotFoundError: No module named 'jeff'` even though the checkout is complete — that error is an invocation problem, not a broken repo.

## Pitfalls

- **400M params = classification only, not generation.** Always pair with an LLM for text output.
- **Lower accuracy than the Jev cloud API** on hard reasoning. JevBench v1.2.2: jeff 66.9 (rank 9/18) vs jev 75.3 (rank 2). Hard tier 37.7% vs 74.1%.
- **No Vietnamese.** GLiFormer is English-only and the multilingual GLiClass checkpoint skips Vietnamese. On 5 Vietnamese routing prompts it scored 3 correct and failed the one that mattered (complex-vs-simple), at confidence 0.134, guessing from keywords.
- **CPU is not the cheap tier.** See measured section. Do not adopt this for cost reasons on CPU-only hardware.
- **No HTTPS by default.** Reverse proxy or Cloudflare Tunnel needed for production.
- **2.3 GB download** for the 400M checkpoint (1.05 GB for the base).
- **Verify a chunked download before you benchmark it.** `bench`/`fetch.sh`-style range downloaders concatenate `part.N` files; if the `cat` runs while the parallel writers are still finishing, you get a silently truncated checkpoint (seen: 309 MB assembled where 2.30 GB was expected) and `rm` then fails with "Device or resource busy". Check that the sum of part sizes equals the `content-length` you fetched first, reassemble only after every writer has exited, and assert the assembled byte count equals the expected length before loading. The parts are usually fine — only the assembly step is broken, so re-concatenating recovers a 2.3 GB model that looks like a failed download.
- **Pass a Windows path (or a HF repo id), never an MSYS path, to `from_pretrained`.** `gliformer.from_pretrained("/d/models/gliformer-large-v1")` raises `HFValidationError: Repo id must be in the form 'repo_name' or 'namespace/repo_name'`. Use `"D:/models/gliformer-large-v1"`.
- **`PYTHONPATH` from the Hermes venv leaks into your model venv** and breaks `import numpy` (`No module named 'numpy._core._multiarray_umath'`, cp311 binaries inside a 3.12 venv). Always `unset PYTHONPATH` before running a separate Python environment; when the repo uses a `src/` layout, set `PYTHONPATH=src` explicitly afterwards instead.
- **Working order matters:** build the deterministic and cache tier first (see below).

## Check the cheaper tier before adding a model

Any system burning tokens on a schedule has a bigger win available for free: deterministic rules, content-keyed caches, output templates, and lower cron frequency. Measure what that recovers before adding a model that taxes every single request.

## Related

- `model-cost-optimization` — broader LLM cost strategy
- `ai-team-orchestration` — multi-agent system to route to
- `served-llm-integration` — endpoint benchmarking
- `references/llm-router-landscape.md` — the four competing approaches (jeff, RouteLLM, LLMRouter, vllm semantic-router) compared with published benchmarks and adoption order
