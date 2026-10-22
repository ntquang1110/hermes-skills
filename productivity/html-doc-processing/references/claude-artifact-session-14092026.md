# Session PMF ngành heo — 14/09/2026

## Context
Quang gửi "Sổ tay tìm PMF ngành heo 14092026.html" (266KB) yêu cầu sửa text + publish dùng unslop.

## Phát hiện chính: file là frame shell
File lưu từ Claude Artifact (comment `saved from url=(0068)https://claude.ai/code/artifact/f71b6946...`).

Diagnosis đã chạy:
1. `read_file` → chỉ 5 dòng, body 10KB toàn chrome (header controls, avatar "Q")
2. Tìm `<h1`, `<h2`, `<section` → 0 hit. Tìm "PMF" → 5 hit nhưng đều là title/meta/iframe ref
3. `<main>` ở 262796 → `<iframe src="./Sổ tay tìm PMF ngành heo 14092026_files/_t.html">`
4. Grep từ khoá tiếng Việt (thịt, lợn, giá, khách hàng, sản phẩm, nuôi...) → **0 hit** = xác nhận không có content
5. Folder `_files/` không được upload kèm → không thể truy cập `_t.html`

Kết luận báo user: file thiếu nội dung thật, yêu cầu gửi cả folder hoặc paste content.

## Bản content thật
Quang gửi `pmf-chan-nuoi-heo.html` (62KB) — standalone HTML sạch (Newsreader + IBM Plex, không AI-signature palette). Yêu cầu: bỏ vị trí "Chuyên gia thiết kế và phân tích thử nghiệm".

## Edit-consistency checklist đã áp dụng
1. Role block: `raw.rfind('<article', 0, idx)` → `raw.find('</article>', idx)` — cắt chính xác 1 block
2. Bảng F: tìm `Chuyên gia thiết kế thử nghiệm (bán thời gian)` → xóa cả `<tr>...</tr>`
3. Đánh số lại: "Vị trí thứ 6"→5, "Vị trí thứ 5"→4 (replace theo thứ tự ngược để tránh đụng nhau)
4. Tổng chi phí: 150–175 tr → 135–150 tr (100 hiện tại + 35–50 Trưởng KT; bỏ 15–25 chuyên gia)
5. Verify: `raw.count('Chuyên gia thiết kế') == 0`, role articles = 5, tag balance OK

## Unslop kết quả
`unslop-html.py --check` → "AI design tells (1): ai-auto-grid (2x)", "Fixed: 0 tells removed".
- **0 text tells** = content đã sạch tự nhiên, không phải lỗi script
- ai-auto-grid (repeat(auto-fit, minmax)) được detect nhưng script không tự fix → chấp nhận

## Publish + verify
- `content-upload.py --file pmf_unslop.html --title "Sổ tay tìm PMF ngành heo"` → https://preview.thefirstonly.com/vvgksxki7j6y
- Browser verify: `removed_string_left: false`, 5 roles đúng tên + rank, totalRow = "135–150 tr/tháng", js_errors = 0

## Windows path gotchas (đã vấp)
- `search_files` trên path filename tiếng Việt → IO error "cannot find the path" → copy sang `~/pmf_work/` ASCII
- `unslop-html.py --file /tmp/pmf.html` → FileNotFoundError (MSYS /tmp ≠ Windows Python path) → dùng path Windows thật
- Chạy python script skill từ bash: `python "C:/Users/.../scripts/unslop-html.py"` forward slashes mới chạy
