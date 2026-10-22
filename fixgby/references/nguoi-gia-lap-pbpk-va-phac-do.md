# Kho NGƯỜI — đường đi của chất trong cơ thể, giả lập, và phác đồ (chốt 21/10/2026)

Quang nói rõ: câu hỏi *"chất đi vào cơ thể thì điều gì xảy ra / track đường đi / đề xuất phác đồ"* là nói về **NGƯỜI**, không phải heo. Heo chỉ là bước đệm rẻ để rút cơ chế.

## 1. Kho dữ liệu: `docs/09-tra-cuu-duong-di/`

**Khung 8 chặng ADME** (khác hoàn toàn 8 chặng của bệnh heo):

`cua_vao → qua_hang_rao → gan_lan_dau → gan_de_di → toi_mo → ra_khoi_te_bao → thai → o_lai`

**15 chất / 3 batch** (kiểm trực tiếp 21/10/2026):

- **A** — ethanol · caffeine · glucose · fructose · natri/NaCl
- **B** — sắt (heme + non-heme) · canxi · curcumin · paracetamol · ibuprofen
- **C** — atorvastatin · metformin · omega-3 (EPA/DHA) · + 2 chất nữa

Số & cấu trúc:

- Mỗi ô = 1 sự kiện, có `pmid[]`; mức bằng chứng **(I) người / (A) động vật lớn / (R) chỉ in-vitro**, ưu tiên (I) rồi (A).
- Audit số: **117 ô có số, 111 khớp nguồn, 6 ô bị cờ** (`_num-report.json`).
- Hình dạng file **không đồng nhất** (cùng pitfall 18 của SKILL.md): batch A là dict có `khung` · `verified` · `doi_chieu_tieu_de_vs_phat_bieu`; batch C là **list** bản ghi với 8 khoá chặng + `bat_kha` · `da_that_bai` · `chi_dau_do_duoc` · `muc_bang_chung` · `tag_H` · `pmids`. Loader phải thử cả hai nhánh.
- Batch C đã có **trường máy đọc được** cho mô phỏng: `first_pass` (có/không) · `mo_dich` · `thu_the` · `bom` (P-gp/ABCB1…) · `chi_tiet`.
  Ví dụ atorvastatin: BA uống **14 %**; đích = **enzyme HMG-CoA reductase** (không phải GPCR); cơ chất **P-gp**, efflux ratio Caco-2 **39,32 → 10,99** khi thêm verapamil.

## 2. Thiếu gì để mô phỏng chạy được

Thiếu **số**, không thiếu khung. Cần bảng tham số cho mỗi chất — mỗi dòng kèm PMID + loài:

| Nhóm | Trường |
|---|---|
| Hấp thu | F % (sinh khả dụng) · Tmax · Cmax · % qua gan lần đầu |
| Phân bố | Vd · % gắn protein · cơ quan đích · có qua hàng rào não / nhau thai |
| Chuyển hoá | enzyme chính (CYP3A4, CYP2C9…) · pha I / pha II · chất chuyển hoá còn hoạt |
| Thải | t½ · CL · % thải theo thận / mật / hơi thở |
| Ra khỏi tế bào | bơm nào (P-gp, BCRP, MRP2) |

Hiện mới có **nửa định tính** (tới đó gõ vào cái gì — batch C đã có). Thiếu nửa định lượng.

## 3. Ba mức mô phỏng

**A — Định tuyến (deterministic, làm ngay).** chất + liều + đường dùng → in 8 chặng kèm số đã verify, cơ quan gánh, đích phân tử, nguồn. Không có gì để bịa vì mỗi dòng có PMID. Trả lời đúng câu "chất này vào cơ thể thì điều gì xảy ra".

**B — PBPK (KHẢ THI Ở NGƯỜI, không khả thi ở heo).** Tham số công khai: DrugBank · ChEMBL · PubChem · PK-DB. Phần mềm miễn phí đủ dùng: **PK-Sim / Open Systems Pharmacology**, có thư viện mô hình dựng sẵn. Ra đường cong nồng độ theo thời gian; đổi liều, chia liều, tuổi, chức năng gan–thận, thuốc dùng kèm → thấy đỉnh nồng độ, thời gian trên ngưỡng, tích luỹ. **Chỉ dùng cho chất có tham số tin cậy**; chất thảo dược/khoáng phải nội suy và dán nhãn bất định.

