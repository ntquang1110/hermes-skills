---
name: feed-additive-sourcing-vn
description: "Use when sourcing/pricing feed additives in Vietnam."
version: 1.1.0
metadata:
  hermes:
    tags: [procurement, feed-additive, TACN, supplier, Vietnam, sourcing]
    category: productivity
---

# Sourcing nguyên liệu TĂCN / phụ gia tại Việt Nam

Dùng khi user cần **mua nguyên liệu cho lô thử nghiệm** (không phải mua tiêu dùng): tìm NCC, báo giá, lên danh sách mua, tính lượng mua. **Hoặc khi cần GIÁ VỐN VND cho một công thức premix** — xem mục *Lấy giá để ĐỊNH GIÁ VỐN* (nguồn giá khác hẳn kênh mua lô thử nghiệm). Bổ trợ cho `purchaser-pro` (skill đó là gate quy trình; skill này là kiến thức thực địa ngành TĂCN VN).

Nguồn gốc: phiên 10/2026, Vua Kiềm — 22 nguyên liệu cho 23 công thức thử nghiệm. **User đã gọi hết danh sách NCC mà không mua được gì.** Đó là bài học trung tâm dưới đây.

## ⚠️ Bài học số 1 — Không phải hết hàng, mà là MOQ

**Nhu cầu lô thử nghiệm ở mức GRAM. MOQ ngành TĂCN ở mức BAO 10–25 kg.** Chênh 4–5 bậc độ lớn.

Số thật đo được: 22 nguyên liệu, đủ cho 23 công thức × 2 kg premix → tổng **864 g**. Món lớn nhất 200 g, **món nhỏ nhất 0,6 g**. Trong khi NCC TĂCN chỉ bán bao 25 kg.

→ Nếu không tính lượng cần TRƯỚC khi đưa danh sách NCC, user sẽ tự phát hiện bằng cách gọi điện thất bại. Mất một vòng đi lại của họ. **Luôn tính trước, và nêu con số "1 đơn vị MOQ đủ cho bao nhiêu lô"** (vd 1 kg thymol đủ 1.666 lô 2 kg) để user thấy vấn đề nằm ở kênh bán, không phải số lượng.

## Định tuyến 3 kênh — đừng đưa một danh sách chung

| Kênh | MOQ | Dùng cho | Câu cần nói |
|---|---|---|---|
| **A. Hóa chất / mỹ phẩm / hóa dược** | 100 g – 1 kg, bán lẻ | hóa chất đơn (thymol, carvacrol, eucalyptol), muối khoáng (MgO, Mg citrate), acid (citric, lactic), chất nhũ hóa (polysorbate 80), vitamin dạng muối (SAP), tannin | "Bán lẻ theo kg không?" |
| **B. Phụ gia chăn nuôi / thủy sản** | bao 10–25 kg, **có quy trình mẫu** | enzyme (phytase, xylanase, protease), probiotic (Bacillus), tannin, acid amin (L-tryptophan), betaine, butyrate, β-glucan | **"Cho tôi xin mẫu 200 g để thử nghiệm công thức"** |
| **D. Sàn TMĐT (Shopee / Lazada / Tiki)** | 100 g – 1 kg, **bán lẻ thật, ship nhanh** | enzyme, probiotic, betaine, tannin, MgO, acid citric, curcumin, dược liệu, tinh dầu | tra bằng `web_search` + `site:shopee.vn` — xem mục *Kênh D* dưới |
| **C. Tự chiết / tự sản xuất** | — | dược liệu bản địa (lá hẹ, huyết dụ, ích mẫu) khi đã có lab | — |

**Kênh bán bao ≠ kênh bán mẫu.** NCC TĂCN lớn thường có quy trình tặng mẫu cho khách kỹ thuật, hoàn toàn khác luồng bán bao cho đại lý. Phải nói rõ loại mình cần, nếu không họ mặc định báo giá bao 25 kg.

