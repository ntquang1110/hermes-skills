# Subagent prompt + build.py + playwright check skeletons

Copy-paste starting points from the validated 08/2026 sessions (piglet-diarrhea catalog, rare-earth REE table).

## 1. Subagent prompt skeleton (delegate_task, leaf role)

Dispatch 2-3 parallel tasks. Every task MUST include:

- **Context block** (Vietnamese, có dấu): user is chủ trại heo + sản xuất hoạt chất tại Việt Nam; output TIẾNG VIỆT có dấu; phân biệt mức bằng chứng.
- **The exact JSON schema** (paste verbatim, do not paraphrase) — see SKILL.md for the two validated schemas.
- **Verify instructions**:
  ```
  curl -sL --compressed 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<term>&retmax=6&retmode=json'
  curl -sL --compressed 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=<PMID>&rettype=abstract&retmode=text'
  Patent: https://patents.google.com/xhr/query?url=q%3D<kw>%26oq%3D<kw>  (nếu 503/block -> ghi number='' + note='chưa verify')
  ```
- **Honesty rule verbatim**: "TUYỆT ĐỐI KHÔNG bịa PMID/patent. Nếu không verify được patent thì ghi type=patent với number='' và note='chưa verify' thay vì bịa."
- **File path + validation**: "GHI FILE: D:/Hermes Proj/<project>/data/group<N>_<name>.json (tạo thư mục os.makedirs). Cuối in stdout: số dòng + PMID/patent verified + đường dẫn file."
- Prior verified PMIDs from past sessions can be given as "GỢI Ý PMID" but MUST be re-verified by the subagent (efetch) before use.

## 2. build.py pattern

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os, re, sys

BASE = r"D:/Hermes Proj/<project>"
DATA_DIR = os.path.join(BASE, "data")
TPL = os.path.join(BASE, "template.html")
OUT = os.path.join(BASE, "<name>.html")

def load_groups():
    rows = []
    for g in ["group1_x.json", "group2_y.json", "group3_z.json"]:
        p = os.path.join(DATA_DIR, g)
        if not os.path.exists(p):
            print(f"MISSING: {p}"); continue
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        # CRITICAL: container key varies per subagent — try all shapes
        items = data if isinstance(data, list) else data.get(
            "compounds", data.get("lines", data.get("rows",
            data.get("items", data.get("data", [])))))
        print(f"{g}: {len(items)} items")
        rows.extend(items)
    return rows

def normalize(rows):
    # setdefault every required key, dedupe by id
    ...
    return out

def main():
    rows = normalize(load_groups())
    html = open(TPL, encoding="utf-8").read()
    html = html.replace("__DATA__", json.dumps(rows, ensure_ascii=False, indent=1))
    open(OUT, "w", encoding="utf-8").write(html)
    print(f"WROTE: {OUT} ({os.path.getsize(OUT)} bytes)")
```

Template must contain exactly `const DATA = __DATA__;`. After build, run a field-completeness check:
```python
import json, glob
issues = []
for g in glob.glob('data/group*.json'):
    data = json.load(open(g, encoding='utf-8'))
    items = data if isinstance(data,list) else data.get("compounds", data.get("lines", data.get("rows", data.get("items", data.get("data", [])))))
    for it in items:
        if not it.get('summary'): issues.append(f"{it.get('id')}: thiếu summary")
        if not it.get('mechanism'): issues.append(f"{it.get('id')}: thiếu mechanism")
        if not it.get('references'): issues.append(f"{it.get('id')}: thiếu references")
print("issues:", len(issues))
```

## 3. Category/chip matching (the diacritics trap)

Data categories are Vietnamese strings WITH diacritics: `Clay hấp phụ`, `REE nặng`, `REE nặng + chung`, `Hỗn hợp/Quy định`, `Tinh dầu`.

WRONG: hardcode slug keys (`clay`, `hree`, `acid`) then compare `c.category === curCat`.
RIGHT: enumerate the actual categories from the JSON first, use the exact string as both chip key and filter value:
```js
const CATS = [['all','Tất cả'],['Tannin','Tannin'],['Clay hấp phụ','Clay'], ...];
// then filter with  r.group === curCat
```
When groups are heterogeneous, `python -c` over the data files with `collections.Counter` to list the real group strings before authoring CATS.

## 4. Playwright functional check skeleton (.cjs, run from camofox-browser dir)

Because deepseek-v4-flash has no vision (browser_vision/vision_analyze 400), and browser_console can 500-loop, use playwright-core directly. File MUST be `.cjs` (camofox-browser package.json is ESM).

```js
const { chromium } = require("playwright-core");
(async () => {
  const browser = await chromium.launch({
    executablePath: "C:/Users/NTQUANG_DELL/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe"
  });
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.goto("http://127.0.0.1:8732/<name>.html");
  await page.waitForTimeout(1500);

  // overflow: only content elements, NOT .chip (chips scroll horizontally by design)
  const list = await page.evaluate(() => {
    const vw = document.documentElement.clientWidth;
    const issues = [];
    document.querySelectorAll('.card h3, .row-head h3, .box, .ref, .note-warn').forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.right > vw + 2 || r.left < -2) issues.push({el: el.className.slice(0,18), right: Math.round(r.right), vw});
    });
    return {vw, rows: document.querySelectorAll('.row, .card').length, issues};
  });

  // filter + expand + search tests
  const filt = await page.evaluate(() => { setCat('REE nặng'); return document.querySelectorAll('#list .row').length; });
  const det = await page.evaluate(() => { setCat('all'); document.querySelectorAll('.row')[0].click(); const o = document.querySelector('.row.open'); return {m: o?.querySelector('.m')?.textContent?.slice(0,40), refs: o?.querySelectorAll('.ref').length}; });
  const srch = await page.evaluate(() => {
    const t = document.querySelector('#search');
    Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set.call(t, 'gadolinium');
    t.dispatchEvent(new Event('input', {bubbles:true}));
    return document.querySelectorAll('#list .row').length;
  });
  console.log(JSON.stringify({list, filt, det, srch, errors}));
  await browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
```

Run: `cd "D:/Hermes Proj/camofox-browser" && node tmp-check.cjs`. Delete temp .cjs files after.

## 5. Serve-before-navigate (Camofox blocks file://)

```bash
terminal(background=true, command="cd 'D:/Hermes Proj/<project>' && python -m http.server 8732 --bind 127.0.0.1")
# health: curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8732/<name>.html   # expect 200
# ... then browser_navigate(http://127.0.0.1:8732/<name>.html)
# cleanup: process(action='kill', session_id=...)
```
