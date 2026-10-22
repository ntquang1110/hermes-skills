#!/usr/bin/env python3
# Build 2-tab HTML: [Visualize] + [Học thuật] from KFlow card
# Reads: flow HTML v1 + card markdown -> writes combined dual-tab HTML
import re, markdown, datetime

FLOW = 'D:/Hermes Proj/cinnamaldehyde-flow.html'
CARD = 'C:/Users/NTQUANG_DELL/hermes-temp/card_cinn.md'
OUT  = 'D:/Hermes Proj/cinnamaldehyde-flow.html'

# Summary card (hiển thị phía trên content giống KFlow app). Lấy từ API /api/cards.
CARD_SUMMARY = 'Cinnamaldehyde (CA) là hoạt chất chính của tinh dầu quế: Michael acceptor gắn Keap1-Cys151 hoạt hóa Nrf2, kích hoạt stringent response RelA/(p)ppGpp'

# ---- 1. Extract visualize panel from existing flow HTML ----
with open(FLOW, encoding='utf-8') as f:
    flow_html = f.read()

m = re.search(r'(<header class="hero">.*?</footer>)', flow_html, re.DOTALL)
if not m:
    raise SystemExit('Cannot extract hero..footer from flow HTML')
visual_panel = m.group(1)

# grab original head CSS for reuse
m_css = re.search(r'<style>(.*?)</style>', flow_html, re.DOTALL)
base_css = m_css.group(1) if m_css else ''

# ---- 2. Card markdown -> academic HTML ----
with open(CARD, encoding='utf-8') as f:
    md = f.read()

# strip OVERVIEW metadata block
md = re.sub(r'<!--OVERVIEW-->.*?<!--/OVERVIEW-->', '', md, flags=re.DOTALL).strip()

acad_html = markdown.markdown(md, extensions=['tables', 'sane_lists', 'fenced_code', 'attr_list'])

# ---- 3. Compose ----
TAB_CSS = """
  /* ===== Tabs ===== */
  .tabbar{
    position:sticky;top:0;z-index:60;
    background:rgba(13,13,13,.94);backdrop-filter:blur(8px);
    border-bottom:1px solid var(--line);
    margin:0 -20px;padding:12px 20px;
    display:flex;gap:10px;align-items:center;
  }
  .tabbtn{
    flex:1;height:48px;border-radius:999px;border:1px solid var(--line);
    background:var(--surface);color:var(--gray);
    font-size:15px;font-weight:600;cursor:pointer;
    display:flex;align-items:center;justify-content:center;gap:8px;
    transition:all .2s ease-out;
  }
  .tabbtn .t-ic{font-size:16px}
  .tabbtn.active{background:var(--yellow);color:#111;border-color:var(--yellow)}
  .panel{display:none}
  .panel.active{display:block}

  /* ===== Academic tab ===== */
  .acad{max-width:680px;margin:0 auto;padding-top:8px}
  .acad .acad-summary{
    background:rgba(255,214,0,.07);border-left:3px solid var(--yellow);
    padding:12px 18px;border-radius:0 16px 16px 0;margin:24px 0 8px;
    color:var(--gray);font-size:14px;font-style:italic;line-height:1.6;
  }
  .acad h2{
    font-size:20px;font-weight:700;margin:36px 0 14px;padding-left:14px;
    border-left:4px solid var(--yellow);line-height:1.3;
  }
  .acad h3{font-size:16px;font-weight:600;margin:24px 0 10px;color:var(--white)}
  .acad p{color:#BDBDBD;font-size:15px;line-height:1.7;margin:12px 0}
  .acad strong{color:var(--white);font-weight:600}
  .acad em{color:var(--gray)}
  .acad table{
    width:100%;border-collapse:collapse;margin:18px 0;
    background:var(--surface);border-radius:18px;overflow:hidden;
    border:1px solid var(--line);font-size:13.5px;
  }
  .acad th{
    background:var(--surface2);color:var(--yellow);font-weight:600;text-align:left;
    padding:11px 14px;border-bottom:1px solid var(--line);
  }
  .tbl-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:18px 0}
  .tbl-wrap table{margin:0;min-width:420px}
  .acad td{padding:11px 14px;border-bottom:1px solid var(--line);color:#BDBDBD;vertical-align:top;line-height:1.55}
  .acad tr:last-child td{border-bottom:none}
  .acad blockquote{
    border-left:3px solid var(--yellow);background:rgba(255,214,0,.06);
    padding:12px 18px;margin:18px 0;border-radius:0 16px 16px 0;
    color:#E0E0E0;font-size:14.5px;line-height:1.65;
  }
  .acad blockquote p{margin:0;color:#E0E0E0}
  .acad ul,.acad ol{padding-left:22px;margin:14px 0}
  .acad li{color:#BDBDBD;font-size:14.5px;line-height:1.65;margin:7px 0}
  .acad li strong{color:var(--white)}
  .acad code{
    background:var(--surface2);border:1px solid var(--line);border-radius:8px;
    padding:2px 7px;font-size:13px;color:var(--yellow);font-family:ui-monospace,Consolas,monospace;
  }
  .acad pre{
    background:var(--surface2);border:1px solid var(--line);border-radius:16px;
    padding:16px;overflow-x:auto;margin:16px 0;
  }
  .acad pre code{background:none;border:none;color:#E0E0E0;padding:0}
  .acad hr{border:none;border-top:1px solid var(--line);margin:28px 0}
  .acad .src-note{font-size:12px;color:#6a6a6a;margin-top:8px;line-height:1.6}
"""