**Đừng chỉ đưa kênh A + B.** Sau khi user gọi điện thất bại, bước đúng tiếp theo là **mở kênh D (sàn TMĐT)** — rất nhiều món MOQ 1 kg thật sự nằm ở đó, không nằm ở NCC TĂCN. Bản đồ món nào có/không có trên Shopee: `references/shopee-sourcing-vn.md`.

## Kênh D — Sàn TMĐT: cách tra, và ranh giới phải nói trước

Sàn TMĐT VN là kênh bán lẻ thật cho khoảng một nửa danh sách TĂCN thử nghiệm.

**Tra bằng `web_search` với `site:shopee.vn`** — trả về link sản phẩm thật kèm tên và giá:

```
site:shopee.vn "phytase"
site:shopee.vn "bacillus subtilis"
```

Điều kiện để query ăn:
- Từ khóa **ngắn, 1–3 từ**. Query dài (`thymol 99% bột nguyên chất`) làm search backend bỏ qua toán tử `site:` và trả kết quả rác hoàn toàn.
- **Mỗi lần một từ khóa.** Đừng ghép `hoặc` / `OR` / ngoặc kép lồng.
- Từ khóa **tiếng Việt** ăn hơn tiếng Anh với mặt hàng nội địa (`"magie oxit"`, `"tinh bột nghệ"`, `"hoàng liên"`), nhưng tên hoạt chất quốc tế ăn hơn với hóa chất (`"phytase"`, `"bacillus subtilis"`, `"polysorbate"`).
- Một số từ khóa trả 0 kết quả dù hàng có thật → **đổi cách gọi tên rồi tra lại** trước khi kết luận "không có".

**Bắt URL đầy đủ — không slice.** Link Shopee percent-encode nặng; cắt bằng `url[:150]` là mất đoạn `-i.{shopid}.{itemid}`, phần duy nhất định danh sản phẩm. In full, hoặc ghi ra JSON rồi nạp lại. Link cụt không dùng được.

**Suy URL shop từ URL sản phẩm:** `...-i.1129318902.51660140469` → shop `https://shopee.vn/shop/1129318902`. Shop nào bán nhiều món của mình thì gom một đơn; ghi rõ "shop vàng" trong output.

**Ranh giới phải nói TRƯỚC với user, một dòng, không giấu:**

> Đọc trang sản phẩm bị chặn, nên em KHÔNG verify được nơi bán / tồn kho / giá chính xác — anh dùng bộ lọc **"Nơi bán: Hà Nội"** trên Shopee.

Đừng im lặng để user tưởng đã lọc hộ. Nhưng **cũng đừng vì thế mà bỏ kênh D**: link thật + tên + giá vẫn là giá trị lớn hơn danh sách NCC qua điện thoại.

**Web shop hóa chất VN thì đọc được bằng `curl`** (verify được: nguyenquan.vn, vdchem.com, hoachatdalat.com, kimmachem.com) → lấy được **địa chỉ + giá thật**. Dùng kênh này cho các món sàn không có.

**Tiki không có nguyên liệu B2B** — `tiki.vn/api/v2/products?q=thymol` trả 0 kết quả. Tiki là sàn tiêu dùng. Đừng mất vòng ở đó.

## Danh bạ NCC (tra 10/2026, số lấy từ website chính thức)

