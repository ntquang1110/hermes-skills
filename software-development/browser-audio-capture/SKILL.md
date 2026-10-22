---
name: browser-audio-capture
description: Use when building browser mic capture for STT pages.
tags:
  - browser
  - audio
  - microphone
  - stt
  - dictation
  - webrtc
  - javascript
---

# Browser Audio Capture for STT / Dictation

Use when building a web page that records the microphone in-browser and streams audio to a server STT pipeline (dictation, meeting recording, voice notes). Covers the pitfalls that break a naive `getUserMedia` → `AudioContext` implementation — especially on mobile browsers and headless testing.

## Architecture

```
Browser: getUserMedia → AudioContext → ScriptProcessor → Float32 → Int16 PCM → buffer
         → wrap WAV (44-byte header) → multipart POST /chunk-live → server VAD + Whisper
         → accumulate text → debounced POST /context → live title/context/decisions
         → POST /end-json → commit-ready summary popup
```

Serve the page SAME-ORIGIN as the API (FastAPI `GET /dictation` returning the HTML file, `API = ''` in JS) → no CORS anywhere.

## Pitfalls (each cost real debugging time — fix before shipping)

### 1. Mic REQUIRES HTTPS (secure context) — #1 cause of "getUserMedia undefined"
`navigator.mediaDevices` is **undefined on HTTP origins** (LAN IP, `http://192.168.1.x`). Error: `Cannot read properties of undefined (reading 'getUserMedia')` — NOT a code bug.

- Works: HTTPS (Cloudflare subdomain, loca.lt, Tailscale serve), or `localhost` (secure by exception).
- Fails: `http://<LAN-IP>:port`, any plain HTTP.
- Fix: tunnel/subdomain with HTTPS. Do NOT chase the JS — switch transport first.

### 2. Echo/feedback: connect ScriptProcessor → destination = mic plays out of speaker
`processor.connect(ctx.destination)` feeds the mic into the speakers → audio feedback during meetings. Keep the processor running but route through a zero-gain node:

```js
source.connect(processor);
const silent = ctx.createGain();
silent.gain.value = 0;
processor.connect(silent);
silent.connect(ctx.destination);
```

### 3. `new AudioContext({sampleRate: 16000})` is IGNORED on iOS Safari
Requested sample rate is a hint, not a contract (desktop Chrome honors it, iOS often does not). Compute chunk size from the REAL rate, and resample to 16k for servers whose VAD only accepts 8/16/32/48kHz:

```js
const rate = ctx.sampleRate;                      // real, e.g. 48000
const chunkSamples = rate * 5;                    // 5 seconds of SAMPLES
// resample Int16 → 16k: out[i] = pcm[Math.floor(i * rate/16000)]
```

