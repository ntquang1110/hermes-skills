# Lô 3 — hoạt chất Cửa D + Cửa E (`docs/12-hoat-chat-mo-rong`)

Chốt 20/10/2026. Deliverable: `batch-lo-3-mam-ngoai-va-ho-hap.md` + `.json`.
Anh em với `references/lo-2-hoat-chat-cua-b-c.md` (Lô 2 = Cửa B + C). Lô 1 = Cửa A.

## Số chốt

| chỉ số | giá trị |
|---|---|
| Hoạt chất | **20** (Cửa D 10 · Cửa E 10) |
| `muc_bang_chung = in_vivo_heo` | **18** (luật cứng đòi ≥5) |
| PMID verify Europe PMC REST (hitCount==1, pmid khớp) | **23 / 23** |
| Số token số không đối chiếu được với `abstractText` | **0** |
| Dòng điểm cắt khớp **nguyên văn** | **20 / 20** |
| Ô `tag_H` | **47** |
| Trùng 26 nguyên liệu nhà (`trong_26=true`) | **6** |

Phân bố chặng: D→`1_xam_nhap` 10 · E→`2_qua_hang_rao` 6 · `3_bam_cu_tru` 3 ·
`7_hau_qua` 2 · `8_thai_lay` 1. **Không** chất nào gán chặng 1 cho tác nhân hô hấp
(khớp dữ liệu 11/11 tác nhân hô hấp không có điểm cắt chặng 1) — nếu lô sau gán
được, coi như đã bịa.

## Cửa D — cắt mầm nhập từ thức ăn–nước (10 chất, đều `1_xam_nhap`)

| id | dòng cắt dùng | PMID | mức |
|---|---|---|---|
| `acid-benzoic` | salmonella | 33126524, 37858213 | in_vivo_heo |
| `kali-diformat` | salmonella | 41096511 | in_vivo_heo |
| `nuoc-dien-phan-acid-nhe` | etec (nước uống, đầu núm) | 37510303, 42511002 | in_vivo_heo |
| `acid-peracetic` | etec (biofilm đường ống) | 42781150, 41714774 | in_vivo_heo |
| `igy-khang-ecoli-k88` | etec | 42399933 | in_vivo_heo |
| `bacteriophage-etec` | etec | 42057154 | in_vivo_heo |
| `mos-mannan-oligosaccharide` | salmonella | 31603198 | in_vivo_heo |
| `humate-hap-phu-doc-to-nam-moc` | salmonella | 41003520 | in_vivo_heo |
| `1-monolaurin` | etec | 37858213 | in_vivo_heo |
| `thymol-rosmarinic` | etec | 39967693, 41497464 | in_vivo_heo |

Cửa D chỉ có **2 dòng** được dùng thật: `salmonella` *(Kiểm soát nguồn thức ăn và
nước, all-in/all-out…)* và `etec` *(Cắt nguồn nước uống nhiễm khuẩn: làm sạch đầu
núm…)*. Mọi chất Cửa D đều phải chọn 1 trong 2 — đây là chỗ dễ gán bừa nhất.

## Cửa E — cửa mở đường hô hấp (10 chất)

| id | dòng cắt dùng | PMID | mức |
|---|---|---|---|
| `acid-glycyrrhizic` | ssuis · 2 (+8_thai_lay) | 42298622 | in_vivo_heo |
| `mcfa-bien-tinh` | prrsv · 2 | 42654760 | in_vivo_heo |
| `hon-hop-phytogenic-ep` | pmult · 2 (+3) | 42211862 | in_vivo_heo |
| `protoberberin-alkaloid` | mhp · 7 | 41575198 | in_vivo_heo |
| `berberine-hydrochloride` | app · 3 | 42661110 | **in_vitro** |
| `baicalin` | prrsv · 3 | 42797950 | in_vivo_heo |
| `houttuynia-cordata` | prrsv · 2 | 35924249 | in_vivo_heo |
| `eucalyptol-limonene-pinene` | siv · 2 | 42547468 | **in_vivo_loai_khac** |
| `carvacrol` | mhp · 7 | 41946977 | in_vivo_heo |
| `yucca-schidigera` | mhp · 2 | 34368272 | in_vivo_heo |

`trong_26=true` (6): Thymol, Eucalyptol, Glycyrrhizin, Carvacrol, Berberine ×2
(`protoberberin-alkaloid` + `berberine-hydrochloride`). Mỗi mục đều có trường
`ly_do_xem_lai` nêu rõ **vì sao đáng xem lại (dạng bào chế / liều / vị trí tác động)**
— luật 10 của schema đòi, đừng chỉ bật cờ rồi để trống.

