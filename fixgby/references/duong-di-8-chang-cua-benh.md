# Tầng BỆNH — 8 chặng đường đi của MẦM BỆNH (khác tầng CHẤT)

`docs/11-duong-di-benh/`. Batch B = 5 virus + 4 ký sinh gây tiêu chảy ở heo.
39 PMID verified 39/39, 9 tác nhân × 8 chặng, 56 điểm cắt, 15 ô `tag_H` (19/10/2026).

Batch A = 8 vi khuẩn tiêu chảy (ETEC · Salmonella · Lawsonia · B. hyodysenteriae ·
B. pilosicoli · C. perfringens A/C · C. difficile · Yersinia).
65 PMID verified 65/65, 8 tác nhân × 8 chặng, **70 điểm cắt**, 16 ô `tag_H` (19/10/2026).

## 0. Đừng lẫn hai tầng

| | tầng CHẤT (`docs/09`, `docs/10`) | tầng BỆNH (`docs/11`) |
|---|---|---|
| chủ thể di chuyển | phân tử | mầm bệnh |
| khoá chặng | `cua_vao` → `o_lai` | `1_xam_nhap` → `8_thai_lay` |
| câu hỏi | chất này đi đâu, bị bơm nào đẩy | mầm vào cửa nào, nhân ở tế bào nào, ra bằng đường nào |
| đơn vị can thiệp | thụ thể / enzyme / bơm | điểm cắt trên từng chặng + `kha_thi` + `bat_kha` + `da_that_bai` |

Schema bệnh (8 khoá, đúng thứ tự — không đổi tên, không gộp):

```
1_xam_nhap       vào cơ thể bằng cửa nào        (miệng, mũi, khí dung, da, tinh dịch)
2_qua_hang_rao   vượt hàng rào đầu tiên         (pH, lớp nhầy, lông mao, IgA mẹ, bổ thể)
3_bam_cu_tru     bám thụ thể nào, cư trú tế bào nào
4_nhan_len       nhân lên ở đâu
5_lan_he_thong   lan ra hệ thống                (huyết, hạch, lách, bào thai, màng não)
6_tin_hieu_hai   phát tín hiệu hại              (độc tố, cytokine, cơ chế chết tế bào)
7_hau_qua        hậu quả trên con vật
8_thai_lay       ra ngoài / lây
```

Mỗi `benh` có: `id, ten, ten_en, nhom_benh, loai_tac_nhan, tuoi_mac, muc_pho_bien, chang{8},`
`diem_cat[], bat_kha[], da_that_bai[], chi_dau_do_duoc[], muc_bang_chung, tag_H[], pmids[]`.
Thêm `toc_do_lay` (1 dòng) — schema gốc không có nhưng task luôn hỏi "tốc độ lây trong đàn";
để trong JSON thì trang ráp bằng code mới hiển thị được, đừng chỉ viết trong `.md`.

`diem_cat` = `{chang, node, diem, kha_thi ∈ {cao,trung,thap}, ly_do, da_co_gi, pmid[]}`.
`kha_thi` viết **không dấu** đúng như schema — đừng "sửa" thành `thấp` rồi làm checker fail.

## 1. Ranh giới nội dung của tầng này (dễ vi phạm nhất)

Task tầng bệnh **cấm đề xuất sản phẩm / công thức / chất**. Cách viết đúng:

- `diem`: mô tả **cơ chế cắt** — "cắt vòng phân → miệng", "giữ hiệu giá sIgA trong sữa",
  "làm khô nền trong 24 giờ đầu", "giữ kiểm soát hệ vi khuẩn tại điểm bám".
  KHÔNG viết "dùng X", "bổ sung Y", "phun Z".
- `da_co_gi`: 1 dòng, thuần **đối chiếu** (all-in/all-out, rửa–sấy chuồng, mồi miễn dịch nái…),
  và ghi rõ "(đối chiếu, không phải đề xuất)" ở ô nào dễ bị đọc thành đề xuất.
