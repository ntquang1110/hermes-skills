---
name: voice-and-stt
title: Voice & Speech-to-Text
description: Configure, test, and troubleshoot Hermes STT (voice message recognition) for Telegram and other platforms. Covers faster-whisper setup, model sizing, provider switching, and Windows-specific gateway lifecycle.
category: software-development
tags: [voice, stt, whisper, faster-whisper, telegram, speech-to-text, windows, gateway]
version: 1.0.0
---

# 🎤 Voice & Speech-to-Text (STT) — Hermes

## When to use

- User asks you to set up or test voice message processing (Telegram voice → text)
- User reports poor transcription quality (garbage text from voice messages)
- User asks which STT provider/model to use
- Gateway needs restart after STT config change
- Windows-specific gateway lifecycle issues arise

## 1. STT Provider Architecture

Hermes supports multiple STT providers. The active one is set in `~/.hermes/config.yaml`:

```yaml
stt:
  enabled: true
  provider: local          # local | openai | elevenlabs | mistral
  local:
    model: base           # tiny | base | small | medium | large-v3
    language: ''          # leave empty for auto-detect, 'vi' for Vietnamese
  openai:
    model: whisper-1
```

**Change provider/model via CLI:**
```bash
hermes config set stt.provider local
hermes config set stt.local.model medium
```

### Provider comparison

| Provider | Cost | Quality on VI | Latency | Setup | Notes |
|----------|------|--------------|---------|-------|-------|
| **local** (faster-whisper) | Free | Good (medium+) | Slow-large | `pip install faster-whisper` | Runs entirely local, no API key. Model must be pre-downloaded |
| **Groq Whisper** ⭐ | Free tier | Excellent (large-v3) | Fastest | Set `GROQ_API_KEY` | 20K req/day free. LPU hardware. ~25MB file limit (OpenAI-compatible). Rate-limited by audio seconds/hour. Best free option for Vietnamese |
| **OpenAI Whisper API** | Paid | Excellent | Fast | Set `VOICE_TOOLS_OPENAI_KEY` | Paid per-minute |
| **ElevenLabs** | Paid credits | Good | Fast | Set `ELEVENLABS_API_KEY` | Scribe model |
| **Mistral** | Free tier | Good | Medium | Set `MISTRAL_API_KEY` | Voxtral model |

## 2. Local STT (faster-whisper) — Đã gỡ

faster-whisper đã được gỡ khỏi hệ thống theo yêu cầu của user. User **chỉ dùng Groq Whisper API** cho STT — không cài lại local STT trừ khi user yêu cầu cụ thể.

### Nếu user muốn cài lại (khi được yêu cầu)

faster-whisper chạy trong Hermes venv:

```bash
# Cài đặt
/c/Users/NTQUANG_DELL/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe -m pip install faster-whisper

# Xác minh
/c/Users/NTQUANG_DELL/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe -c "import faster_whisper; print(faster_whisper.__version__)"
```

**Important**: Hermes venv Python (3.11.x) khác với hệ thống Python (3.14.x). Luôn dùng full venv path, không dùng `pip install` bare.

## 3. Groq Whisper (Recommended for Vietnamese)

Groq Whisper is the **best free option for Vietnamese** STT. It runs Whisper large-v3 on Groq's LPU hardware — fast, accurate, and no local download needed.

### Setup

```bash
# 1. Get a free API key from https://console.groq.com
#    Free tier: 20,000 requests/day

# 2. Set the API key in ~/.hermes/.env
echo 'GROQ_API_KEY=gsk_<your-key-here>' >> /c/Users/NTQUANG_DELL/AppData/Local/hermes/.env

# 3. Switch provider to groq
hermes config set stt.provider groq

# 4. Verify config
grep -A5 "stt:" /c/Users/NTQUANG_DELL/AppData/Local/hermes/config.yaml
# Expected: provider: groq, enabled: true

# 5. Restart gateway
# See section 5 for restart procedure
```

### Vietnamese transcription quality

Groq Whisper (large-v3) handles Vietnamese **significantly better** than local faster-whisper medium:

| Phrase | local base | local medium | Groq (large-v3) |
|--------|-----------|-------------|-----------------|
| "tạo task dịch tả Châu Phi" | "tạo tác dịch tảng chô phi" | "tạo protocol cho dịch tảng chô phi" | ✅ **Chuẩn** |
| "tạo thử task trên notion" | "đạo thứ cái tác ở trên nấu sừng" | (better) | ✅ **Chuẩn** |

