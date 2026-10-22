# Browser Dictation Web App — mic trình duyệt → server STT → live context

Khi user muốn dùng tính năng ghi âm/dictation NGAY trên web (không cài APK).
Đã triển khai thật 2026-08-10 cho meTelligent (`server/web/dictation.html`),
verify full flow qua tunnel: `speech:true`, context `"Mở rộng đại lý bù bán vàng"`, end-json `done`.

## Kiến trúc

```
Browser (Chrome/Safari, điện thoại/desktop):
  getUserMedia({audio: {channelCount:1, echoCancellation:true, noiseSuppression:true, autoGainControl:true}})
  → AudioContext → ScriptProcessorNode(4096, 1, 1)
  → Float32 → clamp → Int16 PCM (s<0 ? s*0x8000 : s*0x7FFF)
  → gom 5s theo rate thật → wrapWav() → FormData POST /api/meeting/chunk-live
  → text nối dần vào transcript live
  → mỗi ~450 ký tự mới (debounce 800ms) → POST /api/meeting/context → 3 ô live (title/context/decisions)
  → stop: flush PCM dư → POST /api/meeting/end-json → popup summary commit-ready + Confirm
```

Server endpoints tái sử dụng y hệt Flutter app (`chunk-live` VAD+transcribe, `context` Groq, `end-json` summary).

## Serve cùng origin (QUAN TRỌNG)

Serve HTML từ chính FastAPI server → browser gọi API relative `''` → **không dính CORS** (dù đã có CORSMiddleware `*`, cùng origin là chuẩn nhất).

```python
_DICTATION_PATH = Path(__file__).resolve().parent.parent / "web" / "dictation.html"
@app.get("/dictation", response_class=HTMLResponse)
async def dictation_web():
    return HTMLResponse(content=_DICTATION_PATH.read_text(encoding="utf-8"))
```

**Path pitfall:** nếu file HTML nằm ở `server/web/` nhưng `__init__.py` nằm trong package `metelligent/`, thì phải `.parent.parent` mới ra khỏi package dir. `.parent` (metelligent/) trỏ SAI → 404 "not found".

## PITFALL 1 — iOS Safari bỏ qua `AudioContext({sampleRate:16000})`

Context trả về rate thật (thường 44100/48000), sampleRate 16000 bị ignore. Hậu quả kép:
1. WAV header phải ghi rate THẬT (`ctx.sampleRate`), không hardcode 16000.
2. Server VAD (webrtcvad) chỉ nhận 8/16/32/48kHz → phải resample về 16k trong JS trước khi wrap.

```js
function resampleTo16k(pcm, fromRate) {
  if (fromRate === 16000) return pcm;
  const ratio = fromRate / 16000;
  const outLen = Math.floor(pcm.length / ratio);
  const out = new Int16Array(outLen);
  for (let i = 0; i < outLen; i++) out[i] = pcm[Math.floor(i * ratio)];
  return out;
}
```

## PITFALL 2 — chunk size theo rate thật, không hardcode

`160000 mẫu` = 5s ở 16kHz nhưng chỉ 3.3s ở 48kHz (chunk sai độ dài). Dùng:

```js
function chunkBytes(rate) { return rate * 2 * 5; }  // 5 giây
```

Ngưỡng bỏ chunk nhỏ cũng theo rate: `raw.length < rate` (dưới 1s bỏ).

## PITFALL 3 — ScriptProcessor vs AudioWorklet

- ScriptProcessorNode deprecated nhưng hoạt động MỌI nơi (Chrome/Safari/Firefox) — dùng cho single-file HTML.
- AudioWorklet cần file module riêng (hoặc Blob URL) — rườm, chỉ dùng khi cần low-latency thật.

## WAV wrap (JS)

```js
function wrapWav(pcm, sampleRate) {
  const buf = new ArrayBuffer(44 + pcm.length * 2);
  const v = new DataView(buf);
  const ws = (o, s) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
  ws(0, 'RIFF'); v.setUint32(4, 36 + pcm.length * 2, true); ws(8, 'WAVE');
  ws(12, 'fmt '); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true);
  v.setUint32(24, sampleRate, true); v.setUint32(28, sampleRate * 2, true);
  v.setUint16(32, 2, true); v.setUint16(34, 16, true);
  ws(36, 'data'); v.setUint32(40, pcm.length * 2, true);
  let off = 44;
  for (const s of pcm) { v.setInt16(off, s, true); off += 2; }
  return new Blob([buf], { type: 'audio/wav' });
}
```

