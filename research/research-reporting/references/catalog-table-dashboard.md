# Catalog dạng bảng + Dashboard + Mindmap (verified 12/08/2026)

Áp dụng khi user yêu cầu catalog data dạng **bảng chia cột + search highlight** và/hoặc **dashboard thống kê + mindmap kiểu Obsidian**. Chạy thành công trên trang đất hiếm REE (66 dòng, 32 nguyên tố).

## Layout tổng thể

- 1 file HTML self-contained, placeholder `__DATA__` → build.py inject JSON (xem Pattern H).
- **2 tab** qua bottom nav: `showTab('table')` / `showTab('dash')` — toggle `#tabTable` vs `#dash`, active class trên nút nav.

## TAB BẢNG (4 cột — v3 user chốt 12/08: cơ chế RỘNG, ref GỌN)

```
<table> min-width:640px (v1 dùng 760px; v3 rút gọn để cột cơ chế rộng hơn trên mobile)
  <thead> Nguyên tố | Tác dụng | Cơ chế | Ref
```

- Cột Nguyên tố: badge element (màu theo group) + tên tiếng Việt + evidence level.
- Cột Cơ chế là cột CHÍNH: `min-width:240px; max-width:380px` (desktop ~333px), font 13px màu sáng #D6D6D6, cắt ~140 ký tự + "chi tiết →". User phản hồi trực tiếp: "cho cột cơ chế tác dụng to hơn".
- Cột Ref GỌN (`width:90px`, white-space nowrap): CHỈ badge số lượng `"6 refs →"` (kèm số patent nếu có: `"6 refs · 1 patent →"`). KHÔNG xếp PMID chips trong bảng — user chốt "ghi số lượng cũng được, bấm vào show ra sau". Bấm badge → mở modal danh sách refs + link PMID ra PubMed. BẮT BUỘC `onclick="event.stopPropagation();openModal('<id>')"` vì badge nằm trong `<tr onclick>` mở modal chi tiết — thiếu stopPropagation sẽ mở nhầm modal.
- Click dòng → modal bottom-sheet (`.modal-panel` slideUp, max-height 82vh): cơ chế đầy đủ, liều, tác dụng phụ/độc tính, refs (kèm "Mở nguồn ↗"), verification.
- Search realtime: `hl()` escape text trước rồi wrap từ khóa bằng `<mark>` (regex escape query). Áp cho cả cột element name + effect + mechanism.

## TAB DASHBOARD

```js
function elementStats(){
  const map = {};
  for(const r of DATA){ map[r.element] ??= {element:r.element, vi:r.element_vi||'', count:0, rows:[]}; ... }
  return Object.values(map).sort((a,b)=>b.count-a.count);
}
```

1. **Stats grid** (2 cột mobile, 4 cột desktop): tổng dòng, số nguyên tố/dạng riêng, bằng chứng Mạnh, "không có bằng chứng trực tiếp".
2. **Lưới số tác dụng theo chất**: `.el-card` click → `selectElem(element)` → re-render dash, card được chọn có border vàng.
3. **Mindmap SVG** (`drawMind(el)`): 
   - Chất trung tâm: rect vàng, text đen, kèm "N tác dụng".
   - Nhánh: n dòng data của chất đó, góc `-PI/2 + i/n*2*PI`, bán kính `R = min(210, 60 + n*22)`.
   - Mỗi node tác dụng: rect bo góc + text wrap tối đa 26 ký tự/dòng, 3 dòng. Màu viền: xanh dương (#448AFF) = có PMID, xanh lá (#44C767) = có patent, xám (#9A9A9A) = chưa ref.
   - Node kẹp trong viewBox (clamp bx/by). Click node → openModal; click tâm → selectElem (đổi chất).
   - viewBox 720×460, `svg{width:100%;height:auto}` responsive.

## Verify không vision (deepseek-v4-flash không nhận ảnh)

Dùng playwright-core `.cjs` (xem camofox-browser skill, đường dẫn chromium):
- Test: rows count, search trả đúng số dòng, search rỗng hiện empty state, filter theo group, click dòng → modal mở + link PMID đúng, JS errors = [].
- browser_console trên Camofox có thể trả 500 → retry 1 lần hoặc dùng playwright `page.evaluate` (đáng tin hơn).

## Pitfall

- Filter chip key phải khớp category trong data (case-sensitive, "REE nặng" ≠ "HREE", "Clay hấp phụ" ≠ "Clay").
- Build script thử nhiều key JSON (`compounds`/`lines`/`rows`/`items`/`data`) — thiếu key = 0 rows âm thầm.
- Đừng viết claim pháp lý vào template trước khi data về: subagent REE lật ngược giả định "chưa được EU công nhận" (EU 2020/1370 đã phê duyệt Lancer; TQ phê duyệt RECC).