**Verdict:** For Vietnamese, Groq Whisper is the clear winner — free, fast, and far more accurate than local models up to `medium`. The only downside: requires internet and a free API key signup.

### 🔴 `whisper-large-v3-turbo` HALLUCINATE tiếng Việt — bắt buộc set `stt.groq.model: whisper-large-v3` (2026-10-19)

**Symptom (đã gặp thật):** voice note tiếng Việt **7,7 giây** → transcript trả về đúng 3 chữ *"Xin chào các bạn."* Bot tưởng user chào hỏi xã giao → trả lời nhầm hoàn toàn câu hỏi thật. Không có log lỗi, không exception, `success: true`. **Đây là kiểu hỏng nguy hiểm nhất: sai nhưng trông hợp lệ.**

**Root cause:** `DEFAULT_GROQ_STT_MODEL = "whisper-large-v3-turbo"` (`tools/transcription_tools.py:113`). Nếu `stt.groq.model` KHÔNG có trong `config.yaml`, Hermes im lặng dùng turbo. Turbo là bản distilled — với audio tiếng Việt có nội dung dài nó **sụp về một câu xã giao ngắn** thay vì báo lỗi.

**Bằng chứng đo được (cùng 1 file, cùng pipeline `transcribe_audio()`):**

| Model | Transcript |
|-------|-----------|
| `whisper-large-v3-turbo` | `'Xin chào các bạn.'` ❌ (bịa) |
| `whisper-large-v3` | `'Giải thích sâu cho anh về bản chất của máy gia tốc là như nào? …'` ✅ |

Không phải lỗi preprocessing — `_prepare_audio_for_transcription` trả nguyên file gốc, và turbo/libop 48k cũng sai y hệt.

**Fix (1 dòng, có hiệu lực NGAY không cần restart gateway):**
```bash
hermes config set stt.groq.model whisper-large-v3
```
`load_config()` cache theo `(mtime_ns, size)` của `config.yaml` → gateway tự thấy file đổi. **Không cần restart** (khác với đổi `stt.provider`).

**Verify đúng cách** — phải test qua `transcribe_audio()` (đọc config) chứ không phải `_transcribe_groq(f, 'model')` (bỏ qua config nên luôn đúng):
```bash
/c/Users/NTQUANG_DELL/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe -c 'import sys
sys.path.insert(0,"C:/Users/NTQUANG_DELL/AppData/Local/hermes/hermes-agent")
import tools.transcription_tools as tt
print(tt.transcribe_audio(r"<path-audio.ogg>").get("transcript"))'
```

**Quy tắc:** đã đo model nào thì ghi rõ model đó. Đừng kết luận "STT hỏng / mạng lỗi / audio bị cắt" khi chưa so 2 model trên cùng file — triệu chứng giống hệt nhau.

### 🔧 Thuật ngữ domain bị bóp méo → `initial_prompt` NGẮN tiếng Việt (không phải prompt tiếng Anh)

Cùng file trên, `whisper-large-v3` vẫn nghe "máy gia tốc" thành *"máy ra dốc"* / *"máy ra gốc"*. Thêm `prompt` **1 câu tiếng Việt** mô tả chủ đề → sửa đúng ngay:
```python
c.audio.transcriptions.create(model="whisper-large-v3", file=fh, language="vi",
    prompt="Anh hỏi về máy gia tốc hạt và phản ứng hạt nhân.")
# -> '…bản chất của máy gia tốc là như nào? …'   ✅
```
2 prompt độc lập cùng hội tụ về "máy gia tốc" ⇒ xác nhận đúng, không phải đoán. **`initial_prompt` NGẮN tiếng Việt = tốt; prompt tiếng Anh = phá toàn bộ transcript** (xem mục bên dưới). Prompt dài liệt kê keyword → Whisper lặp lại chính prompt.

**Cho audio dài/nhiều nội dung, tăng volume trước khi gửi (recipe mục quality tuning):**
```bash
ffmpeg -y -i in.ogg -af "volume=12dB,highpass=f=80,lowpass=f=8000" -ar 16000 -ac 1 -c:a libopus -b:a 48k out.ogg
```


### ⚠️ Groq Whisper quality tuning (đã test thực tế trên meeting 20 phút)

Khi transcript mất từ / bỏ sót nội dung, thứ tự fix theo tác động:

1. **Volume boost TRƯỚC khi gửi Groq — yếu tố quyết định.** Không boost → Whisper bỏ sót nội dung (tên người, con số, thuật ngữ). Boost → bắt đủ:
   ```bash
   ffmpeg -y -i in.mp3 -af "volume=12dB,highpass=f=80,lowpass=f=8000" -ar 16000 -ac 1 -c:a libopus -b:a 48k out.opus
   ```
