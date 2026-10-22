# Groq Whisper Quality Tuning — đã test thực tế

Nguồn: session fix pipeline TFO meeting (D:/Hermes Proj/ai-company/app/main.py), file 20 phút 17.3MB MP3.
Kết quả test: transcript từ 3338 chars (kém) → 5340 chars sạch, bắt đủ tên người + con số + thuật ngữ.

## 1. Pipeline transcribe chuẩn (đã verify)

```
audio gốc (mp3/m4a/webm)
  → [ffmpeg] volume=12dB,highpass=f=80,lowpass=f=8000, 16kHz mono, Opus 48k
  → [Groq Whisper large-v3] language=vi, response_format=text, prompt NGẮN
  → [heuristic clean] nếu có hallucination
```

### Code tham chiếu (Python)

```python
def _groq_transcribe(path, force_compress=False, clean=True):
    # Luôn nén + boost trừ file rất nhỏ (< 1MB)
    if size_mb > 1 or force_compress:
        subprocess.run([
            "ffmpeg", "-y", "-i", str(path),
            "-af", "volume=12dB,highpass=f=80,lowpass=f=8000",
            "-ar", "16000", "-ac", "1",
            "-c:a", "libopus", "-b:a", "48k", str(compressed),
        ], timeout=120)
    # POST https://api.groq.com/openai/v1/audio/transcriptions
    # data={"model": "whisper-large-v3", "language": "vi",
    #       "response_format": "text", "prompt": INITIAL_PROMPT}
```

## 2. Tham số đã test — cái nào ăn, cái nào không

| Cấu hình | Kết quả (chars / 20 phút) | Nhận xét |
|----------|---------------------------|----------|
| mp3 gốc gửi thẳng, không nén, không boost | 3338 | Mất nội dung |
| chunk 15p, không boost | 4208 | Mất, hallucination |
| chunk 10p + Opus 48k, không boost | 6457 | Tốt hơn nhưng mất "anh Mão trại 20-30 con" |
| boost toàn file rồi gửi thẳng | 5392 | **Bắt được chi tiết nhỏ tiếng** |
| boost + chunk 10p | 5697 | Tương đương, chunk thêm an toàn cho file dài |
| LLM clean (llama-3.3-70b) | ❌ | Xóa luôn nội dung thật, trả câu meta "Không có nội dung" |
| heuristic clean | ✅ | Chỉ bỏ câu quảng cáo + chữ vô nghĩa |

Kết luận: **boost là yếu tố quyết định**. Opus 48k + boost toàn file trước → gửi thẳng nếu < 25MB; chỉ chunk khi > 55 phút.

## 3. Hallucination cleaning heuristic (Python)

```python
import re
def _clean_transcript(text):
    REPLACE = [("kiếm vãi nặng","kim loại nặng"), ("tiêu sảy","tiêu chảy"), ...]
    for old, new in REPLACE:
        text = text.replace(old, new)
    # Whisper trả 1 DÒNG liền → tách theo câu, KHÔNG theo dòng
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text)
    AD_MARKERS = re.compile(
        r"subscribe|đăng ký kênh|ủng hộ kênh|like.{0,4}share|hẹn gặp lại|"
        r"cảm ơn các bạn đã theo dõi|ghền mì gõ|ghiền mì|nhận thông tin nhất|"
        r"đăng ký kênh để|theo dõi và hẹn|video hấp dẫn", re.IGNORECASE)
    cleaned = []
    for s in sentences:
        s = s.strip()
        if not s: continue
        if AD_MARKERS.search(s):
            if len(s) > 200:          # câu dài có thể chứa nội dung thật
                s = AD_MARKERS.sub(" ", s)
            else:
                continue
        words = re.findall(r"[a-zà-ỹ]+", s.lower())
        if words and len(words) >= 8:
            if sum(len(w) for w in words)/len(words) < 2.5:
                continue              # chữ vô nghĩa lặp ký tự
        if cleaned and cleaned[-1][:30].lower() == s[:30].lower():
            continue                  # câu lặp liên tiếp
        cleaned.append(s)
    result = " ".join(cleaned)
    return result if len(result) > 50 else text   # bảo vệ: không xóa sạch
```

Marker "Ghiền Mì Gõ" / "La La School" / "lalaschool" = YouTube channel hallucination kinh điển của Whisper — gặp là xóa.

## 4. Summarize dài — chunk-summarize, không truncate

Lỗi kinh điển: `transcript[:8000]` cắt mất 2/3 nội dung cuộc họp dài → vấn đề/task/decision sai hoặc thiếu.
Fix: chia transcript → summarize từng đoạn (model flash, system NGẮN) → gom → ép JSON cuối.

⚠️ **2026-08 UPDATED — KHÔNG dùng `response_format={"type":"json_object"}` với OpenCode endpoint
(`https://opencode.ai/zen/go/v1/chat/completions`) — nó LUÔN trả content rỗng.** Ép JSON bằng prompt
("OUTPUT: CHỈ JSON thuần, bắt đầu bằng {."). Chi tiết đầy đủ + retry patterns →
`hermes-model-provider-troubleshooting` skill → `references/opencode-empty-json-quirks.md`.

```python
def _summarize_full(transcript):
    # chunk 3500 chars + overlap 200 (chunk 5000 + system dài → endpoint trả RỖNG)
    chunks = [transcript[i:i+3500] for i in range(0, len(transcript), 3300)]
    if len(chunks) <= 1:
        return _summarize_single(transcript)
    partials = [summarize_llm(c, sys_short) for c in chunks]   # từng đoạn, system NGẮN
    combined = "\n\n".join(partials)[:4000]                     # cắt ≤ 4000 cho bước cuối
    return _summarize_single(combined)

def _summarize_single(text):
    # system prompt yêu cầu JSON: summary, issues[], decisions[], tasks[{title,assignee,deadline}]
    # KHÔNG response_format → gọi model; nếu kết quả bắt đầu "{" → OK
    # nếu model trả markdown (input dài) → ép JSON LẠI trên output ngắn, retry 4x
    # timeout requests PHẢI ≥ 180s (60s không đủ cho prompt dài)
```

JSON output 4 phần: `summary` (tóm tắt ngắn), `issues` (vấn đề/blockers), `decisions` (quyết định), `tasks` (title/assignee/deadline). Task gen đọc thẳng JSON — bỏ regex keyword ("task", "cần làm", "giao") vốn miss gần hết.

## 5. TFO server (D:/Hermes Proj/ai-company)

- Chạy bằng Python311 hệ thống, KHÔNG phải hermes venv:
  `"/c/Users/NTQUANG_DELL/AppData/Local/Programs/Python/Python311/python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8100`
  (hermes venv thiếu pydantic_core build → ModuleNotFoundError khi import app)
- Restart: kill PID cũ qua `taskkill -f -pid <PID>` (single-dash trong git-bash), rồi start background.
- Chunking quyết định theo duration: `_get_duration(path) > 3300` (55 phút) → `_transcribe_chunked`, ngược lại `_groq_transcribe` direct.
- `call_deepseek` trong hub/store.py: thêm param `response_format` để hỗ trợ json_object.
