#!/usr/bin/env python
"""Unsloth Studio control plane: inspect / load / unload / restore models.

Why this exists: Unsloth Studio exposes a documented management API alongside
its OpenAI-compatible one (spec at /openapi.json). Loading a model with the
right memory strategy is fiddly enough that hand-rolling it per session wastes
time and risks leaving someone's server with zero models loaded.

Usage
-----
  export UNSLOTH_BASE=https://pharma-llm.example.com
  export UNSLOTH_API_KEY=sk-unsloth-...

  # What is this box, what is loaded, what quants exist?
  python unsloth_control.py info
  python unsloth_control.py variants unsloth/Ministral-3-3B-Reasoning-2512-GGUF

  # Load everything into system RAM (CPU inference)
  python unsloth_control.py load <repo> --ram --ctx 16384

  # Load with a specific quant, some layers on GPU
  python unsloth_control.py load <repo> --variant Q8_0 --gpu-layers 20

  # Snapshot before touching anything, then put it back later
  python unsloth_control.py snapshot --out state.json
  python unsloth_control.py restore --from state.json

  # Streaming smoke test (proves it actually decodes)
  python unsloth_control.py test <repo>

Notes
-----
* Always sends a User-Agent. Cloudflare's browser-signature rule 403s the
  default Python-urllib UA on this stack.
* gpu_layers is IGNORED unless gpu_memory_mode is "manual". --ram sets both.
* An empty unload body returns HTTP 400, so model_path is always sent.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = os.environ.get("UNSLOTH_BASE", "").rstrip("/")
KEY = os.environ.get("UNSLOTH_API_KEY", "")
UA = "openai-python/1.0"          # Python-urllib default is 403'd by Cloudflare


def _call(method: str, path: str, payload=None, timeout: int = 240):
    """Return (status, body_text). Never raises on HTTP errors."""
    if not BASE:
        sys.exit("Set UNSLOTH_BASE (e.g. https://pharma-llm.example.com)")
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        BASE + path,
        data=data,
        headers={"Authorization": "Bearer " + KEY,
                 "Content-Type": "application/json",
                 "User-Agent": UA},
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:
        return None, "%s: %s" % (type(e).__name__, e)


def _json(method: str, path: str, payload=None, timeout: int = 240):
    st, body = _call(method, path, payload, timeout)
    try:
        return st, json.loads(body)
    except Exception:
        return st, body


def loaded_ids():
    st, d = _json("GET", "/api/inference/loaded-models", timeout=40)
    if isinstance(d, dict):
        return [m.get("id") for m in d.get("data", [])]
    return []


def wait_for(model: str, timeout: int = 420) -> bool:
    """Poll until `model` is resident. loaded-models is the reliable signal."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        ids = loaded_ids()
        print("  ... loaded: %s" % (ids or "[]"), flush=True)
        if model in ids:
            return True
        time.sleep(12)
    return False


# --------------------------------------------------------------------------- #

def cmd_info(_a):
    st, d = _json("GET", "/api/system")
    if not isinstance(d, dict):
        print("GET /api/system ->", st, d)
    else:
        m, g = d.get("memory", {}), d.get("gpu", {})
        print("host      : %s | cpu %s threads" % (d.get("platform"), d.get("cpu_count")))
        print("ram       : %.2f / %.2f GB free (%.1f%% used)"
              % (m.get("available_gb", 0), m.get("total_gb", 0), m.get("percent_used", 0)))
        for dev in g.get("devices", []):
            print("gpu       : %s | vram free %.2f / %.2f GB | util %s%%"
                  % (dev.get("name"), dev.get("vram_free_gb", 0),
                     dev.get("memory_total_gb", 0), dev.get("gpu_utilization_pct")))

    st, model = _json("GET", "/api/inference/loaded-models", timeout=40)
    print("\nloaded models:")
    for m in (model.get("data", []) if isinstance(model, dict) else []):
        print("  - %s | quant %s | ctx %s (max %s, native %s)"
              % (m.get("id"), m.get("quant"), m.get("context_length"),
                 m.get("max_context_length"), m.get("native_context_length")))

    st, mem = _json("GET", "/api/settings/model-memory", timeout=40)
    if isinstance(mem, dict):
        print("\nmemory settings: keep_resident=%s no_ram_reserve=%s mlock_active=%s"
              % (mem.get("keep_resident"), mem.get("no_ram_reserve"), mem.get("mlock_active")))

    st, props = _json("GET", "/props", timeout=40)
    if isinstance(props, dict):
        print("llama.cpp : alias=%s ftype=%s slots=%s is_sleeping=%s"
              % (props.get("model_alias"), props.get("model_ftype"),
                 props.get("total_slots"), props.get("is_sleeping")))


