#!/usr/bin/env python3
"""dump_remote_session.py — Xem THẬT một phiên Hermes đang dùng system prompt nào,
và bot đã trả lời gì.

Tại sao cần: Hermes ghim system prompt theo từng session (prompt cache). Sửa
SOUL.md / display.personality xong, phiên ĐANG tồn tại VẪN dùng prompt cũ —
restart gateway KHÔNG cứu được. Log chỉ nói
"response ready: ... response=47 chars", không cho biết nội dung. Script này tải
state.db rồi đọc thẳng bảng sessions / system_prompts / messages — bằng chứng duy
nhất đáng tin.

Dùng:
    python dump_remote_session.py --host H --user U --pass P
    python dump_remote_session.py --host H --user U --pass P --source telegram
    python dump_remote_session.py --host H --user U --pass P --keywords "sư phụ,đệ"
    python dump_remote_session.py --local          # state.db của chính máy này

Sau khi xem, clear prompt phiên cũ:
    hermes sessions repair-prompts <session_id> --apply --json
rồi restart gateway.
"""

import argparse
import os
import shutil
import sqlite3
import sys
import tempfile

try:
    import paramiko
except ImportError:  # --local vẫn chạy được nếu thiếu paramiko
    paramiko = None


def remote_localappdata(c):
    """Hỏi máy đích %LOCALAPPDATA% — không hardcode tên user."""
    _, stdout, _ = c.exec_command(
        "powershell -NoProfile -Command "
        "\"[Environment]::GetFolderPath('LocalApplicationData')\""
    )
    path = stdout.read().decode("utf-8", "replace").strip()
    if not path:
        sys.exit("Không lấy được %LOCALAPPDATA% của máy đích")
    return path.replace("\\", "/")


def fetch_db_remote(args, local_dir):
    """Tải state.db + -wal + -shm từ máy đích. Trả (đã tải, đường dẫn nguồn)."""
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(
        args.host,
        port=args.port,
        username=args.user,
        password=args.password,
        timeout=25,
        banner_timeout=40,
        auth_timeout=40,
        allow_agent=False,
        look_for_keys=False,
    )
    try:
        base = f"{remote_localappdata(c)}/hermes"
        sftp = c.open_sftp()
        got = []
        for name in ("state.db", "state.db-wal", "state.db-shm"):
            try:
                dst = os.path.join(local_dir, name)
                sftp.get(f"{base}/{name}", dst)
                got.append((name, os.path.getsize(dst)))
            except Exception:
                pass  # -wal/-shm không có khi gateway đã dừng sạch
        sftp.close()
        return got, f"{base}/state.db"
    finally:
        c.close()


def fetch_db_local(local_dir):
    """Bản local: copy state.db (đọc trực tiếp dễ bị lock khi gateway đang chạy)."""
    base = os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes")
    got = []
    for name in ("state.db", "state.db-wal", "state.db-shm"):
        src = os.path.join(base, name)
        if os.path.exists(src):
            dst = os.path.join(local_dir, name)
            shutil.copy2(src, dst)
            got.append((name, os.path.getsize(dst)))
    return got, os.path.join(base, "state.db")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host")
    ap.add_argument("--user")
    ap.add_argument("--pass", dest="password")
    ap.add_argument("--port", type=int, default=22)
    ap.add_argument("--local", action="store_true", help="đọc state.db của máy này")
    ap.add_argument("--source", default=None, help="lọc theo source: telegram, cli, oneshot")
    ap.add_argument(
        "--keywords",
        default="sư phụ,đệ,xưng hô",
        help="từ khoá persona cần kiểm trong system prompt (phẩy ngăn cách)",
    )
    ap.add_argument("--messages", type=int, default=12, help="số tin nhắn cuối in ra")
    args = ap.parse_args()

    if not args.local and not (args.host and args.user and args.password):
        sys.exit("Cần --host/--user/--pass, hoặc --local")

    tmp = tempfile.mkdtemp(prefix="hermes_state_")
    if args.local:
        got, origin = fetch_db_local(tmp)
    else:
        if paramiko is None:
            sys.exit("Thiếu paramiko: pip install paramiko (hoặc dùng --local)")
        got, origin = fetch_db_remote(args, tmp)

    if not got:
        sys.exit("Không tải được state.db — sai đường dẫn hoặc SSH chưa vào được")
    print(f"Nguồn: {origin}")
    for n, sz in got:
        print(f"  tải {n}: {sz} bytes")
    print()

    con = sqlite3.connect(os.path.join(tmp, "state.db"))
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # ---- hash -> prompt text, để biết phiên đang dùng bản persona nào ----
    prompts = {}
    try:
        cur.execute("SELECT hash, prompt FROM system_prompts")
        for r in cur.fetchall():
            prompts[r["hash"]] = r["prompt"] or ""
    except sqlite3.Error as e:
        print(f"(không đọc được system_prompts: {e})")

    kws = [k.strip() for k in args.keywords.split(",") if k.strip()]
    where, params = "", []
    if args.source:
        where, params = "WHERE source = ?", [args.source]

    cur.execute(
        f"""SELECT id, source, chat_id, system_prompt_hash, message_count, title
            FROM sessions {where} ORDER BY started_at DESC""",
        params,
    )
    rows = cur.fetchall()

    print("=" * 78)
    print("SESSIONS — phiên nào đang ghim prompt nào")
    print("=" * 78)
    for r in rows:
        h = r["system_prompt_hash"]
        if not h:
            verdict = "hash=NULL  -> prompt đã clear, lượt sau dựng lại"
        else:
            p = prompts.get(h, "")
            hits = [k for k in kws if k.lower() in p.lower()]
            if not p:
                verdict = f"hash={h[:16]}  (prompt không có trong bảng system_prompts)"
            elif hits:
                verdict = f"hash={h[:16]}  CÓ: {', '.join(hits)}"
            else:
                verdict = f"hash={h[:16]}  KHÔNG có từ khoá persona nào"
        print(f"\n  {r['id']}  [{r['source']}]  chat={r['chat_id']}")
        print(f"    msg={r['message_count']}  title={r['title']!r}")
        print(f"    {verdict}")

    # ---- tin nhắn thật: bằng chứng bot TRẢ LỜI gì ----
    cur.execute(
        """SELECT id, session_id, role, content
           FROM messages WHERE content IS NOT NULL AND content != ''
           ORDER BY id DESC LIMIT ?""",
        [args.messages],
    )
    msgs = list(reversed(cur.fetchall()))
    print()
    print("=" * 78)
    print(f"{len(msgs)} TIN NHẮN CUỐI (thứ tự thời gian)")
    print("=" * 78)
    for m in msgs:
        body = (m["content"] or "").replace("\n", " | ")[:300]
        print(f"\n  [{m['id']}] {m['role']:9s} session={m['session_id']}")
        print(f"      {body}")

    con.close()
    print()
    print("Phiên cũ ghim prompt cũ thì chữa bằng:")
    print("  hermes sessions repair-prompts <session_id> --apply --json")
    print("  rồi restart gateway.")


if __name__ == "__main__":
    main()
