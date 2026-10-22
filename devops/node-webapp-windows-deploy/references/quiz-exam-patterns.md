# Quiz/Exam App Patterns — tái sử dụng cho hệ thi trắc nghiệm

Các pattern đã verify trong app dithi (node thuần + JSON store), tái dùng được cho bất kỳ hệ thi trắc nghiệm nào trên Windows/self-hosted.

## 1. Gen đề không trùng

- Ngân hàng câu hỏi theo teacher/nguồn với tỉ lệ cố định (vd 20/15/5 trên 40 câu)
- Với mỗi teacher: shuffle pool → lấy N câu → tráo thứ tự 4 đáp án (giữ đáp án đúng: `order.indexOf(correctIdx)`) → tráo thứ tự câu
- Đảm bảo các đề không trùng nhau: signature = sorted qids joined, regenerate nếu trùng (loop max ~200 attempts)
- Số đề gen = số thí sinh tối đa; mỗi thí sinh assign đề chưa dùng (Set of used exam_ids) → không ai trùng đề

## 2. Server enforce deadline (KHÔNG tin client countdown)

Client countdown chỉ là UX. Server giữ `started_at`, deadline = started_at + 50min.
- Mọi request (save/submit/overview) gọi `enforceDeadline(contestant)`: nếu quá hạn mà chưa nộp → tự đánh dấu submitted, `submitted_at = deadline`, `auto = true`, chấm với answers đã save
- Admin overview sweep: loop tất cả contestants, enforceDeadline từng người → hết giờ tự hiện "Đã nộp (auto)" mà không cần thí sinh bấm gì
- Client khi countdown về 0 gọi `/api/submit` luôn (dự phòng)

## 3. Resume + lock STT

- Mỗi STT/contestant có `token` (crypto random). Client giữ trong localStorage → refresh/mất mạng resume: gọi enter với token cũ, server trả exam + answers + remaining_ms
- Lock: STT đang in_progress → enter với token khác trả 409 "đang được sử dụng"; submitted → 409 "đã nộp"; assigned quá 30 phút chưa start → thả STT cho người khác
- Autosave nháp mỗi 15s lên server → hết giờ/mất mạng không mất bài

## 4. Trang thí sinh: 4 screens trong 1 SPA

enter (nhập STT + hiện tên) → ready ("Sẵn sàng chưa?" + hiện tên học viên để xác nhận) → exam (countdown sticky + progress bar + qnav grid + options) → done ("Chúc mừng", KHÔNG hiện điểm).

Pitfall đã sửa: hàm render câu hỏi ban đầu dùng `app.innerHTML = ...` ghi đè toàn trang → phá timer/nav/submit. **Chỉ update `#qcard` innerHTML, giữ layout timer + qnav nguyên vẹn; gán lại event listeners sau mỗi render.**

## 5. Import Excel câu hỏi (lặp lại nhiều lần với file mới)

- Đọc bằng python/openpyxl, `data_only=True`
- So sánh bản cũ/mới theo FULL TEXT câu hỏi (không theo STT — STT bị xáo giữa bản)
- Báo removed/added/changed-answer/changed-options; cấu trúc: teacher, lesson, question, A-D, answer, explain
- Pitfall: keyword match nhầm (2 câu khác nhau cùng chứa "mô hình SBI") → so sánh full text, verify bằng cách đọc lại file nguồn mới trước khi kết luận "còn sót"
- Import xong phải kill server thật + xóa state.json + restart (đề gen lại từ ngân hàng mới)

## 6. Admin + export Excel

- Auth đơn giản: POST login → token → lưu mảng admin_tokens → Bearer header. Đủ cho nội bộ, không cần session cookie
- Overview poll 5s (setInterval) — đủ real-time cho kỳ thi, không cần WebSocket
- Export: exceljs, 2 sheet — Tổng hợp (per thí sinh: STT/tên/status/đề/giờ/điểm/auto) + Chi tiết đáp án (per câu: TS chọn vs đúng)
- KPI cards: total/done/active/assigned

## 7. Danh sách học viên

- Import Excel: STT + tên + CCCD + phone + email → students.json keyed by STT
- Bỏ các dòng chú thích màu trong file (vd "màu xanh = bảo lưu", "màu đỏ = bỏ thi" — không phải học viên)
- STT_MAX lấy từ max(STT trong danh sách), không hardcode 30
- Thí sinh thấy tên mình trên trang đệm (xác nhận đúng người, không cần passcode/CCCD khi vào — CCCD chỉ để hồ sơ admin + export)

## 8. Chấm điểm

- Mỗi câu 1 điểm, score = count(answers[i] === correct)
- Chấm server-side lúc submit, lưu vào state; thí sinh KHÔNG thấy điểm (chỉ "Chúc mừng"), admin + export thấy
