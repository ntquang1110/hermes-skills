# TikTok Pipeline — Verified Examples

## Example 1: Daniel H. Pink — "4 ways to act before you feel ready"
- URL: `https://vt.tiktok.com/ZSqs1Ms5W/`
- Creator: @daniel_h_pink
- Subs: eng-US (auto-captions available)
- Content: Self-help/motivation — act before feeling ready
- Draft: `threads_drafts/tiktok_daniel_pink_act_before_ready.txt`
- Chars: 1821, 4 parts, max 490
- Queue: `tiktok-daniel-pink-act-before-ready-2026-12-01`

## Example 2: Beau — "Pre-selling" (marketing for coaches)
- URL: `https://vt.tiktok.com/ZSqsdNnnq/`
- Creator: @beausbrain
- Subs: eng-US (auto-captions available, 5.6KB vtt)
- Content: Business/marketing — pre-selling through content (desires, frustrations, beliefs)
- Draft: `threads_drafts/tiktok_preselling_beau.txt`
- Chars: 1926, 5 parts, max 473
- Queue: `tiktok-preselling-beau-2026-12-02`

## Example 3: Travis Kalanick — "Excellence is pain"
- URL: `https://vt.tiktok.com/ZSqsdyS7A/`
- Creator: @businessblurb (interview Travis Kalanick x David Senra)
- Subs: eng-US (auto-captions available, 1.8KB vtt)
- Content: Business mindset — marathoner at mile 21, pain = excellence
- Draft: `threads_drafts/tiktok_travis_kalanick_pain.txt`
- Chars: 1555, 4 parts, max 496
- Queue: `tiktok-travis-kalanick-pain-2026-12-03`

## Processing Notes

### Command pattern that works:
```bash
cd /c/Users/NTQUANG_DELL/hermes-temp/tiktok
python -m yt_dlp --impersonate "Chrome-131" --write-subs --sub-langs "eng-US" --skip-download --sub-format vtt -o "output" "URL"
```

### Impersonate target pitfall:
- `--impersonate "Chrome-131:Windows-10"` → FAILS (target not available)
- `--impersonate "Chrome-131"` → WORKS (use bare client name without OS)
- After `pip install --upgrade yt-dlp curl_cffi`, verify with `--list-impersonate-targets`

### Queue ID convention:
`tiktok-<topic-slug>-YYYY-MM-DD` with `"source": "tiktok"` field.

### Processed tracking:
TikTok URLs go into `youtube-processed.json` under `tiktok_urls[]` (separate from `video_ids[]`).
