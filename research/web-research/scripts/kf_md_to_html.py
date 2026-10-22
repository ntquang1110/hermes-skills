# -*- coding: utf-8 -*-
"""Convert a Knowledge Flow (KF) card payload into Premium B/W/Y single-file HTML.

Part of the web-research delivery pipeline (Phase 2: HTML OUTPUT). Reuse this
instead of hand-writing a markdown->HTML converter for each research cron run.

Usage:
    python kf_md_to_html.py input_payload.json output.html

input_payload.json (same shape as the POST /api/knowledge body):
    {
      "title": "🧬 Topic — subtitle",
      "content": "markdown...",
      "tags": ["a", "b", ...],
      "summary": "short summary (optional)"
    }

Handles the markdown dialect used in KF cards:
  ## / ### headings, | tables |, > blockquotes, ``` code blocks,
  **bold**, `code`, numbered lists, bullet lists, plain paragraphs.

Pitfall baked in: never put a regex with a backslash inside an f-string
expression (`SyntaxError: f-string expression part cannot include a backslash`).
Extract the regex result to a variable first (see item_text below).

CSS tokens: --yellow #FFD600, --bg #1B1B1D, --card #242428, --line #333338.
"""
import datetime
import json
import re
import sys


def inline(s):
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    s = re.sub(r'\*\*(.+?)\*\*', '<strong>\\1</strong>', s)
    s = re.sub(r'`(.+?)`', '<code>\\1</code>', s)
    return s


def render_table(rows):
    if not rows:
        return ''
    head, body = rows[0], rows[1:]
    th = ''.join('<th>%s</th>' % inline(c) for c in head)
    trs = ''
    for r in body:
        tds = ''.join('<td>%s</td>' % inline(c) for c in r)
        trs += '<tr>%s</tr>' % tds
    return '<div class="table-wrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, trs)


def md_to_html(text):
    lines = text.split('\n')
    html, code_buf, table_buf = [], [], []
    in_code = in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            if in_code:
                html.append('<div class="code-block"><pre>' + '\n'.join(code_buf) + '</pre></div>')
                code_buf, in_code = [], False
            else:
                in_code = True
            continue
        if in_code:
            code_buf.append(line)
            continue
        if stripped.startswith('|') and '|' in stripped[1:]:
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            if not in_table:
                in_table = True
                table_buf = [cells]
            else:
                if all(re.fullmatch(r':?-{2,}:?', c) for c in cells):
                    continue  # separator row |---|---|
                table_buf.append(cells)
            continue
        if in_table:
            html.append(render_table(table_buf))
            table_buf, in_table = [], False
        if not stripped:
            continue
        if stripped.startswith('## '):
            html.append('<h2>%s</h2>' % inline(stripped[3:]))
        elif stripped.startswith('### '):
            html.append('<h3>%s</h3>' % inline(stripped[4:]))
        elif stripped.startswith('> '):
            html.append('<div class="quote-box">%s</div>' % inline(stripped[2:]))
        elif re.match(r'^\d+\.\s', stripped):
            item_text = re.sub(r'^\d+\.\s', '', stripped)
            html.append('<div class="list-item num">%s</div>' % inline(item_text))
        elif stripped.startswith('- '):
            html.append('<div class="list-item">%s</div>' % inline(stripped[2:]))
        elif re.match(r'^\*\*[^*]+\*\*', stripped):
            html.append('<p class="bold-lead">%s</p>' % inline(stripped))
        else:
            html.append('<p>%s</p>' % inline(stripped))
    if in_table:
        html.append(render_table(table_buf))
    if in_code:
        html.append('<div class="code-block"><pre>' + '\n'.join(code_buf) + '</pre></div>')
    return '\n'.join(html)