## Luồng khởi động

1. `POST /api/meeting/start-json` {title, tags} → `meeting_id` (gọi TRƯỚC khi bật processor).
2. `ctx.createScriptProcessor(4096, 1, 1)` → `onaudioprocess` gom PCM → đủ `chunkBytes(rate)` thì `flushChunk()`.
3. `flushChunk`: splice đủ 5s → resampleTo16k → wrapWav → FormData (`meeting_id`, `chunk_index`, `file` `audio/wav`) → POST chunk-live → text.
4. `maybeContext()`: chỉ gọi khi `currentText.length - lastContextLen >= 450` và chưa có call đang chạy; debounce 800ms; cập nhật `lastContextLen`.
5. Stop: `recording=false` → flush phần dư (≥1s) → disconnect processor/source, close ctx, stop tracks → POST end-json → hiện summary.

## Test full flow qua tunnel (không tin local)

```python
import requests, struct, math
BASE = "https://<sub>.loca.lt"; H = {"bypass-tunnel-reminder": "1"}
r = requests.post(f"{BASE}/api/meeting/start-json", json={"title":"t","tags":"web"}, headers=H)
mid = r.json()["meeting_id"]
# WAV 2s tone 400Hz như JS
sr=16000; n=sr*2
pcm = b"".join(struct.pack("<h", int(8000*math.sin(2*math.pi*400*i/sr))) for i in range(n))
wav = b"RIFF"+struct.pack("<I",36+len(pcm))+b"WAVEfmt "+struct.pack("<IHHIIHH",16,1,1,sr,sr*2,2,16)+b"data"+struct.pack("<I",len(pcm))+pcm
requests.post(f"{BASE}/api/meeting/chunk-live", data={"meeting_id":mid,"chunk_index":0},
              files={"file":("c.wav", wav, "audio/wav")}, headers=H)  # expect speech:true
requests.post(f"{BASE}/api/meeting/context", data={"meeting_id":mid,"text":"..."}, headers=H)
requests.post(f"{BASE}/api/meeting/end-json", json={"meeting_id":mid}, headers=H)  # done
```

## PITFALL 4 — popup summary: nút "Xem lại" đóng popup vĩnh viễn = kẹt

Đã gặp live (2026-08-10): user bấm "Xem lại" → overlay ẩn, mất luôn nút Confirm, không có cách mở lại → "kẹt ở chỗ xem lại, không bấm được".

Fix chuẩn:
- "Xem lại" chỉ ĐÓNG popup + cuộn xuống transcript (`scrollIntoView`), KHÔNG xoá summary state.
- Thêm nút phụ **"📋 Mở tổng kết"** trên header (`hidden` mặc định) → bấm mở lại popup. Confirm ẩn nút này.
- Test bằng browser_console mô phỏng: mở popup → click Xem lại → assert overlay hidden + reopen visible → click reopen → assert overlay visible.

```js
$('sumBack').onclick = () => {
  $('summaryOverlay').classList.add('hidden');
  $('sumReopen').classList.remove('hidden');
  $('transcript').scrollIntoView({ behavior: 'smooth', block: 'start' });
};
$('sumReopen').onclick = () => {
  $('summaryOverlay').classList.remove('hidden');
  $('sumReopen').classList.add('hidden');
};
```

## PITFALL 5 — Mic bắt buộc HTTPS (secure context)

getUserMedia chỉ chạy trên HTTPS hoặc localhost. Link LAN IP HTTP mở được trang nhưng `navigator.mediaDevices` = `undefined` → lỗi `"Cannot read properties of undefined (reading 'getUserMedia')"`. KHÔNG phải lỗi code — là secure-context rule.

- LAN IP HTTP → không dùng mic được, kể cả khi trang load 200.
- Phải dùng HTTPS tunnel (loca.lt / Cloudflare subdomain) HOẶC `https://<hostname>.ts.net` (Tailscale serve cấp cert hợp lệ).
- Khi user báo lỗi mic kiểu này: kiểm tra link đang dùng có phải HTTPS không trước khi debug code.

