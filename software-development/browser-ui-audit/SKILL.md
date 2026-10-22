---
name: browser-ui-audit
description: "Audit web UI: auth-guard fix, detector false positives."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [audit, browser, ui, camofox, auth-guard, qa, detector]
    related_skills: [impeccable, dogfood, html-unslop]
---

# Browser UI Audit — Pitfalls & Workarounds

Kỹ thuật audit giao diện web bằng browser toolset (Camofox) khi KHÔNG mở được app thật
(không có token/login). Bổ trợ cho `impeccable` (design language + ui-audit.js) và
`dogfood` (QA bug-hunting) — chỗ này chỉ giữ pitfalls kỹ thuật chung, không lặp lại design rules.

## When to Use

- Cần audit/chụp UI của trang yêu cầu login, passcode, hoặc có JS guard token
- Detector AI-tells (`impeccable` ui-audit.js) trả cảnh báo nghi ngờ false positive
- `browser_navigate` "thành công" nhưng snapshot rỗng / `browser_console` toàn 500

## Pitfall 1: Auth-guard redirect phá browser toolset

**Triệu chứng** (trang có guard như `if (!token) { window.location.href = '/'; }` mở không qua app thật):
- `browser_snapshot`: timeout "waiting for navigation to finish", snapshot rỗng (element_count 0)
- `browser_console`: 500 "Execution context was destroyed, most likely because of a navigation"
- Camofox `/health` vẫn `{"ok":true}` — KHÔNG phải browser chết, đừng restart vô ích
- Start Camofox mà báo "port in use" (9377) → đã có instance chạy, dùng luôn, đừng start thêm

**Recipe (đã chạy OK trên TFO 8100):**
1. Tìm guard: `grep -nE "window.location.href|localStorage.*token" index.html`
2. Copy + strip guard (sed theo chuỗi THẬT của từng file; guard có thể nhiều dòng):
   ```bash
   sed 's/if (!token) { window.location.href = .\/.; return false; }/if (!token) { return false; }/' index.html > audit.html
   ```
3. Serve bản copy: `python -m http.server 8130 --bind 127.0.0.1` (background=true)
4. `browser_navigate` tới bản copy → chạy detector/audit qua `browser_console`
5. Dọn: xoá file copy + kill server + camofox (nếu tự khởi động)

**Lưu ý:**
- API 404 trên bản static là bình thường — chỉ audit được chrome/design, data không load
- Expression multi-line trong `browser_console` hoạt động tốt sau khi navigation ổn định;
  lỗi 500 trước đó là do navigation loop, không phải do multi-line

## Pitfall 2: Detector "hard-offset-shadow" false positive

Regex `(\d+)px (\d+)px 0px` khớp 3 token cuối của shadow 4 giá trị:
`box-shadow: 0 8px 24px 0px` → "8px 24px 0px" → max(8,24)=24 > 2 → flag nhầm.

**Verify trước khi sửa:** đọc box-shadow thật của element bị flag:
```js
getComputedStyle(el).boxShadow
```
- blur > 0 → depth hợp lệ, bỏ qua (đây là elevation thật)
- `Npx Mpx 0` (zero blur) → hard offset shadow thật, mới sửa

## Verification

- Sau fix, chạy lại detector 1 lượt trên bản copy — kỳ vọng tells giảm đúng nhóm đã sửa
- Test app thật sau khi sửa file gốc: console không lỗi JS, flow chính còn hoạt động
- Bounded: tối đa 2 lượt fix rồi dừng

## Pitfall 3: Đo layout hẹp bằng SỐ (trang tự vẽ lại bằng JS)

Trang sơ đồ/dashboard tự dựng SVG theo `clientWidth` lúc render. Kiểm bằng mắt là vô nghĩa; bốn phép đo dưới đây bắt được đúng những lỗi hay gặp (ca thật 19/10/2026, trang đồ thị đường đi 8 chặng).

**1. Tràn ngang phải đo bằng hiệu số của document, không phải bằng "con tràn khung".**

```js
document.documentElement.scrollWidth - document.documentElement.clientWidth   // phải = 0
```

Phép kiểm quét từng phần tử con xem có vượt khung cha không **bỏ sót** lỗi tràn do **hai khối cạnh nhau** (cột nhãn 150px + khối SVG min-width 300px trong khung 360px → tràn 130px, mà không phần tử nào vượt khỏi khối chứa nó). Luôn đo hiệu số này ở 360px.

**2. KHÔNG mô phỏng khung hẹp bằng `style.width` lên phần tử flex.**

`el.style.width='344px'` không đổi bề rộng thật khi `el` là con flex (flex-grow ghi đè) → số đo vẫn theo khung desktop → kết luận "tràn"/"không tràn" đều sai. Dùng iframe cùng origin 360px rồi đo **bên trong** iframe:

```js
const f=document.createElement('iframe');
f.style.cssText='position:fixed;left:-9999px;top:0;width:360px;height:1700px;border:0';
f.src=location.href; document.body.appendChild(f);
// lượt sau:
const d=f.contentDocument, w=f.contentWindow;
// đếm chữ < 12px, đo tràn ngang, đếm phần tử trong SVG — tất cả trong d.
```

**3. Sàn cỡ chữ: quét cả class nhỏ bị bỏ quên.** SVG giữ được ≥12px mà khối chú thích ngoài SVG (`11,5px`) vẫn dưới sàn. Quét `p,li,span,b,em,div,.chip,.sub,text`, lấy `getComputedStyle(el).fontSize` (không dùng `el.children` để bỏ qua phần tử chứa), ngưỡng **< 12px = lỗi**.

**4. Sơ đồ tự vẽ: đọc bề rộng SAU khi áp breakpoint.** Nếu tính `CAP`/layout từ `clientWidth` lấy **trước** khi thêm class `narrow` thì lượt render đầu sai, người dùng chỉ thấy bản sai. Đo lại số phần tử + bề rộng SVG **sau** khi render xong.

**Cách sửa lỗi tràn cột phụ (đã dùng được):** một ngưỡng bề rộng → `body.classList.add('narrow')`, CSS ẩn cột nhãn, và **vẽ nhãn vào trong SVG như dòng tiêu đề từng hàng** (dịch phần tử xuống 1 dòng, cộng chiều cao hàng). Kèm chặn số phần tử mỗi hàng khi hẹp (`CAP = boxW < 520 ? 10 : 60`) và ghi rõ `+N nữa` — không chặn thì hàng 46 phần tử ở 360px thành 46 dòng, cao hơn 2.000px.

**5. Đo cả bản ĐÃ publish, không chỉ bản local.** Sau khi upload, nạp lại URL thật rồi lặp lại phép đo — bước xử lý HTML trước publish có thể sửa `script`/`style`. Chênh số giữa local và live = dừng lại kiểm bước đó trước khi gửi link.

## Relation

- `impeccable` — design language, ui-audit.js detector, DESIGN.md tokens (user-owned)
- `dogfood` — QA bug-hunting toàn diện (bundled)
- Nếu cần recipe chi tiết auth-guard cho 1 app cụ thể → ghi vào state file của project đó
