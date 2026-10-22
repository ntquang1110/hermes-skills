---
name: meeting-transcriber
description: "Transcribe file ghi âm cuộc họp → Summary CEO + Assistant với KPI Cards, Issues, Context, Action Items"
category: productivity
---

# Meeting Transcriber

## Khi nào dùng
User gửi **file ghi âm** (voice, .ogg, .mp3) và yêu cầu transcribe + summary meeting.

## Quy trình

### Bước 1: Nhận file ghi âm

Telegram gateway có **hard limit 20MB** cho file download — không config được. Nếu user gửi file >20MB:
  1. Gateway tự động skip, không lưu cache, không đến được STT
  2. Báo user: file quá lớn, yêu cầu gửi lại qua **path local** hoặc nén trước

**Xử lý theo dung lượng:**

| Tình huống | Hành động |
|------------|-----------|
| File < 20MB, gửi qua Telegram | Gateway nhận → cache → STT |
| File > 20MB, gửi qua Telegram | **Gateway chặn** — không thể xử lý |
| File > 20MB, có path local | Xử lý trực tiếp từ path, bypass Telegram |

- Nếu user gửi file qua Telegram và bị chặn → hỏi path local. Ví dụ: `E:\path\to\file.mp3`
- Nếu là voice message Telegram → kiểm tra `C:\\Users\\NTQUANG_DELL\\AppData\\Local\\hermes\\cache\\` hoặc đường dẫn từ platform
### Bước 2: Nén file (compression) — Multi-level fallback

Trước khi transcribe, kiểm tra dung lượng file.

**Pipeline nén 3 cấp:**

Level 1 — Nén Opus với bitrate tính động (target 18MB, dùng ffmpeg Opus mono 16kHz)
Level 2 — Nếu Level 1 output vẫn >22MB → nén lại ở 12kbps (ngưỡng tối thiểu cho speech)
Level 3 — Nếu Groq trả 413 (Payload Too Large) → nén lại ở 12kbps + retry 1 lần

Luôn dùng **dynamic ffmpeg timeout** = `max(300, duration_seconds * 2)` — không hardcode.
Lý do: ffmpeg với file 60+ phút có thể mất >300s để nén. Timeout cứng 300s → kill giữa chừng.

> Chi tiết tham số nén, bitrate cho từng duration, 413 retry → xem `references/groq-whisper-limits.md`
> Script cơ bản: `scripts/compress-audio.sh`

**Pitfall — Unicode/ký tự đặc biệt trong path:** script dùng ffmpeg/ffprobe có thể không đọc được file nếu path chứa tiếng Việt, khoảng trắng, hoặc ký tự đặc biệt. Luôn **copy file sang path ASCII thuần** trước khi nén:
```
cp "/path/to/file/vietnamese name.mp3" "D:/meeting_raw.mp3"
```

**Pitfall — MSYS path `/d/` vs `D:/`:** Trong git-bash, ffprobe/ffmpeg có thể không nhận `/d/meeting_raw.mp3` nhưng nhận `D:/meeting_raw.mp3`. Luôn dùng `D:/` style path cho các lệnh ffmpeg/ffprobe.

### Bước 3: Transcribe
Dùng **Groq Whisper** (STT provider đã cấu hình, free, quality cao cho tiếng Việt) để chuyển giọng nói thành văn bản.

**Provider priority:** Groq Whisper (free, large-v3, không giới hạn 20MB cứng) > local faster-whisper (free, chậm, tốn RAM) > Rook (giới hạn 20MB/file).

> Chi tiết cấu hình STT → xem skill `voice-and-stt`.

#### Transcribe từ local path (bypass Telegram)

Khi file được xử lý từ path local (không qua Telegram gateway), **không dùng STT provider config trong gateway** — gọi trực tiếp Groq API bằng curl:

```bash
# Lấy API key từ env
set -a; source ~/.hermes/.env; set +a

# Plain text output (cho summary)
curl -s -X POST "https://api.groq.com/openai/v1/audio/transcriptions" \
  -H "Authorization: Bearer ${GROQ_API_KEY}" \
  -F "file=@/path/to/compressed.ogg" \
  -F "model=whisper-large-v3" \
  -F "language=vi" \
  -F "response_format=text"

# Verbose JSON (có segments + timestamps)
curl -s -X POST "https://api.groq.com/openai/v1/audio/transcriptions" \
  -H "Authorization: Bearer ${GROQ_API_KEY}" \
  -F "file=@/path/to/compressed.ogg" \
  -F "model=whisper-large-v3" \
  -F "language=vi" \
  -F "response_format=verbose_json"
```

