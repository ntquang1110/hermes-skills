# Batch API availability — what to check before recommending the discount

Findings from 26/09/2026, when asked "batch calls are cheaper, can we use it?" against the user's
BytePlus Ark primary (`https://ark.ap-southeast.bytepluses.com/api/coding/v3`) and Command Code.

**Bottom line:** the discount is real, but it does not apply to the model the user is running, and
an interactive agent loop could not use it anyway. Two independent reasons, either one sufficient.

## 1. The 200-with-empty-body trap

BytePlus `GET /batches` returned **HTTP 200 with `Content-Length: 0`**. Same host, same key, real
endpoint for comparison: `GET /models` → 200 with 27,995 bytes. A 200 proves a route is registered,
not that the API exists.

| Probe | Result |
|---|---|
| `GET /api/coding/v3/batches` | 200, **0 byte** |
| `GET /api/coding/v3/batch` | 200, 0 byte |
| `GET /api/coding/v3/models` | 200, 27,995 byte (real) |
| `GET /api/v3/batches` | 404 + `{"code":"PathNotFound"}` (genuinely absent) |
| `GET https://ark.cn-beijing.volces.com/api/v3/batches` | 401 (different region host) |

**Rule:** always diff a candidate endpoint's byte count against a known-good endpoint on the same
host before believing a status code.

## 2. The capability flag lives on the model, not the plan

`GET {base}/models` returns per-model features. BytePlus shape:

```json
{
  "id": "deepseek-r1-250120",
  "features": {
    "batch": { "batch_chat": true, "batch_job": true },
    "cache": { "prefix_cache": true, "session_cache": false },
    "structured_outputs": { "json_object": true, "json_schema": true }
  }
}
```

Measured on the user's own endpoint: **28 of 58 models** advertise `batch.batch_chat: true`. The 11
distinct ones were:

```
deepseek-r1-250120   deepseek-v3         skylark-pro         skylark-vision-250515
seed-1-6-flash       seed-1-6            seed-1-6-250915     kimi-k2-thinking-251104
glm-4-7-251222       seed-2-0-mini       seed-2-0-lite
```

**The user's active model `deepseek-v4-flash` was absent from the listing entirely** — not
"batch unsupported", simply not on that endpoint's catalogue. Same for `deepseek-v4-pro`. The only
DeepSeek models with batch were the older `deepseek-r1-250120` and `deepseek-v3`.

Enumerate the supported set and diff it against what the user actually runs, every time. Do not
assume a model family carries the capability across generations.

## 3. Where batch is retired, the migration target is service_tier

BytePlus docs, verbatim: *"Seed 2.1 and later models no longer support calling the Batch Chat API."*
The suggested migration is synchronous calls with `service_tier=flex`. Tested on the user's model:

```
POST /api/coding/v3/chat/completions  {"model": "deepseek-v4-flash", "service_tier": "flex"}
-> InvalidParameter.UnsupportedParameter:
   "The model version does not support service_tier=flex"
```

So both the old discount and the new discount are closed off for that model. Test the tier
parameter rather than inferring support from the docs.

## 4. The real endpoint, and why a REST probe misses it

BytePlus Batch API (chat): `POST https://ark.ap-southeast.bytepluses.com/api/v3/context/chat/completions`

The official Go SDK (`byteplus-sdk/byteplus-go-sdk-v2`, `api_create_batch_inference_job.go`) does
NOT use a REST path — it posts to `HTTPPath: "/"` with the action in the body:

```go
op := &request.Operation{
    Name:       opCreateBatchInferenceJobCommon,  // "CreateBatchInferenceJob"
    HTTPMethod: "POST",
    HTTPPath:   "/",
}
```

Consequence: probing OpenAI-shaped paths tells you nothing about whether the RPC-style batch API is
available. Confirm via the models catalogue flag, not by path guessing.

## 5. An agent loop structurally cannot use batch

Batch is: upload JSONL → create job → poll status → download output. Results arrive out of band, in
files, on a timescale of minutes to a day. A conversational turn that needs the answer to continue
has nowhere to put that. Building the plumbing (file staging, job registry, polling, result
injection) costs far more than the discount returns for interactive use.

**Batch fits:** scheduled bulk processing of a known corpus. **Not:** chat, agent loops, anything
where the next turn depends on the answer.

## 6. Check quota before proposing any cost optimisation

The same session surfaced, on the plain (non-batch) call path:

```
AccountQuotaExceeded: You have exceeded the weekly usage quota.
It will reset at 2026-09-28 00:00:00 +0800 CST.
```

A discount on a different API does nothing if the current model is simply out of quota. Order of
operations: confirm the primary model can serve at all → then optimise cost.

## 7. Prefix caching is the one that fits chat

`cache.prefix_cache: true` appears on several models in the same catalogue response. It discounts
repeated system prompts on **normal synchronous calls** — no file staging, no polling, works inside
an agent loop. For chat workloads this is the discount worth chasing, not batch.

Unverified for `/api/coding/v3` (quota was exhausted when this was written). Confirm the flag is
honoured on the plan in use before quoting any saving.

## Pre-flight checklist

1. Probe candidate batch paths; compare byte counts against `/models`.
2. `GET /models`; extract `features.batch`; diff against the models the user actually runs.
3. If excluded, test `service_tier=flex` (or the provider's successor tier) — don't assume.
4. Confirm the workload is batch-shaped (bulk corpus) and not an interactive turn.
5. `GET {base}/models` and check `cache.prefix_cache` as the chat-compatible alternative.
6. Make a plain call first to confirm quota is not already exhausted.