2. **Opus 48k, KHÔNG 24k** — 24kbps quá thấp cho tiếng Việt (thanh điệu, từ chuyên ngành) → mất từ ngay từ đầu. Không dùng bitrate tự tính targeting <20MB nữa nếu có thể.
3. **Groq Whisper xử lý Opus 16kHz nén tốt hơn mp3 gốc** — luôn nén + boost trước khi gửi, kể cả file < 25MB.
4. **initial_prompt PHẢI NGẮN (1 câu).** Prompt dài liệt kê từ khóa domain → Whisper hallucination lặp lại chính prompt vào transcript. VD tốt: `"Cuộc họp nội bộ về chăn nuôi, sản xuất, kinh doanh."`
5. **Chunk theo duration, không theo size.** Sau nén 20 phút ≈ 5.6MB < 25MB → gửi thẳng. Chỉ chunk khi > 55 phút (nén ~7MB/30 phút). Chunk 10 phút + overlap 30s + dedup khi nối.
6. **Thứ tự boost-chunk:** boost TOÀN FILE trước, rồi mới chunk (`-c copy`). Boost rồi chunk = sạch; chunk rồi boost = khuếch đại nhiễu → hallucination nặng.

**Hallucination cleaning (heuristic, KHÔNG dùng LLM):** Whisper hay bịa câu quảng cáo lặp ("subscribe cho kênh", "đăng ký kênh", "like, share", "Ghiền Mì Gõ", "hẹn gặp lại"). Dùng llama-3.3-70b để clean là SAI — nó xóa luôn nội dung thật và trả câu meta kiểu "Không có nội dung...". Clean đúng:
- Whisper trả text **1 dòng liền** → tách theo CÂU (regex `(?<=[.!?])\s+|\n+`), không tách theo dòng.
- Xóa câu chứa ad-marker; xóa câu vô nghĩa (toàn từ ngắn, avg word len < 2.5, ≥8 từ); dedup câu lặp liên tiếp (so 30 ký tự đầu).
- Chuẩn hóa từ sai domain: "kiếm vãi nặng"→"kim loại nặng", "tiêu sảy"→"tiêu chảy", "chủ chạy"→"chủ trại".
- Bảo vệ: nếu kết quả clean < 50 chars → giữ nguyên bản gốc.

> Code mẫu đầy đủ → `references/groq-whisper-quality-tuning.md`

### ⚠️ Groq 403 error 1010 = request THIẾU User-Agent (KHÔNG phải account chưa verify)

**Symptom:** `GET /models` trả 200 nhưng `POST /audio/transcriptions` trả `HTTP 403: error code: 1010` — chỉ khi gọi bằng urllib/requests **tự viết, KHÔNG set User-Agent**.

**Root cause (đã verify 2026-09-12):** Groq đứng sau Cloudflare WAF chặn request không có UA header. Cùng key đó:
- `GET /models` không UA → 200 (endpoint này không bị chặn)
- `POST transcriptions` không UA → **403 error 1010**
- `POST transcriptions` có `User-Agent: openai-python/1.30.0` → 200 OK, transcribe tiếng Việt chuẩn
- OpenAI SDK (Hermes `_transcribe_groq`, openai 2.24.0) → tự set UA → 200 OK

⚠️ Kết luận trước đó "account chưa verify SMS → audio bị 403" là **SAI** (ghi nhầm 2026-09-12). Key sống, audio mở, chỉ thiếu header.

**Fix:** luôn gọi qua OpenAI SDK (như `_transcribe_groq`), hoặc nếu tự viết urllib/requests → bắt buộc thêm `User-Agent: openai-python/1.30.0` (hoặc UA trình duyệt). Khi gặp 1010: test lại CÓ UA trước khi kết luận key hỏng / cần verify — đừng chuyển STT sang local vì nhầm lẫn này.

**Verify nhanh key + audio còn sống:**
```bash
/c/Users/NTQUANG_DELL/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe -c "
import sys; sys.path.insert(0, r'C:\Users\NTQUANG_DELL\AppData\Local\hermes\hermes-agent')
from tools.transcription_tools import _transcribe_groq
print(_transcribe_groq(r'<path-to-audio>', 'whisper-large-v3-turbo'))
"
# success=true → Groq OK, đừng đổi provider
```

**Repro đầy đủ:** `references/groq-403-error-1010-missing-ua.md`

### ⚠️ Language hint: Groq transcribe tiếng Việt sang English

