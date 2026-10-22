# -*- coding: utf-8 -*-
"""
report-builder.py — skeleton: data-driven HTML report từ JSON + citation theo PMID.

Ba điều chỉnh sửa cho khỏi phải nghĩ lại mỗi lần:
  1. Bảng render từ JSON, có `data-*` attribute làm nguồn sort (không parse text cell).
  2. Citation ghi bằng PMID trong nội dung, script tự đánh số lại → thêm/bớt ref không lệch.
  3. Tự validate trước khi ghi file.

Cách dùng: copy file này, sửa DATA/ROWS/CITED + phần HTML, chạy `python report-builder.py`.
Sau đó chạy `python scripts/validate-report-html.py <out>.html` và verify trên browser.
"""
import json
import os
import re as _re

BASE = r"D:\path\to\data"
OUT = r"D:\path\to\report.html"

# ---------- load ----------
primary = json.load(open(os.path.join(BASE, "pubchem_out.json"), encoding="utf-8"))
corpus = {}
corpus.update(json.load(open(os.path.join(BASE, "pubmed_out.json"), encoding="utf-8")))
corpus.update(json.load(open(os.path.join(BASE, "pubmed_out2.json"), encoding="utf-8")))

# unique articles by pmid
seen = {}
for arts in corpus.values():
    for a in arts:
        seen.setdefault(a["pmid"], a["meta"])

# ---------- rows ----------
ROWS = []
for name, v in primary.items():
    p = v["props"]
    salt = (v.get("salt") or {}).get("props", {})
    ROWS.append(dict(
        en=name, cid=p.get("CID"), formula=p.get("MolecularFormula"),
        mw=p.get("MolecularWeight"), xlogp=p.get("XLogP", "—"), tpsa=p.get("TPSA"),
        smiles=p.get("ConnectivitySMILES"), cls=v.get("class"),
        salt_formula=salt.get("MolecularFormula", ""),
    ))


def f1(x, d=1):
    try:
        return f"{float(x):.{d}f}".rstrip("0").rstrip(".")
    except (TypeError, ValueError):
        return "—"


def E(x):
    import html as _h
    return _h.escape(str(x))


# ---------- references (CHỈ liệt kê trích dẫn dùng thật) ----------
CITED = ["", ""]          # ← điền PMID
CITED = [c for c in CITED if c]
_missing_from_corpus = [c for c in CITED if c not in seen]
assert not _missing_from_corpus, f"PMID không có trong corpus: {_missing_from_corpus}"


def cite(pmid):
    m = seen[pmid]
    return dict(year=m["year"], journal=m["journal"], title=m["title"], doi=m.get("doi", ""))


# ---------- table ----------
# data-* là nguồn sort duy nhất — JS đọc thẳng, không parse text cell
trs = "".join(
    f'<tr data-en="{E(r["en"])}" data-hw="{f1(r["mw"], 2)}" data-psa="{f1(r["tpsa"], 1)}">'
    f'<td class="nm">{E(r["en"])}</td>'
    f'<td class="num">{E(r["cid"])}</td>'
    f'<td><b>{E(r["formula"])}</b></td>'
    f'<td class="num">{E(r["mw"])}</td>'
    f'<td class="num">{E(r["xlogp"])}</td>'
    f'<td class="num">{E(r["tpsa"])}</td>'
    f'<td><span class="smiles">{E(r["smiles"])}</span></td>'
    f'</tr>'
    for r in ROWS
)

refs_html = "".join(
    f'<li><b>{E(cite(c)["title"])}</b><br>'
    f'<span class="jr">{E(cite(c)["journal"])}</span>'
    f'<span class="meta">{E(cite(c)["year"])} · PMID '
    f'<a href="https://pubmed.ncbi.nlm.nih.gov/{c}/" target="_blank" rel="noopener">{c}</a>'
    + (f' · {E(cite(c)["doi"])}' if cite(c)["doi"] else "")
    + '</span></li>'
    for c in CITED
)

