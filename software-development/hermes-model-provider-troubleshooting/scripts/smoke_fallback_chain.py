#!/usr/bin/env python3
"""Smoke-test EVERY hop of Hermes' fallback chain with a real 1-token completion.

Why: a chain that looks perfect in config.yaml can have ZERO live hops.
Model-alive != provider-usable. Real failures found this way (2026-10-05):
  opencode-zen free tier -> 403 "can only be used from within OpenCode"
  opencode-go            -> 403 "active OpenCode Go subscription is required"
  gemini-2.5-flash       -> 404 "no longer available to new users"
  ark (byteplus)         -> 429 AccountQuotaExceeded  (resets on a stated date)

Reads the chain from top-level `fallback_providers` ONLY. Note that the nested
`model.fallback_providers` block is DEAD CONFIG that Hermes never reads -- if it
exists, this script warns so you know the config is lying to you.

Usage:
    python smoke_fallback_chain.py [--home <HERMES_HOME>] [--timeout 45]
                                   [--chain primary] [--json]

Exit code: 0 = every hop answered, 1 = at least one hop failed (chain has dead
hops), 2 = config/credentials unreadable. Safe to run in CI/cron as a watchdog:
run it and assert exit 0.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

try:
    import yaml
except ImportError:
    print("need pyyaml: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

# Built-in provider -> (base_url, env var holding the key).
BUILTIN = {
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY"),
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai", "GOOGLE_API_KEY"),
    "google": ("https://generativelanguage.googleapis.com/v1beta/openai", "GOOGLE_API_KEY"),
    "groq": ("https://api.groq.com/openai/v1", "GROQ_API_KEY"),
    "deepseek": ("https://api.deepseek.com/v1", "DEEPSEEK_API_KEY"),
    "nvidia": ("https://integrate.api.nvidia.com/v1", "NVIDIA_API_KEY"),
    "xai": ("https://api.x.ai/v1", "XAI_API_KEY"),
    "zai": ("https://api.z.ai/api/paas/v4", "GLM_API_KEY"),
    "minimax": ("https://api.minimax.io/v1", "MINIMAX_API_KEY"),
    "kimi-coding": ("https://api.moonshot.ai/v1", "KIMI_API_KEY"),
    "opencode-zen": ("https://opencode.ai/zen/v1", "OPENCODE_ZEN_API_KEY"),
    "opencode-go": ("https://opencode.ai/zen/go/v1", "OPENCODE_GO_API_KEY"),
    "command-code": ("https://api.commandcode.ai/provider/v1", "HERMES_CUSTOM_COMMAND_CODE_API_KEY"),
    "commandcode": ("https://api.commandcode.ai/provider/v1", "COMMANDCODE_API_KEY"),
}

UA = "HermesAgent/1.0 (fallback-chain-smoke-test)"


def default_home() -> str:
    if os.environ.get("HERMES_HOME"):
        return os.environ["HERMES_HOME"]
    if os.name == "nt":
        return os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes")
    return os.path.expanduser("~/.hermes")


def load_env(home: str) -> dict[str, str]:
    """.env is credentials-only. Strip surrounding quotes -- a quoted key is a
    real bug (Hermes sends it verbatim and the server 401s)."""
    env: dict[str, str] = {}
    path = os.path.join(home, ".env")
    if not os.path.exists(path):
        return env
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def resolve(entry: dict, home_env: dict, custom: dict[str, dict]) -> tuple[str, str, str]:
    """-> (base_url, api_key, note). Handles native / custom / custom:<name>."""
    provider = str(entry.get("provider") or "").strip()
    note = ""

    if provider == "custom":
        base = str(entry.get("base_url") or "").strip()
        key = ""
        key_env = str(entry.get("key_env") or entry.get("api_key_env") or "").strip()
        if key_env:
            key = home_env.get(key_env, "")
            if not key:
                note = f"key_env {key_env} not set in .env"
        if not key:
            key = str(entry.get("api_key") or "").strip()
        return base, key, note

    if provider.startswith("custom:"):
        want = provider.split(":", 1)[1].strip().lower()
        hit = custom.get(want)
        if not hit:
            return "", "", f"no custom_providers entry named '{want}'"
        base = str(hit.get("base_url") or "").strip()
        key = str(hit.get("api_key") or "").strip()
        if not key:
            key_env = str(hit.get("key_env") or "").strip()
            key = home_env.get(key_env, "") if key_env else ""
            if not key and key_env:
                note = f"key_env {key_env} not set in .env"
        return base, key, note

    base, envname = BUILTIN.get(provider, ("", ""))
    if not base:
        # last resort: providers.<name>.base_url declared in config
        return "", "", f"unknown provider '{provider}' (no builtin mapping; add it to BUILTIN)"
    return base, home_env.get(envname, ""), ("" if home_env.get(envname) else f"{envname} not set in .env")


def probe(base: str, key: str, model: str, timeout: int) -> str:
    if not base:
        return "FAIL no base_url"
    body = json.dumps(
        {"model": model, "messages": [{"role": "user", "content": "hi"}], "max_tokens": 1}
    ).encode()
    headers = {"Content-Type": "application/json", "User-Agent": UA}
    if key:
        headers["Authorization"] = "Bearer " + key
    req = urllib.request.Request(base.rstrip("/") + "/chat/completions",
                                 data=body, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8", "replace"))
        if not payload.get("choices"):
            return "WARN 200 but no choices (router/malformed?)"
        return "OK"
    except urllib.error.HTTPError as exc:
        detail = ""
        try:
            detail = exc.read().decode("utf-8", "replace")[:200].replace("\n", " ")
        except Exception:
            pass
        hint = ""
        low = detail.lower()
        if exc.code == 429:
            hint = "  <- rate/quota, often temporary"
        elif exc.code in (401, 402, 403):
            hint = "  <- auth/entitlement/funds"
        elif exc.code == 404:
            hint = "  <- model id likely retired; try a -latest alias"
        return f"FAIL HTTP {exc.code}: {detail}{hint}"
    except Exception as exc:  # noqa: BLE001
        return f"FAIL {type(exc).__name__}: {exc}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--home", default=default_home())
    ap.add_argument("--timeout", type=int, default=45)
    ap.add_argument("--chain", default="fallback_providers",
                    help="config key to test (default: fallback_providers)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    cfg_path = os.path.join(args.home, "config.yaml")
    if not os.path.exists(cfg_path):
        print(f"config not found: {cfg_path}", file=sys.stderr)
        return 2

    with open(cfg_path, encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh) or {}

    home_env = load_env(args.home)
    custom = {
        str(c.get("name", "")).strip().lower(): c
        for c in (cfg.get("custom_providers") or [])
        if isinstance(c, dict)
    }

    chain = cfg.get(args.chain) or []
    if isinstance(chain, dict):
        chain = [chain]

    dead = (cfg.get("model") or {}).get("fallback_providers")
    if dead:
        print("WARNING: `model.fallback_providers` exists but Hermes NEVER reads it "
              f"(dead config, {len(dead)} entries). Delete it; keep only the top-level key.")
    if not chain:
        print(f"no entries under `{args.chain}` -- fallback chain is EMPTY "
              "(Hermes will report 'No fallback providers configured').")
        return 2

    results = []
    print(f"chain `{args.chain}` from {cfg_path}")
    print(f"{'#':>2}  {'provider':<44} {'model':<38} result")
    for i, entry in enumerate(chain, 1):
        if not isinstance(entry, dict):
            continue
        provider = str(entry.get("provider") or "?")
        model = str(entry.get("model") or "?")
        base, key, note = resolve(entry, home_env, custom)
        if note and not base:
            outcome = f"FAIL {note}"
        else:
            outcome = probe(base, key, model, args.timeout)
            if note:
                outcome += f"  ({note})"
        results.append({"n": i, "provider": provider, "model": model,
                        "base_url": base, "result": outcome})
        print(f"{i:>2}  {provider:<44} {model:<38} {outcome}")

    live = sum(1 for r in results if r["result"].startswith(("OK", "WARN")))
    if args.json:
        print(json.dumps({"live": live, "total": len(results), "hops": results},
                         ensure_ascii=False, indent=2))

    print(f"\n{live}/{len(results)} hops answered.")
    if live == 0:
        print("CHAIN IS DEAD: every hop failed. Fix before trusting fallback.")
    elif live < len(results):
        print("Some hops are dead: each one costs a wasted round-trip before the "
              "next is tried. Remove or reorder them.")
    return 0 if live == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
