# LLM Router Landscape (surveyed 25/09/2026)

Four projects the community groups under "router". They solve different problems, so picking the wrong one optimises the wrong layer.

## Quick comparison

| | **jeff** | **RouteLLM** | **LLMRouter** | **vllm semantic-router** |
|---|---|---|---|---|
| Stars | 238 | 5,541 | 2,967 | 5,911 |
| Nature | One 400M classifier before the LLM | Framework for strong-vs-weak binary routing | Library to **train** routers (19 built-in) | Serving-layer routing for Mixture-of-Models |
| Stack | Python + encoder on CPU | Python + LiteLLM + FastAPI | Python + PyTorch + Longformer | **Go + Envoy ExtProc** |
| Decision method | Classify: choice / score / noul | Predicted strong-model win rate vs cost threshold | Query embedding to classifier to model name | Signals, Projections, Decisions, Algorithms (declarative YAML) |
| Needs training | No | No pretrained reuse for new pairs | **Yes**: (query, model, quality, cost) data | No, YAML policy |
| Windows native | Yes | Yes | Yes | **No**, WSL2 + Docker only |
| Best asset | `noul` removes calls entirely | Cost-threshold calibration | 19 algorithms + plugin system | Semantic cache + safety + 60 providers |

## RouteLLM (lm-sys, paper arXiv 2406.18665)

Every router implements one method: `calculate_strong_win_rate(prompt) -> float in [0,1]`. Above threshold, call the strong model; below, the weak one. Integration is a model-name swap: `router-mf-0.11593`.

Router options, and which are usable locally:

| Router | Size | Runs on CPU | Needs external API at inference |
|---|---|---|---|
| `mf` (matrix factorisation, recommended) | ~205K params | Yes | **Yes**, OpenAI `text-embedding-3-small` per prompt |
| `bert` (BERT-base, 3 labels) | ~110M | Yes | No, fully offline |
| `sw_ranking` (similarity-weighted Elo) | heavy, regression per request | Yes but very slow | Yes, OpenAI embeddings |
| `causal_llm` (Llama-3-8B) | 8B | **No**, hardcoded `.to("cuda")` | No |

For a CPU-only or offline box, `bert` is the only fully local option. Reported results: up to 85% cost reduction while holding 95% of GPT-4 quality on MT-Bench; >40% cheaper than commercial routers. Threshold must be recalibrated on your own query distribution.

Known limits: routes on the last message only, and routers were trained on first-turn data.

## LLMRouter (ulab-uiuc, paper arXiv 2608.06867)

A training and benchmarking library, not a serving layer. Pipeline: collect data to train classifier to pick model to benchmark. 19 routers across 5 groups (single-round 13, multi-round 1, multimodal 1, personalised 2, agentic 2), plus a plugin system that discovers from `./custom_routers/`, `~/.llmrouter/plugins/`, or `$LLMROUTER_PLUGINS`.

Its most immediately useful piece is `openclaw_router`: a lightweight OpenAI-compatible FastAPI gateway on port 8000 with 5 strategies (rules, random, round_robin, llm, llmrouter), Contriever routing memory on CPU, media understanding, and API-key isolation. Good as a gateway while a heavier solution is evaluated.

The ML routers themselves require training data and have no semantic cache or safety layer, so keep them out of a hot path.

## vllm semantic-router

A Mixture-of-Models serving layer behind Envoy. Five declarative stages: Signals (heuristic and learned), Projections, Decisions, Algorithms, model pool. Algorithms: static, router_dc, latency_aware, multi_factor, hybrid supported; several experimental. Loopers add cascade, ratings, remom, fusion, workflows. 60+ provider catalog including DeepSeek, Groq, Gemini, Ollama, vLLM, LM Studio.

Published benchmarks, the strongest evidence in this space:
- "When to Reason" (arXiv 2510.08731): +10.2 points MMLU-Pro, **-47.1% latency, -48.5% tokens** vs direct vLLM inference
- Category-aware semantic caching (arXiv 2510.26835): miss cost 30 ms to 2 ms, break-even hit rate 15-20% down to 3-5%

Catch: not native on Windows. Needs WSL2 or Docker, plus Envoy and Go, and several algorithms are still experimental.

## Adoption order that follows from the above

1. **Deterministic and cache tier first.** Rules, content-keyed caches, templates, lower cron frequency. Zero cost, zero latency, no risk, and on a cron-heavy system this is where the tokens actually are.
2. **Only if still needed:** a local classifier. RouteLLM `bert` (110M, offline) is the realistic candidate. Test on your own language before trusting it.
3. **When scale justifies it:** `openclaw_router` as a light gateway, then semantic-router under WSL2 for semantic cache and safety.
4. **Do not** self-host jeff/GLiFormer on CPU-only hardware: slower than the API call it is meant to avoid, 17-20x the per-token cost, and English-only.

## Reusable evaluation lesson

When a project is trending, check whether its headline win is measured on the same kind of hardware you have. jeff's cheap-CPU claim evaporates on CPU and only holds on a GPU L4. The repo's own docs said so plainly; the community summaries did not.