# Trong nội dung, viết: <span class="refmark">[PMID]</span>  ← KHÔNG viết [7]
BODY = """
  <p>Ví dụ: dữ liệu PubChem trực tiếp
     <span class="refmark">[PMID_1]</span> và tổng hợp PubMed
     <span class="refmark">[PMID_2]</span>.</p>
""".replace("PMID_1", CITED[0] if CITED else "0").replace("PMID_2", CITED[1] if len(CITED) > 1 else "0")

HTML = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>REPORT</title>
<style>
/* cream #fcfaf5 · forest #1a3300 · yellow #ffe95c · Bricolage Grotesque */
:root{{--cream:#fcfaf5;--ink:#1a3300;--yellow:#ffe95c;--line:#dcd6c4}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--cream);color:var(--ink);
  font-family:'Bricolage Grotesque',system-ui,'Segoe UI',sans-serif;line-height:1.6}}
.wrap{{max-width:1100px;margin:0 auto;padding:0 20px}}
h1{{font-size:clamp(40px,9vw,90px);line-height:.9;font-weight:800;letter-spacing:-.04em;
  text-transform:uppercase;margin:0 0 18px}}
h2{{font-size:clamp(26px,4.5vw,40px);font-weight:800;letter-spacing:-.03em;
  text-transform:uppercase;margin:38px 0 14px}}
table{{width:100%;border-collapse:collapse;font-size:14px;min-width:820px}}
th{{background:var(--ink);color:var(--cream);padding:9px 10px;text-align:left;
  font-family:ui-monospace,monospace;font-size:11px;text-transform:uppercase;cursor:pointer;white-space:nowrap}}
