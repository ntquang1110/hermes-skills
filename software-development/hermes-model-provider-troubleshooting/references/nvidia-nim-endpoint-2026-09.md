# NVIDIA NIM free endpoint (`integrate.api.nvidia.com`) — probe results (2026-09-25)

OpenAI-compatible, key format `nvapi-...`. Verified end to end from Windows via the `openai` SDK
and raw `urllib`. Useful as a **free fallback / experiment tier**, not as a production provider —
the constraint that decides it is a shared concurrency pool, see below.

## What works

- `GET /v1/models` → **82 models**.
- `POST /v1/chat/completions` → HTTP 200, first token ~1 s.
- Streaming: yes, standard SSE. Parse `chunk.choices[0].delta`.
- **Thinking/reasoning**: pass `extra_body={"chat_template_kwargs": {"enable_thinking": True}}`, then
  read `delta.reasoning_content` alongside `delta.content`. Both stream; the reasoning arrives first.
  Non-stream responses carry `message.reasoning_content` too.
- Models seen: `nvidia/nemotron-3-ultra-550b-a55b`, `nemotron-3-super-120b-a12b`,
  `nemotron-3-nano-omni-30b-a3b-reasoning`, `nemotron-3.5-lightning-30b-a3b`, `nemotron-3-embed-1b`,
  `nemotron-3.5-content-safety`, `deepseek-ai/deepseek-v4.1-flash`, `openai/gpt-oss-20b`, plus
  mistralai/llama families.

## THE constraint — shared free-tier worker pool (HTTP 503)

```
HTTP 503 {"error":{"message":"ResourceExhausted: Worker local total request limit reached (16/16)",
                   "type":"Service Unavailable","code":503}}
```

- 16 concurrent workers, **shared across the free tier** — not per-key. It saturates after only a
  handful of requests, and once saturated **every** request 503s (measured: 0/12 succeeded while blocked).
- **It is retryable and self-heals**: after waiting 90-120 s, 6/6 requests succeeded again. Two
  consecutive post-wait batches ran clean.
- Operational rule: treat 503 as `retry with backoff (60-120 s)`, never as "key dead" and never as
  a config fault. This is exactly the class of failure that makes it unusable for cron jobs — a job
  that fires on a schedule cannot wait out an arbitrary shared-pool saturation.
- Being sequential does not protect you: the pool is shared with other free-tier users, so a clean
  0-in-flight script still 503s.

## Measured model speeds (Vietnamese + English prompts, Windows host)

| Model | Speed | Note |
|---|---|---|
| `nemotron-3-nano-omni-30b-a3b-reasoning` | **116 tok/s** | fastest; clean short Vietnamese |
| `nemotron-3-ultra-550b-a55b` | 70 tok/s | strongest; produced a correct AABBA limerick |
| `nemotron-3-super-120b-a12b` | 68 tok/s | **leaks English reasoning into `content`** |
| `nemotron-3.5-lightning-30b-a3b` | 9 tok/s | slowest in this sample |
| `deepseek-ai/deepseek-v4.1-flash` | **14 tok/s** | slowest, but most reliable Vietnamese |

## Vietnamese capability — prompt-dependent, test before trusting

Same models, two prompt styles:

- **Unambiguous prompt** ("1 con heo nặng 100kg, 20 con nặng bao nhiêu?" → 2000 kg): **all three
  tested models answered correctly**.
- **Loose/ambiguous prompt** ("phân biệt phân bón hữu cơ và vô cơ"): **all three nemotron models
  failed** — one answered about the verb *phân biệt* vs *phản biện*, one reinterpreted it as a
  Vietnamese-grammar question and replied in English, one answered in English about "organic parts".
  Only `deepseek-ai/deepseek-v4.1-flash` gave the right answer, in correct Vietnamese with diacritics.

Conclusion: nemotron is weak on natural, loosely-worded Vietnamese; it degrades to surface keyword
matching. `deepseek-v4.1-flash` is the safer Vietnamese choice here but is ~8x slower.

Related: `nemotron-3-super-120b` returned its chain of thought inside the `content` field
("Okay, let's see. The problem says: ... translating that from Vietnamese"). If you use it, strip or
guard against reasoning text leaking into user-visible output — the same class of issue as the
reasoning-inflation pitfall for local models.

## Wiring notes

- Treat it like any OpenAI-compatible custom endpoint — see the parent skill's sections on
  `custom_providers` vs the `model:provider` block. Nothing NIM-specific is required beyond
  `base_url: https://integrate.api.nvidia.com/v1` + the `nvapi-` key.
- If wiring as a Hermes fallback, remember it is best-effort: a 503 here will cascade to the next
  fallback, which is acceptable for a *last* fallback and bad for a primary.
- `deepseek-ai/deepseek-v4.1-flash` is present here, which makes NIM a plausible free substitute when
  the BytePlus/Ark DeepSeek quota is exhausted (see the BytePlus rate-limit reference) — with the
  caveat that it is slow and the pool saturates.

## Key hygiene when handing over test scripts

The key arrives pasted into chat. Do **not** leave it hardcoded in generated probe scripts — those
files persist on disk. Replace the literal with an env lookup and tell the user to rotate:

```python
KEY = __import__("os").environ["NVIDIA_API_KEY"]
```

Then verify the scripts still run with the var exported, and grep the working directory for the
literal to confirm nothing was missed. Also state plainly that a key pasted into a chat log is
already exposed and should be rotated if it is a real account key.
