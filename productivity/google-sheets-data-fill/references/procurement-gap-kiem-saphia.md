# Rút danh sách thu mua (procurement gap) từ tài liệu R&D — Vua Kiềm / Kiềm Saphia

Worked example 10/2026: 2 tài liệu HTML ở `preview.thefirstonly.com` → 14 mặt hàng thiếu → thêm vào tab "Thu mua" (spreadsheet `<SHEET_ID>`).

## Nguồn dữ liệu

- **`1h3196qthffu`** — "Kế hoạch R&D — 23 Công thức Thử nghiệm". 5 dòng sản phẩm, 23 công thức:
  | Dòng | Mã | Dạng | Số CT | Mục tiêu |
  |---|---|---|---|---|
  | Hô hấp | RS-01 | Bột | 4 | giảm ho, khò khè (heo sau cai sữa) |
  | Tiêu chảy | GT-01 | Bột | 5 | thay ZnO (heo con cai sữa) |
  | Viêm tử cung | MT-01 | Nước | 4 | nái sau đẻ (MMA), trên nền EZ67 |
  | Sinh trưởng | GR-01 | Bột | 5 | giảm FCR, thay AGP |
  | Stress + dễ ngủ | GS-01 | Bột | 5 | L-Tryptophan → serotonin |

  Base: Kiềm Thảo Dược (Ca/Na/K/Mg + Xạ đen, Tía tô, Hoàn ngọc, Chè dây). ~700k/10kg bột, ~1.800k/20L nước. Hoạt chất thêm chỉ 2–6% giá vốn.
- **`ozya5921okt6`** — "Chất chuẩn — 5 dòng Kiềm Thảo Dược". 19 chất tương tác OK + 10 chất có vấn đề ở pH 8–9 kèm giải pháp. **Đây là bảng quyết định dạng nguyên liệu**, không phải bảng lý thuyết.

## Quy trình 4 bước

1. **Gom TẤT CẢ hoạt chất** xuất hiện trong mọi bảng công thức, kể cả dạng gộp. VD `Thymol / Carvacrol` nằm chung 1 dòng sheet nhưng là **2 chất riêng** (RS-01A dùng Thymol, RS-01B dùng Carvacrol) → phải tách, mỗi chất một dòng một giá. Gộp thì không thấy được giá vốn từng dòng công thức.
2. **Đối chiếu 3 nguồn**: (a) danh sách đã mua có báo giá, (b) wishlist sẵn có trong sheet, (c) yêu cầu rút từ tài liệu R&D.
3. **Item chưa có dòng nào → append mới**: `STT | Phân loại | Tên cần [liều — công thức dùng] | Trạng thái`. Để trống NCC/giá/nguồn gốc nếu nguồn không có — không bịa.
4. **Check dạng nguyên liệu** (bên dưới) — đây là chỗ giá trị nhất.

## Checklist dạng nguyên liệu — mua nhầm là thiêu công thức

Số liệu lấy trực tiếp từ bảng chất chuẩn pH 8–9 (dung dịch kiềm khoáng, nền EZ67 / Kiềm Thảo Dược).

| Dạng mua | Dạng cần | Vì sao | Bằng chứng |
|---|---|---|---|
| Chiết xuất thảo dược thô | Hoạt chất tinh khiết / dạng muối | Chiết xuất thô nồng độ thấp, không đạt liều tính trong công thức | "Chiết xuất hoàng liên" 550k/kg ≠ **Berberine HCl**; công thức GT-01 cần 0,10–0,15% berberine. Chiết xuất thô thường 5–10% berberine → liều tính sai hoàn toàn. Bảng chất chuẩn ghi rõ "cần dạng chloride" |
| Selenium Yeast (dạng hữu cơ, bột) | **Na-selenite** (vô cơ, tan nước) | MT-01 là **dạng nước**; selenium yeast bột khó hòa tan | #11 Selenium — "Tan nước. Ổn định pH 8-9" |
| Propolis ethanol extract | **Propolis glycolic extract + Polysorbate 80 0,5%** | Ethanol extract **đục** khi pha vào nước kiềm pH 8–9 | #25 |
| Enzyme dạng thường | **Dạng coated / enzyme chịu kiềm Bacillus** | pH 8–9 phá hoạt tính | #21 Phytase mất **60–80%**; #22 Xylanase mất **50–70%**; #23 Protease mất hoạt tính |
| Curcumin dạng thường | **Nano / phytosome** | Không tan nước, phân hủy 40–60% sau 30 ngày ở pH 8–9 | #24. Nếu NCC không có dạng nano → bỏ mặt hàng |
| Vitamin E (dầu) | **Dạng TPGS** (tan nước) | Dầu không tan trong nước | #26 |
| Vitamin C (ascorbic acid) | **Bỏ, hoặc Sodium ascorbyl phosphate** | Tạo phức Ca²⁺/Mg²⁺ (là khoáng của base), oxy hóa nhanh ở pH>7 | #28 |
| Tannin (chestnut/quebracho) | Vẫn dùng, nhưng **bù liều 25%** hoặc sachet đôi | Tạo phức không tan với Ca²⁺/Mg²⁺ → mất 20–30% | #20 |
| Acid citric | Tăng liều 0,5–1% hoặc bỏ | Bị trung hòa ở pH 8–9, mất tác dụng acid hóa | #29. Riêng mục đích **hạ pH EZ67 12→8–9** thì vẫn dùng (2–5 g/L) |
| Tinh dầu (oregano, thymol...) | **Nhũ hóa Tween 80, tỷ lệ 1:4** | Không tan trong nước | #27 |

