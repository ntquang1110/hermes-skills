# NO-01 — Cửa C (miễn dịch niêm mạc) có bằng chứng trên HEO chưa?

Câu hỏi bằng chứng (21/10/2026), cho `docs/14-cong-thuc-co-ban`. Sản phẩm: `no-01-bacillus-iga.md` + `no-01-bacillus-iga.json`.
Trạng thái trước đó của công thức tiêu chảy: phủ **A/B/D**, **cửa C = 0** (không chất nào trong 57 hoạt chất đã khảo sát có bằng chứng từ bậc L2 cho miễn dịch niêm mạc).

## 1. Kết luận — Bacillus PHỦ ĐƯỢC cửa C ở bậc L2

**CÓ** bằng chứng đo IgA tiết trong phân **trên HEO**: **3 nghiên cứu**, trong đó **2 bài có *B. subtilis* đích danh**.
Luận điểm "57 hoạt chất không có chất nào có L2 cho miễn dịch niêm mạc" **không còn đúng với Bacillus**.

## 2. Thang 4 MỨC IgA — thứ tự này là luật, đừng trộn

| Mức | Là gì | Tính cho cửa C? |
|---|---|---|
| 1 | IgA tiết trong **phân** (fecal sIgA), ELISA | **CÓ — chính là cửa C** |
| 2 | IgA **đặc hiệu kháng nguyên** trong phân (do VẮC-XIN) | KHÔNG — là bằng chứng vắc-xin |
| 3 | sIgA **mô / chất chứa ruột** (sinh thiết, kết tràng) | KHÔNG — gần cơ chế, khác phép đo |
| 4 | IgA **huyết thanh / huyết tương** | KHÔNG — hệ thống, không niêm mạc |

## 3. Bằng chứng mạnh nhất — PMID 40821810 (liều TRÙNG khớp dự án)

- Hỗn hợp **SLV / BioPlus 2B (Chr. Hansen)**: *B. subtilis* DSM5750 + *B. subtilis* DSM27273 + *B. licheniformis* DSM5749, tỉ lệ **2:1:1**, tổng **3,25×10⁹ CFU/g**.
- **360 heo con cai sữa** (D×L×Y, 24 ngày tuổi), 42 ngày, 3 nhóm.
- **SLV200 = 200 mg/kg cám = 0,20 kg/tấn cám** — **TRÙNG ĐÚNG liều 0,20 kg premix/tấn cám của fixgby** (≈ 6,5×10⁸ CFU/kg cám). SLV400 = 400 mg/kg cám (≈ 1,3×10⁹ CFU/kg cám).
- **sIgA phân đo bằng ELISA** → SLV200 tăng ngày 42 (**P = 0,014**); xu hướng tăng ngày 14 (P < 0,10); ↓ tỉ lệ tiêu chảy (P < 0,05).
- Tương quan: sIgA phân ↔ IgM huyết thanh **r = 0,67**; sIgA phân ↔ E. coli phân **r = −0,38**.
- Hội đủ 6 yếu tố mà các bài khác thiếu: đúng đối tượng · liều đổi được ra kg/tấn cám · đo trực tiếp · n lớn · có kết cục lâm sàng · 2/3 chủng là *B. subtilis*.

**Hệ quả thực dụng:** liều premix dự án đang định dùng chính là liều đã chứng minh tăng sIgA phân trên heo con cai sữa. Còn nợ: chế phẩm định mua có đạt 3,25×10⁹ CFU/g không — nếu thấp hơn phải tăng kg premix/tấn cám.

## 4. Ba nghiên cứu đo IgA PHÂN trên heo

| PMID | Chủng | Liều | Kết quả |
|---|---|---|---|
| **40821810** | *B. subtilis* DSM5750 + DSM27273 + *B. licheniformis* DSM5749 | 200 mg/kg cám | ↑ sIgA phân ngày 42 (P=0,014) |
| **30617949** | *B. subtilis* JS01 | 1×10⁶ CFU/g cám, 35 ngày | sIgA phân cao **chỉ sau 35 ngày**; thua chủng *L. johnsonii* BS15 đối chứng |
| **17760301** | *B. cereus* var. *toyoi* NCIMB 40112 (= *B. toyonensis*) | `chua_co_nguon` | ↑ **rõ rệt** IgA phân ở nái; heo con ↑ trước cai sữa |

Cộng thêm: `36364738` (SIgA **chất chứa kết tràng**, *L. acidophilus* + *B. subtilis*, 0,1% khẩu phần) — mức 3, không phải mức 1.

## 5. Bài tổng quan "29 nghiên cứu" — CÓ THẬT, nhưng KHÔNG đo chỉ tiêu này

- **CÓ TỒN TẠI**: PMID **42450761**, PMCID **PMC13359635**, *Animals* (MDPI) 2026, doi 10.3390/ani16132054. 619 bản ghi (2000–2025) → **29 nghiên cứu** đạt PRISMA/PICOS. **Không hề bịa.**
- **Nhưng kiểm toàn văn `PMC13359635/fullTextXML`** → đếm cụm từ:
  - `"fecal IgA"` = **0** · `"faecal IgA"` = **0** · `"sIgA"` = **0** · `"secretory"` = **0**
  - `fecal/faecal` = 41 lần, **toàn bộ** là *fecal score / microbiota / shedding / SCFA*.
