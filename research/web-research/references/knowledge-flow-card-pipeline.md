# Knowledge Flow card creation pipeline (Steps 0–6 + heuristics + pitfalls)

### Knowledge Flow card creation pipeline

When the research target is a Knowledge Flow (KF) instance (a self-hosted knowledge base at `localhost:3003`), follow this end-to-end pipeline to avoid duplication and produce ingestible cards:

**Step 0 — Check research queue first (CRON MODE)**
Call `GET /api/research-queue`; pick oldest `status:"pending"` item, research + card + `PATCH ?id=<id>&action=done` before self-directed topics. If queue empty → Step 1. For the 8-bài/ngày rotation cron (4 topic groups via `knowledge-flow/data/research-rotation.json`): see `references/research-rotation-cron.md`.

**⚠️ KF passcode gate (Aug 2026+):** KF (localhost:3003) is behind the `tfo_auth` passcode gate — ALL `/api/*` calls (queue, cards, POST knowledge) return `307 → /passcode` without the cookie, breaking cron pipelines with a silent JSON parse error. Add `Cookie: tfo_auth=1d1e977a218bfa01fe61106c360c8acf667047e35f17fdb0f1a8484e06cfdb55` to every curl/Python request. Full detail + topic_slug quirk: `references/kf-passcode-gate-cron.md`.

**Step 1 — Check existing cards first (MANDATORY)**

When KF has fewer than ~40 cards, the raw `curl` output is manageable. For larger KBs (50+ cards), the raw JSON can exceed 500KB and get truncated in the terminal buffer. Use the **enumerated compact view** to see all card titles with indices:

```bash
# Get compact view of ALL cards with index numbers (handles 100+ cards)
curl -s http://localhost:3003/api/cards | python -c "import sys,json; cards=json.load(sys.stdin); print(f'Total: {len(cards)} cards'); [print(f'{i}: {c[\"title\"][:90]}') for i,c in enumerate(cards)]"
```

- Scan the **full enumerated list** for any title whose keywords overlap >=60% with your planned topic
- Also check similarly-named cards for partial overlap (e.g. "cGAS-STING" vs "Interferon, PRRs & JAK-STAT")
- If the topic already exists → **skip it entirely**, pick a different angle
- This step prevents wasting API calls and cluttering the knowledge base
- **Paper-card dedup (⚠️ Aug 2026)**: keyword scans miss Vietnamese titles — check `source_url` for the arXiv ID + distinctive title substrings before POST. KF has no DELETE API; duplicates via Supabase REST: `references/kf-duplicate-card-removal.md`

**Step 2 — Choose a novel topic** not covered in existing cards. Prioritize topics that:
- Connect to downstream applications (feed additives, disease prevention, vaccine response)
- Offer mechanistic depth (pathways, protein interactions, gene regulation)
- Are relevant to the user's domain (swine health, veterinary science, microbiology)
- **Fill connected gaps** (most valuable for mature 100+ card KFs): scan the existing card list for topics that are *referenced* by multiple existing cards but never *independently covered*. These "ghost topics" have high connective value because they link existing cards together. Example: Th17/Treg balance and IL-12 family cards both mention IL-17, but IL-17 family itself had no card → creating one instantly connects to 9+ existing pathways via crosstalk sections.

**Systematic gap-finding heuristics for mature KFs (>100 cards):**