**Dấu hiệu cần nghi ngờ dạng nguyên liệu:** công thức ghi một danh tính hóa học cụ thể (Berberine HCl, Na-selenite, Calcium butyrate) nhưng sheet thu mua lại ghi tên chung chung ("chiết xuất hoàng liên", "men selen", "butyrate"). Lệch này không tự sửa được bằng cách bù liều — phải đổi mặt hàng.

**Lưu ý Calcium butyrate vs Na-butyrate:** bảng chất chuẩn ghi Calcium butyrate ("là muối Ca — bổ sung vào nền khoáng") trong khi sheet wishlist ghi "Butyrate (Na-butyrate)". Cần user chốt form theo dòng sản phẩm (GUT-HP muốn muối Ca) trước khi hỏi giá.

## Ma trận đối chiếu theo dòng sản phẩm (5 cột đánh dấu)

Sau khi đã có danh sách mặt hàng, bước tiếp theo user cần là **"đang thiếu gì cho từng dòng công thức"**. Dựng 5 cột (O–S) trên tab "Thu mua", mỗi dòng nguyên liệu đánh dấu `Đã có` / `THIẾU` / để trống (không dùng ở dòng đó).

- Header mỗi cột là công thức tự đếm `COUNTIF(...,"THIẾU")` — xem SKILL.md mục "Technique: status matrix". Mua thêm hàng → số tự giảm, không cần sửa tay.
- Thêm 1 cột "Ghi chú kỹ thuật" ghi lý do cụ thể cho từng dòng (`BẮT BUỘC dạng coated…`, `Chi RS-01D`, `23 CT nhằm THAY THẾ ZnO — không mua đợt này`). Cột này là thứ người mua đọc khi gọi NCC.
- **Ô đánh dấu 1 dòng có thể đại diện nhiều mặt hàng.** Dòng "Thymol / Carvacrol" gộp 2 chất → header đếm theo *dòng*, không theo *chất*. Nói rõ trong báo cáo, đừng để user hiểu nhầm số.

Kết quả 10/2026 (7 mặt hàng đã mua):

| Dòng | Đã có | Thiếu | Món thiếu |
|---|---|---|---|
| MT-01 Viêm tử cung | 5 | 4 | Vitamin E TPGS, Huyết dụ, acid citric, acid lactic, polysorbate 80 |
| RS-01 Hô hấp | 2 | 4 | Thymol, Carvacrol, Glycyrrhizin, lá hẹ, SAP |
| GT-01 Tiêu chảy | 1 | 5 | Tannin Chestnut, Quebracho, Butyrate, Bacillus, β-glucan |
| GR-01 Sinh trưởng | 0 | 5 | Phytase, Xylanase, Betaine, Bacillus, acid citric |
| GS-01 Stress | 0 | 6 | L-Tryptophan, MgO, Mg chelate, Betaine, Phytase, Xylanase |

**Bài học lớn nhất:** 7 mặt hàng đã mua dồn gần hết vào **một** dòng (MT-01). Bốn dòng còn lại chưa chạy được công thức nào, GR-01 và GS-01 trắng hoàn toàn. Khi user nói "anh đã mua rồi", phải chỉ ra ngay **đã mua nhưng chưa mở khoá được gì** — đó mới là giá trị của phần đối chiếu.

## Xếp ưu tiên mua: tối thiểu hoá số món để mở khoá nhiều công thức

Đừng báo "còn thiếu 22 món". Tính **tập mua tối thiểu** rồi xếp ưu tiên theo số công thức mở khoá được trên mỗi món:

| Mua thêm | Mở khoá |
|---|---|
| Vitamin E TPGS (1 món) | MT-01A, MT-01B, MT-01C |
| Thymol + Glycyrrhizin (2 món) | RS-01A |
| Tannin Chestnut + Butyrate (2 món) | GT-01A |

→ **5 món mở khoá 5 công thức của 3 dòng khác nhau.** Đây là câu chốt user cần, không phải danh sách dài.

Nhóm ưu tiên dùng khi viết tab kế hoạch: P1 (mua ngay) → P2 (mở khoá được dòng thứ hai) → P3 (mở khoá dòng khác hoàn toàn) → P4 (phụ liệu dùng chung) → P5 (mở rộng). Tô màu cột Ưu tiên bằng conditional formatting `TEXT_CONTAINS "P1"` / `"P2"` / `"P3"`.

