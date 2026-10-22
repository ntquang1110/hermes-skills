#!/usr/bin/env python3
"""
Shared Scratchpad — bot-to-bot communication via GitHub Gist
Workaround for Telegram's "bots can't see other bots" limitation.

Usage:
  python scratchpad.py write "BotName: message text"
  python scratchpad.py read           # read all
  python scratchpad.py read 3         # read last 3 messages

Environment: GITHUB_PAT env var or ~/AppData/Local/hermes/.env
"""
import sys, json, requests, base64, os
from datetime import datetime, timezone, timedelta

GIST_ID = "a5b9533a50f001ca2a3263df61c1cab5"
PAT = None
env_path = os.path.expanduser("~/AppData/Local/hermes/.env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if "GITHUB_PAT_B64" in line:
                PAT = base64.b64decode(line.split("=", 1)[1].strip()).decode()
                break
if not PAT:
    PAT = os.environ.get("GITHUB_PAT", "")
API = f"https://api.github.com/gists/{GIST_ID}"
VN_TZ = timezone(timedelta(hours=7))

def read_gist():
    r = requests.get(API)
    if r.status_code != 200:
        print(f"Error: {r.status_code}", file=sys.stderr)
        return []
    for fdata in r.json().get("files", {}).values():
        if fdata["filename"].endswith(".json"):
            return json.loads(fdata.get("content", "[]"))
    return []

def write_gist(msgs):
    r = requests.patch(API, headers={"Authorization": f"token {PAT}",
        "Content-Type": "application/json"},
        json={"files": {"scratchpad.json": {"content": json.dumps(msgs, ensure_ascii=False, indent=2)}}})
    if r.status_code != 200:
        print(f"Write error: {r.status_code}", file=sys.stderr)

def add_msg(bot, msg):
    msgs = read_gist()
    now = datetime.now(VN_TZ).strftime("%Y-%m-%d %H:%M:%S")
    msgs.append({"bot": bot, "msg": msg, "ts": now})
    write_gist(msgs)
    print(f"[{now}] {bot}: {msg}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scratchpad.py <write|read> [args]"); sys.exit(1)
    if sys.argv[1] == "write":
        if len(sys.argv) < 3: print("Need message"); sys.exit(1)
        add_msg("Hermes", " ".join(sys.argv[2:]))
    elif sys.argv[1] == "read":
        msgs = read_gist()
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else len(msgs)
        for m in msgs[-limit:]:
            print(f"[{m.get('ts','')}] {m.get('bot','?').upper()}: {m.get('msg','')}")
