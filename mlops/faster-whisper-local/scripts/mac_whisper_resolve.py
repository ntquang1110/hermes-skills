#!/usr/bin/env python3
"""
Locate a DHCP-addressed LAN service (default: Mac Whisper on :9000) without a
hardcoded IP.

Resolution order:
  1. mDNS hostname (Bonjour)  - survives DHCP IP changes
  2. cached last-good IP      - fast path, verified reachable before use
  3. parallel /24 sweep       - finds the host wherever it moved

Deployed at ~/.hermes/scripts/mac_whisper_resolve.py and imported by
watchdog_mac_whisper.py, stt_mac_wrapper.py, stt_mac_local.py. Copy this file
next to any callers that hardcode a LAN IP; call resolve() instead of the literal.

Run directly to diagnose:
    python mac_whisper_resolve.py --force
"""

import concurrent.futures
import json
import os
import socket
import sys
import time

# --- adjust per host -------------------------------------------------------
HOSTNAMES = [
    "Mac-mini-cua-kiem.local",
    "mac-mini-cua-kiem.local",
    "Mac-mini-cua-kiem",
]
PORT = 9000
LAN_PREFIX = "192.168.1."
# ---------------------------------------------------------------------------

CACHE = os.path.join(os.path.expanduser("~"), "AppData", "Local", "hermes",
                     "scripts", ".mac_whisper_ip")


def _reachable(ip, port=PORT, tmo=1.5):
    """True when something accepts a TCP connection on ip:port."""
    s = socket.socket()
    s.settimeout(tmo)
    try:
        return s.connect_ex((ip, port)) == 0
    except Exception:
        return False
    finally:
        s.close()


def _from_hostname():
    for h in HOSTNAMES:
        try:
            ip = socket.gethostbyname(h)
            if ip and _reachable(ip):
                return ip
        except Exception:
            continue
    return None


def _from_cache():
    try:
        with open(CACHE) as f:
            ip = f.read().strip()
        if ip and _reachable(ip, tmo=1.0):
            return ip
    except Exception:
        pass
    return None


def _from_sweep():
    def scan(i):
        ip = LAN_PREFIX + str(i)
        return ip if _reachable(ip, tmo=0.8) else None

    with concurrent.futures.ThreadPoolExecutor(max_workers=80) as ex:
        for r in ex.map(scan, range(1, 255)):
            if r:
                return r
    return None


def _save(ip):
    try:
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        with open(CACHE, "w") as f:
            f.write(ip)
    except Exception:
        pass


def resolve(force=False, verbose=False):
    """Return the service host IP, or None if not found.

    force=True skips the cache - use it from a watchdog so a host that moved
    is re-found on the very next tick instead of trusting a stale address.
    """
    if not force:
        ip = _from_cache()
        if ip:
            if verbose:
                print(f"[resolve] cache -> {ip}")
            return ip

    ip = _from_hostname()
    if ip:
        _save(ip)
        if verbose:
            print(f"[resolve] hostname -> {ip}")
        return ip

    t0 = time.time()
    ip = _from_sweep()
    if ip:
        _save(ip)
    if verbose:
        print(f"[resolve] sweep -> {ip} ({time.time() - t0:.1f}s)")
    return ip


def base_url():
    ip = resolve()
    return f"http://{ip}:{PORT}" if ip else None


if __name__ == "__main__":
    import urllib.request

    ip = resolve(force="--force" in sys.argv, verbose=True)
    if not ip:
        print(f"service NOT FOUND on {LAN_PREFIX}0/24 (port {PORT})")
        sys.exit(1)
    try:
        with urllib.request.urlopen(f"http://{ip}:{PORT}/health", timeout=8) as r:
            print("health:", r.status, json.loads(r.read().decode()))
    except Exception as e:
        print(f"found {ip} but /health failed: {e}")
        sys.exit(1)
