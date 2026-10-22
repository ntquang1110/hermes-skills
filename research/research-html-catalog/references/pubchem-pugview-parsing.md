# PubChem / PUG-View parsing for chemistry catalogs

Validated 10/2026 building a terpenoid report: 52 PubChem records, 12 full PUG-View records
(4,948 extracted rows), 336 PubMed records. Every snippet below ran against real collected data.

## 1. Recursive PUG-View walker (the one that matters)

PUG-View JSON nests arbitrarily deep and puts the human-readable value at
`Section[].Information[].Value.StringWithMarkup[].String`.

**Broken version** — prints `total rows: 0` and looks like empty data:

```python
for s in secs:
    for info in (s.get('Information') or []):
        v = info.get('Value')
        if isinstance(v, dict) and 'StringWithMarkup' in v:   # never matches: it's nested deeper
            ...
```

**Working version:**

```python
def flat_vals(v):
    out = []
    if isinstance(v, dict):
        if isinstance(v.get('StringWithMarkup'), list):
            for s in v['StringWithMarkup']:
                if isinstance(s, dict) and s.get('String', '').strip():
                    out.append(s['String'].strip())
        for k in ('String', 'Number', 'DateISO8601'):
            if k in v:
                val = v[k]
                out += [str(x) for x in val] if isinstance(val, list) else [str(val)]
    elif isinstance(v, list):
        for x in v:
            out += flat_vals(x)
    return out

def walk(secs, path=""):
    rows = []
    for s in secs:
        head = s.get('TOCHeading', '')
        p = (path + " > " + head) if head else path
        for info in (s.get('Information') or []):
            vals = flat_vals(info.get('Value'))
            if vals:
                rows.append((p, " || ".join(vals), info.get('ReferenceNumber'), info.get('URL', '')))
        rows += walk(s.get('Section') or [], p)   # recursion is what makes it work
    return rows
```

`TOCHeading` gives the breadcrumb path (`"> Safety and Hazards > Hazards Identification > GHS Classification"`),
which is what you filter on to find pharmacology/toxicity/regulatory blocks.

**Debugging order when row count is 0:** dump one record's shape first —
`print(list(rec['Record']['Section'][0].keys()))`, then recurse `Section[]['Section']`.
Do NOT conclude the source is empty.

## 2. physchem.json value flattener (dedupe, preserve order)

Shape is `[[{'String': 'x'}], [{'String': 'y', 'Markup': [...]}], ...]` — the same fact appears
from multiple depositors (HSDB, NTP, ...) and that redundancy is provenance worth keeping, but
dedupe exact repeats:

```python
def phys(physchem, name, field):
    d = physchem.get(name) or {}
    out = []
    def rec(x):
        if isinstance(x, dict):
            if isinstance(x.get('String'), str) and x['String'].strip():
                out.append(x['String'].strip())
            for k, v in x.items():
                if k != 'String':
                    rec(v)
        elif isinstance(x, list):
            for y in x:
                rec(y)
    rec(d.get(field) or [])
    seen, res = set(), []
    for s in out:
        if s not in seen:
            seen.add(s); res.append(s)
    return res
```

Render as `" · ".join(vals[:3])`. Never `str(value)` — you get Python reprs in the table.

## 3. Compound resolver (name join does NOT work)

Same substance, three sources, three spellings:

| collected key | PubChem PUG title | record `RecordTitle` |
|---|---|---|
| `Ursolic acid` | Ursolic acid | `(+)-Ursolic Acid` |
| `beta-Carotene` | beta-Carotene | `Beta-Carotene` |
| `Lutein` | Lutein | `Lutein A` |
| `d_limonene` | d-limonene | (absent) |

Case-sensitive matching recovered 5/12. Fallback chain:

```python
PVKEY = {str(title).strip().lower(): title for title in record_titles}

def pv_title_for(name, cid, inchikey, pcid_to_title, pc_name):
    t = pcid_to_title.get(str(cid))
    if t and str(t).strip().lower() in PVKEY:
        return PVKEY[str(t).strip().lower()]
    for cand in (name, pc_name(name)):
        if cand and str(cand).strip().lower().lstrip("(+)-").strip() in PVKEY:
            return PVKEY[str(cand).strip().lower().lstrip("(+)-").strip()]
    if inchikey:                        # first skeleton block is the stereochemistry-free part
        skel = inchikey.split('-')[0]
        for k in PVKEY:
            if k.startswith(skel):
                return PVKEY[k]
    return None
```

Also treat CID as a hint only: PubChem CID ≠ PUG-View file CID for stereo variants
(e.g. beta-Carotene CID 5280489 in the PUG-View file vs a different CID in the property table).
After building, always print the linked/total count — the tell that the join failed:

```python
print("compounds with full PUG-View record:", sum(1 for c in compounds if c["has_pv"]))
```

## 4. External IDs out of the walker

```python
def pv_ids(rows, key):
    out = []
    for path, text, refnum, url in rows:
        if re.search(r">\s*" + re.escape(key) + r"$", path):   # leaf section = ends with key
            out.append({"id": text, "ref": refnum, "url": url})
    return out
```

Keys that work: `CAS`, `ChEBI ID`, `ChEMBL ID`, `DrugBank ID`, `Lipid Maps ID (LM_ID)`,
`InChIKey`, `ATC Code`, `MeSH Pharmacological Classification`.

## 5. ECHA GHS aggregate parser — and the integrity trap

```python
for path, text, refnum, url in rows:
    if not re.search(r"Hazards Identification", path, re.I):
        continue
    if re.search(r"GHS Classification", path, re.I):
        stmts = re.findall(r"(H\d{3}[^:|]{0,80}?)\s*\[", text)
        klass = re.findall(r"(Aquatic Acute \d|Skin Irrit\. \d|Eye Dam\. \d|Org\. Perox\. \w|"
                           r"STOT (?:SE|RE) \d|Muta\. \w|Repr\. \w)", text)
        m = re.search(r"does not meet GHS hazard criteria for ([\d.]+)%", text)
```

**The trap:** "Not Classified" from ECHA means *no company filed a notification*, not *proven safe*.
Real example — ursolic acid: "does not meet GHS hazard criteria for 98.9% (92 of 93) of all reports".
Rendering that as "an toàn" inverts the evidence. Always surface the denominator in the HTML:

> GHS "Not Classified" vì 92/93 doanh nghiệp không nộp thông báo — KHÔNG phải vì đã chứng minh an toàn.

Contrast artemisinin, which genuinely IS classified: `H242` (heating may cause a fire — it is a
peroxide), `H400/H410` (very toxic to aquatic life). Same "Not Classified" label family, opposite
meaning — always read the H-codes, never just the class name.

## 6. Report evidence honesty for chemistry catalogs

- Separate **measured secondary-source values** (PubChem/PUG-View = "nguồn thứ cấp đã kiểm tra của
  NCBI, KHÔNG phải đo trong phòng thí nghiệm của chúng ta") from primary experimental claims.
- State empty-query holes out loud: 25/90 PubMed queries returned 0 hits. Say "trong kho truy vấn
  chúng tôi không thu được bài nào về X" rather than silently omitting the topic — it becomes a
  stated gap instead of a fake gap.
- Report **negative/null results** with the same prominence as positive ones (AREDS2 adding
  lutein/zeaxanthin gave no overall benefit; beta-carotene high-dose paradox in smokers).
- Attach a per-compound data-completeness score (e.g. `n_phys` out of 9 available physicochemical
  fields). Sparse ≠ unimportant; it usually means "little public data", which is itself the finding.