- `da_that_bai`: chỉ nhận **bằng chứng âm tính thật** trong abstract (vaccine không bảo hộ chéo,
  sữa non không bảo vệ, miễn dịch chéo chỉ giảm nặng chứ không loại trừ). Không có PMID thì
  ghi `pmid: []` + `chưa có nguồn` và **vẫn phải** có mặt trong `tag_H`.

## 2. Bank 39 PMID theo tác nhân (verified 19/10/2026, đều đọc abstract)

**PEDV** — `32502552` (review: fecal-oral chính + khí dung phân–mũi "may play a role"; viremia;
atrophic enteritis jejunum+ileum; RNA mũi; vaccine cần cập nhật chủng) · `27317167` (entry: S gắn
sialic acid + APN; trypsin cần cho fusion; "replicates extensively and almost exclusively" ở biểu mô
ruột non) · `17467767` (pAPN chuyển được tính cảm nhiễm in vitro) · `25787280` (APN + N-acetylneuraminic
acid) · **`30315482` (heo ANPEP-null KHÁNG TGEV nhưng VẪN nhiễm PEDV)** · `25010284` (apoptosis không
phụ thuộc caspase, AIF, mPTP/cyclophilin D) · `27212686` (heo sinh ra agammaglobulinic; trục
gut–mammary–sIgA).

**TGEV** — `1350661` (Nature: APN 150K màng bàn chải là thụ thể; virus nhân lên **chọn lọc** trong
enterocyte đã biệt hoá phủ nhung mao) · `29914507` (chết **100%** heo < 2 tuần; teo nhung mao + giảm
chiều cao nhung mao và độ sâu crypt; giảm SIgA+/CD3+, tăng M cell; IL-1β/IL-6/TNF-α/IL-10/TGF-β; loạn
khuẩn) · `30315482` (APN **bắt buộc** — bằng chứng in vivo duy nhất trong nhóm) · `9060696` (mất gắn
sialic acid ở vùng S 145–155 ⇒ giảm độc lực đường ruột) · `10948987` (PRCV = đột biến mất đoạn S, ái
tính hô hấp; miễn dịch chéo làm giảm nặng TGE nhưng không loại trừ) · `33723809` (TGEV/PEDV/PDCoV
bệnh cảnh không phân biệt được).

**Rotavirus A** — `29119972` (Nat Rev Dis Primers: phá enterocyte → malabsorption + NSP4 tiết +
hệ thần kinh ruột; antigenaemia/viraemia) · `8600515` (Science: NSP4 114–135 gây tiêu chảy, tăng Ca²⁺,
tăng tiết Cl⁻, **age-dependent**) · `6489082` (heo con: giảm hấp thu Na⁺/nước, giảm 3-O-methylglucose,
giảm lactase/sucrase, giảm Na⁺,K⁺-ATPase hồi tràng, giảm chiều cao nhung mao, gap thẩm thấu do lactose)
· `33513201` (enteroid heo: HBGA vs acid sialic **khác vai trò theo chủng**; cắt sialic **tăng** nhân
lên ở G9P[13]) · `9015112` (chỉ chủng độc lực gây teo nhung mao; tiêu chảy sớm **trước** khi teo rõ;
bảo hộ tương quan đáp ứng miễn dịch tại ruột) · `41156666` (trại đã tiêm RVA: RVA/RVB không phát hiện,
**RVC 15/15**).

**Rotavirus C** — `32395116` (3 chủng; heo 3 ngày tuổi tiêu chảy nặng cả 3; RV0143 phá nhung mao rõ;
heo 3 tuần nhẹ hơn + IgA cao hơn; đỉnh thải mầm PID 2; IL-17/IFN-α tăng ở nhóm nặng) · `41156666` (RVC
chiếm chỗ sau khi RVA bị loại).

