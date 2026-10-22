---
name: youtube-threads-pipeline
description: "End-to-end pipeline: YouTube transcript -> summarize (Vietnamese plain style) -> schedule queue -> auto-post to Threads as reply chain. Covers cron jobs, Playwright automation, and scheduling rules."
platforms: [windows]
---

# YouTube to Threads Pipeline

Use when setting up or troubleshooting the automated content pipeline that takes YouTube videos, summarizes them in a specific Vietnamese style, schedules them for posting, and auto-publishes to Threads as reply chains.

## Core Flow

```
User sends URL (or cron finds content)
  -> fetch_transcript.py (youtube-transcript-api)
  -> summarize in Vietnamese plain style
  -> add to schedule queue (youtube-schedule.json)
  -> cron job 20:00 posts to Threads via Playwright
  -> reply chain on threads.com/@ntquang1110
```

## Cron Jobs

| Job | Time | Function |
|-----|------|----------|
| Daily Research | 07:30 | Search web for content on topics, fetch transcript, write draft, SEND TO USER FOR APPROVAL before saving to queue |
| YouTube Schedule Poster | 20:00 | Read queue, post next pending item to Threads |

### Research Topics (rotate)

- Than kinh (neuroscience, brain plasticity, dopamine)
- Hanh phuc (happiness, well-being, psychology)
- AI (AI skills, AI and humans)
- Business mind (business mindset, leadership, productivity)

## Writing Style (Quang's Voice — SOUL.md, đã duyệt 2026-08)

User chốt style này sau nhiều lần chê "nông cạn". Bắt buộc tuân theo:

- **Language**: Tiếng Việt có dấu đầy đủ. CRITICAL: Python heredoc/terminal STRIPS dấu tiếng Việt. Viết nội dung bằng `write_file` (giữ encoding) rồi đọc lại từ file; KHÔNG hardcode trong heredoc (`python << 'PYEOF'` → 0 accents).
- **No icons/emojis**: Tuyệt đối không dùng icon, emoji, ký hiệu.
- **No em dashes**: Không dùng — (em dash) hoặc – (en dash). Chỉ dùng - (hyphen).
- **Short sentences**: Câu ngắn, trực tiếp. Một ý mỗi câu, tối đa hai.
- **Mở đầu**: 1-2 câu gây tò mò, tự nhiên như đang nói chuyện (chuyện cá nhân, câu hỏi).
- **Tầng 1 — Cơ chế**: giải thích khoa học/thần kinh đằng sau (PFC, amygdala, dopamine, mirror neurons, cortisol...). Mỗi câu một ý.
- **Tầng 2 — Vòng xoáy/Hệ quả**: cái gì xảy ra khi cơ chế kéo dài. Vòng lặp tự củng cố. Dẫn chứng nghiên cứu (tên tác giả, thí nghiệm).
- **Kết luận**: câu chốt sâu sắc, gọn. **Trích nguyên văn quote từ nguồn — đừng paraphrase mơ hồ** (user: "tại sao mơ hồ thế, em trích dẫn đoạn đó cho anh xem nào"). Đừng "tóm lại". Kết bằng góc nhìn khiến người đọc suy nghĩ lại.
- **KHÔNG dùng "Tóm lại"** ở cuối (user đã bỏ rule cũ này).
- **DEPTH = THESIS, không phải tóm tắt mạch truyện (CRITICAL, 2026-08-27)**:
  Khi viết từ podcast/interview/channel, đừng summarize theo THỨ TỰ SỰ KIỆN
  (guest làm X -> chuyện Y -> thời điểm Z). Đó là bản tin, và Quang chê
  "hơi nông cạn" đúng chỗ này. Phải tìm THESIS của talk (thường nêu ngay
  ở intro / lời mở) và dựng bài QUANH luận điểm đó:
  - Mở bằng thesis (1 câu phá giả định), "Tầng 1, cơ chế" = hệ thống/tư duy/
    chiến lược cốt lõi, "Tầng 2, vòng lặp/hệ quả" = nó bền vững thế nào.
  - Giữ quote nguyên văn những câu đắt + con số. Câu chốt cuối = punchline quote.
  - Test nhanh trước khi gửi: nếu không viết nổi 1 dòng "talk này luận điểm là
    gì / tại sao tồn tại", thì bản còn nông, viết lại.
  - "transcript + summarize" KHÔNG có nghĩa là mỏng. Mỏng khác với ngắn.
    Case mẫu đã duyệt: `D:/Hermes Proj/macro-14.02/draft_hll_ep1.txt` (Municipal,
    3905 chữ). Chi tiết: `references/podcast-channel-ingest.md`.

## TikTok URL drops — khác YouTube, cần audio transcription (thêm 2026-09-18)

Khi user dán link TikTok (vt.tiktok.com / tiktok.com/@user/video/...):

1. **Download**: `python -m yt_dlp --impersonate Chrome-131 "URL"`
   - `--impersonate Chrome-131` là bắt buộc cho TikTok (JS challenge)
   - Output filename chứa `$1m`, `$3m` -> bash interpret thành biến. **Rename ngay**: `mv "file...\$1m..." tiktok_video.mp4`
