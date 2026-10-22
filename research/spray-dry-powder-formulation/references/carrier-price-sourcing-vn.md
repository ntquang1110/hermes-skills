# Sourcing GIÁ chất mang (đường / cyclodextrin / tinh bột biến tính · hydrocolloid / protein / polysaccharid) cho thị trường VN

Knowledge bank cho tác vụ "research giá + hiệu suất thu hồi cho chất mang sấy phun".
Dùng cùng `references/carrier-chemistry-alkaline-ph12.md` (phần hiệu suất/hoá lý).
Bảng giá neo tách theo nhóm: **nhóm T2** (đường/cyclodextrin/tinh bột) và **nhóm T1** (hydrocolloid/protein/polysaccharid) — xem hai mục riêng dưới.

## Nguyên tắc ghi giá (bất di bất dịch)
- Mỗi con số giá PHẢI có: nguồn (URL) + ngày lấy + quy cách/MOQ + **loại giá**.
- 5 loại giá phải phân biệt rõ, không trộn: **báo giá thật · giá niêm yết web · giá sàn B2B
  (Alibaba/1688/Made-in-China/IndiaMART) · giá lẻ phòng lab · ước lượng**.
- Không tìm được nguồn → để `null` + `note='chưa có nguồn'`. KHÔNG bịa giá.
- Ghi rõ **tỷ giá USD/VND đã dùng + ngày** (nguồn: trang tỷ giá Vietcombank — mua/bán, cập nhật
  trong ngày; XE làm mốc đối chiếu).
- Tách "giá thực phẩm" vs "giá hoá chất AR/phòng lab" — chênh 5–20× (vd sucrose thực phẩm
  20–26k đ/kg vs sucrose AR 240k đ/kg). Ghi cả hai, đừng lấy nhầm làm giá sản xuất.

## Kênh tra giá theo nhóm
| Nhóm | Kênh hiệu quả | Ghi chú |
|---|---|---|
| **Thực phẩm ở VN (lẻ & chiết lẻ)** | Shopee, Lazada, Bách Hoá Xanh, Kamereo (giá đường công nghiệp VN) | nhiều listing ghi giá ngay; trang sàn hay trả rỗng khi extract → **giá thường có sẵn trong `description` của kết quả `web_search`**, đọc từ đó |
| **Nhà phân phối nguyên liệu VN** | phugiathucphamdainam.com, hoachatvietmy.vn, qtchem.vn, expfoods.com.vn, 3hcosmetic.com | thường **KHÔNG niêm yết giá** (bao 25 kg, "báo giá qua liên hệ") → chỉ dùng để xác nhận có bán + quy cách/xuất xứ, phải ghi "chưa có nguồn giá" |
| **Hoá chất AR / phòng lab VN** | VietBioLab, hoachatthinghiem.org (Duchefa) | mốc lẻ đắt; KHÔNG dùng làm giá sản xuất |
| **Bulk quốc tế — hàng hoá (commodity)** | **Tridge** (giá *giao dịch thật* theo mã INS/E-number, tách theo nước + lô), Made-in-China, Alibaba, IndiaMART | Tridge là mốc tốt nhất cho tinh bột biến tính E1450 vì báo giá giao dịch thật theo lô, không phải giá rao |
| **Chỉ số giá (không phải báo giá)** | Procurement Resource, IMARC | chỉ dùng làm xu hướng; nhãn `ước lượng` |
| **Lẻ nhãn hiệu nước ngoài** | Sigma-Aldrich, Spectrum, MedChemExpress, MP Biomedicals, Amazon, modernist shops | mốc "trần" tham chiếu, không phải giá mua sản xuất |

## Chiến lược PROXY cho sản phẩm thương hiệu không có giá công khai
Hi-Cap 100, Capsul, Pure-Cote B790, HP-β-CD: **không** có giá niêm yết công khai.
→ Tra giá **hàng hoá generic cùng mã INS/E-number**:
- Tinh bột n-OSA → **E1450 / starch sodium octenyl succinate** (Tridge).
- β-CD → "beta cyclodextrin" (Made-in-China / IndiaMART).
Ghi rõ `do_tin_cay = "sàn B2B (proxy E1450/n-OSA)"` + note nói thẳng "không có giá nhãn hiệu,
đây là proxy". Đừng để proxy trông như giá thật của nhãn hiệu.

