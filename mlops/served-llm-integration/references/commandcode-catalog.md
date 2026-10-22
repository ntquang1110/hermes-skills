# Command Code (`api.commandcode.ai`) — catalog survey

OpenAI-compatible aggregator. Base URL for Hermes provider config:

```
https://api.commandcode.ai/provider/v1
```

Key lives in `.env` as `HERMES_CUSTOM_COMMAND_CODE_API_KEY`. `GET /v1/models` returns **82 models** (verified 26/09/2026).

Docs: `https://commandcode.ai/docs/resources/pricing-limits`

## Free ($0) models — verified against the live API, not the docs

| Model ID (from `GET /v1/models`) | Context | Works? | Measured |
|---|---|---|---|
| `stealth/space-bunny-alpha` | **1M** | yes | 3.2 s |
| `poolside/laguna-s-2.1-free` | 256K | yes | 6.2 s |
| `inclusionai/ling-3.0-flash-sante:free` | 262K | yes | 2.0 s — **capped 100 req/day** |
| `stealth/pixel-canary` | 262K | **NO — 524** | upstream unavailable, every call |

All three working models answered a Vietnamese arithmetic prompt correctly with full diacritics.

**Docs were wrong twice** — always re-verify against `/v1/models`:

- Docs say `laguna-s-2.1-free`; live ID is **`poolside/laguna-s-2.1-free`** (note the provider prefix).
- Docs mark `stealth/pixel-canary` as FREE; it returns `524 Upstream model provider is temporarily unavailable` consistently. Do not put it in a fallback chain — it costs a full timeout per fallback attempt.

The docs page is a JS-rendered Next.js app (~795 KB HTML). `curl` plus a regex strip is enough to read the deal table; a headless browser is not required.

## Not-free models worth knowing

- `deepseek/deepseek-v4-flash`, `deepseek/deepseek-v4-flash-fast`, `deepseek/deepseek-v4-pro`, `deepseek/deepseek-v4.1-flash`
- `meta/muse-spark-1.1`, `-1.2`, `-1.2-contributor`, `-1.3`, `-1.3-contributor`
- `thinkingmachines/inkling`, `thinkingmachines/inkling-small`

## Pricing model (from the docs page)

Credit-based, **credits are denominated in money, not requests** — so the same credit buys fewer requests on expensive models. Structure:

- Monthly subscription credits reset each cycle; top-up credits roll over and never expire.
- Two rolling windows on included monthly credits: a **5-hour** and a **weekly** limit. These throttle only the included monthly pool; on-demand / top-up credits are never throttled and are spent first once a window is hit, so you are never hard-stopped.
- Peak-hour pricing exists on some models (DeepSeek noted as roughly half the requests during peak; peak never applies on weekends).
- Some models carry promos (e.g. "2x usage", "up to 99% off") that are time-boxed.

## Gotcha

`urllib.request` to this host returns **403 error 1010** with its default `Python-urllib/x.y` UA while `curl` passes with any UA. Set `User-Agent: openai-python/1.0`. See the 403 diagnostic section in the parent SKILL.md.
