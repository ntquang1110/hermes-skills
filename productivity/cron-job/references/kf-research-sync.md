# KFlow research sync — verified recipe (2026-09-23, job `da7c6b38c7d9`)

Context: the 4h research pipeline (`d43697af1322`) produces `research → HTML 2-tab →
preview.thefirstonly.com → research-log.md` and **does not POST KFlow** (its STATE says
"không POST KF, tránh duplicate"). The midnight job `da7c6b38c7d9`
"Auto-push research to Knowledge Flow" is the sync step. When KF shows no research cards
for recent days, this gap is the cause — not an empty queue.

App-level skill is `knowledge-researcher` (user-owned; read it for card schema/topic slugs).
This reference is the curator-side copy of the sync recipe so cron sessions have it even
when that skill is not loaded.

## 1. Working scripts on disk (verified end-to-end)

| Script | Purpose |
|---|---|
| `C:/Users/NTQUANG_DELL/hermes-temp/html2md.py` | tolerant HTML→markdown using `html.parser` (handles `<p>`-based AND div-based layouts: `fn-t`/`fn-d`/`callout`/`card`/`stat`) |
| `C:/Users/NTQUANG_DELL/hermes-temp/kf_push_backlog.py` | research-log parse → academic tab → OVERVIEW → live dedup → gates → POST |
| `C:/Users/NTQUANG_DELL/hermes-temp/kf_verify.py` | prints total card count + every card created since a timestamp |

```bash
python hermes-temp/kf_push_backlog.py --auto 30             # discover from logs (last 30h) and POST
python hermes-temp/kf_push_backlog.py --auto 30 --dry ALL    # list only: md/ov chars, dau ratio, src, SKIP lines
python hermes-temp/kf_push_backlog.py --dry <key>            # dump 1 item (title, summary, tags, OVERVIEW, md head+tail)
python hermes-temp/kf_push_backlog.py --force <key>          # override a dedup false positive
```

Always run `--dry ALL` first: it prints `[ERR]`, `[SKIP no-diacritics <ratio>]`,
`[SKIP dup] … ~= <existing title>` per file, so a bad batch never reaches the DB.

## 2. Manifest parsing (research-log.md is the source of truth)

Entry shapes seen across `D:/Hermes Proj/research-log.md` and the `hermes-temp/research-log*.md` variants:

```
- **Local file:** /d/Hermes Proj/<slug>-2tab.html   |  - **Local:** `hermes-temp/<slug>-2tab.html`
- **File:** <slug>-2tab.html                        |  - **Preview:** <url>  |  - **Publish URL:** <url>
- **Summary:** …  |  - **Tóm tắt:** …  |  - **Title:** …
- **Domain:** chăn nuôi (rotation index 4)  |  - **Domains:** Vật lý, Môi trường, Công nghiệp
```

**PITFALL — capture paths with `[^\r\n]+`, never `\S+`.** `D:/Hermes Proj/...` contains a space,
so `\S+` truncates to `D:/Hermes`, the map key becomes `Hermes`, and every lookup silently misses
(only entries whose path had no space matched — 4 of 20). Symptom: `src=-` for most items and
wrong titles taken from the HTML `<title>` instead of the log.
Domain → slug: take the segment before the first comma, match case-insensitively
(`chăn nuôi → chan-nuoi`, `xử lý nước → xu-ly-nuoc`, `kim loại/vật lý → vat-ly`, `hóa học → hoa-hoc`).

## 3. Panel extraction (the part that breaks)

Panel ids are **not stable**. Observed: `viz/acad`, `pv/pa`, `pane-v/pane-a`,
`tab-visualize/tab-academic`, `panel_vis/panel_hoc`, `pa0/pa1`, `panel0/panel1`, and index-based
`showTab(0)/showTab(1)`. Select from the tab buttons, never a hardcoded id:

```python
for bm in re.finditer(r"<button\b[^>]*>([\s\S]*?)</button>", raw, re.I):
    sm = re.search(r"showTab\(\s*(?:'([^']+)'|(\d+))\s*\)", bm.group(0))
    if sm: btns.append((strip_tags(bm.group(1)).lower(), sm.group(1),
                        int(sm.group(2)) if sm.group(2) else None))
# academic = label contains 'học' OR 'hoc' OR 'acad'   ← files exist with unaccented labels ("Hoc thuat")
# visual   = label contains 'visual'
```

Then take each panel as a **region**: from its opening tag to the NEXT panel's opening tag
(or `</body>`). Do **not** depth-match `</div>` — one unclosed inner div silently truncates a
screenful of content (`polymer-2tab.html` 9.4K → 3.0K chars; `co-dinh-dam-2tab.html` 12.4K → 1.6K),
with no error and a plausible-looking result.

