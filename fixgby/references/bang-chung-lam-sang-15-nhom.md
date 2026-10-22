# Phân tầng BẰNG CHỨNG LÂM SÀNG (L0–L4) — `docs/14-cong-thuc-co-ban`

Dựng 20/10/2026. Deliverable: `batch-lo-3-bang-chung-lam-sang.md` + `.json` — **15 nhóm hoạt chất**
(10 nhóm TIÊU CHẢY + 5 nhóm HÔ HẤP), tách 2 trục: bằng chứng theo **TỪNG CHẤT** và theo **NHÓM/BLEND**.
102 PMID verify Europe PMC **102/102**.

Đây là tài liệu trả lời câu hỏi *"nhóm nào đã chứng minh trên heo ở điều kiện nhiễm thật"* —
nó **khác** tầng `tag_H` của `docs/11` và **khác** `muc_bang_chung` của `docs/12` (xem mục "Quan hệ").

---

## 1. Thang bậc + QUY ƯỚC CHẤM (phần dễ tự lừa mình nhất)

| Mã | Định nghĩa |
|---|---|
| L0 | Chỉ có cơ chế suy luận/lý thuyết, chưa có thí nghiệm nào đo |
| L1 | In vitro (tế bào/vi khuẩn/mô hình mô) |
| L2 | In vivo trên HEO có GÂY NHIỄM (challenge study), dù ở phòng thí nghiệm |
| L3 | Thử nghiệm trên TRẠI THẬT, nhiễm tự nhiên, có nhóm đối chứng |
| L4 | Nhiều RCT ở nhiều trại, hoặc tổng quan hệ thống / meta-analysis |

**Lỗ hổng của thang bậc này — và cách vá đã chốt (phải ghi vào chính file deliverable, không chỉ nói miệng):**

1. **L2 chỉ tính khi có GÂY NHIỄM nhân tạo trên heo** (nêu chủng + liều + nhóm đối chứng).
2. Thang **thiếu bậc cho "in vivo trên heo nhưng KHÔNG gây nhiễm, KHÔNG đo chỉ số bệnh"** (rất nhiều thí nghiệm
   80–1.152 heo chỉ đo ADG/FCR/nhung mao). Chốt: **chấm L1 kèm ghi chú "in vivo heo, không gây nhiễm"** —
   vì claim đang xét là claim BỆNH. Tuyệt đối không nâng lên L2 cho "đã thử trên heo".
   Viết rõ trong file: *"nếu Quang muốn đọc theo câu hỏi 'đã thử trên heo chưa' thì các thí nghiệm đó vẫn là in vivo heo"*.
3. **L0 dùng 2 nghĩa, phải khai báo:** (a) chỉ có lý thuyết; (b) **KHÔNG TÌM THẤY** thí nghiệm nào trên
   đúng đối tượng/hỗn hợp đang xét (N3 blend, N13 từng chất, N14 hô hấp, N15 blend). Nghĩa (b) phải nêu
   trong `ket_luan_mot_dong` của chính entry.
4. **Bậc của NHÓM không được suy từ bậc của 1 CHẤT, và ngược lại.** Hai field `bac_cao_nhat_theo_tung_chat`
   / `bac_cao_nhat_theo_nhom_blend` là độc lập. Ca thật: **N3** = MOS L2 nhưng blend **L0** (chưa ai thử hỗn hợp
   oligosaccharide); **N5** = attapulgite có trại thật 1.890 heo/3 trại nhưng chỉ đo năng suất → bậc cho claim
   tiêu chảy vẫn **L2** (ZnO thách nhiễm ETEC), không được kéo lên L3.
5. **L3 = trại thật / trường hợp bệnh tự nhiên + đối chứng.** Nhiều bài "field" chỉ đo năng suất ⇒ ghi L3 nhưng
   phải nói rõ **"L3 chỉ về NĂNG SUẤT"** (attapulgite).
6. Chiều chỉ số và xu hướng: **FCR/F:G cao hơn = XẤU**; G:F/FCE cao hơn = tốt. `P = 0,06/0,08/0,10` = xu hướng.
   `40141053` viết *"higher average daily gain and feed conversion ratio"* — **mâu thuẫn nội tại, không dùng số FCR đó**.
   `16958792` FCR **+8% (P=0,01)** là **xấu đi**. `34368272` tác giả gọi "trends" nhưng P=0,03/0,04 → có ý nghĩa.

---

## 2. Kết quả chốt 15 nhóm (bank số)

