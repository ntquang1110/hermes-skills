# Nợ 02 — Hàm lượng tannin THẬT + bảng giá NCC → giá vốn VND

Deliverable 21/10/2026: `docs/14-cong-thuc-co-ban/no-02-gia-von.md` + `.json`
(anh em của `no-01-bacillus-iga-bang-chung-cua-c.md`). Task: quy đổi cột "giá bậc 1–5" của
`livestock-formula-optimization` sang **giá VND thật**, và trả lời dải tannin 65–75% có đúng không.

---

## 1. Hàm lượng tannin hạt dẻ thật — dải 65–75% chỉ ĐÚNG MỘT PHẦN

Dải thực tế: **40% → 55% → 73±2% → 75%**. Polyphenol tổng đo bằng Folin–Ciocalteu chỉ **~36%**.

| Nguồn / sản phẩm | Số công bố | Loại số | URL |
|---|---|---|---|
| Silvateam/Perdomini (Ý) — Tannisol PB | **Tannin 75%**; polyphenol tổng ≥96%; DM 99% | spec nhà SX | business.sklfertilizers.com/en/product/tannisol-pb-chestnut-tannin/ |
| Tanin Sevnica d.d. (Slovenia) — Farmatan®/Farmatan Plus® | **73 ± 2% chestnut extract** (spec nhà SX); tài liệu trích **55%** (2 nghiên cứu) và **75%** (4 nghiên cứu) | spec + tổng quan | pmc.ncbi.nlm.nih.gov/articles/PMC11678802/ |
| Farmatan® đo lại 2024 | polyphenol tổng **36,14 g GAE/100 g DM**; condensed tannin 1,34; 11 hợp chất HT = 36,3% chế phẩm | số đo thực nghiệm | PMC11678802 |
| Tanin Sevnica — **Tanimil SCC®** (cùng nhà SX) | **40% tannin** | tài liệu thứ cấp | PMC11678802 |
| Farmatan® (Perić et al. 2022, Agriculture) | "contains about **75% tannins**, mostly ellagitannins" | bình duyệt | mdpi.com/2077-0472/12/11/1772 |
| Bột chuẩn hoá 75% titer (Ý, bao 25 kg) | **75% tannin titer**; 244 EUR/bao 25 kg = **9,76 EUR/kg** | bình duyệt 2024 | sciencedirect.com/science/article/pii/S2369969824000367 |
| Patent EP2904910A1 | "**75% by weight of tannins**" | sáng chế | (dẫn qua PMC11678802) |

**Ba điểm phải nói khi chốt mua:**
1. "75%" trong ngành = **tannin titer của bột chiết chuẩn hoá**, KHÔNG phải độ tinh khiết hoá học.
2. Spec nhà SX ghi **73 ± 2% chestnut extract** ⇒ khớp dải 65–75%, nhưng là *chestnut extract*, không đồng nghĩa 75% tannin thật.
3. Cùng nhà SX còn dòng **40%** (Tanimil SCC) ⇒ **65–75% KHÔNG dùng chung được**. Phải đòi **CoA ghi tannin content + phương pháp định lượng**.
4. Nhận hàng 65% thay vì 75% ⇒ tăng liều **×75/65 = 1,154**.

## 2. Bảng giá NCC (14 dòng có nguồn thật, lấy 21/10/2026)

| Nguyên liệu | Giá gốc + MOQ | VND/kg | Nguồn |
|---|---|---|---|
| Tannin hạt dẻ 75% | 244 EUR/25 kg = 9,76 EUR/kg | 290.783 | S2369969824000367 |
| Thymol feed grade 99% | US$12–15/kg, MOQ 1 kg | 391.000 | made-in-china Thymol |
| Acid rosmarinic | US$41,70–42,70/kg, MOQ 25 kg | 1.112.800 | made-in-china Rosemary_Extract |
| Acid glycyrrhizic 98% | US$126–127/kg, MOQ 1 kg | **3.309.620** | made-in-china Glycyrrhizic_Acid_Price |
| Baicalin 85% | US$54–55/kg, MOQ 1 kg | **1.433.300** | kangdupharm.goldsupplier.com |
| Protease feed grade | US$10,20–14,20/kg MOQ 25 kg (bulk 5–10 USD/kg MOQ 200 kg) | 260.600 | made-in-china Protease_Feed_Grade |
| Bacillus subtilis 200 tỷ CFU/g | US$6,00 (1–49 kg) / 5,50 (50+ kg) | 156.400 | made-in-china …2303067755 |
| Kali diformat 98% | US$900–1.000/tấn, MOQ 1 tấn | 26.060 | made-in-china Potassium_Diformate |
| Acid caprylic + capric C8/C10 | 1.850–2.100 USD/MT | 54.726 | oleochemicalsasia.com |
| Montmorillonite feed grade | US$120–130/tấn, MOQ 1 tấn | 3.388 | made-in-china Montmorillonite_Feed_Grade |
| Beta-cyclodextrin | US$4–6/kg, MOQ 25 kg | 156.400 | alibaba b-cyclodextrin-food-grade |
| Silicon dioxide chống vón | US$1,68–1,88/kg, MOQ 100 kg | 48.993 | made-in-china Food_Grade_Silicon_Dioxide |
| Chất mang dextrose | US$0,45–0,55/kg, MOQ 1.000 kg | 14.333 | made-in-china Dextrose_Monohydrate_Price |
| Hương liệu kem sữa | US$6–7/kg, MOQ 5 kg | 182.420 | alibaba …1601581510875 |

