# ADE (Antibody-Dependent Enhancement) ở heo — Roadmap PRRSV

Research xong 2026-08-03, card KF: `c48ba9bd-419a-4d09-9443-1ed1793a07cf` (topic_slug `chan-nuoi-heo`).
**Đừng làm lại topic này.** Nếu cần nghiên cứu tiếp, mở rộng sang: M cells (microfold cells) của Peyer's patches, Kupffer cells/liver immunity, NFAT/calcium signaling trong T cells, bacteriophage therapy cho ETEC, feed enzymes (phytase), nucleotides trong dinh dưỡng heo.

## Tóm tắt

ADE = kháng thể dưới mức trung hòa (sub-neutralizing) gắn virus tạo phức hợp miễn dịch (IC), IC gắn FcγR trên đại thực bào phế nang heo (PAM) → tăng entry + ức chế IFN → viremia cao, tồn tại dai dẳng. Hai lớp cơ chế:

- **Extrinsic:** IC → FcγRI (CD64) / FcγRIII (CD16) → nội hóa cần CD163 (domain SRCR5) + Sn/CD169 (domain Sn1-6). CD16 là FcγR nhiều nhất trên PAM; ADE dịch chuyển tropism virus sang tế bào CD16+.
- **Intrinsic (immune silencing):** FcγRI hoạt hóa → FGR kinase ↑ → ức chế RIG-I/MDA5 → TBK-1/IRF-3/STAT-1/STAT-2 ↓ → IFN-α/β/γ/λ ↓, ISG15/ISG56/OAS1/OAS2/Mx1/RSAD2 ↓, TNF-α ↓, IL-10 ↑, TGF-β1 ↑.

## Tested PubMed queries (đều chạy được, 2026-08-03)

| Query | Kết quả |
|---|---|
| `PRRSV antibody dependent enhancement Fc receptor macrophage` | 8 PMIDs — query chính, ra đủ 2015–2026 |
| `Yoon antibody-dependent enhancement PRRSV 1996` | 8733920 (classic in vivo) |
| `Tirado Yoon antibody dependent enhancement virus infection review 2003` | 12725690 (review tổng) |
| `dengue antibody dependent enhancement Fc gamma receptor mechanism` | ra 2024–2026 papers (39480886, 42519317...) |
| `Arvin perspective potential antibody-dependent enhancement SARS-CoV-2 2020` | 32659783 (Nature 2020) |
| `Halstead O'Rourke dengue enhancement mononuclear phagocytes` | 195000 (Part II), 406347 (Part I — foundational), 6157332 |
| `Katzelnick dengue antibody dependent enhancement Science 2017` | 29097492 (cohort người) |
| `ASFV antibody dependent enhancement` | ⚠️ KHÔNG ra paper ADE — ra paper ức chế innate immunity chung. Đừng claim ASFV ADE khi chưa đọc paper dedicated |
| `porcine Fc gamma receptor opsonization phagocytosis review` | 0 results — FcR review ở heo rất thưa, đừng mất thời gian |

## PMID bank (16, tất cả verified qua esearch + esummary + abstract)

