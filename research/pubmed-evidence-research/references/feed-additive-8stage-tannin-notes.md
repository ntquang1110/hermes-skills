# Tannin trong premix heo — ngân hàng 8 chặng (lô A `10-cong-thuc-23`, 19/10/2026)

Hai nguyên liệu: **Tannin Chestnut** (*Castanea sativa*, tannin THUỶ PHÂN / ellagitannin+gallotannin) và
**Tannin Quebracho** (*Schinopsis lorentzii*, tannin NGƯNG TỤ / proanthocyanidin).
Deliverable: `src/tannin-chestnut.txt` (66 dòng) + `src/tannin-quebracho.txt` (65 dòng).
**32 PMID trích dẫn, verify 32/32 tồn tại thật qua Europe PMC.**

## Luận điểm trung tâm — tannin thuộc lớp chất KHÔNG HẤP THU

Đây là ca thứ hai (sau enzyme/probiotic) của lớp "chất không hấp thu" trong khung 8 chặng. Cách viết
đúng cho cả 8 chặng:

| Chặng | Cách ghi cho tannin |
|---|---|
| 1 `cua_vao` | MIỆNG/RUỘT (theo thức ăn). Phân tử gốc **KHÔNG qua gan lần đầu** vì không hấp thu được |
| 2 `qua_hang_rao` | **KHÔNG** dùng protein vận chuyển để đi qua — nhưng tannin **ĐỔI** hàng rào vận chuyển của ruột (xem dưới) |
| 3 `gan_lan_dau` | **KHÔNG có CYP pha I** cho phân tử gốc. Chỉ phần aglycon nhỏ bị methyl hoá (COMT-like) |
| 4 `gan_de_di` | Chỉ **chất chuyển hoá nhỏ** mới bị liên hợp pha II (methyl/glucuronid/sulfat). Protein chở trong máu = **tag H** |
| 5 `toi_mo` | **NIÊM MẠC RUỘT NON + LÒNG RUỘT + VI SINH ĐẠI TRÀNG.** Không có thụ thể đặc hiệu |
| 6 `ra_khoi_te_bao` | Không phải cơ chất ABC (tag H). **Không có bằng chứng ỨC CHẾ P-gp/BCRP trên heo** — đừng suy từ polyphenol nói chung |
| 7 `thai` | **PHÂN là cửa chính** (phức tannin-protein). Sữa/tỷ lệ % ở heo = **tag H** |
| 8 `o_lai` | t½ phân tử gốc **KHÔNG ÁP DỤNG**. Số định lượng phải mượn người (15369737) / chuột cống (19625746) |

**Ba bằng chứng trụ cho "không hấp thu":**

1. `27646690` — mức hấp thu tannin **tỷ lệ NGHỊCH với mức polymer hoá** (tổng quan, không đơn vị).
2. `9783826` — tannin kết tủa **protein nước bọt giàu proline (PRP)** tạo phức **KHÔNG TAN**, bền vững
   dưới điều kiện mô phỏng dạ dày **và** ruột non ⇒ không có đường vận chuyển nào qua màng.
   *Loài: protein NGƯỜI (in-vitro).*
3. `7575474` — **histatin 5 là chất kết tủa tannin ngưng tụ quebracho mạnh nhất ở pH 7,4 và cả pH 3,0**;
   histatin 5 còn **bảo vệ alpha-amylase khỏi bị tannin ức chế**. *Mô: protein NƯỚC BỌT người in-vitro.*
   ⚠️ Đây là nguồn **quebracho-specific** duy nhất về liên kết protein — dùng nó, nhưng **cấm** gọi nó là
   "protein chở trong máu".

**Cơ chế kết tủa (dùng cho `bat_kha`):** `8729465` — kết tủa 2 bước (tạo phức trước, kết tủa sau);
hiệu lực theo số nhóm galloyl: penta- > tetra- > tri- >> di- >> mono- (HPLC, BSA tinh khiết).
`17474755` — hằng số liên kết ellagitannin hạt dẻ: **gelatin ~2×10⁶ M⁻¹ vs BSA ~8×10² M⁻¹** (chênh 3–4 bậc)
⇒ tannin chọn protein Sợi/giàu proline, không gắn albumin mạnh. Đây là lý do số "gắn albumin" **không**
được dùng làm lập luận hấp thu.