**Lưu ý:** Groq API key từ `.env` có thể bị Hermes redact trong terminal output → dùng `set -a; source` để load vào biến trước khi gọi curl.

### Bước 4: Summary Meeting
Tạo summary dưới **2 góc nhìn**:

#### 👑 Góc nhìn CEO
- **Overall Context**: Bối cảnh, ai họp, về vấn đề gì
- **KPI Cards**:
  - 🎯 Mục tiêu (Objectives)
  - 📊 Chỉ số (Key Results / Metrics)
- **Vấn đề / Blockers**: 🔴 Những gì đang cản trở
- **Rủi ro**: ⚠️ Cảnh báo chiến lược

#### 🤝 Góc nhìn Trợ lý
- **Action Items**: Việc cần làm, ai làm, hạn chót
- **Timeline**: Các mốc thời gian
- **Quyết định**: Những gì đã được quyết định trong cuộc họp
- **Next Steps**: Bước tiếp theo cụ thể

### Bước 5: Định dạng output — 1 HTML duy nhất, 2 tab (user preference)

Tạo **1 file HTML** với 2 tab JavaScript, **không tách thành markdown + HTML riêng.**

> ⚠️ **Mặc định từ 22/08/2026: LƯU LOCAL `D:/Hermes Proj/meeting_<chủ đề>.html`, KHÔNG publish gist/preview** trừ khi user yêu cầu link. Nếu publish, bắt buộc qua design quality gate (skill `impeccable` → Detector Rules → `html-unslop/scripts/unslop-html.py` → ≤1 tell) trước:
> 1. Load skill `impeccable` — chạy Detector Rules checklist
> 2. **Emoji trong UI chrome (tab, heading section) → SVG icon 1 stroke** (bộ icon trong `impeccable/references/svg-icon-set.md`)
> 3. **Bỏ `border-left` màu trên card/callout** (side-tab tell) → dùng tag màu inline + background
> 4. Màu theo token DESIGN.md B/W/Y: `#0f0f0f` nền (không pure black), `#1a1a1e` surface, `#9E9EA4` text-muted, `--border #2D2D32`
> 5. Thêm display font Space Grotesk (Google Fonts) cho h1/h2/.metric, body = system-ui (không Inter)
> 6. Radius lệch nhau (9/11/13px), transition chỉ property cụ thể
> 7. Chạy `html-unslop/scripts/unslop-html.py --file <html> --check` → còn ≤1 tell (ai-auto-grid chấp nhận được nếu có spacing quirk) mới publish
> Kiểm tra sau publish: `curl URL | grep onclick` thấy `switchTab('overview')` + `grep -c "📋|📄|..."` = 0 emoji UI.

#### Tab "Tổng quan"
- **Overall Context**: Bối cảnh, ai họp, về vấn đề gì
- **KPI Cards**: 4 card grid — mỗi card: metric (số/to) + label + note
- **Vấn đề & Blockers**: Mỗi blocker 1 dòng, có tag BLOCKER đỏ / Risk cam
- **Rủi ro**: Dạng list, màu cảnh báo
- **Action Items**: Table: Việc cần làm | Người | Hạn | Ghi chú
- **Quyết định**: Card viền vàng trái
- **Next Steps**: Checklist với ô vuông

#### Tab "Transcript"
- Full conversation với punctuation + paragraph breaks
- Xuống dòng theo speaker / câu hội thoại để dễ đọc
- Footer: model, duration, date

#### Design System (Premium B/W/Y)
```css
:root {
  --yellow: #FFD600; --black: #0D0D0D; --surface: #1B1B1D;
  --surface2: #242428; --text: #E8E8EA; --text-dim: #88889A;
  --red: #FF3B30; --green: #34C759; --orange: #FF9500;
}
```
- Font: system-ui, không dùng Inter/JetBrains Mono
- Responsive: grid 1 cột trên mobile (<600px)
- Sticky tabs, CSS + JS `switchTab()` — không thư viện ngoài

#### Lưu &amp; phân phối (preference 22/08/2026: LƯU LOCAL mặc định)

