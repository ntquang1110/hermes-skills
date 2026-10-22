# Research Queue Processor — Full Cron Job Worked Example

This reference documents the cron job from session 2026-07-16 that processes a research queue, falls back to auto-selected topics, and imports knowledge cards via a local API. Use it as a template for similar queue-processing cron jobs.

## Workflow

```
Bước 1: GET /api/research-queue → check for pending items
  ├─ Has pending → PATCH to "researching" → research → create card → POST card → PATCH done
  └─ Empty/None pending → Step 2

Bước 2: Check recent completed queue items to avoid topic repetition
  → GET /api/research-queue → list all items, identify last N completed topics
  → Pick from rotation (chan-nuoi, sinh-hoc, nghien-cuu) — do NOT repeat a topic recently done

Bước 3: Web research (see web-research skill)
  → Wikipedia REST API for background/summaries (always works)
  → PubMed E-utilities for peer-reviewed literature (never blocked)
  → Paced searches with time.sleep(2) between queries

Bước 4: Write card (markdown, ~1000-2000 chars)
  → Vietnamese with full diacritics
  → Title with emoji + angle
  → Summary + structured content (tables, blockquotes, bullets)
  → Tags derived from content

Bước 5: POST /api/knowledge (Authorization: Bearer hermes-knowledge-secret)

Bước 6 (if queue item): PATCH /api/research-queue {id: "<queue-item-id>", status: "done", card_id: "<card-id>"}
```

## Cron-specific Adaptations

Since this runs in cron mode (`execute_code` blocked):

| Need | Cron-safe approach | Preferred? |
|------|-------------------|------------|
| Execute Python logic | `python -c "..."` (inline — try first; may work) | ✅ Try first |
| Execute Node.js logic | `node -e "..."` (inline — same risk as `python -c`) | ⚠️ May be blocked |
| Fallback if inline blocked (Python) | Write `.py` file → `python script.py` | Use if inline fails |
| Fallback if inline blocked (Node) | Write `.js` file → `node "C:/path/to/script.js"` | Use if inline fails |
| HTTP GET API calls | `curl -sL --max-time 15 URL` | ✅ |
| HTTP POST API calls | `write_file` JSON payload → `curl -d @C:/path/payload.json -X POST URL` | ✅ |
| Parse JSON response + print (Python) | `curl ... -o data.json` → `read_file(data.json)` or write `.py` script | ⚠️ `python -c` pipe often blocked in cron mode |
| Complex data processing | Write `.py` file with full logic → `python file.py` | ✅ For multi-step |
| Clean up temp files | `rm -f /d/tmp/file.py` (avoid `/tmp/` which maps to root on git-bash) | ⚠️ Use `/d/tmp/` |

## Path Strategy (Windows git-bash)

```bash
# Shell operations (git-bash sees /tmp as C:\Users\<USER>\AppData\Local\Temp)
curl -sL http://localhost:3003/api/cards > /tmp/data.json   # OK for shell

# Python operations (Windows Python can't see /tmp)
# Save to D:/tmp/ instead:
write_file(path="D:/tmp/script.py", content=...)
terminal(command="python D:/tmp/script.py")
```

## API Endpoints Used

| Endpoint | Method | Purpose | Notes |
|----------|--------|---------|-------|
| `/api/research-queue` | GET | List all queue items (including status + card_id) | ⚠️ `?status=pending` query param does NOT filter — returns all items regardless |
| `/api/research-queue` | PATCH | Update queue item status + card_id | For queue-driven mode |
| `/api/knowledge` | POST | Create new knowledge card | Requires `Authorization: Bearer hermes-knowledge-secret` |
| `/api/knowledge` | GET | ❌ **405 Method Not Allowed** — do not use for listing | Next.js SPA, not a REST endpoint |

## Key Data Shapes

### Queue item
```json
{
  "id": "abc123",
  "topic": "Topic name",
  "detail": "Detail description",
  "topic_slug": "chan-nuoi",
  "status": "pending|researching|done",
  "card_id": "uuid"  // populated after import
}
```

### Knowledge card POST body
```json
{
  "title": "🐷 Title with emoji",
  "summary": "1-2 sentence summary",
  "content": "## Header\n\nMarkdown content... (1000-2000 chars)",
  "topic_slug": "chan-nuoi",
  "tags": ["chan-nuoi", "research", "..."],
  "source_url": "https://en.wikipedia.org/wiki/..."  // ← Always include if available
}
```

## Research Strategy (for Vietnamese topics)

See the `web-research` skill for full methodology. Key points:

