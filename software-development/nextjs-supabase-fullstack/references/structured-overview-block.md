# Structured metadata block inside markdown content

Pattern for giving content cards a **real, AI-generated structured summary** without schema changes — store a JSON blob inside the card's markdown content, wrapped in HTML comments, and have the client parser extract it.

## Why

Rule-based parsing (regex over markdown) can never truly "understand" an article — it scrapes numbers and sentences but produces a shallow overview. The durable fix is to generate a structured overview **at content-creation time** (when the AI author writes the card), embed it in the content, and let the UI render it as real sections. Old cards get backfilled later by an LLM batch job.

## Format

```markdown
<!--OVERVIEW-->{"what":"Định nghĩa 1-2 câu","why":"Vì sao quan trọng","mechanism":["Bước 1","Bước 2","Bước 3"],"players":["Thành phần 1","Thành phần 2"],"applications":["Ứng dụng 1","Ứng dụng 2"],"limits":"Hạn chế/tranh cãi","analogy":"Ví von dễ hiểu"}<!--/OVERVIEW-->

## Nội dung thực của bài viết...
```

- HTML comments are chosen so the block is invisible when markdown renders raw (safe if a consumer forgets to strip it).
- It MUST be the first thing in content, before any `##` heading, so the parser finds it trivially.

## Parser extraction (client-side)

```typescript
function parseAzuEasy(card: Card) {
  let content = card.content || "";
  let overview: OverviewData | null = null;

  const ovMatch = content.match(/<!--OVERVIEW-->\s*(\{[\s\S]*?\})\s*<!--\/OVERVIEW-->/);
  if (ovMatch) {
    try {
      overview = JSON.parse(ovMatch[1]);
      // Strip the block so it never pollutes the academic/detail tab
      content = content.replace(/<!--OVERVIEW-->[\s\S]*?<!--\/OVERVIEW-->\s*/g, "").trim();
    } catch { /* fall through to rule-based parser */ }
  }
  // ...if overview exists, use its fields (what/why/mechanism/players/applications/limits/analogy)
  // ...else fall back to the old regex-based extraction
}
```

Render as distinct labeled blocks: `what` → 5-second hero, `why` + `mechanism` + `players` → 1-minute tier, `applications` + `limits` → deep-dive tier. Fall back to the regex parser whenever `overview` is null so old cards still render.

## Cron prompt requirement

The cron/research prompt that creates cards must mandate the block. Give the exact format + field semantics so the LLM emits valid JSON:

```
BẮT BUỘC THÊM OVERVIEW BLOCK (đầu content):
<!--OVERVIEW-->{"what":"...","why":"...","mechanism":["..."],"players":["..."],"applications":["..."],"limits":"...","analogy":"..."}<!--/OVERVIEW-->
- what: câu chốt 1 câu
- why: vì sao quan trọng
- mechanism: 3-5 bước (mảng string)
- players: 3-6 thành phần chính
- applications: 2-4 ứng dụng
- limits: 1-2 câu hạn chế/tranh cãi
- analogy: 1 câu ví von
```

## Backfill old content (resume-able LLM batch)

Working script: `C:\Users\NTQUANG_DELL\knowledge-flow\scripts\backfill-overview.py`. Pattern worth copying:

1. **Progress file** (`data/backfill-progress.json` with `{"done": [cardId, ...]}`) — skip already-done IDs on restart. Batch LLM jobs WILL be interrupted; resume is mandatory.
2. **Skip logic** — only process cards where `"OVERVIEW" not in content` (idempotent).
3. **LLM call** — POST to the OpenAI-compatible endpoint (`https://opencode.ai/zen/go/v1/chat/completions`, model `deepseek-v4-flash`), prompt demands "CHỈ TRẢ VỀ JSON THUẦN".
4. **Robust JSON parse** — strip markdown fences, then `text[text.find("{"):text.rfind("}")+1]`, then `json.loads` to validate; wrap in try/except per card so one bad card doesn't kill the run.
5. **PATCH per card** via the app's `PATCH /api/cards?id=<id>` with `{content: "<!--OVERVIEW-->"+ov+"<!--/OVERVIEW-->\n\n" + oldContent}`.
6. `time.sleep(1)` between cards to be gentle on the server.

### LLM JSON output pitfalls (each caused a real failed run)

- **`max_tokens` too small → truncated JSON, no closing `}`**: first run used `max_tokens=1200`; the overview JSON (with `mechanism`/`players`/`applications` arrays) got cut off mid-object, so `text.rfind("}")` returned `-1` and the whole card failed. Use `max_tokens=2500` minimum, and **retry the card up to 3×** — a truncated response on retry usually completes.
- **Trailing commas**: the LLM routinely emits `,}` / `,]` (trailing comma before closing brace/bracket) → `json.JSONDecodeError: Illegal trailing comma`. Clean before parsing:
  ```python
  raw_json = raw_json.replace(",\n}", "\n}").replace(",}", "}").replace(",\n]", "\n]").replace(",]", "]")
  ```
- **Validate required fields**: after `json.loads`, check `parsed.get("what")` is non-empty — the LLM can return a valid-JSON shell with empty fields. Treat as failure and retry.
- **Retry shape**: wrap the whole LLM call in `for attempt in range(3)`; on JSONDecodeError or missing-braces, `time.sleep(3)` and re-send the same prompt. ~1 in 10 calls fails once; with retries the batch completes 100%.

## API key gotcha (Hermes .env)

`OPENCODE_GO_API_KEY` in `~/AppData/Local/hermes/.env` is stored **with surrounding double quotes** (`"sk-..."`). Strip them before use:

```python
raw = line.split("=", 1)[1].strip()
key = raw.strip('"\'')   # REQUIRED — otherwise LLM returns 401 Invalid API key
```

Do NOT base64-decode it — it's a plain sk- key, not the base64-encoded GITHUB_PAT pattern.

## Update flow for the PATCH endpoint

Add a `PATCH` handler to the existing cards route that accepts `content` (and optionally `summary`, `tags`, `title`, `source_url`), recomputes `reading_time_sec` from content length, and touches `updated_at`. Don't add columns for metadata that can live in the content block — schema-free wins for single-app prototypes.
