# Report (editorial, light) build pattern — Say Briefly

For "báo cáo toàn diện" / narrative research reports, NOT the mobile-first dark catalog in
`subagent-schema-and-build.md`. Same publish pipeline (see `research-reporting`), different skin.

## Which template to use

| Deliverable shape | Template | Where |
|---|---|---|
| Tra cứu danh mục, filter/search, mobile, dark | Premium B/W/Y catalog | `references/subagent-schema-and-build.md` |
| Báo cáo đọc tuần tự, editorial, light | **Say Briefly** | `popular-web-designs/templates/say-briefly.md` + reference file below |

`design-template-selector` is the router; `say-briefly` is one row of its Editorial table.

## Say Briefly tokens (cream/green/yellow)

```
--cream:#fcfaf5  --green:#1a3300  --yellow:#ffe95c
--teal:#a8e5e5    --mint:#d5f5c2  --blush:#f6d0ff  --terra:#cb5521
```

**FONT MISMATCH — read this.** The token doc says `Inter` + `Roboto Mono`. The file that actually
renders well (`D:/Hermes Proj/say-briefly-diet-mam-benh.html`) uses:

```html
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

Use **DM Sans + JetBrains Mono**. `Bricolage Grotesque` weight 800 only, letter-spacing `.02em`.

Hard rules: no pure black (`#1a1a1a` ink, `#1a3300` for headings/CTAs); yellow is a **text wash /
badge fill, never a CTA background**; radius 6px buttons, 12px cards; sticky nav; `max-width` 840-960px.

## Section grammar that worked

Numbered `<h2>` per section with a **yellow underline** (`border-bottom:2px solid var(--yellow);
display:inline-block`), then a reusable component vocabulary:

| Component | Class | Use |
|---|---|---|
| callout | `.hl` (+`.y` yellow / `.t` teal / `.r` terracotta) | mechanism, caveats, verdict |
| mechanism box | `.dia` (+`.g` gold / `.t` teal) | per-compound / per-class deep dive |
| inline flow | `.flow .fn` + `.ar` | 4-7 step pipeline, `small` = gloss |
| data table | `.tw` wrap + `.tb` | `min-width:600px`, sticky `th`, hover row tint |
| reference list | `ul.refs li` | yellow left border, PMID link + journal + year + DOI |
| stat tile | `.stats .st` | forest bg, cream value, mono 7.5px label |
| product/drug card | `.cc > .ch` + `.cb` | colored header bar + `.kv` key-value grid |
| integrity banner | `.banner` | terracotta border — "KHÔNG dùng làm cơ sở claim" |

`mark{background:var(--yellow)}` for search-term highlight inside table cells.

## 7-section shape for a full topic report

1. **Bức tranh toàn cảnh** — hero + stat grid + pipeline flow + how-to-read-numbers box
2. **Phân loại & chất lượng dữ liệu** — taxonomy cards + full data table (filter + search) + completeness bars
3. **Hoá học & tính chất vật lý** — the quantitative payoff: group medians + rich per-compound cards
4. **Sinh tổng học** — biosynthesis pathway, why engineering beats extraction
5. **Bằng chứng theo từng nhóm** — per-class: mechanism + **limits/counter-evidence** + newest PMIDs
6. **An toàn & pháp lý** — GHS/safety table, regulatory status, contraindications
7. **Ứng dụng & khoảng trống** — market/tech gaps, honest conclusions

Section 5 is where the report earns trust: **every class gets an explicit
`Giới hạn / phản biện` block**, not just positives.

## Build split for long reports

Past ~450 lines of f-strings, nested triple-quotes inside an f-string body break the script
(`IndentationError` — the inner `'''` closes the outer one). Split:

```python
# build_report.py — sections 1-3, then:
exec(open(os.path.join(BASE, "build_part2.py"), encoding="utf-8").read())
```

`build_part2.py` holds sections 4-7, the JS layer, and final assembly, and inherits all globals
(helpers, dataset, CSS). Cheaper than fighting quoting.

## Client-side extras that add polish cheaply

- Sticky `<nav>` with anchor links per section + `scroll-margin-top:52px` on `.sec` so headings
  don't hide under the nav.
- Filter chips + realtime search over a data table, with `mark` highlight on the matched substring.
- `.scrollhint` ("← Cuộn ngang để xem đủ cột →") under any `overflow-x:auto` table on mobile.
- "Cuộn ngang" hint text is expected behaviour, not an overflow bug (same as catalog chips).

## Verify before publishing

Same as the catalog: serve over `python -m http.server` (Camofox blocks `file://`), then check
with playwright-core `.cjs` from `D:/Hermes Proj/camofox-browser` at 390px: no horizontal overflow
on `.sec h2, .sec h3, .cc, .hl, .st`, filter chip counts correct, search returns expected row count,
`page.on('pageerror')` empty. Tables are `overflow-x:auto` by design — exclude `.tw`/`.tb` from
overflow checks.