**Symptom:** User nói tiếng Việt nhưng voice bị transcribe ra tiếng Anh (đặc biệt audio ngắn <30s).

**Root cause:** Groq Whisper nhận language hint theo thứ tự `stt.groq.language` → `stt.language` (global) → `HERMES_LOCAL_STT_LANGUAGE` env → `None` (auto-detect). Nếu không có hint, Whisper auto-detect thiên vị tiếng Anh. Config thường thiếu cả `stt.groq.language` lẫn `stt.language`.

**Fix:**
```bash
hermes config set stt.groq.language vi
# hoặc global cho mọi provider:
hermes config set stt.language vi
```
Rồi restart gateway. Verify trực tiếp resolution (không cần gửi voice):
```bash
/c/Users/NTQUANG_DELL/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe -c "
import sys; sys.path.insert(0, r'C:\Users\NTQUANG_DELL\AppData\Local\hermes\hermes-agent')
from tools.transcription_tools import _resolve_stt_language
print(repr(_resolve_stt_language('groq')))
"
# Kỳ vọng: 'vi'
```
Nguồn: `tools/transcription_tools.py::_resolve_stt_language` — resolution order `stt.<provider>.language` → `stt.language` → env → None.

### ⚠️ KHÔNG thêm English initial_prompt cho code-switching Việt-Anh (2026-08)

**Symptom:** sau khi set `stt.groq.language: vi`, voice vẫn ra tiếng Anh hoặc transcript lặp lại chính prompt.

**Root cause:** thêm `stt.groq.prompt` tiếng Anh kiểu *"Vietnamese speech mixed with English technical terms. Keep English words in English: dashboard, deploy..."* làm Whisper tưởng người nói đang nói tiếng Anh → transcribe toàn bộ sang English, hoặc hallucination lặp lại prompt trong output (test thực tế 4 biến thể trên cùng 1 file audio). Ngược với intuition — prompt tưởng giúp code-switching nhưng thực tế phá.

**Fix đúng:** Whisper large-v3 với `language: vi` **tự xử lý code-switching** — giữ nguyên từ tiếng Anh trong câu Việt ("check", "dashboard", "deploy", "feature", "production") mà không cần prompt. Chỉ giữ prompt nếu thật sự cần cho domain meeting (prompt NGẮN 1 câu tiếng Việt, xem mục quality tuning ở trên).

**Test nhanh không cần voice thật (edge-tts):**
```bash
# 1. Tạo audio test: câu tiếng Việt lẫn từ tiếng Anh
/c/Users/NTQUANG_DELL/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe -c "
import asyncio, edge_tts
async def main():
    await edge_tts.Communicate(
        'Chào anh, em cần check dashboard rồi deploy feature lên production.',
        'vi-VN-HoaiMyNeural').save('C:/tmp/mix_test.mp3')
asyncio.run(main())"
# 2. Gọi Groq 4 biến thể: auto / language=vi / language=vi+prompt / prompt-only → so sánh
# Kết quả thực tế: auto ≈ language=vi (chuẩn), thêm prompt tiếng Anh → hỏng toàn bộ
```
Script test đầy đủ: gọi `client.audio.transcriptions.create` với từng biến thể `language`/`prompt` lên cùng file → chọn biến thể cho transcript đúng nhất.

### ⚠️ Gateway restart note

After setting `stt.provider: groq`, you **must** restart the gateway. See section 5 for the correct procedure. Unlike local model changes, no pre-download is needed — Groq processes remotely.

### File upload limits

Groq Whisper (like OpenAI Whisper API) has a **~25MB file upload limit**. This is a hard limit at the API level — files larger than 25MB are rejected.

For long recordings (> 60 min or > 20MB), pre-compress audio before sending:

```bash
# Using the meeting-transcriber compression script
bash /c/Users/NTQUANG_DELL/AppData/Local/hermes/skills/meeting-transcriber/scripts/compress-audio.sh input.mp3
```

The script converts to Opus mono at auto-calculated bitrate, targeting < 20MB. See `meeting-transcriber` skill for full workflow.

## 4. Model Quality Tuning

### Vietnamese language considerations

Vietnamese transcription is significantly harder than English. Model sizing matters:

| Model | Quality on VI | RAM/VRAM | Download | Speed |
|-------|--------------|----------|----------|-------|
| `tiny` | Poor | ~1GB | ~75MB | Fastest |
| `base` | Poor-Fair | ~1GB | ~142MB | Fast |
| `small` | Fair-Good | ~2GB | ~466MB | Medium |
| `medium` | Good | ~5GB | ~1.5GB | Slow |
| `large-v3` | Excellent | ~10GB | ~3.1GB | Slowest |

