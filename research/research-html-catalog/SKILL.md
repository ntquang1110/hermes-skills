---
name: research-html-catalog
description: "Use when research output must be a catalog/table HTML page."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, html, catalog, subagent, json, mobile, table]
    related_skills: [research-reporting, web-research, camofox-browser, claude-design]
---

# Research → HTML Catalog (parallel subagent pipeline)

Use when the user wants a **structured catalog/table deliverable** from research: "list all X with mechanism + side effects", "bảng mỗi dòng = nguyên tố x tác dụng x cơ chế x tham chiếu", "danh sách chất + chi tiết từng chất", OR a full **multi-section editorial report** ("báo cáo toàn diện nhóm X") from already-collected data. Validated four times (piglet-diarrhea 40 chất, rare-earth 66 dòng, terpenoid 50 chất + 336 PubMed, 08–10/2026).

Complements `research-reporting` (which owns the publish → preview → KFlow hard default). This skill owns the **build side**: how to produce the HTML artifact efficiently and honestly.

**Two skins — pick by deliverable shape:**
- **Tra cứu / catalog, filter+search, mobile, dark Premium B/W/Y** → `references/subagent-schema-and-build.md`
- **Báo cáo đọc tuần tự, editorial, light Say Briefly** → `references/editorial-report-template.md`
- **Chemistry/natural-product data (PubChem/PUG-View parsing)** → `references/pubchem-pugview-parsing.md`

## Pipeline (validated)

1. **Fan-out research**: `delegate_task` with 2-3 parallel leaf subagents, each writing JSON to `D:/Hermes Proj/<project>/data/group<N>_<name>.json` (subagent creates dirs via os.makedirs). Each subagent gets: exact schema, verify instructions (PubMed E-utilities curl esearch/efetch + Google Patents XHR), and the rule "NEVER fabricate PMID/patent — if unverifiable, write number='' + note='chưa verify'".
2. **While subagents run**, author `template.html` (mobile-first, Premium B/W/Y) + `build.py` in the same folder. Template holds `const DATA = __DATA__;` placeholder; build.py reads all group JSONs, injects via `html.replace("__DATA__", json.dumps(rows, ensure_ascii=False))`.
3. **Build** → verify in browser → publish via research-reporting pipeline (preview.thefirstonly.com + KFlow).

## Subagent schema (use for both catalogs)

Per-item keys that worked (piglet-diarrhea): `id, name_vi, name_en, latin, category, summary, mechanism[], evidence_level, dosage_ref, side_effects[], extraction{method,variants[],yield_tips,quality_control,risks[],mold_prevention,equipment} OR production{}, references[{type,label,pmid,doi,number,note}], verification`.

Table-row keys that worked (rare-earth, 1 row = 1 entity × 1 effect): `id, element, element_vi, name_en, effect, group, mechanism, evidence_level, dosage_ref, side_effects[], references[], verification`.

Add `verification` to EVERY item: what was efetch-verified, what is not. Users trust this.

## User research-integrity rules (Quang, bắt buộc)

- **Research ≠ marketing claim.** Research output MUST carry a visible banner: "KHÔNG dùng làm cơ sở claim sản phẩm". Product-doc rules (e.g. Kiềm Saphia bỏ đất hiếm) still apply — research is for knowing, not for advertising.
- **Evidence levels**: Mạnh / Vừa / Sơ bộ / Không có bằng chứng trực tiếp — assign honestly per item. When no direct pig trial exists, SAY SO in the row (e.g. "KHÔNG có trial heo; dữ liệu gián tiếp trên gà").
- **Include toxicity rows**, not just beneficial effects.
- **Verify regulatory claims from the source itself** — don't assume. This session: assumed EU had NOT approved rare-earth feed additives, but EFSA FEEDAP opinion + EU 2020/1370 actually approved Lancer (lanthanide citrate) for weaned piglets 250 mg/kg ≤120 days; Trung Quốc approved RECC since 2013; US FDA none. Check EFSA journal/registers before writing a "banned/unapproved" warning.
- Contradictory evidence is a feature: TQ reported ADG +12-19%, EU trials (112 piglets, 200 mg/kg, 6 wks) showed no effect — present both, don't average.

