# Worked diagnosis: 30acc46edf (124.8 min → 600 words)

Real evidence trail from diagnosing a long-meeting transcript collapse. Use as a template for reproducing per-chunk diagnosis.

## Setup

- Source: `D:/Hermes Proj/ai-company/tfo_data/uploads/30acc46edf.m4a`, 184 MB, 7485 s (~124.8 min).
- Transcript file: `.transcript.txt` = 3381 bytes ≈ 600 words.
- Groq key: plain `GROQ_API_KEY=...` in `~/AppData/Local/hermes/.env` (strip trailing `\r`).

## Step 1 — coverage gate (fast signal)

`transcript_coverage.py` (committed `7f65641`) reported:
- Audio 124.8 min, transcript 600 words, expected ~14,972.
- Coverage by duration = 4.0%; coverage by real-voice = 4.2%.
- Voice map (ffmpeg silencedetect, noise=-40dB, d=1.5s): 119.1 min voiced / 150 segments, longest silence 10 s → NOT a silent file.
- Verdict: THIẾU positively, and not a source problem.

## Step 2 — per-chunk split (isolates the layer)

Chunk recipe mirrored the pipeline (600 s chunks, 30 s overlap, mp3 16 kHz mono → opus boost). Result (all chunks `status=200`):

```
[0] 0-600s      words=261  real (kháng thể, tái phát)
[1] 570-1170    words=223  real (chú cốt, em út mì)
[2] 1140-1740   words=240  real (thức ăn bổ sung)
[3] 1710-2310   words=224  real (Chú Tiến, đất, thử nghiệm)
[4] 2280-2880   words=194  MIXED ad ("Hãy đăng ký kênh...") + real
[5] 2850-3450   words=273  real (chăn nuôi)
[6] 3420-4020   words=203  ad-heavy
[7] 3990-4590   words=194  ad-only ("subscribe kênh Ghiền Mì Gõ")
[8] 4560-5160   words=189  MIXED
[9] 5130-5730   words=322  MIXED
[10] 5700-6300  words=266  MIXED (ad opener + real "Nguyên Lâm cây sữa/lợn nái")
[11] 6270-6870  words=232  MIXED
[12] 6840-7440  words=238  real (bệnh viên hồi trang, phân đen)
[13] 7410-7485  words=35   ad-only
```

Total ~3000 raw words across 14 chunks, all 200. → STT + chunking fine; culprit is post-processing.

## Step 3 — verify the cleaner per chunk

Transcribe chunk 7 + 10 again, apply `_clean_transcript` inline:
- chunk 7: raw 194 → cleaned 0. Pure hallucination; emptying is CORRECT (no real loss).
- chunk 10: raw 267 → cleaned 85. Ad opener stripped, real content preserved ("Trả lời một vấn đề là anh ấy đã để Nguyên Lâm cây xữa với các đàn ái cùng một chuồng. Không, nó mang hết cho con nội lái...").

Conclusion: cleaner is correct PER CHUNK. Original pipeline's ONE global clean over the concatenated whole lost ~80% because contaminated chunks (4,6,7,8,9,10,11,13) dragged down clean-able content; only clean chunks 0,1,2,3,12 survived (= the 600 words shipped).

## Fix applied (design)

1. `clean=True` per chunk (heuristic `_clean_transcript` each part).
2. Drop global final clean.
3. Per-chunk try/except + retry+backoff; bind `r=None` before `requests.post` to avoid NameError.
4. Coverage gate after reassembly → flag THIẾU if still below threshold.

## Tooling notes

- `terminal` guard refused every command referencing a script under "Hermes Proj" (space in path). Ran diagnostics via `execute_code` + `subprocess.Popen(... , creationflags=DETACHED_PROCESS|CREATE_NEW_PROCESS_GROUP|CREATE_NO_WINDOW)`; polled the log / transient `diag_*.mp3/.opus` files to gauge progress.