**PDCoV** — `25817405` (orogastric 5 ngày tuổi; tiêu chảy nhẹ–trung bình; thải mầm ngày 2→7; tổn thương
đại thể/vi thể) · `25811229` (gnotobiotic: 21–120 h, tiêu chảy nặng + atrophic enteritis) · `27086031`
(nhiễm biểu mô nhung mao **toàn** ruột non + ruột già, chính là jejunum/ileum; viremia thoáng qua;
chết do mất nước) · `29618640` (pAPN là thụ thể chức năng; **ái lực PDCoV-S1 thấp hơn TGEV-S1**).

**Isospora suis** — `6543059` (3 thế hệ vô tính + 1 hữu tính: ngày 2 / 3–4 / 4–5 / 5–6; nửa xa ruột non;
prepatent 5 ngày; patent **2 đợt** 5–8/9 và 11–14; chu kỳ ngoài ruột chỉ **đặt thuyết**) · `3666610`
(tổn thương ngày 7–14 tuổi, đỉnh 9–10; **50–140 cm trước lỗ hồi–manh tràng**; hoại tử đầu nhung mao;
gamont/oocyst trong mô lympho Peyer) · `16323027` (10.000 noãn nang: tiêu chảy đỉnh ngày 6, nửa số heo
≤ 2 ngày, 220–251.501 opg, teo nhung mao còn ở ngày 14) · `6837100` (excystation: taurocholate ± trypsin;
sporocyst không có thể Stieda, thành tách 4 tấm) · `18289796` (sporulation < 24 h ở mọi nhiệt độ; 100% RH
+ 25 °C: 100%→17% sau 96 h; 25–30 °C + 53–62% RH: chết trong 24 h) · `10321581` (sức đề kháng do miễn
dịch **không đặc hiệu** chưa trưởng thành, không phải miễn dịch đặc hiệu).

**Cryptosporidium** — `1496800` (52 heo thường + 20 gnotobiotic: tổn thương nặng nhất **jejunum sau +
ileum ngày 3–7**, dịch về đuôi, kết thúc ở ruột già; patent 8–9 ngày; gnotobiotic tới ngày 16; **sữa non
không bảo vệ**; ký sinh trong biểu mô tuyến lạc chỗ dưới niêm mạc ngày 9–10) · `3943690` (**chuột lang**:
vi rìa lõm → túi màng tế bào chủ → dung hợp màng 5 lớp → ngoại bào tương) · `8968331` (prostaglandin →
interneuron cholinergic → VIPergic/cholinergic → giảm hấp thu NaCl; **75%** hiệu ứng qua hệ thần kinh ruột).

**Trichuris suis** — `16600510` (5.000 trứng, định cư gần 100%; manh tràng + đại tràng gần; trứng đỉnh
7 tuần; đào thải ~9 tuần, gần 100% sạch 11 tuần) · `16750534` (tăng sinh crypt, goblet cell hyperplasia,
phì đại niêm mạc; chiều dài crypt ~ số giun; IL-4/5/13 ↑, iNOS/TNF-α/IL-10 ↓; eosinophil đỉnh 5 tuần,
basophil 7 tuần) · `9157675` (2.500 trứng: tiêu chảy, phù niêm mạc, **vi khuẩn tích tụ tại điểm bám**,
adenomatosis, hạch lympho to; **khi loại vi khuẩn thì tổn thương chỉ còn khu trú**) · `42119804` (38 °C
một mình **không** gây nở; nở do kích thích cơ học trực tiếp lên màng trứng) · `21684689` (trứng vỏ cứng
tồn tại lâu; Th2 ↑/Th1 ↓; có thể giảm hiệu lực vaccine vi khuẩn).

**Ascaris suum** — `9364572` (100/1.000/10.000 trứng: gan đỉnh ngày 3, phổi đỉnh ngày 7, đốm sữa đỉnh
ngày 7 và tồn tại đến 21–56; **47–58%** trứng thu hồi ở ruột non ngày 10; đào thải 17–21 ngày) ·
`21684689` (vỏ cứng, zoonotic, Th2/Th1, độ nhiễm đất tăng 2–3 năm đầu).

## 2b. Bank batch A — 8 vi khuẩn (65 PMID, 70 điểm cắt)