## Pitfalls (all hit in real sessions)

1. **JSON container key varies per subagent**: one wrote `{"compounds":[...]}`, another `{"lines":[...]}` with a `meta` dict. Build script must try in order: `list` → `compounds` → `lines` → `rows` → `items` → `data`.
2. **Category/chip exact-match**: HTML filter chips keyed by slug (`clay`) never match data category strings with diacritics (`Clay hấp phụ`). Use the data's exact category string as both chip key and filter value. Also handle multi-group values like `REE nặng`, `REE nặng + chung` — enumerate from data, don't guess.
3. **Vision-less verification** (deepseek-v4-flash): browser_vision/vision_analyze return 400 `unknown variant image_url`. Use playwright-core directly (see camofox-browser skill references) to run FUNCTIONAL JS checks: `setCat(...)` count, `toggle(0)` open state, search-input dispatch count, plus overflow detection (getBoundingClientRect right > viewport on h3/chips/boxes). Do NOT retry browser_console after repeated 500s — switch to the .cjs script.
4. **Camofox blocks file://** — serve via `python -m http.server` background, then navigate to http://127.0.0.1:port. Kill server after.
5. **Google Patents XHR throttles (503 "Sorry...")** — mark patents `number=''` + `note='chưa verify'`; never invent patent numbers. PubMed E-utilities is the reliable verify path.
6. **Hash routing for shareable detail views**: `showDetail` must set `location.hash = '#/ct/'+id` so refresh/deep-link works; `route()` on hashchange re-opens the same detail.
7. **Mobile layout**: chips row scrolls horizontally by design (overflow-x:auto) — a horizontal overflow "issue" on chips is expected, not a bug; check only content elements.
8. **PUG-View `Information[]` needs a RECURSIVE flattener — a shallow walk silently returns 0 rows.** The value lives at `Section[].Information[].Value.StringWithMarkup[].String`, arbitrarily nested, with sibling keys (`Number`, `String`, `DateISO8601`, `Boolean`). A walker that only checks `if 'StringWithMarkup' in v` collects nothing and prints `total rows: 0` for every record — looks like empty data, is actually a broken parser. Debug by dumping ONE record's keys first (`print(list(rec['Section'][0].keys()))`, then recurse into `Section[].Section`) before concluding the source is empty. Verified pattern in `references/pubchem-pugview-parsing.md`.
9. **Never join chemistry records by compound NAME — case and stereoprefix break the match.** Collected JSONs disagree systematically: `Ursolic acid` (PubChem PUG) vs `(+)-Ursolic Acid` (record title) vs `(+)-ursolic-acid`; `beta-Carotene` vs `Beta-Carotene`; `Lutein` vs `Lutein A`; `d_limonene` vs `D-limonene`. Case-sensitive name join linked 5/12 records. Resolve in this order: **exact CID → lowercased-and-`( +)-`-stripped name → first InChIKey skeleton (text before the first `-`)**. Also note CID itself varies across sources for the same substance (PubChem CID ≠ PUG-View file CID for stereo variants), so treat CID as a *hint*, not a guarantee.
10. **physchem.json values are lists-of-lists-of-dicts, not strings.** Shape is `[[{'String': 'x'}], [{'String': 'y', 'Markup': [...]}, ...]]`. Flatten recursively and **dedupe preserving order** (the same fact recurs from HSDB + NTP + other depositors — that redundancy is provenance, not noise). Render a joined " · " string, not a Python repr. Never assume `value[0]` is the field.
11. **ECHA GHS "Not Classified" means NO DATA, not SAFE.** Aggregated text reads "does not meet GHS hazard criteria for 98.9% (92 of 93) of all reports" — i.e. 92/93 companies simply never filed a notification. Rendering that as "an toàn" inverts the evidence. Always capture the **denominator** and say so: "GHS 'Not Classified' vì 92/93 doanh nghiệp không nộp thông báo — KHÔNG phải vì đã chứng minh an toàn." Same trap as pitfall on rare-earth feed additives in `research-reporting`. Extract H-codes with a regex over `H\d{3}[^:|]{0,80}?\[` and pull the `(\d+\.\d+)%` beside it.

