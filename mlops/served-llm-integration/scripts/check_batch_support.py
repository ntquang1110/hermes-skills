#!/usr/bin/env python3
"""Check whether a provider's BATCH discount actually applies to a given model.

Answers three questions that docs and pricing pages do not:
  1. Does a real batch endpoint exist? (A 200 with 0 bytes is NOT an API.)
  2. Is the model you run flagged as batch-capable?
  3. If not, is the successor cheap tier (service_tier) accepted?

Usage:
    export PROV_KEY=...          # provider key
    python check_batch_support.py https://base-url/v1 deepseek-v4-flash
    python check_batch_support.py https://base-url/v1 deepseek-v4-flash --tier flex

Key is read from the environment only, never a literal, so the script is safe
to keep on disk after a paste-the-key session.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

UA = {
    "User-Agent": "openai-python/1.0",
    "Content-Type": "application/json",
}

BATCH_PATHS = ["/batches", "/batch", "/v1/batches"]


def call(url, key, method="GET", body=None, timeout=60):
    """Returns (status, body_bytes, headers). Never raises for HTTP errors."""
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        url, data=data, headers={**UA, "Authorization": f"Bearer {key}"}, method=method
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers)
    except Exception as e:  # noqa: BLE001 - probe must not die on one bad path
        return "ERR", str(e)[:200].encode(), {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base", help="API base URL, e.g. https://host/v1")
    ap.add_argument("model", help="the model you actually run")
    ap.add_argument("--tier", default="flex", help="successor cheap tier to test (default: flex)")
    ap.add_argument("--timeout", type=int, default=60)
    args = ap.parse_args()

    key = os.environ.get("PROV_KEY")
    if not key:
        sys.exit("Set PROV_KEY first (never pass the key as an argument).")

    base = args.base.rstrip("/")

    # --- Control: a known-real endpoint, for byte-count comparison ----------
    st, ref_body, _ = call(f"{base}/models", key, timeout=args.timeout)
    ref_len = len(ref_body)
    print(f"CONTROL  GET /models -> {st} ({ref_len} bytes)")
    if st != 200 or ref_len == 0:
        print("  Control failed. Base URL or key is wrong; fix that before reading anything else.")
        return 1
    print()

    # --- 1. Is there a real batch endpoint? --------------------------------
    print("1) BATCH ENDPOINT PROBE")
    print("   A 200 with 0 bytes is a registered route, NOT an API.")
    for p in BATCH_PATHS:
        url = f"{base}{p}" if not p.startswith("/v1") else f"{base.rsplit('/v1', 1)[0]}{p}"
        st, body, hdrs = call(url, key, timeout=args.timeout)
        n = len(body)
        declared = hdrs.get("Content-Length", "?")
        verdict = "REAL" if n > 0 else "not a real API" if st == 200 else "absent"
        print(f"   {st:>4} {n:>7} byte (Content-Length {declared:>7})  {verdict:<15} {url}")
    print()

    # --- 2. Per-model capability flags -------------------------------------
    print("2) PER-MODEL CAPABILITY FLAGS")
    try:
        catalogue = json.loads(ref_body).get("data", [])
    except Exception as e:  # noqa: BLE001
        print(f"   Could not parse /models ({e}); cannot check capability flags.")
        catalogue = []

    if not catalogue:
        print("   No 'data' list; some providers use a different shape. Inspect the raw response.\n")
    else:
        batch_models, cache_models = [], []
        for m in catalogue:
            f = (m.get("features") or {}) if isinstance(m, dict) else {}
            b = f.get("batch") or {}
            if b.get("batch_chat") or b.get("batch_job"):
                batch_models.append(m.get("id", "?"))
            c = f.get("cache") or {}
            if c.get("prefix_cache"):
                cache_models.append(m.get("id", "?"))
        print(f"   {len(catalogue)} models total | {len(batch_models)} batch-capable")
        if batch_models:
            print("   Batch-capable:")
            for i in range(0, len(batch_models), 3):
                print("     " + " | ".join(f"{x:<28}" for x in batch_models[i : i + 3]))
        target = next((m for m in catalogue if isinstance(m, dict) and m.get("id") == args.model), None)
        print()
        if target is None:
            print(f"   >>> '{args.model}' is NOT in this endpoint's catalogue.")
            print("       It is not 'batch unsupported' - it is not offered here at all.")
            print("       Do not infer a price or a capability for it from sibling models.")
        else:
            fb = (target.get("features") or {}).get("batch") or {}
            if fb.get("batch_chat") or fb.get("batch_job"):
                print(f"   >>> '{args.model}' IS batch-capable. Confirm the provider's real batch endpoint")
                print("       in their docs - an RPC-style SDK may post to '/' with the action in the body.")
            else:
                print(f"   >>> '{args.model}' is NOT batch-capable (batch={fb}).")
        if cache_models:
            print()
            print(f"   prefix_cache available on {len(cache_models)} models "
                  f"(chat-compatible discount, no file plumbing):")
            print("     " + ", ".join(cache_models[:10]) + (" ..." if len(cache_models) > 10 else ""))
    print()

    # --- 3. Successor cheap tier -------------------------------------------
    print(f"3) SUCCESSOR TIER  (service_tier={args.tier})")
    st, body, _ = call(
        f"{base}/chat/completions",
        key,
        method="POST",
        body={
            "model": args.model,
            "messages": [{"role": "user", "content": "1+1="}],
            "max_tokens": 20,
            "service_tier": args.tier,
        },
        timeout=args.timeout,
    )
    raw = body.decode(errors="replace")
    if st == 200:
        print(f"   {st} -> tier accepted. This is the discount path for an agent loop.")
    else:
        print(f"   {st} -> tier refused. {raw[:220]}")
        if "quota" in raw.lower():
            print("   NOTE: the refusal is a QUOTA error, not a capability error.")
            print("   Fix quota (or change model) before evaluating any cost optimisation.")
    print()
    print("Reminder: batch returns results out of band in files. Even where supported it does not")
    print("fit an interactive agent turn. For chat, prefix_cache is the applicable discount.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