**Progression pattern:** Start at `base`, test with a real voice message. If poor, bump to `small`, test again. Then `medium` if still insufficient. Don't jump straight to `large-v3` without confirming the user can accept the latency.

### Language hint

Set `stt.<provider>.language: vi` (vd `stt.groq.language: vi`, `stt.local.language: vi`) cho Vietnamese-specific optimization. `stt.language: vi` là global fallback áp dụng mọi provider. Để trống = auto-detect (chỉ nên dùng cho audio đa ngôn ngữ). Lưu ý: auto-detect thiên vị tiếng Anh với audio ngắn tiếng Việt — xem section 3 "Language hint: Groq transcribe tiếng Việt sang English".

### ⚠️ CRITICAL: Pre-download models before switching

When you change `stt.local.model` to a larger model (e.g. `base` → `medium`), the new model file must be **pre-downloaded** before the gateway processes any voice message. **Do NOT skip this step.**

**Why:** The first voice message after a model switch triggers a synchronous download of the new model (up to 1.5GB for `medium`). This blocks the STT pipeline, times out, and the user gets **no response at all** — not even an error. The gateway log shows nothing about it.

**How to pre-download:**
```python
# Run this from the Hermes venv Python
/c/Users/NTQUANG_DELL/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe -c "
from faster_whisper import download_model
print('Downloading...')
model_path = download_model('medium')
print(f'Model downloaded to: {model_path}')
"
```

Model cache location on disk:
```
~/.cache/huggingface/hub/models--Systran--faster-whisper-<model>/snapshots/<hash>/
```

**Symptom checklist for missing model:**
- User sends voice → bot says nothing back
- Gateway log shows Telegram connected, no errors
- No audio file cached in `~/AppData/Local/hermes/audio_cache/`
- The `~/.cache/huggingface/hub/` directory lacks the target model

**Model download sizes:**
| Model | Download size |
|-------|--------------|
| `tiny` | ~75 MB |
| `base` | ~142 MB |
| `small` | ~466 MB |
| `medium` | ~1.5 GB |
| `large-v3` | ~3.1 GB |

**Workflow: change model → pre-download → restart gateway → test voice**

## 5. Gateway Lifecycle (Windows)

**CRITICAL**: The gateway CANNOT be restarted from **inside its own process** (i.e., from a Telegram/bot agent session that runs within the gateway). Any `hermes gateway restart` command from inside the gateway will be blocked:

```
Blocked: cannot restart or stop the gateway from inside the gateway process.
```

**However**, `hermes gateway restart` **works from the TUI** (terminal UI) because the TUI is a separate process. The block only applies when the command is issued from a session running inside the gateway's own process group.

### Correct restart procedure

**Option A — schtasks (works from git-bash):**
```bash
schtasks //end //tn "Hermes_Gateway"
sleep 2
hermes gateway status   # Should show gateway starting up again
```

**⚠️ THỰC TẾ 2026-08-05:** `schtasks //end //tn "Hermes_Gateway"` từ git-bash **fail** với `ERROR: Invalid argument/option - '//end'` (MSYS mangle cả double-slash). `cmd //c 'schtasks /end ...'` cũng không chạy (chỉ mở prompt cmd trống). Trên máy này, lối đi đáng tin là **user tự restart**:
```bash
hermes gateway restart   # từ Terminal Admin (shell Hermes không có admin)
```
hoặc nếu cần tự động: `taskkill -f -pid <PID>` (single-dash, xem Option B) — scheduled task auto-restart trong vài giây.

**Option B — taskkill (single-dash flags for git-bash):**
```bash
taskkill -f -pid <PID>
```

Both methods terminate the current gateway process. The Windows Scheduled Task auto-restarts it within seconds.

**Option B — Gateway is already down (no process detected):**
```bash
hermes gateway start
```
This always works when no gateway process is active. Gateway being down is the normal state to restart from.

### Checking status
```bash
hermes gateway status
```
Look for: `✓ Gateway process running (PID: NNNNN)` — success; `✗ No gateway process detected` — gateway is down.

### Verifying Telegram connection after restart
```bash
tail -5 /c/Users/NTQUANG_DELL/AppData/Local/hermes/logs/gateway.log
```
Look for: `[Telegram] Connected to Telegram (polling mode)` and `✓ telegram connected`.

### Windows `taskkill` path quirk

