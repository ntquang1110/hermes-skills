# Transcript Integrity — không bao giờ viết draft từ transcript cụt (2026-10-05)

## Sự cố thật

TikTok `beausbrain` (105s, `vt.tiktok.com/ZSb91bVYw/`):

1. Call Groq đầu trả `verbose_json` có `text` đầy đủ, NHƯNG script chỉ in
   `print("RAW:", r.stdout[:600])` → chỉ đọc được ~600 ký tự đầu.
2. Lần thử ghi ra file (`-o ...\hermes-tmp\groq_out.json`) fail `FileNotFoundError`
   vì thư mục đích chưa tồn tại.
3. Thay vì fetch lại, một transcript "mở rộng" đã được **viết tay theo suy đoán**
   (thang máy vs cầu thang, donut vs táo, "points of inflection") → draft 3887 chars
   gán các claim này cho tác giả. User duyệt xong mới lộ ra khi đối chiếu.
4. Transcript THẬT (`verbose_json`, 2284 chars) hoàn toàn khác: framework 4 giai đoạn
   `points of awareness → point of contemplation → point of decision → test`.
   Draft phải viết lại từ đầu (3557 chars).

Nội dung suy đoán nghe rất hợp lý và "đúng chủ đề" — chính vì vậy nó nguy hiểm:
không ai phát hiện được nếu không đối chiếu nguồn.

## Quy tắc

1. **Ghi response ra FILE, không đọc stdout.** `curl -s -o <path>.json ...` rồi
   `json.load(open(path, encoding="utf-8"))`. Không bao giờ `print(r.stdout[:N])`
   rồi viết tiếp từ đó.
2. **Path `-o` phải tồn tại trước.** Dùng thư mục thật (`C:\Users\...\hermes-tmp\`,
   tạo bằng `mkdir -p` trước) — không dùng MSYS `/tmp/...` với curl.exe.
3. **Sanity-check độ dài:** audio nói đều ≈ **12-14 ký tự/giây**.
   - 105s → kỳ vọng ~1.300-1.500 ký tự
   - 275s (4.5 phút) → ~3.800-4.800 (đo thật: 4.767)
   - 22 phút → ~20K
   Nhận ít hơn nhiều = CỤT → fetch lại.
4. **Transcript cụt/rỗng → DỪNG.** Không viết tiếp phần thiếu bằng suy đoán, dù
   nghe hợp lý. Draft gán claim sai cho nguồn là lỗi nặng hơn chậm vài phút.
5. **Đã present draft sai → báo user ngay** + viết lại. Đừng sửa ngầm rồi trả bài
   khác nội dung mà không giải thích.
6. `verbose_json` trả thêm `duration` — so với độ dài audio thật để phát hiện file
   tải về bị cắt (YouTube `bestaudio` đôi khi chỉ về một phần).

## Ghi chú phụ — yt-dlp YouTube

Warning `No supported JavaScript runtime could be found. Only deno is enabled by
default ... some formats may be missing` KHÔNG chặn pipeline: `extract_info` vẫn trả
title/channel/duration, và tải `bestaudio` vẫn chạy. Nhưng khi đường caption
(json3 / timedtext) bị 429 hoặc `The read operation timed out` thì rơi thẳng xuống
audio + Groq STT — đúng như nhánh fallback trong SKILL.md.

## Đường dẫn pipeline đã verify trong session này

- Draft: `C:\Users\NTQUANG_DELL\AppData\Local\hermes\cache\draft_<video_id>.txt`
- Transcript: `...\cache\transcript<_tiktok>_<id>.txt`
- Audio tạm: `C:\Users\NTQUANG_DELL\hermes-tmp\`
- Queue: `...\cache\youtube-schedule.json` (220 items, tail 2027-01-22)
- Processed: `...\cache\youtube-processed.json`
