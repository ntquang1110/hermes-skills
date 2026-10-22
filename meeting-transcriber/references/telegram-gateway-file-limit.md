# Telegram Gateway File Size Limit

## Hard Limit: 20MB

Khi user gửi file audio >20MB qua Telegram, gateway trả về:
```
Telegram audio file skipped: file size X MB exceeds the 20 MB limit.
```

## Vị trí code

File: `plugins/platforms/telegram/adapter.py` (trong Hermes source)

```python
# Document size cap. Telegram's public Bot API caps getFile at 20MB; a
# locally-hosted telegram-bot-api server (configured via extra.base_url)
# raises that to 2GB, so the presence of base_url is the opt-in.
self._max_doc_bytes: int = (
    2 * 1024 * 1024 * 1024  # 2GB
    if self.config.extra.get("base_url")
    else 20 * 1024 * 1024   # 20MB mặc định
)
```

## Cơ chế

- **Mặc định (20MB):** Dùng Telegram Bot API public → `getFile` giới hạn 20MB
- **Có `extra.base_url` (2GB):** Trỏ tới local `telegram-bot-api` server → Telegram's local server API cho phép download tới 2GB

## Các hướng xử lý

| Hướng | Mô tả | Độ phức tạp |
|-------|-------|-------------|
| **Path local** | User cung cấp đường dẫn file trên máy (vd `E:\recordings\meeting.mp3`) | Thấp — ưu tiên |
| **Nén < 20MB** | Dùng script `compress-audio.sh` → Opus mono → gửi lại | Trung bình |
| **Local telegram-bot-api** | Chạy server `telegram-bot-api` local, set `extra.base_url` trong config | Cao — cần setup |

## Cấu hình `extra.base_url`

Trong config gateway, section `platforms.telegram`:

```yaml
platforms:
  telegram:
    extra:
      base_url: "http://localhost:8081"  # telegram-bot-api local server
```

Khi có `base_url`, Hermes tự động:
1. Gửi request Bot API tới URL đó thay vì `api.telegram.org`
2. Tăng `_max_doc_bytes` lên 2GB

## Giới hạn kế tiếp sau gateway

Sau khi qua gateway, file vẫn phải qua được STT provider:
- **Groq Whisper:** ~25MB/file (compress nếu cần)
- **Local faster-whisper:** Không giới hạn file size, nhưng chậm hơn

## Debug

Nếu cần kiểm tra limit hiện tại:
```bash
grep -n "_max_doc_bytes\|MAX_FILE_SIZE\|20 \* 1024" path/to/adapter.py
```

Check Telegram config extra:
```python
self.config.extra.get("base_url")  # None = 20MB, truthy = 2GB
```
