# KF Unreachable — Research Output Fallback

Use this when the Knowledge Flow server at `localhost:3003` is unreachable during a research cron job. The research output is valuable independently of whether you can POST to KF.

## Detection

```bash
# Quick probe — 3s timeout
curl -sv --max-time 3 http://127.0.0.1:3003/ 2>&1 | head -5
```

| Probe result | Meaning | Action |
|-------------|---------|--------|
| Hangs / times out (exit 28) | KF stuck in CLOSE_WAIT state or overloaded | Attempt research anyway; try POST at end |
| Connection refused (exit 7) | KF not running | Skip POST entirely |
| Responds but slow | KF alive but slow | Proceed normally |

## Fallback rule

```
THỢT NGHIÊN CỨU ≠ KHẢ NĂNG POST
Nếu nghiên cứu ra kết quả → deliver cho user dù KF có đang hoạt động hay không.
Không để KF chết làm mất giá trị research.
```

**When KF POST fails:**
1. Research normally (Wikipedia + PubMed — independent of KF)
2. If POST to `/api/knowledge` fails (timeout after 5s, exit 28, exit 7):
   - **DO** produce output directly as cron response (inline markdown + citations)
   - **DO NOT** fail the whole cron tick
   - **DO NOT** output [SILENT] when there's real research done
3. If a research queue item was pending:
   - Don't mark as "done" (card wasn't created)
   - Report: "Queue item [topic] — KF unavailable, card not persisted"
   - Item stays pending for next tick

## See also

- `cron-job` skill → `references/research-queue-processor.md` → "KF Unreachable — Fallback Output" section for server recovery steps
- `web-research` skill → "Knowledge Flow card creation pipeline" section for normal KF workflow
