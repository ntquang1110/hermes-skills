---
name: visual-academic-html
description: "Turn a KFlow card into a 2-tab HTML: Visualize + Học thuật."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [html, visualize, kflow, research, premium-bwy, tabs, markdown]
    related_skills: [html-publishing, dashboard-design-system, knowledge-researcher, impeccable]
---

# Visual + Academic 2-Tab HTML

## Trigger

User Quang nói: "bài nào cũng làm 2 tab: Visualize + Học thuật", "dựng visual flow từ bài học thuật", "đóng skill này để áp dụng bài tiếp theo". Mọi bài học thuật / card KFlow → HTML DUY NHẤT có 2 tab.

## Quy tắc cốt lõi (Quang chốt 10/08/2026)

1. **1 file HTML, 2 tab**: tab **Visualize** (dễ hiểu, flow từng bước) + tab **Học thuật** (nội dung gốc nguyên vẹn, đủ PMID).
2. Design LUÔN theo Premium B/W/Y (`dashboard-design-system` skill): bg `#0D0D0D`, surface `#1B1B1D`, yellow `#FFD600`, card radius 28, mobile-first 360+.
3. Tab Visualize: bắt đầu bằng **Bản đồ dòng chảy** (8-10 chặng: phân tử → từng cơ chế → bằng chứng → mục tiêu), mỗi cơ chế 1 bước với mini-flow chip (CA → Keap1 → Nrf2 → HO-1), callout đánh dấu ý nghĩa thực tế, kết bằng card vàng **Mục tiêu** với 3 hành động cụ thể.
4. Tab Học thuật: GIỮ NGUYÊN 100% nội dung card gốc như KFlow app hiển thị: strip `<!--OVERVIEW-->` block (KFlow cũng strip), render markdown → styled HTML. Nếu card có `summary`, hiển thị box summary phía trên (giống KFlow). KHÔNG thêm header/tag/h1/meta/src-note tự chế — đó là lỗi Quang bắt được (10/08/2026: "sao anh thấy khác nhau rồi"). Verify bằng diff text: render md gốc cùng pipeline rồi so text thuần với #pa → phải IDENTICAL.
5. Publish preview.thefirstonly.com + verify HTTP 200. KHÔNG lưu KFlow nếu đây là bản visual của card đã có (tránh duplicate).

## Trình bày tab Học thuật (Quang chốt 17/08/2026 — "ok em apply cho trang sau nữa nhé, lưu lại đi")

KHÔNG dùng đoạn văn dài + bullet list đơn điệu cho phần Học thuật. Áp dụng 4 kiểu sau (verified trên trang berberine-tannin 17/08):

1. **Accordion**: mỗi chủ đề = 1 thanh ngang (số vàng tròn `.acctag` + tiêu đề `.acctitle` + mũi tên xoay `.accarrow`), bấm gấp/mở `.accbody`. CSS: `.acc` surface + border radius 18, mặc định JS mở hết (`document.querySelectorAll('.acc').forEach(a=>a.classList.add('open'))`), `toggleAcc(id)` toggle class `open`.
2. **Fact cards**: mỗi dữ kiện 1 card nhỏ `.fc` trong grid 2 cột (mobile 1 cột), badge màu theo loại nguồn `.fbadge`:
   - `fbadge-pap` (PAPER, nền vàng) — nghiên cứu, kèm PMID
   - `fbadge-pat` (PATENT, nền xanh lá) — patent, kèm số patent
   - `fbadge-ind` (DỮ LIỆU, nền xám) — số liệu công nghiệp/khác
   Tags nguồn (PMID/patent/URL) nằm trên cùng `.fctags`, text dữ kiện `.fctext` bên dưới.
3. **Tóm tắt nhanh**: box `.acsum` (surface2, radius 12) ở đầu mỗi chủ đề — 1-2 câu ý chính trước khi vào fact cards.
4. **Callout quy trình**: phần thực hành/quy trình từng bước tách riêng `.accmd` (border-left vàng 3px, nền vàng 5%) — không lẫn vào lý thuyết.

HTML mẫu (đã chạy OK):
```html
<div class="acc" id="t0">
  <button class="acchead" onclick="toggleAcc('t0')"><span class="acctag">1</span><span class="acctitle">Chủ đề</span><span class="accarrow">▾</span></button>
  <div class="accbody">
    <div class="acsum">Tóm tắt 1-2 câu</div>
    <div class="fgrid">
      <div class="fc"><div class="fctop"><span class="fbadge fbadge-pap">PAPER</span><span class="fctags">PMID 12345678</span></div><div class="fctext">Nội dung dữ kiện</div></div>
    </div>
    <div class="accmd"><b>Quy trình / Thực hành.</b> Các bước…</div>
  </div>
</div>
```
JS: `function toggleAcc(id){const a=document.getElementById(id);if(a){a.classList.toggle('open');}}` + mở mặc định tất cả.

## Workflow

### Bước 1 — Lấy card gốc từ KFlow
```bash
curl -s --max-time 55 "http://localhost:3003/api/cards" -H "Cookie: tfo_auth=1d1e977a218bfa01fe61106c360c8acf667047e35f17fdb0f1a8484e06cfdb55" | python -c "
import sys, json
cards = json.load(sys.stdin)
found = [c for c in cards if str(c.get('id','')) == '<CARD_ID>'] or [c for c in cards if '<Từ khóa>' in c.get('title','')]
with open('C:/Users/NTQUANG_DELL/hermes-temp/card.md', 'w', encoding='utf-8') as f:
    f.write(found[0].get('content',''))
print('saved', len(found[0].get('content','')))
"
```

