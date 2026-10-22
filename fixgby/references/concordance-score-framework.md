# Khung chấm điểm Concordance Score (CS) — heo ↔ người theo từng cơ quan

Nguồn: `docs/05-plan-do-trung-khop-co-quan.md` (khung + Phụ lục A) và `docs/06a-research-do-trung-khop-co-quan.md` (bằng chứng, 62 PMID).
Toàn bộ số trong file này đều truy được về 2 tài liệu trên. Chỗ nào cần verify thêm thì ghi mã `V#`.

## 1. Công thức — 6 tầng

```
CS = 0.10·T1 + 0.25·T2 + 0.15·T3 + 0.15·T4 + 0.30·T5 + 0.05·T6
```

| Tầng | Nội dung | Trọng số gốc | Đề xuất |
|---|---|---|---|
| T1 | Mô học / giải phẫu | 10% | giữ |
| T2 | Transcriptome bulk | 25% | **hạ → 20%** |
| T3 | Single-cell | 15% | **nâng → 20%** |
| T4 | Proteome / metabolome | 15% | giữ |
| T5 | **CHỨC NĂNG** | **30%** | giữ — nặng nhất |
| T6 | Bệnh học tự nhiên | 5% | giữ |

**Vì sao T5 nặng nhất:** fixgby bán *can thiệp có tác dụng*, không bán "sự giống nhau". T5 là tầng duy nhất có bằng chứng in vivo trên người.

## 2. Ngưỡng quyết định (đặt TRƯỚC khi chấm, không sửa sau)

| CS | Ý nghĩa | Hành động |
|---|---|---|
| ≥ 75 | 🟢 Dùng được | được ngoại suy kết cục sang người |
| 55–74 | 🟡 Dùng có điều kiện | bắt buộc kiểm chéo 1 chỉ dấu ở người |
| 45–54 | 🟠 Học cơ chế nền | không ngoại suy kết cục |
| < 45 | 🔴 | chuyển hướng |

**Cửa phase:**

- Phase 0 → Phase 1: **≥ 4/10 cơ quan có CS ≥ 55** ← *con số này đang là điểm mắc lớn nhất, xem mục 6*
- Phase 1 → Phase 2: **≥ 1 cơ quan có CS ≥ 75**

**Luật chuyển hướng toàn cục:** nếu cửa fail → bỏ ngoại suy heo→người, **giữ heo làm thị trường** (Kịch bản B trong `04-market-gap-analysis.md` đứng độc lập, không phụ thuộc kết quả này).

## 3. Xếp hạng 10 cơ quan theo bằng chứng (06A — định tính, chưa phải CS)

| Mức | Cơ quan | Ghi chú quyết định |
|---|---|---|
| CAO (3) | **GAN** | tốt ở T2/T5 (ghép sống 171 ngày, PMID:41076089); **heo KHÁNG gan nhiễm mỡ** → T5=T6=0 cho NAFLD/NASH; **trống T3 single-cell** |
| CAO (3) | **RUỘT** | mạnh nhất trong 3 cơ quan khởi đầu; microbiome tương đồng nổi bật; lấy mẫu không xâm lấn (1.074.127 tế bào, PMID:41047495) |
| CAO (3) | **TIM** | T5 tốt ngắn hạn (2 ca ghép người sống, PMID:35731912 + PMID:39779924); giải phẫu đại thể khác ("Valentine heart"); **không lặp đo được** |
| TB (5) | **THẬN** | lưỡng cực tầng rõ nhất: T3 cao (138.469 tế bào / 29 loại, PMID:40116025), T2 thấp (nằm trong 3/15 mô mà chuột > heo) |
| TB (5) | **MÁU** | heo cùng nhóm "LPS-sensitive" với người (PMID:39730996) nhưng khoảng cách tuyệt đối lớn; khác biệt đáp ứng LPS >100.000 lần giữa các loài có xương sống |
| TB (5) | **MÔ MỠ** | loại tế bào bảo tồn; heo có riêng mesenchymal + B cell, người có riêng dendritic + mast cell |
| TB (5) | **DA** | **lưỡng cực ngược thận**: mô học CAO ("gold standard" cho nghiên cứu vết thương), T2 THẤP → không dùng da để kết luận điều hoà gen |
| TB (5) | **CƠ XƯƠNG** | có dữ liệu riêng theo mô (47 cơ xương trong Pig BodyMap); **béo phì đảo hướng** đáp ứng gen so với người và chuột |
| THẤP (2) | **PHỔI** | thiếu dữ liệu: chỉ review rào cản miễn dịch, không có số đo tương quan phiên mã, **không có ca ghép phổi heo→người nào** |
| THẤP (2) | **XƯƠNG/KHỚP** | không có số đo transcriptome/proteome; chuột + cừu mới là lựa chọn cho nghiên cứu xương |