Số trong ngoặc = điểm cắt / PMID của tác nhân. PMID in đậm = nguồn trụ cho chặng 3 hoặc 6.

**ETEC (10/16)** — `22669578` (**pAPN = thụ thể F4ac**, clathrin-mediated endocytosis) ·
`19208633` (F18/FedF gắn glycosphingolipid kháng nguyên nhóm máu H type 1) · `42209446` (FUT1 M307:
A/A kháng, G/A + G/G cảm nhiễm; thực nghiệm 1×10⁹ CFU; tăng trọng ngày 0–5 giảm **58,9%** và **62,2%**) ·
`36303242` (LT làm tăng F4/flagellin/STb → vòng tự khuếch đại bám) · `42462087` (pH dịch dạ dày heo cai
sữa **4,0**; ruột non 5,9–6,0) · `38133272` (kháng thể mẹ ức chế vaccine FaeG ở heo con — **da_that_bai**
đã kiểm) · `41227403` (ZnO 1500 vs TBZC 680 mg/kg) · `28526080` (colistin/mcr-1).

**Salmonella (9/7)** — `41562556` (heo 90 ngày, **10⁸ CFU** uống, tiêu chảy ngày 5, loét cúc áo hồi-manh
tràng, hạch mạc treo to/xuất huyết) · `42288159` (traC chiêu mộ C4BP; mất traC giảm tải khuẩn máu **80%**,
gan **32%**, lách **63%**) · `38228171` (T3SS-1 + Rck/PagN; mô hình chuột — ghi loài) · `42369544`
(SPI-1/SPI-2, MDR) · `41491793` (5 serovar, đường lây khác nhau trong cùng trại).

**Lawsonia (8/9)** — `42335564` (**tế bào khuếch đại tạm thời trong crypt**, mất biệt hóa do phá BMP tại
crypt–villus, giảm goblet/enteroendocrine, liều nhiễm thấp) · `41916197` (R0 **3,35**; 63%/86% heo tiếp
xúc nhiễm sau 38 ngày từ **một** heo nguồn) · `42718558` (thải từ **3 dpi**; ADG **252,21** vs **300,98**
g/ngày) · `42304539` (thể granulomatous: Lawsonia trong đại thực bào/tế bào khổng lồ lamina propria +
dưới niêm mạc, viêm u hạt mảng Peyer) · `42012559` (vaccine giảm thải, không loại trừ nhiễm) · `41558228`
(Wnt **không** hoạt hóa — đừng mượn Wnt).

**B. hyodysenteriae (8/7)** — `38951921` (7 tuần tuổi, qPCR dương + phân máu/nhầy cùng **8 dpi**, trễ
0–3 ngày; haptoglobin/CRP/CK tăng) · `33686884` (MUC5AC de novo, sialomucin ↑, sulfomucin ↓, TGF-β1 ↓) ·
`41724371` (MMP tăng sớm trước loét; S100A8/9/12 khi cấp) · `32471432` (4 gen hemolysin `tlyA/tlyB/tlyC/
hlyA` — chặn 1 gen không đủ) · `23665849` (lây gián tiếp, heo mang trùng nhập đàn).

**B. pilosicoli (9/4)** — `39349383` (**BPP43_05035** bám N-glycan bề mặt + tight junction → tăng tính
thấm; giảm gen tight junction/bờ bàn chải) · `20200654` (bám màng đỉnh đại tràng, "bàn chải giả", hiếm
spirochetemia) · `37289435` (tiêu chảy/sốt ở người — ghi loài).

**C. perfringens A/C (8/6)** — `31955664` (**CPB tấn công tế bào nội mô mạch máu**, ức chế tiểu cầu;
chất ức chế trypsin trong sữa đầu bảo vệ CPB) · `39908342` (vị trí tiên phát = **ruột non gần**) ·
`39674030` (khu trú + nồng độ CPB ở **hỗng tràng**) · `36718447` (beta2 → S100A9, IL-6/8, TNF-α, IL-1β) ·
`36870204` (vai trò alpha toxin/CPB2 type A **chưa rõ** — đừng khẳng định).