In git-bash (MSYS), native Windows commands with `/` flags are misinterpreted:
```bash
# These FAIL in git-bash:
taskkill /F /PID 12684        # MSYS converts /F to a path
"C:/Windows/System32/taskkill.exe" /F /PID 12684  # Also fails

# Use single-dash syntax instead:
taskkill -f -pid 12684
```

## 5. Voice Message Test Flow

When a user reports poor transcription or wants to test STT:

1. **Check current config**: `grep -A10 "stt:" /c/Users/NTQUANG_DELL/AppData/Local/hermes/config.yaml`
2. **Adjust model** if needed (see section 3)
3. **Verify gateway is running**: `hermes gateway status`
4. **Ask user to send a voice message** on Telegram (short, clear phrase)
5. **Compare transcribed text** vs what the user actually said
6. **Iterate model size** if quality is poor

### What to tell the user
> "Anh gửi thử 1 voice message ngắn vào Telegram — em sẽ nhận, transcribe bằng faster-whisper model [X], và show lại text cho anh check."

## 7. Common Pitfalls

> **🧩 Related:** `meeting-transcriber` skill — full workflow for transcribing long meeting recordings including pre-compression.

- ❌ **Installing pip packages into system Python instead of Hermes venv** — always use the full venv path
- ❌ **Trying to restart gateway from inside gateway** — blocked by design; use schtasks or taskkill from external shell
- ❌ **`taskkill` with MSYS path mangling** — use single-dash flags (`-f -pid`); never `/F /PID` which MSYS converts to filesystem paths
- ❌ **`schtasks` với MSYS path mangling** — `schtasks //end //tn "Hermes_Gateway"` **vẫn fail** 2026-08-05 (`Invalid argument/option - '//end'`); `cmd //c` cũng không chạy. Trên máy này: user tự `hermes gateway restart` (Terminal Admin) hoặc `taskkill -f -pid <PID>` (xem section 5)
- ❌ **Expecting `tiny`/`base` model to handle Vietnamese well** — Vietnamese needs at least `small`, preferably `medium` or Groq Whisper
- ❌ **Switching to a larger model without pre-downloading it first** — the first voice message triggers a synchronous download; user gets **zero response** while it hangs. Always pre-download (see section 4).
- ❌ **Forgetting to restart gateway after config change** — config changes to `stt.*` only take effect on gateway restart
- ❌ **Reading gateway.log without confirming process PID** — log may be stale from a previous process instance
- ❌ **Using local model for Vietnamese when Groq is available** — Groq Whisper (large-v3) free tier is significantly more accurate than local medium, with lower latency
- ❌ **Kết luận "voice không tới" khi chưa check log** — 2026-08 thực tế: voice message VÀO đủ (log `Cached user voice at ...audio_xxx.ogg` + `inbound message` msg='') nhưng downstream agent (OpenClaw) kêu không nhận vì Hermes transcribe xong QUÊN forward text qua inbox. Debug 2 bước: (1) `grep "Cached user voice" gateway.log` xác nhận đã nhận + file tồn tại trong `audio_cache/`, (2) nếu có cả "Cached" + "inbound message" thì STT đã chạy — vấn đề nằm ở BƯỚC SAU (forwarding/xử lý tiếp), không phải STT. Đừng đổ lỗi voice/STT khi thực ra thiếu pipeline forward. **Fix AI Company:** `echo "<text>" | python D:/Hermes Proj/ai-company/shared/voice_to_claw.py` → gửi transcript qua inbox cho OpenClaw (`send(to='OpenClaw', subject='🎙️ Voice transcript')`) — pipeline Hermes transcribe duy nhất → forward Claw bắt buộc, không giữ im lặng. Chi tiết: skill `ai-company-ops`.
- ❌ **Kết luận "Groq account chưa verify / key chết" khi gặp 403 error 1010** — 1010 từ urllib/requests tự viết thiếu `User-Agent` = Cloudflare WAF chặn, KHÔNG phải vấn đề account (đã chứng minh 2026-09-12). Test lại bằng `_transcribe_groq()` hoặc thêm `User-Agent: openai-python/1.30.0` trước khi kết luận. Chi tiết: section 3 "Groq 403 error 1010".
- ❌ **Để mặc định `stt.groq.model` → Hermes dùng `whisper-large-v3-turbo` → BỊA transcript tiếng Việt** (audio 7,7s dài nội dung → trả về *"Xin chào các bạn."*, `success: true`, không log lỗi). Fix: `hermes config set stt.groq.model whisper-large-v3`. Verify bằng `tt.transcribe_audio(path)` (đọc config), không phải `_transcribe_groq(path,'model')`. Chi tiết + bảng so sánh: section 3 (2026-10-19).
- ❌ **Kết luận "STT hỏng / mạng lỗi / audio bị cắt" khi chưa so 2 model trên CÙNG file** — turbo và large-v3 cho ra 2 transcript khác hoàn toàn trên cùng 1 input. Triệu chứng giống hệt nhau, nguyên nhân khác nhau.
- ❌ **Groq transcribe tiếng Việt ra English** — thiếu `stt.groq.language` / `stt.language` trong config → auto-detect thiên vị English. Fix: `hermes config set stt.groq.language vi` + restart gateway (xem section 3).
- ❌ **Thêm English initial_prompt khi muốn code-switching Việt-Anh** — prompt tiếng Anh ("Keep English words in English: dashboard, deploy...") làm Whisper transcribe TOÀN BỘ sang English hoặc lặp prompt. `language: vi` đã tự xử lý code-switching; không cần prompt (xem section 3).
- ❌ **Sending files >25MB to cloud STT (Groq/OpenAI)** — these providers limit file uploads to ~25MB (OpenAI-compatible standard). Files exceeding this get silently rejected. Compress long recordings first using `meeting-transcriber` skill's `scripts/compress-audio.sh` (Opus mono, auto-bitrate, targets <20MB).
- ❌ **Gọi sai route khi transcribe qua Whisper server trên Mac (`192.168.1.3:9000`)** — route đúng là `POST /v1/audio/transcriptions` (OpenAI-compatible), KHÔNG phải `/inference` (trả `{"detail":"Not Found"}`). Cần boost/convert trước chỉ khi đẩy Groq; gọi server Mac thì trỏ thẳng file `.ogg` trong `audio_cache/`. Chi tiết: `references/remote-local-whisper-and-tts-sampling.md` mục 2b.

