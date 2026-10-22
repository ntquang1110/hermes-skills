# Bản đồ TƯƠNG KỴ HOÁ LÝ lô 1 — premix TĂCN heo (`docs/14`)

Chốt 20/10/2026. Deliverable: `docs/14-cong-thuc-co-ban/batch-lo-1-tuong-ky.md` (94 KB) +
`batch-lo-1-tuong-ky.json` (77 KB). Anh em trong cùng thư mục (05 khung · 06 chốt · engine-cong-thuc.py ·
`_verified.json`) do subagent khác viết — **chỉ đọc, không đè**.

Lớp này là **CHẤT × CHẤT trong một bao premix** — khác hẳn lớp chất × 8 chặng (pitfall 37: cặp tương tác
trong premix) và khác lớp hoạt chất × cửa (`docs/12`). Ở đây câu hỏi là: trộn chung một bao thì cái gì
phá cái gì, bằng phản ứng hoá học nào.

**→ Anh em của file này: LÔ B — `references/ban-do-tuong-ky-premix-lo-B.md`** (chốt cùng 20/10/2026).
Cùng tầng "trong một bao premix" nhưng ở mức **NHÓM CHỨC NĂNG** (17 nhóm N1–N17, 133 cặp) và câu hỏi lõi
là **TÁCH BAO MẤY GÓI**: kết luận 6 gói cho bộ đầy đủ, thang biến thể 3/4/6/7/8, 17 cặp "tuyệt đối không
nằm chung", bank 20 PMID then chốt. Schema Lô B là **khoá tiếng Việt** (`nhom_a`·`nhom_b`·`co_che`·`muc_do`·
`muc_bang_chung`·`cach_xu_ly`·`pmid` + `pmid_vai_tro` + `pmid_la_bang_chung_cua_cap`) — **khác hẳn schema
Lô 1**, nên `scripts/qc-tuong-ky.py` (viết cho Lô 1) KHÔNG đọc được file Lô B: kiểm bằng đoạn kiểm riêng.

**Luật honesty bổ sung từ Lô B:** khi đề bài cấm gán PMID cho khẳng định chỉ là suy luận, đừng bỏ PMID
tiền đề đi — **giữ nhưng gắn `pmid_vai_tro = "tien_de"`** và hiển thị 3 nhãn phân biệt (trực tiếp /
tiền đề published / chỉ là tiền đề hoá lý). PMID nằm trần cạnh một câu suy luận hoá lý là lỗi bị bắt.



**Luật sinh file (áp cho cả hai lô):** ghi nội dung lớn thành **7–8 chunk nhỏ 8–18 KB** (mỗi chunk
`write_file` validate ngay), rồi một **renderer nhỏ** đọc chunk → ghi `.json` final **và** render `.md`
từ chính `.json` đó (JSON = nguồn duy nhất, hai file không thể lệch). Viết một phát 85 KB bị **cắt nội
dung + bỏ dấu tiếng Việt** mà vẫn báo `success`. Renderer phải lọc **cặp đã có trong bảng mức độ thì bỏ
khỏi bảng "tương thích"** (lượt này 5 cặp bị cả hai bảng nói ngược nhau). **Đừng `rm` renderer trước khi
chốt deliverable** — lượt này xoá sớm rồi phải viết lại từ JSON để sửa nhãn. Sau khi render: tự kiểm bằng
code (đủ 7 khoá/cặp, enum `muc_do`/`muc_bang_chung`, `ket_luan_dong_goi` đủ 3 khoá, `pmid_verify` toàn
`hitCount==1 && pmid_khop`), và `ls` file deliverable. `read_file` vẫn báo **binary** cho `.md` 190 KB
sinh trong repo này (đúng pitfall 1) — file sạch, đọc bằng python/`sed` theo dải dòng.

## Điều kiện nền (bắt buộc phản ánh trong ô `co_che`)

- Tất cả trộn chung **một bao premix khoáng–vitamin**, sau đó trộn vào cám **5 kg/tấn**.
- Cám viên có thể qua **hơi nước 70–90 °C trong 30–60 giây** (pelleting/conditioning).
- Premix có độ ẩm, hút ẩm; **pH của bao trôi theo acid** đang có.
- Một số chất phải qua **dạ dày heo pH 2–4** mới tới đích.

## Schema (khoá tiếng Anh cố định — KHÔNG đổi tên, KHÔNG thêm khoá)

Mỗi phần tử `cap_tuong_ky[]`:

| Khoá | Giá trị |
|---|---|
| `cap` | `["chất A", "chất B"]` — luôn đúng 2 phần tử |
| `nen_tang` | `cung_premix` \| `cung_cam` \| `cung_nuoc_uong` \| `nhiet_ep_vien` |
| `trang_thai` | `ky_manh` \| `ky_nhe` \| `trung_tinh` \| `tuong_thich` \| `hiep_luc` |
| `co_che` | phản ứng cụ thể: `2 HCOOH + CaCO3 -> Ca(HCOO)2 + CO2 + H2O` |
| `hau_qua` | hệ quả định lượng nếu có (số phải nằm trong abstract của PMID được trích) |
| `xu_ly` | cách xử lý khi trộn: tách gói · bọc lipid · đổi sang muối/diformate · đổi thời điểm · giảm liều · đổi tá dược |
| `pmid` | bằng chứng **cho chính cặp đó** |
| `muc_bang_chung` | `in_vivo_heo` \| `in_vivo_loai_khac` \| `in_vitro` \| `chua_co_nguon` |
| `tag_H` | `chua_co_nguon_cho_cap_nay`, `nguon_nen_<pmid>` |

Top-level: `{"cau_truc": {...điều kiện nền...}, "cap_tuong_ky": [...], "nguon": {...}}`.
`nguon` giữ: `phuong_phap_verify`, `so_pmid_verify_duoc`, `pmid_da_dung`, `so_pmid_nguon_nen`,
`pmid_nguon_nen`, `so_pmid_verify_tong`, `so_cap`, `thong_ke_muc_bang_chung`, `ghi_chu`.

## 4 quy ước honesty đã chốt (dùng lại cho lô 2)

1. **Cặp chưa có nguồn** → `pmid=[]`, `muc_bang_chung="chua_co_nguon"`, tag `chua_co_nguon_cho_cap_nay`,
   và **vẫn phải viết cơ chế hoá học** (pKa, Ksp, độ tan, liên kết hydro/kỵ nước, bề mặt hấp phụ) + nói
   thẳng "đây là suy luận hoá học, không phải bằng chứng". Đây là giá trị lớn nhất của lớp này.
2. **PMID chỉ là nguồn NỀN** (bài nói về chất, không thử cặp) → tag `nguon_nen_<pmid>`,
   **không để PMID nằm trần trong câu chữ**. Audit lấy haystack từ `pmid` + `nguon_nen_*`; bỏ bước này
   sinh cờ giả hàng loạt (đã xảy ra: 36 cờ → 0 sau khi bơm nền vào tag).
3. Số trong `hau_qua`/`xu_ly` phải nằm trong `abstractText` của **chính** PMID được trích.
   p-value bị Europe PMC cắt (chuỗi kết thúc bằng `(p`) → **không trích số**, viết "có ý nghĩa thống kê theo bài".
4. `.md` có **Phụ lục A** (kết quả verify) + **Phụ lục B** (giới hạn: khai thẳng bao nhiêu cặp chưa có nguồn,
   bao nhiêu nguồn là loài khác/in vitro). Nhóm K (sát trùng đường nước) chỉ để so sánh, ghi rõ **không trộn vào cám**.

## Số chốt 20/10/2026

- **58 cặp** · 33 PMID bằng chứng (**14 `in_vivo_heo`** / 7 `in_vitro` / 5 `in_vivo_loai_khac`) ·
  14 PMID nguồn nền → **47 PMID verify 47/47** (Europe PMC `hitCount==1` + `pmid` khớp).
- **32 cặp `chua_co_nguon`** (khai thẳng, không độn nguồn).
- 58/58 tiêu đề `## A × B` · 58/58 đủ 4 ô bắt buộc · 0 giá trị số không khớp abstract.
- Dùng đủ 4 `nen_tang` và đủ 5 `trang_thai`.

## Bank số đã verify (lấy lại được cho lô 2 / trang HTML)