2. **Không có subtitles** — TikTok không expose transcript API. Phải extract audio + transcribe:
   - `ffmpeg -y -i tiktok_video.mp4 -vn -ar 16000 -ac 1 -b:a 64k tiktok_audio.mp3`
3. **Transcribe** — dùng faster-whisper qua Hermes venv Python:
   ```
   /c/Users/NTQUANG_DELL/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe -c "
   from faster_whisper import WhisperModel
   model = WhisperModel('base', device='cpu', compute_type='int8')
   segments, info = model.transcribe('C:/Users/NTQUANG_DELL/tiktok_audio.mp3', language='en', beam_size=5)
   print(' '.join(seg.text for seg in segments))
   "
   ```
   ⚠️ **Không dùng `python` (system default)** — Python 3.14 không tương thích numpy/faster-whisper. Luôn dùng full path venv Python.
   ⚠️ Nếu GROQ_API_KEY còn sống, có thể dùng Groq STT thay faster-whisper (nhanh hơn). Key hiện tại trong .env đã hỏng.
4. **Nội dung routing** — TikTok business/SaaS content (Alex Hormozi, etc.) thuộc category business, không tâm lý. Viết draft thesis-driven, quote nguyên văn câu đắt.
5. Dọn file tạm sau xong: `rm -f tiktok_video.mp4 tiktok_audio.mp3`

## Manual URL drops trong group (user dán link, không phải cron) — thêm 2026-09-03

Khi Quang dán MỘT URL YouTube trần vào group convert/publish (không kèm lệnh):
- Đây là yêu cầu THỦ CÔNG xử lý video này ngay, đúng chuẩn cron flow (draft → duyệt → queue) nhưng KHÔNG auto-post.
- Flow: oEmbed title → fetch_transcript → đọc TOÀN BỘ → draft theo thesis + title blocks → unslop_check + chunk_500 → gửi duyệt. Đừng bỏ qua bất kỳ gate nào chỉ vì thủ công.
- Trước khi fetch: check processed + quét 3 queue (None-safe, xem Pitfalls) để không làm lại video đã xử lý/đang chờ.
- **Duyệt ngầm (implicit approval) — cập nhật 2026-10, thay rule cũ**: Quang KHÔNG nói "ok" mỗi lần. Khi anh dán link mới vào group, việc đó ĐỒNG THỜI là (a) duyệt bài draft vừa gửi ở lượt trước, và (b) yêu cầu xử lý link mới. Nên: add bài trước vào queue ở ngày `max+1` (ngày đệ đề xuất cuối reply trước) TRƯỚC KHI fetch link mới, rồi mới chạy flow cho link mới. Vẫn KHÔNG tự post — chỉ tự add queue. Nếu reply trước đệ chưa đề xuất ngày cụ thể, đề xuất rồi hỏi; đừng đoán mò.
- **Chỉ nhận "ok" trần khi có draft đang chờ**: nếu không có draft nào chờ duyệt mà user nói "ok", HỎI lại đang duyệt bài nào — đừng add nhầm.
- **Batch nhiều URL liên tiếp trong 1 phiên**: Quang gửi từng link một, đệ draft từng bài gửi duyệt, rồi cuối buổi user thường trả một câu terse "ok duyệt hết" để duyệt CÙNG LÚC nhiều draft. Khi đó add toàn bộ vào queue trong MỘT script, giữ MỘT biến `nxt` tăng dần (bài 1 = max+1, bài 2 = max+2,...), update processed.json (video_ids + urls + items) trong cùng run, rồi verify từng id + date + status + content chars.
- **Content-type routing**: queue tâm lý chung (youtube-schedule.json) có thể nhận nội dung không phải tâm lý (khoa học/math, business/sales, communication) khi Quang xử lý video học thuật. Đây là convention chấp nhận được — chỉ cần báo đuôi lịch mới. Nếu thật sự không chắc nên vào queue chung hay kênh riêng (macro/HLL), HỎI trước khi add; nhưng "duyệt hết" trần = đưa hết vào queue tâm lý chung.

### Case phiên 2026-09-03 (batch 4 URL)
Krishnamurti (vi auto-gen transcript, 27.8K), Terence Tao "Six Math Essentials" (EN 92K, solution-driven), Will Barron sales systems, Patrick Winston "How to Speak". Mỗi bài → unslop PASS (0 em dash/emoji) → chunk_500 mọi part ≤ 500 → gửi duyệt. Quang: "Ok duyệt hết" → add liền mạch ngày kế tiếp (18/11, 19/11, 20/11). Vi EN transcript đều nhiễu tên riêng (Krishnamurti→"Krisam", Terence Tao OK nhưng Wigner→"Eugene RNA", Bohr→"Neil B") — phục hồi theo ngữ cảnh, đừng quote bản rối.

## Playlist / Course content (batch) — thêm 2026-08-27

Áp dụng khi user đưa một PLAYLIST học thuật (MIT OCW, Stanford, ...) và muốn xử lý nhiều lecture tuần tự. Case: MIT 14.02 Principles of Macroeconomics, playlist `PLUl4u3cNGP62EXoZ4B3_Ob7lRRwpGQxkb` (25 bài, ~50 phút/bài).

