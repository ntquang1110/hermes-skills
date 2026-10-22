# App thi dithi — hồ sơ vận hành

Hệ thống thi trắc nghiệm cho CTĐT Huấn luyện viên Cân bằng Kiềm hoá Cơ thể (K02).
Build 14/08/2026, deploy sau Cloudflare tunnel.

## Thông tin cốt lõi

| Item | Giá trị |
|------|---------|
| Thư mục | `D:/Hermes Proj/dithi/` |
| Port | 5100 |
| Link thí sinh | `https://dithi.thefirstonly.com` |
| Link admin | `https://dithi.thefirstonly.com/admin.html` |
| Admin password | `dithi2026` (sửa `ADMIN_PASSWORD` đầu server.js) |
| Start | `cd D:/Hermes Proj/dithi && node server.js` |
| Stack | Node thuần + exceljs (chỉ 1 npm dep) + JSON files |
| Tunnel | TQUANG-DELL `0ce9aa47-...`, `config_src: cloudflare` (sửa qua API, không YAML) |

## Data files (`data/`)

- `questions.json` — ngân hàng câu hỏi (hiện 120 câu: Cô Tâm 58 / Cô Minh 48 / Cô Dung 14). Import từ Excel bằng `import_questions.py` (đổi SRC path tới file mới rồi chạy).
- `students.json` — danh sách học viên STT 1-36 (tên, CCCD, phone, email). Import bằng `import_students.py`.
- `state.json` — runtime state: contestants (STT → token, exam_id, status, answers, score), admin_tokens, exams (36 đề gen sẵn). **File này chính là "đã thi chưa" — xóa là reset toàn bộ.**

## Reset đúng cách (đã học phải luôn làm vậy)

1. Tìm PID thật: `netstat -ano | grep ":5100" | grep LISTEN`
2. `powershell -Command "Stop-Process -Id <PID> -Force"` cho TỪNG PID (process(action='kill') KHÔNG giết node thật!)
3. Backup + xóa: `cp data/state.json data/state_backup_<ts>.json && rm data/state.json`
4. Verify port free → start lại → login admin + overview phải thấy `done:0 active:0 assigned:0`

Khi user nói "em reset thông tin các bài đã thi" → làm chính xác chuỗi trên.

## Import câu hỏi mới (lặp lại nhiều lần)

User hay gửi file `vkh_questions_all*.xlsx` mới. Quy trình:
1. Copy file vào thư mục dithi với tên có version (`_1408b.xlsx`...)
2. So sánh với bản cũ bằng python/openpyxl: đếm theo nội dung câu hỏi (không theo STT — STT xáo), liệt kê removed/added/changed-answer/changed-options
3. Sửa `SRC` trong `import_questions.py` → chạy → verify tổng câu + teacher counts
4. Kill server thật, xóa state.json, start lại (đề gen lại từ ngân hàng mới)

Pitfall so sánh: 2 câu khác nhau có thể chứa cùng keyword (vd cả 2 có "mô hình SBI" nhưng là câu khác nhau). So sánh theo full text câu hỏi, và khi check "câu đã xóa còn sót" phải xem CẢ file mới đã thực sự bỏ chưa — đừng kết luận lỗi khi chỉ là keyword match nhầm.

## Luồng thí sinh (đã test kỹ)

Nhập STT 1-36 → trang đệm hiện tên học viên ("Học viên STT 13 — Nghiêm Thái Hoa") → "Vào thi" → 40 câu, 50 phút countdown + progress bar → nộp có confirm (báo câu bỏ trống) → auto nộp hết giờ (server enforce) → "Chúc mừng hoàn thành" KHÔNG hiện điểm.

Đặc điểm thiết kế:
- Mỗi STT 1 lần; token localStorage (`dithi_token`) → refresh/mất mạng resume không mất bài
- STT đang thi chặn người khác (409); assigned quá 30 phút chưa vào thi thì thả STT
- 36 đề gen sẵn, mỗi đề 40 câu (Tâm 20/Minh 15/Dung 5), tráo A/B/C/D + thứ tự câu, không trùng (verify bằng signature sorted qid)
- Server enforce deadline (không tin client countdown): started_at + 50min, quá hạn auto nộp với answers đã save
- Autosave nháp mỗi 15s lên server

## Admin

- Overview poll 5s: 36 STT, cột tên, trạng thái (Chưa có/Chưa vào thi/Đang thi/Đã nộp(+auto)), mã đề, giờ bắt đầu/nộp, điểm
- Detail modal: 40 câu + đáp án TS vs đáp án đúng + giải thích
- Export Excel 2 sheet: Tổng hợp (STT/tên/CCCD/SĐT/trạng thái/đề/giờ/điểm/auto) + Chi tiết đáp án (120 dòng/submitted TS)

## UI/theme

- Emerald (ngọc lục bảo): nền `#f2f7f5`, accent `#0f9d76`, text `#0f2e26`, radius ramp 8/12/16
- KHÔNG Google Fonts (gây render-blocking 30s ở VN — đã debug), dùng system-ui
- SVG icons 1 stroke, không emoji UI
- Tiêu đề trang thi: "CTĐT HUẤN LUYỆN VIÊN CÂN BẰNG KIỀM HOÁ CƠ THỂ KHOÁ K02" + "PHẦN THI TRẮC NGHIỆM" (user đổi K03 → K02 giữa session — kiểm tra khoá nào khi sửa)
- Câu hỏi KHÔNG hiện tên giáo viên cho thí sinh (user yêu cầu bỏ), admin detail vẫn hiện

## File phụ trợ

- `import_questions.py`, `import_students.py`, `add_ingress.py`, `add_dns.py` (CF token qua env `CF_TOKEN`, decode từ cert.pem)
- Excel nguồn: `vkh_questions_all*.xlsx`, `DANH_SACH_HOC_VIEN_K02.xlsx`
- Backups: `data/state_backup_*.json` — giữ khi user test, xóa khi chắc chắn không cần
