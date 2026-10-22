# HTML research page → KF card markdown converter (VERIFIED Sep 08, 2026)

Use when the midnight auto-push (`da7c6b38c7d9`) finds a finished research HTML page in a chat-session project folder (preview published at preview.thefirstonly.com) that was never POSTed to KF. Converts the dark-theme research HTML into (1) an `<!--OVERVIEW-->` JSON block (Visualize tab) + (2) clean markdown (Học thuật tab).

## Input assumption

The research HTML pages share this structure (built by the Hermes- research group):
- `<style>` block followed by `<body>`
- content wrapped in `<div class="wrap">...</div></body>`
- headings `<h2>` / `<h3>` (sections and sub-sections)
- content blocks `<div class="card">` containing `<p>` paragraphs (some with `<span class="num">N</span>` numbering), `<table>` markdown-style tables, `<div class="flow">` pathway diagrams, and `<p class="ref">` citation footnotes

## Converter skeleton (write_file + run as `python script.py` — never inline)

```python
import re, html, json

def strip_tags(s):
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).strip()

def html_to_markdown(fpath):
    raw = open(fpath, encoding="utf-8").read()
    raw = re.sub(r"<style[\s\S]*?</style>", "", raw, flags=re.I)
    raw = re.sub(r"<script[\s\S]*?</script>", "", raw, flags=re.I)
    m = re.search(r'<div class="wrap">\s*(.*?)\s*</div>\s*</body>', raw, re.S)
    body = m.group(1) if m else raw
    lines = []
    parts = re.split(r'(<h2>.*?</h2>|<h3>.*?</h3>)', body, flags=re.S)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        hm = re.match(r'<h([23])>(.*?)</h\1>', part, re.S)
        if hm:
            lines.append("#" * (int(hm.group(1)) + 1) + " " + strip_tags(hm.group(2)))
            continue
        tm = re.search(r'<table>([\s\S]*?)</table>', part)
        if tm:
            rows = re.findall(r'<tr[^>]*>([\s\S]*?)</tr>', tm.group(1))
            md_rows = []
            for i, row in enumerate(rows):
                cells = [strip_tags(c).replace("|", "\\|")
                         for c in re.findall(r'<t[dh][^>]*>([\s\S]*?)</t[dh]>', row)]
                md_rows.append("| " + " | ".join(cells) + " |")
                if i == 0:
                    md_rows.append("|" + "---|" * len(cells))
            lines.append("\n".join(md_rows))
            part = re.sub(r'<table>[\s\S]*?</table>', '', part)
        fm = re.search(r'<div class="flow">([\s\S]*?)</div>', part)
        if fm:
            lines.append("```\n" + strip_tags(fm.group(1)) + "\n```")
            part = re.sub(r'<div class="flow">[\s\S]*?</div>', '', part)
        # PITFALL: generic <p> regex ALSO matches <p class="ref"> — check attrs and skip
        pm = re.findall(r'<p([^>]*)>([\s\S]*?)</p>', part)
        for pattrs, p in pm:
            if 'class="ref"' in pattrs:
                continue
            txt = re.sub(r'<span class="num">\s*\d+\s*</span>', '', p)
            txt = strip_tags(txt)
            if txt:
                lines.append(txt)
        rm = re.findall(r'<p class="ref">([\s\S]*?)</p>', part)
        for r in rm:
            txt = strip_tags(r).strip()
            # PITFALL: ref text already begins with "Nguồn:" — strip before wrapping
            if txt.lower().startswith("nguồn:"):
                txt = txt[len("nguồn:"):].strip()
            if txt:
                lines.append("")
                lines.append("_Nguồn: " + txt + "_")
    md = "\n".join(lines)
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return md
```

## OVERVIEW block (prepend to content)

```html
<!--OVERVIEW-->{"what":"...","why":"...","mechanism":["b1","b2","b3"],"players":["..."],"applications":["..."],"limits":"...","analogy":"..."}<!--/OVERVIEW-->
```
JSON via `json.dumps(overview, ensure_ascii=False)` — keeeps Vietnamese diacritics.

## Push + verify

```python
payload = {"title": ..., "content": ov_block + "\n\n" + md, "summary": ...,
           "tags": [...], "topic_slug": ..., "source_url": preview_url}
# POST http://localhost:3003/api/knowledge with BOTH cookie + Bearer → expect 201
# Verify: fetch /api/cards (all), match by id, count diacritics > 0, check <!--OVERVIEW--> present
```

## Worked example (Sep 08, 2026)

| source HTML | card title | KF id | preview |
|---|---|---|---|
| tingo_opium_research.html | 🌿 Cây thuốc phiện & Cây tí ngọ | 230f1389-… | preview.thefirstonly.com/b056zdflndnn |
| smoking_health_lip.html | 🚬 Hút thuốc & sức khỏe + môi thâm | e6d8075e-… | preview.thefirstonly.com/54vw996bcugn |
| tooth_yellow_research.html | 🦷 Hút thuốc vàng răng | ddaee3c7-… | preview.thefirstonly.com/0xwjywwc2d4c |

State file marker to look for: `Yêu cầu sau nếu có: KFlow push` in `D:/Hermes Proj/.hermes-state/chat/telegram-group-hermes-research.md`. After pushing, append `ĐÃ PUSH KFLOW <uuid>` to the state line so the next run skips it.