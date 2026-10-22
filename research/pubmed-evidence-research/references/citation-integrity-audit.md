# Citation Integrity Audit

The step that turns "sourced" into "verifiable". Run it on **every** deliverable
whose value rests on identifiers (PMIDs, DOIs) — a schema-valid file with one
mis-attributed PMID is worse than no citations, because the wrongness is
invisible and inherits your credibility.

Companion script: `scripts/verify_citations.py` (stdlib only). Run it before
delivering, not after the user finds the problem.

```bash
python scripts/verify_citations.py DELIVERABLE.json      # JSON with a source list
python scripts/verify_citations.py report.md             # prose/markdown
python scripts/verify_citations.py D.json --no-crossref  # PMID-only, faster
```

## The loop

1. **Build the deliverable** with every figure carrying its own identifier.
2. **Mechanically resolve** each identifier: PMID -> Europe PMC, DOI -> CrossRef.
   Never eyeball a plausible-looking PMID; that is exactly the class of error
   that survives review.
3. **Diff your entry against the registry's own metadata** — title AND year.
   Resolution alone is not enough: an id can resolve perfectly to the *wrong
   paper*.
4. **Fix, re-run, and only then report.** Report what the audit found; the
   audit trail is part of the deliverable's value.

## Registry recipes

**Europe PMC — resolve a batch of PMIDs** (10-15 per call is comfortable):

```python
q = {"query": " OR ".join("EXT_ID:" + p for p in pmids),
     "format": "json", "resultType": "core", "pageSize": len(pmids) + 5}
url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urlencode(q)
# resultList.result[] -> pmid, doi, title, authorString, pubYear,
#                        journalInfo.journal.title, pmcid, isOpenAccess
```

`resultType=core` is required for `authorString`/`journalInfo`; `lite` omits
them. Use `authorString` verbatim when writing the source list — it removes any
opportunity to invent or garble an author list.

**Europe PMC — full text** (open-access only):

```
https://www.ebi.ac.uk/europepmc/webservices/rest/{PMCID}/fullTextXML
```

Strip tags to read, and cache each fetched XML to a local dir (e.g.
`_ftcache/{pmid}.xml`). Persisting the source text is what lets you re-audit
later without re-fetching, and lets you quote verbatim from the body.

**CrossRef — confirm a DOI is registered**:

```
https://api.crossref.org/works/{url-quoted-doi}
```

Poll politely: CrossRef returns HTTP 429 readily. Back off and retry, and send
a User-Agent with a `mailto:`.

## Defect classes this catches (all four occurred in one real dossier)

1. **Right shape, wrong paper.** A PMID was cited 18 times for an
   ASFV-structural-protein review; it actually resolved to an unrelated
   **malaria** trial (Lancet Global Health). Well-formed, plausible, and
   completely wrong. Only registry resolution catches this. *Fix: look the
   topic up by title* (`TITLE:"..."`) rather than trusting a remembered number.
2. **Wrong DOI inside a correct entry.** A vaccine-review entry carried a
   plausible `10.3390/v18...` DOI while Europe PMC recorded
   `10.3390/vaccines14030284`. Serial-looking DOIs are easy to mis-transcribe.
   *Fix: take the DOI from the registry record, never from memory or a
   neighbouring entry.*
3. **Stale / mis-pasted metadata.** A source-list entry's title, authors, and
   DOI belonged to a *different* paper than its PMID. The PMID was real; the
   prose around it was not. *Fix: rebuild source-list entries
   programmatically from `authorString` + `title` + journal + `pubYear` + `doi`,
   then re-verify.*
4. **Secondary source mis-cites the primary.** A review reproduced a data
   table but attributed it to the wrong reference number, while the content
   actually matched a different primary study. *Fix: cite the PRIMARY study;
   record the discrepancy in a note. Never launder a citation through a review.*

Two more patterns worth policing by hand:

- **Over-claiming via an adjacent paper.** A diagnostic-method paper (a
  viability-qPCR study) was nearly used as evidence of *disinfection efficacy*.
  It supported only "this assay can distinguish live from dead virus". Check
  that each citation supports the *claim made*, not merely the topic.
- **Unregistered-but-real DOIs.** Some publisher DOIs live in PubMed metadata
  but do not resolve at CrossRef (observed with Medknow/Wolters journals, e.g.
  `10.4103/...`). Do **not** delete them and do not silently pass: keep the
  DOI and annotate the entry as "not CrossRef-resolvable at date of check".

## DOI extraction pitfall

A regex that captures sentence-final DOIs drags the terminating period along,
producing `10.1128/jvi.00932-24.` and a spurious 404. Always `rstrip` the
trailing punctuation set `.,;:)]}"'` before resolving. A run that reports 10+
DOI failures at once is usually this bug, not 10 bad DOIs — check the
normalization before believing the failures.

## Verify titles tolerantly, years strictly

Titles come back with markup, casing, and punctuation differences. Compare
**normalized** (lowercase, alphanumeric only) and test containment of a ~40-char
prefix of the registry title inside your entry text. Years are exact-match —
`pubYear` vs the listed year is the cheapest high-signal check there is.

## Also check the reverse direction

Harvest identifiers mentioned in the *body* and confirm each appears in the
source list. A PMID cited in prose but missing from the list is an unattributed
claim, and it is the same drift that produces defect #3.