12. **Schema text missing after a compaction handoff → derive it from the project's own builder, never invent it.** A delegate prompt said *"đúng schema bên dưới"* but the schema block itself was lost in compaction. Fix, in this order: read `data/group0*.json` (the demo/test file kept in every one of these projects) for the canonical sample row, then read `build.py` and list every key its normalizer `pick()`s. Emit `{meta, lines:[...]}`. Full recipe: `references/group-json-conformance.md`.
13. **Custom nested fields are SILENTLY DROPPED.** `build.py:norm_row()` rebuilds the display `extra` dict from a **whitelist of top-level keys only** — `nhom_hoa_hoc, xep_loai, canh_bao, maillard, phap_ly_vn, legal_vn, tg_kho_C, hut_am_drh, trong_so_tinh_diem, ket_luan_1_dong, effect, mechanism, route, approval, ksp, side_effects, dosage_ref, element`. A row that looks perfect in the JSON but keeps its payload under `extra: {...}` renders with empty sections (verified: `extra keys: []` for all 52 rows). Promote the payload to those exact key names; put free-form payloads (data tables) into `mechanism` with a `SỐ LIỆU:` block.
14. **`rating` must be an int** — `int(round(float(rating)))`, defaulting to **3** when it fails. Every row carrying a Vietnamese verdict string in `rating` silently became 3, which collapses the HTML grading + sort. Keep verdict text in `ph12` / `xep_loai` / `verdict`, and carry an explicit `{id: int}` score map in the merge script (document what the score means — for actives: stability at pH 12–14; for excipients: fit to the target).
15. **Don't collide with the shared build side-effects.** `build.py` writes `_khuyen_nghi.json` / `_nguon_B.json` from whichever group file defines `khuyen_nghi_cong_thuc` / `nguon` — sorted-glob order means your new group silently REPLACES group B's block. Omit those keys unless replacement is intentional.
16. **Verify conformance by importing the builder, not by eyeballing the JSON.** ~30 seconds, catches the whole class of drift above:
```python
import sys, json, io; sys.path.insert(0, '.'); import build
doc = json.load(io.open('data/groupC_x.json', encoding='utf-8'))
rows = [build.norm_row(r, 'Hoạt chất', 'groupC_x.json') for r in doc['lines']]
assert len(rows) == doc['meta']['so_dong']
print({k: sum(1 for r in rows if k in r['extra']) for k in ('Cơ chế','Xếp loại','Hút ẩm / DRH')})
print(sum(1 for r in rows if not r['thermal']), sum(1 for r in rows if not r['references']))
```
Then `python build.py` and grep the HTML for a handful of your ids — `cat` counts must match (`Hoạt chất 23 / Muối kiềm 18 / Thiết bị 6 / Hóa học pH 12 5` for a 52-row group).

