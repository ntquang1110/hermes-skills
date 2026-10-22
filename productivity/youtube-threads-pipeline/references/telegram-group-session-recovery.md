# Telegram Group Session Recovery

Khi một session trong Telegram group bị treo vì `clarify` tool đang chờ response (user không trả lời câu hỏi), agent có thể:

1. Phân tích session bị stuck để lấy transcript/content đã fetch
2. Xử lý nội dung độc lập (viết draft, verify)
3. Gửi kết quả trực tiếp vào group qua Telegram Bot API
4. Đánh dấu đã xử lý trong youtube-processed.json

## Telegram Bot API Direct Send

Không dùng `curl -d` vì UTF-8 bị lỗi ("Bad Request: text must be encoded in UTF-8"). Dùng Python `urllib.request` với JSON payload:

```python
import json, urllib.request

# Lấy token từ .env
with open('.env', encoding='utf-8') as f:
    tok = None
    for line in f:
        if line.startswith('TELEGRAM_BOT_TOKEN='):
            tok = line.strip().split('=', 1)[1].strip()
            break

chat_id = "-5533508241"  # YouTube group
msg = "Nội dung cần gửi..."

data = json.dumps({"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}).encode('utf-8')
req = urllib.request.Request(
    f"https://api.telegram.org/bot{tok}/sendMessage",
    data=data,
    headers={"Content-Type": "application/json"},
)
resp = urllib.request.urlopen(req, timeout=30)
res = json.loads(resp.read())
print("OK" if res.get("ok") else res.get("description", "?"))
```

## Flow khi session bị treo trên clarify

1. **Đọc session bị treo**: `session_search(session_id="...")` để lấy transcript và context
2. **Xác định content type**: tâm lý, macro, podcast, book review
3. **Viết draft theo style của group** (thesis-driven, quote nguyên văn, 2-layer depth)
4. **Verify**: đếm chars (target ~2600-3200), diacritics (>300), 0 em dash/emoji, no AI vocab
5. **Gửi vào group** qua Telegram Bot API với "Anh duyệt?"
6. **Đánh dấu processed**: thêm video ID vào `youtube-processed.json`

## Cấu trúc message gửi group

```
✅ Link xử lý xong: https://youtu.be/VIDEO_ID

Draft bài Threads về [topic]:

[draft content]

Anh duyệt? Nếu ok em add queue đăng hôm sau.
```

## Pitfalls

- **curl -d lỗi UTF-8**: Không dùng `curl -d` cho text có dấu tiếng Việt. Luôn dùng Python urllib với JSON encode UTF-8.
- **Không double-send**: Sau khi gửi, đánh dấu processed ngay để tránh xử lý lại.
- **Kiểm tra bot token**: TELEGRAM_BOT_TOKEN trong .env, chat_id là số âm cho group (-5533508241 cho YouTube group).
- **Session cũ vẫn pending**: Không cần force-close session cũ. Session sẽ timeout tự nhiên. Agent làm việc trong session mới.
