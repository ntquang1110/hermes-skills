# Citation verification without the publisher page (Crossref + Semantic Scholar)

For psychology / organizational-behavior / HCI papers. These are usually NOT in PubMed
(See `scientific-literature-retrieval.md` for the PubMed eutils ladder, which still covers
everything indexed there), and the publisher page is captcha-walled. Two free keyless JSON
APIs cover what you need. Verified working 2026-09-29 while writing a psychology article
on attention residue (Zeigarnik / Ovsiankina / Leroy 2009).

## The rule this enables

**Never write an author's name, year, or number into an article before you have fetched
it.** Crossref gives you the bibliographic record in one call. Do that first, always.

This generalises beyond papers. Any identifier that carries an argument — statute
number, article, standard code, document ID, product code, API version — must be
retrieved, not recalled. A wrong statute number is a defective filing; a wrong
price is a bad number. Same failure, different blast radius.

The pattern that catches most mistakes: **treat the identifier as a hypothesis,
search the subject matter, then read what identifier the source assigns.**
Searching the identifier and accepting the top hit confirms your own error.
One measured VN legal session wrote 6 wrong document/article numbers from memory,
every one plausibly formatted and none self-reporting as wrong — including a
"Land Law 2003" number that was actually the Accounting Law, and a claimed
"Civil Code amendment 2025" that does not exist because the Civil Code has never
been amended.

For statutory/regulatory retrieval specifically (Vietnam: source hierarchy,
proving a negative across ≥3 sources, effective dates moved by amending
instruments, keyword-match ≠ scope-match, historical-effect traps), see
`vietnam-legal-source-routing.md`.

## 1. Crossref — bibliographic metadata

```bash
curl -s --max-time 30 "https://api.crossref.org/works?query.bibliographic=Why+is+it+so+hard+to+do+my+work+attention+residue+Leroy&rows=3" \
 | python -c "
import sys,json
for it in json.load(sys.stdin)['message']['items']:
    print(it.get('title',[''])[0][:100])
    print('  ',it.get('container-title',[''])[:1],'vol',it.get('volume'),'iss',it.get('issue'),'p',it.get('page'),it.get('issued',{}).get('date-parts'))
    print('   DOI:',it.get('DOI'))"
```

No auth, no key, no scraping. Works for journals (OBHDP, Journal of Occupational Health
Psychology) AND conference proceedings (CHI, ISMAR).

- `query.bibliographic` accepts the full title as a single quoted phrase. `rows=3` shows
  near-misses so you can confirm you hit the right paper and not a same-title item.
- Prefer this over search engines for anything you intend to cite. It is deterministic:
  same query, same metadata, no bot-detection roulette.
- Got a DOI in hand already? `https://api.crossref.org/works/<doi>` returns the full
  record plus `is-referenced-by-count` (a cheap "is this seminal or forgettable" signal).

## 2. Semantic Scholar — abstract when the publisher strips it

```bash
curl -s --max-time 30 "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.obhdp.2009.04.002?fields=title,abstract,year,venue,tldr,citationCount,externalIds" \
 | python -c "import sys,json;print(json.dumps(json.load(sys.stdin),ensure_ascii=False,indent=1))"
```

- **`abstract` is `null` when the publisher withholds it** (Elsevier, ACM, Springer, IEEE).
  That is not a failure. Crossref already gave you the metadata needed to cite it; the
  abstract is a bonus, not a prerequisite.
- **`tldr.text` is a generated one-line summary of the abstract and IS usable** to
  characterise a finding. For Leroy 2009 it returned: "it is difficult for people to
  transition their attention away from an unfinished task and their subsequent task
  performance suffers." Treat it as a summary to confirm against — never as a verbatim
  quote from the authors, and never as a source for a specific number.
- `citationCount` + `externalIds` (PMID, MAG, CorpusId) tell you how load-bearing the
  paper is and whether a PubMed route exists after all.

### Lookup beats search on the free tier

`/paper/DOI:<doi>?fields=...` is the reliable path. `/paper/search?query=<long natural
language sentence>` frequently returns `total: null` on the keyless tier even for papers
that definitely exist (seen repeatedly 2026-09-29). Use search only when you have no DOI
and crossref also failed.

### 429 is throttling, not absence

A few `/paper/search` calls in quick succession return `HTTP Error 429`. Fix: `sleep 2`
between calls, or restructure to avoid search entirely. Do not report "no such paper" on a
429.

## 3. What is DEAD for this task (don't spend calls)

ScienceDirect, ResearchGate, PsycNET (its record IDs go stale → "Could not locate the
requested record"), CORE, BASE (Anubis PoW wall), `api.fatcat.wiki` (unparseable JSON).

`r.jina.ai` against `dl.acm.org` and `sciencedirect.com` returns a Cloudflare
"Just a moment..." / "Are you a robot?" page plus a large blob of minified JS, not
article content. The one useful part: grep the jina output for the abstract with a narrow
`grep -io` before giving up — sometimes the page title line survives.

## 4. Recent meta-analyses are the best citation for a contested claim

When a popular claim is disputed, a recent meta-analysis states the settled position
explicitly in its abstract, which is exactly what you want. Two found this way:

- **Ghibellini & Meier 2025**, *Humanities and Social Sciences Communications*
  (DOI `10.1057/s41599-025-05000-w`): meta-analysis of the Zeigarnik and Ovsiankina
  effects. "We found no memory advantage for unfinished tasks but found a general tendency
  to resume tasks." This lets you correct a century-old oversimplification with a citation.
- **Wendsche, Weigelt & Syrek 2026**, *Anxiety, Stress, & Coping* 39(4):385-407,
  PMID 41554526, DOI `10.1080/10615806.2026.2616302`: the abstract carries exact effect
  sizes (rho .382 between-person, .247 within-person, k=17/N=2,473 and k=14/N=12,129), which
  is what makes a quantitative claim citable without inventing a number.

## 5. Wikipedia via API for the effect's origin story

```bash
curl -s "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=<kw>&format=json" \
 | python -c "import sys,json;[print('-',r['title']) for r in json.load(sys.stdin)['query']['search'][:6]]"
```
Then `r.jina.ai` the article page for clean markdown with full reference lists. The
Zeigarnik page carried the Lewin-waiter anecdote, the Lewin field-theory tension
explanation, the failed replications, and the 2025 meta-analysis pointer — all in one fetch.

Wikipedia's article body is citable context for a story ("Lewin noticed a waiter
remembering unpaid orders"), but cite the primary paper for the mechanism, not the wiki.