**Unit trap that silently killed live dictation (verified Aug 2026):** `pcmBuffer` is an array of SAMPLES (one element per sample), NOT bytes. `rate * 2 * 5` = `rate * 10` = 10 seconds of samples, not 5s. Symptom: user talks for <10s, nothing appears live; only a single leftover chunk arrives at stop (see #8). The `* 2` (bytes per Int16 sample) belongs only in WAV byte math (`rate*2*5` bytes IS 5s), never in JS array-length thresholds. On the Flutter side, byte streams make `160000` bytes = 5s correct — the trap is JS sample arrays.

### 4. CSS `.hidden` loses to a later `display:flex`
If `.hidden { display:none }` is declared BEFORE a rule like `.overlay { display:flex }` (same specificity), the overlay wins and `classList.add('hidden')` does NOT close the popup. Fix: `.hidden { display: none !important; }`. **Verify with `getComputedStyle(el).display`, not `classList.contains('hidden')`** — class presence ≠ applied style.

### 5. `let` vars declared in one async fn are invisible to another
`let source` inside `start()` but used in `stop()` → `ReferenceError: source is not defined`. Declare shared state (ctx, stream, source, processor) at module scope.

### 6. Double-click / re-entrancy on the record button
`start()` is async; before `recording=true` is set a second click re-runs it → two getUserMedia streams. Guard with a `processing` flag + `micBtn.disabled` set at the top of start/stop, cleared in `finally`.

### 7. Flush leftover PCM on stop (don't lose the tail)
On stop, if the buffer holds ≥ ~0.5s of audio, upload it as a final chunk BEFORE calling end-json, or the last words never reach the transcript.

### 8. "No text appears" — triage server logs, don't guess client-side
When the user reports "nói mà không thấy text", the fastest discriminator is the SERVER access log — check how many chunk requests arrived:

- **0 chunks** → mic never started (HTTPS? permission?) — client problem. See pitfall #1.
- **Exactly 1 chunk, arriving only at stop** → live flush never fired: chunk threshold too big (see #3 unit trap — `rate*2*5` = 10s, so a <10s talk produces zero live chunks) and/or VAD rejected the single leftover (see #9 head-silence). Fix BOTH.
- **N chunks arriving but no text** → server-side: VAD blocking or STT returning empty. **Add explicit prints to the chunk endpoint** so each chunk logs its fate:
  ```python
  # in /chunk-live handler
  if not _has_speech(contents):
      print(f"[chunk-live] {meeting_id} #{i} VAD=NO_SPEECH size={len(contents)}", flush=True)
      return {"text": "", "speech": False, ...}
  result = stt.transcribe(str(file_path))
  print(f"[chunk-live] {meeting_id} #{i} VAD=SPEECH dur={result.get('duration',0):.1f}s text={result.get('text','')[:60]!r}", flush=True)
  ```
  `VAD=NO_SPEECH` everywhere → user too far/quiet, threshold too high, or wrong sample rate (VAD only accepts 8/16/32/48k — a 44.1k WAV makes `_pcm_from_wav` fail and VAD silently pass-through). `VAD=SPEECH` + empty text → whisper model issue, not client. Always restart the server after adding prints and verify the new process is actually serving (`netstat -ano | grep :PORT | grep LISTEN`, health endpoint) — a stale process with old code silently gives you old behavior.

  **VAD aggressiveness mode matters as much as the threshold (verified Aug 2026):** `webrtcvad.Vad(2)` (default "aggressive") drops quiet/soft-spoken voices on a phone mic even when the ratio threshold is sane — every chunk logs `VAD=NO_SPEECH` and the user sees "nói mà không có text". Switch to `Vad(1)` for dictation use-cases where users hold the phone naturally (not up to their mouth). After changing the mode you MUST restart the server AND confirm the new PID is the one serving the port (an old process with `Vad(2)` silently keeps the old behavior).

  **Server died mid-session — the case where logs PROVE STT works but the user saw nothing:** the chunk logs show `VAD=SPEECH text='...'` (real Vietnamese text transcribed) yet the UI showed nothing after the first chunk. Root cause found: the server process exited (exit code 1) right after the first requests — killed/lost due to process-manager tracking loss and orphan processes fighting over the port — so later chunks got no handler. When process manager reports a session "not found" or "exited" but the port still listens, identify the REAL holder and kill it before restarting:
  ```bash
  netstat -ano | grep ":PORT" | grep LISTEN   # PID may differ from the managed process
  taskkill -F -PID <real_pid>                  # single-dash form works in git-bash; //F does NOT
  # then start fresh, wait for health endpoint, and curl the public URL
  ```
  Rule: after ANY server restart, verify three layers — local health, public subdomain HTTP code, and the new chunk-log prints actually appearing in the live process output.

### 9. Server VAD must scan the WHOLE chunk — head silence is normal
Users tap the mic, THEN start talking. The first 0.5–1.5s of a chunk is dead silence. A VAD that only inspects the first N frames (e.g. "check 1s, ≥3 speech frames") will return NO_SPEECH on real speech and silently drop the chunk — even though the audio is perfect. Fix: scan ALL frames and use a ratio threshold:

```python
# frame 20ms; scan entire PCM, not just the first second
speech_frames = 0; total_frames = 0
for i in range(0, len(pcm) - frame_bytes + 1, frame_bytes):
    try:
        if vad.is_speech(pcm[i:i+frame_bytes], sr): speech_frames += 1
    except Exception: continue
    total_frames += 1
return total_frames > 0 and (speech_frames / total_frames) >= 0.05  # ≥5% frames
```

**Verify against the REAL captured chunk, not a synthetic tone:** dump the server's saved `.wav` and measure per-second RMS:
```python
import wave, struct, math
f = wave.open(path, 'rb'); sr = f.getframerate(); raw = f.readframes(f.getnframes()); f.close()
for i in range(int(f.getnframes()/sr)):
    seg = raw[i*sr*2:(i+1)*sr*2]; n = len(seg)//2
    s = struct.unpack(f'<{n}h', seg)
    print(f"giây {i}: RMS={math.sqrt(sum(x*x for x in s)/n)/32768:.3f}")
```
RMS=0.000 in second 0 then 0.1–0.4 later = user tap-delay, audio is fine, VAD logic is the bug. All-zero across → capture broken client-side. This distinguishes "VAD too strict" from "mic never captured" without guessing.

## Headless QA (browser console)

You CANNOT get a real mic in a headless browser. Mock it and drive the whole flow:

```js
// Mock getUserMedia — return any object with getTracks
navigator.mediaDevices.getUserMedia = async () => ({ getTracks: () => [{ stop() {} }] });
// Mock AudioContext — real one hangs on resume() in headless
window.AudioContext = window.webkitAudioContext = class {
  constructor(o){ this.sampleRate = 16000; this.destination = {}; }
  async resume(){} async close(){}
  createMediaStreamSource(s){ return { connect(){}, disconnect(){} }; }
  createGain(){ return { gain:{value:0}, connect(){}, disconnect(){} }; }
  createScriptProcessor(){ const p = { connect(){}, disconnect(){}, set onaudioprocess(f){this._fn=f}, get onaudioprocess(){return this._fn} }; window.__proc = p; return p; }
};
```

- **`let`/`const` at top level do NOT attach to `window`** — you can't read `recording` etc. from console. Expose test hooks explicitly (`window.__proc`).
- To simulate audio: `window.__proc._fn({ inputBuffer: { getChannelData: () => new Float32Array(16000*6).fill(0) } })` → triggers a 5s chunk flush.
- Test popup open/close via computed style, click handlers via `.click()`, and verify against real server logs (`POST /chunk-live 200`).

## Serving + tunnel

- FastAPI: `@app.get("/dictation", response_class=HTMLResponse)` returning the HTML file content (read with `Path(__file__).resolve().parent.parent / "web" / "dictation.html"` — mind the `..`; `__file__` is inside the package dir).
- For HTTPS on LAN: Cloudflare named tunnel (see `cloudflare-tunnel` skill — token-service tunnels ignore local config.yml; create a dedicated named tunnel instead) or Tailscale serve. Never ship the LAN HTTP URL as the mic-capable link.