| Mã | Nhóm | Bệnh | TỪNG CHẤT | BLEND | Gây nhiễm | Trại thật | Chất mạnh nhất |
|---|---|---|---|---|---|---|---|
| N1 | Acid hữu cơ chuỗi ngắn | tiêu chảy | **L3** | **L3** | có | có | formic ester hoá (37760214: 240 heo/3 trại, thải Salmonella 50%→20%, P<0,001); benzoic = L2 (ETEC F4) |
| N2 | Butyrate/MCFA/GML | tiêu chảy | **L2** | **L2** | có | không | tributyrin+GML vi nang (PEDV); Na-butyrate bọc MCFA (ETEC F4, 32108496) |
| N3 | MOS/GOS/scFOS | tiêu chảy | **L2** | **L0** | có | không | MOS (42217260: SIV + AFB1, 32 heo con) — **blend trắng** |
| N4 | Acid amin & dễ tiêu | tiêu chảy | **L2** | **L1** | có | không | L-glutamate 1% (ETEC F18, giảm thải β-hemolysin) |
| N5 | Khoáng & hấp phụ | tiêu chảy | **L2** | **L2** | có | có | ZnO/pZnO thách nhiễm ETEC (40061905, 40005874); attapulgite L3-chỉ-năng-suất (36288170) |
| N6 | Tanin chestnut/quebracho | tiêu chảy | **L3** | **L2** | có | có | **tanin hạt dẻ đơn chất** (39852918: 254 heo con, kháng sinh −84%, P=0,001) |
| N7 | IgY (K88) | tiêu chảy | **L2** | **L1** | có | không | IgY K88 6 g/kg (42399933, 24 heo con, thách nhiễm K88) |
| N8 | Men vi sinh | tiêu chảy | **L4** | **L2** | có | không | **Bacillus subtilis** (42450761: tổng quan hệ thống, 619 bản ghi → 29 nghiên cứu) |
| N9 | Thảo dược alkaloid/flavonoid | tiêu chảy | **L1** | **L3** | không | có | berberine+colistin **tiêm bắp** (42753344: 180 heo con tiêu chảy tự nhiên) |
| N10 | Đất hiếm | tiêu chảy | **L1** | **L1** | không | không | RECC 200 mg/kg (40141053) — kết quả MÂU THUẪN với 16958792 |
| N11 | Tinh dầu phenol/terpen | hô hấp | **L3** | **L3** | không | có | **carvacrol** (41946977: 324 heo, đàn lưu hành Mhp, có tổn thương phổi khi giết mổ) |
| N12 | Alkaloid/flavonoid chống viêm | hô hấp | **L2** | **L2** | có | có | baicalin (PRRSV); protoberberin-jatrorrhizine (Mhp, MIC 8–32 µg/mL, tương đương florfenicol) |
| N13 | Blend phytogenic+MCFA+probiotic | hô hấp | **L0** | **L2** | có | không | blend EP 0,4% — thách nhiễm kép PRRSV + *S. suis* (42211862) |
| N14 | Acid hữu cơ/khoáng trong cám cho hô hấp | hô hấp | **L0** | **L0** | (chỉ tiêu chảy) | có | acid benzoic — **chưa có 1 chỉ số hô hấp nào trên heo** |
| N15 | Chitosan | hô hấp | **L1** | **L0** | có | không | in vitro tế bào miễn dịch heo (42263574); mạnh nhất trên heo sống là tiêu hoá (EHEC) |

**Ba danh sách trả lời trực tiếp câu hỏi trung tâm:**
- **Trại thật + ĐÚNG chỉ số bệnh: chỉ 3 nhóm** — N1 (formic/Salmonella phân), N6 (tanin/dùng kháng sinh), N11 (carvacrol/tổn thương phổi).
- **Chỉ có bằng chứng ở dạng HỖN HỢP, không có cho từng chất: N13 (từng chất L0), N9 (đơn chất L1), N14 (L0).**
  Nửa vời: N1, N2, N5, N6 blend ≥ đơn chất. Ngược lại **N3 là nhóm duy nhất "đơn chất mạnh, blend trắng"**.
- **Chỉ có trên LOÀI KHÁC:** eucalyptol/1,8-cineole (người, 42547468) · limonene/pinene (không có trên heo) ·
  Scutellaria–*M. gallisepticum* (**gà**, 42083016) · baicalin–*P. multocida* + rhein–APP + berberine–APP
  (**chuột**, 41153980/38668646/42661110) · Akkermansia (**không có trên heo**) · 1-monolaurin (**không có trên heo**) ·
  acid rosmarinic (chỉ có thí nghiệm TIÊU HOÁ trên heo, 39967693).

---

## 3. Bẫy cơ học của lượt này

1. **Hai cache phải MERGE trước khi dig, không thì PMID in ra ở bước search lại "MISSING" khi dig.**
   `_search.py` (vòng 1) chỉ ghi `_hits.json`, `_search2.py` (vòng 2) ghi thẳng vào `_abs.json` ⇒ 10 PMID
   quan trọng nhất (B. subtilis systematic review, baicalin-PRRSV…) **vắng mặt** ở bước đọc. Luật: sau mọi vòng
   search phải merge vào **một** cache abstract, và hàm dig in sentinel `MISSING <pmid>` (phải = 0).