## 3 mục đã LOẠI kèm lý do (đã ghi trong `.md`, không độn lô)

- **tannin chestnut/quebracho** (`42662228`) — giảm tiêu chảy nhưng **không diệt**
  *E. coli*/*Salmonella* trong ruột ⇒ không khớp dòng cắt chặng 1 của Cửa D.
- **chitosan** (`42816880`) — chỉ xu hướng giảm thải *E. coli* trong phân, không có
  dòng cắt khớp Cửa D/E.
- **tinh dầu bạch đàn EEO** (`39228381`) — chỉ in vitro; đã có Eucalyptol làm đại diện.

## 2 kết luận quan trọng nhất (dùng lại được cho đề cương)

1. **Cửa D: điểm nghẽn thật của chặng 1 là NƯỚC, không phải cám.** Hai can thiệp có
   bằng chứng heo sống + đo được kết cục lâm sàng đều nằm ở đường nước (SAEW: giảm
   coliform nước 100 %, giảm 100 % tỷ lệ tiêu chảy, 72 heo con; PAA: >3 log biofilm,
   mọc lại sau 3 ngày ⇒ buộc duy trì liên tục). Acid hữu cơ trong cám chỉ chạm phần
   mầm trong thức ăn ⇒ **2 nhóm phải ghép, không thay thế nhau**.
2. **Cửa E: mọi can thiệp hô hấp hiệu quả phải đứng ở đường mũi/amidan TRƯỚC khi mầm
   bám; các điểm hậu quả chỉ đạt mức "ngang kháng sinh".** Mạnh nhất là tái cấu trúc
   hệ vi sinh đường hô hấp trên (glycyrrhizic acid 2,6 g/kg, 225 heo con — giảm đồng
   thời Mhp, *S. suis*, *G. parasuis*, *M. hyorhinis*); ngược lại ở `7_hau_qua`
   carvacrol chỉ "không khác kháng sinh" về điểm phổi. Khớp với 62 điểm bất khả ⇒
   đừng dồn ngân sách vào chặng 7–8 của đường hô hấp.

## Bẫy mới của lô này (đã bổ sung vào SKILL.md pitfall 41)

1. **`nham_diem_cat` KHÔNG đồng nhất hình dạng giữa các lô** ⇒ làm gãy checker dùng
   chung. Lô 2: `` `mam` · chặng X — câu ``. Lô 3: `câu (\`mam\` · chặng X) — lý do`.
   `scripts/check-cut-lines.py` nay có `parse_cut()` nhận cả hai.
2. **NBSP (`\xa0`) và số viết bằng CHỮ** (`Twenty-four`, `Twenty-six`) sinh cờ giả
   "số không có nguồn" — cùng họ với pitfall 30(b) (dấu nghìn) và luật `·`→`.`.
3. **Bẫy CHIỀU của kết cục**: abstract ghi *"feed conversion efficiency was
   significantly higher"* ⇒ phải viết "hiệu quả chuyển hoá thức ăn cao hơn", **KHÔNG**
   viết "tăng FCR" (FCR cao hơn = xấu hơn). Đọc kỹ chiều trước khi diễn giải.
4. **Xu hướng ≠ có ý nghĩa**: `P = 0.06/0.08` phải ghi "xu hướng", không ghi "giảm".
5. **Mục nằm SÁT VÙNG CẤM phải có bullet `rủi ro` nêu rõ ranh giới.** 3 ca thật:
   berberine ↔ `app` *"loại APP khỏi amidan bằng kháng sinh toàn thân"*; EP blend ↔
   `pmult` *"loại P. multocida khỏi khoang mũi"*; yucca ↔ `mhp` *"phục hồi lông mao
   đã mất"*. Câu chốt: *"đề xuất cơ chế X, KHÔNG đề xuất mục Y trong VÙNG CẤM"*.
   Xem chặng 2 và 7 hô hấp là nơi dễ đụng nhất.
6. **`muc_bang_chung` = cấp cao nhất cho CHÍNH CLAIM TRÊN HEO, không phải cấp cao
   nhất mà bài báo có.** `berberine-hydrochloride`: in vitro trên chủng APP heo +
   mô hình CHUỘT ⇒ `in_vitro`. `eucalyptol-limonene-pinene`: tế bào mũi người + mô
   hình chuột ⇒ `in_vivo_loai_khac`. `acid-peracetic`: thí nghiệm tại **trại heo
   thương phẩm** ⇒ `in_vivo_heo` hợp lệ. Phải mở abstract đọc vật chủ, không suy
   từ tiêu đề.