| PMID | Nguồn | Đóng góp |
|------|-------|----------|
| 406347 | Halstead & O'Rourke, J Exp Med 1977, DOI 10.1084/jem.146.1.201 | Nền tảng ADE: kháng thể không trung hòa tăng nhiễm dengue trong mono/phagocyte |
| 195000 | Halstead & O'Rourke, J Exp Med 1977, DOI 10.1084/jem.146.1.218 | Part II: danh tính bạch cầu máu/mô hỗ trợ nhiễm in vitro |
| 8733920 | Yoon et al., Viral Immunol 1996, DOI 10.1089/vim.1996.9.51 | ADE PRRSV in vivo trên heo: kháng thể sub-neutralizing tăng viremia |
| 12725690 | Tirado & Yoon, Viral Immunol 2003, DOI 10.1089/088282403763635465 | Review ADE virus gây bệnh: cơ chế + ý nghĩa vaccine |
| 25752917 | Gu et al., J Gen Virol 2015, DOI 10.1099/vir.0.000118 | CD16 nhiều nhất trên PAM; trung gian nội hóa IC; cần FcRγ chain; dịch chuyển tropism |
| 29761267 | Shi et al., Virol Sin 2018, DOI 10.1007/s12250-018-0032-3 | FcεRI tham gia ADE PRRSV; tăng AKT/ERK hướng chống viêm |
| 30273630 | Shi et al., Dev Comp Immunol 2019, DOI 10.1016/j.dci.2018.09.019 | 6 isoform FcγRI do alternative splicing (4 mới); màng pCD64-T1 thúc ADE; hòa tan pCD64-T3 gây viêm không ADE |
| 32046249 | Zhang et al., Viruses 2020, DOI 10.3390/v12020187 | ADE giảm IFN-α/TNF-α, tăng IL-10 qua FcγRI/III |
| 36136686 | Zhang et al., Vet Sci 2022, DOI 10.3390/vetsci9090470 | FcγRI + FcγRIII + CD163 (SRCR5) + Sn (Sn1-6) cùng cần cho ADE entry |
| 37008366 | Zhang et al., Front Vet Sci 2023, DOI 10.3389/fvets.2023.1150430 | ADE giảm IFN-γ/λ1/3/4, tăng TGF-β1 |
| 29097492 | Katzelnick et al., Science 2017, DOI 10.1126/science.aan6836 | Cohort Nicaragua: sốc dengue cao nhất ở dải titer hẹp; titer cao bảo vệ. "Correlate of enhancement" ≠ "correlate of protection" |
| 32659783 | Arvin et al., Nature 2020, DOI 10.1038/s41586-020-2538-8 | SARS-CoV-2: chưa có bằng chứng lâm sàng ADE; in vitro/animal models không dự đoán được rủi ro |
| 39480886 | PLoS Pathogens 2024, DOI 10.1371/journal.ppat.1012111 | Dengue tăng cường qua B cell receptor (BCR); B cells là reservoir lớn nhất |
| 41012704 | Zhang et al., Viruses 2025, DOI 10.3390/v17091277 | ADE chặn RIG-I/MDA5 qua FcγRI → giảm IFN-α/β |
| 41633078 | Xu et al., Vet Microbiol 2026, DOI 10.1016/j.vetmic.2026.110913 | FcγRI → FGR ↑ → ức chế RIG-I/TBK-1/IRF-3/STAT-1/2 → giảm IFN-α, ISG15/ISG56/OAS1/2/Mx1/RSAD2. Knockdown FcγRI/FCER1G/FGR giải phóng ức chế |
| 42519317 | Front Immunol 2025, DOI 10.3389/fimmu.2025.1577732 | Mô hình FcγR-ACE2 hợp tác ở coronavirus; FIPV ADE cổ điển; mức ADE SARS-CoV-2 do khả năng chặn spike-ACE2 quyết định |

## Sơ đồ cơ chế (dùng trong card)

```
PRRSV + IgG sub-neutralizing
  → Phức hợp miễn dịch (IC)
  → Gắn FcγRI (CD64)/FcγRIII (CD16) trên PAM (FcRγ chain/FCER1G truyền tín hiệu)
  → Nội hóa IC cần CD163 (SRCR5) + Sn/CD169 (Sn1-6)
  → Virus nhân lên mạnh
  → FcγRI hoạt hóa → FGR ↑ → ức chế RIG-I/MDA5 → TBK-1/IRF-3/STAT-1/2 ↓
  → IFN-α/β/γ/λ ↓, ISG15/ISG56/OAS1/OAS2/Mx1/RSAD2 ↓, TNF-α ↓
  → IL-10 ↑, TGF-β1 ↑ → im lặng miễn dịch → viremia cao, tồn tại dai dẳng
```

## Hàm ý vaccine PRRSV (đã viết trong card)

1. MLV tạo kháng thể; khi titer rơi xuống dải sub-neutralizing trước khi gặp virus thực địa → cửa sổ ADE.
2. Kháng thể mẹ suy giảm ở heo con = cửa sổ nguy cơ ADE kinh điển.
3. Chủng dị loại (ORF5 khác) không trung hòa chéo → dễ rơi vào sub-neutralizing.
4. Vaccine thế hệ mới: kháng thể trung hòa mạnh + IFN-γ, tránh kháng thể "chết". Mục tiêu mới: FcγRI/FGR (41633078), splice FcγRI (30273630).
5. Khoảng trống: chưa có cohort in vivo heo xác định dải titer ADE như Katzelnick 2017 ở người.

## Vietnamese terms

ADE = tăng cường nhiễm phụ thuộc kháng thể; kháng thể dưới mức trung hòa = sub-neutralizing antibody; phức hợp miễn dịch = immune complex (IC); đại thực bào phế nang heo = porcine alveolar macrophages (PAM); im lặng miễn dịch = immune silencing.

## Pitfalls gặp khi research

- **Keyword `ADE` trong dedup scan** false-match card "cAMP/PKA/CREB" (title chứa "adenylate cyclase" — substring `ade` nằm trong "adenylate"). Dùng keyword ≥5 ký tự hoặc scan context.
- **ASFV ADE search** trả về paper ức chế innate immunity chung, không phải ADE — không claim ASFV ADE nếu chưa có paper dedicated.
- **Halstead 1977 có 2 phần:** Part I = 406347 (infection enhancement — dùng cái này), Part II = 195000. Đừng tráo.
- efetch 5-PMID/batch chạy ổn; giữ `sleep 2` giữa các esearch group để tránh RemoteDisconnected.