> **Quick automated check:** Run `scripts/kf-gap-analysis.py` (from this skill's directory) to scan all cards against a candidate list and identify gaps before starting research. Use `--candidates "topic1,topic2"` to test specific topics, or run with no args for DETECT mode (scans for structural gaps across the entire KF).

See `references/gap-finding-ghost-topics.md` for the "ghost topic" pattern — concepts referenced in ≥5 cards but lacking dedicated coverage. Automated scan: `scripts/kf-gap-analysis.py` (`--candidates` or DETECT mode).
1. **Pathway/cytokine inventory**: List every signaling pathway and cytokine mentioned across existing card cards. Any pathway referenced in 3+ cards but not independently covered is a high-priority gap
2. **Crosstalk score**: For each candidate topic, count how many existing KF cards it connects to through signaling crosstalk. Prioritize topics scoring 5+ connections — these weave the knowledge base together
3. **Structural symmetry**: If the KF has cards for most members of a family (e.g., IL-1, IL-6, IL-10, IL-12, IL-22) but is missing one (e.g., IL-2 family, IL-17 family), fill the gap
4. **Downstream épaisseur**: If a pathway is discussed in feed-additive context but its molecular mechanism hasn't been documented in its own card, elevate it
5. **Rotation-group coverage scan (4-group cron)**: before picking a subtopic for the current rotation index, map existing card titles to the 4 rotation groups and pick an uncovered gap WITHIN that group, not just any novel topic. Example (Hóa học & Dược): soil/heavy-metal treatment cards were dense AND natural compounds (curcumin, quercetin, resveratrol, berberine, saponin, tannins, EOs) were covered → glycyrrhizin was the gap (keyword dedup `glycyrrhizin` = 0 matches; `saponin` matches don't block a compound-specific card)

**Step 3 — Research** using the APIs in this skill:
1. **Wikipedia Action API** (Level 2a) — search by keyword, fetch full-page extracts for background
2. **PubMed E-utilities** (Level 2c) — search from 2-3 query angles, get summaries + abstracts
3. **Multi-query PubMed pattern** (see Level 2c) — ensures coverage across subtopics
4. **AI/tech/CS rotation topics: use arXiv, not PubMed** — search by `submittedDate`, download PDF + pypdf extract (arXiv HTML often missing for LaTeX). Recipe: `references/arxiv-pdf-fulltext-extraction.md`. Cite exact numbers; GRPO/RL reasoning bank: `references/grpo-rl-llm-reasoning-roadmap.md`.
   **arXiv API — try FIRST:** `https://export.arxiv.org/api/query?search_query=ti:...` and `?id_list=<id>&max_results=1` return full Atom XML reliably (4+ calls + 5MB PDF OK; earlier "always times out" note is stale). Use first for AI/tech verification: one call gives canonical title/date/category/full abstract. Semantic Scholar is the FALLBACK and is itself 429-rate-limited without a key. Flow: arXiv first → if exit-28 timeout/empty, Semantic Scholar → on 429, retry arXiv id_list. Pull the PDF (`/pdf/<id>` → pypdf) for concrete benchmark numbers. Cite AI/CS by arXiv ID (arXiv:2501.12948).
5. **Verify the card landed**: after POST 201, re-fetch `/api/cards` (background, long timeout) and match the returned `id` — the POST response alone isn't proof of ingestion for large KBs. For 8-bài/ngày rotation cards also confirm `<!--OVERVIEW-->` in returned content.

**Step 4 — Compile structured card content** following these conventions:
- **Title**: starts with an emoji + topic name in Vietnamese + brief subtitle, e.g. `🧬 Nrf2/KEAP1 — Con đường tín hiệu chống oxy hóa chủ chốt ở heo`
- **Content format**: Markdown with rich elements — tables (| col | col |), code-block diagrams (```), callout blockquotes (> **key point**), numbered lists, sections (## headings), emoji markers per section
- **Tags**: 10-20 specific tags covering the pathway, species, compounds, and related pathways for searchability
- **References table**: each PMID cited gets a table row with `PMID: number (Journal Year) — brief description of what the paper contributes`
- **Citation anchoring**: every mechanism claim in the content should map to a PMID in the references table
- **For virus/pathogen topics**, use the 11-section outline template at `references/virus-pathogen-card-template.md` — it covers overview, genome, proteins, immune evasion, pathogenesis, genotype, vaccine, diagnosis, global epidemiology, conclusions, and references with PubMed multi-query patterns
- **For bacterial pathogen topics** (ETEC, Salmonella, APP, M. hyopneumoniae, Lawsonia, S. suis, Clostridium, Brachyspira), use the 12-section outline template at `references/bacterial-pathogen-card-template.md` — it covers virulence factors (adhesins, toxins, secretion systems), pathogenesis, immune evasion, AMR, vaccines, and nutritional interventions with section emphasis tables per pathogen type and PubMed query templates
- **For pathway/mechanism topics** (cytokine families, signaling cascades, protein families), use the 10-section outline template at `references/pathway-card-template.md` — it covers overview, structure, signaling mechanism (classical vs alternative), biological function, developmental aspects, disease relevance, nutritional modulation, family members, pathway crosstalk, and references
- **For feed additive / phytochemical topics** (essential oils, tannins, polyphenols, organic acids, MCFAs, saponins, prebiotics, botanicals), use the 10-section outline template at `references/feed-additive-card-template.md` — it covers definition & classification, active compounds with per-compound mechanisms, multi-mechanism action (antimicrobial, antioxidant Nrf2, anti-inflammatory NF-κB, gut barrier, microbiota), swine application by production stage with dose tables, synergistic interactions, Vietnam-context application, challenges, and future research directions
- **For toxic agent/contaminant topics** (aflatoxin, fumonisin, ochratoxin, T-2 toxin, heavy metals, pesticides), use the 10-section outline template at `references/toxic-agent-card-template.md` — it covers chemical structure & types, sources & growth conditions, toxicokinetics (ADME diagram), molecular toxicity mechanisms (bioactivation, DNA adducts, p53 mutations), pig health effects with dose-response tables, regulatory limits (EU/FDA/Vietnam QCVN), prevention & mitigation strategies (adsorbents, biotransformation, botanical hepatoprotectants), co-contamination interactions, and complete PMID reference tables

**Step 5 — Final deduplication check** before POST:

```bash
# Search ALL cards for any title containing your topic keywords (not just last N)
curl -s http://localhost:3003/api/cards | python -c "import sys,json; cards=json.load(sys.stdin); kw='YOUR_KEYWORD'; [print(f'DUP: {c[\"title\"][:90]}') for c in cards if kw.lower() in c['title'].lower()]"
```

**Multi-keyword dedup (recommended):** Search across several keyword variants to catch partial overlaps:

```bash
# Check multiple keyword variants in one pass
curl -s http://localhost:3003/api/cards | python -c "
import sys,json
cards = json.load(sys.stdin)
keywords = ['tgf', 'smad', 'tgf-beta', 'transforming growth', 'activin', 'bmp']
for c in cards:
    t = c['title'].lower()
    for kw in keywords:
        if kw in t:
            print(f'MATCH [{kw}]: {c[\"title\"][:100]}')
            break
"
```

This is important for topics where the pathway has multiple names/abbreviations (e.g. "TGF-β" check should cover "TGF-beta", "transforming growth factor", "SMAD", "activin"). Only POST if zero matches across ALL keyword variants.

**⚠️ False-positive pitfall with short/collision keywords:** When the keyword list contains short substrings like `CD28`, `CD80`, `CD86`, `TNF`, or `IL2`, the `if kw in t` match will also hit cards whose titles contain supersets of those strings (e.g. `CD28` matches "CD8+ T cells", "CD86", "CD80"; `TNF` matches "TNFR", "TNF-α", "TNF/TNFR"). **Fix:** only use keywords that are ≥5 characters or unlikely to collide as substrings of unrelated terms. Common troublemakers: `CD`, `IL`, `TGF`, `TNF`, `Zn`, `Fe`. If a keyword is short, either omit it (rely on longer synonyms) or verify the match context with a second pass:

```bash
# For short/collision-prone keywords, add a second filter using word-boundary regex
curl -s http://localhost:3003/api/cards | python -c "
import sys,json,re
cards = json.load(sys.stdin)
keywords = ['checkpoint', 'PD-1', 'PD-L1', 'CTLA-4', 'immune checkpoint', 'costimulation', 'B7-1', 'CD80', 'CD86']
for c in cards:
    t = c['title'].lower()
    for kw in keywords:
        if re.search(r'\\b' + re.escape(kw.lower()) + r'\\b', t):
            print(f'MATCH [{kw}]: {c[\"title\"][:100]}')
            break
"
```

The `\b` word-boundary assertion prevents `CD28` from matching `CD8` or `CD86`, and `TNF` from matching `TNFR` or `TNFRSF`.

Also check for **partial keyword matches** by scanning the enumerated list from Step 1 — a card titled "Interferon, PRRs & JAK-STAT" may partially overlap with a planned "cGAS-STING" card even though neither title contains the other's full name.

**Step 6 — POST to KF** using **Pattern D** (Python POST script) — the most robust method for Vietnamese Unicode + multi-line markdown content. Pattern C (curl -d @path) breaks when the content field contains markdown tables, code blocks, or line breaks because `write_file` serializes `\n` as literal characters instead of actual newlines in JSON.

✅ **Pattern D — Python POST (RECOMMENDED for all KF cards):**
Write a `.py` script that constructs the payload as a native Python dict and POSTs via `urllib`:

```python
# write_file -> post_card.py
import urllib.request, json

card_content = """## 🧬 Title

Markdown content with **bold**, | tables |, ```code```, and emoji 🐷

| Gene | Expression |
|------|-----------|
| ZO-1 | 🔺 Tăng |

Nguồn: [PMID 12345678, Journal, Year]
"""

payload = {
    "title": "🧬 Topic — Vietnamese subtitle",
    "content": card_content,
    "summary": "Short Vietnamese summary",
    "tags": ["tag1", "tag2"],
    "topic_slug": "chan-nuoi-heo",
    "source_url": "https://en.wikipedia.org/wiki/Topic"
}

data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
req = urllib.request.Request(
    "http://127.0.0.1:3003/api/knowledge",
    data=data,
    headers={
        "Authorization": "Bearer hermes-knowledge-secret",
        "Content-Type": "application/json",
        "Cookie": "tfo_auth=1d1e977a218bfa01fe61106c360c8acf667047e35f17fdb0f1a8484e06cfdb55"
    },
    method='POST'
)

try:
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read().decode())
    print(f"SUCCESS! Card ID: {result.get('id', 'N/A')}")
    print(f"Status: {resp.status}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode()[:500]}")
except Exception as e:
    print(f"Error: {e}")
```

✅ **Pattern C (curl -d @path) — use ONLY for short JSON without markdown formatting:**
```bash
write_file(path="C:/Users/<user>/hermes-temp/card_payload.json", content='{"title": "🧬 Topic", "tags": ["tag1"]}')
curl -s -X POST http://localhost:3003/api/knowledge \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer hermes-knowledge-secret" \
  -d @C:/Users/<user>/hermes-temp/card_payload.json
```

Verify the response contains `"id"` — this confirms ingestion. **Card reading time** is returned as `reading_time_sec`; target ~5-15 minutes (300-900 sec).

**Pitfalls:**
- **Forgot to check cards first → duplicate cards**: The cost is wasted research + a messy KB. Always check before starting research AND before final POST.
- **Pattern C (`write_file` + `curl -d @path`) breaks with multi-line markdown content**: When the `content` field contains Markdown with embedded newlines (tables, code blocks, line breaks), `write_file` writes literal `\n` characters inside the JSON string — producing **invalid JSON** (`json.loads()` fails with `Invalid control character`). **Fix:** use the two-step Python approach (build dict natively → `json.dumps(ensure_ascii=False)` → write clean JSON) or POST directly from Python (Pattern D). See the `cron-job` skill's "Critical: write_file produces invalid JSON" section for the exact pattern.
- **Title too generic**: `"Nrf2 pathway"` is too short. Add species context and an emoji so users scanning the card list know the scope immediately.
- **Missing tags**: Without 10+ specific tags, the card won't appear in search results for related topics (e.g. `Zn-L-SeMet`, `weaning stress`, `intestinal barrier`).
- **`topic_slug` in POST is effectively ignored (tested Aug 2026)**: recent cards GET returns `topic_id: None`; `GET /api/topics` only lists stale generic dev topics (ai-ml, react-nextjs, card_count 0) — don't waste calls probing for a valid slug. Pass a neutral slug (e.g. `chan-nuoi`) or omit it; both POST successfully.
- **Abstract text over-trimmed**: PubMed abstracts can be 2000+ chars. Include at least 500 chars of the key mechanism findings, not just the background sentence.

