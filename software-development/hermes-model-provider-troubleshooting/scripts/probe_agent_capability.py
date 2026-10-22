#!/usr/bin/env python3
"""probe_agent_capability.py — verify a model can survive a TOOL-CALL ROUND TRIP.

Why this exists
---------------
A single-turn chat probe ("hi") does NOT prove a model is usable as a Hermes
fallback. Some models answer plain questions correctly but collapse on the turn
AFTER they receive a tool result, emitting degenerate text (observed 2026-09:
`moonshotai/kimi-k3` returned content='' + reasoning_content='!!!!...').
A fallback chain whose entry #1 does that is useless even if the other 16
entries are fine.

This script drives the 2-turn sequence directly against an OpenAI-compatible
endpoint:  user -> tool_call -> tool result -> final answer.

Usage
-----
  python probe_agent_capability.py --base https://integrate.api.nvidia.com/v1 \
      --key "$NVIDIA_API_KEY" \
      --models "nvidia/nemotron-3-ultra-550b-a55b,z-ai/glm-5.3,moonshotai/kimi-k3"

  # models from a file, one per line:
  python probe_agent_capability.py --base ... --key ... --model-file chain.txt

  # discover the whole catalog instead of naming models (filters non-chat names):
  python probe_agent_capability.py --base ... --key ... --from-catalog

Exit code 0 always; read the printed matrix. PASS models are safe to put first
in `fallback_providers`.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

TOOLS = [{
    "type": "function",
    "function": {
        "name": "run_shell",
        "description": "Run a shell command and return its stdout.",
        "parameters": {
            "type": "object",
            "properties": {"command": {"type": "string", "description": "shell command"}},
            "required": ["command"],
        },
    },
}]

PROMPT = ("Dung tool run_shell de tinh 5 nhan 6. Sau do tra loi ket qua ngan gon.")

NON_CHAT = ["embed", "reward", "safety", "guard", "parse", "rerank", "retriever",
            "asr", "tts", "vision-encode", "clip", "diffusion", "flux", "sdxl",
            "deplot", "grounding", "ocr", "detector", "segmentation", "biomedclip"]


def post(base: str, key: str, model: str, messages: list, tools: bool = True,
         max_tokens: int = 512, timeout: int = 150) -> dict:
    body = {"model": model, "messages": messages,
            "max_tokens": max_tokens, "temperature": 0.3}
    if tools:
        body["tools"] = TOOLS
        body["tool_choice"] = "auto"
    req = urllib.request.Request(
        f"{base.rstrip('/')}/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST")
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode())


def degenerate(text: str) -> bool:
    """True for junk like '!!!!!!' / '?????' / '......' — the collapse signature."""
    if not text:
        return False
    return bool(re.fullmatch(r"[!?.,;:\-_*#=~]{6,}", text.strip()))


def test_model(base: str, key: str, model: str, timeout: int = 150):
    """Return (model, status, detail). status == 'OK' means safe for the chain."""
    try:
        # --- turn 1: model must choose to call the tool -------------------
        msgs = [{"role": "user", "content": PROMPT}]
        r1 = post(base, key, model, msgs, timeout=timeout)
        ch1 = (r1.get("choices") or [{}])[0]
        msg1 = ch1.get("message", {}) or {}
        tcs = msg1.get("tool_calls") or []
        if not tcs:
            return (model, "NO_TOOL_CALL",
                    f"content={(msg1.get('content') or '')[:60]!r}")

        # --- turn 2: feed the tool result back ----------------------------
        call = tcs[0]
        msgs.append({"role": "assistant", "content": msg1.get("content") or "",
                     "tool_calls": tcs})
        msgs.append({"role": "tool", "tool_call_id": call.get("id"), "content": "30"})
        r2 = post(base, key, model, msgs, timeout=timeout)
        ch2 = (r2.get("choices") or [{}])[0]
        msg2 = ch2.get("message", {}) or {}
        content = (msg2.get("content") or "").strip()
        reasoning = (msg2.get("reasoning_content") or "").strip()

        if degenerate(content) or degenerate(reasoning):
            # THE failure this script exists to catch
            return (model, "DEGENERATE",
                    f"content={content[:40]!r} reasoning={reasoning[:40]!r}")
        if not content and not reasoning:
            return (model, "EMPTY", "no content, no reasoning after tool result")
        if "30" not in content:
            return (model, "NO_ANSWER", f"content={content[:70]!r}")
        return (model, "OK", content[:60])
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:110]
        # 400 "auto tool choice requires --enable-auto-tool-choice" => no tool support
        return (model, f"HTTP{e.code}", detail)
    except Exception as e:  # noqa: BLE001
        return (model, type(e).__name__, str(e)[:110])


def from_catalog(base: str, key: str) -> list[str]:
    req = urllib.request.Request(f"{base.rstrip('/')}/models",
                                 headers={"Authorization": f"Bearer {key}"})
    data = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
    ids = [m["id"] for m in data.get("data", [])]
    return sorted(m for m in ids if not any(k in m.lower() for k in NON_CHAT))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", required=True, help="OpenAI-compatible base URL, e.g. .../v1")
    ap.add_argument("--key", required=True, help="API key")
    ap.add_argument("--models", help="comma-separated model ids")
    ap.add_argument("--model-file", help="file with one model id per line")
    ap.add_argument("--from-catalog", action="store_true",
                    help="discover models from /models (filter non-chat names)")
    ap.add_argument("--workers", type=int, default=4,
                    help="concurrency (keep low: free tiers 503 on shared pools)")
    ap.add_argument("--timeout", type=int, default=150)
    a = ap.parse_args()

    if a.from_catalog:
        models = from_catalog(a.base, a.key)
    elif a.model_file:
        models = [l.strip() for l in open(a.model_file, encoding="utf-8")
                  if l.strip() and not l.startswith("#")]
    elif a.models:
        models = [m.strip() for m in a.models.split(",") if m.strip()]
    else:
        ap.error("give --models, --model-file or --from-catalog")

    print(f"probing {len(models)} model(s) — tool-call round trip\n", flush=True)
    results: dict[str, tuple[str, str]] = {}
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(test_model, a.base, a.key, m, a.timeout): m for m in models}
        for f in as_completed(futs):
            model, status, detail = f.result()
            results[model] = (status, detail)
            print(f"{status:12} {model:52} {detail}", flush=True)

    passed = [m for m in models if results.get(m, ("", ""))[0] == "OK"]
    print(f"\n===== PASS ({len(passed)}/{len(models)}) — safe to put FIRST in the chain =====")
    for m in passed:
        print(f"  {m}")
    print("\n===== FAIL / SUSPECT =====")
    for m in models:
        st, detail = results.get(m, ("?", ""))
        if st != "OK":
            print(f"  {st:12} {m:52} {detail[:80]}")

    print("\nNOTE: a model that passes here can still break against a real Hermes\n"
          "session (large system prompt + many tool schemas). Confirm the head of\n"
          "the chain inside the harness:\n"
          '  hermes --provider <p> -m "<model>" -z "Dung lenh terminal de tinh 5 nhan 6, roi tra loi ngan gon."\n'
          '  -> "5 x 6 = 30" good, "!!!!..." broken.')
    return 0


if __name__ == "__main__":
    sys.exit(main())
