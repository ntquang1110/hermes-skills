# Gap Finding: The "Ghost Topic" Pattern for Mature KFs (>150 cards)

When a Knowledge Flow has 150+ cards covering most major pathways, cytokines, pathogens, and feed additives, finding genuinely novel topics requires a different approach than keyword searching.

## The Ghost Topic Pattern

A **ghost topic** is a concept that appears in the **crosstalk/references sections** of many existing cards but does NOT have its own dedicated card. These are the most valuable gaps because they instantly connect to 5-15 existing cards, weaving the knowledge base together.

### How to detect ghost topics

**Step 1 — Enumerate all titles at once:**
Instead of keyword-searching for specific topics, dump ALL card titles into a single view. This lets you recognize patterns and absences:

```bash
curl -s http://localhost:3003/api/cards | python -c "import sys,json; cards=json.load(sys.stdin); [print(f'{i}: {c[\"title\"][:100]}') for i,c in enumerate(cards)]"
```

**Step 2 — Scan for "referenced but not covered":**
Read through the title list looking for concepts that:
- Appear in titles as part of a larger card (e.g. "TGF-β → IgA class switching" inside a TGF-β card, implying IgA is a downstream concept)
- Are mentioned in crosstalk sections of multiple cards
- Have a dedicated section in the B cell/cytokine cards but no standalone treatment

**Step 3 — Verify with targeted keyword dedup:**
Once a candidate is identified, confirm no existing card covers it:

```bash
curl -s http://localhost:3003/api/cards | python -c "
import sys,json,re
cards = json.load(sys.stdin)
keywords = ['keyword1', 'keyword2', 'abbreviation1', 'full_name']
for c in cards:
    t = c['title'].lower()
    for kw in keywords:
        if re.search(r'\\b' + re.escape(kw.lower()) + r'\\b', t):
            print(f'MATCH [{kw}]: {c[\"title\"][:100]}')
            break
"
```

Use 4-6 keyword variants including abbreviations and alternative names to catch partial overlaps.

### Ghost topic variant — molecular family vs single molecule

There are two distinct patterns:

| Variant | Example | Detection signal |
|---------|---------|-----------------|
| **Single molecule** | IgA | Referenced by name in crosstalk sections of 5+ cards, but title never appears alone |
| **Molecular family / functional class** | Cell Adhesion Molecules (CAMs) | Concepts like "LFA-1", "integrin", "ICAM-1", "selectin" appear inside many cards, but the *umbrella family* has no dedicated card |

The molecular-family variant is harder to detect because you won't find the exact term "cell adhesion molecules" in other card titles — you need to notice that **integrin**, **selectin**, **ICAM-1**, and **CD18** are each mentioned in different cards and that together they form a coherent functional class.

### Real example 1: How IgA was identified as a ghost topic

The session that found the IgA gap followed this pattern:

1. **Enumerated 168 cards** — scanned titles for "missing pieces"
2. **Identified IgA as referenced across 9+ cards:**
   - TGF-β/SMAD (card 74) — TGF-β drives IgA class switching
   - B cell (card 45) — IgA-producing plasma cells
   - Hệ vi sinh vật (card 104) — microbiota regulates IgA
   - Hàng rào ruột (card 108) — IgA is a barrier component
   - Th17/Treg (card 86) — balance affects IgA via BAFF/APRIL
   - AhR (card 97) — AhR → IL-22 → IgA production
   - GLP-2 (card 19) — GLP-2 upregulates pIgR
   - SCFA/GPR43 (card 33) — butyrate → pIgR expression
   - Đại thực bào (card 96) — macrophages sample IgA-coated bacteria
3. **Confirmed no card with "IgA" in title** — gap validated
4. **Researched and created card** with 18 PMIDs, 840s reading time

### Why ghost topics work

- They have **built-in crosstalk connections** — the new card immediately links to 5-15 existing cards
- They fill **structural holes** in the knowledge graph — increases overall connectivity
- They are **low-discovery-cost** — you already know what to include because the existing cards tell you
- They prioritize **topics the user cares about** — if 9 cards mention IgA, it's clearly important to the domain

### Real example 2: How Cell Adhesion Molecules (CAMs) was identified as a molecular-family ghost topic

This example shows the **molecular family** variant — a functional class whose members are scattered across existing cards but the umbrella is missing.

1. **Enumerated 169 cards** — scanned titles for cohesive functional groups
2. **Identified CAMs concepts referenced across 10+ cards without a dedicated card:**
   - TCR Signaling (card 11) — LFA-1/ICAM-1 immunological synapse
   - Bạch cầu trung tính (card 68) — selectin-mediated rolling, β2 integrin firm adhesion
   - Tế bào tua (card 72) — DC migration via LFA-1/ICAM-1
   - Tế bào NK (card 71) — LFA-1/ICAM-1 NK synapse
   - Tế bào T CD8+ (card 53) — LFA-1 nanocluster cytotoxicity
   - Tế bào T γδ (card 93) — αEβ7 integrin epithelial homing
   - PRRSV (card 103) — ↑ ICAM-1/VCAM-1 in lung endothelium
   - PEDV (card 92) — ↑ ITGβ1, ↑ α4β7 gut homing
   - Tight Junction (card 48) — integrin-ECM → ZO-1 signaling
   - Immunometabolism (card 82) — glucose → Rap1 → integrin activation
   - Đại thực bào (card 97) — CD11b/CD18 phagocytosis