th:hover{{background:#2b4d0f}}
td{{padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}}
td.num{{font-family:ui-monospace,monospace;text-align:right;white-space:nowrap}}
td.nm{{font-weight:800;white-space:nowrap}}
.smiles{{font-family:ui-monospace,monospace;font-size:11.5px;word-break:break-all;color:#2b4d0f;display:block}}
.scroller{{overflow-x:auto}}
.tools input,.tools select{{font-family:ui-monospace,monospace;font-size:12px;padding:6px 8px;
  border:1px solid var(--line);background:var(--cream);color:var(--ink)}}
sup.refmark{{font-family:ui-monospace,monospace;font-size:10px;font-weight:700;
  background:var(--yellow);border:1px solid var(--ink);padding:0 4px;margin-left:2px}}
.refs{{list-style:none;padding:0}}
.refs li{{padding:9px 0;border-bottom:1px solid var(--line);font-size:14px}}
.refs .meta{{display:block;font-family:ui-monospace,monospace;font-size:11.5px;color:#5c6b52}}
.refs a{{color:#2b4d0f}}
@media(max-width:820px){{body{{font-size:16px}}}}
</style>
</head>
<body>
<div class="wrap">
  <h1>Report<br><span style="font-size:.32em;font-weight:400;text-transform:none">tên phụ</span></h1>
  {BODY}

  <h2>Bảng dữ liệu</h2>
  <div class="tools">
    <input id="q" type="search" placeholder="Tìm..." aria-label="Tìm">
    <select id="sort" aria-label="Sắp xếp">
      <option value="en">Theo tên</option>
      <option value="hw">Khối lượng ↑</option>
      <option value="-hw">Khối lượng ↓</option>
      <option value="psa">TPSA ↑</option>
    </select>
  </div>
  <div class="scroller"><table id="tbl">
    <thead><tr>
      <th data-k="en">Tên</th><th data-k="en">CID</th><th data-k="en">Công thức</th>
      <th data-k="hw">MW</th><th data-k="lp">XlogP</th><th data-k="psa">TPSA</th>
      <th data-k="en">SMILES</th>
    </tr></thead>
    <tbody>{trs}</tbody>
  </table></div>
  <p><span id="cnt">{len(ROWS)} / {len(ROWS)}</span></p>

  <h2>Tài liệu tham khảo</h2>
  <ol class="refs">{refs_html}</ol>
</div>

<script>
(function(){{
  var tbl=document.getElementById('tbl'), q=document.getElementById('q'),
      sel=document.getElementById('sort'), cnt=document.getElementById('cnt');
  if(!tbl) return;
  var tb=tbl.tBodies[0], all=Array.prototype.slice.call(tb.rows);

  // QUAN TRỌNG: chỉ số cột trong mảng này phải khớp đúng <th> của bảng.
  // Sai chỉ số → fallback so sánh chuỗi → sort sai hướng, filter vẫn "chạy" nên rất khó phát hiện.
  var cells={{0:'en',1:'en',2:'en',3:'hw',4:'lp',5:'psa',6:'en'}};

  function key(r,k){{
    if(k==='en') return (r.cells[0].getAttribute('data-en')||'').toLowerCase();
    var v=parseFloat(r.getAttribute('data-'+k));
    return isNaN(v)?0:v;
  }}
  function apply(){{
    var term=(q.value||'').toLowerCase().trim();
    var s=sel.value, desc=s.charAt(0)==='-', k=desc?s.slice(1):s;
    var vis=all.filter(function(r){{
      return !term || (r.textContent||'').toLowerCase().indexOf(term)>-1;
    }});
    vis.sort(function(a,b){{
      var x=key(a,k), y=key(b,k);
      if(x===y) return a.cells[0].textContent.localeCompare(b.cells[0].textContent);
      return (x>y?1:-1)*(desc?-1:1);
    }});
    all.forEach(function(r){{ r.style.display='none'; }});
    vis.forEach(function(r){{ r.style.display=''; }});
    tb.appendChild.apply(tb, vis);
    cnt.textContent=vis.length+' / '+all.length;
  }}
  tbl.querySelectorAll('th').forEach(function(th,i){{
    th.addEventListener('click',function(){{
      tbl.querySelectorAll('th').forEach(function(t){{t.classList.remove('sorted');}});
      th.classList.add('sorted');
      if(cells[i]) sel.value=cells[i];
      apply();
    }});
  }});
  q.addEventListener('input',apply);
  sel.addEventListener('change',apply);
  apply();
}})();
</script>
</body>
</html>
"""

# ---------- citation renumber: PMID → [n] ----------
_MARK = r'(?:\\?)refmark(?:\\?)">\[(\d{8})\]'
_used = set(_re.findall(_MARK, HTML))
_missing = _used - set(CITED)
assert not _missing, f"PMID được trích dẫn nhưng không có trong CITED: {_missing}"
HTML = _re.sub(r'<span class="(?:\\?)refmark(?:\\?)">\[(\d{8})\]</span>',
               lambda m: f'<sup class="refmark">[{CITED.index(m.group(1)) + 1}]</sup>', HTML)

# ---------- tag balance ----------
from html.parser import HTMLParser

_VOID = {"area","base","br","col","embed","hr","img","input","link","meta",
         "param","source","track","wbr"}


class _Bal(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors = [], []

    def handle_starttag(self, t, a):
        if t not in _VOID:
            self.stack.append((t, self.getpos()))

    def handle_endtag(self, t):
        if t in _VOID:
            return
        if not self.stack:
            self.errors.append(f"stray </{t}> line {self.getpos()[0]}")
            return
        if self.stack[-1][0] != t:
            self.errors.append(
                f"crossed: <{self.stack[-1][0]}> line {self.stack[-1][1][0]} "
                f"vs </{t}> line {self.getpos()[0]}")
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == t:
                    del self.stack[i:]
                    return
            return
        self.stack.pop()


_b = _Bal()
_b.feed(HTML)
if _b.errors or _b.stack:
    print("TAG PROBLEMS:")
    for e in _b.errors:
        print("  ", e)
    for t, p in _b.stack:
        print(f"   unclosed <{t}> line {p[0]}")
    raise SystemExit(1)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)

print("WROTE", OUT)
print("size KB:", round(os.path.getsize(OUT) / 1024, 1))
print("rows:", len(ROWS), "| refs:", len(CITED), "| cited:", len(_used))
print("uncited refs:", sorted(set(CITED) - _used) or "none")
print("superscripts:", HTML.count('sup class="refmark"'))