### Style khác hẳn neuroscience
Nội dung học thuật kinh tế (GDP, IS-LM, Phillips curve, Mundell-Fleming, exchange rate, growth) KHÔNG có amygdala/cortisol/mirror neurons. Ép cấu trúc tâm lý vào = giả tạo. Adapt:
- Giữ giọng Quang (câu ngắn, mở đầu hồi tưởng/câu hỏi, dấu đầy đủ, no emoji, no em dash).
- Nội dung chia 2 phần chính (cơ chế + hệ quả/vòng lặp), áp dụng Mỹ/Việt Nam, con số thật.
- **KHÔNG dùng cụm "Tầng 1"/"Tầng 2" trực tiếp** (user chốt bỏ, 2026-08-31, sau 2 lần nhắc). Thay bằng TIÊU ĐỀ đứng riêng cho mỗi phần, và mỗi title phải thành MỘT REPLY RIÊNG trên thread (xem dưới).
- Quote con số GIỮ NGUYÊN văn (vd S&P sập 2%, nonfarm payroll dự đoán 190k vs thực 500k, lạm phát 6.5-8%, target 2%).
- Hook hay thường là nghịch lý thật: "tin tốt làm thị trường sập vì Fed phải tăng lãi suất".

### Cấu trúc reply + tiêu đề (user chốt 2026-08-31)

`threads_poster.py` chia bài thành reply theo BLOCK `\n\n` (split_posts trên mỗi khối ngăn cách bởi dòng trống): mỗi block = một reply riêng. Nên:
- Mỗi TIÊU ĐỀ đứng một mình thành block riêng → nó ra một reply riêng (đúng yêu cầu user "mỗi tiêu đề là 1 reply riêng trong thread").
- KHÔNG đặt title inline đầu một khối nội dung dài (nó bị dính vào reply nội dung, không có reply hiển thị title riêng).
- Cấu trúc macro chuẩn: [block mở hook] → [block: title 1] → [block(s): nội dung phần cơ chế] → [block: title 2] → [block(s): nội dung hệ quả/vòng lặp] → [block: kết]. Draft lecture 4 đã căn đúng mẫu này.

### Protocol duyệt (user chốt 2026-08-27)
User: "trước ngày đăng 1 ngày em gửi cho anh duyệt đi". Nghĩa là:
- Mỗi ngày xử lý 1 lecture kế tiếp, draft → gửi duyệt.
- User OK → lên lịch đăng ngày hôm sau.
- KHÔNG tự đăng, KHÔNG tự add queue trước khi duyệt.
- User chốt lịch (a): playlist mới đăng kênh RIÊNG / xen kẽ từ hôm nay, KHÔNG chèn đuôi queue chung đang full. xác nhận lịch trước khi chốt.

### Playlist processing kỹ thuật
- Lấy danh sách video: yt-dlp flat playlist JSON (xem references/yt-dlp-playlist.md).
- Track tiến độ lecture đã xử lý để không trùng: ghi file state riêng theo playlist (vd `D:/Hermes Proj/macro-14.02/`).
- Kiểm tra queue trước khi lên lịch (77 pending bài tâm lý → đừng đè lên — đã xác nhận queue full tới 13/11).

### Kênh SONG SONG (channel thứ 2, cùng hệ thống publish)

Khi user thêm một kênh nội dung mới chạy song song với queue tâm lý (playlist khác topic, e.g. macroeconomics) — KHÔNG đè vào `youtube-schedule.json`. Dùng 1 queue + 1 scheduler + 1 cron riêng, và đặt giờ poster lệch khỏi 20:00 (2 Chromium dùng chung `threads_state.json` cùng phút = xung đột session, đã bị). Kèm một resolver "draft-waiting": chỉ draft lecture kế khi không còn draft đang chờ duyệt (tránh trùng/lặp). Toàn bộ recipe có file đầy đủ: `references/parallel-content-channel.md`. Bản mở rộng cho một CHANNEL podcast (không phải course, hàng trăm episode) — lọc video <30 phút, nhịp 3 bài/ngày, style "transcript + summarize": `references/podcast-channel-ingest.md`.

## Science-content interviews (single video, e.g. Big Think) — thêm 2026-09-03

Áp dụng khi user gửi MỘT video dạng talk/interview học thuật khoa học (Big Think, TED, nhà khoa học nói về ngành của họ). Đây là style THỨ BA: khác tâm lý (không amygdala/dopamine) và khác macro (không GDP/IS-LM). Case: Terence Tao "Six Math Essentials" (OOMx2BHHWtE, Big Think, 37 phút).

## Philosophy/Business wisdom (single video, e.g. Inamori Kazuo book review) — thêm 2026-09-05

Áp dụng khi user gửi video review sách triết lý kinh doanh, bài học cuộc sống từ doanh nhân (Inamori Kazuo, Konosuke Matsushita, v.v.). Đây là style THỨ TƯ: khác tâm lý, macro, science-interview. Case: Inamori Kazuo review (YxaOH8rzwAk, ~37 phút, vi auto-gen).

