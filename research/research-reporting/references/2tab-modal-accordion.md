# 2-Tab Modal + Accordion Pattern (Premium B/W/Y)

Chốt 16-17/08/2026 trên `premix-heo` (25 thành phần, 147 PMID) và `berberine-tannin-extraction` (16 topics, 78 PMID). Mẫu chạy OK: `D:/Hermes Proj/premix-heo-research/build_premix.py`, `D:/Hermes Proj/berberine-tannin-extraction/build_extraction.py`.

## Khi nào dùng

- Research JSON → 2-tab HTML có nhiều thành phần/topic (≥8) mà mỗi cái có chi tiết dài (mechanism + evidence + PMID + safety).
- User phản hồi: "visualize bị cắt chưa đủ thông tin", "học thuật khó đọc toàn đoạn văn".

## Tab Visualize: card grid + modal popup

Card (`.pc`, grid 2 cột, mobile 1 cột):
```html
<div class="pc" onclick="openModal('beta-glucan')">
  <div class="pchead"><b>Beta-glucan</b><span class="pev pev-mạnh">Mạnh</span></div>
  <div class="pcdose">100–1000 mg/kg</div>
  <p class="pcsum">Tóm tắt ~110 ký tự...</p>
  <div class="pctap">Bấm xem chi tiết →</div>
</div>
```

Modal (mỗi item 1 div, đặt cuối body trước script):
```html
<div class="modal" id="m-beta-glucan" onclick="if(event.target===this)closeModal('beta-glucan')">
  <div class="mbox">
    <button class="mclose" onclick="closeModal('beta-glucan')">×</button>
    <h3 class="mtitle">Beta-glucan <span class="latin">Beta-glucan (yeast cell wall)</span></h3>
    <div class="mcat">Beta-glucan</div>
    <div class="mdose"><b>Liều:</b> 100–1000 mg/kg</div>
    <p class="msumm">Tóm tắt đầy đủ...</p>
    <h4>Cơ chế</h4><ul><li><b>Cơ chế 1.</b> Chi tiết <code>[PMID 12345]</code></li></ul>
    <h4>Bằng chứng trên heo</h4><ul><li>Effect <code>(in vivo heo, Mạnh, PMID 12345)</code></li></ul>
    <h4>Bệnh liên quan</h4><ul><li><b>Bệnh:</b> vai trò <code>[PMID 12345]</code></li></ul>
    <p class="msafe"><b>An toàn:</b> ...</p>
    <h4>Tham khảo</h4><div class="ref"><b>Label</b> note <code>[PMID 12345]</code></div>
  </div>
</div>
```

CSS modal:
```css
.modal{display:none;position:fixed;inset:0;z-index:200;background:rgba(0,0,0,.82);overflow-y:auto;-webkit-overflow-scrolling:touch;padding:20px}
.modal.open{display:block}
.mbox{position:relative;max-width:640px;margin:24px auto;background:var(--surface);border:1px solid var(--border);border-radius:28px;padding:28px 24px 32px}
.mclose{position:absolute;top:14px;right:14px;width:40px;height:40px;border-radius:50%;border:1px solid var(--border);background:var(--surface2);color:var(--text);font-size:20px;cursor:pointer}
.mtitle{font-size:20px;font-weight:700;margin:0 40px 4px 0;padding-left:14px;border-left:4px solid var(--yellow)}
.mtitle .latin{font-size:13px;color:var(--text2);font-weight:400;display:block}
.mcat{display:inline-block;font-size:11px;color:var(--yellow);border:1px solid rgba(255,214,0,.3);border-radius:999px;padding:3px 10px;margin:10px 0 6px}
.msumm{font-size:14px;color:var(--text2);margin-bottom:14px}
.mbox h4{font-size:14px;font-weight:700;color:var(--yellow);margin:16px 0 8px}
.mbox ul{margin:0 0 10px 20px}
.mbox li{font-size:13.5px;color:var(--text);margin-bottom:6px}
.mbox code{background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:1px 6px;font-size:12px;color:var(--yellow)}
.msafe{font-size:13px;color:var(--text2);margin-top:10px;padding:10px 14px;background:rgba(68,199,103,.06);border-radius:12px}
```

JS modal:
```js
function openModal(id){const m=document.getElementById('m-'+id);if(m){m.classList.add('open');document.body.style.overflow='hidden';m.scrollTop=0;}}
function closeModal(id){const m=document.getElementById('m-'+id);if(m){m.classList.remove('open');document.body.style.overflow='';}}
document.addEventListener('keydown',e=>{if(e.key==='Escape'){document.querySelectorAll('.modal.open').forEach(m=>{m.classList.remove('open');document.body.style.overflow='';});}});
```

## Tab Học thuật: accordion + fact cards