**Đối chứng âm bắt buộc:** thêm **TUỴ** vào bảng chấm — không phải để chọn, mà để **kiểm tra công thức CS có phân biệt được tốt/xấu không**. Tuỵ nằm trong nhóm chuột > heo. Nếu tuỵ cũng điểm cao thì công thức vô dụng.

## 4. 8 luật bắt buộc trước khi công bố CS (R1–R8)

Áp các điểm 06A buộc phải phản ánh vào trọng số hoặc điều kiện loại. Không áp thì CS chỉ là con số trang trí.

- **R1 — Gene family & enhancer không chuyển.** Chỉ **2,86%** regulatory element của *Sus scrofa* bảo tồn chéo loài; **16,35%** là Suidae-specific. Nếu tập gen tính T2 chứa gen khứu giác / miễn dịch / α-amylase / ABC transporter → **T2 = 0**. Bắt buộc ghi danh sách gen đã loại.
- **R2 — Tầng bulk không được một mình quyết định.** Với **THẬN · DA · TUỴ** (3 mô mà chuột > heo): T2 phải kèm phân tích song song người–CHUỘT; nếu heo không vượt chuột → **T2 ≤ 50**.
- **R3 — Chuyển hoá thuốc theo từng chất nền.** CYP2C9/diclofenac chuyển hoá rất thấp ở heo và **không tương quan** với người. Tỉ trọng isoform khác (CYP2A 31%, CYP2D 28%, CYP3A 14%). Phenotype phụ thuộc CYP2A/CYP2C/CYP2D → **T4 = T5 = 0**.
- **R4 — Miễn dịch/đông máu bị loại khỏi ngoại suy.** Thất bại ghép do T-cell + kháng thể, thải ghép ngày 12, tái hoạt PCMV/PRV. → **T4 = T5 = 0** cho readout miễn dịch.
- **R5 — Phenotype đã chứng minh ngược chiều.** GAN: **T5 = T6 = 0** cho NAFLD/NASH/gan nhiễm mỡ. CƠ XƯƠNG: **T5 = 0** cho viêm/chuyển hoá cơ do béo phì.
- **R6 — Vi giải phẫu thận.** THẬN: **T5 = T6 = 0** cho cô đặc nước tiểu / nội môi nước–điện giải (heo ít nephron hơn, ít quai dài hơn; người 85:15). Chỉ dùng phenotype lọc/nội môi toàn thân (eGFR, cân bằng acid-base, Ca/P).
- **R7 — Phân ly tầng.** Mọi dòng CS phải kèm 6 điểm tầng. Chênh lệch tầng cao nhất − thấp nhất **> 30 điểm** → gắn nhãn "PHÂN LY TẦNG" và **chặn trần CS ở 74** (không được xếp ≥75).
- **R8 — Giả định ortholog & batch effect.** Bắt buộc: (a) một pipeline duy nhất cho heo + người; (b) chuẩn hoá trong-từng-loài trước, so sau; (c) báo cáo cả chỉ số trước và sau hiệu chỉnh batch; (d) luôn kèm đối chứng song song người–CHUỘT; (e) hạ xuống single-cell khi có thể. Thiếu (a)–(d) ⇒ **không công bố T2/T3**.

**Ví dụ R7 bằng số thật:** gen **CRH** cho **2 kết luận ngược nhau ở 2 tầng** — corCor heo > chuột (0,304 vs 0,065), nhưng module-level chuột > heo (0,399 vs 0,011). PMID:42801618. Một tầng không đủ để kết luận.

## 5. Tầng chưa đo = 0, ghi rõ "chưa đo", KHÔNG nội suy

Hệ quả phải biết trước: **nâng T3 lên 20% làm GAN mất điểm** — không phải vì gan kém, mà vì gan **chưa có dữ liệu T3 single-cell**. Nếu đọc bảng điểm mà không biết điều này thì kết luận sai là gan kém.

## 6. Việc còn treo (mọi thay đổi phải được Quang chốt)

