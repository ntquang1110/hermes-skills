# Auditing a daily research batch (cron "check today's research")

Cron job of the shape *"kiểm tra tất cả research mới được tạo hôm nay"* — the
running prompt may be **truncated** (see `upload-online-link` incident below), so
reconstruct intent from artifacts on disk rather than guessing.

VERIFIED 2026-10-02 on a 4-article batch (Âm học / Magie / Cân bằng hóa học /
Khử trùng nước).

## Step 0 — Reconstruct the manifest, don't guess the prompt

Truncated prompt + missing skill → read the day's **research log** first. It is
the manifest: file path, preview URL, domain, sources, one-line summary per
article.

```
C:/Users/<user>/hermes-temp/research-log-YYYY-MM-DD.md
```

`~/AppData/Local/hermes/cron/jobs.json` holds the full untruncated prompt if the
log is missing.

## Step 1 — Scope `find` to the working dir (CORRECTS older guidance)

Older versions of this skill say "avoid `find`, use `ls -la`". That is true for
a **deep home-directory scan**, and false for a scoped scan. VERIFIED working
command — returns in well under a second, no starvation:

```bash
cd ~/hermes-temp && find . -maxdepth 1 -type f \( -name "*.html" -o -name "*.md" \) \
  -newermt "YYYY-MM-DD 00:00" -printf "%TH:%TM  %8s  %p\n" | sort
```

- `-maxdepth 1` + `cd` into the working dir is what makes it fast. Drop either
  and you're back to the starving deep scan.
- `%8s` (size in bytes) is the column that earns the scan — see Step 3.
- `ls -la --time-style` truncates long path lists and buries the size column;
  `find -printf` is better for auditing.

## Step 2 — Verify every preview link with curl, not the browser

```bash
mkdir -p ~/hermes-temp/vfy && cd ~/hermes-temp/vfy
for u in <slug1> <slug2> <slug3> <slug4>; do
  code=$(curl -s -o p_$u.html -w "%{http_code}" -L "https://preview.thefirstonly.com/$u")
  echo "$u | HTTP $code | $(wc -c < p_$u.html)B | $(grep -o '<title>[^<]*' p_$u.html | head -1)"
done
```

Four numbers per link are the audit row: **HTTP status, byte size, `<title>`, and
(tab) count**. 200 + non-trivial size + correct Vietnamese `<title>` = link is
genuinely live.

⚠️ **Write curl output to a Windows-visible path.** `-o /tmp/x.html` lands where
bash can't see it (curl is a native Windows binary; MSYS does not translate the
path) → `wc: /tmp/x.html: No such file or directory` while curl still prints
HTTP 200. Same trap as the JSON `/tmp` trap in the main SKILL.md. `-o p_$u.html`
after `cd` avoids it entirely.

⚠️ A short `for` loop like the above is fine. See the SKILL.md pitfall for the
compound-command shapes that get blocked.

## Step 3 — ⚠️ Source-file integrity: the `278 byte` tell

**The highest-value check in the whole audit.** Files named `<topic>_full.html`
are *fetched source pages*. A failed fetch writes a tiny text file that looks
like a successful fetch:

```
-rw-r--r-- 278  chlorine_full.html     ← NOT HTML. Rate-limit text.
-rw-r--r-- 278  eq_const_full.html     ← NOT HTML. Rate-limit text.
-rw-r--r-- 171763  lechatelier_full.html   ← real page
-rw-r--r-- 760367  magnesium_full.html     ← real page
```

Content of a failed one:

```
You are making too many requests to the API.
Please follow the best practices at <https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits>.
```

**Any source file under ~5 KB is not a source.** Confirm with `cat`:

```bash
cd ~/hermes-temp && cat chlorine_full.html
```

### Why this matters more than it looks

The article still builds and still publishes. The prose in the Học thuật tab
looked complete — because the writer filled it from parametric knowledge instead
of the missing source. So:

- The **preview link passes every superficial check** (200, right title, 2 tabs).
- The **article is silently under-sourced** in exactly the sections whose fetch
  failed (chlorine chemistry; equilibrium constants).

An audit that only checks HTTP status + tab structure will call this batch
healthy. Only the byte-size column surfaces it. **Always print file sizes.**

### Report it as a named gap, not a general caveat

Say which file, which byte count, which error text, and which article section
lost its source. "Evidence base yếu" without naming `chlorine_full.html` is
unactionable.

## Step 4 — Structural verification without a working browser

Camofox/Camofox-browser returned `500` on `localhost:9377` during this audit.
That is **not** a reason to skip verification — grep and read the local source:

```bash
cd ~/hermes-temp
grep -c "<table" acoustics-2tab.html magnesium-alloy-2tab.html ...   # bảng per file
grep -c "<h3>"   acoustics-2tab.html ...                              # heading depth
grep -o 'class="tabbtn[^>]*>[^<]*' acoustics-2tab.html               # tab labels
grep -o 'fonts.googleapis[^"]*' acoustics-2tab.html                  # font subset risk
grep -o '<span class="chip">[^<]*' acoustics-2tab.html               # declared sources
grep -o "TODO\|Lorem\|\[insert\]\|placeholder" *.html                # unfinished markers
```

Checklist per file: 2 tabs present with both labels, `<table>` count > 0,
`<h3>` count ≥ 10, no placeholder markers, declared-source chips match the log.

**System-font stacks are safe for Vietnamese.** These files used
`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif` — zero
`fonts.googleapis` links, so the missing `subset=vietnamese` font bug that
plagues the Google-Fonts pages does not apply. If `grep fonts.googleapis` returns
nothing, say so explicitly rather than leaving font risk unassessed.

## Step 5 — Report shape

Quang reads for defects, not for the fact that things worked:

1. One-line verdict up front (**cả 4 đã publish, không có bài nào hỏng**).
2. Compact table: `# | chủ đề | domain | link | HTTP | bảng | h3`.
3. **Vấn đề cần biết** — numbered, each naming the concrete file/byte/link.
4. **Việc cần làm** — the fix, and what it costs. Offer to dispatch it.

State plainly when a check was *not* possible (browser render unverified) rather
than implying full verification.