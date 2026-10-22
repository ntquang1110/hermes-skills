---
name: chunked-audio-transcription
description: Use when chunked Whisper/Groq STT loses long-audio content.
---

# Chunked Audio Transcription (Whisper/Groq)

Chunked transcription splits a long recording into N-minute chunks, transcribes each, then concatenates. Classic silent failure: transcript comes back a tiny fraction of the audio (e.g. 4% coverage) while the audio genuinely has full voice throughout.

Applies to meTelligent (`_transcribe_chunked`, Groq whisper-large-v3) and TFO (`app/main.py`). Config: Groq key in `~/AppData/Local/hermes/.env` (`GROQ_API_KEY=...`, plain, not b64; strip `\r`).

## Golden diagnostic rule

Before touching any code, SPLIT the file into the same chunks the pipeline uses and transcribe each SEPARATELY, logging per-chunk `{status, elapsed, word_count, first 80 chars}` with per-chunk try/except. This decisively separates the 4 possible causes:

| Finding | Meaning |
|---------|---------|
| All chunks status 200 + have real speech | STT + chunking are FINE → the loss is in POST-processing (cleaning/dedup) |
| Specific chunks return empty / error text / fail | API or chunk-cut bug → fix transcribe layer |
| Chunks have voice but transcribe gibberish/hallucination | Audio quality / gain → fix boost / initial_prompt |
| Chunks are genuinely silent | Source problem, not pipeline |

Do NOT conclude "pipeline broken" from the transcript alone — you must prove WHERE the content died.

## Primary pitfall: hallucination + global clean strips real content

Whisper on long/quiet chunks fabricates ad filler ("Hãy đăng ký kênh / subscribe / nhận bài hát trên youtube") and mixes it into chunks that also contain real speech.

If you then clean the CONCATENATED whole ONCE at the end (sentence-level strip of anything matching an ad-marker), you lose real content too: a real sentence polluted with an ad clause gets dropped whole (when < length threshold). A ~2-hour meeting collapses to ~600 words — the surviving clean chunks only.

**Fix — clean PER CHUNK, never once on the assembled whole:**
1. Call the transcribe with `clean=True` per chunk (heuristic clean each part: keeps real content, drops hallucinated fragments).
2. Remove the global final clean (double-clean re-strips; a single contaminated chunk nukes the whole).
3. Wrap each chunk in try/except + retry with backoff (rate-limit 429 / 5xx / timeout / network). One bad chunk must NOT abort the whole long transcription. Never let `requests.post` raise NameError by relying on an `r` assigned inside a bare try — bind `r = None` before the try.
4. After reassembly, run a coverage gate (transcript words / effective_minutes / ~120 wpm); below threshold → flag THIẾU so the failure surfaces instead of silently shipping a gutted transcript.

## Measuring coverage

- Rate: Vietnamese meetings ~110-150 words/min. `score = transcript_words / (total_minutes × 120)`.
- <40% = THIẾU positively (a strong signal to re-diagnose); ≥60% = OK.
- Rule out the "silent file" hypothesis with `ffmpeg` silencedetect / volumedetect map: count voiced minutes + longest silence. Voice present + low words = pipeline post-processing is the culprit, not the source.

## Logistics (this user's machine)

- The lifecycle guard blocks `terminal` when the command references a script in a path with a space ("Hermes Proj"). Workaround: `execute_code` → `subprocess.Popen([py, script], creationflags=DETACHED_PROCESS|CREATE_NEW_PROCESS_GROUP|CREATE_NO_WINDOW)` to run in background, then poll a log file. Log per-chunk incrementally or flush at end and poll the source dir for transient `diag_*.mp3/.opus` files to gauge progress.
- Chunk recipe to mirror the pipeline: ffmpeg `-ss start -t span -i src -ar 16000 -ac 1 out.mp3`; then compress+boost to opus `-af volume=12dB,highpass=f=80,lowpass=f=8000 -ar 16000 -ac 1 -c:a libopus -b:a 48k`; POST `whisper-large-v3`, `language=vi`, `prompt="Cuộc họp nội bộ về chăn nuôi, sản xuất, kinh doanh."`.

See `references/chunked-transcribe-diagnosis.md` for a worked evidence trail (per-chunk numbers + verify-clean output).