Convert with a real parser (`html2md.html_to_md`), not regex block matching:
`superconductivity-2tab.html` has only 3 `<p>` tags (content lives in `fnode`/`callout` divs) —
regex conversion yielded 998 chars vs 5855 with the parser. Drop the leading `class="hero"` block
first (title/kicker duplicate the card title).

## 4. OVERVIEW block (required on every new card)

`<!--OVERVIEW-->{"what","why","mechanism","players","applications","limits","analogy"}<!--/OVERVIEW-->`
at the very start of `content`, markdown after. Derive from the visual tab, never invent:

- `what` = first non-trivial paragraph of the academic markdown (~420 chars cap)
- `why` = hero `<p>` (fallback `hero-sub` / `hero-lead` div)
- `mechanism` = ordered `<span class="chip">` chain of the flow map (fallback: `<h3>` of section 2)
- `players` = footer non-PMID sources; top up from stat labels when < 2
- `applications` = `<div class="goal">` `<li>`s; `limits` = "Nhược điểm"/"Hạn chế" card text
- `analogy` = only if the hero contains a quoted sentence; otherwise omit the key

## 5. Gates before POST

| Gate | Rule |
|---|---|
| Length | academic markdown ≥ 1200 chars else `[ERR]`, skip |
| Diacritics | `accent_ratio(md) ≥ 0.15` (normal research cards: 0.56–0.77; 0.00 = generator wrote unaccented Vietnamese → do NOT push) |
| Dedup | title keyword overlap ≥ 0.6 vs **live** `/api/cards` → skip; read the flagged title first |
| Shape | OVERVIEW at head; no raw HTML tags (`<div|<style|<table|<span|<p`) in content or the KFlow feed breaks |

`accent_ratio` = share of words with combining marks: `unicodedata.normalize("NFD", w) != w`
over `re.findall(r"[A-Za-zÀ-ỹ]+", txt)` words longer than 1 char.

## 6. KFlow write API

```
POST http://localhost:3003/api/knowledge
Headers: Authorization: Bearer hermes-knowledge-secret
         Cookie: tfo_auth=1d1e977a218bfa01fe61106c360c8acf667047e35f17fdb0f1a8484e06cfdb55
Body: {title, content, summary, tags[], source_url} → 201 {id}
```

Missing cookie → 307 → `/passcode` on every `/api/*`. `PATCH /api/cards?id=<uuid>` accepts
`title`, `content`, `summary`, `tags`, `source_url` (recomputes `reading_time_sec`).
Posts that match the existing corpus omit `topic_slug` (leaves `topic_id` null) and carry
keywords + a domain label in `tags`.

## 7. Pitfalls

1. **`curl -d` mangles Vietnamese on MSYS.** A PATCH body sent with curl stored
   `? ??ng h? sinh h?c` in the DB title. All POST/PATCH with diacritics go through
   `write_file` + `urllib.request` (`json.dumps(body, ensure_ascii=False).encode("utf-8")`).
   Re-GET and write the field to a UTF-8 file to confirm — the console rendering lies, the DB does not.
   (GET via curl is fine.)
2. **Dedup false positives** on shared compound lists: "Biochar — than sinh học xử lý nước:
   hấp phụ Pb/Cd/As/Cr" was flagged against "Xử lý KHÔ — Loại As, Pb, Hg, Cd". Read the match;
   `--force <key>` when it is a false positive. Keep genuine overlaps skipped
   (a 3rd PRRSV mechanism card against 2 existing ones).
3. **Stale cache re-posts.** Refresh `/api/cards` live immediately before dedup; a cache snapshot
   from before the batch makes the script re-POST everything it just pushed.
4. **Emoji prefix range.** Titles already carrying `⏰ ⚡ ⌚` (U+2190–U+2BFF) must not get a second
   emoji: check the wide range, or you ship `🧬 ⏰ Đồng hồ sinh học`.
5. **Unaccented source files are a pipeline bug, not a sync bug.** 3 files from the 4h pipeline
   (22/09 20:00 and 23/09 00:04 runs) had `accent_ratio = 0.00`. Report them as needing
   regeneration; propose adding the same gate to the research cron itself.
6. **Unaccented stage direction inside HTML**: panel labels like "Hoc thuat" and hero-less layouts
   exist. Label matching must accept ASCII (`hoc`) and overview extraction must fall back to
   `hero-sub`/`hero-lead` divs, or the academic panel is mis-selected / `why` comes out empty.

## 8. Evidence from the 2026-09-23 run

- `/api/cards` 549 → 569; 20 new cards, all with OVERVIEW head, tags, source_url, 4.5K–15K chars
- Verified with `kf_verify.py` (`created_at ≥ 2026-09-22T17Z` → 20 rows) and `GET /card/<id>` → 200
- Skipped: 3 unaccented files, 1 real duplicate (PRRSV); 1 title re-PATCHed after the curl-d incident
