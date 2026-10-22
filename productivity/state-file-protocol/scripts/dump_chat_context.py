"""Đọc context của 1 chat từ state.db — dump messages gần nhất để tổng hợp state file.
Usage: python dump_chat_context.py <chat_id>
Path: C:/Users/NTQUANG_DELL/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe
"""
import sqlite3, sys

CHAT_ID = sys.argv[1] if len(sys.argv) > 1 else ''
DB = r'C:\Users\NTQUANG_DELL\AppData\Local\hermes\state.db'

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("""
SELECT id, started_at, ended_at, title, message_count, display_name, chat_type, chat_id, model,
       end_reason, last_activity_description
FROM sessions
WHERE chat_id = ?
ORDER BY started_at DESC
LIMIT 12
""", (CHAT_ID,))
sessions = cur.fetchall()

print(f"=== CHAT {CHAT_ID} — {len(sessions)} sessions gần nhất ===")
for s in sessions:
    print(f"SESSION {s['id']} | {s['started_at']} | msgs={s['message_count']} | title={s['title']} | end={s['end_reason']}")

if not sessions:
    print("NO SESSIONS")
    sys.exit(0)

target = None
for s in sessions:
    cur.execute("SELECT COUNT(*) FROM messages WHERE session_id=?", (s['id'],))
    if cur.fetchone()[0] > 0:
        target = s['id']
        break

print(f"\n=== MESSAGES session {target} (user+assistant, truncate 300) ===")
cur.execute("""
SELECT role, content, timestamp, tool_name
FROM messages
WHERE session_id=? AND role IN ('user','assistant')
ORDER BY id
LIMIT 120
""", (target,))
for m in cur.fetchall():
    c = (m['content'] or '').strip()
    if len(c) > 300:
        c = c[:300] + '…'
    c = c.replace('\n', ' ⏎ ')
    print(f"[{m['role']}] {c}")
