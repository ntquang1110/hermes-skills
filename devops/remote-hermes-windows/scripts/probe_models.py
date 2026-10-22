#!/usr/bin/env python3
"""
Probe an OpenAI-compatible model endpoint across three gates.

Gate 1  reachability      — does the model exist for this account?
Gate 2  tool-call        — does it emit a tool_call when one is offered?
Gate 3  tool round trip  — does it use the tool RESULT, or degenerate?

A model can pass 1 and 2 and fail 3: a 1T-parameter model answered ordinary
questions correctly but emitted reasoning_content='!!!!!!!!' and an empty
content string on the turn right after a tool result, breaking every agent
turn that used it. Only gate 3 predicts survival of an agent loop, so a
fallback chain must be ordered by gate 3, not by parameter count.

Catalog size is also a lie: one free-tier account listed 82 models and only 14
were reachable. The rest returned
    404 {"detail":"Function '<uuid>': Not found for account '<uuid>'"}
which is an entitlement failure, not a broken model.

Usage:
    PROVIDER_KEY=nvapi-... PROVIDER_BASE=https://integrate.api.nvidia.com/v1 \\
        python probe_models.py                  # all chat candidates
    PROVIDER_KEY=... PROVIDER_BASE=... \\
        python probe_models.py model/a model/b   # explicit list

Env:
    PROVIDER_KEY   bearer token (required)
    PROVIDER_BASE  base URL ending in /v1
    TIMEOUT        per-request seconds, default 90
    CONCURRENCY    parallel probes, default 5
    ROUNDS         retries per gate, default 2
"""
import json
import os
import re
import sys
import time
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

# A run of repeated punctuation/symbols means the decoder collapsed.
DEGENERATE = re.compile(r"[!?.,;:\-_*#=~\s]{6,}")

NOT_CHAT = ("embed", "reward", "safety", "guard", "parse", "rerank", "retriever",
            "asr", "tts", "vision-encode", "clip", "diffusion", "flux", "sdxl",
            "deplot", "grounding", "ocr", "detector", "segmentation", "biomedclip")


def is_chat(mid):
    low = mid.lower()
    return not any(k in low for k in NOT_CHAT)


def degenerate(text):
    t = (text or "").strip()
    return bool(DEGENERATE.fullmatch(t)) if t else False