1. **DDG Lite** — works for most queries. Pace with `time.sleep(2)` every ~3 searches to avoid silent rate limiting.
2. **Wikipedia REST API** — always works. Use for background science/medicine/technology.
3. **Direct article fetch** — hit or miss. Vietnamese news sites use Cloudflare. Try the article URL, but expect partial content.
4. **Query language** — Vietnamese queries return better results for Vietnamese topics. English queries for global science.

## Topic Auto-selection (when queue empty)

**Rotation pool (defined by cron job config):** `chan-nuoi`, `sinh-hoc`, `nghien-cuu`

**Rule:** Select the next field in rotation that has NOT been covered recently. Check the queue history — if the last 2 items covered `sinh-hoc` and `nghien-cuu`, pick `chan-nuoi`.

**Avoid repetition:** Always check the 2-3 most recent completed queue items before deciding. Do NOT re-cover a topic already done in the last 2-3 ticks.

**Fallback:** If uncertain, pick the field furthest in time from its last coverage.

## KF Unreachable — Fallback Output (CRITICAL)

When the KF server at `localhost:3003` is unreachable (connection timeout, connection refused, or curl exit code 28), do **not** let the entire cron tick produce nothing. The research output is still valuable on its own.

### Detection at startup

Before investing time in research, quickly probe whether KF is reachable:

```bash
# Quick probe (3s timeout) — if this fails, KF is down
curl -sv --max-time 3 http://127.0.0.1:3003/ 2>&1 | head -5
```

- If the probe **hangs or times out** → KF is stuck (CLOSE_WAIT state). Decide: try recovery (see Server Recovery section below) or bypass KF entirely.
- If the probe returns **connection refused** → KF is not running. Skip the POST step.
- If the probe works but **research-queue or cards endpoint times out** → KF is alive but slow. Proceed with research; the POST might work after you're done.

### Fallback behavior

1. Attempt research normally (Wikipedia + PubMed — these are independent of KF).
2. If KF POST to `/api/knowledge` fails (timeout after 5+ seconds, or curl exit 28/7):
   - **DO NOT** fail the whole cron tick
   - **DO** produce the research output directly as the cron response (inline markdown with full citations)
   - The user gets the research value even without the KB entry
3. If a research queue item was pending and KF is down:
   - Don't mark it as "done" — the card wasn't created
   - Report in the output: "Queue item [topic] — KF not available, research done but card not persisted"
   - The item stays pending for the next cron tick

### Key principle

```
KF is a delivery mechanism, not the research itself.
Research value exists independently of whether you can POST to KF.
If KF is down → deliver inline output.
If KF is up → POST as usual.
Never let a KF outage produce [SILENT] when there's real research done.
```

## Server Recovery: Stuck Next.js API on Windows

The local API server (`http://localhost:3003`) can accumulate **CLOSE_WAIT** TCP connections over time and stop responding — the TCP handshake succeeds but the server never replies. This manifests as `curl` operations timing out with exit code 28 even though `netstat` shows the port in LISTENING state.

### Detection

```bash
# Check if port responds at all
curl -sv --max-time 10 http://127.0.0.1:3003/   # Hangs → server is stuck

# Find the process
netstat -ano | grep "3003.*LISTEN"
# → PID shown with many CLOSE_WAIT connections

# Confirm it's your process
wmic process where processid=PID get name,commandline
# → C:\Program Files\nodejs\node.exe ... next dev or next start
```

### Recovery steps

```bash
# 1. Kill the stuck process (MSYS-safe)
cmd.exe /c "taskkill /F /PID $STUCK_PID"

# 2. Check for production build
ls "$USERPROFILE/knowledge-flow/.next"   # If no .next dir → use dev mode
ls "$USERPROFILE/knowledge-flow/.next"   # If .next exists → use start mode

# 3. Restart the server
# No production build (dev mode):
cd "$USERPROFILE/knowledge-flow" && npx next dev -p 3003

# With production build:
cd "$USERPROFILE/knowledge-flow" && npx next start -p 3003
```

### Why this happens

The Next.js dev server opens a new connection per API call (to Supabase, etc.). Under rapid cron firing or sustained uptime, connections accumulate in CLOSE_WAIT state (the remote peer closed but the local server hasn't fully released). Eventually the process hits the limit and stops processing new requests — they connect but never get a response.

### Prevention

- Use `next start` (production mode) instead of `next dev` if a production build exists — fewer connections, more stable
- Current 2-hour tick cadence should be adequate; the issue may arise from the server running continuously for days
- If the pattern persists, add a health-check heartbeat to the cron job that detects and auto-recovers
