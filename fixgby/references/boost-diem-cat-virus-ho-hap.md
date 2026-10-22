# Boost `diem_cat` cho lô VIRUS hô hấp (prrsv · pcv2 · pcv3 · siv · prv)

Bổ sung cho `references/boost-diem-cat-8-chang.md`. File đó viết quy trình chung + bộ từ khoá
**cho vi khuẩn**; file này là **luật riêng của lô virus** — và một trong các luật đó **ngược lại**
kết luận của file kia.

Chạy 20/10/2026 · output `docs/11-duong-di-benh/boost-b-ho-hap-virus.json` ·
15 ô (prrsv ×3 · pcv2 ×2 · pcv3 ×4 · siv ×3 · prv ×3) ·
**15/15 ô có PMID · 0 ô tag H** · 49 PMID verify **49/49** ·
`kha_thi`: 4 cao / 8 trung / 3 thap · `loai`: 12 A / 3 R.
Nguồn đối chiếu: `batch-c-ho-hap.json` (file hô hấp thật; `batch-b-ho-hap.json` **không tồn tại**
— xem mục 0 của file boost chung).

## 1. ĐẢO CHIỀU so với vi khuẩn: chặng 1 của VIRUS là điểm cắt MẠNH

File boost chung, mục "Mẹo cặp", viết:

> *"Chặng 1 và 4 của hầu hết mầm **không có thử nghiệm can thiệp on-farm** → đừng cố ép."*

Câu đó đúng cho **VI KHUẨN**, **SAI cho VIRUS**. Virus hô hấp vào bằng niêm mạc mũi nên có
**vaccine NIÊM MẠC** với kết quả đo được trên heo ⇒ `kha_thi="cao"`, không phải ô yếu:

- **PRV** — `41666694` (gB + poly(I:C) **nhỏ mũi**: bảo vệ hoàn toàn về lâm sàng, giảm tải virus
  trong mô và giảm bài thải khi thách chủng chủng biến thể ZJ01, hơn hẳn tiêm bắp gB) ·
  `42316174` (tá dược nhầy cGAMP) → **điểm cắt mạnh nhất của cả lô**
- **SIV** — `41695213` (LAIV vs replicon particle: kháng thể niêm mạc + tế bào T trên heo) ·
  `41891722` (kháng thể mẹ đồng dòng/dị dòng + stress cai sữa làm đổi mức nhân lên và lây truyền)
- **PCV2** — `42402413` (động học kháng thể mẹ trên 40 heo con: đỉnh 1–3 ngày tuổi, giảm hàm mũ
  tới ngày 19) cộng `42604973` (thời điểm tiêm **KHÔNG** liên quan đáp ứng huyết thanh — bằng
  chứng âm hữu ích) ⇒ điểm cắt đúng là **dò hàm lượng kháng thể mẹ của từng đàn**, không phải
  chốt một mốc lịch cứng
- **PRRSV** — `42259180` (MLV bảo vệ một phần trước chủng độc lực cao) · `42654760` (mMCFA bất
  hoạt >4 log trong 5 phút ⇒ cắt liều nhiễm theo đường ăn) · `41745969` (Saccharomyces MIIP
  đường ăn, 4 trại nhiễm: giảm viremia) · `42529228` (đơn tế bào hạch khí–phế quản: PRRSV phá
  đáp ứng miễn dịch thích ứng)

**Mầm không có vaccine đặc hiệu thì chặng 1 chỉ còn sàng lọc + cách ly:**
**PCV3 chưa có vaccine**, cross-protection từ vaccine PCV2 hạn chế (`42303972`) ⇒ chặng 1 của PCV3
ghi `kha_thi="trung"` và nói thẳng là không có can thiệp đặc hiệu.

## 2. Bộ từ khoá theo chặng — RIÊNG cho virus (khác bộ ở file chung)

Bộ ở file chung có `MIC` / `Apx` / `dermonecrotoxin` — vô dụng với virus. Bộ chạy được:

- **1_xam_nhap** — `vaccine efficacy`, `maternal antibody`, `colostrum`,
  `"maternally derived antibodies"`/MDA, `"infectious dose"`, `aerosol`, `"air filtration"`, `biosecurity`
- **2_qua_hang_rao** — `sialic acid`, `hemagglutinin`, `mucosal`, `IgA`, `"lymphoid tissue"`,
  `"in situ hybridization"`, `epithelium`, `tonsil`
- **4_nhan_len** — `replication`, `"in vitro"`, `PK-15`, `"bone marrow-derived cells"`, `capsid`,
  `gE`, `CRISPR`, và tên hợp chất ức chế (`thymol`, `myricetin`, `isoliquiritigenin`)
- **5_lan_he_thong** — `viremia`, `"bronchial tree"`, `dissemination`, `transplacental`, `neurotropic`
- **6_tin_hieu_hai** — `cytokine`, `IL-10`, `TNF`, `IFN`, `NS1`, `neuroinflammation`, `ferroptosis`,
  `autophagy`, `apoptosis`, `"single-cell"`
- **7_hau_qua** — `"lung consolidation"`, `"lung lesions"`, `pneumonia`, `abortion`, `stillborn`,
  `"growth performance"`, `"average daily gain"`, `slaughter`
- **8_thai_lay** — `shedding`, `"oral fluid"`, `"tracheobronchial swab"`, `carrier`, `persistence`

Thêm `AND pigs` (hoặc `(pig OR piglet OR swine OR porcine)`) vào **mọi** query — bộ lọc loài rẻ
nhất (xem pitfall 34 của SKILL.md: `sort=relevance` trả bài MỚI chứ không phải bài ĐÚNG); rồi mới
lọc tay.

Quy trình 2 tốc độ đã dùng: `resultType=lite` quét rộng nhiều query (in `pmid · năm · title · tạp chí`
thành dòng gọn, `pageSize≈5–8`, `sleep 0.2`) → chọn shortlist → `resultType=core` lấy `abstractText`
để viết `diem`/`ly_do` chính xác. Đừng lấy `core` cho cả trăm kết quả.

## 3. Chặng 5: SIV KHÁC PRRSV — đừng chép khuôn

- **PRRSV** lan qua máu: viremia trong 3 ngày, tới amidan/hạch/lách/Peyer/gan + **thai qua nhau thai**
  ⇒ chặng 5 mới có điểm cắt kiểu "cắt viremia trước khi tới thai".
- **SIV** lan theo **trục khí–phế quản** xuống các thùy phổi (`20682805`); **viremia và tổn thương
  ngoài hô hấp không phổ biến** ⇒ chặng 5 của SIV **không có** điểm cắt hệ thống. Điểm cắt khả thi
  chỉ là **giảm liều khí dung + thông khí chuồng** (`32971371`), `kha_thi="trung"`.

## 4. Chặng 6–7 của virus: ô "chỉ ĐO được" là hợp lệ

Đừng ép thành cơ chế nếu nguồn chỉ cho chỉ dấu. Hậu quả virus đo bằng:
- mổ khám — `41064406` đông đặc phổi vùng bụng–đầu (22 trại, 20 mẫu phổi/trại)
- giám sát thực địa — `42625238` dịch miệng 3 mốc + dịch khí–phế quản + 30 heo/trại tại lò mổ (21 trại Đức)
- sản lượng — `42774789` tăng trọng heo cai sữa→vỗ béo theo chiến lược vaccine

⇒ `diem` mô tả đúng **cái đo được**, `kha_thi="trung"`. Bịa cơ chế đảo ngược được là overclaim
(cùng họ pitfall 3 của `duong-di-8-chang-cua-benh.md`).

## 5. Ba bẫy mới (20/10/2026)