class Probe:
    def __init__(self, base, key, timeout=90, rounds=2):
        self.base = base.rstrip("/")
        self.key = key
        self.timeout = timeout
        self.rounds = rounds

    def _post(self, payload):
        req = urllib.request.Request(
            f"{self.base}/chat/completions",
            data=json.dumps(payload).encode(),
            headers={"Authorization": f"Bearer {self.key}",
                     "Content-Type": "application/json"},
            method="POST")
        return json.loads(urllib.request.urlopen(req, timeout=self.timeout).read().decode())

    def list_models(self):
        req = urllib.request.Request(
            f"{self.base}/models", headers={"Authorization": f"Bearer {self.key}"})
        data = json.loads(urllib.request.urlopen(req, timeout=self.timeout).read().decode())
        return sorted(m["id"] for m in data.get("data", []))

    def probe(self, mid):
        """Return (verdict, detail); verdict OK|GATE1|GATE2|GATE3|ERROR."""
        # ---- Gate 1: plain completion, retried on transient timeout ----
        body, last = None, ""
        for attempt in range(self.rounds):
            try:
                body = self._post({
                    "model": mid,
                    "messages": [{"role": "user", "content": "hi"}],
                    "max_tokens": 8, "temperature": 0.1})
                break
            except urllib.error.HTTPError as e:
                return "GATE1", f"HTTP {e.code}: {e.read().decode()[:120]}"
            except Exception as e:
                last = f"{type(e).__name__}: {str(e)[:90]}"
                if attempt < self.rounds - 1:
                    time.sleep(2 * (attempt + 1))
        if body is None:
            return "ERROR", last

        msg = ((body.get("choices") or [{}])[0]).get("message", {})
        txt = ((msg.get("content") or "") + (msg.get("reasoning_content") or "")).strip()
        if not txt:
            return "GATE1", "200 but empty content and no reasoning"

        # ---- Gate 2: must offer a tool_call ----
        ask = "Use the run_shell tool to multiply 5 by 6."
        try:
            r2 = self._post({
                "model": mid,
                "messages": [{"role": "user", "content": ask}],
                "tools": TOOLS, "tool_choice": "auto",
                "max_tokens": 512})
        except urllib.error.HTTPError as e:
            detail = e.read().decode()[:120]
            if "tool choice" in detail.lower():
                return "GATE2", "specialised model, tool_choice unsupported (HTTP 400)"
            return "GATE2", f"HTTP {e.code}: {detail}"
        except Exception as e:
            return "GATE2", f"{type(e).__name__}: {str(e)[:90]}"

        m2 = ((r2.get("choices") or [{}])[0]).get("message", {})
        calls = m2.get("tool_calls") or []
        if not calls:
            return "GATE2", f"no tool_call; content={str(m2.get('content') or '')[:60]!r}"

        # ---- Gate 3: feed the result back, must use it ----
        call = calls[0]
        convo = [
            {"role": "user", "content": ask},
            {"role": "assistant", "content": m2.get("content") or "", "tool_calls": calls},
            {"role": "tool", "tool_call_id": call.get("id"), "content": "30"},
        ]
        try:
            r3 = self._post({"model": mid, "messages": convo,
                             "max_tokens": 512, "temperature": 0.3})
        except urllib.error.HTTPError as e:
            return "GATE3", f"HTTP {e.code}: {e.read().decode()[:100]}"
        except Exception as e:
            return "GATE3", f"{type(e).__name__}: {str(e)[:90]}"

        m3 = ((r3.get("choices") or [{}])[0]).get("message", {})
        content = (m3.get("content") or "").strip()
        reasoning = (m3.get("reasoning_content") or "").strip()

        if degenerate(content) or degenerate(reasoning):
            return "GATE3", (f"degenerate -> content={content[:40]!r} "
                             f"reasoning={reasoning[:40]!r}")
        if not content and not reasoning:
            return "GATE3", "both content and reasoning empty"
        if "30" not in content:
            return "GATE3", f"did not use tool result; content={content[:70]!r}"
        return "OK", content[:70]


def main():
    key = os.environ.get("PROVIDER_KEY", "")
    base = os.environ.get("PROVIDER_BASE", "")
    models = sys.argv[1:]
    if not key or not base:
        print(__doc__)
        return 2

    p = Probe(base, key,
              timeout=int(os.environ.get("TIMEOUT", "90")),
              rounds=int(os.environ.get("ROUNDS", "2")))

    if not models:
        print("fetching model list ...")
        allm = p.list_models()
        models = [m for m in allm if is_chat(m)]
        print(f"{len(allm)} in catalogue, {len(models)} chat candidates\n")

    results = {}
    with ThreadPoolExecutor(max_workers=int(os.environ.get("CONCURRENCY", "5"))) as ex:
        futs = {ex.submit(p.probe, m): m for m in models}
        for i, f in enumerate(as_completed(futs), 1):
            mid, (verdict, detail) = f.result()
            results[mid] = (verdict, detail)
            print(f"[{i:>3}/{len(models)}] {verdict:<6} {mid:<52} {detail}", flush=True)

    ok = [m for m in models if results[m][0] == "OK"]
    print("\n" + "=" * 78)
    print(f"PASS (safe for an agent loop): {len(ok)}")
    for m in sorted(ok):
        print(f"  OK    {m}")

    for verdict in ("GATE3", "GATE2", "GATE1", "ERROR"):
        bad = [m for m in models if results[m][0] == verdict]
        if bad:
            print(f"\n{verdict}: {len(bad)} — do not put in a fallback chain")
            for m in sorted(bad):
                print(f"  {verdict:<6} {m:<52} {results[m][1]}")

    print("\nOrder the chain by parameter count WITHIN the OK set only.")
    print("Then confirm each OK model in the real harness — a ~15K-token system")
    print("prompt with the full tool set is a different test:")
    print("  hermes --provider <p> -m <model> -z 'Use terminal to compute 5*6, then answer briefly.'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
