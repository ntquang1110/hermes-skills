# Jeff/Jev Pattern Reference

## Repo

- **Jeff** (self-hosted): https://github.com/logan-markewich/jeff — MIT, 238★
- **TypeSafe Jev API** (cloud): https://docs.typesafe.ai/api
- **Model**: `knowledgator/gliformer-large-v1` (400M params) on HuggingFace
- **Multilingual sibling**: `knowledgator/gliclass-multilang-ultra` (2.5 GB, 20 languages, **no Vietnamese**)

## Origin of this thread

Quang heard about "Jeff" from internet buzz — described as "a gateway that sits before the LLM, decides routing, reduces hallucination and cost." The pattern matches, but the cost and latency framing in the buzz does not survive measurement. See `SKILL.md` → "Measured reality".

## Architecture

```
Input → classifier (400M params, CPU: ~1 s/query measured)
         ├── choice(list) → pick one option
         ├── score([levels]) → rate on scale
         └── noul() → probability of yes
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
    No LLM needed        LLM needed
    (route/classify)     (forward + context)
```

## Use case: multi-agent task routing

Corrected table (earlier revisions of this file claimed 5ms and 0 tokens, which was wrong):

| Aspect | Routing with the main LLM | Routing with a CPU classifier |
|---------------|--------------|--------------|
| Marginal token cost | ~15K tokens per route decision | 0 tokens, but 17-20x the per-token cost of the cloud API when amortised over CPU time |
| Latency | 2-5 s (model dependent) | ~1 s at 400M on this hardware; 10.97 s p95 on hard input |
| Hallucination risk in routing | present | lower, it is a classifier not a generator |
| Vietnamese support | yes | **no** for every off-the-shelf checkpoint tested |

The gate decision (`noul`) is the only mode that removes work rather than moving it.

## SDK

```python
pip install typesafe-sdk

from typesafe_sdk import Choice, Noul, Score, TypeSafeClient
client = TypeSafeClient(api_key="key", base_url="http://localhost:8000")
```

## Verify

```bash
curl http://localhost:8000/healthz
curl -H "Authorization: Bearer devkey" http://localhost:8000/v1/models
```

`/v1/models` requires auth and returns 401 without it, which is easy to misread as a broken server.

## Measured on Intel i7-4910MQ (25/09/2026)

| Case | Result |
|---|---|
| Model load, GLiClass multilang ultra (2.5 GB) | 994 s (16.5 min) |
| GLiClass inference, single Vietnamese prompt | 3.7 - 9.0 s |
| GLiFormer base 150M, torch fp32, 77 tokens | 411 ms |
| GLiFormer base, full `Engine.run` (3 questions) | 621 ms |
| GLiFormer large 400M, extrapolated | ~1.0-1.1 s short, ~11 s on 3-4k token state |

## Python version note

jeff pins `requires-python = ">=3.12,<3.13"`. Python 3.14 resolves and runs but triggers `torch.jit.script is not supported in Python 3.14+` from gliformer at import time. Use 3.12 via `uv python install 3.12`.