**C. difficile (8/7)** — `42188921` (cư trú theo tuổi: **100%** ngày 2 → **10,7%** ngày 9 → 0 sau 21 ngày;
cửa sổ nhiễm cực hẹp) · `41844812` + `42043050` (TcdA/TcdB glucosyltransferase bất hoạt Rho/Rac/Cdc42,
phá junction, phá endolysosome) · `36621110` (phù mạc treo; calprotectin tương quan) · `38797681`
(ST11/RT078 heo–người) · `40432050` (vaccine toxoid: có kháng thể, **chưa** có bằng chứng bảo vệ đàn).

**Yersinia (10/8)** — `37255474` (**vào bằng miệng VÀ mũi/hầu**; 24 h đã có trong amidan/phân; 3 pha
P1/P2/P3, P2 từ 2 dpi, tồn tại **56 dpi**) · `39793062` (invasin → integrin β1) · `41012721` (ail/yst/inv/
yad; amidan + ruột) · `42463076` (YopP giảm NO) · `35627029` (4/O:3 tồn tại trong amidan 43% heo giết mổ).

## 3. Bốn phát hiện đọc ra từ chính 9 đường đi (đừng viết lại thành "tổng quan chung")

1. **Chặng 3 là nút thắt GIẢ; chặng 2 là nút thắt THẬT của nhóm virus.** Chỉ TGEV có thụ thể bắt buộc
   chứng minh in vivo (`30315482`); PEDV dùng cùng APN mà knockout vẫn nhiễm; PDCoV ái lực thấp; RVA
   nhiều cửa glycan và cắt một cửa còn làm tăng nhân lên (`33513201`). Cửa chung thật là **sIgA sữa**
   (`27212686`, `9015112`) — và nó **không** dùng được cho ký sinh (`1496800`: sữa non không bảo vệ).
2. **Teo nhung mao không phải cơ chế duy nhất ⇒ cắt vào nhung mao là trượt pha sớm.** Tiêu chảy trước
   khi teo rõ (`9015112`); NSP4 (`8600515`); hệ thần kinh ruột (`29119972`, `8968331`).
3. **Ở ký sinh, chặng 8 mới là nút thắt** (môi trường: 24 h sporulation, 96 h ở 100% RH, vỏ trứng bền)
   — vì ký sinh đã nằm trong tế bào/mô, không có bề mặt để chặn.
4. **Cắt một mầm làm mầm khác nổi lên** — RVA/RVB sạch nhưng RVC 15/15 (`41156666`). Mọi điểm cắt đơn
   tác nhân phải đọc kèm chỉ dấu các mầm còn lại.

## 3b. Ba phát hiện của nhóm vi khuẩn (batch A)

1. **Chặng 2 là chặng duy nhất cả 8 mầm đều qua, nhưng là chặng kém hiệu quả nhất.** Tất cả vào bằng
   miệng (Yersinia thêm mũi–hầu) và đều qua dạ dày — nhưng pH dạ dày heo cai sữa đo được **4,0**
   (`42462087`), và mỗi mầm chịu acid một kiểu: Salmonella có acid tolerance response (`31190705`),
   hai Clostridium lợi dụng dạ dày heo sơ sinh chưa tiết acid mạnh, Lawsonia/Brachyspira chỉ cần liều
   thấp. Kết luận: điểm cắt ở chặng 2 chỉ **giảm liều**, không chặn.
2. **Chặng 3 chia 8 mầm thành 2 nhóm quyết định loại điểm cắt dùng được.** Nhóm bám **bề mặt** có đích
   ngoài tế bào (ETEC–pAPN/F18; B. pilosicoli–BPP43_05035; C. perfringens–nội mô mạch máu) ⇒ chặn bám
   khả thi về nguyên tắc. Nhóm **nội bào/crypt** (Lawsonia trong tế bào khuếch đại; Salmonella trong đại
   thực bào; Yersinia trong mô lympho amidan/Peyer; C. difficile sau nảy mầm) bị chính màng tế bào vật
   chủ chặn ⇒ mọi điểm cắt chặng 3–4 đều `thap`.