**C — Đo thật (rẻ nhất ở người).** N-of-1 trên chính Quang: xét nghiệm máu/nước tiểu (nồng độ chất hoặc dấu ấn gan–thận), CGM, vòng tay, nhật ký triệu chứng, đo trước/sau. Đây là dữ liệu **per-host** để hiệu chỉnh mô hình — ở heo phải chờ hết lứa.

## 4. Phác đồ đúng nghĩa gồm những gì

Không chỉ "chất nào, liều bao nhiêu":

- **lúc nào** — chất cần pH thấp thì uống xa bữa; chất bị CYP3A4 phá thì tránh bưởi; cơ chất P-gp thì tránh thuốc ức chế bơm
- **cùng gì / không cùng gì** — chồng đích thì **không cộng dồn** lợi ích; đối kháng thì mất tác dụng (tannin kết protein ↔ IgY; acid hoá mạnh ↔ vỏ bao butyrate)
- **đo gì để biết đúng sai** — chỉ tiêu + mốc thời gian
- **PMID cho từng dòng** — kèm loài + mức bằng chứng

## 5. Nối hai kho tại **CƠ QUAN**

Tầng BỆNH (heo) = cơ chế bị phá ở đâu. Tầng CHẤT (người) = chất tới đâu, gõ vào gì. `docs/06a` kết luận trùng khớp heo↔người cao nhất là **GAN và THẬN** — đúng dòng sản phẩm "Gan Thận". Nên chất điểm để mô phỏng đầu tiên phải là chất đi qua gan/thận (atorvastatin, paracetamol, metformin đều đã có trong kho), không chọn ngẫu nhiên.

## 6. Làn pháp lý cho engine hướng người

| Làn | Hệ quả |
|---|---|
| Tự dùng / nội bộ | nhẹ nhất — làm được ngay, nên bắt đầu ở đây |
| Công cụ tham khảo cho khách | được, nhưng phải ghi rõ **không thay bác sĩ, không chẩn đoán** |
| Bán thành sản phẩm | NĐ 15/2018 (TĂBS — cấm claim trị bệnh) hoặc NĐ 98/2021 (thiết bị y tế); dữ liệu cá nhân theo NĐ 13/2023 |

Engine mà kết luận ra "chẩn đoán / điều trị" là vào làn hành nghề y → không làm.

## 7. Nếu chất đích là nước kiềm pH 12–14 (sản phẩm của mình)

Không phải bài toán phân tử → **PBPK không mô tả được**. Mô hình đúng: nạp bicarbonat/khoáng → đệm dịch dạ dày → hấp thu ở ruột → thận điều chỉnh thải. Đo được rẻ tại nhà: **pH nước tiểu theo mốc thời gian · bicarbonat máu · điện giải · huyết áp**. N-of-1 là thiết kế hợp nhất, không cần chờ cỡ mẫu lớn.

## 8. Thứ tự đã đề xuất (chờ Quang chốt)

1. **Chuẩn hoá 15 chất** sang bảng tham số số (+ đánh dấu ô thiếu nguồn). ~2 ngày. Không có bước này thì mọi mô phỏng sau là đoán.
2. **Trang "định tuyến"** (Mức A): chọn chất + liều → 8 chặng có số + cơ quan gánh + cảnh báo thời điểm uống, tương tác CYP/P-gp. ~1 tuần.
3. **PK-Sim cho 3–5 chất** (Mức B), hiệu chỉnh theo dữ liệu công khai. ~1–2 tuần.
4. **N-of-1 của chính Quang** (Mức C) — nguồn dữ liệu per-host.

Hai câu cần Quang chốt trước khi dựng: engine để **tự dùng / cho khách / thành sản phẩm**? và chất đích là **nước kiềm của mình** (mục 7, đo được ngay) hay **hoạt chất nói chung** (mục 2–3, cần chuẩn hoá tham số)?

## 9. Bẫy giao tiếp đã dính (đừng lặp)

- Trả lời câu chiến lược về **người** bằng số của **kho heo** (28 mầm bệnh · 57 chất trộn cám · `1_xam_nhap`…). Quang phải chỉnh: *"Anh đang nói về người chứ không phải heo"*. **Xác định kho nào trước khi lấy số.**
- Bê nguyên kết luận **"không làm PBPK"** từ heo sang người — sai chiều: heo thiếu tham số, người thì có.
- Đừng gọi mô phỏng là "mô phỏng sinh học/phân tử" khi thực chất là duyệt đồ thị + cộng hiệu lực có trọng số. Gọi đúng tên: **mô hình dự đoán dựa trên bằng chứng**, xuất **khoảng** kèm số nghiên cứu và liều, cấm xuất một con số điểm.
