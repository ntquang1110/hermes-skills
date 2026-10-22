# LLM router / pre-LLM classifier landscape (researched 2026-09-25)

Four repos get lumped together as "LLM routers" but solve four different problems. Picking the
wrong one means optimising the wrong layer. Clone targets + measured numbers below.

## The four, by nature

| Repo | Stars | Nature | Decision mechanism | Needs training? |
|---|---|---|---|---|
| `logan-markewich/jeff` | 238 | Self-hosted impl of TypeSafe **jev System One**; a ~400M encoder (GLiFormer) sitting *before* the LLM | Multi-label sigmoid over label groups. Three question types: `choice` (pick one), `score` (graded scale), `noul` (P(yes)) | No (zero-shot) |
| `lm-sys/RouteLLM` | 5.5k | Framework to **train + serve binary strong-vs-weak** routing | Every router implements one method: `calculate_strong_win_rate(prompt) -> [0,1]`; `>= threshold` → strong, else weak | Needs preference data; pretrained ckpts exist |
| `ulab-uiuc/LLMRouter` | 2.9k | **Training library + benchmark** (19 routers, 5 groups: single-round / multi-round / multimodal / personalized / agentic) + plugin system | Query → Longformer embedding → classifier → `model_name` | **Yes** — needs `query, model, quality, cost` rows |
| `vllm-project/semantic-router` | 5.9k | **Serving-layer router** for Mixture-of-Models (Go 1.25 + Envoy ExtProc) | Declarative YAML: Signals → Projections → Decisions → Algorithms → model pool | No (policy is config) |

RouteLLM's routers: `mf` (matrix factorization, ~205K params, **needs an OpenAI embedding call per prompt**), `bert` (BERT-base, ~110M, **fully local CPU, no network**), `causal_llm` (Llama-3-8B, **hardcoded `.to("cuda")` — will not run on CPU without patching**), `sw_ranking` (Elo MLE over 55k Arena battles — accurate, far too slow for production).

## Published benchmarks worth quoting

- RouteLLM: up to **85% cost cut** while holding **95% of GPT-4** on MT-Bench; vs commercial routers it matched Unify's 8.7579 score using **25.4%** GPT-4 calls (Unify used 45.6%) and matched Martian at **29.7%** (Martian ~50%). Default calibrated threshold for `mf` is **0.11593** ≈ 50% strong calls.
- semantic-router: **-48.5% tokens, -47.1% latency, +10.2 pt MMLU-Pro** (arXiv 2510.08731); category-aware semantic cache cut miss cost 30 ms → 2 ms.
- jeff vs hosted jev: JevBench v1.2.2 score **66.9 (#9)** vs **75.3 (#2)**; hard tier **37.7%** vs **74.1%**. jeff only wins on the Cost axis and on `temporal_numeric`.
- **The repo's own conclusion on the CPU arm: "the CPU arm is not a cheaper tier."** Per token, CPU was **17-20x more expensive** than jev's list price. GPU L4 was **5x cheaper** than jev. Batching barely helps on CPU (~20% from bs=1→16).

## Measured on the local box (i7-4910MQ Haswell, 15.9 GB, torch CPU fp32)

jeff's GLiFormer on CPU: 400M = 823 ms @77 tok, 9.5 s @797 tok, 20.8 s load, **11.2 GB peak RSS**;
base 150M = 411 ms / 621 ms per 3-question request. Full detail in the parent SKILL.md step 9.

GLiClass multilingual `knowledgator/gliclass-multilang-ultra` (2.5 GB, a *different* model from jeff's
GLiFormer): load **994 s**, **3.7-9.0 s per single classification** on the same box, and it emitted
`Missing key(s) ... encoder.embed_tokens.weight` — the checkpoint is mis-packaged, which degrades it further.

## The two blockers that actually decide it

1. **No Vietnamese.** GLiFormer's HF card is tagged `en` only. GLiClass multilang covers 20 languages
   (**en, sv, cs, pl, lt, et, lv, es, fi, de, fr, ro, it, pt, nl, uk, hi, zh, ar, he**) — **Vietnamese is
   not among them**. RouteLLM's `bert` router is English-trained too. Measured on 5 Vietnamese routing
   prompts: 3/5 correct on multi-label, but the binary "needs a big LLM vs short answer" test returned
   the WRONG label at **0.134** confidence. It keys on surface words, not semantics. Any Vietnamese use
   case requires relabelling + fine-tuning first.
2. **Latency exceeds what it replaces.** A sub-second-to-9-second local classifier in front of an LLM
   call adds to total latency rather than reducing it, when a small hosted model answers in 0.3-0.8 s.

## Recommendation shape that survived scrutiny

Tier the work and put the free layer first — the savings live in determinism and caching, not in a small model:

- **Tier 0 — deterministic + cache, 0 tokens.** Pattern rules, existing helper calls, content-hash cache
  keys, response templates. Blocks an estimated 20-30% of calls at zero cost and zero risk. **This is
  where the money actually is** for a system burning tokens on recurring cron jobs.
- **Tier 1 — classification, only if Tier 0 leaves headroom.** RouteLLM's `bert` (~110M, fully local, no
  API key). Verify Vietnamese before trusting it.
- **Tier 2 — gateway with caching + safety.** `openclaw_router` (from LLMRouter) is the light
  OpenAI-compatible option to stand up now; `semantic-router` is the real token-saving win but is
  **not native Windows** — needs WSL2 + Docker + Envoy.
- **Tier 3 — periodic offline measurement.** Run LLMRouter over your own logs to learn which router
  helps on your traffic, then distil the finding back into Tier 0 rules.

Do **not** self-host jeff/GLiFormer on a CPU-only Windows box: slower than the API call it replaces,
17-20x more expensive per token, and blind to Vietnamese.
