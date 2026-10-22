# Setup local TTS/STT trên Mac-mini (192.168.1.3) — recipe đã verify

Node xử lý audio local: Mac mini M1, 16GB RAM, macOS 14.5 (Macmini9,1).
User SSH: `tquang`, pw `<PASSWORD>` (LAN nội bộ). SSH từ Windows/git-bash: không có `sshpass`, key auth fail → dùng **paramiko** kết nối bằng password.

## 1. Local Whisper (STT) — faster-whisper large-v3

- venv: `~/whisper-venv` (tạo từ python system 3.9, KHÔNG ảnh hưởng system)
- cài: `pip install faster-whisper` (đã có 1.2.1 + ctranslate2 4.8.2)
- model: `Systran/faster-whisper-large-v3` (2.9G, trong `~/.cache/huggingface/hub`), device cpu, compute_type int8
- script: `~/whisper/run_whisper.py` — args `--lang vi`, `--json`, `--model`
- chạy: `~/whisper-venv/bin/python ~/whisper/run_whisper.py <file> --lang vi`
- Verified: tiếng Anh 100%, tiếng Việt xử lý được.

Trước đó model khác đã có trong cache: `Systran/faster-whisper-small`, `faster-whisper-tiny`, `vinai/PhoWhisper-small`, `OpenMOSS-Team/MOSS-Audio-Tokenizer-Nano`, `pnnbao-ump/VieNeu-TTS-v3-Turbo` (LƯU Ý: folder HF Hub là `pnnbao-ump`, KHÔNG phải `vinai`).

## 2. VieNeu-TTS v3 Turbo (TTS tiếng Việt, 20 giọng preset)

SDK chính thức: `vieneu` (PyPI, đã cài 3.4.0). Tác giả pnnbao97, model `pnnbao-ump/VieNeu-TTS-v3-Turbo`, license apache-2.0, 48kHz, clone giọng, cảm xúc inline `[cười]`, code-switching EN-VI.

- **PHẢI có Python ≥3.10.** python system trên Mac là 3.9 → `pip install vieneu` FAIL.
  Fix: dùng `~/.local/bin/python3.11 -m venv ~/vieneu-venv` rồi cài trong venv đó.
- Device: mặc định CPU/ONNX (int8) — Nhanh hơn MPS trên Apple Silicon. Không cần PyTorch.
- Lần đầu `Vieneu()` tự tải thêm model file (speaker_encoder.onnx, model.safetensors...) vào HF cache. Cần mạng.
- **Pitfall quan trọng:** `style` arg bị deprecated/ignored trên v3 Turbo. Phong cách đọc (tự nhiên/tin tức/kể chuyện/đọc truyện) gắn sẵn TRONG từng giọng preset → chọn bằng `voice="Tên"`.
- Sinh cực nhanh trên M1: clip ngắn mỗi giọng ~4-5s (init model ~20s lần đầu).

### 20 giọng preset (đã verify qua `list_preset_voices`)
- **Bắc:** Minh Đức (nam·tin tức), Phạm Tuyên (nam·tự nhiên), Thanh Bình (nam·kể chuyện), Trúc Ly (nữ·tự nhiên), Ngọc Linh (nữ·kể chuyện), Đoan Trang (nữ·tự nhiên), Mai Anh (nữ·tin tức), Ngọc Huyền (nữ·tự nhiên), Quỳnh Anh (nữ·đọc truyện)
- **Nam:** Xuân Vĩnh (nam·tự nhiên), Thái Sơn (nam·kể chuyện), Thục Đoan (nữ·kể chuyện), Minh Triết (nam·tin tức), Thùy Dung (nữ·tin tức), Adam (nam·tự nhiên), Mỹ Duyên (nữ·đọc truyện), Đức Trí (nam·đọc truyện), Kim Thanh (nữ·đọc truyện)
- **Trung:** Quang Sơn (nam·tự nhiên), Ngọc Trân (nữ·tự nhiên)

### Sinh mẫu (đã dùng)
```python
from vieneu import Vieneu
tts = Vieneu()
for label, vid in tts.list_preset_voices(): print(label, "->", vid)
audio = tts.infer(TEXT, voice="Ngọc Huyền")
tts.save(audio, "natural.wav")
```
- Clone giọng: `tts.infer(text, ref_audio="voice.wav", denoise=True)` hoặc `tts.add_voice("Tên", "voice.wav")`.
- Streaming: `tts.infer_stream(...)` với `Vieneu(backend="onnx")`.

