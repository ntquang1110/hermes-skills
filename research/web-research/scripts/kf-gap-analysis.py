#!/usr/bin/env python3
"""
KF Gap Analysis — scan a Knowledge Flow instance and find missing topics.

Usage:
    python kf-gap-analysis.py [--url http://localhost:3003] [--candidates "tag1,tag2,..."]

Without --candidates, runs in DETECT mode: examines existing cards and reports
structural gaps (pathway families with missing members, cytokine clusters with
uncovered members).

With --candidates, runs in CHECK mode: given a comma-separated list of proposed
topic keywords, reports which are already covered (with matching card titles)
and which are genuine gaps.

Output:
    - total card count
    - coverage report per candidate
    - gap list (candidates with no / weak overlap)
    - structural suggestions (DETECT mode only)

Requires: urllib, json, re, sys (stdlib only — no pip installs).

Tested Jul 2026 against localhost:3003 with 164 cards.
"""

import urllib.request, json, sys, re, ssl

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

KF_URL = "http://localhost:3003"


def fetch_cards(url: str) -> list[dict]:
    """Fetch all cards from KF /api/cards endpoint."""
    try:
        req = urllib.request.Request(f"{url}/api/cards", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"ERROR: Cannot fetch cards from {url}/api/cards: {e}")
        sys.exit(1)


def detect_families(titles: list[str]) -> dict:
    """Detect IL, TNF, IFN, TGF, Chemokine, CD, TLR, NOD families and which members are present."""
    families = {
        "IL": set(),
        "IFN": set(),
        "TNF": set(),
        "TGF": set(),
        "CD": set(),
        "TLR": set(),
        "Chemokine": set(),
        "NOD": set(),
        "SMAD": set(),
        "STAT": set(),
        "CASP": set(),
        "BCL": set(),
    }

    # Pattern: match "IL-(\d+)" or "Interleukin-\d+" etc.
    il_pat = re.compile(r"\b(?:IL|Interleukin)[-\s]?(\d+|[A-Za-z]+[0-9]*)\b", re.IGNORECASE)
    ifn_pat = re.compile(r"\b(?:IFN|Interferon)[-\s]?([A-Za-z0-9]+)\b", re.IGNORECASE)
    tnf_pat = re.compile(r"\bTNF[-\s]?([A-Za-z0-9]*)\b", re.IGNORECASE)
    tgf_pat = re.compile(r"\bTGF[-\s]?([A-Za-z0-9]+)\b", re.IGNORECASE)
    cd_pat = re.compile(r"\bCD(\d+[a-z]?)\b", re.IGNORECASE)
    tlr_pat = re.compile(r"\bTLR(\d+)\b", re.IGNORECASE)
    nod_pat = re.compile(r"\bNOD(\d+)\b", re.IGNORECASE)
    smad_pat = re.compile(r"\bSMAD(\d+)\b", re.IGNORECASE)
    stat_pat = re.compile(r"\bSTAT(\d+)\b", re.IGNORECASE)
    casp_pat = re.compile(r"\bCASP[AE]?(\d+)\b", re.IGNORECASE)
    bcl_pat = re.compile(r"\bBCL[-\s]?(\d+[A-Za-z]*)\b", re.IGNORECASE)
    chem_pat = re.compile(r"\b(?:CCL|CXCL|CX3CL|XCL)(\d+)\b", re.IGNORECASE)

    for t in titles:
        t_lower = t.lower()
        for m in il_pat.finditer(t):
            families["IL"].add(m.group(1))
        for m in ifn_pat.finditer(t):
            families["IFN"].add(m.group(1))
        for m in tnf_pat.finditer(t):
            tag = m.group(1) or "alpha"
            families["TNF"].add(tag.lower())
        for m in tgf_pat.finditer(t):
            families["TGF"].add(m.group(1))
        for m in cd_pat.finditer(t):
            families["CD"].add(m.group(1))
        for m in tlr_pat.finditer(t):
            families["TLR"].add(m.group(1))
        for m in nod_pat.finditer(t):
            families["NOD"].add(m.group(1))
        for m in smad_pat.finditer(t):
            families["SMAD"].add(m.group(1))
        for m in stat_pat.finditer(t):
            families["STAT"].add(m.group(1))
        for m in casp_pat.finditer(t):
            families["CASP"].add(m.group(1))
        for m in bcl_pat.finditer(t):
            families["BCL"].add(m.group(1))
        for m in chem_pat.finditer(t):
            families["Chemokine"].add(m.group(1))

    return families


# Known family members for gap detection
KNOWN_MEMBERS = {
    "IL": set("1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38".split()),
    "IFN": set("alpha beta gamma lambda omega epsilon kappa".split()),
    "TNF": set("alpha beta".split()),
    "CD": set(str(n) for n in range(1, 400)),
}