**Kênh A — hóa chất / dược / mỹ phẩm**
- VietChem (CP XNK Hóa chất & Thiết bị Kim Ngưu) — 0963 029 988 / 0862 157 988 — 41 phố Trạm, Long Biên, HN — hóa chất công nghiệp + thực phẩm
- Vĩnh Nam Anh — 028 37107317 (HCM) / 024 38717853 (HN) — phụ gia, nguyên liệu thực phẩm/dược/thú y/thủy sản
- Hải Âu (CP Quốc tế Hải Âu) — 0983 56 56 28 / 0976 244 181 — Lô 112 Mỗ Lao, Hà Đông, HN — hóa chất thực phẩm
- Hóa chất Nguyễn Phát — 036 222 5552 / 0932 099 488 — 50/1A TL29, Q12, HCM
- VMC Group (Hóa chất Việt Mỹ) — 0947 464 464 — 61 Ngõ 381 Nguyễn Khang, HN
- Đắc Khang — 0983 111 490 — 482/10/28A1 Nơ Trang Long, Bình Thạnh, HCM — nhập khẩu đa ngành
- Nguyễn Quân — 028 38654110 — 354/6 Lý Thường Kiệt, Q10, HCM — **polysorbate 80 (Croda Singapore)**
- VCS Group — 0919 105 399 — **Tween 80 Duksan Hàn Quốc**
- VDchem — 028 38208121 — **sodium ascorbyl phosphate**
- Nguyễn Bá Chemical — 0931 15 17 12 — SAP, nguyên liệu mỹ phẩm
- Dalosa Việt Nam (Tinh dầu Thảo dược Dalosa) — 0967 22 7899 / 0902 82 2729 — 234/1 Vườn Lài, Tân Phú, HCM — **thymol 99%, carvacrol, eugenol, camphor, dược liệu khô**

**Kênh B — phụ gia chăn nuôi / thủy sản**
- Acare Việt Nam — 028 6280 5457 — KDC Rạch Chiếc, Phước Long, HCM — **CarePhos (phytase), ButyMax/TributyCare (butyrate), CareBiotics/GUTCARE (probiotic), PLEXOMIN (khoáng hữu cơ)**
- ICFOOD Việt Nam — 0896 649 000 (B2B) — KCN Tân Bình, Tân Phú, HCM — **enzyme Angel Yeast (phytase 10.000 u/g), men vi sinh, β-glucan**
- Hưng Tín (TNHH XNK Hưng Tín) — 0919 60 1838 — Q12, HCM — **Betaine HCl 98% Sunwin, β-glucan Immunowall, acid amin, acid citric**
- Kim Mã — 0948 411 105 — **Betaine HCl 98%** (bao 25 kg, CAS 590-46-5)
- Hóa chất Bách Khoa — 0976 898 778 — 71 Nguyễn Tư Nghiêm, Bình Trưng, HCM — **L-Tryptophan 98% (Ajinomoto/CJ/Evonik)**
- Bio-Pharmachemie — 028 3731 3489 — men vi sinh, probiotic, thú y
- Vemedim — 0293 394 9269 — 322A đường 30/4, Ninh Kiều, Cần Thơ — chế phẩm sinh học
- BioPro Khánh Hòa — 0901 135 126 — men vi sinh nguyên liệu, enzyme
- **Ánh Dương Khang (TNHH MTV Dinh dưỡng)** — 0938 171 477 / 0283 6204131 — 44 Đường N1, KDC LaCasa, Phú Thuận, HCM — **nhập Silvafeed (Ý): tannin Chestnut ≥75% thủy phân, tannin Quebracho**

**Nước ngoài (khi nội địa không có)**
- Hunan Nutramax / Tây An Rongsheng / Shaanxi Jiahe — chiết xuất thảo dược TQ (glycyrrhizin/cam thảo) — 2–4 tuần
- PMC Isochem (Pháp) / alphahi-tech (TQ) — **Vitamin E TPGS (tocofersolan)** — khó nhất, chưa có NCC nội địa xác nhận — 3–5 tuần
- Silvateam (Ý) / Unitán (Argentina) — tannin Quebracho
- Zhejiang Nhu (TQ) / DSM — sodium ascorbyl phosphate

## Toán lượng mua cho lô thử nghiệm

Cấu trúc bài toán đã gặp: **lô N kg premix, tỷ lệ trộn M kg/tấn cám**.

1. `gram nguyên liệu i trong 1 lô = tỷ lệ % i / 100 × N × 1000`
2. `cám trộn được từ 1 lô = N / M × 1000` (vd 2 kg premix, 5 kg/tấn → **400 kg cám**)
3. **Tổng cần = Σ qua tất cả công thức**, cộng theo nguyên liệu (SUMIF), **không cộng tay**
4. `base = tổng sản phẩm − tổng hoạt chất` — dùng làm ô đối chiếu, phải khớp
5. Bọc mọi công thức trong `ROUND(...,3)` ngay từ đầu (nhiễu float từ `/100*2000`)

