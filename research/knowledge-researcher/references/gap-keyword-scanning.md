# Keyword-Dictionary Gap Scanning

A practical, automated alternative to manual ghost-topic identification. Instead of visually scanning the card list, define candidate topics with multiple keyword variants and let Python check programmatically.

## How it works

1. Define a dictionary of candidate topics, each with a list of search keywords
2. Fetch all cards from `/api/cards`
3. For each candidate, check if ANY existing card's title or early content matches ANY keyword
4. Output GAP (not covered) vs COVERED for each candidate

## Code pattern

```python
import sys, json, re, urllib.request

cards = json.loads(
    urllib.request.urlopen("http://localhost:3003/api/cards", timeout=10).read()
)

# Define candidates with multiple keyword variants per topic
# Include full names, abbreviations, synonyms — anything a card title might use
candidates = {
    "Vitamin A / Retinoic Acid": [
        "vitamin a", "retinoic acid", "retinol", "retinal", "RAR", "RXR", "RA"
    ],
    "TRP channels": [
        "TRP channel", "TRPV", "TRPA", "TRPM", "TRPC",
        "transient receptor", "capsaicin"
    ],
    "Mycoplasma hyopneumoniae": [
        "mycoplasma hyopneumoniae", "M. hyopneumoniae", "MHYO",
        "enzootic pneumonia", "mycoplasmal pneumonia"
    ],
    "Enteroendocrine cells / gut hormones": [
        "enteroendocrine", "GLP-1", "GLP1", "PYY", "ghrelin",
        "secretin", "CCK", "GIP"
    ],
    "CaSR signaling": [
        "calcium sensing receptor", "CaSR", "CaSR signaling", "GPRC6A"
    ],
    "Zinc transporters (ZIP/ZnT)": [
        "zip transporter", "znt transporter", "zinc transporter",
        "SLC39A", "SLC30A"
    ],
    # Add more candidates as needed — one per line
}

for topic, keywords in candidates.items():
    hits = []
    for c in cards:
        combined = (c["title"] + " " + c.get("content", "")[:500]).lower()
        for kw in keywords:
            if re.search(r"\b" + re.escape(kw.lower()) + r"\b", combined):
                hits.append(c["title"][:70])
                break
    if hits:
        print(f"COVERED: {topic}")
        for h in hits[:3]:
            print(f"    -> {h}")
    else:
        print(f"GAP: {topic}")
    print()
```

## Tips for keyword selection

| Keyword type | Example | Notes |
|-------------|---------|-------|
| **Full name** | `"mycoplasma hyopneumoniae"` | Catches exact title matches |
| **Abbreviation** | `"MHYO"`, `"CaSR"` | Short forms used in titles |
| **Synonym** | `"enzootic pneumonia"`, `"mycoplasmal pneumonia"` | Alternative names |
| **Related term** | `"capsaicin"` for TRP channels | Indicates partial coverage |
| **Gene symbol** | `"SLC39A"`, `"GPRC6A"` | May appear in content when not in title |

## Pitfalls

- **Short keywords collision**: `CD28` matches `CD8`, `CD86`, `CD80`. Fix: use word-boundary regex (`\b`) as shown above. If a keyword is 3-4 chars and collision-prone, replace it with a longer synonym (e.g., use `"calcium sensing"` instead of `"CaSR"`).
- **Content buffer too short**: `[:500]` covers the first 500 chars of content — enough for summary/tables but not full text. Increase to `[:2000]` if cards have long introductions before keyword mentions.
- **Partial coverage false positive**: A card may mention a topic in passing (e.g., "TRP channels like TRPV1 are involved...") without being about that topic. The result is a false GAP label — the topic IS mentioned but deserves its own card anyway. Treat `COVERED` as "don't create a duplicate of this exact topic" and `GAP` as "needs verification — could be a false positive if the card list has partial coverage."
- **Always pair with symmetry check**: This automated scan is a accelerator for Step 2 (ghost topic identification). Combine it with the symmetry table in Step 3 for maximum reliability.

## Integration with gap-finding workflow

Run this scan first during Step 1 (card enumeration), then use the GAP list as input to Step 3 (symmetry check). Topics that show as GAP AND appear in the symmetry table's "Missing gaps" column are highest priority.

Example: if the scan shows `Mycoplasma hyopneumoniae` as GAP and the symmetry table shows it's a missing bacterium, that's your next research target.
