# Cron Job Token Analysis — query patterns for state.db

When optimizing recurring token burn, don't guess which job is expensive. Query `state.db` for real numbers.

## Monthly summary table (all requests, all sources)

Script: `D:/ai-router-test/usage_final.py`

Produces clean monthly table with:
- Request count + avg/day
- Input + output tokens ("real tokens" — what providers bill on)
- Cache read tokens (separated — billed at ~10% of input, don't inflate the total)

Core query:
```python
rows = con.execute("""
    SELECT last_seen, api_call_count, input_tokens, output_tokens,
           cache_read_tokens
    FROM session_model_usage WHERE last_seen IS NOT NULL
""").fetchall()
months = {}
for ts, calls, inp, out, cr in rows:
    mk = datetime.fromtimestamp(ts, TZ).strftime("%Y-%m")
    m = months.setdefault(mk, {"req":0, "in":0, "out":0, "cr":0, "days":set()})
    m["req"] += calls or 0; m["in"] += inp or 0; m["out"] += out or 0
    m["cr"] += cr or 0
    m["days"].add(datetime.fromtimestamp(ts, TZ).date())
```

## Cron vs chat breakdown (first diagnostic step)

Cron sessions have a `cron` prefix in `session_id`:
```python
cron_rows = [r for r in all_rows if r.session_id.startswith("cron")]
chat_rows = [r for r in all_rows if not r.session_id.startswith("cron")]
```

Real data (94 days, 2026-06-25 → 2026-09-26): cron = **46.6%** of all real tokens (180M of 387M total).

## Group cron jobs by logical name

Cron titles have date suffixes like `· Sep 26 14:00`. Strip them:
```python
import re
CUT = re.compile(r"\s*[·•]\s*[A-Z][a-z]{2}\s+\d{1,2}.*$")
def job_name(title):
    return CUT.sub("", title).strip() if title else "cron"
```

Then group by `job_name`:
```python
jobs = defaultdict(lambda: {"req":0, "in":0, "out":0, "cr":0, "n":0, "days":set()})
for sid, calls, inp, out, cr, st, title in rows:
    k = job_name(title, sid)
    j = jobs[k]
    j["req"] += calls or 0; j["in"] += inp or 0; j["out"] += out or 0
    j["cr"] += cr or 0; j["n"] += 1
```

Real data (94 days): top 3 cron jobs by token burn:

| Job | Token | % of cron | Status |
|---|---|---|---|
| KFlow Push Tâm lý | 52.2M | 28.9% | PAUSED |
| knowledge-researcher-4h | 48.9M | 27.0% | 6→1/day |
| Auto Threads - Ministral | 11.5M | 6.3% | running |

## Cache read is cumulative per session (NOT a bug)

`cache_read_tokens` in `session_model_usage` is the TOTAL across all calls in that session row. One session: 691 calls × 262K context = 180M cache read. The number is real. It means **context is very long and read many times**, not that the DB is wrong.

Real ratio: cache read = **17x** real tokens (6.58B vs 387M over 94 days). This is normal when prefix caching is active — every call re-reads the cached system prompt + tool definitions.

## Reference scripts

- `D:/ai-router-test/usage_final.py` — monthly stats table, separates real vs cache
- `D:/ai-router-test/cron_group.py` — cron jobs grouped by name, sorted by token burn
- `D:/ai-router-test/cron_detail.py` — raw cron session list with per-run counts
- `D:/ai-router-test/find_waste.py` — find sessions with highest input/req ratio
- `D:/ai-router-test/usage_by_month.py` — extended version with model/provider breakdown