User Quang yêu cầu: **soạn xong HTML → lưu local vào `D:/Hermes Proj/` trước, KHÔNG publish gist/preview trừ khi user chủ động yêu cầu link chia sẻ.** Tên file: `meeting_<chủ đề>.html` (e.g. `meeting_kiemsaphia_noibo.html`). Báo đường dẫn local + tóm tắt trong chat.

##### ⚠️ OVERRIDE cho group Telegram "hermes - meeting note" (chốt 26/09/2026)

Khi user gửi **text transcript** vào group này (file .txt hoặc paste): **publish NGAY**, không hỏi lại, không chỉ lưu local.
- Template: **NEWSPRINT** (light) — dùng skill `newsprint-design`. KHÔNG dùng Slush.
- Lưu tại `D:/Hermes Proj/meeting_<chủ-đề>.html` **VÀ** publish preview.thefirstonly.com
- Gửi 1 link preview + tóm tắt ngắn. Không gửi markdown kèm.
- User nói "infographic" → làm thêm bản infographic riêng (mục dưới).

##### ⚠️ FONT PHẢI CÓ SUBSET TIẾNG VIỆT (user sửa 26/09/2026: "design lỗi hết font tiếng Việt")

Slush dùng **Antonio** — Google Fonts KHÔNG có subset `vietnamese` → dấu tiếng Việt rơi về fallback, chữ vỡ. **JetBrains Mono cũng KHÔNG có subset vietnamese.**

Chỉ dùng các font sau (đều CÓ subset vietnamese):

| Role | Font | Fallback |
|------|------|----------|
| Headline | **Playfair Display** | 'Times New Roman', serif |
| Body | **Lora** | Georgia, serif |
| UI / label | **Inter** | 'Helvetica Neue', sans-serif |
| Mono / số liệu | **Roboto Mono** (KHÔNG JetBrains Mono) | 'Courier New', monospace |

Link chuẩn:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Lora:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;500;600;700&family=Roboto+Mono:wght@400;500;700&display=swap" rel="stylesheet">
```

Verify sau publish (phải khác nhau, nếu bằng nhau là font chưa áp):
```js
cv.font="40px 'Playfair Display'"; const a=cv.measureText('Chiến lược').width;
cv.font="40px 'Times New Roman'"; const b=cv.measureText('Chiến lược').width;
// a !== b  →  font đã load
```

##### 6. CÂY MEETING THEO DÒNG THỜI GIAN (user duyệt 27/09/2026)

Mọi meeting note **không** nằm phẳng ở `D:/Hermes Proj/`. Nằm trong cây:

```
D:/Hermes Proj/Meetings/
├── INDEX.md          ← bảng timeline, đọc là ra bối cảnh
├── CONTEXT.md        ← tóm tắt bối cảnh + số liệu nhất quán (VIẾT TAY, cập nhật sau mỗi họp)
├── DECISIONS.md      ← nhật ký quyết định theo ngày (VIẾT TAY, chỉ append)
├── _previews.json    ← map tên file gốc → URL preview
├── _archive/         ← bản trùng chủ đề, bản tóm tắt bị thay
└── 2026-08/, 2026-09/
    └── YYYY-MM-DD_<slug>.html