| PMID | Số dùng được |
|---|---|
| 42462087 | heo con cai sữa; giảm ABC 40–50 meq/kg bằng acidifier **không đủ** hạ ABC/pH dạ dày; ABC-4 = 256–300 (pha 1) / 194–220 / 129–176 meq/kg; liều 0.30–0.50% lactic-formic |
| 42824833 | định nghĩa ABC-3 / ABC-4 (pH 3.0 / 4.0) |
| 41727420 | 45 mẫu nước: độ cứng 142–1,181 mg CaCO3/L (TB 441.2), pH 7.42–8.47; chuẩn độ về pH 5.0 và 4.0 ± 0.05 |
| 41515164 | sinh khả dụng kẽm 42% / 24% / 27% tuỳ dạng; tỉ lệ phytate:Zn 2:100 → 4:100 |
| 42602773 | 1152 heo con (6.72 ± 0.63 kg, 21 ngày); ZnO cơ học hoá 400 mg Zn/kg ≈ ZnO thường 1600 mg Zn/kg |
| 41923320 | 360 heo (5.90 ± 0.03 kg), 38 ngày, khẩu phần ABC-4 thấp + pZnO 500/800 rồi 300/500 mg/kg |
| 42353498 | 45 heo con Meishan: 60 mg/kg Cu_Gly + 10 g/kg KDF (kali diformat) |
| 42000567 | vi nang thymol + carvacrol + 4 acid (citric/fumaric/malic/phosphoric); 200/400/800 mg/kg trên 120 heo con 21 ± 3 ngày (5.34 ± 0.74 kg) |
| 42571401 | 210 heo 21 ngày; benzoic acid bọc phóng thích chậm 0.25%; 42 ngày |
| 41096511 / 42359391 | 24 heo con cai sữa; K-diformat 0.6 / 1.2 / 1.8%; 28 ngày |
| 34608725 | xà phòng canxi MCFA: E. coli còn **< 1/3**, C. jejuni **1/5**, phân bê giảm một nửa |
| 42553629 | 180 heo con (24 ± 1 ngày), 42 ngày; hỗn hợp monoglyceride 600/1,000/1,400 mg/kg, tốt nhất 1,000 |
| 41301971 | 18 heo con (7.54 ± 0.86 kg); GML 1,000 mg/kg; LPS ngày 21, đo ở 4 h |
| 41096437 | tributyrin 0.2%; heo con 21 ngày; 28 ngày thí nghiệm |
| 42399933 | IgY 6 g/kg; 24 heo con 17 ngày (4.63 ± 0.39 kg); 11 ngày; thử thách E. coli K88 |
| 40961760 | vi nang IgY: hiệu suất bao 94.16%; β-CyD +3.5% so với alginate |
| 42662228 | 36 heo con cai sữa 21 ngày; tannin chestnut 0.75% và quebracho 0.5%; 4 tuần; tiêu chảy 41.7% → 25% → 0%; cả hai đều hạn chế tăng trọng |
| 32349238 | 144 heo con 28 ngày (7.81 ± 0.99 kg); ZnO 2000 mg/kg pha 1 rồi 137.5; tannin thuỷ phân 1,000 mg/kg ngày 1–28 |
| 42327680 | berberine trên biochar-montmorillonite: dung lượng cực đại **231.60 mg/g**, pH tối ưu 5–7, giữ 76.99% sau 5 chu kỳ |
| 42791726 | palmatine–montmorillonite intercalate 0.02%/0.5%/1.5%; 30 heo con (15.12 ± 2.95 kg); 1.5% giảm ảnh hưởng ETEC |
| 41244632 | MMT + tinh dầu Satureja montana: EC50 0.011 mg/mL (Daphnia), ức chế tảo ≥0.021, an toàn <0.007 mg/mL |
| 42765101 | vi nang OEO: hiệu suất bao 84.2%, hạt 151 μm; 3,600 gà thịt; 80/120/160 mg/kg; 42 ngày |
| 42797933 | TOA-EO 0.75/1.5 g/kg trên 360 Ross 308 |
| 42531847 | carvacrol 50% ở 1,100 và 2,200 g/tấn; thymol 45% ở 250 g/tấn; 1,200 con |
| 42335775 | protease mất hoạt lực khi ép viên: thấp 46.6% / trung bình 29.2% / cao 12.5% |
| 41484313 | lanthanum carbonate 45 mg/kg/ngày; 10 heo con 7 ngày tuổi; 1 tuần trước mổ + 4 tuần sau; canxi giảm (p=0.009), xương/khối lượng không đổi |
| 32087732 | cam thảo (glycyrrhizin) × berberine: AUC cửa gan 425.8 → 270.4 ng.h/mL; gan 29,500.8 → 15,422.4 |
| 42816880 | 108 heo; chitosan oligosaccharide 100 mg/kg; thử thách EHEC O157:H7 |
| 42451595 | bentonite biến tính chitosan hấp phụ anion; R² > 0.99004 |
| 40242779 | kieselguhr an toàn **5000 mg/kg** thức ăn hoàn chỉnh; cần **15,000 mg/kg** để đủ hiệu lực chống vón |
| 42784191 | humate làm chất ổn định hạt nano ZnO (HA-ZnO) |
| 41180245 | humate 300 mg/kg + chiết Yucca 100 mg/kg; 240 gà; 42 ngày; FCR 1.50 vs 1.66; E. coli 5.3 → ~2.0 log; LAB +1.2–2.3 log |
| 42121774 | Yucca YSE (10.8% saponin) 0/150/300 mg/kg; 40 heo vỗ béo; 42 ngày; NH3-N manh tràng giảm (p=0.015) |
| 42738434 | phân tích gộp 39 thí nghiệm / 73 nghiệm thức về khoáng sét |
| 37068353 | palygorskite (attapulgite) 0–2,000 mg/kg; 320 gà; tốt nhất 1,000 mg/kg |
| 41721436 | 200 heo (55.40 ± 3.36 kg); silicate 0.1% |
| 42041352 | Bacillus subtilis 10^7 CFU/ngày × 21 ngày |
| 42511002 | SAEW 0.3 và 0.6 mg/L; 15 ngày liên tục; 144 heo con cai sữa (0.3 tốt nhất) |
| 41806649 | vi nang acid citric (PEG-CA) + NaClO2 nhả ClO2 theo nhiệt; 88.13% (ethylene); kéo dài 2 lần ở 25 °C |
| 41970919 | chlorite trong vi sợi PVA nhả ClO2 theo pH; phản ứng phụ với nền làm cạn chlorite |
| 41820557 | acid amin (L-lysine/L-arginine) + Ca-montmorillonite, hỗn hợp 1:40 — đối kháng tạo "nano-environment" |
| 42797950 | baicalin tới 80 μg/mL (mô hình PRRSV trên heo) |
| 42105244 | scFOS 0.15%/0.33% cho nái rồi 0.10%/0.15% — protein sữa non, IgG, TGF-β1 |

