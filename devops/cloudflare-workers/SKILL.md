---
name: cloudflare-workers
description: "Deploy Cloudflare Workers on Windows: scripts, KV, secrets."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cloudflare, workers, kv, wrangler, deploy, edge, dns, routes]
    related_skills: [cloudflare-tunnel, publish]
---

# Cloudflare Workers Deployment

Deploy and manage Cloudflare Workers (scripts, KV, secrets, custom domains) from a Windows host via `wrangler`. Distinct from `cloudflare-tunnel` (that is tunnels, this is Workers).

## When to Use

- Deploying/updating a Worker (`wrangler deploy`)
- Creating KV namespaces, binding them, setting secrets
- Wiring a custom domain or route to a Worker
- Building a Worker that serves/stores content (e.g. an HTML preview proxy)

## Wrangler v4 syntax (diffs from v3 — the v3 forms fail)

- `wrangler kv namespace create NAME` — the old `wrangler kv:namespace create NAME` is gone in v4 ("Unknown arguments").
- `wrangler secret name` — subcommands live under `wrangler secret` (list/put); see `wrangler --help`.
- `npx --yes wrangler deploy --config wrangler.toml` — deploy with account env vars set.

## wrangler.toml

```toml
name = "my-worker"
main = "src/worker.js"
compatibility_date = "2025-04-01"
workers_dev = true

# Custom domain route — requires the zone on the SAME Cloudflare account
routes = [
  { pattern = "preview.example.com/*", zone_id = "<zone_id>" }
]

# KV namespace binding
[[kv_namespaces]]
binding = "MY_STORE"
id = "<namespace_id>"
```

## KV gotchas

- **`expirationTtl: 0` is INVALID.** `STORE.put(k, v, { expirationTtl: 0 })` throws *"Invalid expiration_ttl of 0. Please specify integer greater than 0."* For permanent keys **omit the options argument**: `await STORE.put(k, v)`.
- KV bindings surface on `env` (`env.MY_STORE`), not as globals.

## Secrets

- In source, read via `env`: `async fetch(request, env)` → `const X = env.SECRET_NAME`. A bare global `GITHUB_PAT` stays `undefined` and auth silently drops (→ 429 from GitHub).
- Set: `echo "$VAL" | wrangler secret put NAME` (pipe the value; the interactive prompt hangs in non-TTY).
- The Cloudflare REST secret-create endpoint returns `405 Method not allowed` for a Workers-scoped token — prefer `wrangler secret put`.

## Custom domain wiring

1. Ensure the zone (`example.com`) is on the same CF account (get `zone_id` via `GET /zones?name=...`).
2. Add `routes = [{ pattern = "subdomain.example.com/*", zone_id = "..." }]` to wrangler.toml, deploy.
3. Also add a DNS CNAME record `subdomain :=> <worker>.<subdomain>.workers.dev`, **proxied** (orange cloud) — a bare Workers token may not have DNS edit permission; do this in the dashboard or with a DNS-scoped token.

## Build patterns worth reusing

- **Serve raw GitHub content as HTML:** GitHub raw URLs serve `text/plain` even for `.html`. A Worker can fetch then re-serve with `Content-Type: text/html`. Gist raw URLs REQUIRE the username: `gist.githubusercontent.com/{user}/{gist_id}/raw/{file}` (omit user → 404). Pair a `GITHUB_PAT` secret to dodge egress 429s.
- **KV direct-store + serve (no external storage):** `POST /api/store` accepts `{content}`, `PUT(randId, content)`, returns `{id, preview_url}`; `GET /<id>` reads KV first (`STORE.get`), falls through to upstream if null. Add an `X-Source` header (`kv` vs `gist`) for debugging. `Cache-Control: public, max-age=3600`.
- Random IDs: standard `crypto.getRandomValues` exists, but `Math.random()` over a 36-char alphabet is simpler and sufficient for short ids. Avoid `import from 'node:crypto'` (not available in Workers).

## Workers AI Binding (env.AI)

Workers AI runs models on Cloudflare's GPUs via `env.AI.run(model, input)`. Key findings:

**Temporary accounts (`wrangler deploy --temporary`)** — only a subset of models are available. All text-generation LLMs (`@cf/meta/llama-*`, `@cf/google/gemma-*`, `@cf/mistral/*`, `@cf/deepseek-*`, `@cf/zai-org/glm-*`, `@cf/moonshotai/kimi-*`, `@cf/nvidia/nemotron-*`, `@cf/openai/gpt-oss-*`) return:
- `5028: deprecated` for older model aliases
- `5034: not available to temporary accounts. Add a payment method` for current models

**Models that DO work on temporary accounts** (from catalog scan):
- Embeddings: `@cf/baai/bge-small-en-v1.5`, `@cf/baai/bge-base-en-v1.5`, `@cf/baai/bge-large-en-v1.5`, `@cf/baai/bge-m3`, `@cf/google/embeddinggemma-300m`
- Classification: `@cf/huggingface/distilbert-sst-2-int8`
- Translation: `@cf/meta/m2m100-1.2b`, `@cf/ai4bharat/indictrans2-en-indic-1b`
- Image gen: `@cf/black-forest-labs/flux-1-schnell`, `flux-2-dev`, `flux-2-klein-4b/9b`, `@cf/bytedance/stable-diffusion-xl-lightning`, `@cf/lykon/dreamshaper-8-lcm`, `@cf/leonardo/phoenix-1.0`
- STT/TTS: `@cf/deepgram/nova-3`, `@cf/deepgram/aura-*`, `@cf/myshell-ai/melotts`
- Vision: `@cf/moondream/moondream3.1-9b-a2b`, `@cf/llava-hf/llava-1.5-7b-hf`, `@cf/facebook/detr-resnet-50`
- Other: `@cf/microsoft/phi-2` (deprecated), `@cf/pfnet/plamo-embedding-1b`

**Model alias resolution** — Cloudflare internally rewrites some model names (e.g. `@cf/meta/llama-3.1-8b-instruct` → `@cf/meta/infire-llama-3.1-8b-instruct`). Use explicit variant suffixes (`-fp8`, `-fast`, `-awq`) when possible to avoid deprecated paths.

**Input formats** supported:
- Completion: `{ prompt: "..." }`
- Chat: `{ messages: [{role, content}, ...] }`

**Debugging AI errors — `wrangler tail`:** when curl/Python `requests` returns only `error code: 1101` (500) with no detail, the real exception is invisible from the client. Run `npx wrangler tail --temporary` in background, hit the endpoint, then read the log — it shows `AiError` stack with the exact cause (90% of the time: `5028: deprecated model` or `5034: not available to temporary accounts`). This is the fastest way to tell "model alias resolved to a deprecated variant" from "model needs billing".

**Temporary-account URL churn:** each `wrangler deploy --temporary` may (re)create a temp account, so the `*.workers.dev` subdomain can CHANGE between deploys (e.g. first deploy → `xxx.sulfuric-distance.workers.dev`, later → `yyy.candle-music.workers.dev`, then "reused" on subsequent deploys). Always curl the URL printed by the CURRENT deploy — don't hardcode a URL from an earlier run, and don't reuse the old subdomain when testing after redeploy.

## Common Pitfalls (Windows)

1. **curl from git-bash fails TLS against workers.dev** (schannel `SEC_E_ILLEGAL_MESSAGE`). Test the Worker with Python `requests`, not curl.
2. **Python path resolution** — git-bash `/c/...` paths are not understood by Python; pass `C:\\...` or use `os.path` joins.
3. Register the `workers.dev` subdomain once in the dashboard before first `workers_dev = true` deploy; otherwise deploy errors "you need to register a workers.dev subdomain".
4. **Workers AI on temporary accounts** — text generation models require a paid account. Use embedding/classification/image models for free-tier testing, or `wrangler login` with a billing-enabled account.

## Verification Checklist

- [ ] `wrangler deploy` reports the new version id and the route/workers.dev URL
- [ ] Custom domain returns 200 with correct `Content-Type` (Python requests)
- [ ] KV store + read-back works (POST /api/store then GET returns stored content)
- [ ] Secrets visible to Worker (auth header sent, no silent 429/unauthorized)
- [ ] DNS CNAME proxied and propagates

## Related Skills

- `cloudflare-tunnel` — exposing localhost via Cloudflare; different mechanism (tunnels vs Workers)
- `publish` — the content-publish umbrella that uses a Worker+KV preview backend (see its worker source + wrangler.toml for a concrete example)