```

**Sau mỗi cuộc họp, chạy:**
```bash
python "C:/Users/NTQUANG_DELL/AppData/Local/hermes/skills/meeting-transcriber/scripts/build-meetings-index.py"
```

Script tự: quét file gốc ở `D:/Hermes Proj/meeting_*.html` + `infographic_*.html`, dedupe (giữ bản **lớn nhất** cùng slug), dựng lại cây, viết `INDEX.md`.

**3 điều script đã sửa sau khi hỏng — đừng làm lại:**
1. **Staging bắt buộc.** Copy vào `Meetings/_stage/` TRƯỚC, xoá `Meetings/20*` SAU, rồi mới move từ staging. Xoá trước rồi move = mất sạch cây (đã xảy ra 2 lần).
2. **Chỉ quét ROOT + `_archive/`.** KHÔNG quét `Meetings/20XX-YY/` — đó là bản dịch, quết lại thành vòng lặp.
3. **`CONTEXT.md` / `DECISIONS.md` không bao giờ bị xoá.** Script chỉ regenerate `INDEX.md`.

**Ngày họp:** `NGAY_GAN` trong script là nguồn sự thật. `mtime` **không tin được** (copy file đổi mtime thành hôm nay). File mới thì thêm dòng vào `NGAY_GAN`; file cũ không còn dùng thì xoá dòng.

**Slug:** bỏ dấu, `đ` → `d`, giới hạn 48 ký tự, cắt tại ranh giới từ. Tên file phải an toàn Windows + URL.

**Backup trước khi chạy lần đầu:** `D:/Hermes Proj/_backup_meetings_20260926/`.

##### 5 luật cứng khi dựng HTML meeting (bắt buộc, user sửa 26/09/2026)

1. **Tiếng Việt PHẢI có dấu đầy đủ** mọi chỗ: heading, card, bảng, transcript, footer. Kiểm tra trước khi publish.
2. **KHÔNG em dash (—) / en dash (–)**. Thay bằng phẩy, hai chấm, hoặc viết lại. Verify: `grep -c '—' file.html` = 0.
3. **Transcript: mỗi lượt nói = 1 ô riêng, KHÔNG lồng div cha con.** Mỗi block viết trên MỘT dòng, tự đóng:
   ```html
   <div class="transcript-block"><span class="tag-sticker tag-S1">Speaker 1</span> Nội dung...</div>
   ```
   Nếu mở div rồi lồng div con bên trong mới đóng → hiển thị loop vô tận. Verify:
   ```bash
   python -c "
   h=open('file.html',encoding='utf-8').read().split('\n')
   bad=[i+1 for i,l in enumerate(h) if l.startswith('<div class=\"transcript-block\">') and not l.rstrip().endswith('</div>')]
   print('nested blocks:', bad)"
   ```
   Kết quả phải `[]`.
4. **Balance div:** `h.count('<div')` == `h.count('</div>')` trước khi publish.
5. **JS tab:** `data-tab` + `onclick="switchTab('x')"`, không escape. Verify sau publish: `curl -s URL | grep -o 'onclick="[^"]*"'` phải ra `switchTab('overview')`.

##### Infographic biến thể (khi user nói "phong cách infographic")

Dựng HTML riêng (không phải bản meeting 2 tab), cấu trúc: Hero tên chủ đề → Top stats row (số to nhất, mỗi card 1 màu) → Grid lĩnh vực/nhóm sản phẩm → So sánh `X vs Y` (số to 2 bên + kết luận giữa) → Card thông số kỹ thuật → Bottom stripe chốt định hướng. Cùng token Slush. Publish riêng 1 link.

#### Publish (chỉ khi user yêu cầu link online)
```bash
python "C:/Users/NTQUANG_DELL/AppData/Local/hermes/skills/productivity/content-publish/scripts/content-upload.py" \
  --file "D:/Hermes Proj/meeting_<chủ đề>.html" \
  --title "Meeting - <ngày> <chủ đề>"
```
Gửi **1 link duy nhất** vào chat — không gửi markdown kèm.

## Cấu trúc output mẫu

```markdown
# 📋 Meeting Summary

## 🧭 Overall Context
[Bối cảnh cuộc họp: dự án nào, ai tham gia, vấn đề gì]

---

## 👑 Góc nhìn CEO

### 🎯 Mục tiêu (KPI Cards)
| Mục tiêu | Chỉ số | Hiện tại | Mục tiêu | 
|----------|--------|----------|----------|
| ... | ... | ... | ... |

### 🔴 Vấn đề & Blockers
- ...

### ⚠️ Rủi ro
- ...

---

## 🤝 Góc nhìn Trợ lý

### ✅ Action Items
| Việc cần làm | Người phụ trách | Hạn | Ghi chú |
|-------------|----------------|-----|---------|
| ... | ... | ... | ... |

### 📌 Quyết định
- ...

