# -*- coding: utf-8 -*-
"""Create CNAME for a tunnel subdomain in the EXACT zone, then verify DNS.

Usage:
    CF_TOKEN=<token> python add-cf-dns.py <ZONE_NAME> <subdomain> <TUNNEL_ID>

Example:
    CF_TOKEN=... python add-cf-dns.py thefirstonly.com dithi 0ce9aa47-7d52-4d6a-9a16-13b48c508cff

Pitfall handled: resolves the zone by NAME (never uses cert.pem's zoneID — that often
belongs to a DIFFERENT zone, e.g. cert.pem carries theliems.com while you want
thefirstonly.com). Creates CNAME sub.<zone> -> <TUNNEL_ID>.cfargotunnel.com (proxied).
"""
import json, os, sys, urllib.request, urllib.error, socket

TOKEN = os.environ.get("CF_TOKEN")
if not TOKEN:
    sys.exit("Missing CF_TOKEN env var (decode from ~/.cloudflared/cert.pem)")
if len(sys.argv) != 4:
    sys.exit("Usage: add-cf-dns.py <ZONE_NAME> <subdomain> <TUNNEL_ID>")

ZONE, SUB, TUNNEL = sys.argv[1], sys.argv[2], sys.argv[3]
API = "https://api.cloudflare.com/client/v4"

def cf(url, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=40))
    except urllib.error.HTTPError as e:
        try:
            return json.load(e)
        except Exception:
            return {"errors": [{"message": f"HTTP {e.code}"}]}

z = cf(f"{API}/zones?name={ZONE}")
if not z.get("success") or not z["result"]:
    print("ZONE ERR:", z.get("errors")); sys.exit(1)
ZONE_ID = z["result"][0]["id"]
print("Zone:", ZONE, "->", ZONE_ID)

existing = cf(f"{API}/zones/{ZONE_ID}/dns_records?name={SUB}.{ZONE}")
if existing.get("success") and existing["result"]:
    rec = existing["result"][0]
    print("CNAME ALREADY EXISTS:", rec["name"], "->", rec["content"], f"(id {rec['id']})")
else:
    body = {"type": "CNAME", "name": SUB, "content": f"{TUNNEL}.cfargotunnel.com", "ttl": 1, "proxied": True}
    d = cf(f"{API}/zones/{ZONE_ID}/dns_records", "POST", body)
    if not d.get("success"):
        print("POST ERR:", d.get("errors")); sys.exit(1)
    rec = d["result"]
    print("CNAME created:", rec["name"], "->", rec["content"], f"(id {rec['id']})")

# DNS propagation takes 1-5 min; resolution failing right after create is NORMAL
try:
    ips = socket.gethostbyname_ex(f"{SUB}.{ZONE}")[2]
    print("DNS resolve:", ips)
except Exception as e:
    print("DNS resolve failed (may take 1-5 min to propagate):", e)