- **Thesis-driven + practical wisdom**: tìm luận điểm xuyên suốt (vd Inamori: "Không có công việc nào sinh ra đã vĩ đại, chỉ có sự tận tâm cực đoan mới biến tầm thường thành kiệt xuất" / "Đào một giếng sâu, tìm thấy cả đại dương" / "Làm việc là đạo lý cao đẹp, hình thức tu hành vĩ đại"). Dựng bài quanh các thesis này, KHÔNG tóm theo chương sách.
- **Mỗi thesis lớn mở bằng TIÊU ĐỀ block riêng** (tách `\n\n` = 1 reply riêng). KHÔNG dùng "Tầng 1/2". Title kiểu "Không có công việc nào sinh ra đã vĩ đại", "Đào một cái giếng thật sâu", "Sáng tạo là 1% tốt hơn hôm qua", "Làm việc nhiều hơn, không phải ít đi" — lấy từ ẩn dụ/story trong transcript.
- **Story + quote nguyên văn**: Kepler đo thùng rượu (science case), Inamori xưởng gốm bùn đất, thợ mộc/bán phở thành bậc thầy, lập trình viên code không lỗi, tiền thuế xây bệnh viện — chi tiết cụ thể, quote nguyên văn câu đắt.
- **Transcript auto-gen tiếng Việt nhiễu**: đọc TOÀN BỘ bằng python slice (~19K ký tự/lần), phục hồi thuật ngữ theo ngữ cảnh (đừng quote bản rối).
- **Kết bằng punchline thực thi**: "Sứ mệnh nằm ngay dưới bàn tay — trong dòng code, tờ báo cáo, bát phở, viên gạch. Yêu lấy nó. Đào giếng sâu. 1% mỗi ngày. Mồ hôi bạn rơi, nơi nào đó đang nuôi sống một đời người."

- **Thesis-driven**: tìm luận điểm xuyên suốt (vd Tao: "khái niệm toán phát minh vì tò mò, vài chục năm sau thành ngôn ngữ chính xác mô tả thực tại" = unreasonable effectiveness of mathematics). Dựng bài quanh nó, KHÔNG tóm theo mạch chương (chapter 1 → chapter 2 → chapter 3).
- **Mỗi phần lớn mở bằng TIÊU ĐỀ block riêng** (tách `\n\n` = 1 reply riêng, đúng quy ước 01/09). KHÔNG dùng cụm "Tầng 1/2". Title kiểu "Xếp cam thành tiền tỷ", "Trực thăng đưa thẳng tới thác nước" — mở theo phép ẩn dụ/story trong transcript, không khô khan.
- Ưu tiên kể bằng chi tiết/story nội tại (Kepler đo thùng rượu, sphere packing → viễn thông không dây, compressed sensing → MRI nhanh) + quote con số nguyên văn (74% hiệu quả xếp cam, phỏng đoán Kepler giải 1998/kiểm chứng 2014).
- Video 37-60 phút => transcript 30-90K chữ. Đọc TOÀN BỘ bằng python slice theo mốc ~19K ký tự (`print(t[0:19000])`, `t[19000:38000]`, ...). Đừng read_file theo line (full_text không newline).
- Kết bằng quote người thật (vd Bohr "chuyên gia là người đã phạm mọi sai lầm...") làm punchline khi tale nói về failure/process.

## Bắt buộc trước khi gửi bài cho user duyệt

1. **Đọc TOÀN BỘ transcript** (`--text-only`, dùng `tail` nếu dài). User chê 2 lần vì viết từ vài dòng đầu: "nghe nông cạn thế, em đã đọc toàn bộ transcript để xử lý chưa", "em đi sâu hơn đi vẫn nông cạn".
   - **Transcript dài bị truncate trong terminal output** (vd podcast 65K chars): output tool trả `full_output_path` trỏ tới `~/AppData/Local/hermes/cache/terminal-output/out-*.log` + `truncation_note`. Đừng chạy lại lệnh. Parse thẳng file đó để lấy phần giữa bị cắt:
     ```python
     import io, json
     raw = io.open(r'<full_output_path>', encoding='utf-8').read()
     marker = raw.find('__HERMES_CWD')          # marker cuối file, cắt trước nó
     js = raw[:marker] if marker != -1 else raw
     data = json.loads(js[js.find('{'):js.rfind('}')+1])
     t = data['full_text']
     # lấy đoạn giữa bằng find() hai mốc nội dung, in ra từng phần
     ```
     PITFALL: `raw.rfind('}')` trên toàn bộ file (không cắt marker) → `JSONDecodeError: Extra data` vì marker `__HERMES_CWD_...` nằm sau JSON. LUÔN cắt marker trước.
