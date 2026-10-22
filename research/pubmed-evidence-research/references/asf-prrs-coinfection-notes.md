# ASF + PRRS đồng nhiễm — verified PMID bank (01/09/2026)

Ca: đàn lợn phơi nhiễm ASF (chủng chưa rõ) lần 1 âm tính, sau đó bị đàn mới lây thêm tai xanh (chủng Bắc Mỹ HP-PRRS) + ASF → dương tính cả hai. Câu hỏi: phân tích hệ miễn dịch + khả năng sống sót.

## Verified PMIDs (đã efetch abstract, verify đúng species=heo)

- **41478517** — Balakrishna et al., Infect Genet Evol 2026, DOI 10.1016/j.meegid.2025.105872. Đồng nhiễm tự nhiên ASF+PRRS: lợn lai chết cao, giống bản địa Zovawk có dung nạp; ASFV **chuyển tropism sang phổi**; genotype II ASFV + lineage 8 PRRSV-2. → nguồn chính cho bệnh nặng hơn khi đồng nhiễm.
- **40143222** — Xu et al., Viruses 2025, DOI 10.3390/v17030290. HP-PRRSV giai đoạn sớm giảm CD4+/CD8+ T, CD19+ B ở tonsil; PKR-mediated necroptosis tế bào miễn dịch. → nguồn ức chế miễn dịch HP-PRRS.
- **39097704** — Fabros & Charerntantanakul, BMC Vet Res 2024, DOI 10.1186/s12917-023-03760-8. PRRSV ức chế type I IFN/đồng kích thích (CD80/CD86) qua tăng TGF-beta; knock-down TGF-beta phục hồi IFN-beta, IRF3/7, giảm RNA PRRSV. → cơ chế "tai xanh mở cửa cho virus khác".
- **42383926** — Gata-de-Benito et al., J Virol 2026, DOI 10.1128/jvi.00636-26. ASFV MGF110-2L gây rối loạn IFN/cytokine storm; deleting gene → attenuation + bảo hộ đồng chủng. → ASF tự phá miễn dịch.
- **41400713** — Choudhury et al., Trop Anim Health Prod 2025, DOI 10.1007/s11250-025-04786-w. Dịch tễ Assam 2021-2023: ASF+PRRS nguy cơ cao hơn mùa hè/thu (OR~1.2), lợn già dễ PRRS (OR 1.72).

## Query terms hoạt động (PubMed esearch)
- `("African swine fever" AND "porcine reproductive and respiratory syndrome") AND (co-infection OR coinfection)`
- `(HP-PRRSV OR "highly pathogenic" AND "porcine reproductive and respiratory syndrome") AND (immunosuppression OR "type I interferon" OR "alveolar macrophage")`
- `("African swine fever") AND (immune evasion OR "cross-protection" OR neutralizing)`
- `("African swine fever") AND (macrophage OR monocyte) AND (target OR replication)`

## Kết luận phân tích (đã chốt)
Cả ASFV và PRRSV cùng đánh vào đại thực bào phế nang (CD163+) → đồng nhiễm phá tầng bẩm sinh. HP-PRRS ức chế IFN-I, giảm T/B cell, necroptosis (40143222, 39097704) → mở cửa cho ASF nhân lên không kiểm soát. ASF tự gây rối loạn IFN (42383926). Đồng nhiễm → ASF chuyển tropism phổi, đa cơ quan, tử vong cao (41478517). "Âm tính lần 1" không bảo hộ: ASF kháng thể không trung hòa tốt, bảo hộ chéo genotype kém. Khả năng sống đàn đồng nhiễm (ASF độc lực cao + HP-PRRS) ≈ 0; xử lý: tiêu hủy + phân loại + genotyping B646L/p72 + cách ly.

## Honest gaps
- Chưa verify PMID riêng cho "ASF kháng thể không trung hòa / bảo hộ chéo genotype kém" — claim này là kiến thức nền vững nhưng chưa gắn PMID cụ thể trong session này. Nếu deliverable yêu cầu, phải esearch + efetch thêm, không tự chêm số.
- Không có số phần trăm tử vong chính thức từ 1 paper duy nhất cho đồng nhiễm HP-PRRS+ASF — dùng "tiếp cận 90-100%" là ước lượng tổng hợp từ ASF đơn độc lực cao + tác động cộng hưởng, ghi rõ là ước lượng.