## 8. Verification Checklist

- [ ] STT config: `provider` set to `groq`
- [ ] `GROQ_API_KEY` set in `.env` and provider set to `groq`
- [ ] Gateway running (PID visible)
- [ ] Gateway log shows Telegram connected
- [ ] Sent test voice message and got readable transcription
- [ ] User confirmed quality is acceptable

## 9. Mac Whisper DHCP IP drift (2026-10)

Mac Mini 192.168.1.x **lấy IP mới mỗi lần DHCP lease refresh** — IP hardcode trong script bị thụt.
Session 2026-10 trace:

- 192.168.1.3 → ARP cũ (`1c-56-8e`), máy không còn ở IP này
- 192.168.1.5 → MAC `6a-7b-91-18-62-f4` — **Mac Mini hiện tại**, port 22 + 9000 OPEN
- Verify: SSH OK, `/health` trả `{"status":"ok","model":"large-v3","pid":34030}`

**Fix (apply to ALL 3 scripts):** thay IP hardcode bằng dynamic resolve. Resolver đã có: `scripts/mac_whisper_resolve.py`

```python
# Thay thế HOST = "192.168.1.3" trong 3 file:
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mac_whisper_resolve import resolve, PORT as MAC_PORT
host = resolve(force=True)   # trả "192.168.1.5" hoặc None
port = MAC_PORT             # 9000
```

**3 file cần patch:**
- `scripts/stt_mac_wrapper.py` — `host = "192.168.1.3"` (dòng 18)
- `scripts/stt_mac_local.py` — `HTTPConnection("192.168.1.3", 9000)` (dòng 56)
- `scripts/watchdog_mac_whisper.py` — `HOST = "192.168.1.3"` (dòng 8)

**Resolver hoạt động thế nào:**
1. mDNS hostname `Mac-mini-cua-kiem.local` → `socket.gethostbyname` → đúng IP
2. Fallback: cache IP trước đó (`~/.hermes/scripts/.mac_whisper_ip`)
3. Fallback cuối: sweep subnet `/24` tìm host có port 22+9000 OPEN (< 4s)

### ⚠️ ĐỪNG kết luận "máy tắt" khi ping fail — phân biệt 3 trạng thái bằng mã lỗi socket

Sai lầm đã xảy ra thật (2026-10, bị user sửa 2 lần: *"Mac của anh vẫn đang bật mà"*):
ping `192.168.1.3` 100% loss + SSH timeout → kết luận "Mac đã tắt, anh bật lại đi".
Sai. **IP đã đổi do DHCP**, máy vẫn chạy (uptime 71 ngày). Ba lần liên tiếp đưa user
đi sai hướng vì chỉ dựa vào ping.