## PITFALL 6 — CSS cascade: `.hidden` khai báo TRƯỚC `.overlay` thì bị đè

Đã gặp live: popup summary không bao giờ ẩn dù `classList.add('hidden')` — vì `.hidden { display:none }` đứng TRƯỚC `.overlay { display:flex }` trong file CSS (cùng specificity → rule SAU thắng).

- Fix: `.hidden { display: none !important; }`.
- **Verify popup phải check `getComputedStyle(el).display`, KHÔNG chỉ `classList.contains('hidden')`** — class có thể đúng mà CSS bị đè (chính mình đã báo "test OK" sai vì chỉ check classList).

## PITFALL 7 — JS scoping: biến khai báo trong hàm async không thấy ở hàm khác

`const source = ctx.createMediaStreamSource(stream)` trong `start()` → `stop()` không có biến `source` → `"source is not defined"`.

- Khai báo TOÀN BỘ state ở top-level: `let ctx=null, stream=null, source=null, processor=null;`
- Trong `start()` gán `source = ...` (không `const`).
- Biến `let` top-level KHÔNG attach vào `window` — test từ browser_console không truy cập được trực tiếp; phải lưu handle (vd `window.__proc = processor` trong mock).

## PITFALL 8 — Chống echo: không nối processor thẳng ra destination

`processor.connect(ctx.destination)` phát tiếng mic ra loa → nghe vọng trong họp. ScriptProcessor vẫn cần nối destination để chạy, nhưng nối qua gain 0:

```js
const silentGain = ctx.createGain();
silentGain.gain.value = 0;
source.connect(processor);
processor.connect(silentGain);
silentGain.connect(ctx.destination);
```

## PITFALL 9 — Race double-click: start()/stop() async

Bấm mic 2 lần khi `start()` chưa xong → 2 luồng getUserMedia; bấm trong lúc `end-json` đang chạy → ghi đè meetingId. Guard chuẩn:

```js
let processing = false;
async function start() {
  if (processing || recording) return;
  processing = true; micBtn.disabled = true;
  try { ... } finally { processing = false; micBtn.disabled = false; }
}
```

## Test UI flow không cần mic thật (browser headless)

`ctx.resume()` TREO trong headless browser (autoplay policy). Cách test full flow:
1. Mock `navigator.mediaDevices.getUserMedia` trả stream oscillator 440Hz (có `await actx.resume()` trong mock), HOẶC mock toàn bộ `window.AudioContext` class: `resume()` trả ngay, `createScriptProcessor()` trả object có setter/getter `onaudioprocess`, lưu vào `window.__proc` để push data giả từ console.
2. Bấm nút mic qua browser_click → assert `recording=true`, nút đỏ ⏹.
3. Push Float32Array sóng sine qua `window.__proc._fn({inputBuffer:{getChannelData:()=>ch}})` → chunk gửi lên server thật.
4. Bấm stop → chờ end-json → assert overlay `display:flex`, test Xem lại/Mở tổng kết/Confirm.



User chốt: "anh đang ở trong mạng lan cho nên dùng link IP máy luôn cho nhanh". Khi user test từ điện thoại CÙNG WiFi:
1. Lấy IP LAN thật: `powershell "(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike '*Loopback*' -and $_.IPAddress -notlike '169.*'} | Select-Object InterfaceAlias,IPAddress | Format-Table -HideTableHeaders)"` — bỏ qua `172.x` (WSL/VirtualBox), chọn `192.168.x` / `10.x`.
2. Verify trước khi gửi: `curl http://<ip>:8766/dictation` → 200.
3. Gửi link `http://<ip>:8766/dictation` thẳng. Nếu không vào được → Windows Firewall chặn port (cần Terminal Admin mở).
4. Tunnel chỉ cần khi user ở mạng NGOÀI (4G/mạng khác).

## Tunnel cho web

```bash
lt --port 8766 --subdomain <ten-moi>   # localtunnel subdomain mới, KHÔNG cloudflared
curl -s -o /dev/null -w "%{http_code}" -H "bypass-tunnel-reminder: 1" https://<ten-moi>.loca.lt/dictation
```

Loca.lt hiện trang trung gian "bypass-tunnel-reminder" lần đầu — báo user bấm *Visit Site / Continue*.
