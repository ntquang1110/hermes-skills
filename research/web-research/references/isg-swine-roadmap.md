# ISG (Interferon-Stimulated Genes) Swine Roadmap

Research date: 2026-08-02 (cron rotation index 2 — Sinh học). Result: KF card `2f971276-d486-4c30-963e-5230a9a44f38`, reading time 720s, 24 tags.

## Summary table

| Item | Content |
|------|---------|
| What | ~450 genes induced by IFN (mostly type I); ~10% of human genome IFN-regulated. The downstream effector layer of innate antiviral immunity. |
| Key effectors (porcine-verified) | Mx1 (dynamin GTPase), OAS1/OAS2/OASL → RNase L (2-5A system), PKR/EIF2AK2 → eIF2α, ISG15 + ISGylation (UBE1L/UBE2E2/HERC5), Viperin/RSAD2 (ddhCTP + nsp8 binding), BST2/Tetherin (virion tethering + selective autophagy), CH25H/25HC (entry block) |
| Why it matters for pigs | PRRSV/ASFV/PEDV/PDCoV/PoRVA all encode dedicated ISG-antagonists (Nsp11, Nsp1β, Nsp2, E, L11L, MGF110-7L, NSP4). Understanding ISG = understanding immune evasion + therapy targets. |
| Gap-finding note | KF had 223 cards with Type I IFN / RIG-I-MDA5 / cGAS-STING / JAK-STAT cards but NO dedicated ISG card — classic ghost topic (referenced by 10+ cards, never independently covered). |

## Tested PubMed queries (Aug 2026 — all returned relevant porcine hits)

| Query | Hits | Best PMIDs |
|-------|------|------------|
| `ISG15 porcine PRRSV antiviral interferon` | 6 | 36921497, 39645133, 31043527, 37008366 |
| `Mx1 OAS PKR pig antiviral interferon stimulated genes` | 1 (too narrow — expand) | 31043527 |
| `viperin RSAD2 porcine virus` | 1 (narrow but gold) | 41941904 |
| `tetherin BST2 pig virus infection` | 6 | 31868081, 24931347, 24717029, 24448163 |
| `interferon stimulated genes pig intestinal epithelial` | 6 | 42338383, 40319282, 40941331 |
| `Mx1 porcine influenza resistance antiviral` | 6 | 40565228, 40406095 |
| `OAS RNase L porcine virus replication` | 6 | 41618367, 30885302, 26437676, 30013278 |
| `protein kinase R PKR porcine virus` | 6 | 41291300, 36377947 |
| `CH25H 25-hydroxycholesterol porcine antiviral` | 6 | 39454283, 38140647, 33476696, 31341055, 30955825 |

Query lesson: split effector-by-effector (one query per ISG member) rather than one combined query — combined queries collapse to 1 hit; per-effector queries each return 6.

## PMID table (22 verified, DOI checked via esummary)

| PMID | Journal (Year) | Contribution |
|------|----------------|--------------|
| 41618367 | BMC Vet Res (2026) | PRRSV Nsp11 ↓ OAS1/RNase L mRNA (endoribonuclease, autophagy-dependent, Baf A1 rescues) |
| 36921497 | Vet Microbiol (2023) | PRRSV Nsp11 ↓ ISG15 transcription + ISGylation; Nsp2 OTU/PLP2 also inhibits ISGylation |
| 31043527 | J Virol (2019) | PRRSV Nsp1β binds Nup62 → NPC disintegration → blocks mRNA export → ↓PKR/OAS/Mx1/ISG15/IFIT1/2/IRF3; L126A mutant attenuated |
| 39645133 | Int J Biol Macromol (2025) | Recombinant porcine ISG15-IFN-λ3: ↑ISG15/ISG56/HERC5, ↓PRRSV viremia + lung pathology in piglets |
| 41291300 | Cell Mol Life Sci (2025) | ASFV L11L binds IRF3 (S396/S398) blocks TBK1 phos; inhibits PKR dimerization (K196) |
| 36377947 | Microbiol Spectr (2022) | ASFV MGF110-7L activates PKR → translation suppression + stress granules (pro-viral) |
| 41941904 | Int J Biol Macromol (2026) | Viperin-nsp8 (K82) disrupts RTC, conserved across α/β/γ/δ coronaviruses; ddhCTP inhibits PEDV |
| 31868081 | Autophagy (2020) | BST2 (IRF1-induced) → MARCHF8 ubiquitinates PEDV N → CALCOCO2/NDP52 → selective autophagy |
| 33476696 | Virus Res (2021) | CH25H/25HC blocks PDCoV entry (IPI-FX ileum cells); partly enzyme-independent |
| 30955825 | Vet Microbiol (2019) | 25HC therapy vs HP-PRRSV: ↓viremia, ↓lung load, ↑survival; ↑IL-1β/IL-8 in PAMs |
| 39454283 | Vet Microbiol (2024) | CH25H inhibits PCV3 |
| 38140647 | Viruses (2023) | CH25H suppresses SADS-CoV via spike/entry block |
| 31341055 | J Virol (2019) | PRRSV E protein degrades CH25H via UPR (evasion) |
| 30885302 | Vet Immunol Immunopathol (2019) | Porcine OAS1b cloning: conserved P-Loop/D-Box, RNase L-dependent, inhibits PRRSV |
| 26437676 | J Med Virol (2016) | pOAS1/2/L vs JEV: pOASL + pOAS1 most inhibitory; pOASL antiviral RNase L-independent |
| 42338383 | Transbound Emerg Dis (2026) | PoRVA NSP4 → NRBF2-mediated autophagic degradation of MDA5 → ↓IFN-I |
| 40406095 | Front Immunol (2025) | Baicalin ↑ antiviral protein expression + respiratory mucosal immunity |
| 40319282 | BMC Vet Res (2025) | L. plantarum LP1 (piglet gut) activates STING-IFN-I → anti-PoRV |
| 24931347 | Microbiol Immunol (2014) | BST2 inhibits PERV release |
| 24717029 | Acta Virol (2014) | Tetherin of various species inhibits PERV from human cells |
| 24448163 | J Microbiol Biotechnol (2014) | Comparison of retroviral restriction factors vs PERV |
| 37008366 | Front Vet Sci (2023) | ADE of PRRSV downregulates ISG15 |

