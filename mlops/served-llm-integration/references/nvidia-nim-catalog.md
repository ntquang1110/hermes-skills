# NVIDIA NIM hosted catalog (`integrate.api.nvidia.com`) — survey 26/09/2026

Endpoint: `https://integrate.api.nvidia.com/v1`, OpenAI-compatible, key from build.nvidia.com.
Auth: `Authorization: Bearer nvapi-...`. Without it: 401 `Not authenticated`.

## Catalog

**82 models** via `GET /v1/models`. Notable families:

| Family | Models seen |
|---|---|
| nemotron-3 | `embed-1b`, `nano-omni-30b-a3b-reasoning`, `super-120b-a12b`, `ultra-550b-a55b`, `lightning-30b-a3b`, `3.5-content-safety` |
| deepseek | `deepseek-ai/deepseek-v4.1-flash`, `deepseek-ai/deepseek-coder-6.7b-instruct` |
| gpt-oss | `openai/gpt-oss-20b` |
| mistral | `mistralai/mistral-large`, `mistral-large-2-instruct`, `mistral-nemotron`, `mixtral-8x22b-v0.1`, `mistral-7b-instruct-v0.3`, `codestral-22b-instruct-v0.1` |

`deepseek-ai/deepseek-v4.1-flash` is worth noting when the user's own key runs
`deepseek-v4-flash`-class models — it is the same line available on the free hosted tier.

## Measured throughput (single short Vietnamese prompt, ~400 output tokens)

| Model | Total | tok/s | Vietnamese verdict |
|---|---|---|---|
| `nemotron-3-nano-omni-30b-a3b-reasoning` | 3.1 s | **116** | clean `content`, passed both prompts |
| `nemotron-3-ultra-550b-a55b` | — | **70** | strongest; limerick + reasoning stream fine |
| `nemotron-3-super-120b-a12b` | 5.9 s | 68 | **leaks English CoT into `content`** |
| `deepseek-ai/deepseek-v4.1-flash` | 19–28 s | **14** | most accurate Vietnamese, but slow |

Reasoning is exposed as `reasoning_content` on the delta, enabled with
`extra_body={"chat_template_kwargs": {"enable_thinking": True}}`. Verified streaming works.

## Limit behaviour

See SKILL.md section 5 for the full picture. Summary: 40 RPM nominal, ~29 req/min
practical, **shared global pool of 16 workers** (a 503 body read `1902/16` — the
numerator is other users' in-flight requests), ~15 s recovery, no upgrade path on the
free tier.

## Sources checked, with reliability

| Source | Value | Verdict |
|---|---|---|
| NVIDIA developer forum, moderator reply | 40 RPM, no upgrade on free tier, limit varies with model + use-case + traffic | **Authoritative** — quoted verbatim in SKILL.md |
| `forums.developer.nvidia.com/t/382934`, `/t/366043` | 1,000 signup credits, "40 RPM is already enough to test" community pushback | Corroborating, multiple users |
| `api-evangelist/nvidia-nim` rate-limits YAML | 5 concurrent, 4096 max output, 128k input, 60 s SSE idle | **Unverified** — cites `docs.api.nvidia.com/nim/reference/limits`, which returns **404** |
| `docs.api.nvidia.com` | — | Real site, but no public rate-limit page; JS-rendered, curl sees an empty shell |

Lesson: a third-party catalog citing a dead official URL should not be trusted for
numbers. Cross-check against the vendor forum before planning around a figure.

## Auth and key hygiene

Keys look like `nvapi-...`. They are free-tier and shared-pool, so treat the endpoint as
best-effort. Always read from an env var — never leave one in a probe script on disk
(see SKILL.md "Never leave a pasted key in test scripts").
