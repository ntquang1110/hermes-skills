---
name: critique-council
description: "Use when: 4-agent council evaluates ideas (BSIJ)."
category: productivity
version: 1.1.0
---

# Critique Council

## Tong quan

Dieu phoi 4 agent: Believer (tim co hoi), Skeptic (tim diem yeu), Investor (tai chinh), Judge (verdict).

## Pipeline

```
Input → Believer + Skeptic + Investor → Judge (Python) → HTML publish
```

## Running the Council

### Primary: via chat (manual trigger)

User sends an idea → load `critique-council` → run the 4 roles → return verdict + HTML link.
No setup needed. Session context persists per chat, so follow-up questions ("what about GUT?")
reuse everything already established.

### CLI fallback: `council_full.py`

```
python council_full.py --idea "<idea>" --lite
```

**5 verified pitfalls — all cost real debugging time:**

1. **`hermes chat` does not exist.** `chat` is not a subcommand. Correct form is
   `hermes -z <prompt_file> --cli --yolo`. Wrong form returns ~1040 chars of usage text
   that a naive length check happily treats as a real report. Guard with
   `out.startswith("usage:") or "invalid choice:" in out`.

2. **Windows stdout defaults to cp1252 → Vietnamese diacritics destroyed.**
   Must pass `PYTHONIOENCODING=utf-8` + `PYTHONUTF8=1` in the subprocess env AND
   `result.stdout.decode("utf-8", errors="replace")`. Verify with a non-ASCII count
   (healthy run = 400-600 non-ASCII chars).

3. **Strip the `[Humalike]` auth banner** from stdout, plus the `⚠ Deprecated .env settings`
   block. Both prepend before the actual response.

4. **The 3 agents must run SEQUENTIAL.** Three concurrent `hermes` processes exhaust the
   machine and the third times out — silently returning a `[LOI]` string that the old Judge
   scored as a default 5.0/10. Sequential costs 8-10 min but always returns real data.

5. **`delegate_task` has no CLI equivalent.** It is a tool callable only inside a Hermes
   agent session. Spawning subagents from a plain Python script requires `hermes -z` subprocesses.

6. **Output can be truncated mid-response, and length is not a health signal.**
   Observed: believer returned 1275 chars cleanly and stopped — no JSON, no error, exit 0.
   The same agent returned 4176 chars with valid JSON on an immediate rerun. Validate on
   `f'"{key}"' in output` (key = confidence/risk_score/verdict per agent), not on size.
   Raise the subprocess timeout to 420s and retry up to 2 times — truncation and quota
   errors are both transient. A genuinely short response with the JSON present is valid.

### Judge must never invent a score

The scoring formula defaults (`confidence=5`, `risk_score=5`, `verdict="MAYBE"`) look
harmless and are the exact defect that made this pipeline lie. When any of the 3 agents
fails or emits malformed self-critique JSON, the verdict is `INCOMPLETE` and
`total_score` is `None` — never 5.0.

Reason: `MORE-DATA` reads like a considered judgment ("we need more evidence, go look").
A reader has no way to know it was auto-generated from missing input. `INCOMPLETE` is
the honest signal.

Validate before scoring: type must be numeric (reject `"high"`), range 0-10 (reject 99),
verdict must be one of `INVEST|MAYBE|PASS` (reject `"MUA"`). A bare `except: pass` around
JSON parsing silently empties the score dict and produces a wrong verdict.

**Regression gate — run these before trusting any change:**

```python
run_judge({'believer':'[LOI]','skeptic':'[LOI]','investor':'[LOI]'}, 'x')  # INCOMPLETE
run_judge({'believer':'{"confidence":"high"}','skeptic':'{"risk_score":4},
           'investor':'{"verdict":"INVEST"}'}, 'x')                        # INCOMPLETE
run_judge({'believer':'{"confidence":99},'...}, 'x')                      # INCOMPLETE
run_judge({'believer':'{"confidence":8}','skeptic':'{"risk_score":4},
           'investor':'{"verdict":"INVEST"}'}, 'x')                        # GO, 8.0
```

### Known scaling limit

Each agent is a fresh Hermes process with its own context and skill load. 8-10 min for
one idea. Ten ideas = 80-100 min. This CLI is for batch/overnight evaluation and regression
audits, not for interactive use — chat-triggered council is the interactive path.

### KNOWN DEFECT — the score is not calibrated, do not present it as a measurement

The scoring formula in `council_full.py` is **not validated**. Read this before
quoting any verdict to a user or a partner.

```python
feasibility = max(0, believer_conf - max(0, skeptic_risk - 5))
market      = max(0, believer_conf - max(0, skeptic_risk - 5))   # identical line
```

Two defects:

1. **60% of the weight is one variable multiplied by two.** Those two lines are the
   same computation. The formula is effectively 2 dimensions, not 3. `0.3X + 0.3X + 0.4Z`
   carries no more information than `0.6Y + 0.4Z` — keeping the duplicate line makes the
   output look more rigorous than it is.

2. **The three agents are not independent.** A high skeptic risk lowers both feasibility
   and market through the same subtraction, so Skeptic controls 60% of the score with a
   single claim. And the number it produces is a probability-weighted estimate, not a
   verified fact — "the idea looks hard" is not "the idea is hard".

The thresholds (>7 GO, >5 CAUTIOUS, >3 MORE-DATA) are equally arbitrary. Nothing has been
calibrated against known outcomes.

**So: a 4.4/10 is an impression with a decimal point on it.** The written analysis has
real value — the CAC/LTV math, the TĂBS registration constraint, the channel conflict
are all substantive findings worth reading. The number is not.

**Fix options, not yet chosen:**
- Separate the dimensions — Skeptic subtracts only from feasibility; market comes from
  Believer alone. Or add a `market_killer` field to Skeptic's schema when Skeptic has a
  genuine demand-side objection.
- Drop the score, keep three separate verdicts. Believer GO / Skeptic NO-GO / Investor
  MAYBE surfaces the disagreement directly instead of averaging it into a plausible
  midpoint. Score is easier to track over time; verdict is easier to act on.
- Calibrate: run 5-10 ideas with known outcomes, fit the weights and thresholds.

Until someone picks one, present the analysis and label the score uncalibrated.

### Publish

POST directly to `https://preview.thefirstonly.com/api/store`. Do not use the
`content-upload.py` script — it runs html-unslop, which strips Vietnamese diacritics.

## Che do

| Che do | Token | Khi nao |
|---|---|---|
| full | 60-150K | SP moi, hop tac, dau tu |
| lite | 20-50K | Y kien nhanh |
| quick | 0 | Anh tu cham diem |

## Cach dung

```bash
python company.py council --idea "Mo ta..." --publish
python company.py council --file idea.md --lite
```

## Self-critique built-in

Moi agent ghi JSON self-critique. Judge doc de kiem tra consistency.
