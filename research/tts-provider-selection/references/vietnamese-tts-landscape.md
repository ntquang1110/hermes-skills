# Vietnamese TTS Landscape — verified from vendor pages (Sep 2026)

All figures verified directly from official vendor docs in a Sep 2026 session. Re-verify before quoting in later sessions — prices/voice lists change.

## Microsoft Azure TTS (tts tab of language-support page)
| Voice | Gender | Type | Notes |
|---|---|---|---|
| `vi-VN-HoaiMyNeural` | Female | Standard | long-standing neural, smooth |
| `vi-VN-NamMinhNeural` | Male | Standard | deep male voice |
| `vi-VN-Linh:MAI-Voice-2-Flash` | Female | **Neural HD Flash** | **NEW 2026** — LLM-based HD voice, auto emotional cues, adjusts tone by context |

- Supports SSML; standard voices at 24kHz & 48kHz.
- Neural standard price ~$15/1M chars (not directly verified this session — mark as such).

## Google Cloud TTS (voices + pricing pages)
- **Chirp3-HD (Premium), 30 voices `vi-VN-Chirp3-HD-*`** — 15 Female / 15 Male (e.g. Aoede, Autonoe, Callirrhoe = F; Charon, Enceladus, Fenrir = M). Current quality leader for VN.
- `vi-VN-Neural2-A` (F), `vi-VN-Neural2-D` (M) — older neural.
- `vi-VN-Wavenet-A/B/C/D`, `vi-VN-Standard-A/B/C/D` — legacy.
- **Pricing (verified):** Chirp3 HD voices **$30/1M chars** (0–1M free); Neural2 **$16/1M**; WaveNet/Standard **$4/1M**; Studio **$160/1M**; Instant custom voice $60/1M.
- **Gemini TTS (Gemini API, supports Vietnamese):** Gemini 2.5 Flash TTS — input $0.50/1M text tokens, output **$10/1M audio tokens (~25 tokens/sec)**; Gemini 2.5/3.1 Pro — $1 input / $20 output. Granular prompt control over emotion/voice.

## ElevenLabs (docs/overview/models + pricing/api)
| Model | Vietnamese? | Price (API) | Notes |
|---|---|---|---|
| `eleven_v3` | **YES** (`vie`) | **$0.10/1K chars = $100/1M** | 70+ langs, most emotional; 5,000 char limit |
| `eleven_v3_conversational` | YES | $0.05/1K ($50/1M) | ~280ms low latency |
| `eleven_flash_v2_5` | **YES** (`vi`) | $0.05/1K ($50/1M) | 32 langs = v2's 29 + hu,no,vi; 40,000 char limit |
| `eleven_multilingual_v2` | **NO** (29 langs, no vi) | $0.10/1K ($100/1M) | ⚠️ common trap — NOT for Vietnamese |
| `eleven_flash_v2` | NO (en only) | — | older |

- Free tier ~10K chars → enough to test a v3 voice before paying. Creator plan $22/mo (first month $11) includes 220K chars.

## Amazon Polly (available-voices page — lazy-rendered table)
- Traditional VN voices: Hanna (F), Lam (M).
- ⚠️ In Sep 2026 the available-voices page table snapshot did NOT show a Vietnamese row (lazy-render / possibly removed). Page has a "Download Markdown" link (`available-voices.md`) — use it to read the table reliably. Re-verify Hanna/Lam availability.

## Vietnamese domestic providers — NOT verified this session (fetch ran out of turns)
Do NOT quote prices for these as fact until verified from their own sites:
- **Zalo AI (Zalo TTS)** — many native VN voices, generous free tier; needs Zalo developer account.
- **Vbee AIVoice** — popular for audiobook/radio-style VN reading.
- **Viettel AI TTS** — newsreader-style VN voices.
- **FPT AI TTS** — diverse domestic VN voices.
- **VinAI VieNeu** — open-source VN TTS on HuggingFace, self-hostable, free.

## TOP-3 picks for "đọc nội dung tiếng Việt tự nhiên, ấm, truyền cảm" (Sep 2026)
1. **Google `vi-VN-Chirp3-HD-*`** — best price/quality: $30/1M (~$0.15 for a 5k-char article), 30 voices to pick warm/deep, SSML.
2. **ElevenLabs `eleven_v3`** (or Flash v2.5) — most human/emotional; $100/1M (v3) / $50/1M (Flash); free tier to audition.
3. **Azure `vi-VN-HoaiMyNeural`** or new `vi-VN-Linh:MAI-Voice-2-Flash` — stable + new emotion-aware HD female.

Note in recommendation whether key already available (e.g. existing Azure/Google key) vs needs purchase.