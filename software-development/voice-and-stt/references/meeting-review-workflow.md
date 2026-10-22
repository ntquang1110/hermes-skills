# Meeting Transcript Review Workflow — Transcribe → Duyệt → Task list → Xử lý

> Derived from user instructions (2026-08-05, meeting summary pipeline):
> - "đầu tiên em trả cho anh hết toàn bộ transcript anh duyệt xem đã chuẩn chưa, trước khi đến bước xử lý, em lên task để anh duyệt từng phần 1 đi"
> - "stop đi, nêu toàn bộ vấn đề đang gặp đi, chốt phương pháp trước khi thực hiện"
> - "em tự thực hiện 3 phương án, tạo html cho kết quả của 3 phương án đó, mỗi phương án 1 tab và có 1 tab cuối so sánh 3 phương án, đề xuất của em"

## Bối cảnh

Khi xử lý meeting (transcribe → summarize → task), user KHÔNG muốn agent tự ý chạy thẳng pipeline rồi báo kết quả. Muốn **duyệt từng lớp** trước khi chuyển sang bước tiếp theo. Đây là quy trình critique-first ở cấp độ vận hành, không chỉ ở cấp độ code.

## Quy trình 5 lớp (đã được user xác nhận)

```
Lớp 1: 🎙️ Transcribe xong → TRÌNH TOÀN BỘ transcript cho user duyệt
             │
Lớp 2: 📝 User xác nhận / sửa từng điểm nghi vấn
             │
Lớp 3: 📋 Lên task list (đánh số, có thứ tự phụ thuộc) → user duyệt từng phần
             │
Lớp 4: 🔧 Sau khi task list được duyệt → mới bắt đầu xử lý (summarize, tạo task...)
             │
Lớp 5: 📊 Khi có nhiều phương án → chạy TẤT CẢ, so sánh trong 1 HTML, kèm đề xuất
```

## Chi tiết từng lớp

### Lớp 1 — Trình toàn bộ transcript

- Gửi **toàn bộ** text transcript vào chat, không tóm tắt, không cắt.
- Kèm danh sách đánh số các chỗ agent nghi Whisper sai (tên riêng, số liệu, thuật ngữ).
- Với mỗi điểm nghi vấn: ghi bản Whisper nghe + giả thuyết đúng, để user xác nhận nhanh.
  VD: `"sạng mới" → có thể là "trại mới"` / `"900 muôn đợt con" → số con?`
- User trả lời theo kiểu đánh số: `"1-4 ok, 6 OKR, 7 chuẩn, 8 chuẩn, 9 900 con, 10 chuẩn"`.

### Lớp 2 — Xử lý điểm nghi vấn

- Nếu user chỉ nói "chuẩn" → giữ nguyên, đừng tự sửa.
- Nếu user sửa → replace chính xác chuỗi trong file transcript, lưu bản mới (v7 → v8_final), verify từng điểm bằng script đếm occurrence.
- Nếu user muốn check thêm 1 điểm → **trích đúng đoạn hội thoại** kèm bối cảnh trước/sau, KHÔNG chỉ đưa 1 câu lẻ. Bối cảnh giúp user đoán đúng (VD: "bám OCR" vs "bám OKR" — chỉ rõ ai đang nói, nói về mục tiêu gì).

### Lớp 3 — Task list để duyệt

- Đánh số task (1..N), mỗi task 1 dòng, ghi rõ trạng thái (Xong / Chờ duyệt).
- Nêu **thứ tự phụ thuộc** (2 → 3 → 4+5 → 6 → 7+8).
- Nêu **điểm cần user quyết** riêng (VD: task tự sinh có tự tạo vào tasks.json luôn không?).
- Không bắt đầu bước nào cho tới khi user duyệt task list (hoặc nói "em tự thực hiện").

### Lớp 4 — Chốt phương pháp trước khi chạy

- Khi đang kẹt nhiều vấn đề chồng nhau → **DỪNG**, trình bày toàn bộ vấn đề đang gặp (bảng ngắn), rồi đưa phương án kèm độ tin cậy, chờ user chốt 1 cái.
- User từng chọn: "em tự thực hiện 3 phương án" — tức là khi có ≥3 cách, user muốn agent chạy hết rồi so sánh, không chọn hộ.

### Lớp 5 — HTML so sánh nhiều phương án

Khi user yêu cầu so sánh phương án, format HTML chuẩn:
- **Mỗi phương án 1 tab** (tab-btn + tab-panel, `data-tab` attribute, `switchTab()` JS).
- **Tab cuối cùng: so sánh** — bảng tiêu chí × 3 cột (Độ ổn định, Đúng cấu trúc, Đầy đủ chi tiết, Assignee+Deadline, Phụ thuộc provider, Chi phí) + khối "Đề xuất" có lý do chọn/loại từng PA.
- Publish qua content-publish → gửi 1 link duy nhất, kèm tóm tắt ngắn kết quả thực tế từng PA.

### Lớp 6 — Output HTML PHẢI theo đúng cấu trúc skill `meeting-transcriber` (user reject 2026-08-05)

User từng reject bản Meeting Notes vì không follow skill: *"anh k đồng ý bản này, follow skill của hermes đi"*.

Bản bị reject: layout phẳng tự thiết kế (Context → KPI → Issues → Risks → Actions → Decisions → Next Steps) + **KPI cards rỗng** vì LLM extract không ra số.
Bản được duyệt: đúng skill — **2 tab** (Tổng quan + Transcript), trong Tab Tổng quan **tách rõ 2 view**:
- **👑 Góc nhìn CEO**: Overall Context → KPI Cards (4 card, **số liệu THẬT từ transcript**, không để trống) → Vấn đề & Blockers (tag BLOCKER) → Rủi ro (tag RISK)
- **🤝 Góc nhìn Trợ lý**: Action Items (table) → Quyết định (viền vàng trái) → Next Steps (checklist)

Quy tắc:
- Đừng tự improvise layout khác skill — đọc lại skill `meeting-transcriber` (Bước 4 + Bước 5) trước khi build.
- KPI cards KHÔNG được trống: nếu LLM extract bỏ sót số liệu → **đối chiếu transcript thủ công**, trích số thật (VD: "5 công thức", "60 nái + 900 con", "20-30 con") vào card. Đây là điểm user check đầu tiên.
- Số liệu chỉ lấy từ transcript đã user duyệt (bản v8), không suy diễn.

## Pitfalls

- ❌ Chạy thẳng pipeline summarize khi transcript chưa được user duyệt → user bắt dừng lại.
- ❌ Tự sửa transcript theo phỏng đoán khi user chưa xác nhận → chỉ sửa những gì user xác nhận, phần còn lại giữ nguyên.
- ❌ Đưa điểm nghi vấn dạng câu lẻ không bối cảnh → user không đoán được; luôn trích đoạn + bối cảnh.
- ❌ Sau khi user duyệt transcript, quên lưu bản v8 riêng → mất vết thay đổi; luôn tạo file mới + script verify occurrence từng điểm.
- ❌ Báo cáo giữa chừng "đang làm" → user muốn kết quả cuối, ngắn gọn (xem user profile).