1. **Từ CẤM bị chính mình trích lại trong `ghi_chu` ⇒ pass kiểm từ cấm FAIL.** Bản đầu viết vào
   `ghi_chu`: *"Từ ngữ dùng 'can thiệp/chặn/giảm', không dùng '<từ cấm 1>' hoặc '<từ cấm 2>'."* —
   chính câu đó CHỨA hai từ cấm nên `assert not any(w in blob ...)` đổ, dù 15/15 ô đều sạch.
   Luật: **không bao giờ trích nguyên văn từ cấm trong BẤT KỲ trường nào của output**, kể cả để
   giải thích quy ước. Viết: *"Từ ngữ dùng 'can thiệp/chặn/giảm' theo quy ước của dự án."*
2. **Đừng mặc định ô virus sẽ là `tag H`.** Lô này ra **0 tag H / 15 ô** vì bệnh virus hô hấp heo
   có tài liệu rất dày. Giả định sẵn là tag H ⇒ dừng tra quá sớm, tự hạ chất lượng. Chỉ gắn tag H
   sau khi đã chạy đủ bộ từ khoá ở mục 2.
3. **`kha_thi="thap"` vẫn phải có nguồn và phải nói rõ THẤP VÌ LÝ DO GÌ.** Ba ô thấp của lô này
   (pcv3 `4_nhan_len`, pcv3 `6_tin_hieu_hai`, prv `6_tin_hieu_hai`) đều có PMID thật nhưng chỉ ở mức
   PK-15 / tế bào N2a / chuột. Viết cơ chế trong `ly_do` rồi mới hạ `kha_thi`; nêu rõ loài trong
   `loai_chi_tiet` (`"in vitro (PK-15)"`, `"in vitro + chuột"`). Không bỏ ô.

## 6. Kết quả ÂM của lô virus — đừng tra lại từ đầu

- **PCV3 × thymol / carvacrol / tinh dầu / acid hữu cơ** — không có bài nào dùng được; query chỉ trả
  tổng quan chung không chứa claim.
- **ZnO / acid hữu cơ × 5 virus hô hấp** — ZnO chỉ có dữ liệu đường ruột / tiêu chảy / tăng trọng;
  **KHÔNG** có bằng chứng kháng virus hô hấp. Đừng suy từ hiệu quả đường ruột sang đường hô hấp.
- **PCV3 — tế bào đích và thụ thể chưa xác định.** `2_qua_hang_rao` chỉ có bằng chứng **ĐỊNH VỊ**
  (`37621535` lai tại chỗ thấy PCV3 ở phổi + mô lympho), không có bằng chứng can thiệp ở mức hàng
  rào. Đây là ô yếu nhất của lô và đã ghi thẳng vào `bat_kha`, không tô hồng.
- **PRV × tinh dầu / thảo dược** — không có nghiên cứu can thiệp trên heo; chỉ có hợp chất in-vitro
  (`42798008` isoliquiritigenin · `42858589` IL-2/IFN-α/Tα1 trên PK-15).
- **SIV × tăng trọng** — không tìm được thử nghiệm can thiệp đo ADG trên heo ⇒ phải hạ xuống dùng
  chỉ dấu giám sát / mổ khám.

## 7. Kiểm tra cuối đã dùng (đủ 5 phép, chạy trên file ĐÃ ghi)

```python
# 1. coverage: đúng bằng set ô đề bài yêu cầu, không thiếu / không thừa
# 2. assert all(c["pmid"] for c in cells)      # 0 ô tag H
# 3. assert not any(w in blob for w in TU_CAM) # chạy trên BẢN ĐÃ BỎ trường meta
# 4. verify lại TOÀN BỘ PMID bằng 1 vòng EXT_ID (không cộng dồn theo mầm)
#    và kiểm rec["pmid"] == pmid truy vấn, rồi đọc title xác nhận đúng chủ đề
# 5. in bảng tóm tắt mầm × chặng × kha_thi × loai × số PMID
```

Ghi file **ngay sau mỗi mầm** (rewrite cả list từ biến trong bộ nhớ) — mất context giữa đường vẫn
còn dữ liệu. Đã dùng đúng như vậy: ghi sau prrsv (3 ô) → pcv2 (2) → pcv3 (4) → siv (3) → prv (3) + meta.
