# Tế bào Paneth (Paneth Cells) ở heo — Condensed Research Roadmap

## Tổng quan

Tế bào Paneth là dòng biểu mô chuyên biệt ở đáy crypt ruột non, đảm nhiệm:
1. **Sản xuất AMPs**: lysozyme, β-defensin (pBD), sPLA2, REG3γ
2. **Duy trì ISC niche**: tiết Wnt3a, DLL4 (Notch ligand), EGF

Markers ở heo: lysozyme + Sox9 (IHC, cố định Carnoy — PMID 42015263)

## Phân bố đặc thù heo

- **Tập trung ở tá tràng** (duodenum) — khác với chuột phân bố đều
- 5–12 tế bào/crypt
- Không có α-defensin như người; heo dùng β-defensin (pBD) làm AMP chính

## Các PMID cốt lõi

| PMID | Focus | Journal (Year) |
|------|-------|----------------|
| **42015263** | Phân bố Paneth heo theo tuổi và nhiễm bệnh; tối ưu IHC | BMC Vet Res (2026) |
| **37582766** | REVIEW: Paneth ở gia súc (heo, bò, cừu, gà, thỏ) | J Anim Sci Biotechnol (2023) |
| **37688865** | Paneth bảo vệ ISC niche khỏi DON; mất PC → nặng thêm | Ecotoxicol Environ Saf (2023) |
| **31959773** | TGEV → Paneth (APN) → mất Notch → ức chế ISC → teo nhung mao | Cell Death Dis (2020) |
| **32880235** | PEDV ↓ lysozyme Paneth, ↓ tế bào M, ↑ viêm | Vet Pathol (2020) |
| **40749794** | Nur77 → ER homeostasis → Paneth necroptosis (sepsis) | J Adv Res (2026) |
| **37683828** | Nur77 → Dact1 → Wnt → biệt hóa Paneth | Mucosal Immunol (2024) |
| **36993974** | REVIEW: Paneth đa vai trò (NEC, gan, tụy, Crohn) | Front Immunol (2023) |
| **36632926** | Stress nhiệt ↓ Paneth, ISC, Goblet qua FAK | BBA Mol Cell Res (2023) |
| **41047495** | IPGCA: Single-cell atlas ruột heo (1M+ tế bào) | Adv Sci (2025) |
| **40135895** | PDCoV kích hoạt Wnt → ↑ ISC self-renewal | J Virol (2025) |
| **39012142** | AhR ligands từ LGG ↑ ILC3 → IL-22 → chống PEDV | J Virol (2024) |
| **34506767** | Lauric acid bảo vệ ISC khỏi DON (Akt/mTORC1) | Chem Biol Interact (2021) |
| **36535023** | Selenomethionine → Nrf2 → chống DON | J Agric Food Chem (2023) |
| **34216418** | L-Carnosine → Nrf2 → chống DON | Mol Nutr Food Res (2021) |
| **31650938** | EGF → Wnt/β-catenin → ↑ Paneth heo cai sữa | Animal (2020) |

## PubMed queries đã test (tháng 7/2026)

```python
queries_paneth = [
    'Paneth cells swine pig',                    # 10 results, good coverage
    'Paneth cell alpha-defensin pig gut',         # 0 results (pigs don't have α-defensin)
    'Paneth cells intestinal stem cell niche Wnt',# 5 results
    'Paneth cells piglet weaning diarrhea',       # 2 results
    'Paneth cells nutrition pig intestine',       # 10 results
    'Paneth cells single cell RNA seq pig porcine',# 1 result (IPGCA)
    'lysozyme Paneth cells pig porcine',          # 5 results
    'NOD2 Paneth cells swine pig',                # 0 results
]
# Best multi-angle: combine 'Paneth cells swine pig' + 
# 'Paneth cells intestinal stem cell niche Wnt' + 
# 'Paneth cells nutrition pig intestine'
```

## Cơ chế TGEV → teo nhung mao (hoàn chỉnh nhất)

1. TGEV → APN receptor → Paneth cell
2. Tổn thương ty thể → ROS
3. Mất Paneth → mất Notch (DLL4, Hes5)
4. Ức chế Lgr5+ ISC self-renewal và differentiation
5. Teo nhung mao 48h → tiêu chảy cấp

NSP10/NSP16 → bất hoạt Notch signaling.

## Điều hòa dinh dưỡng

| Yếu tố | ↑ Paneth | Cơ chế |
|--------|----------|--------|
| Kẽm (ZnO) | ↑ | Wnt/β-catenin |
| Butyrate | ↑ pBD-2 | HDACi |
| EGF (sữa đầu) | ↑ | Wnt/β-catenin |
| Selenomethionine | Bảo vệ | Nrf2 |
| Lauric acid (C12) | Bảo vệ ISC | Akt/mTORC1 |

## Liên kết pathway

Paneth ← Wnt/β-catenin, Notch, Nur77/Dact1, NOD2, TLR9
Paneth → AMPs, ISC niche, microbiota regulation
TGEV/PEDV → ↓ Paneth → ↓ ISC → teo nhung mao
DON/Heat stress → ↓ Paneth → tổn thương ruột

## Vietnamese keywords

Tế bào Paneth, tế bào biểu mô ruột, peptide kháng khuẩn nội sinh, lysozyme, β-defensin, tế bào gốc ruột, ngách ISC, crypt Lieberkühn, tá tràng, heo con cai sữa, TGEV, PEDV, DON, stress nhiệt, necroptosis, Nur77
