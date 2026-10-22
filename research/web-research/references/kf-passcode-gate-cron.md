# KF passcode gate — cookie bắt buộc cho mọi API call (từ Aug 2026)

Knowledge Flow (localhost:3003) nằm sau passcode gate `tfo_auth` (passcode `<PASSCODE>`, xem skill `web-passcode-gate`). Gate chặn cả `/api/*` — không chỉ trang web.

## Triệu chứng

Mọi cron/script cũ gọi API KF không kèm cookie sẽ nhận:
```
307 → /passcode?next=%2Fapi%2F...
```
và code parse JSON fail với `JSONDecodeError: Expecting value: line 1 column 1 (char 0)` — không có lỗi rõ ràng, trông như API chết.

## Fix: thêm cookie vào MỌI request

Hash cookie (sha256 của passcode `<PASSCODE>`):
```
tfo_auth=1d1e977a218bfa01fe61106c360c8acf667047e35f17fdb0f1a8484e06cfdb55
```

**curl** (queue check, cards check, POST):
```bash
curl -s -H "Cookie: tfo_auth=1d1e977a218bfa01fe61106c360c8acf667047e35f17fdb0f1a8484e06cfdb55" \
  "http://localhost:3003/api/research-queue"
```

**Python urllib** (Pattern D POST):
```python
headers = {
    "Authorization": "Bearer hermes-knowledge-secret",
    "Content-Type": "application/json",
    "Cookie": "tfo_auth=1d1e977a218bfa01fe61106c360c8acf667047e35f17fdb0f1a8484e06cfdb55"
}
```

## Verified (2026-08-03, cron rotation run)

- `/api/research-queue` không cookie → 307; có cookie → JSON đầy đủ
- `/api/cards` không cookie → 307; có cookie → 227 cards
- POST `/api/knowledge` với cookie + Bearer → 201, card ID trả về
- Bearer `hermes-knowledge-secret` ĐƠN LẺ không đủ — cookie là yếu tố quyết định

## Pitfall phụ: `topic_slug` không map vào topic

POST với `topic_slug: "sinh-hoc"` trả 201 nhưng card lưu có `topic_id: None` / `topics: None`. API chấp nhận field nhưng không tạo quan hệ topic. Không chặn việc ingest — verify card bằng `id` trong `/api/cards`, đừng verify bằng topic.