def cmd_variants(a):
    st, d = _json("GET", "/api/models/gguf-variants?repo_id=" + a.repo, timeout=90)
    if not isinstance(d, dict):
        print("->", st, d)
        return
    for v in d.get("variants", []):
        print("  %-14s %10.2f GB  downloaded=%s  %s"
              % (v.get("quant"), (v.get("size_bytes") or 0) / 1e9,
                 v.get("downloaded"), v.get("filename")))


def cmd_snapshot(a):
    st, model = _json("GET", "/api/inference/loaded-models", timeout=40)
    data = model.get("data", []) if isinstance(model, dict) else []
    snap = {"taken": time.strftime("%Y-%m-%dT%H:%M:%S"), "loaded": [
        {"model_path": m.get("id"), "gguf_variant": m.get("quant"),
         "context_length": m.get("context_length")} for m in data]}
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(snap, f, indent=2)
    print(json.dumps(snap, indent=2))
    print("\nwrote", a.out, "- restore with: restore --from", a.out)


def _do_load(repo, variant=None, ram=False, gpu_layers=None, ctx=16384,
             force=False, timeout=300):
    p = {"model_path": repo, "load_in_4bit": False, "force_reload": force}
    if variant:
        p["gguf_variant"] = variant
    if ram:
        # BOTH are required: "manual" is what makes gpu_layers respected.
        p["gpu_memory_mode"] = "manual"
        p["gpu_layers"] = 0
        p["cpu_fallback"] = True
        p["load_mode"] = "mlock"        # keep in RAM, don't swap/compress
        p["max_seq_length"] = ctx
        p["disable_vision"] = True
    elif gpu_layers is not None:
        p["gpu_memory_mode"] = "manual"
        p["gpu_layers"] = gpu_layers
        p["max_seq_length"] = ctx
    st, body = _call("POST", "/v1/load", p, timeout=timeout)
    if st == 200 and "_deferred_error" not in body:
        print("load accepted:", body[:200])
        return True
    print("LOAD FAILED (HTTP %s)" % st)
    print(body[:2500])
    print("\nRead the 'llama-server output' section. If the error is raised at "
          "context creation and identical across memory configs, it is an "
          "architecture incompatibility, not a memory problem.")
    return False


def cmd_load(a):
    ok = _do_load(a.repo, a.variant, a.ram, a.gpu_layers, a.ctx, a.force)
    if ok:
        print("\nwaiting for residency...")
        print("=> READY" if wait_for(a.repo) else "=> TIMED OUT waiting for load")


def cmd_unload(a):
    if loaded_ids() == [a.repo] and not a.yes:
        print("REFUSING: %s is the ONLY loaded model. Unloading leaves the "
              "endpoint with zero models and every request will 404." % a.repo)
        print("Re-run with --yes if that is genuinely what you want.")
        return
    st, body = _call("POST", "/v1/unload",
                     {"model_path": a.repo, "force_cancel_active": True}, timeout=120)
    print("unload HTTP %s: %s" % (st, body[:300]))


def cmd_restore(a):
    with open(a.src, encoding="utf-8") as f:
        snap = json.load(f)
    for m in snap.get("loaded", []):
        print("restoring %s (variant %s)" % (m["model_path"], m.get("gguf_variant")))
        if not _do_load(m["model_path"], m.get("gguf_variant"), force=False):
            print("  !! restore failed for", m["model_path"])
    print("\nwaiting...")
    for m in snap.get("loaded", []):
        wait_for(m["model_path"])
    print("\nverify quant matches the snapshot:")
    cmd_info(a)


