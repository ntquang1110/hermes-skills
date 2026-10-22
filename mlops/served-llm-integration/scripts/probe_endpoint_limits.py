#!/usr/bin/env python3
"""Probe an OpenAI-compatible endpoint for real rate limits and saturation behaviour.

Answers the questions you actually need before wiring an endpoint into a cron:
  - how many concurrent requests survive?
  - what is the practical requests/minute?
  - how long until a saturated endpoint recovers?

Usage:
    export NVIDIA_API_KEY=nvapi-...            # or any provider key
    python probe_endpoint_limits.py \
        --base-url https://integrate.api.nvidia.com/v1 \
        --model nvidia/nemotron-3-nano-omni-30b-a3b-reasoning \
        --env-var NVIDIA_API_KEY

Design notes (learned the hard way):
  - Keeps the key in an env var. Never hardcode it; these scripts end up on disk.
  - Waits between phases so a shared pool can drain. Without the waits the numbers
    measure your own backlog, not the provider's limit.
  - Prints the raw 503 body. On NVIDIA NIM that body contains the shared-pool
    counter (e.g. "1902/16"), which is the only way to tell a per-key limit from a
    global one.
  - Deliberately uses tiny max_tokens: this measures request-rate limits, not
    generation speed. Use a separate throughput test for tok/s.
"""

import argparse
import concurrent.futures as cf
import json
import os
import sys
import time
import urllib.error
import urllib.request


def one(base_url, model, key, tag):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "1+1=?"}],
        "max_tokens": 8,
        "temperature": 0,
    }
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            json.load(r)
        return (tag, "200", time.perf_counter() - t0, None)
    except urllib.error.HTTPError as e:
        return (tag, str(e.code), time.perf_counter() - t0, e.read()[:200].decode(errors="replace"))
    except Exception as e:
        return (tag, "ERR", time.perf_counter() - t0, f"{type(e).__name__}: {str(e)[:150]}")


def burst(args, key, n):
    print(f"\n--- concurrency {n}: firing {n} at once ---", flush=True)
    with cf.ThreadPoolExecutor(max_workers=n) as ex:
        res = list(ex.map(lambda i: one(args.base_url, args.model, key, i), range(n)))
    ok = sum(1 for r in res if r[1] == "200")
    codes = {}
    for r in res:
        codes[r[1]] = codes.get(r[1], 0) + 1
    slowest = max((r[2] for r in res), default=0.0)
    print(f"    ok {ok}/{n} | codes {codes} | slowest {slowest:.1f}s", flush=True)
    for r in res:
        if r[1] != "200":
            print(f"    sample error body: {r[3]}", flush=True)
            break
    # A 4-wide burst failing while a 16-wide burst passes means a SHARED pool,
    # not a per-key concurrency cap. Read the counter in the error body to confirm.
    return ok, n


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base-url", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--env-var", default="API_KEY")
    p.add_argument("--bursts", default="2,4,8,16", help="comma-separated concurrency levels")
    p.add_argument("--wait", type=int, default=60, help="seconds between phases")
    args = p.parse_args()

    key = os.environ.get(args.env_var)
    if not key:
        sys.exit(f"error: env var {args.env_var} is not set")

    print("=== phase 0: sanity — single request ===", flush=True)
    r = one(args.base_url, args.model, key, "sanity")
    print(f"    {r[1]} in {r[2]:.2f}s" + (f" | {r[3]}" if r[3] else ""), flush=True)
    if r[1] != "200":
        print("    endpoint not answering; aborting", flush=True)
        return

    print("\n=== phase 1: concurrency threshold ===", flush=True)
    for n in (int(x) for x in args.bursts.split(",")):
        burst(args, key, n)
        time.sleep(args.wait)
        print(f"    (slept {args.wait}s so the pool can drain)", flush=True)

    print("\n=== phase 2: practical requests/minute (sequential, 1s apart) ===", flush=True)
    ok = i = 0
    codes = {}
    t0 = time.perf_counter()
    while time.perf_counter() - t0 < 60:
        i += 1
        r = one(args.base_url, args.model, key, f"seq{i}")
        codes[r[1]] = codes.get(r[1], 0) + 1
        if r[1] == "200":
            ok += 1
        time.sleep(1)
    el = time.perf_counter() - t0
    print(f"    sent {i} in {el:.0f}s | ok {ok} | codes {codes}", flush=True)
    print(f"    => practical ceiling ~{ok / (el / 60):.1f} req/min", flush=True)

    print("\n=== phase 3: recovery time after saturation ===", flush=True)
    burst(args, key, 16)
    waited = 0
    for step in (15, 15, 30, 60, 120):
        time.sleep(step)
        waited += step
        r = one(args.base_url, args.model, key, "probe")
        print(f"    after {waited}s cumulative: {r[1]}", flush=True)
        if r[1] == "200":
            print("    => recovered", flush=True)
            break

    print("\nReminder: if phase 1 is non-monotonic (4 fails, 16 passes), the limit is a")
    print("shared pool. Cap concurrency at 1-2 and wrap calls in retry-with-backoff.")


if __name__ == "__main__":
    main()
