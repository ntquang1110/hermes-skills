#!/usr/bin/env python3
"""Probe một OpenAI-compatible endpoint để xác định model/provider trả empty ở ngưỡng nào.

Dùng khi Hermes báo "Empty response from model" hoặc "No fallback providers configured":
1. Kiểm tra endpoint còn sống.
2. Test với nhiều context size + tool-call pattern (giả lập request thật của Hermes).
3. Stream=True + parse SSE dòng "data: " — non-stream có thể bị 400.

Usage:
    python probe_provider.py [base_url] [model]
    python probe_provider.py http://192.168.1.110:20128/v1 auto/best-coding
"""
import json
import sys
import time
import urllib.request

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://192.168.1.110:20128/v1"
MODEL = sys.argv[2] if len(sys.argv) > 2 else "auto/best-coding"


def probe(label, chars, use_tool=False, max_tokens=100):
    text = ("Lặp lại nội dung test để tăng context. Đây là đoạn văn bản tiếng Việt có dấu. " * (chars // 10))[:chars]
    if use_tool:
        messages = [
            {"role": "user", "content": "Đếm ký tự: " + text},
            {"role": "assistant", "content": None, "tool_calls": [
                {"id": "call_1", "type": "function", "function": {"name": "count", "arguments": "{\"x\": 1}"}}
            ]},
            {"role": "tool", "tool_call_id": "call_1", "content": "12345"},
            {"role": "user", "content": "Tiếp tục. Trả lời: OK"},
        ]
    else:
        messages = [{"role": "user", "content": text + "\nTrả lời: OK"}]

    body = json.dumps({
        "model": MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "stream": True,
    }).encode()
    req = urllib.request.Request(BASE_URL + "/chat/completions", body, {"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=240) as r:
            raw = r.read().decode()
        dt = time.time() - t0
        contents = []
        for line in raw.splitlines():
            if line.startswith("data: "):
                try:
                    d = json.loads(line[6:])
                    ch = d.get("choices", [{}])[0].get("delta", {})
                    if ch.get("content"):
                        contents.append(ch["content"])
                except Exception:
                    pass
        joined = "".join(contents)
        status = "OK" if joined.strip() else "EMPTY!"
        print(f"{label}: {status} latency={dt:.1f}s sse={len(raw)}B content={repr(joined[:60])}")
        return bool(joined.strip())
    except Exception as e:
        dt = time.time() - t0
        try:
            detail = e.read().decode()[:200] if hasattr(e, "read") else str(e)[:200]
        except Exception:
            detail = str(e)[:200]
        print(f"{label}: ERROR after {dt:.1f}s: {type(e).__name__}: {detail}")
        return False


def main():
    # 1. Endpoint còn sống?
    try:
        with urllib.request.urlopen(BASE_URL + "/models", timeout=10) as r:
            data = json.loads(r.read().decode())
            print(f"Endpoint OK: {len(data.get('data', []))} models\n")
    except Exception as e:
        print(f"Endpoint DEAD: {e}")
        sys.exit(1)

    # 2. Context size ramp (chars, tiếng Việt ~1.6 chars/token)
    results = []
    for chars in (5000, 50000, 150000, 250000):
        results.append(probe(f"ctx {chars//1000}K", chars))
    # 3. Tool-call pattern với context lớn (giả lập request Hermes thật)
    results.append(probe("tool+220K", 220000, use_tool=True))

    empty = [r for r in results if not r]
    if empty:
        print(f"\n=> {len(empty)}/{len(results)} probe trả rỗng. Provider yếu với context lớn / tool schemas.")
        sys.exit(2)
    print("\n=> Tất cả probe OK. Nghi request thật của Hermes (system prompt + tool schemas) hoặc lỗi tạm thời lúc đó.")


if __name__ == "__main__":
    main()
