#!/usr/bin/env python3
"""Push approved psychology articles to KFlow (Knowledge Flow) at localhost:3003.

Usage:
    python push_psy_to_kflow.py <draft.txt> [<draft2.txt> ...]

Each file: first line may be "# Title..." (title auto-derived if not given via --title).
Headers: Bearer hermes-knowledge-secret + Cookie tfo_auth (sha256 of passcode <PASSCODE>).
Without the cookie, proxy.ts redirects POST /api/knowledge to /passcode (307) -> import fails.

Requires a running KFlow server (port 3003). Verify success by opening http://localhost:3003
in browser (passcode <PASSCODE>) and checking the Feed.
"""
import sys
import json
import os
import hashlib
import ssl
import urllib.request

BASE = "http://localhost:3003"
AUTH = "Bearer hermes-knowledge-secret"
PASSCODE = "<PASSCODE>"
COOKIE = f"tfo_auth={hashlib.sha256(PASSCODE.encode()).hexdigest()}"
SLUG = "tam-ly"

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE


def push(path: str, title: str | None = None) -> dict:
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if not title:
        first = content.strip().splitlines()[0] if content.strip() else ""
        title = first.lstrip("# ").strip() if first.startswith("#") else os.path.basename(path)
    body = json.dumps(
        {"title": title, "content": content, "topic_slug": SLUG, "source_url": ""},
        ensure_ascii=False,
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE}/api/knowledge",
        data=body,
        headers={"Authorization": AUTH, "Content-Type": "application/json", "Cookie": COOKIE},
    )
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=20)
    return json.loads(resp.read().decode())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for arg in sys.argv[1:]:
        try:
            result = push(arg)
            print(f"OK  {os.path.basename(arg)} -> {result.get('id', result)}")
        except Exception as e:
            err = str(e)
            try:
                if hasattr(e, "read"):
                    err += " | " + e.read().decode()[:300]
            except Exception:
                pass
            print(f"ERR {os.path.basename(arg)}: {err}")
            sys.exit(2)
