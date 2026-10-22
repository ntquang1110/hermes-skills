---
name: faster-whisper-local
description: Local faster-whisper STT on Mac/CPU. Deploy, verify, call.
---

# Local faster-whisper STT (faster-whisper / CTranslate2)

Use when the user wants Whisper transcription running **locally** (no Groq/OpenAI API) — typically on a Mac, or any CPU box. Covers: picking the right model, clean install, Apple Silicon config, and verifying before calling it production.

## Decision: model size by RAM
faster-whisper sizes (Systran/faster-whisper-`{tiny,base,small,medium,large-v3,large-v3-turbo}`):
- large-v3 = biggest, most accurate, ~2.9 GB. Needs ~10 GB free to transcribe; good on 16 GB.
- 8 GB Mac → small or medium. 16 GB → large-v3.
- "Nặng nhất phù hợp máy" theo nghĩa max precision trên máy đủ RAM => large-v3 (không phải turbo). Turbo = nhanh hơn, chính xác ~tương đương, dùng khi cần tốc độ qua RAM.

## Install (macOS, không đụng system python)
1. Check hardware first: `sysctl -n machdep.cpu.brand_string`, `sysctl -n hw.memsize`, `sysctl -n hw.ncpu`. Mac mini M1 = 8 core, RAM tùy model.
2. `python3 --version`; system python (3.9.6 CommandLineTools) — TẠO venv riêng, không pip vào system:
   ```
   [ -d ~/whisper-venv ] || python3 -m venv ~/whisper-venv
   ~/whisper-venv/bin/pip install --upgrade pip -q
   ~/whisper-venv/bin/pip install faster-whisper -q
   ```
3. Verify imports: `faster_whisper.__version__`, `ctranslate2.__version__`.

## Apple Silicon config (M1/M2/M3)
No CUDA. Use:
```python
model = WhisperModel("Systran/faster-whisper-large-v3", device="cpu", compute_type="int8")
```
That's the supported path for ctranslate2 on Mac. Don't pass device="auto" expecting a GPU.

## Model download
Loading the model auto-downloads into `~/.cache/huggingface/hub/models--Systran--faster-whisper-*`. Check pre-downloaded models there (user may already have smaller ones cached — `ls ~/.cache/huggingface/hub`). First load is the slow step (~3 GB for large-v3).

## Verify before shipping (ảnh âm thanh tự tạo)
macOS ships a TTS CLI — no audio file needed to test:
```
say -o /tmp/test.aiff "Xin chào, đây là bài kiểm tra"
```
PITFALL: default English `say` voice reads Vietnamese phonetically wrong → transcribe output for VN will look garbled even though the stack is healthy. For a true VN-accuracy check use an English string (comes out ~100%) or a real VN voice/audio; a mangled VN output from a `say` default-voice file is an audio-source artifact, not a whisper bug.

## Realtime vs file-duration: WHERE local whisper is usable (measured)
Measured end-to-end (Windows → SSH → Mac M1 → run_whisper.py --lang vi, short clip): **~10.6s** (SFTP upload + SSH roundtrip + model load every run). Model load on CPU M1 is the dominant cost and happens per-invocation. Consequence for a voice assistant:
- **Realtime turn-by-turn (needs <3s) → NOT this.** Local whisper on CPU cannot do it; use Groq Whisper realtime, keep local as fallback.
- **File-duration / long audio / non-urgent (meeting 30-60 min) → YES.** This is the right call: free, no rate-limit (R1 mitigation), handles long files Groq drops.
Deploy the node once, call it for the long-file path; never wire it into the realtime mic loop expecting sub-3s. On the remote node `run_whisper.py` persists at `~/whisper/run_whisper.py` on `~/whisper-venv` 3.9.6 (faster-whisper 1.2.1, ctranslate2 4.8.2, models large-v3/small/tiny cached) — already verified live.

## Call interface
Known-good script: `templates/run_whisper.py` (copy to target). Usage:
```
~/whisper-venv/bin/python ~/whisper/run_whisper.py /path/to/file --lang vi [--json]
```
- `--lang vi` force Vietnamese, omit for auto-detect.
- `--json` prints segments [{start,end,text}].
- beam_size=5 default.

## Running from another machine (Windows → Mac) without sshpass
git-bash lacks `sshpass` and `expect`. Install `paramiko` in the LOCAL python, drive password-auth SSH from a script. Full pattern: `references/win-mac-ssh-paramiko.md`.