17. **JS object literal rejects an UNQUOTED NEGATIVE KEY — and the failure is invisible.** `const RL = {-1:'x', ...}` is a `SyntaxError: Unexpected token '-'`. The entire `<script>` never parses, so the page renders with the hero only, every `innerHTML`-filled block empty, chips missing and list empty — while the server still answers **HTTP 200** and Camofox console capture is **unavailable** (it reports `total_messages: 0` regardless). Looks like a CSS/layout bug; is a dead script. Diagnose by evaluating in the page: `typeof DATA` → `'undefined'` means parse failure, not a runtime error. Fix: `'-1':'x'`. **Prevention (do this, it is the only check that catches the class):** in `build.py`, extract the `<script>` body, write it to `_chk.js`, run `subprocess.run(["node","--check",jsf])` and print `JS OK` / the stderr. Added this session after shipping one dead page; it found the bug in 2 seconds on the retry.
18. **Heterogeneous subagent schemas need an ADAPTER + a re-classifier, not a stricter schema mandate.** Three parallel leaf subagents returned three different containers/shapes (`{lines:[...]}` with `group`, `{items:[...], bang_xep_hang:[...]}`, `{lines:[...]}` with `cat`), and one group's 35 rows were **four kinds of content mixed together** (human drugs / pH-12 inorganic chemistry / Vietnamese legal texts / mine geology) all sharing `cat = '...hiếm'`. Result: the rating column collapsed to a constant 3 for 35 rows and the headings repeated the same element name 3 times. Fix, in order: (a) `pick(d, *aliases)` normalizer so each shape maps into one schema; (b) a per-group `classify_X(r, row)` that branches on the row's own `group` field and rewrites `cat`, `rating`, `name_vi`; (c) give reference-only rows (legal texts, background notes) `rating = -1` and render them as "Thông tin tham chiếu" with no dots — and remember to widen the clamp to `max(-1, min(5, float(rating)))` or the -1 is silently squashed back to 0.
19. **Em dash arrives inside the DATA, not the template — sanitize the payload, not the HTML.** `grep -c '—' template.html` returned 1 while the built page had **95**. They all came from subagent prose. One `deep_clean()` walk over the parsed rows, applied immediately before `json.dumps`, fixed all of them (em dash → `·`, keeping en dash for numeric ranges). Checking only your own template guarantees a miss.
20. **Contrast must be COMPUTED, not eyeballed — and the token is usually what fails.** `--mut:#6b7a5c` on cream `#fcfaf5` is **4.41**, just under the 4.5 AA floor, and it is the most-used token in the page (captions, refs, English names) → **1337 low-contrast text nodes**. Compute candidate tokens offline in Python first, then re-measure in the browser: walk every leaf node, resolve the effective background up the ancestor chain (skip `rgba(0,0,0,0)`), apply the relative-luminance formula. Two token changes (`--mut` → `#5c6a4d` = 5.56, `--orange`/`--cond` → `#a85a00` = 4.88) dropped it 1337 → **89**, and the remaining 89 are the deliberately faint empty rating dots. Don't chase those.
21. **`code{font-size:.92em}` breaks the 12px floor inside 13px table cells** — 13 × 0.92 = **11.96**, which `verify-deliverable.cjs` flags as `1 text nodes under 12px` at 360/390px only (desktop passes, so a desktop-only check misses it). Use `font-size:max(12px,.92em)`.
22. **`verify-deliverable.cjs` runs from ANY cwd via `NODE_PATH`** pointing at an existing `playwright-core` — no need to copy the script into the repo (which the older skill text told you to do): `export NODE_PATH="D:/Hermes Proj/camofox-browser/node_modules" && node "$HOME/AppData/Local/hermes/skills/devops/camofox-browser/scripts/verify-deliverable.cjs" "<url>" 12`. Its JSON tail is long; pipe through a 6-line Python filter to print one row per viewport + `FAILURES` + `VERDICT` instead of reading 40 lines.

