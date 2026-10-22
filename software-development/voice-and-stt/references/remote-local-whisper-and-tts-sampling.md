# Remote local Whisper (Mac) + TTS voice sampling — 2026-09 test

Verified 2026-09-04 on Mac mini M1 / 16GB. Reusable recipe for (a) deploying a
standalone local Whisper on a *remote* box and driving it from Windows, (b)
generating + verifying Vietnamese TTS voice samples.

## Contexte: hai "local" khác nhau

`voice-and-stt` SKILL.md nói về STT *của Hermes* chạy trong venv của Hermes trên
chính máy host. Đây là *node riêng* (Mac-mini 192.168.1.3) chạy Whisper local độc
lập, gọi từ xa qua SSH. Đừng gộp chung bước cài vào venv Hermes.

## 1. Chọn model whisper theo RAM (không theo "to nhất tuỳ tiện")

| Model | RAM khi transcribe | Download | Chất lượng VI |
|-------|--------------------|----------|---------------|
| small | ~2GB | 466MB | Khá |
| medium| ~5GB | 1.5G | Tốt |
| large-v3 | ~10GB | 2.9G | Tốt nhất |

Máy 16GB → `large-v3` chạy ổn (cần ~10GB). Máy 8GB chỉ nên `medium`. Khi user nói
"cài model nặng nhất phù hợp" → check RAM trước (`sysctl -n hw.memsize`), rồi chốt.

## 2. Deploy local Whisper trên remote (M1, macOS)

```bash
# tách venv riêng, KHÔNG đụng system python (macOS 3.9)
[ -d ~/whisper-venv ] || python3 -m venv ~/whisper-venv
~/whisper-venv/bin/pip install --upgrade pip -q
~/whisper-venv/bin/pip install faster-whisper -q   # kéo ctranslate2

# model large-v3 (~2.9G) vào ~/.cache/huggingface — chỉ tải lần đầu
~/whisper-venv/bin/python -c \
 "from faster_whisper import WhisperModel; m=WhisperModel('Systran/faster-whisper-large-v3', device='cpu', compute_type='int8')"
```
M1 không có CUDA → `device='cpu'`, `compute_type='int8'` là đường ổn định.

### Script driver `run_whisper.py` (đặt trên remote)
```python
from faster_whisper import WhisperModel
m = WhisperModel(f"Systran/faster-whisper-{args.model}", device="cpu", compute_type="int8")
segments, info = m.transcribe(args.audio, language=args.lang, beam_size=5)
# in text nối, hoặc --json đưa segments [{start,end,text}]
```
Args: `<audio>` bắt buộc, `--lang` (bỏ = auto-detect, `vi` ép tiếng Việt),
`--json`, `--model` (mặc định `large-v3`).

### Test nhanh trên Mac bằng `say`
```bash
say -o test_en.aiff "Hello, transcription test"   # giọng Anh OK
```
⚠️ **`say` mặc định đọc tiếng Việt SAI** (voice tiếng Anh đọc phonetic của chữ VN).
Muốn test tiếng Việt thật → dùng file audio VN có sẵn hoặc edge-tts giọng VN, đừng
dùng `say` cho VN rồi đổ lỗi Whisper.

## 2b. Whisper HTTP server trên Mac (launchd, port 9000) — endpoint ĐÚNG

Ngoài driver CLI ở mục 2, Mac còn chạy **whisper_server.py** qua launchd, nghe ở
`http://192.168.1.3:9000`. Gọi từ Windows bằng curl (không cần SSH/paramiko).

**Endpoint đúng là OpenAI-compatible: `POST /v1/audio/transcriptions`.**

```bash
curl -s -F "file=@C:/Users/NTQUANG_DELL/AppData/Local/hermes/cache/audio/audio_xxx.ogg" \
     -F "model=whisper-large-v3" -F "language=vi" \
     "http://192.168.1.3:9000/v1/audio/transcriptions"
# → {"text": "<transcript>", "duration": 17.06, "language": "vi"}
```

| Path | Kết quả |
|---|---|
| `POST /v1/audio/transcriptions` | ✅ 200, OpenAI-style `{text, duration, language}` |
| `POST /inference` | ❌ `{"detail":"Not Found"}` — **đừng dùng**, đây không phải route của server này |

Transcribe voice message Telegram: file đã nằm sẵn ở
`C:/Users/NTQUANG_DELL/AppData/Local/hermes/cache/audio/audio_<hash>.ogg` — trỏ
`file=@` thẳng vào đó, không cần convert/boost trước (server tự xử lý; boost chỉ
cần khi đẩy lên Groq — xem mục quality tuning trong SKILL.md).