SSH key may fail (Permission denied) if the Mac only has password auth. paramiko with password works regardless.

## Pitfalls
- Reading paramiko stdout: `stdout.readline()` returns bytes if `; out = b""` — mixing str/bytes crashes. Use `stdout.read()` at end, or stay consistent (all str / all bytes). See reference.
- HF warns about missing HF_TOKEN on download — harmless for public models.
- Long downloads (model) exceed SSH exec default: bump timeout to 900-1500 s and make the install-idempotent script echo a DONE marker, retry on missing marker.
- Streaming install output byte-by-byte is fragile; collect `stdout.read()` once.

## HTTP server mode — Mac as persistent STT microservice (deployed 2026-09-22)

When the Mac must serve as a **persistent STT fallback** for the Hermes gateway (not one-shot CLI), run it as an OpenAI-compatible HTTP service so Windows never pays the 5–7s model-reload or SSH handshake.

- **Server** `~/whisper/whisper_server.py` (FastAPI + uvicorn, OpenAI-compatible): `POST /v1/audio/transcriptions` (multipart `file` + `language`), `GET /v1/models`, `GET /health`. Loads `Systran/faster-whisper-large-v3` once at startup (`device=cpu`, `compute_type=int8` on M1) — verify with `curl http://192.168.1.3:9000/health`. Start: `~/whisper-venv/bin/python ~/whisper/whisper_server.py --port 9000 --model large-v3` (needs `fastapi uvicorn python-multipart` in `~/whisper-venv`).
- **launchd** `~/Library/LaunchAgents/com.user.whisper-server.plist` (`Label com.user.whisper-server`, `RunAtLoad` + `KeepAlive`, logs `~/whisper/server.log` / `.err`). `launchctl load …` / `launchctl list | grep whisper-server`. Survives reboot/crash. No tmux needed.
- **Hermes fallback chain** (gateway path `transcribe_audio` → `transcribe_audio_local_fallback`):
  1. Primary `stt.provider: groq` stays. Two Mac entry points: (a) explicit command provider `stt.providers.mac-whisper` (`type: command`, `command: "python \"…/stt_mac_wrapper.py\" {input_path} {output_path} {language}"`) backed by `scripts/stt_mac_wrapper.py` (multipart POST to `:9000`, writes `output_path`); (b) gateway fallback `HERMES_LOCAL_STT_COMMAND` in `~/.hermes/.env` → `scripts/stt_mac_local.py` (parses Hermes template `{input_path} {output_dir} {language} {model}`, POSTs to Mac, writes `{output_dir}/{stem}.txt`).
  2. **Required patches** in `tools/transcription_tools.py`: (a) `_get_local_command_template()` must also read via `hermes_cli.config.get_env_value` — `os.getenv` alone misses `~/.hermes/.env` (Hermes loads .env via `hermes_cli.config`, not process env). (b) `transcribe_audio_local_fallback()` must try `local_command` **before** `faster-whisper` on Windows where `venv/Lib/numpy` is cpython-3.11 built but runtime is 3.14 (`ModuleNotFoundError: numpy._core._multiarray_umath`) — otherwise fallback always fails before reaching Mac.
  3. Verify after `.env` edit: `python -c "import sys; sys.path.insert(0, …); from hermes_cli.config import get_env_value; print(get_env_value('HERMES_LOCAL_STT_COMMAND'))"` — plain `os.getenv` stays None until gateway restart.
- **Watchdog** `scripts/watchdog_mac_whisper.py` (`GET /health`, silent on `status==ok`, `no_agent=true` cron `every 30m`) so a dead Mac server surfaces without spamming when healthy.
- **Pitfall**: `stt_mac_local.py` must handle the full Hermes template grammar (`{input_path} --output_format txt --output_dir {output_dir} --language {language}`) with loose arg parsing; `stt_mac_wrapper.py` handles `{input_path} {output_path} {language}`.

## DHCP IP drift — never hardcode the Mac's IP

