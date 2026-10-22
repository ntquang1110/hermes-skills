# Food-additive / ADI regulatory safety retrieval (JECFA · EFSA · FDA · WHO)

Companion reference for ingredient-safety briefs when the ask is a **regulatory/ADI
status** (safe level in mg/kg, "có ADI hay không") rather than a PubMed toxicology
table. Session 19/08/2026 (NaHCO₃ & K₂CO₃ in drinking water for a VN founder).
"KHÔNG bịa số" applies doubly here: **never invent a numeric ADI** — JECFA frequently
deems a substance safe with **no numeric ADI** ("ADI not specified"). Saying so is the
correct, honest answer.

## Durable retrieval paths (verified working this session)

### 1. WHO guidelines — download the real PDFs from IRIS (not the landing page)
- Landing pages (`who.int/publications/i/item/...`) carry **no** recommendation text —
  only a download link. The numbers live in the PDF.
- IRIS is DSpace-7 (JS SPA). `curl` on `/handle/` returns an empty shell; direct
  `/bitstreams/<uuid>/...` links work. To find them: `browser_navigate` to
  `https://iris.who.int/handle/<handle>`, dismiss the cookie banner, then pull the
  bitstream links from the console:
  `[...document.querySelectorAll('a')].map(a=>a.getAttribute('href')).filter(h=>h && h.includes('bitstream'))`
  then `curl -s https://iris.who.int/<bitstream-href> -o file.pdf`.
- Known handles: sodium guideline **10665/77985** (ISBN 9789241504836); potassium
  guideline **10665/77986**. Extract text with pymupdf and `str.find()` the
  recommendation sentence for a verbatim quote.
- Verified verbatim (2012): sodium "<2 g/day sodium (5 g/day salt) … (strong
  recommendation)"; potassium "at least 90 mmol/day (3510 mg/day) for adults
  (conditional recommendation)".

### 2. FDA GRAS status — use the eCFR *developer API*, not the HTML site
- `ecfr.gov` HTML is CAPTCHA/403 for curl AND (`Federal Register :: Request Access`).
- The versioner API returns clean XML with the full §184 text:
  `https://www.ecfr.gov/api/versioner/v1/full/<YYYY-MM-DD>/title-21.xml?part=184&section=<NNN>`
- GRAS sections verified this session: NaHCO₃ §184.1736; KHCO₃ §184.1613;
  K₂CO₃ §184.1619. GRAS wording to page-scrape for the quote:
  "used in food with **no limitation other than current good manufacturing practice**".

### 3. EFSA (EU) authorised additives + ADI
- EFSA Journal lives on **Wiley (Cloudflare)** — blocked for curl, browser, and even
  r.jina.ai. FAO **GSFA Online** also Cloudflare-blocked (r.jina.ai included).
- **Don't guess EFSA DOI article numbers.** This session's guesses
  `10.2903/j.efsa.2013.3161` (really an EPA/ADHD health-claim opinion) and `.3138`
  (VTEC) were WRONG. Resolve through Crossref:
  `https://api.crossref.org/works?query.bibliographic=<title words>&filter=from-pub-date:..,until-pub-date:..`
  then read `message.items[].DOI` + `title` + `issued`.
- PubMed/esearch and Europe PMC (`ebi.ac.uk/europepmc/webservices/rest/search`)
  generally do **NOT index** EFSA food-additive re-evaluation opinions (E500/E501 →
  0 hits). Their re-evaluations (erythritol E968, calcium carbonate E170, etc.) ARE
  in Europe PMC/PMC — search `JOURNAL:"EFSA Journal" AND TITLE:"..."`.
- Fallback for "is it an authorised EU additive": cite the European Commission food
  additives database (Regulation (EC) 1333/2008) rather than a Wiley DOI you can't read.
- r.jina.ai (`https://r.jina.ai/<url>`) bypasses Cloudflare for **some FAO pages**
  (worked for the FAO JECFA additive detail page) — worth one try on otherwise-blocked
  regulatory pages, but not a guarantee (fails on GSFA + Wiley).

### 4. JECFA (FAO/WHO)
- JECFA status is authoritative for "ADI or no ADI". FAO JECFA additives DB:
  `https://www.fao.org/food/food-safety-quality/scientific-advice/jecfa/jecfa-additives/`.
- Read the JECFA wording precisely: "ADI not specified" (no number) is a real,
  correct outcome for physiological/self-limiting substances — do not convert it to a
  guesstimated mg/kg.

## Verified regulatory-fact bank (sodium/potassium carbonates & bicarbonates)
- JECFA: NaHCO₃, K₂CO₃, KHCO₃ → **no numeric ADI** ("ADI not specified"); considered
  safe/physiological (carbonate = the blood buffer; Na⁺/K⁺ = electrolytes).
- FDA: all three **GRAS**, no limitation beyond GMP (sections above).
- EFSA: authorised additives — E 500(ii) sodium bicarbonate (NaHCO₃), E 501(i)
  potassium carbonate (K₂CO₃), E 501(ii) potassium bicarbonate (KHCO₃).
- **WHO daily limits are the real "safe level" to report**: Na < 2000 mg/day;
  K ≥ 3510 mg/day (90 mmol). Practical risk is exceeded-Na (from NaHCO₃) and
  hyperkalemia (K₂CO₃/KHCO₃ in renal impairment), not intrinsic toxicity.
- INS numbering: 500(i) Na₂CO₃, 500(ii) NaHCO₃, 500(iii) sesquicarbonate;
  501(i) K₂CO₃, 501(ii) KHCO₃, 501(iii) sesquicarbonate.

## Chemistry write-up (drinking water, textbook — no PMID needed)
- NaHCO₃ → Na⁺ + HCO₃⁻; carbonate system CO₂ ⇌ H₂CO₃ ⇌ H⁺+HCO₃⁻ (pKₐ₁≈6.35) ⇌
  H⁺+CO₃²⁻ (pKₐ₂≈10.33). At drinking-water pH the dominant species is **HCO₃⁻**.
- K₂CO₃ → 2K⁺ + CO₃²⁻; **CO₃²⁻ hydrolyses → HCO₃⁻ + OH⁻** (makes the solution
  strongly alkaline, pH≫NaHCO₃). KHCO₃ → K⁺ + HCO₃⁻ (weakly alkaline).
- For these don't force a fake citation — the equilibrium is established general
  chemistry; present it directly rather than attaching an invented DOI.

## Windows gotcha (this box)
- Default `python` is a venv with **no pip / no pymupdf**; `pip` belongs to Python 3.14
  (`/c/Python314/python.exe -m pip`). For PDF/text extraction run
  `/c/Python314/python.exe` (has `fitz`/`pymupdf`). Prefer `import pymupdf` over the
  deprecated `import fitz` alias.
