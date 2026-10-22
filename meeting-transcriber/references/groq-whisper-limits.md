# Groq Whisper Limits — Meeting Transcription

## File size & rate limits

| Limit | Value | Ghi chú |
|-------|-------|---------|
| File upload | ~25MB | Chuẩn OpenAI-compatible |
| Rate limit | Audio seconds / hour + / day | Free tier |
| Requests/day | ~20,000 | Free tier |
| Minimum charge | 10s audio/request | Dưới 10s vẫn tính 10s |
| Models | `whisper-large-v3`, `whisper-large-v3-turbo` | |

## So sánh với các provider khác

| Provider | File limit | Cost | Quality VI |
|----------|-----------|------|------------|
| **Groq Whisper** | ~25MB (dựa trên thời lượng) | Free (20K req/ngày) | ⭐ Xuất sắc (large-v3) |
| Rook | 20MB cứng | - | Tốt |
| Local faster-whisper | Không giới hạn | Free (local) | Khá (medium+), chậm |

## Compression strategy — Multi-level fallback

Mục tiêu: đưa file xuống dưới **22MB** (Groq max ~25MB, để margin 3MB).

Pipeline nén 3 cấp:

```
Level 1 — Tính bitrate động
  bitrate = min(64, max(12, 18MB * 8 / duration_seconds))
  → Opus mono 16kHz, -application voip
  → Nếu file còn >22MB → Level 2

Level 2 — Nén ở bitrate tối thiểu (12kbps) 
  ffmpeg Opus mono 16kHz, -b:a 12k
  → 12kbps là ngưỡng dưới cho speech còn nghe rõ
  → 120 phút @12kbps = ~10.8MB
  → Nếu file còn >22MB → Level 3

Level 3 — Gửi lên Groq, nếu bị 413 thì nén lại + retry
  → Groq trả HTTP 413 (Payload Too Large)
  → Nén lại ở 12kbps, retry 1 lần
  → Nếu vẫn 413 → báo user file quá dài, cần chunk thủ công
```

| Loại file | Cách xử lý | Bitrate mục tiêu |
|-----------|-----------|-----------------|
| Audio (mp3, wav, ogg, m4a) | Convert sang Opus mono | 12-64kbps động |
| Video (mp4, mov, avi, mkv) | Extract audio → Opus mono | 12-64kbps động |
| File < 22MB + audio thuần | Bỏ qua, không nén | - |

**Dynamic ffmpeg timeout:** Không dùng timeout cứng. Tính `max(300, duration_seconds * 2)` để tránh ffmpeg bị kill giữa chừng với file dài.

**Tại sao Opus?**
- 24kbps cho speech gần như lossless quality (Level 1)
- 12kbps vẫn nghe rõ speech (Level 2, fallback cho file siêu dài)
- 60 phút @24kbps = ~10.8MB, thoải mái dưới 22MB
- ffmpeg built-in, không cần thư viện ngoài

**Pitfall — duration không đọc được:** ffprobe có thể fail với file lạ. Fallback: dùng bitrate mặc định 24k và timeout 600s.

**Pitfall — MSYS path:** ffprobe/ffmpeg trong git-bash cần path kiểu `D:/path/file.mp3`, không phải `/d/path/file.mp3`. Dùng Windows-style forward slash.

> Script: `scripts/compress-audio.sh` trong skill directory (basic). Multi-level fallback implemented in `D:/hermes_upload_server/server.py`.

## Khi nào cần chunk

- File > **22MB** kể cả sau Level 2 (nén 12kbps) → cần chunk
- Strategy: chunk → compress từng đoạn → transcribe tuần tự → ghép kết quả
- Hoặc báo user file quá dài, cần cắt ngắn

## 413 (Payload Too Large) — Retry pattern

```python
r = requests.post(GROQ_URL, files={...}, data={...})
if r.status_code == 413:
    # Nén lại ở bitrate tối thiểu
    subprocess.run(['ffmpeg', '-y', '-b:a', '12k', ...])
    # Retry 1 lần
    r = requests.post(GROQ_URL, files={...}, data={...})
if r.status_code != 200:
    raise RuntimeError(...)  # Bỏ qua, báo user
```

## Cấu hình hiện tại

```yaml
stt:
  enabled: true
  provider: groq
  local:
    model: large-v3
    language: ''
```

> Ref: https://console.groq.com/docs/rate-limits, https://groq.com/pricing/