## Giá neo tham chiếu — nhóm T2 (đường / cyclodextrin / tinh bột biến tính) — lấy ngày 22/10/2026 (tỷ giá 25.700 VND/USD)
Chỉ dùng làm mốc; luôn lấy lại + ghi ngày khi dùng.

| Chất | Giá VN (đ/kg) | Giá bulk/lô (USD/kg) | Nguồn neo |
|---|---|---|---|
| trehalose | 155.000 (lẻ Shopee, hàng Nhật) | 1,80–3,00 (MOQ 2.000 kg) | Shopee; Made-in-China |
| maltodextrin DE10 | 64.000 (chiết lẻ VN) | 0,60–0,85; chỉ số ≈515–546 USD/MT | Shopee; Made-in-China; Procurement Resource |
| maltodextrin DE20 | ≈64.000 (không tách được giá riêng) | như DE10 | — |
| sucrose | 26.000 (giá đường CN VN; lẻ 31–37k; AR 240k) | — | Kamereo; Bách Hoá Xanh; VietBioLab |
| beta-cyclodextrin | 491.000 (lẻ Shopee 1 kg) | 2,30–4,00 (TQ); ₹555/kg (Ấn) | Shopee; Made-in-China; IndiaMART |
| HP-beta-cyclodextrin | *(không có ở VN)* | ≈48 (Ấn); niêm yết 238–413 (US) | IndiaMART; Spectrum; Sigma |
| n-OSA Hi-Cap 100 | *(không có giá nhãn hiệu)* | **2,26 (VN) · 2,45 (TQ) · 4,44 (Ấn) · 3,97 (US) · ~1,1 (TH)** | Tridge E1450 |
| n-OSA Capsul | *(không có giá nhãn hiệu)* | như trên (proxy E1450) | Tridge E1450 |
| n-OSA Pure-Cote B790 | *(không có)* | proxy E1450; lẻ US$5,99/gói, CA$38,28/kg | Tridge; Foods of Nations; Amazon.ca |
| PVP K30 | *(không niêm yết ở VN)* | 9–25 (sàn); ₹800/kg (Ấn) | Alibaba; IndiaMART |

## Hiệu suất thu hồi / EE — nguồn để neo
- Đừng lấy EE đo trong môi trường trung tính áp cho dịch kiềm pH 12–14 (nhóm n-OSA bị
  xà phòng hoá → retention đã công bố không transfer được). Ghi rõ cảnh báo này.
- Neo định lượng hữu ích: β-CD EE tới 79,4% (Hadian 2018, PMC5937076); MD+gum arabic EE
  83,67–89,98% và microencapsulation yield ~89% (Azarpazhooh 2026, RSC Food & Function);
  tinh bột biến tính yield 72,7–98,69% (Marquez-Gomez); Hi-Cap 100 retention d-limonene cao
  nhất nhóm so sánh (Soottitantawat 2005); citral giữ tương đương sucrose vs trehalose,
  trehalose ổn định vật lý hơn (Sosa 2011, doi 10.1111/j.1365-2621.2011.02721.x).
- Nhiều chất KHÔNG có số thu hồi riêng → để `null` + note `chưa có nguồn số riêng`, đừng bịa.

## Ghi chú pháp lý phải kèm khi báo giá chất mang
- **HP-β-CD** và **PVP (E1201)**: chủ yếu là tá dược dược phẩm / phạm vi phụ gia thực phẩm rất
  hẹp ở VN → gắn cờ "cân nhắc loại khỏi công thức thực phẩm", đừng chỉ báo giá.
- Thời gian tiếp xúc kiềm: với nhóm n-OSA (E1450) phải ghi rõ giới hạn tiếp xúc (khuyến nghị
  bơm định lượng trực tiếp vào đầu vòi phun, tránh trộn lâu với kiềm).