## Nguồn TRÊN HEO (hạng A — ưu tiên, đây là bằng chứng chính)

| PMID | Nội dung thật | Mô |
|---|---|---|
| `29799865` | 1 % chiết xuất hạt dẻ (chứa **54 % tannin thuỷ phân**) giảm điểm phân, tỷ lệ + số ngày tiêu chảy sau lây ETEC F4; 72 heo con 26 ngày (7,4 ± 1,5 kg); P<0,05 | Ruột + phân heo con (Swiss Large White) |
| `32106264` | 2 % chiết xuất hạt dẻ giảm độ nặng tiêu chảy + lượng ETEC F4 thải phân; **tương tác ÂM có ý nghĩa với sodium salicylate (P<0,05) làm TĂNG thải ETEC** | Phân + ruột heo con |
| `33105748` | Tổ hợp hạt dẻ + quebracho **1,25 %** ở heo con 28±2 ngày: giảm nhẹ tiêu hoá chất khô in vitro nhưng **KHÔNG hại ăn vào/tăng trọng**; 120 con | Ruột + phân heo con |
| `32255185` | Tannic acid **vi bao 1.000 mg/kg**: TĂNG SLC6A19 + SLC15A1/PEPT1 ở **hồi tràng**, GIẢM SLC5A1/SGLT1 ở **hỗng tràng** (P<0,05); **ức chế hoạt tính maltase hồi tràng**; đổi thành phần vi khuẩn đại tràng | Hồi tràng + hỗng tràng + đại tràng heo con |
| `32884745` | Tannic acid 0,2 % và 1,0 %: TĂNG occludin (tá tràng/hỗng tràng/hồi tràng), giảm crypt depth, **giảm DAO và D-lactate huyết thanh**; 108 heo con 6,60 ± 0,27 kg | Niêm mạc ruột non + huyết thanh heo con |
| `32349238` | Tannin thuỷ phân 1.000 mg/kg tăng chiều cao nhung mao hỗng tràng + tăng hoạt tính **trypsin, lipase**; 144 heo con 28 ngày (7,81 ± 0,99 kg) | Ruột non heo con |
| `35204135` | Acid ellagic 0,005–0,02 % ở heo con cai sữa: trục **Nrf2→HO-1/NQO1** (đây là "con đường tín hiệu", KHÔNG phải thụ thể) | Niêm mạc ruột non heo con |
| `31979207` | Tiêu hoá in-vitro chiết xuất hạt dẻ + quebracho: ức chế **E. coli F4+ và F18+** tới **1.200 µg/mL**, giữ hoạt tính sau tiêu hoá mô phỏng; bảo vệ IPEC-J2 khỏi H2O2/DSS | Dòng tế bào biểu mô ruột **HEO** IPEC-J2 + vi khuẩn |
| `24810761` | Tannin ngưng tụ phá huỷ **lớp vỏ + mô tiêu hoá** của ấu trùng *Ascaris suum* thu từ **heo** | Ấu trùng A. suum từ heo (in-vitro) |

**Điểm mạnh hiếm có:** tannin là một trong số ít nguyên liệu premix có **bằng chứng heo in-vivo dày**
(6 PMID heo in-vivo), không phải suy từ chuột. Vì vậy cả 2 file chốt `MUC: A`.

## Nguồn loài KHÁC — dùng được nhưng PHẢI ghi rõ loài ở cột "mô & loài"

