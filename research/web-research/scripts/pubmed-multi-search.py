#!/usr/bin/env python3
"""
PubMed Multi-Angle Search + Summarizer — for knowledge-card compilation.

Usage:
    python pubmed-multi-search.py "query1" "query2" "query3" [--max 5] [--format card|table|list]

Queries are run independently; results are deduplicated by PMID.
Output formats:
    card   → Markdown table of papers, ready for insertion into a knowledge card
    table  → Simple ASCII table (default)
    list   → Bullet list with PMID + title + source + DOI

Requires: urllib (stdlib), json (stdlib), ssl (stdlib)
No pip installs needed.

Tested Jul 2026 — all NCBI E-utilities endpoints return JSON with no CAPTCHAs.
"""

import urllib.request, urllib.parse, json, ssl, sys, time, textwrap

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def pubmed_search(query: str, max_results: int = 5) -> list[str]:
    """Search PubMed, return list of PMIDs."""
    params = urllib.parse.urlencode({
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
    })
    url = f"{BASE}/esearch.fcgi?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, context=SSL_CTX, timeout=20) as resp:
        data = json.loads(resp.read().decode())
    return data.get("esearchresult", {}).get("idlist", [])


def pubmed_summaries(pmids: list[str]) -> dict:
    """Fetch titles, journals, DOIs, authors for a list of PMIDs."""
    if not pmids:
        return {}
    url = f"{BASE}/esummary.fcgi?db=pubmed&id={','.join(pmids)}&retmode=json"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, context=SSL_CTX, timeout=20) as resp:
        data = json.loads(resp.read().decode())
    result = {}
    for uid, info in data.get("result", {}).items():
        if uid == "uids":
            continue
        doi = info.get("elocationid", "")
        # Clean up DOI field
        if "doi: " in doi:
            doi = doi.split("doi: ")[-1].split(". ")[0].strip()
        authors = [a.get("name", "") for a in info.get("authors", [])[:3]]
        result[uid] = {
            "title": info.get("title", ""),
            "source": info.get("source", ""),
            "pubdate": info.get("pubdate", ""),
            "doi": doi,
            "authors": authors,
        }
    return result


def format_card(papers: dict) -> str:
    """Format as a Markdown table for knowledge-card insertion."""
    if not papers:
        return "_No papers found._"
    lines = [
        "| PMID | Năm | Tạp chí | Tựa đề | DOI |",
        "|------|-----|---------|--------|-----|",
    ]
    for pmid, info in papers.items():
        year = info.get("pubdate", "")[:4]
        title = info["title"][:90] + ("…" if len(info["title"]) > 90 else "")
        doi = info.get("doi", "")
        doi_link = f"doi:{doi}" if doi else ""
        lines.append(
            f"| {pmid} | {year} | {info['source'][:30]} | {title} | {doi_link} |"
        )
    return "\n".join(lines)


def format_table(papers: dict) -> str:
    """Simple ASCII table."""
    if not papers:
        return "No papers found."
    lines = []
    for pmid, info in papers.items():
        lines.append(
            f"[{pmid}] {info['title']}\n"
            f"  {info['source']} ({info.get('pubdate','')})\n"
            f"  Authors: {', '.join(info['authors'])}\n"
            f"  DOI: {info.get('doi', '')}\n"
        )
    return "\n".join(lines)


def format_list(papers: dict) -> str:
    """Bullet list."""
    lines = []
    for pmid, info in papers.items():
        lines.append(
            f"- PMID {pmid}: **{info['title']}** "
            f"({info['source']}, {info.get('pubdate','')}) "
            f"[doi:{info.get('doi','')}]"
        )
    return "\n".join(lines)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    fmt = "table"
    max_results = 5
    for i, a in enumerate(sys.argv[1:]):
        if a == "--format" and i + 2 < len(sys.argv):
            fmt = sys.argv[i + 2]
        if a == "--max" and i + 2 < len(sys.argv):
            max_results = int(sys.argv[i + 2])

    queries = args if args else [
        "miRNA mechanism gene regulation review",
        "miRNA cancer diagnosis biomarker",
        "miRNA therapeutic clinical trial 2025 2026",
    ]

    all_papers = {}
    for q in queries:
        pmids = pubmed_search(q, max_results)
        if pmids:
            summaries = pubmed_summaries(pmids)
            for pmid in pmids:
                if pmid not in all_papers:
                    all_papers[pmid] = summaries.get(pmid, {})
        time.sleep(1.5)  # critical pacing

    if fmt == "card":
        print(format_card(all_papers))
    elif fmt == "list":
        print(format_list(all_papers))
    else:
        print(format_table(all_papers))

    print(f"\n--- {len(all_papers)} unique papers total ---")


if __name__ == "__main__":
    main()