### ⏭ Next Steps
- [ ] ...
```

## Lưu ý
- Luôn transcribe trước khi summary
- **Telegram gateway limit (20MB):** Đây là hard limit (`adapter.py:self._max_doc_bytes`) — gateway tự động skip file >20MB, không lưu cache. Chỉ tăng được khi chạy local telegram-bot-api server (`extra.base_url` → 2GB). Xem `references/telegram-gateway-file-limit.md` cho technical deep-dive và `references/web-upload-portal.md` cho giải pháp thay thế (upload portal tại upload.thefirstonly.com — Python server port 8769, file không giới hạn dung lượng). Nếu user gửi file >20MB, ưu tiên hỏi path local trước.
- **Pipeline server (D:/hermes_upload_server/server.py):** Nếu user set up web upload, flow là:
  1. Upload file (multipart POST /upload) → lưu D:/hermes_uploads/
  2. Background thread: compress (3-level fallback Opus) → Groq Whisper → save transcript
  3. `_make_html(transcript, filename)` → publish 2-tab HTML via content-publish script
  4. Trả preview URL (kết quả gửi về chat thủ công — server chưa có webhook)
  Xem `references/web-upload-portal.md` cho full architecture, Cloudflare tunnel config, API token extraction.
- **Giới hạn file Groq Whisper:** ~25MB/file (theo chuẩn OpenAI-compatible). Nếu file đã qua gateway nhưng > 20MB hoặc dài > 60 phút → chunk thành từng đoạn (ví dụ 10-15 phút/đoạn) và xử lý tuần tự. Groq không có hard limit 20MB như Rook, rate limit tính theo audio seconds/hour.
  - **Pattern chunking đã chốt (P7):** chunk ~10 phút + **overlap 15-30s** giữa các chunk (tránh mất từ bị cắt giữa câu) → transcribe từng chunk → nối transcript + timeline (`chunk 1 = 00:00-10:00, chunk 2 = 10:00-20:00...`). Nén Opus 16kHz mono nếu chunk vẫn nặng. Fallback lỗi 413 → giảm bitrate + chunk nhỏ hơn + retry. Dùng ffmpeg: `-ss start -t duration -ar 16000 -ac 1` cho từng chunk.
- Dùng tiếng Việt có dấu cho output (trừ khi nội dung gốc tiếng Anh)
- **Multi-user group:** Bot chỉ trả lời user trong `TELEGRAM_ALLOWED_USERS` (.env). Nếu có người khác trong group mà bot không reply, thêm user ID của họ vào biến đó và restart gateway.

## Upload băng thông thấp / file lớn — streaming receive (updated 15/08)

Server upload portal (`D:/hermes_upload_server/server.py`) đã chuyển sang **streaming receive**:

1. **Không đọc cả body vào RAM** — đọc theo chunk 64KB, ghi thẳng ra disk, chỉ giữ `keep = len(boundary)-1` bytes cuối để không cắt boundary. File 500MB+ không ngốn RAM.
2. **ThreadingHTTPServer** (thay HTTPServer) — 1 upload lớn không block server.
3. **Progress thật** trong upload.html — XHR `upload.onprogress` (fetch không có upload event), hiển thị % + KB/s + thời gian còn lại. Bỏ fake interval.
4. **Nén vẫn xảy ra SAU khi nhận đủ file** (theo yêu cầu Quang 15/08: upload không giới hạn theo mạng, nhận đủ rồi mới nén).

### Pitfall — `rfile.read(n)` BLOCK vô hạn trên keep-alive socket

❌ **Sai:** `self.rfile.read(65536)` trong vòng lặp nhận file — BufferedReader.read(n) block cho tới khi đủ n bytes HOẶC EOF. HTTP/1.1 keep-alive không đóng socket sau body → không bao giờ EOF → treo vô hạn khi phần còn lại < 65536. Biểu hiện: upload file 60MB, file ghi đủ nhưng **response trống**, curl timeout 90-120s, server log `ConnectionAbortedError: [WinError 10053]` khi cố gửi response.

✅ **Đúng:** đọc theo đúng số bytes còn lại từ Content-Length:
```python
left = content_length - read_total
if left <= 0:
    f.write(remaining); size += len(remaining); break