JS = """
  const panels = {viz: document.getElementById('pv'), acad: document.getElementById('pa')};
  const btns = {viz: document.getElementById('b-viz'), acad: document.getElementById('b-acad')};
  function showTab(k){
    panels.viz.classList.toggle('active', k==='viz');
    panels.acad.classList.toggle('active', k==='acad');
    btns.viz.classList.toggle('active', k==='viz');
    btns.acad.classList.toggle('active', k==='acad');
    window.scrollTo({top:0});
    requestAnimationFrame(update);
  }
  btns.viz.onclick = () => showTab('viz');
  btns.acad.onclick = () => showTab('acad');
  /* wrap academic tables for horizontal scroll on mobile */
  document.querySelectorAll('#pa table').forEach(t => {
    const w = document.createElement('div');
    w.className = 'tbl-wrap';
    t.parentNode.insertBefore(w, t);
    w.appendChild(t);
  });
  /* progress only meaningful in visualize tab */
  const sections = ['s0','s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11'];
  const fill = document.getElementById('fill');
  const count = document.getElementById('count');
  const labels = ['Bản đồ','Bước 1','Bước 2','Bước 3','Bước 4','Bước 5','Bước 6','Bước 7','Bước 8','Bước 9','Bước 10','Chốt'];
  function update(){
    if(!panels.viz.classList.contains('active')) return;
    let idx = 0;
    for(let i=0;i<sections.length;i++){
      const el = document.getElementById(sections[i]);
      if(!el) continue;
      const r = el.getBoundingClientRect();
      if(r.top < window.innerHeight*0.45) idx = i;
    }
    const pct = Math.round((idx/(sections.length-1))*100);
    fill.style.width = pct + '%';
    count.textContent = labels[idx] + ' · ' + pct + '%';
  }
  window.addEventListener('scroll', update, {passive:true});
"""

summary_box = f'<div class="acad-summary">{CARD_SUMMARY}</div>' if CARD_SUMMARY else ''

academic_panel = f"""
<div class="panel" id="pa">
  <div class="acad">
    {summary_box}
    {acad_html}
  </div>
</div>
"""

visual_panel = f"""
<div class="panel active" id="pv">
  <div class="progress">
    <span class="label">Visual Flow</span>
    <div class="track"><div class="fill" id="fill"></div></div>
    <span class="count" id="count">Bản đồ · 0%</span>
  </div>
  {visual_panel}
</div>
"""

final_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cinnamaldehyde · Tinh dầu quế — Visualize / Học thuật</title>
<style>
{base_css}
{TAB_CSS}
</style>
</head>
<body>
<div class="wrap">

  <div class="tabbar">
    <button class="tabbtn active" id="b-viz"><span class="t-ic">◈</span> Visualize</button>
    <button class="tabbtn" id="b-acad"><span class="t-ic">≡</span> Học thuật</button>
  </div>

  {visual_panel}
  {academic_panel}

</div>
<script>
{JS}
</script>
</body>
</html>
"""

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(final_html)
print('OK written:', OUT, '| total chars:', len(final_html))
print('acad html chars:', len(acad_html))
