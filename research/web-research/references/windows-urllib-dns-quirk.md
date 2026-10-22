# Windows `urllib` DNS Quirk — Wikipedia & Other Domains

## Symptoms

Running `urllib.request.urlopen()` on a Windows machine (git-bash / MSYS environment) against certain domains — notably `en.wikipedia.org` — fails with:

```
urllib.error.URLError: <urlopen error [Errno 11001] getaddrinfo failed>
```

The same request succeeds via `curl` on the same machine.

## Root Cause

Python's `urllib` on Windows uses its own socket-level DNS resolution, which can fail on corporate/VPN/proxy networks where `curl` (which uses the system's cURL DNS resolution) succeeds. This is distinct from a 403 (TLS fingerprint) error — here the domain literally cannot be resolved by Python's socket layer.

Commonly affected domains:
- `en.wikipedia.org` (and other Wikipedia subdomains)
- Some Cloudflare-protected sites
- Sites behind enterprise proxy/VPN

## Fix

Use `curl` instead of `urllib` for Wikipedia API access on Windows. Three reliable fallback patterns:

### Pattern A — Pipe to Python for processing
```bash
curl -sL --max-time 15 "https://en.wikipedia.org/w/api.php?action=query&titles=Page_title&prop=extracts&explaintext=1&format=json" \
  -H "User-Agent: Mozilla/5.0" \
  | python -c "import sys,json; d=json.load(sys.stdin); pg=list(d['query']['pages'].values())[0]; print(pg.get('extract','?')[:2000])"
```

### Pattern B — Save JSON + Read
```bash
curl -sL --max-time 15 "https://en.wikipedia.org/w/api.php?action=query&titles=Page_title&prop=extracts&explaintext=1&format=json" \
  -H "User-Agent: Mozilla/5.0" \
  -o C:/Users/NTQUANG_DELL/hermes-temp/wiki.json
```

### Pattern C — Python script with subprocess
Write a `.py` script that calls `urllib.request` with a custom DNS resolver or falls back to `requests` library if available. Simpler: just use `subprocess.run(['curl', ...])` inside your Python to get the data.

## Known unaffected endpoints

The following APIs work fine via `urllib` on the same Windows machine:
- PubMed NCBI E-utilities (`eutils.ncbi.nlm.nih.gov`)
- KFlow API (`127.0.0.1:3003`)
- Local services

The issue is domain-specific — Wikipedia is the most common trigger.

## When to use this reference

Whenever a Python research script using `urllib` to call Wikipedia API returns a DNS error (`getaddrinfo failed`, `Errno 11001`) but `curl` with the same URL/headers works. Switch to `curl` for the Wikipedia access layer and pipe the JSON into Python for processing.
