# Recipe xác minh nguồn quản lý (regulatory source recipes)

Đã kiểm chứng 10/2026 (hồ sơ kim loại hiếm/đất hiếm cho người, `say-phun-kiem`). Chạy bằng `terminal` (`curl`) — không cần API key.

## 1. openFDA — nhãn thuốc (chỉ định, liều, đường dùng, số phê duyệt)

```bash
# theo HOẠT CHẤT (đáng tin nhất)
curl -s 'https://api.fda.gov/drug/label.json?search=openfda.generic_name:"CISPLATIN"&limit=2'
# theo BIỆT DƯỢC (hay trả rỗng — chỉ dùng để đối chiếu)
curl -s 'https://api.fda.gov/drug/label.json?search=openfda.brand_name:"RIDAURA"&limit=1'
# số NDA/ANDA + nhà SX
curl -s 'https://api.fda.gov/drug/drugsfda.json?search=openfda.brand_name:"FOSRENOL"&limit=3'
```

Các field cần lấy: `openfda.application_number` (NDA…/ANDA…), `openfda.brand_name`, `openfda.route`,
`openfda.manufacturer_name`, `indications_and_usage[0]`, `dosage_and_administration[0]`.

**Bẫy:**
- `brand_name` trả về `[]` (không lỗi) với thuốc đã ngừng bán → **thử `generic_name` trước khi kết luận**.
- Thuốc OTC theo monograph có `application_number` không phải NDA (vd bismuth subsalicylate: `M008` / `part335`) — ghi đúng bản chất, đừng gán thành NDA.
- Thuốc bị rút hoàn toàn → cả hai truy vấn rỗng. Ghi `number='' note='chưa verify'` cho số NDA gốc; đừng lấy số NDA từ trí nhớ.

**Nhãn gốc + approval letter:** `accessdata.fda.gov/drugsatfda_docs/label/<năm>/<số>s<seq>lbl.pdf` và
`accessdata.fda.gov/drugsatfda_docs/appletter/<năm>/<số>Orig1s<seq>ltr.pdf` — URL này xuất hiện trong kết quả
`web_search` và là **bằng chứng chính thức cho số NDA** khi openFDA không có hồ sơ (vd xác nhận `NDA 021759` = Eloxatin/oxaliplatin).

## 2. eCFR — danh mục phụ gia TĂCN (kết luận âm có căn cứ)

`21 CFR Part 573` = danh mục phụ gia thức ăn chăn nuôi của Mỹ. Lấy JSON/XML toàn phần của part rồi grep tên chất
(vd `lanthanum`, `cerium`) → không có kết quả = kết luận âm hợp lệ, ghi rõ part + ngày truy vấn.

## 3. EU — EFSA FEEDAP + Register of Feed Additives

Tên phụ gia đã được cấp phép ở EU là bằng chứng mạnh nhất cho nhóm TĂCN (vd `lanthanide citrate` = Lancer,
tối đa 250 mg/kg TĂ cho heo con cai sữa; EFSA FEEDAP 2016/2019; Quy định (EU) 2020/1370).
Trích theo **số Quy định (EU) + năm + số EFSA Journal**, không chỉ tên thương mại.

## 4. Tiêu chuẩn quốc gia — kiểm BẢN trước khi trích

- Việt Nam: `QCVN 8-2:2011/BYT` (kim loại nặng trong thực phẩm: As, Cd, Pb, Hg, Sn…) — **không có mục cho REE**.
- Trung Quốc: `GB 2762` — bản **2005/2012 có** giới hạn `稀土`, **2017 đã xoá**. Luôn mở bản PDF của đúng năm và đọc mục "主要变化" (thay đổi chính) để biết cái gì bị bỏ.
- Khi hai bản khác nhau: ghi **bản nào, năm nào**, và nếu hồ sơ cũ đã dùng bản cũ thì **đánh dấu đính chính**.

## 5. Nguồn dữ liệu khoáng sản / trữ lượng

`USGS Mineral Commodity Summaries` — `pubs.usgs.gov/periodicals/mcs<năm>/mcs<năm>-<commodity>.pdf`,
`web_extract` đọc trực tiếp PDF. Bảng "Salient Statistics" chứa reserves + mine production theo nước.
Số của các nước thường bị **điều chỉnh giữa các bản** → luôn lấy bản mới nhất và nêu năm bản.

## 6. Bảng số phê duyệt đã verify (dùng lại được, nhưng vẫn nên đối chiếu lại nếu trích chính thức)

| Chất | Số đã verify qua openFDA/accessdata |
|---|---|
| Lanthanum carbonate | Fosrenol NDA 021468 (+ NDA 204734 bột); generic ANDA206868 |
| Cisplatin | ANDA207323 (gốc Platinol NDA 018057) |
| Carboplatin | ANDA077861 / ANDA076517 / NDA219921 (KYXATA) |
| Oxaliplatin | **NDA 021759** (Eloxatin) |
| Auranofin | **NDA 018689** (Ridaura) |
| Lithium carbonate | ANDA090702 |
| Bismuth subsalicylate | OTC monograph `M008` / `part335` |
| Silver sulfadiazine 1% | **NDA 018810** (và NDA 018578) |
| Gadoterate meglumine | **NDA 204781** (Dotarem); generic ANDA210016 |
| Gadobutrol | ANDA215061 / ANDA219287 |
| Radium Ra-223 | **NDA 203971** (Xofigo) |
| Lu-177 dotatate | **NDA 208700** (Lutathera) |
| Lu-177 vipivotide tetraxetan | **NDA 215833** (Pluvicto) |
| Sodium zirconium cyclosilicate | **NDA 207078** (Lokelma) |

Chưa verify được (đừng trích như đã chắc): NDA của Gallium nitrate (Ganite, đã ngừng — truy vấn rỗng),
Arsenic trioxide (Trisenox — `generic_name` không trả kết quả), Sodium aurothiomalate (Myocrisin),
Cerium nitrate + SSD (Flammacerium — lưu hành ở châu Âu theo Burns 2005, **số giấy phép chưa verify**),
Nedaplatin/Heptaplatin/Lobaplatin (phê duyệt ở Nhật/Hàn/TQ — chưa verify PMDA/MFDS/NMPA).