2. **Chạy qua humanizer skill** (skill `humanizer`, port từ blader/humanizer v2.5.1): bỏ em dash, bỏ emoji, bỏ boldface máy móc, tránh AI vocabulary (crucial, pivotal, delve, vibrant, showcase, testament, underscore, enhance, fostering, key, additionally), tránh rule of three, tránh negative parallelism ("không chỉ X mà là Y"), tránh staccato drama (chuỗi câu ngắn cắt khúc), tránh aphorism sáo ("X là Y của Z"), tránh persuasive authority tropes ("câu hỏi thật là", "vấn đề cốt lõi là"), tránh signposting ("hãy cùng tìm hiểu"), tránh filler, tránh vague attribution (không nói "các chuyên gia cho rằng" không nêu tên), kết bằng chi tiết cụ thể/câu hỏi thật, thêm biến thiên độ dài câu.
   - **Chạy tool kiểm tra thực tế**: `python "C:/Users/NTQUANG_DELL/AppData/Local/hermes/scripts/unslop_check.py" <draft.txt>` (chú ý full Windows path, không dùng `~`). Output: Hard (humanizer) OK + structure scan. Soft flags như `opener_repetition`, `sentence_burstiness` → PASS nhưng ghi chú "kiểm tra giọng, không chặn" — đọc lại nếu số quá thấp (< 0.3) nhưng không bắt buộc viết lại.
3. **Kiểm tra accent tiếng Việt** bằng script đếm ký tự có dấu (nếu < 20 → viết lại).
4. **Chunk 500 ký tự cắt tại câu** bằng `scripts/chunk_500.py <draft.txt>` (kèm trong skill): đếm dấu + em dash + emoji, rồi tách part ≤ 500 ký tự tại ranh giới câu. Draft ~6900 chars → ~17 parts, max ~493.
   - **Part cuối nhỏ (< 150 chars) là OK, đừng gộp**: cắt theo câu thuần, part cuối có thể chỉ 70-110 chars (case systems thinking part 17 = 102, charisma part 12 = 70). Gộp sẽ làm part trước vượt 500. Bài trước trong queue cũng có part nhỏ tương tự — không phải lỗi.
5. **Gửi draft cho user duyệt**. KHÔNG tự thêm queue, KHÔNG tự post khi chưa có "ok". User OK → mới lưu vào `youtube-schedule.json` + `youtube-processed.json` (chống trùng link).

## Schedule Queue

File: `C:\Users\NTQUANG_DELL\AppData\Local\hermes\cache\youtube-schedule.json`

### K-Flow Schedule Viewer (user-facing)

Built 2026-07-26, user reviews pending posts here:

- **Page**: `http://localhost:3003/schedule` (tab "📅 Lịch" in K-Flow nav, added to `TopBar.tsx`)
- **API**: `GET http://localhost:3003/api/schedule?filter=pending` (or `?filter=all`) — reads `youtube-schedule.json` directly, returns `{queue: [...]}`
- **Route files**: `~/knowledge-flow/src/app/schedule/page.tsx` + `schedule-client.tsx`, `~/knowledge-flow/src/app/api/schedule/route.ts`
- If the page shows 500 but the API works, it's usually a client-component/Turbopack issue — check `schedule-client.tsx`; the API route is the reliable source.
- K-Flow runs on port 3003 via `npx next dev -p 3003` (background).

### Date Calculation Rule

1. Read ALL `scheduled_date` values in the queue; `next_date = max(dates) + 1` (thực tế code dùng `max(last_dates)` trên mọi item, không chỉ item cuối)
2. New date = that date + 1
3. If new date = today AND current time >= 20:00 -> post immediately
4. If new date = today AND current time < 20:00 -> schedule 20:00 today
5. If new date > today -> schedule 20:00 that day
6. **Duyệt NHIỀU bài cùng lúc**: giữ biến `nxt` tăng dần trong vòng lặp add — bài 1 = max+1, bài 2 = max+2, ... (đã dùng cho batch 2 bài 2026-08-15 → 22-10 + 23-10). KHÔNG tính lại max từ queue sau mỗi item (queue chưa đổi cho tới khi flush cuối).

### Queue JSON Format

```json
{
  "last_posted_date": "2026-07-15",
  "queue": [
    {
      "id": "videoId-YYYYMMDD",
      "title": "Title",
      "url": "https://youtu.be/...",
      "scheduled_date": "2026-07-16",
      "status": "pending",
      "content": "Summary text..."
    }
  ]
}
```

## Threads Posting (Playwright)

Script: `~/AppData/Local/hermes/scripts/threads_poster.py`
Session cookies: `~/.hermes/threads_state.json`

### Key Technical Details

- **Ctrl+Enter** to submit (clicking Post button is unreliable on Threads web)
- **Reply chain**: post part 1 as main, then reply to that post with parts 2+
- **Make editor visible**: on subsequent replies, the editor may be hidden by React. Use JS `evaluate()` to set `editor.style.position = 'static'; editor.style.opacity = '1';` before `fill()`
- **Editor detection**: after clicking Reply, wait for 2nd contenteditable to appear. Use `page.locator('[contenteditable="true"]').all()` and take `editors[-1]`
- **Force click**: use `click(force=True)` if overlay intercepts pointer events
- **Session**: login once via `threads_login.py` (interactive), then cron uses saved cookies

### Script Locations

- `threads_poster.py`: publishes content to Threads
- `threads_login.py`: one-time login to save session cookies
- `youtube-scheduler.py`: cron job script that reads queue and calls threads_poster.py

### Threads Login Flow

1. Open `threads.com/login`
2. Fill `input[placeholder="Username, phone or email"]` and `input[placeholder="Password"]`
3. Click `div[role="button"]:has-text("Log in")`
4. Handle post-login dialogs (Save info, Not Now, etc.)
5. Navigate to `threads.com`, save cookies to `threads_state.json`

