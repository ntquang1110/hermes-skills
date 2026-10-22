# KF Large-KB & PubMed Reliability Pitfalls (tested Jul 2026)

Session-derived pitfalls from the "Research sâu" cron run on a 212-card Knowledge Flow (~3MB cards dump) + porcine Siglec/PRRSV PubMed research.

## ⚠️ KF API behind passcode gate — EVERY call needs the `tfo_auth` cookie (Aug 2026)

The Knowledge Flow app (3003) now runs the web-passcode-gate (see `web-passcode-gate` skill). The Next.js proxy matcher `/((?!_next/static|_next/image|favicon.ico).*)` protects **ALL** routes including `/api/*` — `/api/research-queue`, `/api/cards`, `/api/knowledge` all return `307 /passcode?next=%2Fapi%2F...` when called without the auth cookie. This breaks every pattern in the skill (Pattern 0/A/B/C/D, Step 0 queue check, dedup scans, POST /api/knowledge).

**Symptoms:**
- `curl` prints `/passcode?next=%2Fapi%2Fknowledge` (or empty + non-zero parse downstream)
- Python `urllib` Pattern D raises `HTTP Error 307: /passcode?next=%2Fapi%2Fknowledge`
- Piping the redirect body into `python -c "json.load(sys.stdin)"` → `JSONDecodeError` (it's HTML, not JSON)

**Fix — add the cookie to EVERY request (Authorization Bearer alone is NOT enough):**
```bash
# curl
curl -s -b "tfo_auth=1d1e977a218bfa01fe61106c360c8acf667047e35f17fdb0f1a8484e06cfdb55" http://localhost:3003/api/cards ...
```
```python
# Python Pattern D — add to headers dict
headers = {
    "Authorization": "Bearer hermes-knowledge-secret",
    "Content-Type": "application/json",
    "Cookie": "tfo_auth=1d1e977a218bfa01fe61106c360c8acf667047e35f17fdb0f1a8484e06cfdb55",
}
```
The hash is `sha256` of the machine-wide passcode `<PASSCODE>`. If the passcode changes, recompute: `python -c "import hashlib; print(hashlib.sha256(b'<passcode>').hexdigest())"`. Verify the gate once per run: `curl -s http://localhost:3003/api/research-queue` should return JSON array, not `/passcode?...`.

## `/api/cards` times out on large KFs — fetch in background

**Symptom:** foreground `curl -s --max-time 55 "http://localhost:3003/api/cards"` returns `HTTP 000`, exit 28 (operation timed out), 0 bytes — while `/api/research-queue` and `/api/health` respond instantly. The cards dump endpoint is slow (3MB JSON takes ~4 min at 212 cards), not dead. Retrying in foreground 3x just wastes 3×55s.

**Fix (background fetch + continue working):**
```bash
# background=true + notify_on_complete=true, long timeout
curl -s --max-time 240 "http://localhost:3003/api/cards" -o C:/Users/<user>/hermes-temp/cards.json \
  -w "cards: HTTP %{http_code}, size %{size_download}\n"
```
While it runs, do the independent work: check `/api/research-queue`, run PubMed topic-probe searches, browse recent sessions for dedup. Then `process(action='wait')` and parse the file with Python (`json.load` → enumerate titles). One fetch covers both queue-check and dedup.

**⚠️ Background-fetch file may vanish from `/tmp`:** a file written by a background curl to `/tmp/cards_raw.txt` can be invisible to a later Python process (`FileNotFoundError`), or visible once then gone — MSYS bash `/tmp` and native Python `/tmp` resolve differently and temp files get cleaned. Always `-o` to an explicit Windows path (`C:/Users/<user>/hermes-temp/...`) when the file will be consumed by a later tool call.

## NCBI E-utilities `RemoteDisconnected` on rapid calls

**Symptom:** after ~8–10 back-to-back `esearch` calls, NCBI forcibly closes the connection:
```
http.client.RemoteDisconnected: Remote end closed connection without response
```
This is NOT a 429 — it's a connection reset. The skill's 429 guidance doesn't cover it.

**Fix — retry wrapper with backoff, applied to EVERY E-utilities call:**
```python
def fetch(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=25)
            return resp.read().decode('utf-8', errors='replace')
        except Exception as e:
            wait = 5 * (i + 1)
            time.sleep(wait)
    return None
```
Also pace query groups with `time.sleep(3)` between searches (not just 1–1.5s). With backoff+3s pacing, all calls recovered.

## Topic-selection probe — `esearch` count before committing

When the research queue is empty and you must self-select a topic, probe 8–12 candidate queries first and let the literature depth decide:
```python
def esearch_count(query):
    url = ('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term='
           + urllib.parse.quote(query) + '&retmax=0&retmode=json')
    ...  # return esearchresult.count
# candidates = [('name', 'term AND (swine OR porcine OR pig)'), ...]
```
Jul 2026 example: Siglecs (135), galectins (135), MUC2 (176) were rich; viperin (11), OAS/RNaseL (8), T3/thyroid (8) were thin. Combined with the KF content-mention scan (below) this picks a gap topic that ALSO has enough literature.

## Ghost-topic scan — count content mentions, not just titles

Title-only dedup misses ghost topics. Scan the `content` field of every card for candidate keywords — topics referenced in many cards but with zero title hits are prime gap candidates:

```python
kws = ['siglec', 'cd169', 'galectin', 'sialic', 'lectin']
for kw in kws:
    titles = [c['title'] for c in cards if kw.lower() in c['title'].lower()]
    mentions = sum(1 for c in cards if kw in (c.get('content') or '').lower())
    print(f'{kw}: {len(titles)} title hits, {mentions} content mentions')
```
Jul 2026 result: `siglec: 0 title hits, 5 content mentions` → Siglec/CD169 card was a genuine gap (CD169 = PRRSV entry receptor, referenced in the PRRSV card but never independently covered).

## f-string backslash SyntaxError in card→HTML scripts

`SyntaxError: f-string expression part cannot include a backslash` — happens when a regex with a backslash sits inside an f-string expression:
```python
# BROKEN:
html.append(f'<div class="list-item num">{inline(re.sub(r"^\d+\.\s", "", stripped))}</div>')
# FIX — extract to a variable first:
item_text = re.sub(r'^\d+\.\s', '', stripped)
html.append(f'<div class="list-item num">{inline(item_text)}</div>')
```

## Reusable card→HTML converter

`scripts/kf_md_to_html.py` (in this skill) converts a KF card payload JSON (`{title, content, tags, summary}`) into the Premium B/W/Y single-file HTML used by the delivery pipeline — headings, tables, blockquotes, code blocks, bold, lists. Reuse it instead of hand-writing a converter each run:
```bash
python scripts/kf_md_to_html.py payload.json siglec_card.html
# then POST the HTML to https://preview.thefirstonly.com/api/store via curl -d @payload.json
```

## OVERVIEW JSON block breaks single-quoted Python strings (Aug 2026)

The mandatory `<!--OVERVIEW-->{"what":"...","why":"...","mechanism":[...]}<!--/OVERVIEW-->` block is conventionally built as a single-quoted Python string (`overview = '<!--OVERVIEW-->{"what":"..."}...'`). Any apostrophe inside a field value (e.g. `'máy đóng dấu ubiquitin'`, `Peyer's patches`) terminates the string early → `SyntaxError: invalid syntax` pointing at a confusing column deep in the line.

**Fix:** build the overview as a triple-quoted string (`overview = """<!--OVERVIEW-->..."""`), strip apostrophes from field text, or construct the dict natively and `json.dumps(ensure_ascii=False)` it. The main content triple-quote block is immune to this.

## Reading-time overshoot is not undoable (Aug 2026)

The KF API exposes only POST `/api/knowledge` and GET `/api/cards` — **no PATCH/PUT/DELETE on cards**. If the POST response's `reading_time_sec` exceeds the 300–900s target, the card is already ingested and cannot be trimmed in place (removal requires Supabase REST, see `kf-duplicate-card-removal.md`).

Calibration observed 2026-08: ~19 000 chars of markdown ≈ 1200s; aim ~12–14k chars to stay ≤900s. Decide length BEFORE posting; never re-POST a second copy to "fix" length — that creates a duplicate card.
