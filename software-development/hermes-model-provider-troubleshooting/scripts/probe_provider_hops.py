#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe sống từng hop trong chuỗi provider của Hermes (primary + fallback_providers).

Dùng khi cần biết hop nào CÒN SỐNG trước khi tin chuỗi fallback, hoặc sau khi đổi provider.
Đọc config.yaml thật, resolve base_url/api_key (inline, key_env, .env, providers, custom_providers),
gọi /chat/completions với max_tokens nhỏ, in HTTP status + latency. KHÔNG in key (mask).

Chạy:  python probe_provider_hops.py [--maxtok 16] [--timeout 40]

Đọc kết quả:
- HTTP 200            -> hop sống.
- 402 "more credits"   -> request lớn vượt balance; max_tokens nhỏ vẫn 200 => vô dụng cho agent thật.
- 429                  -> limit theo plan/thời gian; xem message có "resets at/in" để biết mốc hồi.
- 403 "error code: 1010" -> Cloudflare chặn UA lạ (probe thô), KHÔNG kết luận provider chết; phải test bằng agent thật.
- 404 InvalidEndpointOrModel -> sai endpoint/model; check bucket (/api/v3 vs /api/coding/v3...) hoặc tên model.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

try:
    import yaml
except Exception:  # pragma: no cover
    print("cần PyYAML: pip install pyyaml")
    sys.exit(2)


def home_dir() -> str:
    env = os.environ.get("HERMES_HOME")
    if env and os.path.isdir(env):
        return env
    local = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~/.local/share")
    for cand in (os.path.join(local, "hermes"), os.path.expanduser("~/.hermes")):
        if os.path.isfile(os.path.join(cand, "config.yaml")):
            return cand
    return os.path.join(local, "hermes")


def load_env(path: str) -> dict:
    env: dict = {}
    if not os.path.isfile(path):
        return env
    for line in open(path, encoding="utf-8", errors="ignore"):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def mask(v) -> str:
    v = str(v or "")
    if not v:
        return "-"
    return "len%d..%s" % (len(v), v[-4:]) if len(v) > 8 else "set"


def norm_base(u: str) -> str:
    u = (u or "").strip().rstrip("/")
    if u.endswith("/chat/completions"):
        return u
    return u + "/chat/completions"


def resolve(base_url, key, sentry: int = 0) -> tuple:
    """Điền base_url/key còn thiếu từ providers / custom_providers / .env."""
    return base_url, key


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--maxtok", type=int, default=16)
    ap.add_argument("--timeout", type=int, default=40)
    args = ap.parse_args()

    H = home_dir()
    cfg_path = os.path.join(H, "config.yaml")
    if not os.path.isfile(cfg_path):
        print("không thấy config.yaml ở", cfg_path)
        return 1
    cfg = yaml.safe_load(open(cfg_path, encoding="utf-8")) or {}
    env = load_env(os.path.join(H, ".env"))

    provs = dict(cfg.get("providers") or {})
    customs = {}
    for cp in (cfg.get("custom_providers") or []):
        if isinstance(cp, dict) and cp.get("name"):
            customs[str(cp["name"]).lower()] = cp

    def provider_cfg(name: str):
        n = str(name or "").strip()
        if n.lower().startswith("custom:"):
            return customs.get(n.split(":", 1)[1].lower()) or {}
        return provs.get(n) or {}

    def key_for(name: str) -> str:
        p = provider_cfg(name)
        inline = str(p.get("api_key") or "").strip()
        if inline and not inline.isupper():
            return inline
        ke = str(p.get("key_env") or p.get("api_key_env") or inline or "").strip()
        if ke and env.get(ke):
            return env[ke]
        guess = str(name).split(":")[-1].upper().replace("-", "_").replace(".", "_")
        for cand in (f"{guess}_API_KEY", f"HERMES_CUSTOM_{guess}_API_KEY"):
            if env.get(cand):
                return env[cand]
        return ""

    # --- danh sách candidate: primary + từng hop fallback ---
    cands = []
    m = cfg.get("model") or {}
    if m.get("default"):
        cands.append(("PRIMARY", m.get("provider"), m.get("base_url"), m.get("default"), None))
    for i, e in enumerate(cfg.get("fallback_providers") or [], 1):
        if isinstance(e, dict):
            cands.append((f"hop {i}", e.get("provider"), e.get("base_url"), e.get("model"), e))
    if not cands:
        print("⚠ fallback_providers RỖNG hoặc sai định dạng (string thay vì list) -> chuỗi fallback chết.")

    print("config:", cfg_path)
    print("primary:", m.get("default"), "|", m.get("provider"), "|", m.get("base_url"))
    print()
    print("%-8s %-34s %-42s %-6s %s" % ("VAI", "PROVIDER", "MODEL", "HTTP", "GHI CHÚ"))
    print("-" * 120)

    for role, provider, base_url, model, entry in cands:
        p = provider_cfg(provider)
        base_url = (base_url or p.get("base_url") or "").strip()
        key = ""
        if isinstance(entry, dict):
            inl = str(entry.get("api_key") or "").strip()
            ke = str(entry.get("key_env") or entry.get("api_key_env") or "").strip()
            key = inl if inl else (env.get(ke, "") if ke else "")
        key = key or key_for(provider)
        if not base_url or not model:
            print("%-8s %-34s %-42s %-6s %s" % (role, str(provider)[:34], str(model)[:42], "-", "thiếu base_url/model"))
            continue
        url = norm_base(base_url)
        body = json.dumps({"model": model, "messages": [{"role": "user", "content": "ok"}],
                           "max_tokens": args.maxtok}).encode()
        req = urllib.request.Request(url, data=body, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + key,
            "User-Agent": "hermes",
        })
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=args.timeout) as r:
                r.read()
                print("%-8s %-34s %-42s %-6s %.1fs key=%s" % (role, str(provider)[:34], str(model)[:42], r.status, time.time() - t0, mask(key)))
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:150].replace("\n", " ")
            note = ""
            if "1010" in msg:
                note = "cloudflare UA block -> test lại bằng agent thật"
            elif "401" != str(e.code) and "credits" in msg.lower():
                note = "request lớn vượt balance (max_tokens nhỏ có thể qua)"
            print("%-8s %-34s %-42s %-6s %.1fs key=%s | %s %s" % (role, str(provider)[:34], str(model)[:42], e.code, time.time() - t0, mask(key), msg, note))
        except Exception as e:
            print("%-8s %-34s %-42s %-6s %.1fs key=%s | %s" % (role, str(provider)[:34], str(model)[:42], "FAIL", time.time() - t0, mask(key), str(e)[:90]))

    print()
    print("Nhắc: probe 200 chỉ là ứng viên. Bằng chứng cuối cùng phải là lượt agent thật;")
    print("đọc hop đã phục vụ trong state.db: select billing_provider, billing_base_url from sessions order by started_at desc limit 3;")
    return 0


if __name__ == "__main__":
    sys.exit(main())