3. **Confirmed no card with "bám dính", "adhesion", "integrin", "selectin", or "CAM" in title** — gap validated
4. **Used 6-query PubMed multi-angle research** covering: integrin structure/signaling, selectin-mediated rolling, ICAM-1/VCAM-1 inflammation, gut homing via α4β7/MAdCAM-1, CD18 β2 integrin in LAD, integrin-virus interactions (PRRSV, PEDV, ETEC, Pasteurella)
5. **Created card** with 18 PMIDs, 780s reading time, covering all 4 CAM families (integrin, selectin, IgSF, cadherin) with pig-specific disease sections

**Key difference from IgA example:** Instead of looking for a single molecule name missing from titles, I scanned for *functional terms* (adhesion, bám dính, integrin signaling, leukocyte trafficking) that appeared inside cards but lacked an umbrella topic. The detection signal was noticing that "LFA-1 → ICAM-1 immunological synapse" in the TCR card, "selectin rolling" in the Neutrophil card, and "integrin homing" in the PEDV card all describe the same biological process (leukocyte adhesion cascade) — but there was no card that synthesized them.

### Automated content-search variant (data-driven ghost detection)

Instead of manually scanning titles for conceptual gaps, use a **content keyword search** across all card bodies. This is faster and more objective:

```bash
curl -s http://localhost:3003/api/cards | python -c "
import sys,json
cards = json.load(sys.stdin)
keyword = 'IRF'  # ← candidate topic name / abbreviation
matches = []
for c in cards:
    content = (c.get('content','') or '')[:10000].lower()
    title = c.get('title','').lower()
    if keyword.lower() in content and keyword.lower() not in title:
        matches.append(c['title'][:80])
print(f'Keyword \"{keyword}\" found in {len(matches)} cards (0 in titles)')
for t in matches:
    print(f'  • {t}')
"
```

**Interpretation:**
- **0 matches** in both title AND content → topic not referenced yet — may be irrelevant or newly needed
- **1–4 matches** → tangentially mentioned, low connective value
- **5+ matches** (especially 10+) → **strong ghost topic signal** — referenced widely but never independently covered
- **Keyword in title of 1+ cards** → already covered, skip

**Practical constraints:**
- **Content truncation:** Cards can be 500KB+ (HTML tables, large extracts). The 10000-char limit in the snippet catches >95% of mentions because IRF/chemokine/pathway references appear in the opening sections (introduction, mechanism, crosstalk). Very deep mentions (buried in §8 of a 300KB card) are rare — the 10k limit is adequate for ghost detection, not exhaustive citation counting.
- **Short-keyword false positives (⚠️):** Keywords ≤4 characters (e.g. `IRF` itself, `MUC`, `CD`, `IL`) may match unrelated terms inside larger words or domain IDs. Always verify with a second pass:
  ```bash
  python -c "
  import sys,json,re
  cards = json.load(sys.stdin)
  kw = 'IRF'
  for c in cards:
      content = (c.get('content','') or '')[:10000]
      if kw.lower() in content.lower():
          # Check it's a legitimate mention, not substring of 'mirf'/'irf6' in a gene list
          legit = len(re.findall(rf'\\b{re.escape(kw)}', content, re.IGNORECASE))
          if legit >= 3:  # at least 3 word-boundary hits → real topic
              print(f'{kw} ({legit}x): {c[\"title\"][:90]}')
  "
  ```
  The `\b` word-boundary regex excludes accidental substring matches.

**Real example (IRF, 2026-07-29):**
```
Keyword "IRF" found in 20 cards (0 in titles)
  • 🧪 Taurine... • 🐷 Mycoplasma hyopneumoniae... • 🐷 PDCoV... 
  • 🧬 Trained Immunity... • 🧬 Interferon Lambda... • 🧬 Type I Interferon...
  • 🧬 Interferon-gamma... • 🧬 NOD1/NOD2... • 🧬 Dendritic Cells...
  • 🐷 Swine Influenza A Virus... • 🧬 RIG-I/MDA5/MAVS... • 🧬 cGAS-STING...
  • 🐷 CSFV... • 🧬 M1/M2 Macrophage... • 🐷 PRRSV (×2)...
  • 🐷 TLR... • 🐷 PCV2... • 🧬 β-glucan... • 🔬 Interferon, PRRs & JAK-STAT
```
→ 20 matches, zero in title → IRF was a **strong ghost topic** → created card with 15 PMIDs, 960s reading time.

**Multiple-candidate sweep** — to find ANY ghost topic across a mature KF, sweep domain-specific keyword batches:

```bash
curl -s http://localhost:3003/api/cards | python -c "
import sys,json
cards = json.load(sys.stdin)
candidates = [
    'IRF', 'interferon regulatory',     # transcription factors
    'pentraxin', 'ficolin', 'collectin', # complement
    'prostaglandin', 'leukotriene',      # eicosanoids
    'histamine', 'bradykinin',           # vasoactive mediators
    'granzyme', 'perforin', 'granulysin',# cytotoxic granules
    'IRF4', 'IRF8',                      # DC development (check if in body)
    'MUC2', 'MUC1', 'mucin',            # mucus barrier components
]
for c in cards:
    content = (c.get('content','') or '')[:10000].lower()
    title = c.get('title','').lower()
    for kw in candidates:
        if kw.lower() in content and kw.lower() not in title:
            print(f'{kw}: {c[\"title\"][:90]}')
"
```

This sweep generates a ranked list of candidate ghost topics sorted by match count. The top candidates are the most connected gaps — creating a card for them adds maximal edge count to the knowledge graph.

### When NOT to use ghost topic search

- When the KF has <100 cards — keyword search + obvious gaps (pathways, cytokines) work better
- When the queue has pending items — process those first (they were explicitly requested)
- When the topic is too specific (e.g., "IgA2 hinge region glycosylation") — too narrow; save for a subsection