## YouTube Metadata & Transcript Fallbacks

**Script location (verified 2026-08)**: `fetch_transcript.py` KHÔNG còn nằm trong `~/AppData/Local/hermes/scripts/` nữa. File thật nằm trong bundled skill:
`C:/Users/NTQUANG_DELL/AppData/Local/hermes/hermes-agent/skills/media/youtube-content/scripts/fetch_transcript.py`
Gọi: `python "C:/Users/NTQUANG_DELL/AppData/Local/hermes/hermes-agent/skills/media/youtube-content/scripts/fetch_transcript.py" <VIDEO_ID>`

When `fetch_transcript.py` fails (rate-limit, 0 segments, disabled transcript):

1. **Title lookup — oEmbed first**: `curl -sL --max-time 10 "https://www.youtube.com/oembed?url=<url>&format=json" -H "User-Agent: Mozilla/5.0"` → JSON with `title` + `author_name`. Nếu oEmbed trả rỗng (đã xảy ra với `LNSvp-9b-J0`), fallback: `curl -sL "https://www.youtube.com/watch?v=<ID>" | grep -oP '<title>[^<]+'`.
2. **Transcript — youtube_transcript_api trực tiếp** (dùng khi fetch_transcript.py trả `Segs: 0`, như case `jfL-KzUIxq4` — video Việt):
   ```python
   import sys, os
   sys.path.insert(0, os.path.expanduser(r'~/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages'))
   from youtube_transcript_api import YouTubeTranscriptApi
   api = YouTubeTranscriptApi()
   tr = api.list('VIDEO_ID').find_transcript(['vi', 'en'])
   data = tr.fetch()
   text = ' '.join(x.text for x in data)   # BẮT BUỘC dùng .text attribute
   ```
   PITFALL: `data` items là `FetchedTranscriptSnippet`, KHÔNG subscriptable — `x['text']` lỗi `'FetchedTranscriptSnippet' object is not subscriptable`. Dùng `x.text`.
   - **Lỗi "No transcript found. Try specifying a language with --language."** (case `js4N6KwRzBg`, `5RbEyB5zuKQ`, `VumDCWjI8a8` — video Việt, đã verify 3/3): KHÔNG phải hết transcript. List langs trước để xem có gì:
     ```python
     tr = api.list('VIDEO_ID')
     for t in tr: print(t.language_code, t.is_generated)
     # vi True → auto-generated tiếng Việt, vẫn fetch được
     data = api.list('VIDEO_ID').find_transcript(['vi']).fetch()
     ```
   - **Transcript auto-generated tiếng Việt rất nhiễu**: sai chính tả hàng loạt (waterfall → "waterfone", SME → "SMI", founder → "founder"), tên riêng và thuật ngữ phải phục hồi theo ngữ cảnh. Đọc kỹ toàn bộ trước khi viết draft, đừng quote nguyên văn từng từ bị sai — dựng lại đúng thuật ngữ (VD: "premeditatio malorum", "maranasati" đều là tái tạo từ transcript rối).
   - **Transcript auto-generated TIẾNG ANH cũng nhiễu tên riêng (2026-09-03)**: pitfall trên không chỉ riêng tiếng Việt. Case Terence Tao transcript EN interactive: Eugene Wigner → "Eugene RNA", Bernard Riemann → "Bernard Roman"/"Romian", Tycho Brahe → "Eritrea Brahe", Niels Bohr → "Neil B", Leibniz → "Lipets". PHẢI phục hồi tên người/khái niệm theo ngữ cảnh trước khi trích trong draft; đừng quote nguyên văn bản rối (sẽ bung tên sai lên bài viết).
3. **Kiểm tra trước khi gửi duyệt**: đếm accent tiếng Việt (dấu < 20 → viết lại) VÀ đếm em dash (`c.count('\u2014') + c.count('\u2013')` phải = 0). Cả hai trong cùng 1 lệnh python trước khi gửi draft cho user.

## Khôi phục draft từ cron job (khi user duyệt "ok" nhưng draft bị truncate trong reply)

Khi cron 07:30 gửi draft vào chat, tin nhắn bị truncate (chỉ thấy preview). User reply "ok" nhưng bạn không có full text. Cách lấy lại:

1. **Kiểm tra `~/hermes-temp/draft_*.txt` trước** — cron prompt yêu cầu lưu draft vào đây (vd `draft_loss_aversion.txt`). Đọc thẳng file.
2. Nếu không có file: `session_search(query="cụm từ đặc trưng trong draft")` → kết quả lớn được persist vào `~/AppData/Local/hermes/cache/terminal/hermes-results/call_*.txt`. Đọc file đó, parse JSON `data['results'][0]['messages']`, tìm message có `role == 'assistant'` và chứa `DRAFT`/`BÁO CÁO`, in `msg['content']`.
3. Lưu content vào `write_file` (KHÔNG heredoc — mất dấu tiếng Việt), rồi đếm accent trước khi add queue.
4. Nếu draft có header/footer (báo cáo, nguồn), strip phần `---` đầu và cuối, chỉ giữ nội dung post.