The Mac is on DHCP. Its LAN IP moves across router/network restarts; `.3 → .2 → .4 → .5` was observed inside a single session. Every hardcoded `192.168.1.3` (including this skill's own earlier text, and `stt.edge`-style config elsewhere) silently rots into a permanent false "server down".

**A watchdog alert does NOT mean the Mac is down.** "Mac Whisper Server unreachable (:9000): timed out" arrived while the Mac had been up 74 days with a healthy server. Probe before believing:

| Probe | What it actually tells you |
|---|---|
| `ping` the OLD ip | 100% loss proves nothing — it is simply the wrong address now |
| `arp -a` | still lists the stale dynamic entry even though the host moved |
| subnet sweep for port 9000 | finds the Mac at its NEW ip (this is the decisive probe) |
| `uptime` / `launchctl list \| grep whisper` / `lsof -nP -iTCP:9000 -sTCP:LISTEN` over SSH | shows the service was healthy the whole time |
| `REFUSED` on :22 | host is UP; sshd is off — different problem from "timeout" |

Never conclude "the machine is off" from a failed ping to a hardcoded address.

**Resolver** `scripts/mac_whisper_resolve.py` (deployed): resolution order
1. mDNS hostname (`Mac-mini-cua-kiem.local`) — survives DHCP
2. cached last-good IP (`~/.hermes/scripts/.mac_whisper_ip`)
3. parallel `/24` sweep for a host answering on 9000

All three callers import it: `watchdog_mac_whisper.py`, `stt_mac_wrapper.py`, `stt_mac_local.py`. The watchdog uses `resolve(force=True)` to bypass the cache so a moved Mac is re-found on the next tick. Recipe + paramiko probe helpers: `references/lan-service-ip-drift.md`.

## STT returns a fluent but WRONG sentence — hallucination triage

Whisper does not fail loudly. Given audio that is not the language you forced, it emits a confident canned sentence. Fingerprint observed: forcing `language=vi` yielded `"Hãy subscribe cho kênh La La School Để không bỏ lỡ những video hấp dẫn"` — a YouTube-outro phrase from its training data. Byte-identical 70-char output for both the `.ogg` and `.wav` of the same file is the tell: the model is not decoding your audio at all.

Triage in this order (isolate audio → model → server; do not guess):
1. **Measure the audio** with `wave` + peak/RMS in dBFS. Peak ≈ −4 dBFS with real RMS ⇒ the file has content, so the fault is upstream of the model.
2. **Transcribe the same file on the box** using the server's own venv (`~/whisper-venv/bin/python`; the system `python3` lacks `faster_whisper`), once with `vad_filter=True` and once `False`. Same garbage both ways ⇒ not VAD, not the HTTP server.
3. **Question the SOURCE audio.** Here the upstream TTS was Hermes `tts.edge.voice: en-US-AriaNeural` — an English voice reading Vietnamese text, so the "Vietnamese" clip was never Vietnamese. Details in `vietnamese-tts`.

Lesson: when STT output is fluent nonsense, suspect the audio's language before the model or the server.

## Making test audio on macOS (no ffmpeg)

The Mac has no ffmpeg; `afconvert` ships with macOS:
```
say -v Linh -o /tmp/t.aiff "Câu tiếng Việt có dấu đầy đủ."
afconvert -f WAVE -d LEI16@16000 -c 1 /tmp/t.aiff /tmp/t.wav
```
`say -v '?' | grep vi_VN` lists Vietnamese voices (`Linh` on this box). Always write the source string WITH full diacritics — unaccented input makes `say` read wrong tones and the transcript then looks broken on an otherwise healthy stack. Measured on the deployed box: proper-diacritic Vietnamese → 87% word match, and the two "misses" were just `7`/`bảy` and `10`/`mười`.

## Support files
- `templates/run_whisper.py` — reference local transcribe script (copy to box).
- `references/win-mac-ssh-paramiko.md` — paramiko password-SSH control pattern from Windows.
- `references/openclaw-vs-opencode.md` — OpenClaw≠OpenCode wiring, auth (models.providers.*.apiKey + baseUrl), free-tier vs paid, 402 funds error, Mac deploy state.
- `scripts/stt_mac_local.py` / `scripts/stt_mac_wrapper.py` + `scripts/watchdog_mac_whisper.py` — live deployed wrappers/watchdog for the HTTP fallback (see section above).
- `scripts/mac_whisper_resolve.py` — DHCP-proof host resolution (mDNS → verified cache → `/24` sweep). Copy/adapt for any drifting LAN service; all three callers above import it.
- `references/lan-service-ip-drift.md` — diagnosis protocol for "service unreachable" false alarms, stdlib sweep recipe, Windows→Mac paramiko probe helpers, prevention rules.