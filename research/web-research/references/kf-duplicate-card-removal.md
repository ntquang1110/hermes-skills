# KF duplicate card removal — no DELETE API (tested Aug 2026)

## Incident
Cron research picked arXiv 2607.28576 ("Sample More, Reflect Less"). Pre-research
dedup scanned card titles with a keyword list `['ai','llm','model','transformer',
'agent','learning','neural','deep','gpt','reason','grpo','rl','robotics','chip',
'semiconductor','frontier']` — the existing card (created 2 days earlier) had the
exact same `source_url` but a **Vietnamese title with none of those tokens**, so the
scan passed and a full duplicate card was POSTed (201). The post-POST re-fetch of
`/api/cards` (matching the returned id + eyeballing the title list) revealed two
"Sample More" cards.

## Root cause
Dedup by English topical keywords fails when the card title is Vietnamese and/or
uses non-obvious phrasing. The canonical check for a paper-based card is the
`source_url` field (it stores the arXiv abs link), plus distinctive substrings from
the paper's own title (`sample more`, `reflect less`, `speculative`, `kv cache`...),
not generic category words.

## Fix — delete via Supabase REST (KF API has NO DELETE route)
- `DELETE /api/knowledge/<id>` → returns a 404 HTML page. The Next.js app defines
  `/api/knowledge` as POST-only and `/api/cards` as GET-only; there is no delete
  endpoint.
- Supabase REST DELETE works with the **anon key** from the app's `.env.local`
  (verified: HTTP 204). It lives next to the app at `knowledge-flow/.env.local`:

  ```
  # from knowledge-flow/.env.local
  NEXT_PUBLIC_SUPABASE_URL=https://<ref>.supabase.co
  NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable__...

  curl -s -X DELETE "https://<ref>.supabase.co/rest/v1/knowledge_cards?id=eq.<card-uuid>" \
    -H "apikey: $ANON" -H "Authorization: Bearer $ANON"
  # HTTP 204 = deleted
  ```

- Verify: re-fetch `/api/cards` → total drops by exactly 1 and the offending title
  is gone. (Total went 223 → 222 in the incident.)

## Prevention checklist for paper-based cards
1. **Before research**: fetch `/api/cards` and check whether any card's `source_url`
   contains the arXiv ID you plan to card. Zero matches required.
2. **Title-substring check too**: use distinctive tokens from the paper's own title
   (e.g. `sample more`, `reflect less`), not generic category words that a Vietnamese
   title would omit.
3. **After POST**: re-fetch cards, match the returned `id`, and eyeball the title
   list for near-duplicates. POST response alone is not proof of uniqueness.