## Virus evasion table (the "arms race" — key narrative for the card)

| Virus | Protein | Mechanism | PMID |
|-------|---------|-----------|------|
| PRRSV | Nsp11 | Endoribonuclease ↓ OAS1/RNase L mRNA AND ↓ ISG15 transcription; autophagy-lysosome degradation | 41618367, 36921497 |
| PRRSV | Nsp1β | Nup62 binding → NPC disintegration → blocks host mRNA export → shuts down all ISGs | 31043527 |
| PRRSV | Nsp2 | OTU/papain-like protease (PLP2) inhibits ISGylation | 36921497 |
| PRRSV | E | Degrades CH25H via UPR | 31341055 |
| ASFV | L11L | Blocks IRF3 phos (S396/S398) + PKR dimerization (K196) | 41291300 |
| ASFV | MGF110-7L | Activates PKR → host translation suppression + stress granules (hijack) | 36377947 |
| PoRVA | NSP4 | NRBF2-mediated autophagic degradation of MDA5 | 42338383 |

## Vietnamese terminology (card sections)

- ISG = Gene kích hoạt bởi interferon; "đội quân effector kháng virus"
- ISGylation = gắn đồng hóa trị ISG15 vào protein mới tổng hợp
- 2-5A system = hệ OAS/RNase L; chain terminator ddhCTP = "mồi chặn chuỗi"
- Evasion table = "cuộc chạy đua vũ trang" (arms race)
- BST2/PERV = nền tảng cấy ghép dị chủng (xenotransplantation) — góc y học người

## Feed additive / therapy modulation

| Agent | Effect | PMID |
|-------|--------|------|
| ISG15-IFN-λ3 fusion | ↓PRRSV viremia, milder lung pathology (piglets) | 39645133 |
| 25HC | ↓HP-PRRSV viremia, ↑survival | 30955825 |
| Baicalin | ↑ antiviral proteins, respiratory mucosal immunity | 40406095 |
| L. plantarum LP1 | STING-IFN-I → anti-PoRV | 40319282 |

## Crosstalk (connects existing KF cards)

Type I IFN (87), RIG-I/MDA5 (138), cGAS-STING (143), JAK-STAT (183), IFN-λ (73), PRRSV (157), ASF (214), PEDV (146), β-glucan trained immunity (182), polyphenols (108).

## Card creation recipe used

1. Gap-check: scan card titles with word-boundary regex for `ISG|Mx1|OAS|RNase L|PKR|ISG15|viperin|RSAD2|tetherin|BST2|CH25H|effector` → only Type I IFN card matched (mention-only, not dedicated) → gap confirmed
2. Wikipedia Action API: search → pageids (44939434 ISG, 14156559 ISG15, 14723952 MX1, 14166840 OAS1, 6846786 PKR, 34333508 Viperin, 15706431 Tetherin) → per-pageid curl loop with `sleep 1` (avoids exlimit cap)
3. PubMed: 9 per-effector queries → merge dedup → esummary for DOI check → efetch abstracts (per-PMID scoping regex)
4. POST Pattern D with `<!--OVERVIEW-->` JSON block at content start (cron requirement)
5. Verify: re-fetch `/api/cards`, match returned `id` AND confirm `<!--OVERVIEW-->` present in content
6. Update `knowledge-flow/data/research-rotation.json` `last_index` → next rotation index
