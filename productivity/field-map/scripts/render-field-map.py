#!/usr/bin/env python3
"""Render a comprehensive field knowledge map with KPI cards, cross-links,
external field connections, and three-level terminology glossary.

Usage:
  python render-field-map.py --data data.json --output map.html
"""

import json, sys, os, argparse, html


ESC = lambda s: html.escape(str(s))


HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #0b1120; color: #e2e8f0;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    line-height: 1.6;
  }}
  .wrap {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; }}

  /* ─── HERO ─── */
  .hero {{
    padding: 50px 0 30px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
  }}
  .hero h1 {{
    font-size: 2.2rem; font-weight: 800;
    background: linear-gradient(135deg, #38bdf8, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }}
  .hero .root-def {{
    font-size: 0.92rem; color: #94a3b8; margin-top: 10px;
    max-width: 800px; line-height: 1.65;
  }}

  /* ─── GLOBAL KPI ─── */
  .kpi-row {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 10px; margin: 24px 0 30px;
  }}
  .kpi-global {{
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px; padding: 14px 16px;
    text-align: center;
  }}
  .kpi-global .num {{
    font-size: 1.7rem; font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    color: #38bdf8; line-height: 1.1;
  }}
  .kpi-global .label {{
    font-size: 0.7rem; color: #64748b;
    font-weight: 600; letter-spacing: 0.04em;
    text-transform: uppercase; margin-top: 3px;
  }}

  /* ─── FLOW DIAGRAM ─── */
  .flow-section {{
    margin-bottom: 30px;
  }}
  .flow-eyebrow {{
    font-size: 0.65rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: #475569; margin-bottom: 12px;
  }}
  .flow-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 8px;
  }}
  .flow-node {{
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px; padding: 10px 12px;
    text-align: center; cursor: default;
    transition: all 200ms;
  }}
  .flow-node:hover {{
    transform: translateY(-2px);
    border-color: rgba(255,255,255,0.15);
  }}
  .flow-node .fn-icon {{ font-size: 1.1rem; margin-bottom: 2px; }}
  .flow-node .fn-name {{ font-size: 0.78rem; font-weight: 600; color: #e2e8f0; }}

  /* ─── CROSS-FIELD CONNECTIONS ─── */
  .xfield-section {{
    margin-bottom: 30px;
  }}
  .xfield-list {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 10px;
  }}
  .xfield-card {{
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 8px; padding: 12px 14px;
  }}
  .xfield-name {{
    font-size: 0.82rem; font-weight: 700; color: #f1f5f9; margin-bottom: 4px;
  }}
  .xfield-topics {{
    font-size: 0.78rem; color: #64748b; margin-bottom: 4px;
  }}
  .xfield-rel {{
    font-size: 0.78rem; color: #94a3b8; line-height: 1.5;
  }}

  /* ─── SPECIALTY CARDS ─── */
  .specialty-card {{
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px; margin-bottom: 22px;
    overflow: hidden;
    transition: border-color 200ms;
  }}
  .specialty-card:hover {{ border-color: rgba(255,255,255,0.1); }}

  .spec-header {{
    padding: 18px 22px;
    display: grid; grid-template-columns: auto 1fr auto;
    gap: 14px; align-items: start;
    cursor: pointer; user-select: none;
    border-bottom: 1px solid transparent;
    transition: background 200ms;
  }}
  .spec-header:hover {{ background: rgba(255,255,255,0.03); }}
  .spec-header.open {{ border-bottom-color: rgba(255,255,255,0.06); }}

  .spec-icon {{
    width: 40px; height: 40px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem; flex-shrink: 0;
  }}
  .spec-meta {{ flex: 1; }}
  .spec-name {{
    font-size: 1.05rem; font-weight: 700; color: #f1f5f9;
    display: flex; align-items: center; gap: 8px;
  }}
  .spec-name .accent-line {{
    width: 3px; height: 18px; border-radius: 2px;
  }}
  .spec-purpose {{
    font-size: 0.82rem; color: #64748b; margin-top: 3px;
  }}
  .spec-mini-kpis {{
    display: flex; gap: 8px; flex-shrink: 0;
  }}
  .mini-kpi {{
    text-align: center; background: rgba(255,255,255,0.03);
    border-radius: 8px; padding: 5px 9px; min-width: 46px;
  }}
  .mini-kpi .mk-num {{
    font-size: 0.95rem; font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
  }}
  .mini-kpi .mk-label {{
    font-size: 0.58rem; color: #64748b;
    text-transform: uppercase; letter-spacing: 0.04em;
  }}
  .chevron {{
    width: 18px; height: 18px; color: #475569;
    transition: transform 200ms; flex-shrink: 0; margin-top: 2px;
  }}
  .spec-header.open .chevron {{ transform: rotate(180deg); }}

  /* ─── SPEC BODY ─── */
  .spec-body {{ display: none; padding: 0 22px 22px; }}
  .spec-body.show {{ display: block; }}

  .spec-grid {{
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 14px; margin: 18px 0;
  }}
  @media (max-width: 640px) {{ .spec-grid {{ grid-template-columns: 1fr; }} }}

  .info-box {{
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 8px; padding: 12px 14px;
  }}
  .info-box .ib-label {{
    font-size: 0.62rem; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; margin-bottom: 5px;
  }}
  .info-box .ib-body {{
    font-size: 0.84rem; color: #cbd5e1; line-height: 1.6;
  }}
  .ib-concept .ib-label {{ color: #38bdf8; }}
  .ib-frontier .ib-label {{ color: #a78bfa; }}
  .ib-challenge .ib-label {{ color: #f87171; }}
  .ib-purpose .ib-label {{ color: #34d399; }}

  /* ─── SUBTOPICS ─── */
  .subtopic-list {{ display: flex; flex-direction: column; gap: 8px; }}
  .subtopic-card {{
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 8px; padding: 12px 14px;
    transition: border-color 200ms;
  }}
  .subtopic-card:hover {{ border-color: rgba(255,255,255,0.09); }}

  .st-header {{
    display: flex; align-items: center; gap: 8px;
    cursor: pointer; user-select: none;
  }}
  .st-name {{ font-size: 0.9rem; font-weight: 600; color: #e2e8f0; flex: 1; }}
  .st-term-badge {{
    font-size: 0.63rem; padding: 2px 7px; border-radius: 4px;
    background: rgba(56,189,248,0.1); color: #38bdf8;
    font-weight: 600;
  }}
  .st-chevron {{
    width: 14px; height: 14px; color: #475569;
    transition: transform 200ms;
  }}
  .st-header.open .st-chevron {{ transform: rotate(180deg); }}

  .st-body {{ display: none; margin-top: 8px; }}
  .st-body.show {{ display: block; }}

  .st-detail-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 8px; }}
  @media (max-width: 640px) {{ .st-detail-grid {{ grid-template-columns: 1fr; }} }}

  /* Cross-links inside subtopic */
  .cross-link-row {{
    display: flex; flex-wrap: wrap; gap: 4px; margin-top: 8px;
  }}
  .xlink {{
    font-size: 0.72rem; padding: 2px 8px; border-radius: 4px;
    background: rgba(167,139,250,0.08); color: #a78bfa;
    border: 1px solid rgba(167,139,250,0.15);
    cursor: default;
  }}
  .xlink.ext {{ background: rgba(52,211,153,0.08); color: #34d399; border-color: rgba(52,211,153,0.15); }}
  .xlink-title {{ font-size: 0.75rem; color: #64748b; margin-top: 6px; }}

  /* ─── GLOSSARY ─── */
  .glossary-section {{
    margin-top: 14px;
    border-top: 1px solid rgba(255,255,255,0.04);
    padding-top: 12px;
  }}
  .gloss-header {{
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; color: #475569;
    margin-bottom: 8px; cursor: pointer; user-select: none;
  }}
  .gloss-header:hover {{ color: #64748b; }}
  .gloss-body {{ display: none; }}
  .gloss-body.show {{ display: block; }}

  .term-card {{
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 6px; padding: 10px 12px; margin-bottom: 6px;
  }}
  .term-name {{
    font-size: 0.85rem; font-weight: 700; color: #f1f5f9;
    font-family: 'JetBrains Mono', monospace; margin-bottom: 4px;
  }}
  .term-levels {{
    display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px;
  }}
  @media (max-width: 640px) {{ .term-levels {{ grid-template-columns: 1fr; }} }}
  .tl-box {{
    background: rgba(255,255,255,0.02);
    border-radius: 4px; padding: 6px 8px;
  }}
  .tl-label {{
    font-size: 0.58rem; font-weight: 700; letter-spacing: 0.06em;
    text-transform: uppercase; margin-bottom: 2px;
  }}
  .tl-body {{
    font-size: 0.78rem; color: #94a3b8; line-height: 1.5;
  }}
  .tl-basic .tl-label {{ color: #34d399; }}
  .tl-inter .tl-label {{ color: #fbbf24; }}
  .tl-deep  .tl-label {{ color: #f87171; }}
  .tl-basic {{ border-left: 2px solid rgba(52,211,153,0.3); }}
  .tl-inter {{ border-left: 2px solid rgba(251,191,36,0.3); }}
  .tl-deep  {{ border-left: 2px solid rgba(248,113,113,0.3); }}

  .footer {{
    text-align: center; padding: 32px 0;
    color: #475569; font-size: 0.76rem;
  }}
</style>
</head>
<body>
<div class="wrap">
  <div class="hero">
    <h1>{title}</h1>
    <div class="root-def">{root_def}</div>
  </div>

  <div class="kpi-row">
    <div class="kpi-global"><div class="num">{total_specialties}</div><div class="label">Chuyên ngành</div></div>
    <div class="kpi-global"><div class="num">{total_topics}</div><div class="label">Chủ đề</div></div>
    <div class="kpi-global"><div class="num">{total_terms}</div><div class="label">Thuật ngữ</div></div>
  </div>

  {flow_html}

  {xfield_html}

  {specialty_html}

  <div class="footer">Field Knowledge Map · Generated by Hermes Agent</div>
</div>

<script>
document.querySelectorAll('.spec-header').forEach(h => {{
  h.addEventListener('click', () => {{
    h.classList.toggle('open');
    h.nextElementSibling.classList.toggle('show');
  }});
}});
document.querySelectorAll('.st-header').forEach(h => {{
  h.addEventListener('click', () => {{
    h.classList.toggle('open');
    h.nextElementSibling.classList.toggle('show');
  }});
}});
document.querySelectorAll('.gloss-header').forEach(h => {{
  h.addEventListener('click', () => {{
    h.nextElementSibling.classList.toggle('show');
  }});
}});
</script>
</body>
</html>
'''


def spec_color_name(s):
    return s.get("color", "#38bdf8"), s.get("name", "")


def render_cross_links(links):
    if not links:
        return ""
    items = []
    for l in links:
        cls = "xlink ext" if l.get("type") == "external" else "xlink"
        icon = "🔗 " if l.get("type") == "external" else "↗ "
        label = l.get("target", "") or l.get("field", "")
        items.append(f'<span class="{cls}">{icon}{ESC(label)}</span>')
    if items:
        return f'<div class="cross-link-row">{" ".join(items)}</div>'
    return ""


def render_glossary(terms):
    if not terms:
        return ""
    cards = []
    for t in terms:
        name = ESC(t.get("term", ""))
        basic = ESC(t.get("basic", "") or t.get("co_ban", ""))
        inter = ESC(t.get("intermediate", "") or t.get("trung_binh", ""))
        deep  = ESC(t.get("deep", "") or t.get("chuyen_sau", ""))
        cards.append(f'''<div class="term-card">
  <div class="term-name">{name}</div>
  <div class="term-levels">
    <div class="tl-box tl-basic"><div class="tl-label">Cơ bản</div><div class="tl-body">{basic or "—"}</div></div>
    <div class="tl-box tl-inter"><div class="tl-label">Trung bình</div><div class="tl-body">{inter or "—"}</div></div>
    <div class="tl-box tl-deep"><div class="tl-label">Doctor</div><div class="tl-body">{deep or "—"}</div></div>
  </div>
</div>''')
    return f'''<div class="glossary-section">
  <div class="gloss-header">📖 Thuật ngữ ({len(terms)}) ▼</div>
  <div class="gloss-body show">{''.join(cards)}</div>
</div>'''


def render_st_subtopic(st, color):
    ov = ESC(st.get("overview", ""))
    res = ESC(st.get("current_research", ""))
    cha = ESC(st.get("challenges", ""))
    xlinks = render_cross_links(st.get("cross_links", []))
    tcount = st.get("term_count", 0)
    return f'''<div class="subtopic-card">
  <div class="st-header">
    <span class="st-name">{ESC(st["name"])}</span>
    <span class="st-term-badge">{tcount} terms</span>
    <svg class="st-chevron" viewBox="0 0 20 20" fill="none"><path d="M5 8l5 5 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </div>
  <div class="st-body">
    <div class="info-box ib-purpose"><div class="ib-label">Tổng quan</div><div class="ib-body">{ov}</div></div>
    <div class="st-detail-grid">
      <div class="info-box ib-frontier"><div class="ib-label">Nghiên cứu sâu nhất</div><div class="ib-body">{res or "—"}</div></div>
      <div class="info-box ib-challenge"><div class="ib-label">Rào cản khoa học</div><div class="ib-body">{cha or "—"}</div></div>
    </div>
    {xlinks}
  </div>
</div>'''


def render_specialty(s):
    color = s.get("color", "#38bdf8")
    subs = s.get("subtopics", [])
    terms = s.get("terms", [])
    subs_html = "\n".join(render_st_subtopic(st, color) for st in subs)
    gloss_html = render_glossary(terms)
    xlinks = render_cross_links(s.get("cross_links", []))

    return f'''<div class="specialty-card">
  <div class="spec-header">
    <div class="spec-icon" style="background:{color}22;color:{color}">{s.get("icon", "📚")}</div>
    <div class="spec-meta">
      <div class="spec-name">
        <div class="accent-line" style="background:{color}"></div>
        {ESC(s["name"])}
      </div>
      <div class="spec-purpose">{ESC(s.get("purpose", ""))}</div>
    </div>
    <div class="spec-mini-kpis">
      <div class="mini-kpi"><div class="mk-num" style="color:{color}">{s.get("topic_count", 0)}</div><div class="mk-label">chủ đề</div></div>
      <div class="mini-kpi"><div class="mk-num" style="color:{color}">{s.get("term_count", 0)}</div><div class="mk-label">thuật ngữ</div></div>
    </div>
    <svg class="chevron" viewBox="0 0 20 20" fill="none"><path d="M5 8l5 5 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </div>
  <div class="spec-body">
    <div class="spec-grid">
      <div class="info-box ib-concept"><div class="ib-label">Hiểu cơ bản</div><div class="ib-body">{ESC(s.get("basic_concept", ""))}</div></div>
      <div class="info-box ib-frontier"><div class="ib-label">Đi sâu nhất</div><div class="ib-body">{ESC(s.get("current_frontier", ""))}</div></div>
    </div>
    <div class="info-box ib-challenge"><div class="ib-label">Rào cản khoa học</div><div class="ib-body">{ESC(s.get("challenges", ""))}</div></div>
    {xlinks}
    {subs_html}
    {gloss_html}
  </div>
</div>'''


def render_flow_diagram(specialties):
    if not specialties:
        return ""
    nodes = []
    for s in specialties:
        nodes.append(f'''<div class="flow-node">
  <div class="fn-icon">{s.get("icon", "📚")}</div>
  <div class="fn-name">{ESC(s["name"])}</div>
</div>''')
    return f'''<div class="flow-section">
  <div class="flow-eyebrow">🌳 Sơ đồ chuyên ngành</div>
  <div class="flow-grid">{''.join(nodes)}</div>
</div>'''


def render_xfield_connections(data):
    xf = data.get("external_links", [])
    if not xf:
        return ""
    cards = []
    for f in xf:
        topics = ", ".join(f.get("topics", []))
        cards.append(f'''<div class="xfield-card">
  <div class="xfield-name">🔗 {ESC(f.get("field", ""))}</div>
  <div class="xfield-topics">{ESC(topics)}</div>
  <div class="xfield-rel">{ESC(f.get("relevance", ""))}</div>
</div>''')
    return f'''<div class="xfield-section">
  <div class="flow-eyebrow">🔗 Liên kết ngoại ngành</div>
  <div class="xfield-list">{''.join(cards)}</div>
</div>'''


def render(data):
    specialties = data.get("specialties", [])

    total_terms = data.get("total_terms", 0)
    # If total_terms is 0 but specialty terms exist, calculate
    if total_terms == 0:
        for s in specialties:
            total_terms += s.get("term_count", 0)

    sp_html = "\n".join(render_specialty(s) for s in specialties)
    flow_html = render_flow_diagram(specialties)
    xfield_html = render_xfield_connections(data)

    html = HTML_TEMPLATE.format(
        title=ESC(data.get("field", "Knowledge Map")),
        root_def=ESC(data.get("root_definition", "")),
        total_specialties=data.get("total_specialties", len(specialties)),
        total_topics=data.get("total_topics", 0),
        total_terms=total_terms,
        flow_html=flow_html,
        xfield_html=xfield_html,
        specialty_html=sp_html,
    )
    return html


def main():
    parser = argparse.ArgumentParser(description="Render field knowledge map as HTML")
    parser.add_argument("--data", "-d", help="JSON data file path")
    parser.add_argument("--output", "-o", default=None, help="Output HTML file")
    args = parser.parse_args()

    if args.data:
        with open(args.data, encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    html = render(data)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(html)


if __name__ == "__main__":
    main()