def build_html(payload):
    title = payload.get('title', 'Research')
    content = payload.get('content', '')
    tags = payload.get('tags', [])
    summary = payload.get('summary', '')
    body = md_to_html(content)
    tag_html = ''.join('<span class="tag">%s</span>' % t for t in tags)
    today = datetime.date.today().strftime('%d/%m/%Y')
    summary_html = '<p class="summary">%s</p>' % inline(summary) if summary else ''
    return TEMPLATE.format(title=title, today=today, tags=tag_html, summary=summary_html, body=body)


TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
:root {{ --yellow:#FFD600; --bg:#1B1B1D; --card:#242428; --line:#333338; --muted:#9a9aa2; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:var(--bg); color:#e8e8ea; font-family:-apple-system,'Segoe UI',Roboto,sans-serif; line-height:1.65; }}
.wrap {{ max-width:900px; margin:0 auto; padding:32px 20px 80px; }}
.hero {{ background:var(--card); border-radius:28px; padding:36px 32px; margin-bottom:28px; border:1px solid var(--line); }}
.hero h1 {{ color:var(--yellow); font-size:1.7rem; line-height:1.3; margin-bottom:14px; }}
.hero .meta {{ color:var(--muted); font-size:.85rem; margin-bottom:14px; }}
.summary {{ color:#c5c5cc; font-size:.95rem; }}
.tags {{ display:flex; flex-wrap:wrap; gap:8px; }}
.tag {{ background:#333338; color:#d8d8dc; border-radius:20px; padding:4px 12px; font-size:.75rem; }}
h2 {{ color:var(--yellow); font-size:1.35rem; margin:38px 0 14px; padding-bottom:8px; border-bottom:2px solid var(--line); }}
h3 {{ color:#ffffff; font-size:1.05rem; margin:22px 0 10px; }}
p {{ margin:10px 0; color:#d5d5da; }}
strong {{ color:#ffffff; }}
code {{ background:#333338; padding:2px 6px; border-radius:6px; font-size:.85em; color:#ffd600; }}
.table-wrap {{ overflow-x:auto; margin:16px 0; border-radius:16px; border:1px solid var(--line); }}
table {{ width:100%; border-collapse:collapse; font-size:.88rem; }}
th {{ background:#2e2e33; color:var(--yellow); text-align:left; padding:12px 14px; font-weight:600; }}
td {{ padding:11px 14px; border-top:1px solid var(--line); color:#d0d0d6; vertical-align:top; }}
tbody tr:nth-child(even) {{ background:#202024; }}
.quote-box {{ border-left:4px solid var(--yellow); background:var(--card); padding:14px 18px; border-radius:0 14px 14px 0; margin:16px 0; color:#e5e5ea; }}
.code-block {{ background:#111113; border:1px solid var(--line); border-radius:14px; padding:16px; margin:16px 0; overflow-x:auto; }}
.code-block pre {{ font-family:'Cascadia Code',Consolas,monospace; font-size:.8rem; color:#9be39b; line-height:1.55; }}
.list-item {{ padding:4px 0 4px 18px; position:relative; color:#d5d5da; }}
.list-item::before {{ content:'▸'; color:var(--yellow); position:absolute; left:0; }}
.bold-lead {{ color:#ffffff; }}
.footer {{ margin-top:50px; padding-top:20px; border-top:1px solid var(--line); color:var(--muted); font-size:.8rem; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="hero">
    <h1>{title}</h1>
    <div class="meta">📅 {today} · TheFirstOnly Knowledge Flow</div>
    {summary}
    <div class="tags">{tags}</div>
  </div>
  {body}
  <div class="footer">TheFirstOnly Knowledge Flow · nguồn: PubMed/DOI trong bảng tham khảo</div>
</div>
</body>
</html>"""


def main():
    if len(sys.argv) != 3:
        print('Usage: python kf_md_to_html.py input_payload.json output.html')
        sys.exit(1)
    with open(sys.argv[1], encoding='utf-8') as f:
        payload = json.load(f)
    html = build_html(payload)
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        f.write(html)
    print('HTML written: %d bytes' % len(html))


if __name__ == '__main__':
    main()
