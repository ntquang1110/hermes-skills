# Standup 08/09/2026 — bài học vận hành

## 1. Agent đồng loạt báo SAI số liệu = briefing.md context cũ (đừng đổ lỗi agent)
- Triệu chứng: 5/5 agents (CTO, Dev1, QA, CMO, Content) đều báo "7 task planning no-dc chờ Quang chốt, #40≈#35 chưa đóng" trong khi guard nói planning=4 (#43-46), #35-42 ĐÃ completed (Quang đóng 03/09).
- Gốc rễ: KHÔNG phải agent bịa. `base_agent.think()` nạp `briefing.md` vào mọi prompt → block standup cũ (mốc 04/09, "7 task...") còn nằm nguyên ở đầu file → mọi agent echo cùng con số cũ.
- Fix: mỗi standup khi flush, GHI SỐ LIỆU THẬT vào block head briefing.md (timestamp + STALE/NO_DC + completed/paused/planning/in_progress + các task đáng chú ý), không chỉ sửa timestamp. Cập nhật cả dòng "Standup (last)" và "Last Updated" cuối file.
- Pattern nhận diện: nhiều agent báo CÙNG một con số sai → nghi briefing trước khi nghi từng agent.

## 2. Retire dead-letter wake (Claw tắt) — sửa thẳng JSON, KHÔNG dùng ack()
- Wake gửi cho Claw khi Claw tắt kẹt `status=sent` vĩnh viễn → ops_guard WAKE>0 mỗi standup (đã 7 tin: 4 relic 22/08 + 3 meeting transcript 24/08/04/09/07/09).
- KHÔNG gọi `ack()` (gửi tin "✅ ACK" ngược cho người gửi = Hermes → nhiễu + spam) — sửa TRỰC TIẾP `shared/to_claw.json`:
  - Cấu trúc file: `{"messages": [...], "next_id": N}` (dict, KHÔNG phải list — từng dính AttributeError khi iterate list).
  - Với từng tin id: `status = "read"`, `read_at = <now>`, `note = "Dead letter - Claw tat tu 24/08, Hermes giu Front. Retired trong standup <ngày>."`
  - Sau đó commit + push (inbox files PHẢI tracked).
  - Verify: `python hub/ops_guard.py --json` → `wake` về 0.
- TODO nếu chưa làm: kiểm tra các script khác còn ghi wake cho Claw (xem mục 3).

## 3. `_send_transcript_to_claw` còn gửi wake Claw dù Claw tắt — đã gate
- `app/main.py` tới 07/09 vẫn gửi "🎙️ Meeting X — transcript sẵn sàng" qua inbox (mỗi meeting mới = 1 wake chết). Commit b348840 đã bỏ `send()` — chỉ lưu transcript local (meeting đã được lưu + push TG bởi tg_push). **Hiệu lực sau restart server 8100.**
- Kiểm tra khi thấy WAKE>0 với subject meeting gần đây: sinh từ main.py pipeline cũ, chưa restart.

## 4. Context-scan dedup hash KHÔNG bắt proposal tái sinh sau khi đóng
- 03/09 Quang đóng lô draft #35-42 (trùng nội dung trong batch). 04/09 context-scan tạo LẠI 4 proposal y hệt thành #43-46 (#43≈#40/#35, #44≈#39/#36, #45≈#42, #46≈#41).
- Vì sao dedup trượt: `scan_key = sha256(noi_dung)` lệch mỗi lần scan (brief nguồn đổi theo ngày/phrasing LLM), và dedup chỉ so task còn planning/review (không so completed).
- Xử lý đúng khi gặp: planning drafts mới mà title gần giống context-scan task COMPLETED gần đây → chia cặp trùng, báo Quang chốt đóng lại (assignee là NGƯỜI Anh Quân/Quang, không phải agent → wake agent vô ích). Đừng tự ý đóng (đó là quyết định sản phẩm của Quang).
- Cải tiến pipeline nếu được duyệt: so title similarity (difflib ratio > ~0.7) với completed context-scan tasks khi tạo draft.

## Số liệu thật 08/09 (ghi vào briefing cho standup sau)
- guard STALE=5 (#43-46 planning 3.8d + #8 in_progress 2.0d), NO_DC=4 (#43-46), WAKE=0 sau cleanup.
- tasks.json: 32 completed, 9 paused, 4 planning, 1 in_progress. #35-42 completed — KHÔNG còn "7 task chờ chốt".