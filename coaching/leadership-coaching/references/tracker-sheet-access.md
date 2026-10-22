# Tracker Sheet Access — Leadership Mastery (Quang)

Sheet dùng trong Leadership Mastery check-ins:
- **ID:** `<SHEET_ID>`
- **Title:** `⚡ Tracker — Kết quả, Công việc`
- **Owner:** `<EMAIL>` (đúng token active trong `google_token.json`)
- **Vị trí:** shared drive (parent `0AEM6ws2M3DgPUk9PVA`), `driveId: None` khi query
- **Tab thật:** `'Task'`, `'📋 Dự án'`, `'🎯 Mục tiêu & KQ'`
  - Cron prompt cũ ghi "3 tabs: Tuần, Dự án, Mục tiêu & KQ" → SAI. Không có tab `Tuần`.

## Symptom → meaning

| Symptom | Meaning |
|---|---|
| Sheets API trả `Unable to parse range: Tuần!A1:J15` | File ĐƯỢC tìm thấy, nhưng tab `Tuần` không tồn tại → thử tab thật |
| Sheets API trả `400 Request contains an invalid argument` cho mọi range (kể cả `A1:H20`) | File-level failure — API không đọc được (shared-drive quirk / scope) |
| Drive `files.get` by ID trả `404 File not found` | Nhưng `files.list` search (`name contains 'Tracker'`) vẫn trả file, `trashed: false`. Đây là quirk của shared drive — KHÔNG kết luận file mất |
| Anonymous `export?format=csv` trả HTML "Không tìm thấy trang" | Sheet không public — phải dùng authed API, không dùng curl không header |
| `gviz/tq` trả 400 | Cũng không hoạt động cho sheet này |

## Ghi chú token

- Chạy `setup.py --check` → `AUTHENTICATED` (token `C:\Users\NTQUANG_DELL\AppData\Local\hermes\google_token.json`).
- Refresh token cũ OK: `POST https://oauth2.googleapis.com/token` với `client_id/client_secret/refresh_token` → `access_token` (scope sheets + drive đủ).
- `drive/v3/about` xác nhận user = `<EMAIL>`.

## Cách đọc khi khả dụng

```python
# pattern đã chạy thành công trước đó (fix_sheet.py, Jul 31):
update(f"'{tab}'!A1:H4", [['...']])  # tab có quote đơn
# đọc: GET https://sheets.googleapis.com/v4/spreadsheets/{SID}/values/'Task'!A1:H10
```

## Fallback cho cron check-in

Nếu không đọc được sheet sau 2-3 lần thử, ĐỪNG block check-in:
1. `session_search(query="Leadership check-in ...", sort="newest")` → lấy nội dung check-in gần nhất + issue user nêu (vd "team không chủ động").
2. Soạn check-in liên tục với lịch sử đó + hỏi thẳng user (Feedback Friday ai? EQ Journal ngày nào? Sheet fill chưa?).
3. Không giả vờ đã đọc dữ liệu sheet — hỏi thật, không bịa số liệu.

## Trạng thái quan sát 2026-08-06

- `files.list` search: thấy, `trashed: false`, `modifiedTime 2026-07-31`.
- Direct get 404, Sheets API 400 cho mọi range, export 400. Sheet hiện đọc qua API KHÔNG ổn định.
- Kết luận thực dụng: đừng phụ thuộc sheet để soạn check-in; dùng lịch sử session + câu hỏi trực tiếp.