## Business / valuation / money content (style THỨ NĂM) — thêm 2026-10-18

Áp dụng khi video về định giá doanh nghiệp, phụ thuộc người sáng lập, mua bán công ty, unit economics (case: Roland Frasier `_cjjea6LXE4`). Khác hoàn toàn tâm lý/macro/science.

- **Không ép cơ chế thần kinh vào.** Chất liệu là con số, hệ số, cấu trúc tổ chức, thương vụ thật.
- **Giữ con số nguyên văn, đây là phần đắt nhất**: multiple 2-3x / 4-6x / 6-8,5x EBITDA, "$1M lợi nhuận → $2,5M vs $4,5M", tên nguồn số liệu (Value Stats). Sai một con số là mất cả bài.
- **Gọi tên cơ chế bằng tên gốc tiếng Anh trong ngoặc kép** khi nó là thuật ngữ tác giả tự đặt ("the myth of unlimited capacity", bài kiểm tra cái tổ), rồi gloss 1 câu.
- **Nhịp bài**: hook ngược đời → tác giả là ai (số thương vụ, số năm) → cơ chế → con số → framework → ví dụ cụ thể → hệ quả lớn nhất → 4 việc làm được → câu hỏi chốt.
- **Cầu nối bản địa 1 block**: áp vào doanh nghiệp gia đình VN (mặc định một người nắm hết, không ai gọi đó là vấn đề cho tới lúc muốn bán). Loại bài này Quang dùng trực tiếp nên cầu nối đáng giữ.

## Hai gate bắt buộc trước khi viết (thêm 2026-10-18)

**1. Gate nguồn — nói rõ nguồn là gì, ngay trong bài.** Trước khi draft, xác định loại nguồn và ghi thẳng vào bài:
- Nghiên cứu / sách có nguồn (Thinknetic, Value Stats) → được gọi là dữ liệu, nêu tên nguồn.
- **Ghi chép cá nhân của người làm video** (case MikeAnti brainmaxxing: "5-6 năm ghi chép cá nhân") → PHẢI nói rõ là ghi chép cá nhân, KHÔNG gán cho nghiên cứu. Tinh thần `số không nguồn = không số`.
- **Video kết bằng CTA/upsell** (bán tool, khoá học, newsletter) → nói 1 câu cho minh bạch: "cuối video ông mời người xem làm một công cụ của chính ông. Phần nội dung mình kể, phần mời gọi mình bỏ qua." Mẫu câu này đã dùng và được giữ.

**2. Gate trùng vùng chủ đề.** Trước khi viết, quét `title` của queue trong cửa sổ ~3 tháng quanh ngày đăng dự kiến với danh sách keyword của chủ đề (vd `não, học, chú ý, hiệu suất, memory, focus, thói quen`).
- Trùng 1-2 bài → chọn **góc KHÁC hẳn**, không chỉ đổi tiêu đề: bỏ hẳn phần mà bài cũ đã nói, giữ phần chưa ai nói. Case brainmaxxing: queue đã dày vùng não/học (Daniel Pink fix attention span 21/01, "Stop Studying Like This" 12/01, Huberman hard work 08/01, Flow 20/12) → góc chọn là "bỏ qua hết phần ngủ/ăn/supplement, tập vào 5 việc không ai làm" + nhấn "nghỉ làm sai" và "não không tắt".
- Báo cho user biết đã check và chọn góc gì — Quang đọc phần này để duyệt.
- Vùng chủ đề dày cũng là lý do để **cắt block** cho vừa trần 7K (xem dưới).

## Trần độ dài: 3-7K chars — đừng phát hiện muộn

Draft Threads phải nằm trong **3.000-7.000 chars**. Bài business/valuation đầu tiên viết ra 10.524 chars và phải cắt qua ~10 lượt — đó là lỗi budget, không phải lỗi viết.

- `write_file` trả `bytes_written`; với tiếng Việt có dấu **chars ≈ bytes / 1,32**. 9.200 bytes ≈ 7.000 chars. Check ngay con số này sau mỗi lần write, không cần gọi thêm tool.
- ~7.000 chars ≈ **30-35 block** (mỗi block ~2 câu, 200-230 chars). Outline quá 35 block là chắc chắn vượt trần → cắt ở outline.
- Quá trần **hơn 15% thì XOÁ NGUYÊN BLOCK, đừng viết lại câu**. Đo thật: 5 lượt reword chỉ lấy lại ~10%; xoá 3 block lấy lại ~25% trong 1 lượt.
- Thứ tự xoá: transition filler → quan sát phụ → caveat → gloss của quote đã gloss → aside về thời điểm/nỗ lực → câu thứ hai của một định nghĩa.
- KHÔNG xoá: quote nguyên văn, con số, attribution nguồn, câu nói rõ nguồn, cầu nối bản địa, câu hỏi chốt.
- Chi tiết đầy đủ (bảng budget theo cửa sổ, skeleton 30 block, thứ tự xoá có xếp hạng): skill `content-length-trimming`, `references/vietnamese-draft-length-budget.md`.
- Gate verify 1 lệnh duy nhất: `python "C:/Users/NTQUANG_DELL/AppData/Local/hermes/skills/productivity/content-length-trimming/scripts/draft_metrics.py" <draft.txt> 3000 7000` — in CHARS/ACC/EMDASH/CJK/TOI/PARTS-MAX và FAIL nếu lệch cửa sổ, có em dash, có CJK, có chữ "tôi" ngoài quote, hoặc part > 500. Thay cho việc tự viết lại script đếm mỗi phiên.

