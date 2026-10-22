#!/usr/bin/env python3
"""
Canva OAuth callback server — PKCE S256.
B1: server tự sinh code_verifier + code_challenge.
B2: / -> in link authorize kèm code_challenge & code_challenge_method=s256.
B3: user bấm link, Canva redirect /callback?code=...
B4: đổi code -> token (gửi code_verifier) -> lưu canva_token.json + canva_token.txt.
Chạy public qua tunnel (Canva KHÔNG nhận localhost redirect URI).

Cần chỉnh: CLIENT_ID, CLIENT_SECRET, REDIRECT_URI theo app.
"""
import http.server, json, urllib.request, urllib.parse, sys, secrets, hashlib, base64

CLIENT_ID = "OC-XXXX"                       # thay bằng client id Connect API
CLIENT_SECRET = "xxxx"                      # thay bằng client secret
REDIRECT_URI = "https://your-sub.domain.com/callback"  # HTTPS public, đã đăng ký
TOKEN_URL = "https://api.canva.com/oauth/token"
AUTH_URL = "https://www.canva.com/api/oauth/authorize"
TOKEN_FILE = "canva_token.json"
TOKEN_TXT = "canva_token.txt"

# PKCE S256
verifier = secrets.token_urlsafe(64)
challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()

SCOPES = ("asset:read asset:write design:content:read design:content:write "
          "design:meta:read design:meta:write brandtemplate:content:read brandtemplate:content:write "
          "comment:read comment:write folder:read folder:write profile:read")

auth_link = (
    f"{AUTH_URL}?code_challenge_method=s256&response_type=code"
    f"&client_id={CLIENT_ID}"
    f"&redirect_uri={urllib.parse.quote(REDIRECT_URI, safe='')}"
    f"&scope={urllib.parse.quote(SCOPES)}"
    f"&code_challenge={challenge}"
)

def exchange_code(code):
    data = urllib.parse.urlencode({
        "grant_type": "authorization_code", "code": code,
        "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI, "code_verifier": verifier,
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            tok = json.loads(resp.read())
            with open(TOKEN_FILE, "w") as f:
                json.dump(tok, f, indent=2)
            acc = tok.get("access_token", "")
            if acc:
                with open(TOKEN_TXT, "w") as f:
                    f.write("CANVA_ACCESS_TOKEN=" + acc)
            return tok
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "body": e.read().decode()[:400]}
    except Exception as e:
        return {"error": str(e)}

PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Canva OAuth</title></head>
<body style="font-family:sans-serif;padding:40px;text-align:center">
<h2>Canva OAuth</h2><div id="s">%s</div>
<pre id="d" style="text-align:left;background:#f5f5f5;padding:15px;white-space:pre-wrap">%s</pre></body></html>"""

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("/callback", "/"):
            qs = urllib.parse.parse_qs(parsed.query)
            code = qs.get("code", [""])[0]
            err = qs.get("error", [""])[0]
            if parsed.path == "/callback" and code:
                tok = exchange_code(code)
                ok = "access_token" in tok
                detail = json.dumps({k: (v[:8]+"..." if k.endswith("token") else v)
                                     for k, v in tok.items()}, indent=2) if ok else json.dumps(tok, indent=2)
                body = PAGE % ("✅ SUCCESS token saved" if ok else "❌ FAILED", detail)
            elif parsed.path == "/":
                body = PAGE % ("Auth link:", auth_link)
            else:
                body = PAGE % ("ERROR", err or "no code")
            b = body.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)
        else:
            self.send_response(404); self.end_headers()
    def log_message(self, fmt, *args):
        sys.stderr.write("[oauth] %s\n" % (fmt % args))

if __name__ == "__main__":
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 8790), Handler)
    print("OAuth server (PKCE) on :8790", flush=True)
    print("AUTH LINK:\n" + auth_link, flush=True)
    httpd.serve_forever()