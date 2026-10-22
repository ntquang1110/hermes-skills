# Scientific literature retrieval: PubMed eutils + Wikipedia curl

Verified-citation workflow for science/health/neuroscience research posts (works with plain
curl, no auth, no scraping). Produces exact quotes, years, journals, DOIs and PMIDs straight
from primary sources — never guess a quote or a number.

Sibling reference: `references/ree-pig-feed-sources.md` — verified source bank for the
rare-earth-in-pig-feed research project (23 PubMed PMIDs by topic + EU/EFSA/US/CN regulatory
facts with verification trail + the output JSON schema used by that project).

**Never use PubMed RSS endpoints** (`pubmed.ncbi.nlm.nih.gov/rss/?term=...`) — they return empty NCBI HTML boilerplate ("There is nothing to see here"). Go straight to E-utilities (esearch → efetch/esummary).

## PubMed eutils (NCBI) — primary source for abstracts/quotes

Three-step pattern, all plain `curl`:

1. **esearch** → find PMIDs by exact title words + first author + year:
```bash
curl -sL --compressed "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Raichle+default+mode+of+brain+function+2001&retmode=json" \
  | python -c "import json,sys; d=json.load(sys.stdin); print(d['esearchresult']['idlist'])"
```
2. **efetch** → full abstract + citation metadata (authors, year, journal, DOI, PMID). Batch IDs comma-separated:
```bash
curl -sL --compressed "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=11209064,21071660,18400922&rettype=abstract&retmode=text"
```
3. **esummary** → cheap title/journal/year check when you have candidate PMIDs:
```bash
curl -sL --compressed "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=33206471&retmode=json"
```

Tips:
- Disambiguate searches with first-author surname + distinctive title words + year; the
  returned PMID is then unambiguous (e.g. `Hamilton default-mode task-positive major
  depressive disorder rumination` → the right 2011 Biol Psychiatry paper).
