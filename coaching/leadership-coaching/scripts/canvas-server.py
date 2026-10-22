#!/usr/bin/env python3
"""
Leadership Canvas Server — Local HTTP server for saving canvas data to file.

Usage: python canvas-server.py
Then open: http://localhost:2345
Click "Save" on the canvas → data writes to canvas-data.json + canvas-data.md

Features:
- Serves the canvas HTML at http://localhost:PORT
- Accepts POST /save with JSON body { b1: "...", b2: "...", ... }
- Saves to canvas-data.json (raw) + canvas-data.md (pretty markdown)
- GET /data returns current saved data
- Same-origin — no CORS issues when opened via localhost
"""

import http.server
import json
import os
from datetime import datetime

LEADERSHIP_DIR = os.path.dirname(os.path.abspath(__file__))
# Fall back to parent dir if running from scripts/ folder
if os.path.basename(LEADERSHIP_DIR) in ("scripts", "templates", "references"):
    LEADERSHIP_DIR = os.path.dirname(LEADERSHIP_DIR)

DATA_FILE = os.path.join(LEADERSHIP_DIR, "canvas-data.json")
MD_FILE = os.path.join(LEADERSHIP_DIR, "canvas-data.md")
HTML_FILE = os.path.join(LEADERSHIP_DIR, "leadership-canvas.html")
HTML_LOCAL_FILE = os.path.join(LEADERSHIP_DIR, "leader-canvas-local.html")
PORT = 2345


def generate_local_html():
    """Read base HTML and inject local-server save logic."""
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    local_js = f"""
  // ─── LOCAL SERVER SAVE ───
  async function saveToServer() {{
    const data = {{}};
    document.querySelectorAll('textarea').forEach(el => {{
      data[el.id] = el.value;
    }});
    try {{
      const resp = await fetch('http://localhost:{PORT}/save', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify(data)
      }});
      const result = await resp.json();
      showToast(result.ok ? '✅ Đã lưu về file!' : '❌ Lỗi: ' + (result.error || 'unknown'));
    }} catch(err) {{
      showToast('❌ Không kết nối được server. Chạy canvas-server.py trước.');
    }}
  }}

  function showToast(msg) {{
    let t = document.getElementById('toast');
    if (!t) {{
      t = document.createElement('div');
      t.id = 'toast';
      t.style.cssText = 'position:fixed;bottom:30px;left:50%;transform:translateX(-50%);background:#00b894;color:#000;padding:10px 24px;border-radius:8px;font-size:13px;font-weight:600;z-index:100;display:none';
      document.body.appendChild(t);
    }}
    t.textContent = msg;
    t.style.display = 'block';
    setTimeout(() => {{ t.style.display = 'none'; }}, 3000);
  }}

  document.querySelector('.btn-save').onclick = saveToServer;
  document.querySelectorAll('textarea').forEach(el => {{
    el.addEventListener('input', () => localStorage.setItem('lc_' + el.id, el.value));
  }});
"""
    html = html.replace("</body>", f"<script>{local_js}</script>\n</body>")
    html = html.replace("Leadership Canvas — Quang", "Leadership Canvas — Local")

    with open(HTML_LOCAL_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    return HTML_LOCAL_FILE


def save_canvas_data(data):
    """Save canvas data to JSON + markdown files."""
    record = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "canvas": data
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    md = f"""# Leader Canvas — {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Mission
{data.get('b1', '_trống_')}

## Vision
{data.get('b2', '_trống_')}

## Values
{data.get('b3', '_trống_')}

## Strengths
{data.get('b4', '_trống_')}

## Growth Areas
{data.get('b5', '_trống_')}

## Style
{data.get('b6', '_trống_')}

## Key Relationships
{data.get('b7', '_trống_')}

## Success Metrics
{data.get('b8', '_trống_')}

## Legacy
{data.get('b9', '_trống_')}
"""
    with open(MD_FILE, "w", encoding="utf-8") as f:
        f.write(md)
    return True


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path != "/save":
            self.send_response(404); self.end_headers(); return
        length = int(self.headers["Content-Length"])
        try:
            data = json.loads(self.rfile.read(length))
            save_canvas_data(data)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode())
            print(f"\n✅ Canvas saved at {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode())

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open(HTML_LOCAL_FILE, "rb") as f:
                self.wfile.write(f.read())
        elif self.path == "/data":
            data = {}
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, encoding="utf-8") as f:
                    data = json.load(f)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
        else:
            super().do_GET()


def main():
    print("=" * 50)
    print("  Leadership Canvas Server")
    print("=" * 50)
    print(f"\n  Open: http://localhost:{PORT}")
    print(f"  Save: {DATA_FILE}")
    print(f"  Markdown: {MD_FILE}\n")

    generate_local_html()
    os.chdir(LEADERSHIP_DIR)

    server = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
