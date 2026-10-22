# -*- coding: utf-8 -*-
"""Merge a hostname into an API-managed Cloudflare tunnel ingress (config_src: cloudflare).

Usage:
    CF_TOKEN=<token> python add-cf-ingress.py <ACCOUNT_ID> <TUNNEL_ID> <hostname> <service>

Example:
    CF_TOKEN=$(python -c "...decode cert.pem...") python add-cf-ingress.py \
        7aa3945509f3a3c90b75fca0317e7e5b 0ce9aa47-... dithi.thefirstonly.com http://localhost:5100

Reads current config, merges the new rule BEFORE the catch-all (http_status:404 must stay last),
PUTs, then re-GETs to verify. Never rebuilds config from memory (external edits bump version).
"""
import json, os, sys, urllib.request, urllib.error

TOKEN = os.environ.get("CF_TOKEN")
if not TOKEN:
    sys.exit("Missing CF_TOKEN env var (decode from ~/.cloudflared/cert.pem)")
if len(sys.argv) != 5:
    sys.exit("Usage: add-cf-ingress.py <ACCOUNT_ID> <TUNNEL_ID> <hostname> <service>")

ACCOUNT, TUNNEL, HOST, SERVICE = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/cfd_tunnel/{TUNNEL}/configurations"

def cf(method, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(URL, data=data, method=method,
                                 headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=40))
    except urllib.error.HTTPError as e:
        try:
            return json.load(e)
        except Exception:
            return {"errors": [{"message": f"HTTP {e.code}"}]}

d = cf("GET")
if not d.get("success"):
    print("GET ERR:", d.get("errors")); sys.exit(1)
cur = d["result"]["config"]
ing = cur["ingress"]

if any(i.get("hostname") == HOST for i in ing):
    print("dithi ingress ALREADY EXISTS, skip")
else:
    ing.insert(len(ing) - 1, {"hostname": HOST, "service": SERVICE})
    payload = {"config": {"ingress": ing, "warp-routing": cur.get("warp-routing", {"enabled": False})}}
    d2 = cf("PUT", payload)
    print("PUT success:", d2.get("success"), "| version:", d2.get("result", {}).get("version") if d2.get("result") else None)
    if not d2.get("success"):
        print("PUT ERR:", d2.get("errors")); sys.exit(1)

d3 = cf("GET")
if d3.get("success"):
    for i in d3["result"]["config"]["ingress"]:
        if i.get("hostname") == HOST:
            print("VERIFY ok:", i["hostname"], "->", i["service"])
            sys.exit(0)
    print("VERIFY FAILED: hostname not found after PUT"); sys.exit(1)