chunk = self.rfile.read(min(65536, left))
read_total += len(chunk)
remaining += chunk
```
- `read_total` khởi tạo = `len(header_buf)` (đã đọc từ socket khi parse header)
- `Content-Length` phải parse từ header (`int(self.headers.get("Content-Length", 0))`)
- Sau khi ghi file xong: **drain** phần closing boundary còn lại (`to_drain = content_length - read_total`) để socket sạch, không lẫn response.

### Verify sau khi sửa (đã test 15/08)
- 1MB upload: 1.27s, response `{"status":"uploaded"}`
- 60MB upload: 1.44s, file lưu chính xác 62914560 bytes
- Pipeline nén → Groq Whisper → HTML vẫn chạy (transcript + notes tạo đủ)

### Chunked upload — vượt giới hạn Cloudflare ~100MB (added 15/08)

**Vấn đề:** Cloudflare free plan chặn request body >~99MB (`413 Payload Too Large`). Test thật: 90MB OK, 100MB/101MB/110MB → 413. File vài trăm MB không upload thẳng được qua tunnel.

**Giải pháp:** chunked upload — chia file thành phần 80MB, upload tuần tự, server ghép lại.

**API:**
- `POST /upload-chunk` — multipart fields: `upload_id, chunk_index, total_chunks, filename` + file. Trả `{status, received:[...], total}`.
- `POST /upload-complete` — multipart field: `upload_id`. Server verify đủ chunks → ghép theo thứ tự → queue xử lý → trả `{file_id, size_mb}`.
- `GET /upload-status?upload_id=X` — trả `{status, received:[...], total, filename}` — dùng cho resume (client skip chunks đã nhận).

**Trạng thái session:** `chunk_sessions[upload_id] = {filename, total, received:set}` trong RAM (thread-safe bằng `SESSION_LOCK`). Chunk lưu tại `D:/hermes_uploads/.chunks/<upload_id>/<index:06d>.bin`. Server restart → session mất → client phải upload lại (chấp nhận được; có thể persist sau).

**Frontend:** upload.html tự quyết định — file ≤90MB upload thẳng `/upload`, file >90MB chunked 80MB. Lưu `upload_id` vào localStorage (`chunk_upload_<name>_<size>`) → resume khi mất mạng, retry 3 lần/chunk, progress thật (% + KB/s + thời gian còn lại + phần i/total).

**Pitfall — multipart parser giữ boundary cho vòng ngoài:**
Khi parse nhiều part (text fields + file), sau khi xử lý xong 1 part KHÔNG cắt cả `\r\n--boundary`, chỉ cắt `\r\n` (2 bytes) để `--boundary` còn lại cho vòng lặp ngoài nhận diện part kế tiếp. Cắt cả delimiter → vòng ngoài nuốt nhầm data vào buffer, text fields sau đó bị mất (triệu chứng: `received` chỉ [0], filename sai, các chunk ghi đè lên nhau).

**Verify (test thật 15/08):**
- 250MB = 4 chunk (80+80+80+10) qua localhost → complete → MD5 khớp 100%.
- 100MB = 2 chunk qua tunnel thật → 200 OK, MD5 khớp (trước đây 413).
- Resume: gửi lại chunk đã có → received giữ nguyên, không double-count.

## Calendar Integration

Sau khi transcribe meeting, có thể tạo sự kiện lịch tự động:

- **Lark Calendar** (ưu tiên, đã cấu hình sẵn): Xem `references/lark-calendar-api.md`
- **Google Calendar**: Cần token có `calendar` scope

## Pitfalls & Quality Checks

### ⚠️ HTML tab switching: dùng `data-tab` + entity quotes, KHÔNG dùng textContent.includes
❌ **Sai lầm:** Để `onclick="switchTab('overview')"` khi wrap HTML trong f-string Python → inner `'` bị Python escape thành `\"` → trình duyệt parse `onclick="switchTab("overview")"` → syntax error, tab không bấm được.
✅ **Cách xử lý — 2 cách an toàn:**
  - **Cách 1 (recommended):** Dùng `data-tab` attribute + `b.dataset.tab===n` trong JS:
    ```html
    <button class="tab-btn active" data-tab="overview" onclick="switchTab('overview')">📋 Tổng quan</button>
    ```
    JS: `b.classList.toggle('active', b.dataset.tab === n)`

  - **Cách 2:** Dùng HTML entity `&#39;` thay cho `'`:
    ```html
    <button class="tab-btn" onclick="switchTab(&#39;transcript&#39;)">📄 Transcript</button>
    ```
    
  Kiểm tra output HTML bằng `curl URL | grep onclick` trước khi gửi user — nếu thấy onclick="switchTab("overview")" là lỗi.