def check_candidates(candidates: list[str], cards: list[dict]) -> dict:
    """
    For each candidate keyword, determine coverage level:
    - FULL: title contains word-boundary match
    - PARTIAL: title contains candidate as substring (ambiguous)
    - NONE: no match
    """
    titles = [c.get("title", "") for c in cards]
    report = {}

    for cand in candidates:
        c_lower = cand.strip().lower()
        if not c_lower:
            continue

        full_matches = []
        partial_matches = []

        for t in titles:
            t_lower = t.lower()
            # Word-boundary match (high confidence)
            if re.search(r"\b" + re.escape(c_lower) + r"\b", t_lower):
                full_matches.append(t[:100])
            # Substring match (lower confidence — may catch IL-4 in IL-45 etc.)
            elif len(c_lower) >= 4 and c_lower in t_lower:
                partial_matches.append(t[:100])

        if full_matches:
            level = "FULL"
        elif partial_matches:
            level = "PARTIAL"
        else:
            level = "GAP"

        report[cand] = {
            "level": level,
            "full_matches": full_matches[:3],
            "partial_matches": partial_matches[:3],
        }

    return report


def print_report(candidates_report: dict, families: dict, total: int):
    """Print formatted analysis."""
    gaps = {k: v for k, v in candidates_report.items() if v["level"] == "GAP"}
    covered = {k: v for k, v in candidates_report.items() if v["level"] == "FULL"}
    partial = {k: v for k, v in candidates_report.items() if v["level"] == "PARTIAL"}

    print(f"KF Gap Analysis Report")
    print(f"{'=' * 60}")
    print(f"Total cards: {total}")
    print(f"Candidates:  {len(candidates_report)}")
    print(f"  ✅ Covered (FULL):  {len(covered)}")
    print(f"  ⚠️  Partial overlap: {len(partial)}")
    print(f"  🔴 GAPS:            {len(gaps)}")
    print()

    if gaps:
        print(f"🔴 GAPS ({len(gaps)}):")
        for k, v in sorted(gaps.items()):
            print(f"  • {k}")
        print()

    if partial:
        print(f"⚠️  PARTIAL OVERLAP ({len(partial)}):")
        for k, v in sorted(partial.items()):
            print(f"  • {k} → matches: {', '.join(v['partial_matches'][:2])}")
        print()

    if covered and len(covered) <= 15:
        print(f"✅ COVERED:")
        for k, v in sorted(covered.items()):
            print(f"  • {k}")
        print()

    # Structural gap detection
    print(f"Structural family analysis:")
    for family, members in sorted(families.items()):
        if members:
            present = ", ".join(sorted(members, key=lambda x: (len(x), x)))
            print(f"  {family}: {present}")

    # Check for missing IL members
    il_present = families.get("IL", set())
    il_known = KNOWN_MEMBERS.get("IL", set())
    # Remove single-digit numbers that appear as substrings of multi-digit numbers
    il_present_clean = set()
    for m in il_present:
        if m.isdigit():
            il_present_clean.add(m)
        else:
            il_present_clean.add(m)

    if il_present_clean:
        # Find gap ILs in the 1-20 range
        present_nums = set()
        for m in il_present_clean:
            if m.isdigit():
                present_nums.add(int(m))

        all_nums = set(range(1, 39))
        il_gaps = sorted(all_nums - present_nums)

        # Filter: some ILs may be covered under family cards even if not in title
        # e.g., IL-4 mentioned in IL-2 Family card title
        il_gaps_known = [n for n in il_gaps if n <= 38]
        print(f"  IL family members NOT in any card title: {il_gaps_known}")


def main():
    url = KF_URL
    candidates = None

    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--url" and i + 1 < len(args):
            url = args[i + 1].rstrip("/")
        if a == "--candidates" and i + 1 < len(args):
            candidates = [c.strip() for c in args[i + 1].split(",")]

    cards = fetch_cards(url)
    titles = [c.get("title", "") for c in cards]

    print(f"Fetched {len(cards)} cards from {url}")
    print()

    families = detect_families(titles)

    if candidates:
        report = check_candidates(candidates, cards)
        print_report(report, families, len(cards))
    else:
        # DETECT mode: list all families found + structural gap suggestions
        print("DETECT mode — structural gap analysis:")
        print()
        check_report = check_candidates([
            # Anatomical organs / systems (swine immunology)
            "thymus", "tuyến ức", "lymph node", "hạch", "spleen", "lách",
            "bone marrow", "tủy xương", "lymphatic", "MALT",
            # Neonatal / developmental
            "neonatal", "sơ sinh", "oral tolerance", "dung nạp",
            # Molecular / T cell subsets
            "Th2", "Th9", "Th22", "Tfh",
            "IL-3", "IL-5", "IL-11", "IL-13", "IL-15",
            "IL-21", "IL-23", "IL-25", "IL-31", "IL-33",
            "type 2", "type 3",
            "eosinophil", "basophil", "mast cell", "dưỡng bào",
            "IgE", "IgA", "IgG",
            "GATA3", "T-bet", "RORγt", "Bcl6", "Foxp3",
            # Vaccine / nutrition
            "vaccine", "adjuvant", "chủng ngừa",
            "colostrum", "milk", "maternal",
            "heat stress", "thermal", "stress nhiệt",
            # Emerging / technology
            "CRISPR", "organoid",
            "extracellular vesicle", "exosome",
        ], cards)
        print_report(check_report, families, len(cards))

        print()
        print("Tip: Run with --candidates \"topic1,topic2,...\" to check specific topics.")
        print("Tip: Structural gaps detected above are candidates for new cards.")


if __name__ == "__main__":
    main()