Dựng thành **tab tính sống** trong Google Sheet: ô khối lượng lô + cột tỷ lệ % đều sửa được, đổi số là cả bảng tự tính lại. Xem `google-sheets-data-fill` để biết chi tiết API.

**Tỷ lệ không có trong tài liệu gốc → phải đánh dấu `GIẢ ĐỊNH - cần chốt`, không im lặng dùng.** Liều chuẩn để tham chiếu khi phải giả định:
- Phytase: 1% của premix, với premix trộn 5 kg/tấn → 500 FTU/kg cám (đúng liều chuẩn). Số này verify được bằng phép tính, giữ được.
- Xylanase 1%, Protease 0,5%, Bacillus 0,5%, Vitamin E 0,05%, Se (men selen 2000 ppm) 0,02%.

## ⚠️ Khâu cân — lượng cần < 5 g/lô thì cân thường không cân được

Với món dưới ~5 g/lô (thymol, carvacrol, eucalyptol, SAP, Mg chelate, vitamin E, Se), phải **pha premix mẹ 1%**: 1 g hoạt chất + 99 g chất độn, rồi cân bội số 100×. Ví dụ carvacrol 0,6 g → cân 60 g premix mẹ. Nêu trong output khi có món dưới ngưỡng.

## Chuẩn bàn giao danh sách NCC (yêu cầu cứng của user)

1. **MỖI mặt hàng phải có tối thiểu 1 NCC kèm SỐ ĐIỆN THOẠI.** User nói rõ: *"anh yêu cầu tối thiểu một nhà cung cấp là phải có số điện thoại"*. Danh sách không có số = vô dụng vì user sẽ gọi.
2. Số lấy từ **website/kênh chính thức của công ty**, không suy luận. Ghi ngày tra.
3. **Tách rõ 2 loại NCC:** `Có sẵn` (đã niêm yết đúng sản phẩm đó trên website) vs `Hỏi` (suy luận theo nhóm hàng của NCC, phải gọi xác nhận). Trộn lẫn hai loại làm user hụt khi gọi.
4. Mặt hàng tự chiết vẫn phải có dòng NCC cho **nguồn nguyên liệu thô** kèm số, để không vi phạm quy tắc 1.
5. Format: 2 tab — **Danh bạ NCC** (công ty | SĐT | email | website | địa chỉ | chuyên mặt hàng) + **NCC theo mặt hàng** (mặt hàng | NCC | SĐT | trạng thái | ghi chú). Dạng long, mỗi dòng 1 cặp item–NCC.
6. Khi deliverable là **danh sách link sàn**: gom theo TRẠNG THÁI MUA, không theo thứ tự nguyên liệu — nhóm `mua được ngay` (xanh) / `shop vàng` (vàng) / `không có trên sàn` (đỏ). User cần biết mua được gì TRƯỚC; phần không mua được để riêng ở cuối.
7. **Mỗi món 1–4 link để user tự chọn.** User nói rõ: *"Một sản phẩm có thể có được nhiều link để anh đưa lựa chọn."* Một link duy nhất là không đủ.
8. Ghi rõ món nào **đúng quy cách** vs món nào **phải hỏi shop trước** (tinh dầu oregano → hỏi % carvacrol; tannin → hỏi có phải chestnut; "bột cam thảo" → là rễ nghiền, KHÔNG phải glycyrrhizin chiết). Trộn lẫn hai loại làm user mua nhầm.

## ⚠️ Cảnh báo dạng nguyên liệu — mua nhầm là thiêu công thức

