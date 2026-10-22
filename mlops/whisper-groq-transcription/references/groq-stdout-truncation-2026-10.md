# Groq response qua stdout bị CẮT → dùng nhầm transcript thiếu (2026-10-05)

## Sự cố thật

`verbose_json` cho audio TikTok 105s trả `text` đầy đủ, nhưng script chỉ in
`print("RAW:", r.stdout[:600])` → chỉ đọc được ~600 ký tự đầu (kỳ vọng ~1.400).
Phần thiếu bị viết tiếp bằng **suy đoán** và dùng để viết draft → gán sai claim
cho tác giả. Transcript thật khi fetch lại: 2.284 ký tự, nội dung khác hoàn toàn.

Đây là lỗi nặng hơn "chậm": nội dung sai được gán cho nguồn thật, và không ai phát
hiện nếu không đối chiếu lại transcript.

## Cách gọi Groq ĐÚNG (ghi ra file, không đọc stdout)

```bash
mkdir -p "$WORKDIR"                      # -o phải trỏ vào thư mục CÓ THẬT
curl -s --max-time 120 -o "$OUT" \
  -X POST https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_KEY" \
  -F "file=@$MP3" \
  -F model=whisper-large-v3 \
  -F language=en \
  -F response_format=verbose_json
python - <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
print("chars:", len(d["text"]), "| duration:", d.get("duration"))
PY
```

- KHÔNG `print(r.stdout[:N])` rồi viết tiếp — buffer/tool cap cắt mất phần sau.
- `-o` phải là path Windows/C: THẬT. MSYS `/tmp/...` không thấy bằng curl.exe; và
  `-o` vào thư mục chưa tạo → `FileNotFoundError` khi `json.load`.
- Đọc lại bằng `json.load(open(OUT, encoding="utf-8"))`, không parse `r.stdout`.
- `GROQ_API_KEY`: lấy **dòng cuối** khớp `GROQ_API_KEY=gsk`, verify `len==56` và
  không chứa `...` (file .env từng bị tool cắt thành bản rút gọn).

## Sanity-check độ dài (BẮT BUỘC trước khi dùng transcript)

Nói đều ≈ **12-14 ký tự/giây**.

| Audio | Kỳ vọng |
|---|---|
| 105 s (TikTok) | ~1.300-1.500 |
| 275 s (video 4.5 phút) | ~3.800-4.800 (đo thật 4.767) |
| 22 phút | ~20.000 |

Ít hơn nhiều = transcript cụt → fetch lại. `verbose_json` trả `duration` — so với
độ dài file audio thật để phát hiện file tải về bị cắt một phần.

## Quy tắc

1. Transcript cụt/rỗng → **DỪNG, fetch lại**. Không viết tiếp bằng suy đoán.
2. Nếu đã lỡ dùng transcript sai để viết draft → **báo user ngay** và viết lại;
   đừng sửa ngầm rồi trả bài khác nội dung mà không giải thích.
3. Cùng nhánh này áp cho YouTube: khi caption json3 bị 429 / `The read operation
   timed out` thì rơi xuống audio + Groq STT, và vẫn phải qua sanity-check độ dài.
