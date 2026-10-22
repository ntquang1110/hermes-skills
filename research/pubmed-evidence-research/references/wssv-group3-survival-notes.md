# WSSV Group 3 — survival/transmission/epidemiology verified notes (2026-08-16)

Deliverable written: `D:/Hermes Proj/wssv-research/data/group3_survival.json` (8 topics, 52 facts, 29 verified PMIDs, Vietnamese). Reuse for later WSSV groups (host immunity, disinfection products, Kiem Saphia context).

## Verified PMID bank (all esearch+efetch verified this session)

**Lịch sử dịch / history**
- 19216439 — Leu 2009 Whispovirus review: first appearance 1992–1993 Asia → global spread; WSSV = sole Nimaviridae, ~300 kbp dsDNA.
- 22434000 — Lightner 2012: WSD emerged East Asia ~1992, most of Asian industry by 1994, eastern USA 1995 via frozen commodity, Americas Pacific 1999.
- 32272137 — Millard 2021: global losses >$3 bn/yr, industry $19 bn/yr; pond temperature + salinity are main outbreak drivers.
- 26797629 — Verbruggen 2016: billion-dollar losses since 1990s; wide host range = translocation risk.
- 39576200 — Puttirungroj 2024: Japan isolates 288–299 kbp, ~99% identity with NC_003225.3; ongoing evolution.

**Sống sót môi trường / environment**
- 36282009 — Islam 2023 review (open access): soil DNA up to 10 months; sediment survivability = key variable for new ponds; 100 ppm NaOCl/10 min inactivates WSSV; ponds rinsed with 100 ppm bleaching powder re-positive at 20 days post-disinfection; formalin 70 ppm blocks transmission; total death within 3–10 days of outbreak; clay adsorption protects virus.
- 35623490 — Kim 2022: iron flocculation concentrates infective WSSV from farm seawater (~10² copies/mL).
- 15276606 — Jiravanichpaisal 2004: crayfish carry WSSV at 4–12 °C (0% mortality), 100% mortality on transfer to 22 °C.

**Nhiệt độ / đông lạnh**
- 11463105 — Soto 2001: viruses remain infectious in frozen shrimp tissue; ingestion mortality 0.40–0.75.
- 16956056 — Hasson 2006: 2/20 boxes imported frozen bait shrimp WSSV+; homogenate injection → 100% mortality in 48–72 h; oral exposure did not infect PLs (freeze-thaw/dose).
- 9329114 — Lightner 1997: WSSV/YHV infectious in frozen shrimp imported into US; gulls/seabirds/aquatic insects spread factors.
- 23186704 — Bateman 2012: lobsters fed high-dose frozen supermarket shrimp died of WSD; low dose → latent infection.
- 39166794 — Xiao 2024: 32 °C inhibits WSSV replication via HSP70-Toll4-Dorsal-AMP.
- 16948707 — Balasubramanian 2006: inactivation by physical+chemical treatments — **citation-only, NO abstract on PubMed**.

**Host range / vectors**
- 14735935 — Hameed 2003: 16/20 Indian marine crab species susceptible; 4 refractory = potential reservoirs.
- 16905144 — Syed Musthaq 2006: lobsters 100% mortality via injection (120–168 h), not via oral route.
- 24953350 — Sánchez-Paz 2015: Palaemon ritteri novel host, VP28 transcription = replication.
- 24895865 — Mendoza-Cano 2014: copepod Calanus pacificus californicus susceptible → potential vector.
- 20024621 — Zhang 2010: Artemia (4 stages) infected; PLs fed WSSV+ Artemia PCR-positive.
- 38004813 — Chauhan 2023: WSSV genome (273,795 bp, 99.94% identity) from pooled chicken cloacal swabs — bird mechanical spread.
- 37533749 — EFSA 2023: vector/reservoir species; WSSV/TSV/YHV 90–100% likely infective under ANY transport condition.

**Lây ngang / horizontal**
- 37766231 — Cox 2023: death within 78 h; shedding within 6 h of onset, peak 12 h post-death; water exposure risk 1.0 vs feces 0.2 vs molts 0.0; cannibalism NOT significantly worse than water immersion.
- 37238106 — Kim 2023: waterborne MID 10¹ copies/mL → infection in 7 d; 10³ → 3 d; 10⁵ → 1 d; shedding threshold 3.1×10³ copies/mg, mortality threshold 8.5×10⁴ copies/mg.
- 11775794 — Wu 2001: collective rearing 75.6% vs isolated 1.2% mortality; immediate dead-shrimp removal cut mortality 64% → 4%.
- 11463105 — tissue ingestion transmission (see above).

**Lây dọc / vertical**
- 38182102 — Vijayan 2024: 58% wild P. indicus brooders WSSV+; 61% spermatophore / 54% immature / 48% ripe ovaries; TEM shows particles in ovary + spermatophore; FIRST molecular+histological trans-ovarian evidence (vertical previously debated).
- 18062468 — de la Peña 2007: wild P. monodon subclinical carriers (no white spots), dry-season prevalence higher; broodstock → hatchery vertical risk.

**Carrier / sống sót sau dịch**
- 21624105 — Oidtmann & Stentiford 2011: load at mortality onset 10⁹–10¹⁰ copies/g; survivors/wild crustaceans lower by multiple logs.
- 40914555 — Aguila-Toral 2026: Scylla serrata resistance = viral clearance (96–144 h) or replication inhibition (48–72 h).
- 23186704, 18062468, 14735935 — latent/subclinical/reservoir (see above).

## Working query patterns
- Author-field search is the fastest triage for classics: `Chang PS[Author] AND white spot syndrome`, `Lo CF[Author] AND white spot`. **Empty result ≠ author has no paper — often the paper is simply not indexed** (Lo 1996, Chang 1998, Satheeshkumar 2012 all absent from PubMed).
- `white spot syndrome virus chlorine disinfection` → 0 hits; `... chlorine disinfection inactivation` or `... inactivation temperature` works.
- PMC OA full text (BioC XML) + regex grep is the reliable way to get exact numbers when abstracts truncate: endpoint `https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC10029913/unicode`, grep `inactiv|chlorine|°C|freez|surviv|sediment|ppm`.

## Honest-gap notes (recorded in deliverable, do not fill in later)
- Lo 1996 / Chang 1998 / Satheeshkumar 2012: NOT on PubMed → no PMID assigned; history covered via 19216439 + 22434000.
- No verified "50–60 °C / X min" heat-inactivation numbers in any PubMed abstract → stated as unverifiable instead of invented.
- ">90 susceptible crustacean species" = OIE (WOAH) manual claim → `pmid: ""` with document reference, never borrow a PMID.