- Abstracts are primary text — quotes taken from them are safe to reproduce with attribution.
- **Stats that are NOT in the abstract** (e.g. Killingsworth & Gilbert's "46.9% of waking
  hours" figure, which the Science abstract omits) must be verified via a secondary
  authoritative source — university news release (news.harvard.edu/gazette), publisher page,
  or archive.org. Never invent numbers from memory.
- PubMed eutils also resolves "does this researcher have a Wikipedia page?" — if not
  (e.g. Jessica Andrews-Hanna), skip Wikipedia and go straight to their papers.

## Wikipedia via curl — compression/UA workaround

Plain `curl -sL` to wikipedia.org `action=raw` / REST HTML endpoints can return **HTTP 200
with SIZE:0 and curl exit 23** (write error). Fix — add `--compressed` and a browser UA:

```bash
curl -sL --compressed -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36" \
  "https://en.wikipedia.org/w/index.php?title=Default_mode_network&action=raw"
```

- `action=raw` wikitext is best for grepping facts/refs (sections, cite templates with PMIDs).
- The REST summary endpoint (`/api/rest_v1/page/summary/<Page>`) works WITHOUT the workaround
  but returns only the lead paragraph — fine for a quick definition, not for deep extraction.
- Extract facts from HTML with a python one-liner: strip `<script>/<style>`, strip tags,
  unescape entities, then regex-search keywords with ±300 char context windows.

## Blocked publishers — don't fight them

- journals.sagepub.com → DNS failure (HTTP 000); researchgate.net → 403; Google Scholar via
  curl → HTTP 429. All three are dead ends; PubMed eutils has the abstract, university press
  releases / archive.org have the rest.

## Worked example: DMN research brief (2026-08-04)

Full brief produced with this workflow: `D:/Hermes Proj/dmn_research_summary.md` — 17 papers
with PMIDs (Raichle 2001 PNAS, Buckner et al. 2008, Mason et al. 2007 Science, Killingsworth
& Gilbert 2010 Science, Hamilton 2011, Sheline 2010, Brewer 2011 PNAS, Ulrich 2014, ...),
exact quotes (Raichle SciAm 2010 "The Brain's Dark Energy", K&G "A wandering mind is an
unhappy mind", Brewer "the default mode of humans appears to be that of mind-wandering"),
and region facts (mPFC, PCC+precuneus, angular gyrus). Every citation in that brief was
reproduced via the query patterns above.

## Verifying patents — Google Patents XHR (no key, JSON)

```bash
curl -sL --compressed "https://patents.google.com/xhr/query?url=q%3D<urlencoded-kw>%26oq%3D<urlencoded-kw>" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
```

JSON path: `results.cluster[0].result[].patent` → `publication_number`, `title`, `assignee`,
`priority_date`/`grant_date`. **NOT reliably available**: the XHR endpoint can return HTTP
503 and the browser a "Sorry... automated queries" block (bot-detection/IP dependent —
seen 2026-08). When blocked: never fabricate numbers; emit `number:""` + `note:"chưa
verify"` per the identifier-discipline rules below. **TESTED WORKING FALLBACK (2026-08): Espacenet in the browser.** `browser_navigate` to
`https://worldwide.espacenet.com/patent/search?q=<urlencoded>` (phrase-quote keywords:
`q=%22pig%20manure%22%20separation`; unquoted queries sometimes hang on the progressbar —
re-navigate with a quoted phrase). Results load async — pull them with `browser_console`:
`[...document.querySelectorAll('article')].map(a=>a.textContent.trim().replace(/\s+/g,' ').slice(0,150))`
→ each row carries publication number + date + first assignee, e.g.
`Select result1.Pig manure solid-liquid separation deviceCN210855757U • 2020-06-26 • DEZHOU ZHENGHONG`
(also shown as a tooltip when ticking a result checkbox). Numbers read from the live DOM are
authoritative — record number/title/date/assignee. Less-proven candidates: WIPO Patentscope
`patentscope.wipo.int/search/en/result.jsf?query=FP:(...)` returned HTTP 200 in one test
(body may be brotli-encoded → `pip install brotli`), FreePatentsOnline
`freepatentsonline.com/result.html?query_txt=...` (connection reset in that same test).
CN patent titles are often machine-translated — verify number + assignee, keep the
translated title with a note. A verified patent number comes from a fetched response,
never from memory.

## Rate limits on efetch — retry, don't conclude "missing"

Unauthenticated efetch is ~3 req/s per IP. `{"error":"API rate limit exceeded"}` means
throttled, NOT a dead PMID: `sleep 1–3` and retry. In batch loops over many PMIDs, add
`sleep 1` between efetch calls (esearch calls are lighter — batch them freely).

## Search-term refinement (compound / animal-health queries)

Generic terms return noise (e.g. `sanguinarine pig diarrhea` surfaced unrelated new
papers; `sanguinarine weaned piglets` found the real trials). Refine with
`compound + "weaned piglets"` / `"post-weaning diarrhea"` / species+condition pairs.
Zero hits with one phrasing ≠ nothing exists — retry synonyms (`peppermint oil` vs
`menthol`). Always efetch candidates to confirm the abstract matches the claim.

## PubMed synonym-expansion noise — hit count ≠ relevance

esearch auto-expands terms through MeSH + Supplementary Concepts, which inflates counts and
pulls in off-topic papers. Worked example: `rare earth chloride pig` returned 90 hits
dominated by thulium-fiber lasers ("metals, rare earth" Supplementary Concept catches ANY
rare-earth element) and guinea-pig chloride-channel physiology ("pig" → "swine"[MeSH] and
"pig" also matches "guinea pig"). Before trusting a hit list:

- Read the `querytranslation` field in the esearch JSON — it shows exactly what the engine
  expanded your terms into; if it grew wild (e.g. thulium appeared), tighten the query.
- Title-screen cheaply: batch 10–15 candidate PMIDs through `esummary` (retmode=json) and
  print `pubdate|source|title` one-per-line with a python one-liner; drop obvious noise
  (imaging/MRI/case reports) BEFORE spending efetch calls on full abstracts.
- Prefer phrase-quoted or tightly-scoped queries (`"rare earth elements"[Title/Abstract]
  AND pig[Title/Abstract]`, or compound + species + condition) over bare keywords.
- Confirm the abstract supports the claim (efetch) — a title that fits can still be about
  something else (e.g. `lanthanum carbonate swine` surfaced a cardiovascular allograft
  calcification model, not feed/nutrition).

## Regulatory/legal verification — absence is provable by grep

For "is X approved/permitted" questions, verify against the authoritative full text, not
secondary summaries:

- **US regulations**: the eCFR API serves a whole part as XML —
  `curl -sL "https://www.ecfr.gov/api/versioner/v1/full/<date>/title-21.xml?part=573"`,
  then grep for the substance(s). Zero matches = verified absence (this confirmed that no
  rare-earth element is in 21 CFR Part 573 "Food Additives Permitted in Feed and Drinking
  Water of Animals"). Distinguish "grep of the full authoritative text" (strong) from
  "no result on a search engine" (weak).
- **EU regulations**: find the Commission Implementing Regulation number via
  Google-in-browser, then confirm the eur-lex URL pattern
  `eur-lex.europa.eu/eli/reg_impl/<year>/<num>`. EFSA Journal opinions are on PubMed with
  PMIDs — search `EFSA <substance> feed additive` (e.g. the Lancer lanthanide-citrate
  opinions 42109452/32626202; lanthanum carbonate cats/dogs 35233256/38601863).
- **Chinese GB/MOA standards**: Google-in-browser handles Chinese queries well and gov.cn
  snippets are rich. GB 2762-2017 "删除了稀土限量要求" (deleted REE limit requirements)
  was confirmed from multiple Chinese government/standards sources; note that GB 2762-2012
  explicitly carried the old REE limits forward ("稀土限量指标按原GB 2762—2005执行").
- **Search-engine fallback ladder when curl engines are blocked**: html.duckduckgo.com now
  serves a CAPTCHA ("select all squares containing a duck"); bing.com via curl returns
  nothing usable. `browser_navigate` to google.com still works (localized UI, rich
  snippets) — use the browser for regulatory fact-finding, curl only for the APIs above.
- **Standards PDFs** sometimes fail curl download or are image-based; `pdftotext` exists in
  git-bash if you need to convert. Do not cite specific limit values unless a snippet/PDF
  confirms them — state only what you verified (e.g. "tea 2.0 mg/kg" from a snippet; the
  other 2005 table values were left unstated rather than guessed).
- MOA/Ministry announcements in China are often only found via secondary news sites — cite
  them with an explicit "nguồn thứ cấp, cần verify văn bản gốc" note (see the RECC/MOA
  288号 entry in the REE source bank).

## Vietnamese regulatory documents (QCVN / Thông tư)

Verified access ladder (pig-wastewater QCVN 62 research, 2026-08 — full verified tables in
`pubmed-evidence-research/references/pig-waste-group3-chemical.md`):

- **english.luatvietnam.vn** — official English translations of Circulars (including the
  Thông tư that carries a QCVN) fetch fine with plain urllib/curl; the full parameter
  table is in the HTML. Fastest path to QCVN limit values.
- **Bing search in browser** works for finding Vietnamese regulatory PDFs; the compact
  `browser_snapshot` hides organic results — extract them via `browser_console`:
  `Array.from(document.querySelectorAll('#b_results > li.b_algo')).map(li => li.querySelector('h2 a')?.innerText + ' ||| ' + li.querySelector('h2 a')?.href + ' ||| ' + (li.querySelector('.b_caption p, p')?.innerText ?? ''))`.
  Gov/mirror PDFs (xulymoitruong.com, *.gov.vn uploads, cdn.thuvienphapluat.vn) then
  download via curl and extract text with pymupdf. If the default `python` has no pip,
  find the interpreter that does (`py -0`) and run extraction with it after
  `pip install pymupdf` (`import fitz`).
- **Blocked, plan around**: thuvienphapluat.vn → Cloudflare challenge (403 even in the
  browser); vanban.chinhphu.vn → HTTP 200 but a JS-only shell with no document text in
  static HTML; luatvietnam.vn deep URLs → 404 unless the exact search-engine slug is used.
- Re-confirmed 2026-08: luatminhkhue, vanbanphapluat.co, lawnet, thuvienmoitruong were also
  Cloudflare-walled or empty, Wayback CDX returned [], and Bing/Google could not surface the
  limit table — a whole session stalled here. Go STRAIGHT to the documented
  english.luatvietnam.vn path instead of re-probing mirrors. If that fails too, emit the
  standard by name (verified identity) with an explicit `verification` note
  "giá trị giới hạn chưa đối chiếu văn bản gốc" — never fill limits from memory, and check
  whether the QCVN was replaced (see the 2025-replacement note above).
- Always check whether a QCVN has been **replaced**: QCVN 62-MT:2016/BTNMT was superseded
  by QCVN 62:2025/BTNMT (Thông tư 04/2025/TT-BTNMT) with stricter limits and new
  parameters (T-P added) — citing an outdated QCVN in a compliance deliverable is a real
  error, not a style one.

## Identifier discipline (hard rules)

- Re-verify PMIDs reused from earlier sessions with a quick efetch — "verified before"
  is not "verified now".
- An unverifiable patent is emitted with an empty number + explicit "unverified" note
  (e.g. `number:''`, `note:'chưa verify'`) — never a guessed or misattributed number.
- Mark direct vs indirect evidence in citation notes (poultry trial cited for a pig
  product = "gián tiếp — loài khác"; in vitro ≠ in vivo).
- Record the verification trail in the deliverable: which PMIDs efetch-confirmed, which
  patents found, what remains unverified.
- Batch workflow for N-compound catalogs: esearch all first, efetch candidates in a loop
  with `sleep 1`, patents XHR for 2–3 key items only, then write output via a generator
  script (`ensure_ascii=False` for Vietnamese/diacritics) + a schema validator that
  re-parses the written file and asserts every required key.

## Delegated research batches — write per-item, never one big final dump (verified 08/2026)

**Symptom:** subagents in a parallel research batch (delegate_task fan-out) hit their
tool-iteration cap (~50 calls) BEFORE writing the deliverable JSON. Batch reports
`status=completed` but the file is missing; the data exists only as inline JSON buried in
the final summary. Happened repeatedly (piglet-premix 3/3, vingroup 3/3) until the pattern
below was applied. The parent must treat a child's `completed` status as unverified until
`json.load` on the expected file succeeds.

**Fix — bake into every delegation prompt:**
1. **Write per-item, not per-batch.** Tell the child to append one JSON record to the
   target file immediately after finishing each compound/topic — NOT to accumulate
   everything in memory and dump once at the end. A mid-run cap then leaves a partial
   but usable file instead of nothing.
2. **Return payload inline in the summary as fallback.** Instruct the child: "if you hit
   the tool cap before writing the file, embed the complete final JSON verbatim in your
   summary" — the parent can persist it in one step. Children that follow this lose
   nothing.
3. **JSONL for long loops** (13+ items): append `json.dumps(item) + "\n"` per item; on
   restart skip ids already present. A killed/timed-out process keeps its progress.
4. **Parent verifies before merging:** after the batch completes, check each expected file
   with `json.load`; if missing, extract the inline payload from the subagent summary
   (saved at `hermes/cache/delegation/subagent-summary-*.txt`) and persist it yourself.
   Set `"file_written": true` in the payload when done.
5. **PMID/patent discipline holds in the fallback path:** every inline fact must carry its
   verified PMID/patent + source URL; never fill gaps from memory when persisting a
   child's payload.
