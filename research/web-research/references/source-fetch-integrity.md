# Source Fetch Integrity — size-check every fetched file

A fetch can fail and still **write a file that looks like a successful fetch**.
The failure mode is silent: the article builds, publishes, and reads complete,
because the writer filled the gap from parametric knowledge.

## The tell: byte size

Real fetched pages are large. Failed fetches are tiny.

```bash
cd ~/hermes-temp && ls -la --time-style=+%H:%M *_full.html
```

```
-rw-r--r--   278  chlorine_full.html        ← FAILED
-rw-r--r--   278  eq_const_full.html        ← FAILED
-rw-r--r-- 171763  lechatelier_full.html    ← real page
-rw-r--r-- 760367  magnesium_full.html      ← real page
```

**Rule of thumb: a fetched HTML source under ~5 KB is not a source.** Confirm
with `cat` before trusting it:

```bash
cd ~/hermes-temp && cat chlorine_full.html
```

## Verbatim Wikimedia rate-limit body (Oct 2026)

```
You are making too many requests to the API.
Please follow the best practices at <https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits>.
If you are unsure how to get the access you need, contact <bot-traffic@wikimedia.org>.

request-id: d0792933-7526-4409-b31a-cfcb56adc9a2
```

Other APIs return their own shape — Cloudflare 403 pages, `{"error":"rate_limit"}`,
HTML login walls. Same rule applies: read the first bytes.

## When to run the check

**Before authoring**, right after a fetch batch — not at publish time. Listing
sizes costs one command and catches the entire class:

```bash
cd <workdir> && find . -maxdepth 1 -type f -name "*_full.html" \
  -printf "%8s  %p\n" | sort -n | head -20
```

Sorting by size puts every failed fetch at the top of the output.

## What to do about it

1. **Name the gap in the report** — which file, which byte count, which error
   text, which article section lost its source. Vague "evidence base yếu" is
   unactionable.
2. **Re-fetch with backoff**, or drop the section and say so.
3. **Never let parametric knowledge silently fill a failed source.** If the
   fetch died, the claim is unsourced — label it or remove it. A section that
   reads well but rests on a dead fetch is worse than a visibly thin one,
   because nothing in the output signals the difference.

## Related

- `cron-job` → `references/auditing-daily-research-batches.md` — the same
  check applied on the audit side, after the fact.
- `research-reporting` pitfall 10 — PMIDs must be efetch-verified, never from
  memory. This is the file-level analogue of that rule.