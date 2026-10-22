---
name: html-doc-processing
description: "Use when editing HTML docs from Claude artifacts."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [html, claude-artifact, editing, consistency, publish]
    related_skills: [publish, html-unslop]
---

# HTML Document Processing (html-doc-processing)

Xử lý tài liệu HTML gửi lên cho Quang: nhận diện bản chất file, lấy content thật, sửa nội dung nhất quán, rồi bàn giao cho unslop + publish.

## When to Use

- User gửi file HTML (thường lưu từ Claude Artifact) và yêu cầu "sửa text", "bỏ mục X", "publish lại"
- File có comment đầu: `<!-- saved from url=(0068)https://claude.ai/code/artifact/... -->`
- Cần sửa nội dung có số liệu chéo nhau (bảng, tổng, đánh số)

**Không dùng cho:** sinh HTML mới từ đầu (dùng `claude-design`/`sketch`), publish thuần (dùng `publish`), unslop thuần (dùng `html-unslop`).

## Bước 1 — Nhận diện file: shell hay content thật

Claude Artifact lưu về máy = 1 file HTML + 1 folder `<tên>_files/`. File chính CHỈ là frame shell.

**Dấu hiệu shell:**
```html
<!-- saved from url=(0068)https://claude.ai/code/artifact/f71b... -->
<iframe ... src="./<tên>_files/_t.html" id="frame-content">
```

**Test nhanh (quan trọng nhất):** grep từ khoá tiếng Việt của chủ đề trong file (`thịt`, `khách hàng`, `sản phẩm`...). **0 hit = không có content trong file.** Đừng unslop, đừng sửa, đừng upload shell.

**Xử lý:** báo user rõ: file thiếu nội dung thật, gửi cả folder `_files` (hoặc zip), hoặc paste nội dung từ Claude. Một lần nói đúng nguyên nhân + 2 lựa chọn, không làm việc trên shell.

## Bước 2 — Sửa nội dung nhất quán

Khi user yêu cầu "bỏ vị trí X" / "xóa mục Y", tài liệu thường có số liệu tham chiếu chéo. Rà TOÀN BỘ trước khi sửa:

| Chỗ cần rà | Ví dụ lỗi hay gặp |
|---|---|
| Đánh số mục/vị trí | Bỏ "Vị trí thứ 4" → các vị trí sau phải đánh số lại (5→4, 6→5) |
| Bảng tổng hợp | Bỏ 1 dòng trong bảng F → tổng "Chi phí/tháng" phải tính lại |
| Con số tổng | 150–175 tr → 135–150 tr (100 hiện tại + 35–50 mới, bỏ 15–25) |
| Tham chiếu chữ | "xem mục 02", "sau Cổng 4" — đảm bảo vẫn đúng sau khi xóa |

**Cách làm sạch (đã test):** dùng `execute_code` với Python string ops, không dùng regex sửa HTML nhiều tầng:
```python
idx = raw.find('<text cần bỏ>')
art_start = raw.rfind('<article', 0, idx)   # lùi về đầu block
art_end = raw.find('</article>', idx) + len('</article>')
raw = raw[:art_start] + raw[art_end:]
```
Sau khi sửa, verify bằng đếm: `len(re.findall(r'<article class="role', raw))`, check tag balance mỗi tag mở/đóng bằng nhau.

## Bước 3 — Verify trên browser trước khi báo xong

```js
// browser_console expression — kiểm tra mục đã bỏ + số liệu mới
(() => {
  const body = document.body.innerText;
  return JSON.stringify({
    removed_string_left: body.includes('<từ khoá mục đã bỏ>'),
    roles: [...document.querySelectorAll('.role h3')].map(h => h.textContent.trim()),
    totalRow: [...document.querySelectorAll('tr.total td')].map(td => td.textContent.trim())
  }, null, 2);
})()
```
Check: `removed_string_left: false`, số roles đúng, tổng mới hiện ra. Luôn `browser_console` (js_errors) sau đó.

## Pitfalls

### ❌ Markdown parser infinite loop khi build HTML từ .md
Đã xảy ra 10/2026: script `build_html.py` convert markdown → HTML bị treo vô hạn (timeout 30s). **Nguyên nhân gốc:** vòng paragraph check `t2.startswith(("-", "*"))` để break, nhưng list regex là `^[-*]\s+` (cần space). Một dòng chỉ có `-` hoặc `**` đơn lẻ **không match** list/heading/table → rơi vào paragraph branch → paragraph loop không tiêu thụ dòng đó → `i` không tăng → lặp vô hạn.

**Fix:** paragraph break condition phải match ĐÚNG các pattern mà các block khác xử lý:
```python
# SAI — thiếu \s+, dòng "-" hoặc "**" đơn lẻ không break
if t2.startswith(("-", "*")): break

# ĐÚNG — match chính xác regex của list/heading
if (not t2 or t2.startswith(("#", ">"))
        or re.match(r"^[-*]\s+", t2)
        or re.match(r"^\d+[.)]\s+", t2)
        or re.fullmatch(r"-{3,}", t2)): break
```

**Debug pattern:** chạy từng case trong thread có timeout, không đoán:
```python
import threading
res = [None]
def target():
    try: res[0] = md_to_html(test_input)
    except Exception as e: res[0] = str(e)
t = threading.Thread(target=target, daemon=True); t.start(); t.join(3)
print("HANG" if res[0] is None else "OK")
```

### ❌ html-unslop MẤT DẤU TIẾNG VIỆT
`content-upload.py` gọi `apply_unslop()` → `html-unslop` strip dấu tiếng Việt. HTML tiếng Việt publish qua script = mất dấu toàn bộ. **Bypass:** POST thẳng `preview.thefirstonly.com/api/store` với `{"content": html}`. Verify dấu trên server bằng `requests.get(preview_url)` + check chuỗi có dấu. Đã xảy ra 10/2026 (vụ Thanh Quang).

## Windows Path Pitfalls (từ session thực tế)

1. **Filename tiếng Việt** → `search_files`/rg lỗi IO ("cannot find the path"). Copy sang đường dẫn ASCII (vd `~/pmf_work/pmf.html`) trước khi grep/patch.
2. **`/tmp` của git-bash ≠ path Windows Python hiểu.** Python scripts nhận đường dẫn MSYS sẽ FileNotFoundError. Luôn truyền `C:/Users/...` thật.
3. **Đường dẫn script skill** từ bash: dùng `python "C:/Users/.../skills/.../scripts/unslop-html.py"` (forward slashes), không dùng `~` mở rộng kiểu MSYS khi gọi Python.

## Bàn giao unslop + publish

- Content đã sạch → `unslop-html.py --check` báo "0 tells" là chuyện bình thường, không phải lỗi script
- Upload: `content-upload.py --file <ascii-path>.html --title "..."` (xem skill `publish`)
- Verify preview URL bằng browser (publish skill checklist)

## When to Use — bổ sung

- Document HTML có 10-30 section riêng biệt, cần kiểm tra và loại bỏ section trùng lặp (expanded version của sub-section trong Executive Summary)
- Cần phân tích cấu trúc section, so sánh nội dung giữa các section, và cắt bỏ section dư thừa

## Reference

- `references/claude-artifact-session-14092026.md` — transcript chi tiết session PMF ngành heo: shell detection, edit-consistency, verification
- `references/html-deduplication-workflow.md` — phát hiện và xoá section trùng trong HTML multi-section: parsing, so sánh overlap, cắt HTML, verify