## Giá neo nhóm T1 — hydrocolloid / protein / polysaccharid (lấy 22/10/2026, tỷ giá 25.700 VND/USD)
12 chất mang cho dịch nạp pH 12–14. Giá VN là lẻ niêm yết web trừ khi ghi khác; bulk/lô là sàn B2B.

| Chất (id) | Giá VN (đ/kg) | Bulk/lô (USD/kg) | Nguồn neo |
|---|---|---|---|
| gum_arabic | 370.000 (túi 1 kg Shopee; bulk Pháp 25 kg = "liên hệ") | 0,37–4,85 (Made-in-China); ₹105/kg (Ấn) | Shopee; Made-in-China; IndiaMART; Tridge |
| hpmc | 290.000 (160k/500 g, shop mỹ phẩm) | 1,20–3,70 (theo tấn, **grade xây dựng**); food/pharma 14–18 | Nguyên liệu làm mỹ phẩm HCM; ECHEMI; Alibaba |
| mcc | 360.000–480.000 (quy đổi gói 250–500 g) | 6,66–11,45 (Tridge) | Shopee; Tridge |
| cmc | 155.000 (thấp nhất) – 320.000 | 1,15–4,60 | Websosanh; Ovovita; Alibaba; IndiaMART |
| pectin | 320.000 (Genu HLM Đức 1 kg) – 1.372.000 (gói 50 g) | 7,50–35 (Alibaba); FOB 8,88 (Made-in-China) | Lazada; Shopee; Alibaba |
| gelatin | 242.000 (bao 25 kg Đức, ≥2 bao) – 379.000 (lẻ 1 kg) | 3,10–7,50 | Abby; Shopee; Alibaba; Made-in-China |
| **wpi** | **null — chưa có nguồn** | 18,50–34 (FDCM EU €31,27/kg; Alibaba 25–30) | FDCM; Alibaba |
| **sodium_caseinate** | **null — chưa có nguồn** | 7,00–8,00 (Made-in-China); 7,90 (ChemAnalyst Pháp Q2/2026) | Made-in-China; ChemAnalyst; Tridge |
| **pullulan** | **null — chưa có nguồn** | 13–46 (bulk); lẻ lab 410–14.700 | Made-in-China; Chem-Impex; Thermo |
| sodium_alginate | 1.600.000 (lẻ lab 500 g) – 3.471.000 (Louis François 1 kg) | 2,22–28 | Hoá chất thí nghiệm; Classic Deli; Alibaba |
| inulin | 180.000–355.000 (túi 1 kg) | 3,00–12,00 | Shopee; Made-in-China; Alibaba; IndiaMART |
| skim_milk_powder | 419.000 (lẻ 1 kg "nguyên liệu sỉ") | 3,55–3,98 (GDT đấu giá) | Shopee; Global Dairy Trade; Cheese Reporter |

Ba chất **không có giá VN công bố**: `wpi`, `sodium_caseinate`, `pullulan`. NCC VN (NewViet,
Foodchem VN, ALCHEMIST/BioHydro) chỉ ghi "liên hệ". VN bán **whey protein thể thao thành phẩm**,
KHÔNG bán WPI90 nguyên liệu → đừng lấy giá supplement retail thay thế.

## Hiệu suất thu hồi / EE — neo cho nhóm T1
- **Barra 2019** (PubMed 31394884 / Molecules 24:2872, sấy phun L-ascorbic acid): product yield
  **35,1–83,2%** cho cả gum arabic và sodium alginate; EE **>82%** (GA), **>90%** (ALG).
- **Puttarat 2021** (PMC7914317, WPI + nano-crystalline starch): powder yield WPI đơn **83,58%**.
- **Moumnassi 2022** (IJFS doi 10.1111/ijfs.15949, sodium caseinate): EE **74,7–82,9%**; retention
  80,51% (50 °C) / 82,49% (25 °C) / 90,68% (4 °C).