- IgA mà bài tổng quan báo cáo là **IgA huyết tương** (Lewton et al.) và **IgA huyết thanh** (Li et al.) — mức 4.
- ⇒ Dùng bài này để trích **tăng trọng / tiêu chảy / hình thái ruột / microbiota** thì đúng; trích **miễn dịch niêm mạc / sIgA phân** thì **SAI**. Bằng chứng cho cửa C nằm ở các bài **độc lập, NGOÀI** 29 nghiên cứu đó.

## 6. Kỹ thuật tái dùng được

**a) Verify một bài tổng quan bằng ĐẾM CỤM TỪ trên full text, không bằng đọc lướt.** Khi ai đó nói "bài tổng quan X nói có nghiên cứu đo chỉ tiêu Y", chuỗi đúng là:
1. `EXT_ID:<PMID> AND SRC:MED` để chắc bài **tồn tại** (hitCount = 1).
2. Lấy `resultType=core` để có **PMCID**.
3. `https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML` → strip tag → **`re.finditer` đếm từng cụm từ** của chỉ tiêu cần (`"fecal IgA"`, `"sIgA"`, `"secretory"`) **cộng một cụm đối chứng rộng** (`fecal`) để biết bài có nói về ruột/phân không.
4. Kết luận chỉ được phép ở dạng: *"bài KHÔNG BÁO CÁO chỉ tiêu X"*. **Không** được nâng thành *"29 nghiên cứu gốc không bài nào đo X"* — muốn nói câu đó phải mở 29 bộ dữ liệu gốc.

**b) Đếm cụm từ rẻ hơn và chắc hơn đọc abstract** — abstract nhiều bài không nêu chỉ tiêu miễn dịch nhưng full text thì có, và ngược lại (từ khoá xuất hiện trong phần phương pháp, không phải kết quả).

**c) Chỉ tiêu thay thế phải gọi ĐÚNG TÊN.** Các bài heo + Bacillus còn lại đo: tế bào SIgA+ mảng Peyer (`30809953`), sIgA niêm mạc ruột non (`38451226`), sIgA khí quản/phổi/ruột (`33756379`, liên quan cả **cửa E**), tế bào IgA tiết hỗng tràng + microarray (`31528339`), sIgA hỗng tràng/kết tràng (`36548829`), tế bào sinh IgA (`22901748` — chỉ khi **phối hợp** *L. salivarius*), biểu hiện gen sIgA + MUC2 ở nái (`41976011`), IgA huyết thanh/non sữa đầu (`38998090` — mức 4). Loài khác: gà `40913980` (biểu hiện gen sIgA + FCR +7,9%) · `42035530` (sIgA hồi tràng) · chuột `40689169` · `42287552` (chỉ **mô tả**) · `39470280` (surfactin — **hoạt chất**, không phải tế bào *B. subtilis*) · người `40826150` (**sIgA phân GIẢM 24,24%**, P=0,0433 — **ngược chiều** với heo).

## 7. Bẫy đã dính

1. **Hit trong truy vấn chủ đề ≠ nghiên cứu đo chỉ tiêu đó.** `31282365` khớp truy vấn "fecal sIgA + Bacillus" và có chữ "phân", nhưng đó là **IgA đặc hiệu PEDV do VẮC-XIN** → mức 2, **không** được tính cho Bacillus. Đã ghi cảnh báo trong cả `.md` và `.json`.
2. **Chiều tác động mâu thuẫn giữa loài:** Bacillus **tăng** IgA phân ở heo (`17760301`) nhưng **giảm** 24,24% ở người (`40826150`). Đây là câu hỏi bằng chứng, **không** được suy từ cơ chế sang kết luận — đã ghi vào "Việc còn nợ", không chốt chiều.
3. **Liều không có trong abstract thì ghi `chua_co_nguon`**, không suy ra từ chủng hay từ bài khác (12 PMID phải ghi `chua_co_nguon`).
4. **Đối chứng kỹ thuật đáng giá:** `39528052` (*Akkermansia*, **không phải Bacillus**) đo **SIgA phân trên heo con với đơn vị định lượng µg/mg** (7,59 µg/mg, P=0,002) — chứng minh phép đo khả thi và có chuẩn. Ghi rõ trong bảng là **không phải Bacillus** để không bị đọc nhầm thành bằng chứng cho Bacillus.

## 8. Số chốt

- **23/23 PMID verify** bằng `EXT_ID:<PMID> AND SRC:MED`, `hitCount = 1`.
- Trong 23 bài: **5 bài có `do_iga_tiet_trong_phan = true`** (3 heo + 1 người + 1 đối chứng *Akkermansia*).
- Báo cáo 119 dòng · bảng Markdown 4 nhóm (A heo-đo-phân / B heo-chỉ-thay-thế / C loài khác / D tổng quan) · **0 bảng HTML**.
- Quy ước đặt tên tầng này: `no-<NN>-<chủ-đề>.md` + `.json` cùng tên trong `docs/14-cong-thuc-co-ban/`.