## 2.5 VieNeu qua HTTP LAN — Windows app gọi giọng Mac (recipe verify 07/09)

Khi app chạy trên Windows (vd TFO) cần dùng giọng VieNeu trên Mac qua mạng, KHÔNG chạy model trên Windows. **KHÔNG SSH từng lần** — deploy 1 micro HTTP server trên Mac, app gọi GET.

1. **Deploy server trên Mac** (`~/tts_server.py`, paramiko sftp đẩy lên):
```python
import sys, os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
sys.path.insert(0, "/Users/tquang/vieneu-venv/lib/python3.11/site-packages")
from vieneu import Vieneu
tts = Vieneu()
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        text = (q.get("text") or [""])[0]
        if not text: self.send_response(400); self.end_headers(); return
        try:
            audio = tts.infer(text, voice="Thanh Bình")
            import tempfile; tmp = tempfile.mktemp(suffix=".wav")
            tts.save(audio, tmp); data = open(tmp,"rb").read(); os.unlink(tmp)
            self.send_response(200)
            self.send_header("Content-Type","audio/wav")
            self.send_header("Content-Length",str(len(data)))
            self.end_headers(); self.wfile.write(data)
        except Exception:
            self.send_response(500); self.end_headers()
HTTPServer(("0.0.0.0", 8899), H).serve_forever()
```
Chạy nền: `pkill -f tts_server.py; nohup ~/vieneu-venv/bin/python /Users/tquang/tts_server.py > /tmp/tts_server.log 2>&1 &`
- Lần đầu tự tải model (log HF Hub warning), chờ rồi curl verify `HTTP:200` + size >0.
- **Tên giọng phải có dấu đầy đủ:** `voice="Thanh Bình"` — để thành `"Thanh Binh"` sẽ lỗi/disconnect.

2. **Client Windows** (`app/tts.py` `VieNeuProvider`): `httpx.AsyncClient().get("http://192.168.1.3:8899/tts?text="+urllib.parse.quote(text), timeout=60)` → `r.content` (WAV). **PHẢI `async def _synth_async`** (sync `httpx.get` trả bytes → gọi await sẽ lỗi "object bytes can't be used in await").

#### Pitfall: VieNeu ra WAV, edge ra MP3 — cache/serve đặt đuôi .mp3
VieNeu output là **WAV** (header `RIFF/WAVE`), còn edge là MP3. Nếu ghi vào cache `.mp3` và serve `media_type="audio/mpeg"`, trình duyệt fail phát khi dùng giọng VieNeu. Fix `serve /tts/{hash}`: sniff 4 byte đầu file → `audio/wav` nếu RIFF, else `audio/mpeg`.

#### Fallback khi Mac chết
`get_provider()` mặc định VieNeu. Ở tầng gọi, wrap try VieNeu → except gọi edge (truyền provider override). Giữ câu trả lời, đừng chết cả turn. Latency LAN ~2-4s câu ngắn, chấp nhận với giọng "người thật" local.

## 3. Paramiko SSH driver (từ Windows)

```python
import paramiko
c = paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("192.168.1.3", username="tquang", password="<PASSWORD>", timeout=15)
# exec_command + read; upload/download qua c.open_sftp()
```
Mẹo: gửi script bằng heredoc qua bash -s, hoặc ghi script lên remote qua sftp rồi nohup background + poll log (task dài như pip install / tải model). Nếu exec_command chạy dài, poll log bằng vòng lặp SSH. Lưu ý bug: paramiko exec_command đọc ra bytes; copy output bằng text mode dễ `TypeError: can't concat str to bytes` → đọc hết `stdout.read().decode()`.

## 4. Verify audio sinh ra

- Transcribe lại bằng Whisper local để xác nhận đúng ngôn ngữ/nội dung.
- CẢNH GIÁC: `say` (macOS TTS) đọc tiếng Việt KHÔNG chuẩn (voice mặc định người Anh đọc VN méo). `-v Ting-Ting` không tồn tại trên M1. Chỉ dùng `say` để tạo audio test tiếng Anh, KHÔNG dùng để đánh giá chất lượng tiếng Việt.

## 5. Sample text (dùng để so sánh giọng)

"Xin chào Quang. Đây là mẫu giọng tiếng Việt để anh nghe và chọn. Giọng đọc tốt truyền cảm xúc, giữ chân người nghe. Anh hãy so sánh độ tự nhiên và sự ấm áp của từng giọng, rồi quyết định dùng giọng nào cho nội dung của mình."