Accordion mỗi topic:
```html
<div class="acc" id="t0">
  <button class="acchead" onclick="toggleAcc('t0')"><span class="acctag">1</span><span class="acctitle">Nguồn nguyên liệu</span><span class="accarrow">▾</span></button>
  <div class="accbody">
    <div class="acsum">Tóm tắt chủ đề...</div>
    <div class="fgrid">
      <div class="fc">
        <div class="fctop"><span class="fbadge fbadge-pap">PAPER</span><span class="fctags">PMID 12345 · Tạp chí</span></div>
        <div class="fctext">Fact nội dung...</div>
      </div>
    </div>
    <div class="accmd"><b>Quy trình / Thực hành.</b> Chi tiết quy trình...</div>
  </div>
</div>
```

Badge theo loại nguồn:
- PAPER → vàng `background:var(--yellow);color:#111`
- PATENT → xanh lá `background:var(--success);color:#111`
- DỮ LIỆU/industry → xám `background:#666;color:#fff`

CSS:
```css
.acc{background:var(--surface);border:1px solid var(--border);border-radius:18px;margin-bottom:12px;overflow:hidden}
.acchead{width:100%;display:flex;align-items:center;gap:12px;padding:16px 18px;background:transparent;border:0;color:var(--text);cursor:pointer;text-align:left;font-family:inherit}
.acctag{flex:0 0 30px;height:30px;border-radius:50%;background:rgba(255,214,0,.12);border:1px solid var(--yellow);color:var(--yellow);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px}
.acctitle{flex:1;font-size:15px;font-weight:600}
.accarrow{color:var(--text2);transition:transform .2s ease-out}
.acc.open .accarrow{transform:rotate(180deg)}
.accbody{display:none;padding:0 18px 18px}
.acc.open .accbody{display:block}
.acsum{font-size:14px;color:var(--text2);background:var(--surface2);border-radius:12px;padding:12px 14px;margin-bottom:14px}
.fgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.fc{background:var(--surface2);border:1px solid var(--border);border-radius:14px;padding:12px 14px}
.fctop{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px}
.fbadge{font-size:10px;font-weight:700;letter-spacing:.5px;border-radius:999px;padding:2px 8px;flex:0 0 auto}
.fbadge-pap{background:var(--yellow);color:#111}
.fbadge-pat{background:var(--success);color:#111}
.fbadge-ind{background:#666;color:#fff}
.fctags{font-size:11px;color:var(--text2)}
.fctext{font-size:13px;color:var(--text);line-height:1.55}
.accmd{font-size:13.5px;color:var(--text);background:rgba(255,214,0,.05);border-left:3px solid var(--yellow);border-radius:0 12px 12px 0;padding:12px 14px;margin-top:12px}
@media(max-width:480px){.fgrid{grid-template-columns:1fr}}
```

JS:
```js
function toggleAcc(id){const a=document.getElementById(id);if(a){a.classList.toggle('open');}}
document.querySelectorAll('.acc').forEach(a=>a.classList.add('open')); // mặc định mở hết
```

## Builder pattern (Python generator)

- Generator đọc 4 JSON (8+8+8+1 = 25 items, mỗi item schema: id, name_vi, latin, category, summary, mechanisms[], pig_evidence[], diseases[], dosage, safety, references[]).
- Hàm `viz_item()` render card, `viz_modal()` render modal, `topics_acad()` render accordion. `mid = it['id'].replace('.','-')` — id chứa dấu chấm phải replace nếu dùng trong `getElementById`.
- 4 subagent JSON hay có cấu trúc khác nhau: group1 dùng `compounds`, group2 dùng `herbs`, group3/4 là list thuần. Loader phải thử `get('compounds') or get('herbs') or list`.
- Đếm PMID unique trước khi build: `collect_pmids()` đệ quy qua dict/list, in tổng để verify không mất data.

## Verify browser (đã chạy OK)

Serve local rồi Camofox evaluate:
```
JSON.stringify({modalOpen: document.querySelector('.modal.open')!==null, title: ...})
JSON.stringify({accs: document.querySelectorAll('.acc').length, openAccs: document.querySelectorAll('.acc.open').length, factCards: document.querySelectorAll('.fc').length})
JSON.stringify({docSW: document.documentElement.scrollWidth, innerW: window.innerWidth})  // phải bằng nhau
```
Test: click card → modal mở đúng title; click mclose → modal đóng; toggle accordion giảm openAccs; docSW == innerW (không tràn ngang).

## Pitfalls

- Modal phải nằm NGOÀI panel `.active` (cuối body, trước script) — nếu đặt trong panel bị `display:none` của panel chặn.
- Card cần `cursor:pointer` + hover border vàng để gợi ý click được.
- `body overflow:hidden` khi modal mở tránh scroll nền; nhớ reset khi đóng.
- Accordion mở hết mặc định (user thích thấy đủ), không đóng hết — gấp bớt là hành động của user.
- KHÔNG cắt fact: card hiện tóm tắt ngắn, modal giữ 100% nội dung gốc (mọi mechanism/PMID).