### ⚠️ Summary Tab: Không lấy first-N-chars
❌ **Sai lầm:** Summary tab chỉ hiện 200-250 ký tự đầu transcript → vô nghĩa, user không hiểu gì.
✅ **Cách xử lý — Keyword extraction cho summary:**
  - Extract câu chứa từ khóa chính của cuộc họp (sản phẩm, cơ chế, tiêu chảy, giá thành, thử nghiệm, etc.)
  - Dedup câu trùng ý (same first 60 chars)
  - Gom tối đa 10 câu tiêu biểu → ghép thành đoạn summary
  - Kiểm tra: summary phải ≥100 ký tự, nếu không fallback về first-400-chars
  - Code mẫu trong Python:
    ```python
    topics = ['sản phẩm', 'cơ chế', 'chi phí', 'giá thành', ...]
    key_lines = [line for line in transcript.split('.')
                 if any(t in line.lower() for t in topics) and len(line) > 30]
    summary = '. '.join(dict.fromkeys(l[:60] for l in key_lines[:10])) + '.'
    ```


### ⚠️ Telegram gateway chặn file > 20MB
❌ **Sai lầm:** User gửi file audio >20MB qua Telegram → báo lỗi "exceeds the 20 MB limit" — không thể transcribe.
✅ **Cách xử lý:** Telegram gateway có hard limit 20MB ở phía download, không config được. Yêu cầu user:
  - Cung cấp **path local** (ví dụ `E:\recordings\meeting.mp3`) → xử lý trực tiếp từ máy
  - Hoặc nén file xuống < 20MB rồi gửi lại
  - **Không khuyên** user upload lên cloud share link — mất thời gian, thêm bước
- Luôn ưu tiên path local nếu file có sẵn trên máy user

### ⚠️ Xác nhận số liệu — Vietnamese numerical slang & hướng tài chính
❌ **Sai lầm thường gặp:** Đọc "8 lít" thành "8 triệu", hoặc nhầm hướng "lỗ" thành "lãi".
✅ **Cách xử lý — Vietnamese numerical slang:**
  - **"x lít"** = x × 100,000 (VD: "8 lít" = 800k — **lỗi phổ biến: đọc nhầm thành 8 triệu**)
  - **"x củ"** / **"x chai"** = x × 1,000,000 (VD: "4 củ" = 4 triệu)
  - **"x xị"** = x × 100,000 (miền Nam)
  - **"x cây"** = x × 1,000,000 (hoặc 10,000 tùy ngành)
  - **"x xị"** = x × 100,000 (miền Nam)
✅ **Cách xử lý — Hướng tài chính:**
  - Từ khóa số âm: *lỗ, mất, thua, cao hơn chi phí, không có lãi, âm, thâm hụt*
  - Từ khóa số dương: *lãi, tiết kiệm, lợi nhuận, dư, hiệu quả hơn*
  - Nếu nghi ngờ → interpret theo hướng thấp/tiêu cực rồi confirm với user
  - KPI Cards đỏ = số âm (lỗ, mất), xanh = số dương (lãi, tiết kiệm)

### ⚠️ Không suy diễn số liệu không có trong transcript
- Không thêm các KPI "mục tiêu" nếu cuộc họp không đặt ra mục tiêu cụ thể
- Không biến "đang thử nghiệm" thành "đã hoàn thành"
- Chỉ dùng số liệu có thực trong transcript, không phóng đại hoặc suy luận chủ quan

### ⚠️ Xác nhận tên riêng, thuật ngữ chuyên ngành
- Transcript từ Whisper có thể sai tên riêng, tên thuật ngữ, tên sản phẩm
- Kiểm tra ngữ cảnh để suy luận tên đúng. Ví dụ: "kiềm" = sản phẩm/giải pháp của công ty, "Dapaco" = tên đối tác/trại
- Nếu không chắc chắn về tên riêng → để nguyên transcript hoặc hỏi user

### ⚠️ Gửi local / 1 link HTML preview (không markdown riêng)
- Output chính là **1 file HTML** (2 tab: Summary + Transcript), **mặc định lưu local `D:/Hermes Proj/`** (22/08/2026).
- Chỉ gửi link online khi user chủ động yêu cầu chia sẻ.
- Khi gửi local: báo đường dẫn file + tóm tắt ngắn. Khi publish: gửi 1 link duy nhất, không gửi markdown kèm (dư thừa, mất thẩm mỹ).
- HTML đã responsive, đọc được trên mobile, không cần markdown fallback