- **Lisiecka 2023** (Foods 12:3363, inulin & pectin): recovery efficiency **>50%**; pectin 4–8% gây
  nứt/vón hạt. **Etzbach 2020**: inulin có độ hoà tan nước lạnh thấp nhất (82,7%) trong nhóm thử.
- **Neves 2019**: bao vi nang curcumin trong SMP cải thiện độ ổn định (không có số yield riêng).
- **Zaidul 2020** (PMC7452702): HPMC 5 cP / 15 cP bao dầu cá — có nghiên cứu, chưa trích được %.
- Không có số riêng → `null`. Riêng **MCC** ghi thẳng **"không áp dụng (trộn khô sau sấy)"** — đừng để
  null trống trơn khiến người đọc tưởng chưa tra.

## Bẫy giá B2B gặp ở nhóm T1 (áp dụng chung cho mọi nhóm)
- **Giá MOQ 1 kg trên Alibaba là "lẻ ảo"**, không phải bulk: sodium caseinate US$13,50–20/kg (MOQ 1 kg)
  vs US$7–8/kg (MOQ 1.000 kg) — sai 2×, đủ làm hỏng bảng giá vốn. Luôn ghi MOQ cạnh giá.
- **Made-in-China có listing ghi đơn vị mơ hồ** (WPI "US$6.000–7.000", không rõ /kg hay /tấn) → ghi lại,
  gắn cờ "đơn vị không rõ ràng", KHÔNG cho nó làm mốc.
- **Giá rẻ thường là SAI GRADE**: HPMC và sodium alginate giá sàn TQ phần lớn là grade xây dựng/công
  nghiệp; grade thực phẩm E464 / E401 đắt hơn nhiều lần.

## Giá neo nhóm T3 — chất độn / chống vón / khoáng / muối kiềm (22/10/2026, tỷ giá 25.700 VND/USD)
18 chất cho dịch nạp pH 12–14. KHÁC T1/T2: **đây KHÔNG phải chất mang vi năng** ⇒ `ee_pct = null` cho cả nhóm,
và phải ghi LÝ DO (đừng để ô trống trơn) — xem bẫy 6 trong `price-dataset-consumer-contract.md` (dict
`{"gia_tri_dai_dien": None, "dieu_kien": "…không phải chất mang vi năng…"}`).

| id | Giá VN (đ/kg) | Grade / quy cách ghi kèm |
|---|---|---|
| calcium_carbonate | 1.500–3.000 | CN GCC/PCC; có E170 & feed grade — 3 mức giá khác nhau |
| calcium_silicate | ∅ (QT 3,08 USD/kg TQ) | E552; IndiaMART chênh ₹5,2 vs ₹165–275/kg ⇒ hỏi rõ grade |
| trona | **∅ chưa có nguồn** | quặng, không có grade TP; dùng proxy soda ash |
| natron | ∅ (QT 0,17 USD/kg · 10H2O) | E500; ghi rõ dạng ngậm nước (không thì sai hàm lượng Na) |
| aerosil_200 | ∅ VN ("liên hệ"); lẻ lab €121–132/kg; bulk CN 2,8–3,5 USD/kg | 200 F / 200 Pharma; **chênh lẻ-lab vs bulk ~40×** |
| bentonite | 1.700–3.500 | CN (khoan/phụ gia); Na-bentonite trương nở → tăng nhớt dịch nạp |
| kaolin | **∅ chưa có nguồn** | CN gốm/giấy; E559 có điều kiện |
| zeolite_clinoptilolite | 1.200–2.600 | CN/nông nghiệp; ghi % clinoptilolit (khác nhau mạnh theo mỏ) |
| sodium_silicate | 8.500–11.800 | CN; ghi module SiO₂:Na₂O + dạng bột/lỏng |
| C03-muoi-NaOH | 17.000–34.000 (sỉ Lazada 17k) | CN 99% / E524; ăn mòn buồng sấy |
| C04-muoi-KOH | ∅ VN; QT 1,12 USD/kg (SE Asia 9/2026) | CN 90% / E525 ≥95% |
| C05-muoi-Na2CO3 | ∅ VN; QT 0,21 USD/kg FOB | CN 99/99,2; **E500(i) food grade 99,5 phải đặt** |
| C06-muoi-NaHCO3 | 16.800–18.800 (feed TQ 420–470k/bao 25 kg) | feed/food E500(ii)/dược; **phân hủy >50 °C** |
| C07-muoi-K2CO3 | ∅ VN; QT 1,04 USD/kg | phân bón K₂O 68% / CN 99,5 / E501(i) |
| C08-muoi-Na3PO4 | **∅ chưa có nguồn** | CN 98% / E339(iii); ghi khan vs ·12H₂O |
| C10-muoi-Na2SiO3 | 11.800 | CN, pH dung dịch 12,6–12,8 (dự trữ pH tốt nhất nhóm) |
| C11-muoi-CaOH2-CaO | 15.000–20.000 (375–500k/bao 25 kg) | vôi CN / E526 / nông nghiệp |
| C12-muoi-MgO-MgOH2 | 15.000–18.800 (375k/bao 25 kg) | phân bón 65–85% / CN 90% / E530 |