def cmd_test(a):
    """Streaming smoke test. Non-streaming 524s through Cloudflare."""
    body = json.dumps({"model": a.repo,
                       "messages": [{"role": "user",
                                     "content": "Tra loi ngan gon: 2+2 bang may?"}],
                       "max_tokens": a.max_tokens, "temperature": 0.3,
                       "stream": True}).encode()
    req = urllib.request.Request(BASE + "/v1/chat/completions", data=body,
                                 headers={"Authorization": "Bearer " + KEY,
                                          "Content-Type": "application/json",
                                          "User-Agent": UA})
    t0 = time.time()
    buf, n, first = "", 0, None
    try:
        with urllib.request.urlopen(req, timeout=a.timeout) as r:
            for raw in r:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:"):
                    continue
                pl = line[5:].strip()
                if pl == "[DONE]":
                    break
                try:
                    j = json.loads(pl)
                except Exception:
                    continue
                piece = j.get("choices", [{}])[0].get("delta", {}).get("content") or ""
                if piece and first is None:
                    first = time.time() - t0
                buf += piece
                n += 1
    except Exception as e:
        print("ERROR after %.1fs: %s: %s" % (time.time() - t0, type(e).__name__, e))
        return
    dt = time.time() - t0
    closed = "\u003c/think\u003e" in buf
    print("%.1fs | %d chunks | %.1f tok/s | TTFB %s | exited think-block: %s"
          % (dt, n, n / dt if dt else 0,
             ("%.1fs" % first) if first else "n/a", closed))
    if not closed:
        print("  !! never left the think block -> unbounded reasoning, "
              "raise max_tokens and keep a fallback")
    _report_placement(n / dt if dt else 0)
    print("\nanswer:\n" + (buf.split("\u003c/think\u003e")[-1].strip() or "(empty)"))


def _report_placement(tok_per_s: float):
    """Say whether the model is actually on the GPU.

    The quietest failure on a served box is a quant that does not fit VRAM
    falling back to CPU: it still answers, just ~5x slower. Near-zero VRAM
    in use while a model is resident means you are on the CPU path.
    """
    st, d = _json("GET", "/api/system", timeout=40)
    if not isinstance(d, dict):
        return
    devs = d.get("gpu", {}).get("devices", [])
    if not devs:
        print("placement : no GPU reported -> CPU-only host")
        return
    for dev in devs:
        used = dev.get("vram_used_gb") or 0
        total = dev.get("memory_total_gb") or 0
        print("placement : %s | vram %.2f / %.2f GB in use"
              % (dev.get("name"), used, total))
        if used < 0.5:
            print("  !! ~no VRAM in use -> this quant did NOT fit and is "
                  "running on CPU. Expect ~5x slower than GPU-resident. "
                  "Try a smaller gguf_variant (e.g. UD-Q4_K_XL) before "
                  "accepting this throughput as the model's ceiling.")
        elif tok_per_s and tok_per_s < 25 and used < 1.5:
            print("  !! low tok/s with little VRAM used -> verify placement "
                  "before quoting this number as the model's speed.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("info").set_defaults(fn=cmd_info)

    p = sub.add_parser("variants"); p.add_argument("repo"); p.set_defaults(fn=cmd_variants)

    p = sub.add_parser("snapshot"); p.add_argument("--out", default="unsloth_state.json")
    p.set_defaults(fn=cmd_snapshot)

    p = sub.add_parser("load"); p.add_argument("repo")
    p.add_argument("--variant", help="e.g. Q8_0 -- omit and you may get a different quant")
    p.add_argument("--ram", action="store_true", help="all layers in system RAM (CPU)")
    p.add_argument("--gpu-layers", type=int, default=None)
    p.add_argument("--ctx", type=int, default=16384)
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_load)

    p = sub.add_parser("unload"); p.add_argument("repo")
    p.add_argument("--yes", action="store_true")
    p.set_defaults(fn=cmd_unload)

    p = sub.add_parser("restore"); p.add_argument("--from", dest="src", required=True)
    p.set_defaults(fn=cmd_restore)

    p = sub.add_parser("test"); p.add_argument("repo")
    p.add_argument("--max-tokens", type=int, default=4000)
    p.add_argument("--timeout", type=int, default=280)
    p.set_defaults(fn=cmd_test)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
