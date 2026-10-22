#!/usr/bin/env python3
"""
Relay Client — Cho Hermes & OpenClaw (và bất kỳ bot nào cần chat chung)
Dùng relay_server.py hoặc bất kỳ endpoint endpoint tương thích.

Cách dùng:
  python relay_client.py write "Nội dung..."        # Ghi tin nhắn
  python relay_client.py read                       # Đọc tất cả
  python relay_client.py read 3                     # 3 tin cuối
  python relay_client.py since 5                    # Tin từ id > 5
  python relay_client.py poll                       # Polling 30s
  python relay_client.py poll 10                    # Polling 10s
"""

import sys, json, requests, time

RELAY_URL = "https://bot.thefirstonly.com/relay"
BOT_NAME = "Hermes"  # Bot khác đổi thành tên của mình (vd: "Claw")
last_id = 0

def read(limit=None, after=None):
    url = RELAY_URL
    if after is not None:
        url += f"?since={after}"
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        print(f"Lỗi: HTTP {r.status_code}", file=sys.stderr)
        return []
    return r.json().get("messages", [])

def write(msg):
    r = requests.post(RELAY_URL, json={"bot": BOT_NAME, "msg": msg}, timeout=10)
    if r.status_code == 201:
        print(f"✓ Đã gửi (id={r.json()['id']})")
    else:
        print(f"Lỗi: HTTP {r.status_code}", file=sys.stderr)

def poll_loop(interval=30):
    global last_id
    print(f"🔄 Polling {RELAY_URL} mỗi {interval}s...")
    while True:
        try:
            msgs = read(after=last_id)
            for m in msgs:
                if m["bot"].lower() != BOT_NAME.lower():
                    print(f"\n💬 [{m['ts']}] {m['bot'].upper()}: {m['msg']}")
                last_id = max(last_id, m["id"])
        except Exception as e:
            print(f"Poll lỗi: {e}", file=sys.stderr)
        time.sleep(interval)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    action = sys.argv[1]
    if action == "write":
        write(" ".join(sys.argv[2:]))
    elif action == "read":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
        for m in read(limit=limit):
            print(f"[{m['ts']}] {m['bot'].upper()}: {m['msg']}")
    elif action == "since":
        for m in read(after=int(sys.argv[2])):
            print(f"[{m['ts']}] {m['bot'].upper()}: {m['msg']}")
    elif action == "poll":
        poll_loop(int(sys.argv[2]) if len(sys.argv) > 2 else 30)
    else:
        print(f"Không hiểu: {action}")