Ba chất **không có nguồn giá nào** (VN lẫn bulk): `trona`, `kaolin`, `C08-muoi-Na3PO4`.
Sáu chất **chỉ có giá quốc tế proxy, không có giá VN niêm yết**: `calcium_silicate`, `natron`,
`aerosil_200`, `C04-KOH`, `C05-Na2CO3`, `C07-K2CO3` ⇒ consumer tự đặt `co_so = "quy đổi từ giá bulk quốc tế"`.

### Hiệu suất thu hồi cho nhóm T3 (không có EE ⇒ neo vào THU HỒI BỘT)
Không tồn tại tài liệu EE cho chất không-bao-vi-năng. Neo hợp lệ (dùng chung, CÓ dẫn nguồn, ghi nhãn ước lượng):
- cyclone ~90 %+ bột, thêm túi lọc ≈99,9 % thu hồi gộp — dairyconsultant.co.uk/spray-dryer-fines-causes-recovery-control.php
- bột MVD < 5 µm: thất thoát cyclone > 30 % — advancedcyclonesystems.com (Hurricane cyclones PDF)
- yield ướt sấy phun polymer khả dụng > 80 % (bột bám thành) — Sundararajan 2023, PMC10459734
⇒ `thu_hoi_pct` là **ước lượng từ nguồn chung**; ghi thẳng trong `thu_hoi_pct.do_tin_cay`
"ước lượng kỹ thuật, CHƯA có số đo riêng cho chất này ở pH 12–14". Chất không đủ cơ sở → `null`.
Vì sao muối kiềm thu hồi kém hơn chất độn khoáng: NaOH/KOH/K₂CO₃ **chảy nước (deliquescent)** → bám thành
buồng sấy; chất độn không tan, hạt thô (CaCO₃, bentonite, kaolin, zeolite) thu hồi tốt nhất.

## Khi nhiều agent viết song song cùng một họ file
Các sub-agent viết `price_T1/T2/T3.json` song song → mỗi file một schema, và `price_stub.json` được dẫn
là canonical có thể KHÔNG có trên đĩa. **Đừng đoán union alias** — dừng lại và **đọc consumer**: module gộp
họ file đó (ở dự án này là `price_lib.py`) định nghĩa tập key nhận vào qua các tuple `ALIAS_*`; đó chính là
schema có thẩm quyền. Hợp đồng đầy đủ + 6 bẫy parser (đã gây lỗi giá 1000×) + recipe verify:
`references/price-dataset-consumer-contract.md`.
Nếu buộc phải ghi trước khi consumer xuất hiện: giữ key lõi theo stub được dẫn + thêm tên key anh em làm
**alias** (`gia_vn_dkg`, `price_vn_dkg`, `min`/`max`, `quy_cach_dong_bao`, `MOQ`, `nha_cung_cap_vn`) và khai
trong `meta.schema`; rồi **báo parent có thể cần re-map một lần**. Consumer có thể được tạo TRONG lúc bạn
đang chạy — đọc lại lần cuối trước khi ghi.