Bắt buộc kiểm trước khi chốt mua, vì bù liều không cứu được:
- **Berberine HCl ≠ "chiết xuất hoàng liên" thô** (thô thường chỉ 5–10% berberine)
- **Na-selenite ≠ Selenium Yeast** (vô cơ tan nước vs hữu cơ dạng bột — khác hẳn với dòng nước)
- **Propolis glycolic extract ≠ ethanol extract** (ethanol đục khi pha nước kiềm)
- **Enzyme PHẢI dạng coated / chịu kiềm** khi nền là khoáng kiềm pH 8–9 — dạng thường mất 50–80% hoạt tính
- **Vitamin E phải dạng TPGS** (E thường không tan nước)
- **Vitamin C gốc → thay Sodium ascorbyl phosphate** (gốc C tạo phức Ca²⁺, oxy hoá nhanh ở pH > 7)
- **Curcumin phải nano/phytosome** (thường phân hủy 40–60% sau 30 ngày ở pH 8–9)
- **Tannin hạt dẻ: hỏi TITER, đừng hỏi "có phải chestnut" là đủ.** Dải thật ngoài thị trường **40% → 55% → 73±2% → 75%** (cùng một nhà SX Tanin Sevnica có Farmatan 73±2% *và* Tanimil SCC 40%); "75%" là **tannin titer của bột chiết chuẩn hoá**, không phải tannin thật (polyphenol Folin chỉ ~36%). Bắt buộc đòi **CoA ghi tannin content + phương pháp định lượng**, và ghi rõ trong công thức "**quy về tannin titer 75%**" — nhận hàng 65% thì tăng liều **×75/65 = 1,154**.
- **`tannic acid` (gallnut, CAS 1401-55-4) KHÔNG phải tannin hạt dẻ.** Đây là bẫy chết người khi tra giá: phần lớn listing "tannin" trên made-in-china/Alibaba là tannic acid giá **US$2,73–8,1/kg**, rẻ hơn chestnut tannin ~1,5 lần. Dùng giá đó để tính giá vốn tannin hạt dẻ là sai hàng.

## Lấy giá để ĐỊNH GIÁ VỐN — khác hẳn lấy giá để mua lô thử nghiệm

Khi user cần **giá vốn VND cho một công thức premix** (không phải mua), nguồn đúng là **giá niêm yết B2B**, không phải kênh D bán lẻ.

**Nguồn ăn nhất, theo thứ tự:**
1. **`made-in-china.com` + Alibaba — trang SEARCH/SHOWROOM trả giá + MOQ ngay trong snippet kết quả.** Mẫu URL: `made-in-china.com/products-search/hot-china-products/<Tên_Có_Gạch_Dưới>.html` (vd `Potassium_Diformate`, `Montmorillonite_Feed_Grade`, `Glycyrrhizic_Acid_Price`). `web_search` + `web_extract` trang search là đủ; không cần mở từng trang sản phẩm. Đây là đường rẻ nhất cho nguyên liệu Trung Quốc.
2. **`oleochemicalsasia.com/en/market-insights/supply-chain/...`** cho giá hàng hoá (C8–C10, acid béo) theo USD/MT.
3. **Trang sản phẩm nông nghiệp châu Âu** (`agrimag.it`) cho hàng Ý/EU, thường có giá bán theo bao.
4. **Tỷ giá: trang Vietcombank** `vietcombank.com.vn/vi-VN/KHCN/Cong-cu-Tien-ich/Ty-gia` — có đủ USD + EUR (mua tiền mặt / mua chuyển khoản / bán). **Dùng giá BÁN** vì doanh nghiệp phải mua ngoại tệ trả NCC. Ghi kèm ngày + giờ niêm yết.