`chua_co_nguon` (3 dòng): **tannin feed-grade** (SaviotanFeed/Silvafeed/Silvachimica chỉ báo giá qua RFQ),
**biochar**, **"nền kiềm"** (chưa xác định được danh mục) ⇒ TC-1+2 và HH-1+2 **không tính được giá vốn**.

Tỷ giá: Vietcombank 21/10/2026 08:03 — USD **bán 26.060**, EUR **bán 29.793,37**
(`vietcombank.com.vn/vi-VN/KHCN/Cong-cu-Tien-ich/Ty-gia`). Dùng giá **bán** vì DN phải mua ngoại tệ.

## 3. Giá vốn VND (kịch bản A = đúng tên hoạt chất trong công thức)

| Công thức | Liều | VND/kg premix | VND/tấn cám |
|---|---|---|---|
| **TC-1** | 2,50 kg/tấn | **325.851** | **814.628** |
| **HH-1** | 4,50 kg/tấn | **2.113.619** | **9.511.286** |
| Sàn TC | 0,70 kg/tấn | 441.345 | 308.942 |
| Sàn HH | 1,80 kg/tấn | 2.544.542 | 4.580.176 |

Kịch bản B (thay GA 98% → chiết xuất cam thảo 18–20 USD/kg; baicalin 85% → chiết xuất hoàng cầm
18–24 USD/kg, đều có nguồn trên chính trang made-in-china Glycyrrhizic_Acid_Price và Alibaba):
HH-1 **457.651 VND/kg** · 2.059.430 VND/tấn · Sàn HH 530.683 VND/kg.

Giả định bắt buộc đã khai ra: thành phần "thymol/acid rosmarinic" coi là **blend 50:50** → 751.831 VND/kg.
Xin CoA + chốt tỷ lệ thật vẫn là **việc còn nợ**.

## 4. Playbook tra giá B2B TĂCN (dùng lại được)

- **`made-in-china.com` + Alibaba: trang SEARCH/SHOWROOM trả giá + MOQ ngay trong snippet kết quả** —
  không cần mở trang sản phẩm. Mẫu URL: `made-in-china.com/products-search/hot-china-products/<Tên_Có_Gạch_Dưới>.html`.
  Đây là nguồn rẻ nhất và nhanh nhất cho nguyên liệu TQ.
- **Giá thị trường hàng hoá** (acid béo C8/C10…): `oleochemicalsasia.com/en/market-insights/supply-chain/...` — nêu dải USD/MT.
- **Tỷ giá**: trang Vietcombank niêm yết đủ USD + EUR (mua tiền mặt / mua chuyển khoản / bán) — dùng giá **bán**.
- **Giá bán lẻ hàng Ý/vùng châu Âu**: trang sản phẩm nông nghiệp (`agrimag.it`) có giá bán theo bao.
- Khi một dải giá được công bố, **được phép chọn một giá trị trong dải** nhưng phải ghi rõ
  "**giá chọn trong dải công bố**, không phải báo giá chốt" — đó là minh bạch, không phải bịa số.

## 5. Bảy bẫy đã dính / đã tránh

1. **Tannic acid (gallnut, CAS 1401-55-4) ≠ tannin hạt dẻ.** Phần lớn listing "tannin" trên
   made-in-china/Alibaba là tannic acid giá US$2,73–8,1/kg. Dùng giá đó cho chestnut tannin là sai hàng.
   Ghi dòng cảnh báo vào bảng chứ đừng lặng lẽ bỏ.
2. **"75%" là titer bột chiết, không phải tannin thật** — polyphenol Folin chỉ ~36%; đừng nhân ngược
   để ra "0,36 × liều".
3. **Đừng tin tên nhà SX là đủ** — cùng Tanin Sevnica có Farmatan 73±2% và Tanimil SCC 40%.
4. **Hoạt chất tinh khiết 98% ở liều kg/tấn làm giá vốn nổ tung**: GA 98% chiếm **>90% giá vốn HH-1**
   (1,91 triệu VND/kg premix). Kết luận đúng phải là *"hai công thức HH PHẢI dùng chiết xuất chuẩn hoá
   nồng độ thấp"*, không phải báo giá vốn rồi im.
5. **Giá niêm yết B2B chưa gồm vận chuyển/thuế/phí** → giá vốn landed cao hơn **15–30%**. Phải nói ra.
6. **Không bịa giá.** Không có nguồn → `chua_co_nguon`. Ngoại lệ duy nhất được phép là **proxy có khai báo**
   (dùng bột tannin 75% titer làm proxy cho tannin feed-grade, kèm câu "nhà SX chỉ báo giá qua RFQ").
7. **Trần giá vốn 27% giá bán** (quy tắc công ty): TC-1 giá vốn 325.851 → giá bán suy ra **1.206.856 VND/kg**.
   Nếu muốn bán premix ~350.000 VND/kg thì giá vốn phải ≤94.500 VND/kg, hiện **cao hơn ~3,4 lần**.
   Đòn giảm chi phí lớn nhất: **tannin (60% giá vốn TC-1)** rồi **thymol/rosmarinic (40%)**.