| PMID | Loài / mô THẬT | Dùng cho |
|---|---|---|
| `15369737` | **NGƯỜI** — huyết tương: acid ellagic (từ 318 mg ellagitannin trong 180 mL nước lựu) Cmax **31,9 ng/mL** sau **1 h**, hết ở **4 h** | Chặng 7/8 (số định lượng duy nhất có) |
| `19625746` | **CHUỘT CỐNG** — huyết tương + não: acid gallic, catechin, epicatechin bị **methyl hoá** (4-O-methylgallic acid, 3′-methylcatechin, 3′-methylepicatechin); **AUC 0–8 h tăng 198 % / 253 % / 282 % khi dùng lặp lại** so với một liều | Chặng 3/4/8 |
| `23781257`, `35118817` | **NGƯỜI** — urolithin (vi sinh đại tràng chuyển hoá acid ellagic) lưu hành dạng liên hợp **glucuronid/sulfat 0,2–20 µM**; **ĐÃ PHÁT HIỆN TRONG SỮA MẸ NGƯỜI** ⇒ cửa sữa có cơ sở gián tiếp | Chặng 7 (cửa sữa) |
| `17468433` | **BÒ** — quebracho 0–2 % DM (chiết xuất **91 % tannin ngưng tụ**): tiêu hoá biểu kiến protein thô giảm **TUYẾN TÍNH 5 % và 15 %**; KHÔNG đổi tăng trọng/lượng ăn; 3 giai đoạn × 28 ngày | Chặng 7 (% thải gián tiếp) + `da_that_bai`-style |
| `34828048` | **GIA SÚC NHAI LẠI** (meta-analysis 70 bài / 348 nghiệm thức): protein thoát dạ cỏ **không hấp thu tốt ở ruột non → thải trực tiếp vào PHÂN** | Chặng 7 |
| `22740383` | **DỊCH DẠ CỎ BÒ** in-vitro: quebracho ≥100 g/kg DM giảm methane tới **~40 %** | "tác động lên VI SINH đường tiêu hoá" |
| `25434333` | **CỪU SỮA** — tannin hạt dẻ + quebracho KHÔNG đổi năng suất/thành phần sữa, **nhưng nghiên cứu KHÔNG đo dư lượng tannin trong sữa** ⇒ **không** được kết luận "không tồn lưu" | Chặng 7 — viết thẳng là không đo được |
| `35061675` | **GÀ THỊT** — tổ hợp hạt dẻ + quebracho: cải thiện sức khoẻ ruột, đổi hệ vi sinh manh tràng | Chỉ tham chiếu |
| `20173064`, `9758806` | **CỪU / dạ cỏ nhai lại** — đổi cộng đồng vi khuẩn + protozoa; vi khuẩn chịu tannin phân lập từ **RUMEN** cừu/hươu | **9758806 đã bị LOẠI** khỏi deliverable (sinh thái dạ cỏ ≠ vi sinh ruột heo) |
| `15113710`, `19636448`, `35740109` | Tổng quan (người/mô hình) — liên hợp pha II; vi sinh đại tràng mở vòng flavonoid thành acid phenylpropionic/phenylacetic | Chặng 3/4 |
| `28441731` | **Invitro enzyme tiêu hoá tinh khiết** — polyphenol liên kết không cộng hoá, **ức chế KHÔNG cạnh tranh** alpha-glycosidase, alpha-amylase, lipase, pepsin, trypsin, chymotrypsin | Chặng 2 + tương tác |
| `9838798` | Tổng quan hoá học — polyphenol từ đơn phân tử tới polymer hoá cao, MW tới **> 30.000 Da** | `CONG_THUC` |

## Nguồn đã LOẠI khỏi deliverable (audit mô/loài)

- **`23533692`** — *"Sweet chestnut (Castanea sativa Mill.) bark extract: cardiovascular activity and myocyte protection"*:
  **mô = CƠ TIM / tế bào cơ tim** ⇒ loại, không dùng cho phát biểu về ruột (dù tên "chestnut" rất hấp dẫn).
- **`9758806`** — vi khuẩn chịu tannin phân lập từ **RUMEN** nhai lại ⇒ loại khỏi chặng 5.
- **Nhóm truy vấn tannin + P-gp / ABCB1 / BCRP / MRP2** — mọi kết quả hữu ích đều là **tổng quan ung thư**
  hoặc đo trên **dòng tế bào UNG THƯ** ⇒ loại theo quy tắc audit; kết luận đúng là **tag H**, không phải
  "tannin ức chế P-gp".
