# Europe PMC REST — verify-before-you-cite quirks

Use when a task demands that every PMID and every quoted number be provably real
(e.g. "PMID bịa = loại cả lô"). Europe PMC REST is the fastest verifier because it
returns structured JSON, one hit or none.

## 1. Verification recipe (one call per PMID)

```
https://www.ebi.ac.uk/europepmc/webservices/rest/search
  ?query=EXT_ID:<pmid>&resultType=core&format=json
```

Accept the citation only if BOTH hold:
- `hitCount == 1`
- `resultList.result[0]["pmid"] == "<pmid>"` (string compare, not int)

`EXT_ID:` alone can return >1 hit for some ids (comments/corrections), hence the
hitCount check. Batch verifying is safe with a ~0.12–0.2 s sleep between calls and
a local dict cache; re-running the same script must be free.

## 2. abstractText is HTML, and p-values get eaten

- Strip tags first: `re.sub(r"<[^>]+>", " ", abstractText)` then collapse whitespace.
- **Truncated p-values are the big trap.** Europe PMC renders some records as
  `"...resulted in reduced (p"` — the comparison and digits (`<0.05`) are simply
  gone from `abstractText`. Seen on PMID 34237915 and 41265486.
  - NEVER quote a p-value that the API text does not contain.
  - Either pull the full text/PDF, or soften the claim: "giảm ... (có ý nghĩa thống
    kê theo bài)" with no digits.
  - An automated audit that looks for `0.05` in the abstract will flag this, which is
    exactly the point — treat the flag as "remove the number", not "the paper is fake".

## 3. Sample sizes are often spelled out

`Ninety-six piglets`, `Seventy-two piglets`, `Eighteen ... piglets`, `Forty piglets`,
`Twenty-four healthy ... piglets`, `Fifty-six piglets` — numeric-token audits yield
false mismatches. Keep a spelled-number map in the audit script and state in the
deliverable's notes that the file uses digits where the abstract used words.

## 4. Copy the abstract's own number formatting

Formats are inconsistent between records, so "normalise like Vietnamese" (decimal
comma, dot thousands) breaks literal matching:
- `3,000 ppm` (comma thousands) vs `1500 ppm` (no separator) vs `10 kg/1000 L`.
- Decimals are dots: `0.15%`, `6.87 ± 0.15 kg`, `5.67`.
Rule: when a number must be literally verifiable, reproduce the abstract's rendering
(including separators). Do NOT auto-convert `0,15` → `0.15` style edits across a whole
document without re-running the audit; and never let a comma-thousands fixup rewrite
`1500` into `1,500`.

## 5. Ranking buries the in-vivo papers you want

Default ranking is recency-biased: recent reviews hide older pig/chicken in-vivo
trials. To surface trials:
- field queries: `TITLE:butyrate AND (pig OR piglet OR swine) AND (villus OR crypt)`
- quoted substances + species: `"calcium butyrate" (pig OR piglet OR swine OR porcine)`
- add design terms: `weaned piglets AND (Ussing OR "tight junction" OR mucin OR MUC2)`
If a substance returns nothing usable, that is a real finding — record it as
`chua_co` (unsourced) rather than filling the gap with a plausible citation.

## 6. Evidence-level honesty (substance reviews)

- `in_vivo_heo` only when an experiment ran on live pigs. A piglet-trial of a *blend*
  containing the substance, or an in-vitro/mouse result, is a different level — label
  each citation's level separately, and set the entry's overall level to what the cited
  text actually supports.
- Negative results stay negative: if a trial shows no benefit (e.g. C12 lauric acid
  2%: TER tended to decrease, P=0.071, PMID 42467834), do NOT list it as an
  intervention. Demote it to a sourced caution inside the related entry and log it in
  an appendix — that is higher-value than a padded list.
- Numeric tokens inside caution text are still "quoted figures": cite the PMID they
  come from in that same entry, or drop the digits.
