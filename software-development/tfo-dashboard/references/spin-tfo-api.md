# SPIN TFO 16/08 — API surface (sub #29, #31, #32)

5 endpoint mới thêm vào `app/main.py` (commit `12ece36`), tất cả require `?token=` hoặc Form `token` qua `_resolve_user(token)` → 401 nếu sai.

## /api/inbox (GET) — sub #29 Inbox 2 chiều
Đọc cả 2 file inbox qua `shared/inbox`:
- `inbox.FILES["Hermes"]` = shared/to_hermes.json (Claw→Hermes)
- `inbox.FILES["OpenClaw"]` = shared/to_claw.json (Hermes→Claw)

Trả về:
```json
{
  "messages": [ {"id":1,"from":"Hermes","to":"OpenClaw","subject":"...","body":"...","type":"direct","status":"sent|read","sent_at":"...","read_at":null}, ...60 mới nhất ],
  "unread": 3,               // đếm status=="sent"
  "unread_messages": [ ...30 ]
}
```
Sắp xếp `sent_at` DESC. UI: card "📥 Inbox Hermes ↔ Claw" trên dashboard + badge đỏ "N mới".

## /api/inbox/{msg_id}/read (POST) — đánh dấu đọc từng tin
Form field: `token`. Tìm tin trong cả 2 file, đổi `status: sent→read` + set `read_at`, ghi đè file gốc. Trả `{"ok":true}` hoặc 404.
**Lưu ý:** đọc/ghi thẳng file JSON của inbox (không qua `inbox.mark_read()` vì hàm đó nhận me-name khác) — nhưng phải giữ đúng schema (indent=2, ensure_ascii=False) để không phá file sync git.

## /api/inbox/read-all (POST) — đánh dấu hết tin Claw gửi
Chỉ xử lý file `FILES["Hermes"]` (to_hermes.json — tin từ Claw). Trả `{"ok":true,"read":N}`.

## /api/kpi (GET) — sub #31 Dashboard điều hành C-level
Tổng hợp từ nhiều store thật:
- `_user_read(email, "tasks.json")` → user kanban tasks (done = `t.get("done")`)
- `_ai_store("tasks.json")` → AI agent tasks (done = `phase=="completed"` hoặc `status=="completed"`)
- `_user_read(email, "meetings.json")` → đếm meetings
- `_ai_store("cost.json")` → total_spent, month_budget, len(calls)
- `_ai_store("activity.json")` → `activity` list, đếm item có time/created_at trong 7 ngày qua helper `_recent()`

Trả về:
```json
{
  "tasks": {"total_user":32,"done_user":6,"total_ai":34,"done_ai":13},
  "meetings": 2,
  "cost": {"total_spent":0.3263,"month_budget":100.0,"calls":357},
  "activity_7d": 49,
  "updated_at": "2026-08-16 19:26"
}
```
UI: 4 stat-card thứ 2 (Task đã đóng / Meeting meTelligent / Chi phí AI / Hoạt động 7 ngày). `kpiMetMeetings` fill từ endpoint meTelligent, không từ /api/kpi.

## /api/metelligent/meetings (GET) — sub #32 tích hợp meTelligent
Đọc TRỰC TIẾP SQLite (không qua API meTelligent):
`D:/Hermes Proj/meTelligent/server/metelligent/data/meetings.db`

Query:
```sql
SELECT id, title, date, tags, status, corrected_text, full_transcript, created_at, updated_at
FROM meetings ORDER BY COALESCE(updated_at, created_at) DESC LIMIT 40
```
Bảng `meetings` schema: id, title, date, tags, status ('done'|'recording'), full_transcript, corrected_text, created_at, updated_at. (~30 rows thực tế.)
Mapping: `title or "Không có tiêu đề"`, `date[:10]`, `transcript_preview = (corrected_text or full_transcript)[:160]`.
UI: card "🎙️ Meeting từ app meTelligent", nhóm ĐANG GHI ÂM (status=recording) / ĐÃ XONG (status=done, slice 8 + "+N nữa"), click mở `https://metelligent.theliems.com/dictation`.

## /guide (GET public, sub #34)
Route HTML public — `app/static/guide.html`, `response_class=HTMLResponse`, KHÔNG cần token. Hướng dẫn 3 bước cho người ngoài: ghi âm → tự tóm tắt/sinh task → chat voice theo dõi.

## Ghi chú xác minh
- Curl verify trước khi viết JS (pattern chuẩn trong SKILL.md).
- Browser test: login quang@kiemsaphia.com / <PASSCODE> → snapshot → `browser_console` eval DOM state; node check_inline_js.js trước restart.
- `store/tasks.json` gitignored → đóng task #28–#34 chỉ đổi data trên disk, không tạo commit.