1. **Cổng chuyển hướng: giữ 4/10 hay hạ 3/10?** — 06A chỉ xếp **3/10 ở mức CAO** (GAN, RUỘT, TIM). Nếu để 4/10, cổng do chính mình đặt sẽ tự FAIL và buộc bỏ hướng heo→người **không phải vì khoa học, mà vì ghi sai một con số**. Đây là điểm đắt nhất.
2. Trọng số T2 25→20% và T3 15→20%.
3. Danh sách 10 cơ quan (thận · gan · ruột · phổi · tim · cơ · da · máu · mô mỡ · xương/khớp) + có thêm TUỴ làm đối chứng âm không.
4. R1–R8 thành **bắt buộc**.
5. Ngách đầu tiên: **heo trước hay người trước?** — 04-market-gap cho heo Company Fit 5.0, người 1.0.

## 7. Việc verify còn thiếu (V#)

**Chặn cứng:**

- **V1** — corCor trung vị **tuyệt đối theo từng mô** (Table S3 / Figure 2A của PMID:42801618), nhất là GAN và THẬN. Đây là con số **duy nhất** chấm được T2 cho 2 cơ quan khởi đầu. Hiện chỉ có hướng (heo > chuột ở 12/15 mô) và đếm mô.
- **V2** — bài so sánh **single-cell GAN heo ↔ người**. Không có → **T3 của GAN = 0**.

**Chặn từng cơ quan:** V3 (tương quan phiên mã PHỔI) · V4 (transcriptome/proteome XƯƠNG–KHỚP) · V6 (proteome gan/thận — thận chưa có số, chỉ gan có CYP450).

**Chặn quyết định:** V5 (% nephron / tỉ lệ quai ngắn:quai dài **của heo**, hiện chỉ định tính) · **V8 (bảng xếp hạng heo vs khỉ theo từng mô — cơ sở để chuyển sân học cơ chế sang khỉ nếu luật chuyển hướng kích hoạt)** · V7 (bản bình duyệt "Revising the ortholog conjecture", hiện chỉ preprint) · V9 (ca ghép thận heo→người sống 2024 chưa bình duyệt) · V10 (CattleGTEx/ChickenGTEx portal chưa verify API).

**Ngưỡng tự đặt, KHÔNG có nguồn y văn — phải ghi rõ khi báo cáo:** V11 (các mốc 75/55/45 và luật <4/10) · V12 (ngưỡng lệch >15 điểm thì dừng xem lại).

## 8. Bằng chứng neo (dùng lại được, đều đã verify)

- Heo tương đồng người hơn chuột ở **12/15 mô** (tầng co-expression, corCor) — PMID:42801618
- Heo cùng nhóm **"LPS-sensitive"** với người; chuột/rat/khỉ đầu chó/rhesus là nhóm **"LPS-resilient"** — PMID:39730996
- Atlas single-cell heo: **229.268 nhân / 19 mô / 67 loại tế bào** (PMID:41309493) · **>200.000 tế bào / 20 mô / 58 loại** (PMID:35750885)
- **Gan heo 6-gen-edit ghép người chết não**: tiết mật vàng, 66,5 ml mật đến ngày 10, ALT bình thường — PMID:40140580
- **Gan heo 10-gen-edit ghép người sống: sống 171 ngày** — PMID:41076089
- **Thận heo 10-gen-edit**: hỗ trợ cân bằng nội môi, theo dõi 7 ngày ICU — PMID:38290599
- Cảnh báo: các ca ghép chứng minh **chức năng cơ quan** tương thích, **KHÔNG** chứng minh trùng khớp cơ chế phân tử/điều hoà gen. T5 **không được dùng để suy ngược ra T2/T3**.

## 9. Lộ trình và Phase 0 (~0 đồng, 3–4 tuần)

Dữ liệu công khai: **PigGTEx** (heo) + **GTEx** + **Tabula Sapiens** (người) + **FarmGTEx/Ensembl Compara** (ortholog). Việc: dựng ma trận PigGTEx theo mô (≥8 mô, ghi version) → ma trận GTEx khớp 1:1 → ánh xạ ortholog (≥90% gen, có log gen loại) → loại gene family lệch → tính T2 cho 10 cơ quan → tính T3 cho 5 cơ quan → chấm T1/T4/T6 từ y văn (≥2 nguồn mỗi tầng) → xuất bảng CS + xếp hạng (để trống cột T5).

**Cần đúng 1 người biết R/Python + bioinformatics.** Không có người này thì plan nằm trên giấy.
