# Virus/Pathogen Knowledge Card Template

Use this section outline when compiling a Knowledge Flow card about a virus, bacterium, or pathogen that affects livestock. This template was validated on CSFV (Classical Swine Fever Virus) and is directly applicable to other swine pathogens (PRRSV, PCV2, PEDV, ASFV, Swine Influenza, PRV, Mycoplasma, Lawsonia, Brachyspira, etc.).

## Section outline (in order)

| # | Section | Content | Sources |
|---|---------|---------|---------|
| 1 | **🧬 Tổng quan (Overview)** | Taxonomy (family, genus), disease name (EN + VI), WOAH/OIE status, host range, economic impact | Wikipedia summary |
| 2 | **🧱 Cấu trúc virus & genome** | Virion morphology (size, envelope, symmetry), genome type (+ssRNA/dsDNA), genome map (5' → 3'), length (kb), IRES/cap, polyprotein strategy | Wikipedia + review articles |
| 3 | **🔬 Protein: Cấu trúc và chức năng** | **TABLE** — Protein name, type (structural/nonstructural), size (kDa), function. Include all major proteins. Add details for proteins unique to this virus (e.g. Npro + Erns for pestiviruses) | Wikipedia + primary literature |
| 4 | **🛡️ Cơ chế trốn miễn dịch (Immune Evasion)** | Per-mechanism table: mechanism, target protein/pathway, consequence, year discovered. Cover all known evasion strategies. Use mermaid flowchart for multi-pathway mechanisms. Compare with related viruses | PubMed reviews (PMID search: `[virus name] immune evasion`) |
| 5 | **🧪 Cơ chế bệnh sinh (Pathogenesis)** | Transmission routes (direct/indirect/vertical), incubation period, clinical forms table (acute/subacute/chronic/atypical), mortality rates, gross pathology (bulllet points with Vietnamese terms), histopathology | Wikipedia + vet pathology textbooks |
| 6 | **🔬 Phân loại genotype** | **TABLE** — Genotype, subtypes, geographic distribution, characteristics. Vietnamese-specific genotype data. Cross-protection implications | PubMed (genotyping studies) |
| 7 | **💉 Vaccine & Chiến lược phòng bệnh** | **TABLE** — Vaccine type, name/strain, advantages, disadvantages. Cover: MLV, subunit, recombinant, mRNA if applicable. Include: strain name, route, schedule, efficacy, limitations. DIVA strategy explanation with marker vaccine principle. Vietnamese vaccination context | PubMed (vaccine reviews) + WOAH docs |
| 8 | **🔬 Chẩn đoán (Diagnosis)** | **TABLE** — Method, target, time, advantage. Include: PCR/RT-qPCR, ELISA (Ag/Ab), FAT, virus isolation, histopathology. Differential diagnosis section: list diseases with similar presentation, key distinguishing tests. | WOAH manual + diagnostic literature |
| 9 | **🌏 Dịch tễ học toàn cầu** | **TABLE** — Region, status, control measures. Cover: Vietnam, EU, China, USA, Japan, Korea. Note recent outbreaks. Wild reservoir role | OIE WAHIS + review articles |
| 10 | **🎯 Kết luận & ý nghĩa cho chăn nuôi** | 5-8 numbered takeaway points. Practical recommendations for farmers/vets. Future trends (vaccine development, elimination programs) | Synthesis |
| 11 | **📚 Tài liệu tham khảo** | **TABLE** — PMID, Journal (Year), brief description of what the paper contributes. Anchor every mechanism claim in content to a PMID. | All sources used above |

## PubMed query pattern for viruses

For a new virus/pathogen research, use these 4-5 query angles (replace `[virus]` with the actual name):

```python
queries = [
    '[virus] immune evasion innate immunity',
    '[virus] pathogenesis molecular mechanism',
    '[virus] vaccine efficacy control',
    '[virus] genotype diversity epidemiology',
    '[virus] structure protein function',
]
```

## Card formatting conventions

- **Title**: `🐷 [Virus acronym] ([Full name]) — [Vietnamese name]: [brief subtitle]`
- **First section**: starts with bold definition of acronym + one-liner
- **Blockquotes** (`> `) for: key epidemiological facts, critical concepts (DIVA, immunotolerance)
- **Mermaid code blocks** (```mermaid) for: multi-pathway mechanism diagrams
- **Two-column tables** for: paired comparisons (Npro vs Erns)
- **Wide tables** for: proteins, genotypes, vaccines, diagnostics
- **Final check**: every PMID in the references table should have at least one inline citation in the content

## Pitfalls

- **VI Wikipedia often absent for technical viruses** — the Vietnamese Wikipedia page may redirect to ASFV or return unrelated results. Always search both `en` and `vi`; expect to rely on EN for content.
- **Genotype nomenclature varies by virus** — CSFV uses 1/2/3, ASFV uses p72 genotypes (I-XXIV), PRRSV uses 1/2 (European/North American). Verify the correct system before writing.
- **Vaccine section must distinguish MLV vs DIVA** — many livestock viruses have both. The DIVA concept is crucial for eradication programs.
- **Incubation period ranges differ by virulence** — always state the range and note that regulatory quarantine uses the outer limit (e.g. 21 days for CSF).