**Bẫy thứ nhất — ARP entry cũ NẰM LẠI sau khi IP đổi.** `arp -a` vẫn hiện
`192.168.1.3 → 1c-56-8e-...` (dynamic), trông y như máy còn ở đó. ARP cache không
tự xoá khi host rời IP. **ARP entry ≠ host đang sống.** Xoá ARP cần quyền admin
(`arp -d` → *"requires elevation"*), nên đừng tính vào đường thoát.

**Bẫy thứ hai — ping không phân biệt được "host chết" với "host sống nhưng service chết".**
Phải đọc mã trả về của `socket.connect_ex`:

| Mã | Nghĩa | Suy ra |
|----|-------|--------|
| `0` | OPEN | host sống, service đang nghe |
| `10061` | REFUSED | **host SỐNG**, không có gì listen ở port đó |
| `10035` / `10060` | timeout | host không phản hồi: chết, hoặc IP đã đổi, hoặc firewall chặn |

`10061` là mảnh ghép quan trọng nhất: nó chứng minh máy đang chạy. Trong session này
`192.168.1.2` trả REFUSED ở mọi port → Mac đang bật, chỉ là chưa bật sshd/whisper.
Ping cùng lúc đó lại fail. **Ping fail + REFUSED = IP đổi.**

**Quy trình đúng — quét theo SERVICE PORT, không quét ping:**

```python
# sweep /24 tìm host đang mở đúng port service — bắt được cả khi IP đổi
import socket, concurrent.futures
def probe(i, port=9000):
    s = socket.socket(); s.settimeout(1.2)
    try:    return f"192.168.1.{i}" if s.connect_ex((f"192.168.1.{i}", port)) == 0 else None
    finally: s.close()
with concurrent.futures.ThreadPoolExecutor(max_workers=80) as ex:
    print([r for r in ex.map(probe, range(1, 255)) if r])
# → ['192.168.1.5']   ← đây mới là Mac
```

Validate sweep trước khi tin kết quả: probe một cặp (IP, port) ĐÃ BIẾT là mở
(vd SMB `445` của chính máy đang chạy) — phải trả `0`. Nếu sweep báo "không tìm thấy
gì" mà cả gateway lẫn máy local cũng biến mất → sweep sai, không phải mạng sạch.

**mDNS không đáng tin trên máy Windows này:** `socket.gethostbyname('Mac-mini-cua-kiem.local')`
và `ping mac-mini.local` đều fail (`gaierror` / *"could not find host"*) dù máy cùng
subnet. Vì vậy resolver phải có **sweep làm fallback thật**, không dựa vào hostname.

**Quy tắc bàn giao:** khi user nói máy vẫn bật mà mình đo ra "chết", **đo lại bằng
đường khác trước khi khuyên user đi bật máy**. Cụ thể: quét port service + kiểm tra
MAC trong ARP + xác nhận mạng nền còn tốt (ping gateway 192.168.1.1). Sai hướng
"máy anh tắt rồi" tốn công user và làm mất tin cậy.

**Diagnosis recipe (Windows git-bash):**
```bash
# 1. ARP table — MAC address là dấu hiệu chắn nhất, không phải IP
arp -a | grep "192.168.1" | grep -v multicast | grep -v broadcast

# 2. Sweep subnet tìm máy mở port 22 + 9000
for i in $(seq 1 254); do
  (python -c "import socket;s=socket.socket();s.settimeout(0.7);
   print('$i', 'OPEN' if s.connect_ex(('192.168.1.$i',9000))==0 else 'closed');s.close()") 2>/dev/null &
done | grep OPEN

# 3. SSH test (paramiko — git-bash không có sshpass)
python -c "
import paramiko
c=paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('192.168.1.5', username='tquang', password='<PASSWORD>', timeout=20)
i,o,e = c.exec_command('hostname; uptime; scutil --get ComputerName')
print(o.read().decode())
"

# 4. Whisper health
curl -sf http://$(python -c "from scripts.mac_whisper_resolve import resolve; print(resolve())"):9000/health
```

> **🧩 Related:** `references/mac-whisper-dhcp-ip-drift.md` — trace chi tiết từng IP/MAC, diagnosis recipe, resolver usage.
> **🧩 Related:** `references/voice-confirmation-workflow.md` — Transcribe → Confirm → Execute pattern after STT is working.
> **🧩 Related:** `references/meeting-review-workflow.md` — Meeting pipeline: trình toàn bộ transcript để user duyệt → task list từng bước → chốt phương pháp → chạy nhiều PA so sánh HTML (user workflow 2026-08).
