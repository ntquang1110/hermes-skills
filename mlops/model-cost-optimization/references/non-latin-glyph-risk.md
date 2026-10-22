# Non-Latin glyph injection into Vietnamese — includes API models (verified 2026-08-23)

## Claim being corrected
Earlier guidance framed non-Latin glyph injection as a **local-small-model-only** problem
("An 8B local model glitched a Korean hanja char..."). That framing is WRONG. In the same
session's parallel run, a large **API** model (deepseek-v4-pro via opencode-zen) produced the
SAME class of defect.

## Real data point (both from the SAME flow run, same topic "reward prediction error")
- **Local unsloth/Ministral-3-8B** → clean (0 non-Latin) — prompt had the "Latin + diacritics only" self-check rule.
- **Deepseek-v4-pro (API)** → injected a Mandarin char `喂` into the closing sentence, plus a
  nonsense token `trungCredential` ("tegmentum trungCredential (VTA)") that is meaningless Vietnamese/English.

## Why the quality gate does NOT catch it
Vietnamese content goes through an unslop/humanizer gate that hard-fails on **em dash** and
**emoji** and requires a min count of **diacritics**. A Korean/Mandarin glyph is neither em dash
nor emoji, and the surrounding sentence still has plenty of dấu — so the gate reports PASS while
the text is corrupted in front of the reader.

## Durable rule
Treat glyph-intrusion as a risk for **ANY** model-generated Vietnamese, local OR API. For every
content-gen path:
1. Add a prompt rule: "self-check for non-Latin characters (Latin alphabet + Vietnamese
   diacritics only) before saving."
2. Independently spot-scan the saved output, even when the quality gate asserts PASS:
   ```python
   import re
   nonlatin = sorted(set(re.findall(r'[^\x00-\x7F\xc0-\u1ef9\u0009\u000a\u000d]', text)))
   #  además check for arrow glyphs (→ U+2192) and obvious nonsense tokens
   #  e.g. "trungCredential" — regex for /[A-Z][a-z]+[A-Z]/ mid-word
   ```
   Example that caught it: `re.findall(r'[^\x00-\x7F\xc0-\u1ef9\u0009\u000a\u000d]', t)` on a
   draft scored 0 em dash / 0 emoji / 595 dấu yet still contained `喂` and `→`.

## A/B tier validation (which model is good enough for a flow)
To validate a cheaper/local tier against the incumbent API on the SAME pipeline:
- Copy the cron job's prompt; create a parallel cron pinned to the candidate model (pin via
  editing `jobs.json` — see SKILL.md), run both `cronjob action=run`.
- Have each write its draft to a SEPARATE subfolder (e.g. `unsloth/` vs root) so outputs don't
  collide and can be attributed.
- Compare on: factual accuracy (author/year/data), voice (mình/bạn, humor), verbatim-quote
  fidelity, glyph cleanliness, and depth. Local 8B here won on cleanliness+voice but was
  shallower technically (no temporal-difference / TD-learning math); API won on depth but
  introduced glyphs. "Gộp" (use API depth + local cleanliness) is the ideal, not either/OR.