- Nguồn lô C/lô khác của dự án đã mở abstract nhưng **không dùng** cho tannin (trùng lặp hoặc sai loài):
  `22794138`, `26861391`, `31156781`, `23107545`, `8297327`, `35083309`, `30060764`, `33610769`,
  `33066367`, `36230326`, `15998116`, `29847844`, `33042163`, `33525629`, `20480025`, `38800730`,
  `36500366`, `37371871`, `33440730`, `29028844`.

## Tương tác nội công thức — đã ghi vào `TUONG_TAC` của cả 2 file

1. **Tannin × thymol / carvacrol / berberine = CHƯA CÓ NGUỒN (tag H).** Không có nghiên cứu đo tổ hợp này
   trên heo. Ghi thẳng tag H — **không** suy từ "polyphenol nói chung".
2. **Nguy cơ có thật và đo được:** tannin ức chế **không cạnh tranh** enzyme tiêu hoá (`28441731`);
   tannic acid ức chế **maltase hồi tràng heo con in-vivo** (`32255185`); tannin quebracho kết tủa
   alpha-amylase (`7575474`) ⇒ có thể giảm tốc độ giải phóng mọi thành phần khác trong premix.
3. **Tương tác ÂM đã đo trên heo** (`32106264`, sodium salicylate × chestnut extract, P<0,05, tăng thải
   ETEC) — dùng làm câu chuẩn: *"phải tự kiểm tổ hợp thật trên lô 2 kg, không suy diễn"*.
4. **Cảnh báo khoáng:** polyphenol khoá hấp thu **sắt/kẽm** khi liều cao (`36985507`).
5. ⚠️ Lô A SKILL.md đã có sẵn mục "Tannin kết tủa protein/enzyme ⇒ nguy cơ giảm hấp thu chung" —
   bản này là bằng chứng đã đọc abstract cho mục đó (trước đây chỉ có `33105748`, `28004617`).

## Chỉ số đo được (`CHI_DAU_DO_DUOC`) — dùng lại cho lô sau

Điểm phân; tỷ lệ % + số ngày tiêu chảy; ETEC F4 thải phân (CFU/g); nồng độ ức chế E. coli F4+/F18+
(1.200 µg/mL); chiều cao nhung mao / crypt depth (tá–hỗng–hồi tràng); occludin & ZO-2 mRNA;
**hoạt tính maltase hồi tràng, trypsin, lipase**; **DAO + D-lactate huyết thanh**; thành phần vi khuẩn
đại tràng; tỷ lệ tiêu hoá chất khô in vitro; acid ellagic huyết tương (Cmax 31,9 ng/mL); urolithin niệu.

## `tag H` đã chốt cho tannin (đừng đi tìm lại)

CYP pha I; protein chở trong máu; bơm ABC đẩy tannin; thụ thể/kênh đích ở ruột; **cửa sữa heo nái**;
cửa phổi + da/mồ hôi; tỷ lệ % liều thải theo từng cửa ở heo; t½ và tích luỹ ở heo; tương tác trực tiếp
tannin–thymol/carvacrol/berberine.

## Rút ra cho lần chạy sau

- Ngân sách đọc **~6–8 PMID/chất là đủ** khi chất đã có cụm bằng chứng heo in-vivo; tannin ăn ~20 PMID/chất
  vì phải vừa dựng chặng vừa phủ định 4–5 tag H. **Ghi file ngay sau chất đầu tiên** — luật cũ vẫn đúng.
- Chất kết tủa protein luôn có **hai** hệ quả phải viết cùng nhau: (a) không hấp thu → đích ở lòng ruột;
  (b) gắn enzyme/hoạt chất khác → rủi ro **giảm hấp thu toàn công thức**. Viết (a) mà quên (b) là bản
  thiếu nghiêm trọng với một premix nhiều hoạt chất.
