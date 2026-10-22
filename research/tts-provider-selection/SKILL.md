---
name: tts-provider-selection
description: Compare TTS providers; pick Vietnamese HD voices.
---

# TTS Provider Selection

Class-level skill for researching, comparing, and recommending TTS providers (text-to-speech). Optimized for Vietnamese-language use cases (đọc nội dung tiếng Việt tự nhiên, ấm, truyền cảm) but applicable to any language.

## When to use
- User wants to pick a TTS voice/provider ("giọng TTS nào mượt", "đọc content tiếng Việt", "chọn giọng audio")
- Need to compare price / quality / Vietnamese support across providers
- Need an authoritative current list of voices per provider

## Verified landscape (2026) → `references/vietnamese-tts-landscape.md`
Contains verified-from-vendor data: exact Vietnamese voice names, gender, prices per 1M chars, API-key requirements, and which models actually support Vietnamese. Re-read that file before answering — it is the source of truth for figures.

## Key pitfalls (learned the hard way)
- **ElevenLabs `eleven_multilingual_v2` does NOT support Vietnamese** (only 29 langs, no `vi`). Vietnamese IS supported on **`eleven_v3`** (70+ langs incl. `vie`) and **`eleven_flash_v2_5`** (adds `hu, no, vi`). Do not recommend "Multilingual v2" for Vietnamese — this is a common wrong answer.
- **Azure now has a 3rd Vietnamese voice**: `vi-VN-Linh:MAI-Voice-2-Flash` (Female, "Neural HD Flash", LLM-based, emotion-aware) alongside `HoaiMyNeural` (F) and `NamMinhNeural` (M). Check the language-support page for the latest.
- **Google Chirp3-HD** is the current quality leader for VN at a good price: 30 voices `vi-VN-Chirp3-HD-*` at **$30/1M chars** (verified), vs ElevenLabs $100/1M for v3.
- Never trust memory on prices/voice lists — re-verify from vendor pages this year; prices change. All figures in the reference file carry a session date.
- AWS Polly's available-voices page **lazy-renders its table**; a plain grep of the HTML finds nothing. Use the **download Markdown link** (`available-voices.md`) or the browser to read the table.

## Workflow: scraping vendor doc pages (the reliable path)
Heavy JS-rendered vendor doc pages (Google Cloud docs, AWS docs) often fail/timeout in a browser navigate. The reliable path that worked:
1. `curl -sL <url> -A "Mozilla/5.0 ..." -o out.html` via terminal (save to a writable cwd like `D:/Hermes Proj/tmp_tts/`).
2. Parse rows with a python regex, e.g. Google voices:
   `re.findall(r'<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>([a-z]{2}-[A-Z]{2})</td>\s*<td>([^<]+)</td>\s*<td>([^<]*)</td>', html)` → tuple = (Language, VoiceType, locale, VoiceName, SSML Gender).
3. For pricing, also curl the `/pricing` page and strip tags via `re.sub(r'<[^>]+>',' ',html)`, then grep near keywords like "Chirp 3: HD voices" / "per 1 million characters".
4. Run `browser_console` with `document.body.innerText` + `indexOf(...)` to extract a targeted section from an already-open page (faster than full snapshots).

## Output format for the user
Markdown table with columns: Provider | Voice | Gender | Quality | Price | API key needed? | Vietnamese OK? — followed by a TOP-3 recommendation for the stated use-case with reasons + cost math, and a note on which options are usable immediately (existing keys) vs need a new key. Only state figures verified from source; explicitly mark anything unverified rather than guessing.

## Next-action for incomplete runs
If a run ends before verifying all providers (e.g. Zalo/Vbee/Viettel/FPT/VinAI), finish verification on a later session and update the reference file — do not report unverified prices as fact.