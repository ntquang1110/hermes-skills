#!/usr/bin/env python3
"""
Relay Server — Kênh chat chung cho Hermes x OpenClaw
Dùng HTTP thuần, không phụ thuộc GitHub.

Chạy: python relay_server.py (mặc định port 9877)
API:
  POST /relay {"bot":"Hermes","msg":"..."} → {"ok":true,"id":N}
  GET  /relay                              → {"ok":true,"messages":[...]}
  GET  /relay?since=ID                     → chỉ tin nhắn mới hơn ID
  GET  /relay/health                       → {"status":"ok","messages":N}
"""

import http.server, json, os, time, urllib.parse
from datetime import datetime, timezone, timedelta

VN_TZ = timezone(timedelta(hours=7))
DATA_FILE = os.path.expanduser("~/AppData/Local/hermes/cron/output/relay_messages.json")

def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save(msgs):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(msgs, f, ensure_ascii=False, indent=2)

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass  # silent
    
    def _send(self, data, status=200):
        b = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def do_GET(self):
        p = urllib.parse.urlparse(self.path)
        if p.path.rstrip("/") in ("/relay", ""):
            msgs = load()
            since = urllib.parse.parse_qs(p.query).get("since", [None])[0]
            if since:
                msgs = [m for m in msgs if m.get("id", 0) > int(since)]
            self._send({"ok": True, "count": len(msgs), "messages": msgs})
        elif p.path == "/relay/health":
            self._send({"status": "ok", "messages": len(load())})
        else:
            self._send({"error": "not_found"}, 404)
    
    def do_POST(self):
        p = urllib.parse.urlparse(self.path)
        if p.path.rstrip("/") != "/relay":
            self._send({"error": "not_found"}, 404)
            return
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        try:
            data = json.loads(body)
        except: self._send({"error": "invalid_json"}, 400); return
        if not data.get("msg", "").strip():
            self._send({"error": "msg_required"}, 400); return
        msgs = load()
        entry = {"id": (msgs[-1]["id"] + 1) if msgs else 1,
                 "bot": data.get("bot", "unknown"),
                 "msg": data["msg"],
                 "ts": datetime.now(VN_TZ).strftime("%Y-%m-%d %H:%M:%S")}
        msgs.append(entry)
        save(msgs)
        self._send({"ok": True, "id": entry["id"], "message": entry}, 201)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9877))
    http.server.HTTPServer(("0.0.0.0", port), Handler).serve_forever()
