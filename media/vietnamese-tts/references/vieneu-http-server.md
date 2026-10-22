# Serve VieNeu TTS qua HTTP (app khác gọi giọng đã chốt) — recipe đã verify 07/09/2026

Bối cảnh: giọng VieNeu chạy local trên Mac (192.168.1.3), nhưng app cần giọng (TFO trên
Windows) nằm máy khác. Giải pháp: micro HTTP server trên Mac nhận `GET /tts?text=...` →
`tts.infer(voice="Thanh Bình")` → trả WAV. App gọi qua LAN, giữ edge làm fallback.

## 1. Script micro server (Mac, port 8899)

```python
# /Users/tquang/tts_server.py — chạy: nohup ~/vieneu-venv/bin/python tts_server.py &
import io, sys, os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
# BẮT BUỘC: thêm site-packages của vieneu-venv (venv riêng Python 3.11)
for base in ["/Users/tquang/vieneu-venv/lib/python3.11/site-packages"]:
    if base not in sys.path:
        sys.path.insert(0, base)
from vieneu import Vieneu
tts = Vieneu()          # lần đầu tải model ~vài giây (HF Hub), log Warning HF_TOKEN là bình thường
VOICE = "Thanh B\u00ecnh"  # dấu đúng: "Thanh Bình" — NẾU deploy qua heredoc/paramiko, escape unicode để khỏi mất dấu
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        text = (q.get("text") or [""])[0]
        if not text:
            self.send_response(400); self.end_headers(); return
        try:
            audio = tts.infer(text, voice=VOICE)
            import tempfile
            tmp = tempfile.mktemp(suffix=".wav")
            tts.save(audio, tmp)               # tts.save nhận PATH, không nhận BytesIO
            data = open(tmp, "rb").read(); os.unlink(tmp)
            self.send_response(200)
            self.send_header("Content-Type", "audio/wav")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers(); self.wfile.write(data)
        except Exception as ex:
            import traceback; traceback.print_exc()
            msg = str(ex).encode("utf-8")[:300]
            self.send_response(500); self.send_header("Content-Length", str(len(msg)))
            self.end_headers(); self.wfile.write(msg)
HTTPServer(("0.0.0.0", 8899), H).serve_forever()
```

- Lần đầu `Vieneu()` init: chờ 3-8s; curl sớm quá trả HTTP:000 → retry vài lần, đừng tưởng server chết.
- Port mở `0.0.0.0` để máy khác trên LAN gọi; test local `curl http://127.0.0.1:8899/tts?text=...` (URL-encode, giữ dấu).

## 2. Python provider phía app (Windows) — mặc định Thanh Bình, edge fallback

```python
class VieNeuProvider:
    BASE = "http://192.168.1.3:8899"
    async def _synth_async(self, text):
        import httpx, urllib.parse
        r = await httpx.AsyncClient(timeout=60).get(f"{self.BASE}/tts?text=" + urllib.parse.quote(text))
        if r.status_code != 200:
            raise RuntimeError(f"VieNeu HTTP {r.status_code}: {r.text[:200]}")
        return r.content   # WAV bytes
```

Pattern fallback (đã dùng trong TFO `_answer_and_speak`): thử VieNeu → ngoại lệ → `get_edge()` synth; app luôn sống dù Mac chết.

## 3. Pitfall: VieNeu trả WAV, không phải MP3

`tts.save()` xuất RIFF/WAVE. Nếu app serve file dưới tên `.mp3`, browser có thể không phát vì
content-type sai. Sniff 4 byte đầu:

```python
media = "audio/wav" if f.read_bytes()[:4] == b"RIFF" else "audio/mpeg"
```

## 4. Chống hallucinate STT: cổng tần số giọng người (FFT) trước khi gửi Groq

Triệu chứng: VAD chỉ đo RMS (năng lượng) → tạp âm/gió/hum vượt ngưỡng vẫn bị gửi Groq Whisper
→ Groq BỊA RA CHỮ khi không có giọng thật. Fix = cổng phổ trước khi transcribe:

```python
# numpy sẵn trong venv (không cần pip)
SPEECH_BAND_LO, SPEECH_BAND_HI, SPEECH_RATIO_MIN = 300, 3400, 0.55
def speech_ratio(pcm: bytes) -> float:
    n = len(pcm) // 4
    if n < 64: return 1.0
    import numpy as np
    x = np.frombuffer(pcm[:n*4], dtype=np.float32)
    x = (x - x.mean()) * np.hanning(n).astype(np.float32)   # zero-mean + hann chống rò phổ
    spec = np.abs(np.fft.rfft(x))
    freqs = np.fft.rfftfreq(n, d=1.0/16000.0)
    total = float(spec.sum())
    return 0.0 if total <= 0 else float(spec[(freqs >= SPEECH_BAND_LO) & (freqs <= SPEECH_BAND_HI)].sum()) / total
# trong flush: if rms < NOISE_RMS_HARD or speech_ratio(pcm) < SPEECH_RATIO_MIN: bỏ, KHÔNG gửi Groq
```

Verify: hum 50/100Hz → ratio ~0 (loại); sine 500/1000Hz → ratio ~1 (giữ). Giọng người thật luôn
có formant 300-3400Hz nên không bị cắt nhầm. Có đúng không: cắt đoạn ngắn (< 0.4s) vẫn bỏ trước đó.