23. **NEVER derive a "legally excluded" flag from PROSE — the same words mean opposite things.** Real case: a materials group where 4 rows read *"KHÔNG được phép dùng như phụ gia thực phẩm"* (a true ban) while other rows read *"dùng với tư cách nguyên liệu/đường, **không phải phụ gia** trong TT 24/2019"* — the exact phrase `không phải phụ gia` in the second case means **permitted and better** (a food ingredient, not a restricted additive). A substring regex flagged Trehalose, WPI, Inulin and Bentonite as banned; Trehalose at 78.4/100 is a top-tier choice. **Fix: use the ONE structured signal the data already carries** — `xep_loai.startswith("E – LOẠI")`. Five rows, zero false positives. General rule: when a dataset has both prose verdicts and a curated grade field, only ever branch on the grade field; report the prose in the detail panel and let the reader see it.
24. **A high chemistry score next to a "loại" verdict is the contradiction a careful reader catches first.** Score 79.6/100 + four filled "Phù hợp" dots while the verdict says "excluded" reads as *usable*. Give legal exclusion its own state, distinct from a low score: `rating = -2` → label **"Loại vì pháp lý"**, no dots at all, red token (`--red`), bold. Widen the clamp to `max(-2, min(5, ...))` or the -2 is squashed, add `'-2'` to `RL` (quoted!), and **sort blocked rows last inside their category** — `key=(..., 0 if rating >= 0 else 1, -score, name)` — otherwise a banned substance with a high score still sits at the top of the list. Verify after building: count `document.querySelectorAll('.lbl.r-2')` and assert `.dots` is empty for those rows.


## 25. Them tang GIA vao bang xep hang: 4 luat bat buoc

Khi ghep du lieu gia tu nhieu nguon nghien cuu vao mot bang xep hang:

1. **O SO CHI NHAN SO THAT.** Regex vot so trong chuoi se bien ma CAS
   `9004-32-4` thanh gia 9.004 d/kg, va `EE 83,67-89,98%` thanh 83,67.
   Phai: nhan int/float, hoac chuoi ma PHAN CON LAI sau so chi gom don vi
   (%, d, kg, USD). Van xuoi -> None, va giu nguyen cau do lam GHI CHU.
   Chan rieng mau `\d\s*-\s*\d\s*-\s*\d` (ma CAS/so hieu).

   **Ca thu 2 cua cung cai bay: dau cham vua la phan nghin vua la thap phan.**
   `180.000` = 180000 (VN) nhung `0.207` = 0,207 (USD/kg), khong phai 207.
   Quy tac chan: neu nhom truoc dau cham la `"0"` thi LUON la thap phan (so
   dinh dang khong bao gio bat dau bang 0). Subagent tra gia quoc te doi khi
   tra ve dang `0.207` va bi doc thanh 207 d/kg => gia sai 1000 lan. Test ca
   hai chieu: `180.000`->180000, `0.207`->0.207, `3.08`->3.08, `25.700`->25700.

2. **Chi phi de ra 1 kg thanh pham, khong phai gia 1 kg nguyen lieu.**
   `chi_phi = gia x lieu / hieu_suat_thu_hoi`. Chat re dung lieu 40% dat hon
   chat mac dung lieu 3%. Diem gia theo thang LOG vi gia trai 100-150 lan.

3. **Khong so chi phi giua cac chat khac VAI TRO LIEU.** Chat dung 0,3%
   (phu gia tao nhot, on dinh) se luon "re nhat" theo dinh nghia, vi no gan
   nhu khong gop khoi luong vao bot. Phai chia: lieu >=10% = chat mang nen
   (moi so sanh duoc), 3-10% = mang/phu, <3% = lieu nho (chi hien so, khong
   xep hang). Day la loi tung lot qua that: CMC 0,3% hien 465 d/kg bot va
   dung dau bang "re nhat".

4. **Dong bi loai vi PHAP LY khong bao gio duoc dung dau bang "re nhat".**
   Sap xep theo gia/chi phi van phai day chung xuong cuoi. Nguoi doc luot se
   tuong zeolite dung duoc chi vi no hien o vi tri so 1.

Them: **4 subagent nghien cuu = 4 schema khac nhau** (gia la dict long
`{vn:{gia_thap,gia_cao},tq:{}}`, hoac so tran, hoac `price_vn_min/max`,
hoac ten truong tu dat). Bo doc phai chiu duoc het va co alias, neu khong
se mat sach du lieu cua mot nhom ma khong bao loi.