## Pitfalls

- **MSYS `~` path breaks Python (Windows)**: terminal chạy qua git-bash; `python ~/AppData/...` expand `~` thành `/c/Users/...` → Python báo `can't open file 'C:\\c\\Users\\...'`. LUÔN dùng full Windows path: `python "C:/Users/NTQUANG_DELL/AppData/Local/hermes/..."`.
- **Philosophy/Business wisdom videos**: transcript tiếng Việt auto-gen rất nhiễu tên riêng/thuật ngữ (Inamori→"Inam Mary", "quốc"→"cuốc/sẻng"). BẮT BUỘC đọc TOÀN BỘ bằng python slice, phục hồi theo ngữ cảnh TRƯỚC khi viết draft. Đừng quote nguyên văn bản rối.
- **`/tmp` KHÔNG tồn tại với Python Windows**: redirect output ra `/tmp/x.json` → `FileNotFoundError`. Ghi ra `D:/Hermes/tmp/` (đúng disk policy ổ D): `mkdir -p "D:/Hermes/tmp"` trước khi redirect.
- **Transcript file 1 dòng dài → read_file vô dụng**: full_text không có newline, read_file theo line trả rỗng (vd `offset=400` → rỗng). Phải đọc bằng python slice: `t = io.open(path, encoding='utf-8').read()` rồi `print(t[a:b])` với mốc `t.find('...')`.
- **Check processed đừng dùng grep -c**: ID nằm cả `video_ids` lẫn `urls` → `grep -c` trả **2** gây hiểu lầm "đã xử lý". Dùng python: `print(ID in d['video_ids'], any(ID in u for u in d['urls']))`. Nếu đã processed nhưng chưa thấy trong queue (case cron-jung-act-as-if `qkeaDSX-ssQ`), báo user "đã xử lý, đang chờ đăng" — đừng làm lại.
- **Quét queue tìm video trùng PHẢI None-safe (2026-09)**: vài item trong queue (nhất là `youtube-schedule.json`) có `url=None`. `VID in x.get('url','')` hoặc `[dict...]` với loop không bảo vệ → `TypeError: argument of type 'NoneType' is not iterable`, script chết giữa chừng (vụ này tốn 2 lần chạy). Luôn viết: `u = str(x.get('url') or ''); i = str(x.get('id') or '')`, kèm `if not isinstance(x, dict): continue` trước khi đụng field. Pattern an toàn cho cả 3 queue (psych/hll/macro) trong cùng 1 lệnh scan.
- **`write_file` từ chối content dạng bảng `N|...` (2026-08-27)**: khi viết một file playlist/channel index dạng cột `1|id|title|min` (giống output read_file), tool báo `Refusing to write internal read_file display text as file content` và trả về lỗi. ĐÂY LÀ TOOL GUARD, không phải lỗi script. Fix: viết nội dung dạng JSON hoặc markdown thuần (không có tiền tố `STT|` đầu dòng), hoặc tạo file qua `execute_code` `json.dump`. Liên quan playlist: luôn lưu playlist dưới dạng JSON (`mit-14.02-playlist.json`) chứ không phải file bảng text.
- **`fill()` on hidden editor**: Threads reply editor opens hidden on second+ reply, AND the Lexical editor rejects `fill()`/`evaluate(textContent)` for replies (content silently drops even when "Posted!" shows). Fix for replies: `editor.click(force=True)` then `page.keyboard.type(text, delay=5)` + `Ctrl+Enter`. `fill()` is only reliable for the main compose box. See `references/threads-playwright.md`.
- **Post button not working**: Use Ctrl+Enter instead of clicking Post button. Threads web's Post button may be intercepted by overlay divs.
- **Session expires**: Threads cookies expire periodically. Run `threads_login.py` again to refresh.
- **Rate limiting**: If multiple replies fail silently, add longer waits (5s+) between replies.
- **YouTube transcript limit**: Some videos have transcripts disabled. Skip and pick another.
- **DDG Lite blocking**: CAPTCHA blocks automated search after a few queries. Use Wikipedia API as fallback.

## Reference Files

- `references/parallel-content-channel.md` — Song song channel recipe (macro, podcast)
- `references/philosophy-business-wisdom.md` — Inamori Kazuo style details
- `references/podcast-channel-ingest.md` — Podcast ingest (HLL channel)
- `references/telegram-group-session-recovery.md` — Khi session Telegram group bị treo trên clarify: xử lý độc lập, gửi kết quả qua Bot API, flow + code + pitfalls
- `references/threads-playwright.md` — Threads Lexical editor workarounds
- `references/yt-dlp-playlist.md` — Playlist processing with yt-dlp

## Verification

After posting, verify by:
1. Checking `threads.com/@ntquang1110` for new posts
2. Searching for key phrases from the summary in the page text
3. Ensuring reply chain format (main + replies, not separate posts)
