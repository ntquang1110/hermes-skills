#!/usr/bin/env python3
"""
UA-rewrite reverse proxy cho OpenAI-compatible served model bị server chặn theo
User-Agent (HTTP 403 "Your request was blocked").

Khi đúng: origin server / nginx bot-protection chặn mọi UA bắt đầu "OpenAI/" (cả
Python lẫn Node) → Hermes (openai-python SDK) luôn bị 403 dù curl 200. Workaround
mà không cần pip: proxy này nhận request ở local, ép UA hợp lệ, forward tới server.

Start:
    python ua-rewrite-proxy.py [bind host:port] [target_base_url]
VD:
    python ua-rewrite-proxy.py 127.0.0.1:18888 https://pharma-llm.thefirstonly.com/v1

QUAN TRỌNG (double /v1): proxy tự nối "/v1" vào target. base_url Hermes phải là
http://127.0.0.1:18888 (KHÔNG có /v1), nếu không request thành /v1/v1/... → server
trả {"error":"API endpoint not found"}.

Verify:
    curl -s -o /dev/null -w "%{http_code}\n" -A "OpenAI/Python 1.0.0" \
      -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
      --data-binary @body.json http://127.0.0.1:18888/chat/completions   # phải 200
"""
import http.server
import sys
import ssl
import urllib.request
import urllib.error

ALLOWED_UA = "openai-python-client"


def build_proxy(target_base):
    class Handler(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def _forward(self):
            url = target_base.rstrip("/") + self.path
            body = None
            if "Content-Length" in self.headers:
                length = int(self.headers["Content-Length"])
                if length > 0:
                    body = self.rfile.read(length)

            headers = {}
            for k, v in self.headers.items():
                lk = k.lower()
                if lk in ("host", "connection", "content-length", "user-agent"):
                    continue
                headers[k] = v
            headers["User-Agent"] = ALLOWED_UA

            context = ssl.create_default_context()
            req = urllib.request.Request(url, data=body, headers=headers, method=self.command)
            try:
                resp = urllib.request.urlopen(req, context=context, timeout=300)
                data = resp.read()
                status = resp.status
                out_headers = dict(resp.headers.items())
            except urllib.error.HTTPError as e:
                data = e.read()
                status = e.code
                out_headers = dict(e.headers.items()) if e.headers else {}
            except Exception as e:
                data = ("proxy error: %s" % e).encode()
                status = 502
                out_headers = {"Content-Type": "text/plain"}

            self.send_response(status)
            for k, v in out_headers.items():
                if k.lower() == "transfer-encoding":
                    continue
                self.send_header(k, v)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        do_GET = _forward
        do_POST = _forward
        do_PUT = _forward
        do_DELETE = _forward
        do_PATCH = _forward

        def log_message(self, fmt, *args):
            sys.stderr.write("[ua-proxy] %s %s\n" % (self.command, self.path))

    return Handler


def main():
    bind = "127.0.0.1:18888"
    target = "https://pharma-llm.thefirstonly.com/v1"
    if len(sys.argv) > 1:
        parts = sys.argv[1].split(":")
        bind = "%s:%s" % (parts[0], parts[1] if len(parts) > 1 else "18888")
    if len(sys.argv) > 2:
        target = sys.argv[2]
    host, port = bind.split(":")
    httpd = http.server.ThreadingHTTPServer((host, int(port)), build_proxy(target))
    print("UA-proxy running on http://%s -> %s" % (bind, target), flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()