3. **Điểm cắt dùng chung nhiều nhất nằm ở chặng 8 và 7, không phải chặng bám.** qPCR phân/oral fluid +
   tách heo thải cắt chuỗi lây cho cả 8; bù nước điện giải giảm chết cho cả 8 nhưng không cắt mầm nào.
   Ba điểm cắt "hấp dẫn" nhất — chặn pAPN, chặn tế bào M ở Peyer, loại bỏ bào tử khỏi chuồng — đều bất
   khả vì **lý do sinh lý vật chủ hoặc độ bền bào tử**, không vì thiếu công cụ.

## 4. Pipeline đã chạy tốt (tái dùng cho lô khác)

1. **Query Europe PMC** bằng `TITLE_ABS:` ghép nhiều từ, KHÔNG dùng 2 từ chung + `CITED desc`
   (trả về mega-review "Coronaviruses: an overview" không chứa claim). Chuỗi hiệu quả:
   `TITLE_ABS:"Isospora suis" AND (TITLE_ABS:pathogenesis OR TITLE_ABS:pathology)` rồi `CITED desc`;
   hoặc `TITLE:"transmissible gastroenteritis"` khi cần bài kinh điển (ra `1350661` Nature 1992).
   Với mầm cụ thể, `TITLE_ABS:"porcine deltacoronavirus" AND TITLE_ABS:pathogenesis` tốt hơn query
   bệnh học chung.
2. **Verify từng PMID** `EXT_ID:<pmid>&resultType=core` — guard `str(rec["pmid"]) == pmid`.
3. **Builder 2 tầng**: `data_virus.py` / `data_ky_sinh.py` (dict literal) + `build.py` (verify + render
   `.md` + dump `.json`). Không hand-write 90 KB JSON; không build trong `execute_code` (bị cắt thân code).
   Renderer sinh **cả** bảng tổng quan 9 dòng **và** mục "Nút thắt của cả nhóm" từ dữ liệu, để số trong
   phần phân tích không lệch số trong bảng.
4. **Cổng cuối** (chạy trên chính file của mình):
   `len(benh)==9` · mỗi `benh` đủ 8 khoá · `diem_cat>0` mỗi bệnh · mọi `kha_thi ∈ {cao,trung,thap}` ·
   `|set PMID|` in ra từ file · `tag_H` per-ben + top-level · **0 số lạ** so với abstract.

## 5. Pitfall riêng của tầng này

1. **Dấu phân cách NGHÌN làm checker báo "số không có nguồn" (dương tính giả).** Abstract viết
   `10,000` / `251,501`; tiếng Việt viết `10.000` / `251.501`. So chuỗi thô ⇒ FAIL oan. Chuẩn hoá
   **cả hai phía** trước khi so:
   ```python
   def norm_digits(s):           # 10.000 == 10,000 == 10000
       out, i = [], 0
       while i < len(s):
           if s[i].isdigit():
               j = i
               while j < len(s) and (s[j].isdigit() or (s[j] in ".," and j+1 < len(s) and s[j+1].isdigit())):
                   j += 1
               out.append(re.sub(r"[.,]", "", s[i:j])); i = j
           else:
               out.append(s[i]); i += 1
       return "".join(out)
   ```
   Cộng với `abstractText.replace("·", ".")` cho dấu thập phân Lancet. Sau khi vá: 6 cờ → **0**.
2. **PMID trả về kiểu `int` ⇒ `", ".join(pmid_list)` ném `TypeError: expected str, instance int found`.**
   Chuẩn hoá `[str(x) for x in ...]` ngay sau khi nạp data, cho **mọi** trường pmid (kể cả `pmids[]`,
   `yeu_to_anh_huong[].pmid`). Lỗi xảy ra ở bước render, rất muộn, sau khi đã fetch xong 39 PMID.
