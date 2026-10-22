#!/usr/bin/env python3
"""
KF auto-push scan helper: list recent sessions (incl. subagent) + KF cards for dedup.

Use inside the "Auto-push research to Knowledge Flow" cron (or any cron that must
find NEW research created in user sessions and push it to KF at localhost:3003).

Usage (cron mode — inline python -c is blocked):
    python "C:/Users/<user>/AppData/Local/hermes/skills/productivity/cron-job/scripts/kf_scan_recent_sessions.py" [days=2]

Outputs:
    1. Sessions in window from state.db (id, time, source, msg count, title).
    2. For subagent sessions (blank titles): first user message = task description.
    3. For knowledge-researcher sessions: whether push markers ("POST thành công"
       / "Card verified" / "Total:") exist in assistant messages.
    4. Recent KF cards from /api/cards (with passcode cookie) for keyword dedup.

Notes:
    - state.db is at ~/AppData/Local/hermes/state.db; messages table has NO
      created_at column — ORDER BY id is the stable ordering.
    - KF /api/cards needs Cookie tfo_auth=<sha256('<PASSCODE>')> (passcode gate).
    - Use the FULL session id when querying messages (ids get truncated on print).
"""
import os, sys, sqlite3, datetime, json, hashlib, urllib.request

DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 2
db = os.path.expanduser('~/AppData/Local/hermes/state.db')
start = (datetime.datetime.now() - datetime.timedelta(days=DAYS)).timestamp()
own_id_prefix = os.environ.get('HERMES_CRON_ID', '')
if not own_id_prefix:
    # fallback: infer current cron session prefix from state.db if present
    try:
        conn0 = sqlite3.connect(db)
        own_id_prefix = conn0.execute(
            "SELECT id FROM sessions WHERE source='cron' ORDER BY started_at DESC LIMIT 1"
        ).fetchone()[0][:20]
        conn0.close()
    except Exception:
        pass

conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute(
    "SELECT id, title, started_at, message_count, source FROM sessions "
    "WHERE started_at >= ? ORDER BY started_at DESC", (start,))
rows = cur.fetchall()
print(f'== Sessions {DAYS} ngay qua (total {len(rows)}) ==')
for r in rows:
    ts = datetime.datetime.fromtimestamp(r[2]).strftime('%m-%d %H:%M')
    print(f'{ts} | {r[4]:9s} | {r[3]:4d} msgs | {r[0][:26]} | {(r[1] or "")[:70]}')

print('\n== Subagent tasks (first user msg) ==')
for r in rows:
    if r[4] == 'subagent' and (not own_id_prefix or r[0][:20] != own_id_prefix):
        cur.execute("SELECT content FROM messages WHERE session_id=? AND role='user' "
                    "AND content IS NOT NULL AND length(content)>20 ORDER BY id LIMIT 1", (r[0],))
        u = cur.fetchone()
        if u:
            print(f'{r[0][:26]} :: {u[0][:140].replace(chr(10), " ")}')

print('\n== Knowledge-researcher push markers ==')
for r in rows:
    if 'knowledge-researcher' in (r[1] or ''):
        cur.execute("SELECT content FROM messages WHERE session_id=? AND role='assistant' "
                    "AND content IS NOT NULL AND length(content)>100 ORDER BY id", (r[0],))
        msgs = [m[0] for m in cur.fetchall()]
        markers = [kw for kw in ['POST thành công', 'Card verified', 'Card POST', 'Total:',
                                 'SUCCESS', 'Status: 201'] if any(kw in m for m in msgs)]
        died = 'OK' if markers else ('DIED-EARLY' if len(msgs) < 5 else 'NO-MARKER?')
        print(f'{datetime.datetime.fromtimestamp(r[2]).strftime("%m-%d %H:%M")} '
              f'| {died} | {len(msgs)} msgs | markers={markers}')
conn.close()

print(f'\n== KF cards (last {DAYS}d UTC, for keyword dedup) ==')
COOKIE = 'tfo_auth=' + hashlib.sha256(b'<PASSCODE>').hexdigest()
try:
    req = urllib.request.Request('http://localhost:3003/api/cards',
        headers={'Authorization': 'Bearer hermes-knowledge-secret', 'Cookie': COOKIE})
    cards = json.loads(urllib.request.urlopen(req, timeout=60).read())
    print(f'KF total: {len(cards)}')
    cutoff = (datetime.datetime.utcnow() - datetime.timedelta(days=DAYS)).strftime('%Y-%m-%d')
    for c in sorted([x for x in cards if (x.get('created_at') or '') >= cutoff],
                    key=lambda x: x.get('created_at', '')):
        print(f"{c.get('created_at','')[:16]} | {c.get('title','')[:90]}")
except Exception as e:
    print(f'KF fetch failed (server down?): {e}')