**Luật trình bày giá — bắt buộc:**
- Mỗi dòng giá phải có: NCC, **URL thật**, **ngày lấy giá**, đơn vị + **MOQ**, giá gốc, giá VND/kg quy đổi, tỷ giá dùng.
- Dải giá công bố thì **được phép chọn một giá trị trong dải**, nhưng phải ghi rõ "**giá chọn trong dải công bố, không phải báo giá chốt**". Đó là minh bạch, KHÔNG phải bịa số.
- Không có nguồn → ghi `chua_co_nguon`. **Ngoại lệ duy nhất được phép: proxy có khai báo** — dùng mặt hàng cùng loại cùng titer làm giá tạm, kèm câu nói rõ vì sao (vd "nhà SX chỉ báo giá qua RFQ").
- Nêu thẳng **giá niêm yết B2B chưa gồm vận chuyển + thuế + phí → giá vốn landed cao hơn 15–30%**.
- Bảng Markdown rộng **tối đa 6 cột**, mỗi bảng 1 mục, đọc được trên mobile. URL dài để ở mục "Nguồn" bằng nhãn `[S1]`, `[S2]` và bảng chỉ ghi nhãn.

**Cờ đỏ kinh tế phải báo ngay khi thấy:** hoạt chất **tinh khiết cao (98%/85%) ở liều kg/tấn** làm giá vốn nổ tung — ca thật acid glycyrrhizic 98% (3,31 triệu VND/kg) chiếm **>90% giá vốn** một công thức premix, cho ra 9,5 triệu VND nguyên liệu/tấn cám ⇒ **phi thực tế**. Kết luận đúng là *"phải dùng chiết xuất chuẩn hoá nồng độ thấp"*, không phải đưa con số rồi im.

**Đối chiếu trần giá vốn của công ty: giá vốn ≤ 27% giá bán lẻ.** Từ giá vốn suy ra giá bán tối thiểu (`giá vốn / 0,27`) và **nói rõ đạt/không đạt**.

Chi tiết số của một ca thật (14 nguyên liệu, tannin hạt dẻ, giá vốn 4 công thức): `fixgby/references/no-02-gia-von-tannin-va-gia.md`.

## Pitfalls

- **Đừng đưa danh sách NCC trước khi biết lượng cần.** Không có con số thì không định tuyến được kênh, và user sẽ gọi sai kênh hàng loạt.
- **Đừng ghi con số lý thuyết vào cột "đề xuất mua".** Ghi 0,6 g vào cột mua là vô nghĩa với người đi mua. Ghi đơn vị mua được thật (0,5 kg / 1 kg / xin mẫu / tự chiết).
- **Không bịa giá.** Không lấy được giá thật → ghi "Xin báo giá" (khi đi mua) hoặc `chua_co_nguon` (khi tính giá vốn). Chỉ ghi giá khi có nguồn (vd giá tham khảo TQ trên made-in-china). Cách đầy đủ để lấy giá + dựng bảng giá vốn: mục *Lấy giá để ĐỊNH GIÁ VỐN* ở trên.
- **Đừng tự ý "tốt bụng" thêm món ngoài công thức.** Nếu danh sách quy hoạch cũ có món không xuất hiện trong công thức nào, ghi chú `Không có trong CT` để user không mua nhầm — nhưng không tự xoá.
- **Nền khoáng kiềm làm hỏng phân tích theo pH.** pH chỉ có nghĩa khi có dung dịch; với sản phẩm bột khô, biến số đúng là **nước hoạt động (aw)** và độ hút ẩm.
- **Đừng kết luận "thị trường không bán lẻ" sau một vòng NCC TĂCN.** Kênh B (bao 25 kg) gần như luôn thất bại với lô thử nghiệm. Câu trả lời đúng là chuyển kênh D, không phải báo user "phải nhập khẩu". Nhiều món user tưởng phải nhập (phytase, xylanase, protease, bacillus, betaine, tannin, MgO, acid citric) thực tế có sẵn túi 1 kg trên Shopee.
- **Đừng cắt URL sàn khi in ra.** Slice làm mất `-i.{shopid}.{itemid}` — user không mở được link, phải làm lại cả vòng tra.
- **Đừng bỏ qua shop bán nhiều món một lúc.** Shop bán buôn nguyên liệu cấp thực phẩm thường có 4–6 món trong cùng danh sách (một shop đã có phytase + betaine + magiê citrate + L-tryptophan). Tìm ra shop đó tiết kiệm cho user nhiều đơn ship — nêu riêng trong output như một mục "vào đây trước".