3. **Bốn chỗ overclaim tự bắt được khi đọc lại — cùng một họ lỗi: viết cơ chế suy ra, không có trong abstract.**
   - PEDV `5_lan_he_thong`: thêm "hạch mạc treo" — abstract chỉ nói viremia + RNA mũi ⇒ xoá node.
   - PEDV `6`: "mất enzyme bàn chải" ⇒ đổi thành "mất chức năng hấp thu (malabsorption)".
   - PEDV `7`: "tỉ lệ VH:CD **đảo**" là khẳng định định lượng không có trong nguồn ⇒ đổi thành
     "tỉ lệ VH:CD là **chỉ số đọc** mức teo". (Với Cryptosporidium thì `1496800` nói thẳng villous
     atrophy + crypt hyperplasia nên "đảo tỉ lệ" mới được phép.)
   - Isospora/Crypto `2`: "vỏ noãn nang bền pH dạ dày" — không có trong abstract ⇒ "noãn nang qua dạ dày
     xuống ruột non; lô nguồn không nêu chi tiết bước dạ dày".
   - Ascaris `2`: "dịch vị không phải bước giới hạn" ⇒ cùng cách xử lý.
   **Luật: câu nào bắt đầu bằng "nên/do đó/vì vậy" mà nguồn không nói, thì hoặc bỏ, hoặc hạ thành
   "chưa có nguồn" + `tag_H`.**
4. **Cơ chế chết tế bào: chỉ gán khi nguồn gán.** PEDV = apoptosis không caspase (AIF, `25010284`);
   PDCoV = **chưa xác định** ⇒ `tag_H`, không mượn apoptosis của PEDV; TGEV = nguồn dùng chữ
   "necrosis of enterocytes" (`30315482`) nhưng không phân định apoptosis vs hoại tử ⇒ nói đúng như vậy.
5. **Bài trên loài khác vẫn dùng được nhưng phải ghi loài ngay trong node.** `3943690` là **chuột lang**
   (cơ chế bám của Cryptosporidium) — hữu ích, nhưng ghi "(chuột lang, không phải heo)" trong `mo_ta`
   và thêm tag `...loai_vat_chu`.
6. **RVC/RVB là mầm thay chỗ, không phải "nhiễu".** Đừng gộp RVA/RVC thành "rotavirus"; `tag_H` cho
   thụ thể RVC và ghi rõ đỉnh thải mầm PID 2 (cửa sổ can thiệp cực hẹp).
7. **Chặng nào cũng phải có mặt, kể cả khi kết luận là "không có gì xảy ra".** Ascaris `4_nhan_len`
   không phải "nhân lên" — viết "**không** nhân lên trong heo; phát triển/lột xác", kèm số 47–58% để
   chứng minh không khuếch đại. Trichuris/TGEV `5` = "chưa có nguồn" + `tag_H`, không bỏ trống.
8. **Subagent anh em ghi cùng thư mục.** Lượt này batch A (`vi-khuan`) và batch C (`ho-hap`) được ghi
   song song vào `docs/11-duong-di-benh/` (kèm `_build.py`, `_data_*.py`, `_verified_abstracts.json`).
   Dùng tên file riêng (`batch-b-…`), **không** xoá/đổi tên file `_`-prefix của người khác, và sau khi
   ghi phải `ls` lại thư mục để chắc file mình còn nguyên.

## 6. Trạng thái

`batch-b-tieu-chay-virus-ky-sinh.{md,json}` đã ghi (89,8 KB / 98,6 KB).
`batch-a-tieu-chay-vi-khuan.{md,json}` đã ghi (84 KB / 97 KB; 8 vi khuẩn · 70 điểm cắt · 65 PMID ·
16 `tag_H` · 5 `yeu_to_anh_huong`) — batch A xong, đừng viết lại nhóm vi khuẩn.
Còn mở: `balantidium`, `strongy` (danh sách gốc `00-master-list.md` có, lô B không giao) — nếu làm,
đọc `batch-a-*` + `batch-b-*` trước để không trùng PMID và không lặp lại cùng một kết luận overview.