### Bước 2 — Dựng tab Visualize
Thiết kế flow từ OVERVIEW JSON của card (what/why/mechanism/players/applications/limits/analogy). Cấu trúc chuẩn:
1. Hero: 1 câu chủ đề + 3 stat nổi bật (số liệu quan trọng nhất)
2. Bản đồ dòng chảy: flowchain dọc 8-10 fnode (số tròn vàng, nối line)
3. Mỗi cơ chế = 1 section `.sec` với `.step-num` + `.mflow` (mini chips + mũi tên)
4. Bằng chứng in vivo: card highlight + `.evrow` (badge + tx + PMID)
5. Phối trộn: `.combo` cards; Liều: `.dose` rows; Rào cản → Giải pháp: `.ps` pairs
6. Kết: `.goal` card vàng "Mục tiêu" + 3 `.act`
7. Footer: chips PMID + nguồn gốc card

### Bước 3 — Dựng tab Học thuật (markdown → HTML)
```python
import re, markdown
md = re.sub(r'<!--OVERVIEW-->.*?<!--/OVERVIEW-->', '', md, flags=re.DOTALL).strip()
acad = markdown.markdown(md, extensions=['tables', 'sane_lists', 'fenced_code', 'attr_list'])
```
CSS bắt buộc cho `.acad`: h2 có border-left vàng 4px, table bg surface + th vàng, blockquote border vàng trái, code chip vàng.

### Bước 4 — Tabs UI + fix overflow mobile
- Sticky tabbar 2 nút pill: Visualize (yellow active) / Học thuật. `showTab(k)` toggle `.active`, scrollTo top.
- **BẮT BUỘC fix bảng tràn mobile**: th KHÔNG `white-space:nowrap`; JS bọc mọi table trong `#pa`:
```js
document.querySelectorAll('#pa table').forEach(t => {
  const w = document.createElement('div'); w.className = 'tbl-wrap';
  t.parentNode.insertBefore(w, t); w.appendChild(t);
});
```
CSS: `.tbl-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:18px 0}` + `.tbl-wrap table{min-width:420px}`.
- Scroll progress chỉ chạy khi tab Visualize active.

### Bước 5 — Audit (KHÔNG bỏ qua)
Serve HTTP local + mở Camofox:
```bash
cd "/d/Hermes Proj" && python -m http.server 8898 --bind 127.0.0.1  # background
# POST /tabs -> lấy TABID, set viewport 390x844
# POST /tabs/:id/evaluate — click từng tab + kiểm tra:
# docSW <= innerW (hết tràn ngang page), .tbl-wrap đủ 4, active panel đúng
```
Mở cả 2 tab, chụp screenshot (fullPage) làm bằng chứng.

### Bước 6 — Publish
```bash
python -c "
import json
payload = json.dumps({'content': open('D:/Hermes Proj/<file>.html', encoding='utf-8').read(), 'title': '...'}, ensure_ascii=False)
open('C:/Users/NTQUANG_DELL/hermes-temp/payload.json','w',encoding='utf-8').write(payload)"
curl -s -X POST "https://preview.thefirstonly.com/api/store" -H "Content-Type: application/json" --data-binary @"C:/Users/NTQUANG_DELL/hermes-temp/payload.json"
# verify: curl -s -o /dev/null -w "%{http_code}" <preview_url> -> 200
```
File >50KB luôn dùng `--data-binary @payload.json` (tránh ARG_MAX).

## Script mẫu

`scripts/build_2tab.py` — build script tái sử dụng (đọc card md + flow HTML v1, xuất 2-tab HTML). Copy ra, sửa 3 đường dẫn FLOW/CARD/OUT là chạy.

## Pitfalls

- **Camofox chặn `file://`** (400 trên /tabs) → luôn serve qua `http://127.0.0.1:8898/`.
- **Tab Học thuật KHÔNG được thêm thứ gì so với KFlow**: không header tự chế, không src-note, không meta. Chỉ summary (nếu có) + content gốc. Quang từng phát hiện khác biệt vì block header thêm vào — check bằng text-diff IDENTICAL trước khi publish.
- **Model deepseek-flash KHÔNG nhận image** (browser_vision/vision_analyze fail "unknown variant image_url") → audit layout bằng Camofox `/tabs/:id/evaluate` (DOM measure) + screenshot để user xem, KHÔNG tự nhìn được.
- **`white-space:nowrap` trên th = bảng tràn mobile** → tuyệt đối không dùng; dùng `.tbl-wrap` scroll.
- **HTML cũ extract**: lấy từ `<header class="hero">` tới `</footer>` bằng regex DOTALL.
- **Markdown OVERVIEW JSON block** phải strip trước khi convert (nếu không hiện JSON thô).
- Viết file build script bằng write_file, chạy bằng python — heredoc/echo strip dấu tiếng Việt.
- Bảng tham khảo PMID giữ nguyên như card gốc, không thêm bớt.

## Verification Checklist

- [ ] 2 nút tab hiển thị, bấm đổi được panel
- [ ] Tab Visualize: hero + bản đồ flow + các bước + goal card vàng
- [ ] Tab Học thuật: đủ bảng/quote/PMID, không mất nội dung
- [ ] Mobile 390px: `docSW == innerW` (không tràn ngang), bảng scroll trong wrapper
- [ ] Preview URL HTTP 200 + chứa cả "Visualize" và "Học thuật"