Chỉ lấy field `text` ra, đừng in nguyên JSON:
```bash
... | python -c "import sys,json; print(json.load(sys.stdin)['text'])"
```

## 3. Windows → Mac qua paramiko (sshpass/expect KHÔNG có trên git-bash)

Trên git-bash (Windows) không có `sshpass` cũng không có `expect` để nhập password
SSH tự động. Key rất có thể bị từ chối nếu chưa push. Lối đi đáng tin: **paramiko**.

```bash
python -m pip install paramiko   # ⚠️ dùng `python -m pip`, không `pip boxed`
```
Pitfall môi trường Windows này: `pip` (bare) trỏ về python **3.14**, còn `python`
là **3.11**. Luôn `python -m pip install X` rồi kiểm `python -c "import X"`.

```python
import paramiko
c = paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(host, username=user, password=pw, timeout=15)
sftp = c.open_sftp()
sftp.put(src, dst)          # upload file audio / script lên remote
sftp.close()
script = "set -e\n<bash commands>"
stdin,stdout,stderr = c.exec_command("bash -s", timeout=900)
stdin.write(script); stdin.channel.shutdown_write()
data = stdout.read().decode(errors="replace")   # đọc hết ở cuối
c.close()
```
- Trù password/host vào một file python gọi phụ, đừng lặp lại trong từng command.
- `timeout` cao cho download model / transcribe dài.
- Gửi script qua `bash -s` + heredoc để chạy nhiều lệnh trong MỘT phiên SSH.
- **Pitfall:** đừng `readline()` streaming trong khi stdout define str/bytes — dùng
  `read()` hết rồi xử lý. (Lỗi `can't concat str to bytes` dính trong session.)

## 4. edge-tts — giọng tiếng Việt miễn phí, không cần key

Chiếc Windows này: `python -m pip install edge-tts` (v7.x OK).

**Chỉ có 2 giọng tiếng Việt trên edge** (đừng đoán nhiều hơn):
- `vi-VN-HoaiMyNeural` — nữ, "Online (Natural)"
- `vi-VN-NamMinhNeural` — nam, "Online (Natural)"

Liệt kê: `edge_tts.list_voices()` lọc `v["ShortName"].startswith("vi-VN")`.
Sinh mẫu:
```python
import asyncio, edge_tts, os
async def main():
    await edge_tts.Communicate("Xin chào, đây là giọng tiếng Việt.", "vi-VN-HoaiMyNeural", rate="+0%").save("hoaimy.mp3")
asyncio.run(main())
```
Hai giọng này chính là **Azure Neural voice**, free qua edge — một sample audio duy
nhất cho cả 2 nguồn (edge/azure).

## 5. Google Gemini TTS tiếng Việt (đã có GOOGLE_API_KEY)

`sử dụng text_to_speech provider='gemini'` (config `gemini.model: gemini-2.5-flash-preview-tts`)
nói tiếng Việt chuẩn — nhưng cần **instructions** rõ: "Speak natural warm Vietnamese, Southern accent".
Chạy được ngay vì có `GOOGLE_API_KEY` (không cần key mới).
Các provider cần key riêng KHÔNG có trong env hiện tại: ElevenLabs, Azure, Mistral,
OpenAI-direct. Kiểm trước khi hứa sinh mẫu.

## 6. Verify một audio TTS — transcribe ngược qua Whisper

Cách chắc ăn kiểm tra TTS thật sự nói đúng text/ngôn ngữ: transcribe BẢN THÂN file
audio vừa sinh bằng Whisper (local/Mac hoặc Groq) với `--lang vi`. Khớp ~100% →
giọng chuẩn. Dùng chính pipeline local vừa deploy để verify TTS → 2 việc trong 1.
(Pitfall: `mutagen` chưa cài trên venv remote thì `.info.length` fail — không sao,
whisper vẫn transcribe mp3 trực tiếp.)

## Tóm tắt luồng chọn giọng TTS tiếng Việt cho user
1. Kiểm env có key provider nào (edge free, GOOGLE_API_KEY, ELEVENLABS?, MISTRAL?).
2. Sinh audio sample CÙNG MỘT đoạn text cho từng giọng có sẵn.
3. Transcribe ngược để xác nhận đúng tiếng Việt.
4. Gửi MEDIA: mẫu cho user nghe duyệt; research landscape (giá/chất lượng) chạy
   song song qua subagent → bảng khuyến nghị.