## 6 luật trộn premix rút ra (nguyên văn ở cuối file `.md`)

1. **Acid tự do phải ở gói riêng** — nó chỉ tồn tại nếu không gặp carbonat/oxide/humate/bề mặt sét.
2. **Hơi nước 70–90 °C là cửa ải giết 4 nhóm**: tinh dầu bay hơi, vỏ bọc lipid của butyrate,
   enzyme/protease, peptide ngắn (Gly-Gln). Cách sống: **bọc** hoặc **trộn sau ép viên**.
3. **Chất hấp phụ hút cả hoạt chất, không chỉ độc tố** — hoặc tách gói, hoặc biến sét thành hệ mang có chủ đích.
4. **Kim loại là dao hai lưỡi** — liều thấp, dạng hữu cơ/cơ học hoá, không để chung gói với enzyme/men vi sinh/tanin/sét.
5. **pH của bao là tham số thiết kế** — khoanh pH bao quanh 4–5; đổi acid phải kiểm lại các cặp phụ thuộc pH.
6. **Tách ba dòng: bao premix – cám – nước uống** — acid hữu cơ không được ở cùng dòng nước với ClO2/PPMS/SAEW.

## 3 phát hiện đáng nhớ

1. Bột đá trong cám **thắng** acid tự do: giảm ABC 40–50 meq/kg vẫn không hạ được pH dạ dày (42462087).
2. Chỉ số sống sót qua ép viên là **hiệu suất bao vi nang**, không phải liều: EE 84.2% + hạt 151 μm (42765101).
3. Cùng một chất hấp phụ vừa là thảm hoạ vừa là kỹ thuật: berberine bị MMT giữ 231.60 mg/g (42327680),
   nhưng intercalate palmatine–MMT ở 1.5% lại có lợi trên heo (42791726).

## Cách dựng lại / kiểm

```bash
python scripts/qc-tuong-ky.py "D:/Hermes Proj/fixgby/docs/14-cong-thuc-co-ban/batch-lo-1-tuong-ky.json"
```
Cổng 1: verify mọi PMID trong `pmid` + `tag_H(nguon_nen_*)`. Cổng 2: so **giá trị số** (không so cụm
số + đơn vị) với `abstractText`. Kỳ vọng lô 1: `PMID 47/47` · `NUM_MISS 0`.
Nhắc lại luật sinh file: generator chia phần a/b/c, `ls` file deliverable sau khi chạy, script tạm để ở `%TEMP%`.