## 26. Truong nao do duoc "loai vi phap ly": CHI dung truong CO CAU TRUC

Khong bao gio suy co "bi cam" tu van xuoi. Cung cum "khong phai phu gia":
- Trehalose: "dung voi tu cach nguyen lieu, khong phai phu gia" -> NGHIA LA
  DUOC PHEP (va con tot hon, vi khong bi gioi han nhu phu gia).
- HP-beta-cyclodextrin: "khong duoc phep dung nhu phu gia thuc pham" ->
  NGHIA LA BI CAM.

Chi doc truong xep hang co cau truc (`xep_loai` bat dau bang "E - ", hoac
`phap_ly_vn.trang_thai`). Case that: heuristic van xuoi bat 9 dong, dung chi
co 5; no ban nham ca Trehalose 78,4 diem.

## 27. Tang ghep du lieu PHAI mang theo CANH BAO HOA HOC, khong chi mang so

Subagent nghien cuu thuong tra ve 2 loai truong khac nhau:
- truong SO (gia, lieu, hieu suat) -> de ghep vao bang
- truong VAN XUOI (canh bao phoi tron, tuong thich pH, phan huy nhiet) ->
  RAT DE BI BO QUEN khi viet ham `attach()`, va do la loai thong tin lam
  hong cong thuc.

Loi tung xay ra: bang xep hang cho CaCO3 dung dau chi phi (526 d/1 kg bot),
nhung canh bao "Ca2+ ket tua voi PO4^3-/SiO3^2- khi phoi C08/C10" bi tang
gia nuot mat. Nguoi doc chon chat re nhat roi ghep voi dung chat dem kia ->
cong thuc hong ngay o buong say, va bang xep hang khong he bao.

Bat buoc: khi ghep, liet ke het cac truong van xuoi cua nguon va mang nguyen
van vao mot truong rieng (`canh_bao_phoi` / `ghi_chu_*`). Roi hien thanh
MOT BANG RIENG, tach khoi bang diem, va:
- Tu khoa XUNG DOT that su: `ket tua|an mon|phan huy|khong phoi|tuong tac|
  truong no|tao phuc` -> danh dau do + xep len truoc.
- Ghi chu con lai (gioi han giu pH, do tan, gia grade) -> de nguyen phia sau.
- TUYET DOI khong dat tieu de kieu "khong phoi duoc voi nhau" cho mot bang
  ma phan lon noi dung la "chi giu duoc pH 10-11,5". Nhan sai noi dung =
  nguoi doc bo qua bang.

## 28. Do bang canh bao can kiem ca HINH LAN CHU

Sau khi do bang canh bao, phai chay lai Playwright va IN RA 4 dong dau tien
cua bang, khong chi dem so dong. Dem 33 dong khong noi duoc dong nao dang o
dau. Chi khi in ra moi thay: dong 1 la bentonite (gioi han pH) chu khong phai
xung dot that, tuc thu tu dang sai va tieu de dang noi doi.

- `references/group-json-conformance.md` — derive-the-schema recipe, fragment-write technique for large row sets, merge/transform script skeleton, conformance checklist.

- `references/subagent-schema-and-build.md` — exact subagent prompt skeleton, build.py pattern, playwright check script skeleton (copy-paste starting points).
- `references/pubchem-pugview-parsing.md` — working recursive PUG-View walker, physchem flattener, CID/name/InChIKey compound resolver, GHS-aggregate parser (validated on a 12-record / 4,948-row terpenoid corpus).
- `references/editorial-report-template.md` — Say Briefly light-editorial skin: tokens, component vocabulary (incl. the DM Sans vs Inter font trap), 7-section report shape, long-script split.

See `research-reporting` for publish + KFlow steps (hard default, don't skip).