2. **Digest để tiết kiệm context: chỉ in câu CÓ CHỮ SỐ + 2 câu đầu (loài/mô hình).** 143 abstract vào cache,
   chỉ ~1,4 KB/nhóm ra màn hình. Đây là cách duy nhất giữ được trích dẫn chính xác mà không đốt context.
3. **Verify PMID trên **hợp** cuối cùng bằng 1 vòng `EXT_ID` lô-8, không verify từng nhóm rồi cộng**
   (đúng họ với SKILL.md pitfall 43). Lượt này: 108 dòng PMID / **102 PMID duy nhất** — 6 bài nằm ở 2 nhóm
   (33126524, 34237915, 40061905, 42462087, 42571401, 35924249).
4. **Script validate chạy TRƯỚC khi nộp, kiểm cả 5 nhóm điều:** (a) đủ 4 khoá top-level + đúng 16 field/entry;
   (b) `bac_*` ∈ L0..L4, `benh` ∈ {tieu_chay, ho_hap}, cờ ∈ {co, khong}; (c) `so_nghien_cuu_tim_duoc
   == len(pmid)`; (d) mọi pmid ∈ tập đã verify; (e) `muc_bang_chung` ∈ 4 giá trị cho phép.
   Bắt được lỗi lệch số đếm trước khi giao — không dựa vào mắt.
5. **Dọn file tạm: chỉ xoá file `_`-prefix của CHÍNH MÌNH.** Thư mục `docs/14` có subagent khác ghi song song
   (`06-tang-bang-chung.json`, `05-khung-cong-thuc-v1.md`, `engine-cong-thuc.py`, `_ket-qua-toi-uu.json`).
   `ls` trước khi `rm`; để nguyên `__pycache__` (có thể đang được process khác dùng).
6. **Europe PMC cắt ký hiệu p-value thành `(p`** — gặp lại ở lượt này; xem SKILL.md pitfall 42(a).
   Không đoán p-value, viết "có ý nghĩa thống kê theo bài" không kèm số.
7. **Không gán loài khi abstract không nêu.** `41966777` (Folium Isatidis/PCV2) và `39800034` (sanguinarine/PCV2)
   không nêu loài trong abstract đã đọc ⇒ ghi "chưa xác định loài", KHÔNG gán cho heo.
8. **Điều kiện miễn dịch phải đọc, không chỉ đọc chủng.** `35924249` (houttuynia) thử trên heo **đã tiêm vắc xin
   PRRSV-1** rồi thách nhiễm HP-PRRSV-2 ⇒ không được viết thành "chống PRRSV trên heo chưa tiêm phòng".

---

## 4. Khung file deliverable (bắt buộc, đã kiểm)

`.md` phải có **đủ 6 mục**: (1) thang bậc + quy ước chấm; (2) bảng 15 nhóm; (3) **trả lời 5 câu hỏi trung tâm,
mỗi câu 1 mục riêng** — bậc cao nhất là của CHẤT NÀO · nhóm nào chỉ có blend · nhóm nào có trại thật ·
nhóm nào chỉ có loài khác · nhóm nào chỉ có lý thuyết; (4) **"Ba khoảng trống lớn nhất"** — mỗi khoảng trống
phải nói đủ 3 ý: **thiếu cái gì · tại sao nó CHẶN quyết định · thử nghiệm nào bù được nhanh nhất (cỡ mẫu, chỉ số, thời gian)**;
(5) bẫy đã tránh; (6) phụ lục PMID theo nhóm + dòng `verified N/N`.

`.json`: 1 top-level object, 4 khoá `thang_bac` / `nhom` / `khoang_trong_lon_nhat` / `ghi_chu_bay`;
**không thêm khoá ngoài schema** (mọi quy ước phi tiêu chuẩn phải nhét vào text của field có sẵn).

## 5. Quan hệ với các tầng đã có (đừng lẫn)

- `docs/11` `tag_H` = *thiếu nguồn cho một CHẶNG cơ chế*. Tài liệu này = *bậc bằng chứng cho một CLAIM BỆNH*.
- `docs/12` `muc_bang_chung` = cấp cao nhất cho claim **trên heo** của từng hoạt chất (in_vitro / in_vivo_heo / …).
  Ở đây bậc L0–L4 là **thứ tự tin cậy theo thiết kế thí nghiệm** — L1 bao gồm cả `in_vivo_loai_khac`.
- `docs/14` batch này chấm theo **NHÓM hoạt chất**, không theo từng nguyên liệu của 26 premix.