**Đừng quên món lead time dài.** Vitamin E TPGS và Glycyrrhizin 2–4 tuần (nhập khẩu) — chúng chặn cả dòng, nên phải nêu riêng là "đặt trước", không lẫn vào nhóm gọi trong ngày.

## Cảnh báo mua nhầm: 19 dòng wishlist không thuộc 23 công thức

Wishlist cũ trong sheet có 19 dòng **không xuất hiện trong bất kỳ công thức nào** của kế hoạch R&D: Tea tree oil, Inulin, MOS, Chitosan, Bentonite/Zeolite, Yeast cell wall, ZnO, CuSO₄, Rong biển, Acid sorbic, Nisin, Isoliquiritigenin, Saponin Yucca, Capsicum oleoresin, Hydroxyapatite nano, tinh dầu Rosemary, tinh dầu quế, MCFA, bột tỏi. Ghi chú "Không có trong 23 CT" vào cột Ghi chú kỹ thuật cho từng dòng. Riêng ZnO ghi rõ lý do ngược lại: **23 CT được thiết kế để THAY THẾ ZnO**, nên không mua.

Lưu ý: mặt hàng đã mua vẫn có thể vô dụng. Bột tỏi (800k/kg) không có trong công thức nào — phải nói thẳng, không giả định user mua cho việc khác.

## Bàn giao cho purchaser-pro

Sau bước này, danh sách 22 mặt hàng + nhóm ưu tiên là **đầu vào** cho quy trình sourcing: xem skill `purchaser-pro` và `references/vn-feed-additive-suppliers.md` (NCC nội địa thật đã tra được: thymol, betaine, L-tryptophan, tannin, enzyme, probiotic).

## Bột khô thì không có pH — nhưng không có nghĩa là không phản ứng

User hỏi (10/2026): sản phẩm bào chế hoàn toàn dạng bột mịn, không dính nước, thì khoáng Ca/K trong EZ80 có làm đổi pH tổng hay hỏng thành phần nào không. Trả lời có cấu trúc:

1. **pH chỉ định nghĩa khi có dung dịch.** Bột khô không có pH → đúng, nhưng "không có pH" ≠ "không có phản ứng".
2. **Khoáng kiềm tự tạo nước cho nó.** CaO + H₂O → Ca(OH)₂ (dung dịch bão hoà pH ≈ 12,4); K₂CO₃ hút ẩm, pH ≈ 11,5. Bột "khô" kéo hơi ẩm từ không khí về bề mặt hạt khoáng, tạo màng nước siêu mỏng ở **pH 11–12,5** — đúng các phản ứng trong bảng chất chuẩn xảy ra ở đó, chỉ khác quy mô. Oxide/hydroxide hút ẩm mạnh hơn carbonate/phosphate nhiều → **hỏi user dạng khoáng trước khi kết luận**.
3. **Ba cơ chế vẫn chạy trong bột khô:** nước hoạt động (aw), phản ứng xúc tập tại điểm tiếp xúc (tannin + Ca²⁺), và phản ứng acid-base rắn. Bằng chứng cho cái thứ ba: quy trình chế tạo calcium ascorbate chính là cho ascorbic acid phản ứng với CaCO₃/Ca(OH)₂ mol 2:1 ở 60–80 °C (patent CN1112418A) — ở nhiệt độ phòng chậm nhưng không bằng không. Đây là lý do phải dùng **Sodium ascorbyl phosphate** thay ascorbic acid trong nền khoáng.
4. **Đổi trục đánh giá từ pH sang aw.** Bảng chất chuẩn hiện tại chỉ đúng cho **dòng nước (MT-01/EZ67/METRI-HP)**. Bốn dòng bột (RS/GT/GR/GS) phải đánh giá theo **nước hoạt động aw + độ hút ẩm**, ngưỡng kiểm soát aw < 0,6. Không dùng pH để đánh giá bột — vô nghĩa. Enzyme trong bột hỏng vì **aw**, không phải vì pH.

Nguồn cho aw: FDA "Water Activity (aw) in Foods"; Aqualab "Water Activity for Food Safety & Quality Control" (aw điều khiển phản ứng không enzym, oxy hoá lipid, thoái hoá vitamin, biến tính protein).

Câu hỏi cần user trả lời để chốt được: (1) EZ80 khoáng dạng oxide/hydroxide hay carbonate/phosphate, (2) quy trình có sấy/trộn ướt không hay blend khô 100%, (3) bao bì PE thường hay có màng chắn + túi hút ẩm.

## Mẹo điền sheet liên quan

- Ghi liều + mã công thức vào cột "Tên cần" dạng `[liều — công thức]` để người mua biết spec cần hỏi NCC.
- Cột Trạng thái phải lấy đúng từ vựng tab "Tham chiếu" của spreadsheet (xem SKILL.md mục 2).
- Không gõ block tổng nếu user đã xoá trước đó; hỏi lại nếu thật sự cần.
