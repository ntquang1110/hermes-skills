# Bản đồ tương kỵ hoá lý — Lô B (`docs/14-cong-thuc-co-ban/batch-lo-B-tuong-ky.{md,json}`)

Chốt 20/10/2026. Nhiệm vụ: 17 NHÓM hoạt chất dự kiến nằm chung MỘT bao premix heo → đối chiếu
từng cặp, mỗi cặp có vấn đề phải nêu cơ chế · mức độ · mức bằng chứng · cách xử lý; cuối cùng
kết luận TÁCH BAO mấy gói. Khác hẳn Lô 1 (`ban-do-tuong-ky-premix-lo-1.md`, 58 cặp giữa các
nguyên liệu rời): Lô B là tầng NHÓM CHỨC NĂNG, và câu trả lời cuối là **con số gói**.

## Schema — KHÔNG giống Lô 1 (đây là chỗ dễ gãy QC dùng chung)

Lô B dùng **khoá tiếng Việt**, không dùng 9 khoá tiếng Anh của Lô 1:

```json
{"nhom_a":"N1","nhom_b":"N13","co_che":"…","muc_do":"nang",
 "muc_bang_chung":"published","cach_xu_ly":"…","pmid":["16339934"],
 "pmid_vai_tro":"tien_de","pmid_la_bang_chung_cua_cap":true,
 "nhom_a_ten":"Acid hữu cơ tự do","nhom_b_ten":"Men vi sinh …"}
```

Top-level: `meta · nhom[17] · danh_sach_cap[133] · cap_tuong_thich · ghi_chu_ngoai_ma_tran ·
dieu_kien_chung · ket_luan_dong_goi · thong_ke · pmid_verify[38]`.

- `muc_do ∈ {nang, vua, nhe}`; `muc_bang_chung ∈ {published, suy_luan_hoa_ly, phong_doan}`.
- `ket_luan_dong_goi` bắt buộc có `so_goi` · `nhom_trong_goi` · `nhom_khong_duoc_chung`
  (đúng 3 khoá user yêu cầu) + `bien_the_dong_goi` · `thu_tu_phoi_tron_va_cach_dung` ·
  `kiem_soat_chat_luong` · `rui_ro_con_lai_chua_du_bang_chung`.
- `pmid_verify` = nhật ký verify nhúng trong chính file JSON (pmid · title · year · journal ·
  hitCount · pmid_khop) → **không cần giữ file log rời**; `meta.file_verify_log` trỏ vào chính
  trường này.

**Luật mới (đắt nhất của lượt này): `muc_bang_chung = suy_luan_hoa_ly` KHÔNG được kèm PMID trần.**
Đề bài cấm gán PMID cho khẳng định chỉ là suy luận hoá lý. Cách thoả cả hai vế (vẫn minh bạch +
không vi phạm): PMID tiền đề **vẫn giữ** nhưng bắt buộc `pmid_vai_tro = tien_de` và có field
boolean `pmid_la_bang_chung_cua_cap` (true chỉ khi `published`); phần hiển thị in 3 nhãn khác nhau:

| nhãn hiển thị | điều kiện |
|---|---|
| `= bằng chứng PUBLISHED TRỰC TIẾP cho cặp này` | `published` + `pmid_vai_tro=truc_tiep` |
| `= tiền đề published cho một chân của lập luận; KHÔNG đo trực tiếp trên cặp thương phẩm` | `published` + `tien_de` |
| `= chỉ là TIỀN ĐỀ cho nguyên lý hoá lý, KHÔNG phải bằng chứng cho cặp này` | `suy_luan_hoa_ly` |

Kèm `meta.quy_uoc_pmid_trong_suy_luan` nói thẳng quy ước này, để người sau không trích lại
một PMID tiền đề như thể nó là bằng chứng cho cặp.

## Số chuẩn (20/10/2026)

- 17 nhóm N1–N17 · 136 cặp khả hữu → **133 cặp ghi vào `danh_sach_cap`**: **21 nặng / 43 vừa / 69 nhẹ**.
- Mức bằng chứng: **21 `published` / 112 `suy_luan_hoa_ly`** (0 `phong_doan`).
- **38 PMID verify Europe PMC đạt (hitCount=1 + pmid khớp)**, chỉ **34 được dẫn**; 4 verify-không-dùng
  (`30140751 · 33268181 · 36763007 · 42457889`) ghi vào `thong_ke.pmid_verify_khong_dung`.
- 21 cặp NẶNG, 17 cặp trong danh sách "TUYỆT ĐỐI không nằm chung".

## Kết luận đóng gói (câu trả lời lõi — dùng lại được cho mọi biến thể công thức)

**KHÔNG thể một bao.** Bộ đầy đủ 17 nhóm = **6 GÓI** (5 bắt buộc + 1 khuyến nghị):

| Gói | Nhóm | Ghi chú bắt buộc |
|---|---|---|
| 1 Nền khoáng hấp phụ + đệm kiềm | N5 + N6 | gói NẶNG nhất → tách luôn khỏi gói nhẹ để chống phân tầng |
| 2 Acid + tinh dầu vi nang + MCFA | N1 + N2 + N8 + N4 | tinh dầu PHẢI vi nang hoá trước; bao PE lót trong (acid ăn mòn) |
| 3 Tanin + flavonoid/saponin | N11 + N9 | tách khỏi alkaloid (kết tủa) |
| 4 Sinh học | N13 + N12 + N3 + N15(phytase, xylanase) + IgY vi nang | **KHÔNG protease**; men dạng bào tử |
| 5 Khoáng vi lượng | N16 | đúng thực hành ngành: mineral premix tách khỏi vitamin premix |
| 6 Vitamin & acid amin | N17 (+ choline clorid) | nhạy nhất với kim loại/kiềm/oxy/ẩm |

Thang biến thể (trả lời "tách mấy gói" theo quy mô, thay vì một con số cứng):
- **3 gói** = tối thiểu khi bao CHỈ chứa khối chức năng (N16/N17 do premix VTM khác lo):
  {N5,N6} · {N1,N2,N8,N4,N9,N11} · {N13,N12,N3,IgY vi nang,phytase+xylanase}.
- **4 gói** = gộp phyto (gói 2+3) và gộp VTM loãng — kèm điều kiện cứng: khoáng pha loãng ≥1:10
  trên chất mang, vitamin vi nang, bao hàn kín, hạn dùng ≤3 tháng, định lượng lại vitamin tháng 1-2-3.
- **6 gói** = khuyến nghị chuẩn bộ 17 nhóm. **7 gói** nếu tách IgY riêng hoặc dùng đất hiếm.
  **8 gói** nếu vẫn giữ protease dạng trần (khuyến nghị bỏ protease khỏi bao, phun riêng).

17 cặp TUYỆT ĐỐI không chung bao — bản gọn để tra nhanh:
acid×kiềm · acid×men vi sinh · acid×IgY · butyrat bọc/MCFA×kiềm · MCFA×men vi sinh ·
tinh dầu×men vi sinh · tinh dầu×IgY/enzyme · alkaloid×tanin · baicalin×berberin ·
tanin×IgY · tanin×enzyme · IgY×protease · enzyme(phytase)×kim loại · kim loại×vitamin ·
kim loại×kiềm · khoáng sét×alkaloid · khoáng sét×enzyme/IgY · đất hiếm×phosphate(DCP/MCP).

## Bằng chứng then chốt đã verify (đừng truy lại từ đầu)

| PMID | Dùng cho cặp/luận điểm | Vai trò |
|---|---|---|
| 31961233 | monocaprin MIC 0,32 mg/mL với *Bacillus subtilis* + *S. aureus* → **MCFA × men vi sinh** | trực tiếp |
| 16339934 | acid lactic dạng không phân ly giết *L. plantarum* (transcriptome) → acid × men vi sinh | tiền đề mạnh |
| 15246235 + 34071618 | tinh dầu MIC 0,2–10 µL/mL, **Gram dương nhạy hơn Gram âm** → tinh dầu × men vi sinh | tiền đề |
| 40961760 | IgY phải vi nang hoá chống acid–pepsin → acid/tanin/kiềm × IgY, protease × IgY | tiền đề |
| 42791726 | palmatin **intercalate vào montmorillonit** → alkaloid × khoáng sét (nặng) | trực tiếp |
| 22356897 · 38573419 · 37961037 | berberin–tannic acid kết tủa; baicalin–berberin kết tủa trong bài thuốc Scutellaria–Coptis | trực tiếp |
| 22440016 | carbohydrat **ức chế** kết tủa protein bởi condensed tannin → tanin × IgY / tanin × oligo | trực tiếp |
| 7665384 | tanin/polyphenol ức chế enzyme + tương tác protein | tiền đề |
| 25416530 · 24966411 | vi lượng ức chế phytase; phytase–EDTA–polyphenol × hấp thu kẽm | trực tiếp |
| 32810935 · 31888146 · 33923615 · 36381950 · 33094271 | độ bền vitamin trong premix (choline/Cu/Zn, K3, tan nước & tan dầu) | trực tiếp |
| 35233256 · 42831158 | lanthanum carbonat là thuốc **gắn phosphate** → đất hiếm × DCP/MCP | trực tiếp |
| 39476683 · 38117753 | CeO2 tương tác + dephosphoryl hoá phosphate vô cơ; hoạt tính nanozyme | trực tiếp |
| 33466765 | tinh dầu mất do nhiệt khi ép viên, vi nang hoá làm bền | trực tiếp |
| 35047221 | cố định α-amylase lên bentonit → khoáng sét × enzyme | trực tiếp |
| 38247403 | humic acid chelat/giữ ion kim loại → sét/humat × khoáng vi lượng | trực tiếp |
| 12002639 | clinoptilolit trên heo nái: **KHÔNG** thay đổi vitamin A/E và khoáng máu/gan/thận → sét × vitamin chỉ cần ĐO, không cần tách | trực tiếp (ngược trực giác) |
| 35666003 | ionophore đồng giết *Bacillus subtilis* → kim loại × men vi sinh | tiền đề |
| 42866580 | phức vi nang tributyrin–monolaurin trên heo con (PEDV) → butyrat bọc × MCFA dùng chung được | trực tiếp |
| 19108897 | baicalin chelat Fe + chống Fenton → flavonoid × khoáng vi lượng | trực tiếp |

Nguyên tắc khiêm tốn giữ nguyên của dự án: 112/133 cặp là `suy_luan_hoa_ly`; 5 rủi ro phải thí
nghiệm mới chốt được (sét×enzyme/IgY trong BỘT KHÔ, ngưỡng alkaloid làm giảm CFU, tốc độ oxy hoá
bọc lipid bởi Cu/Fe ở aw thấp, ảnh hưởng đất hiếm lên phospho ở heo, dạng nguyên liệu thực tế của
nhà cung cấp) — đã ghi thành mục 10.7 + mục 12 của file `.md`.

## Kỹ thuật sinh 2 file (dùng lại cho mọi deliverable lớn của dự án)

Đề bài đòi 2 file (.md + .json) tiếng Việt có dấu, khối lượng ~190 KB + ~150 KB, có bảng 17×17
và 133 mục chi tiết. Cách chạy được:

1. **Ghi dữ liệu thành 7–8 chunk JSON nhỏ** (mỗi chunk ~8–18 KB: meta+nhóm+điều kiện chung ·
   từng dải cặp theo `nhom_a`), mỗi chunk `write_file` **validate bằng lint JSON ngay** → file
   hỏng lộ ra tức thì. Viết một phát 85 KB bị **cắt nội dung và bỏ dấu tiếng Việt** mà vẫn báo
   `success` (xem pitfall 46).
2. **Một renderer nhỏ** đọc các chunk → ghi `.json` final **và** render `.md`. JSON là **nguồn duy
   nhất**: `.md` sinh từ chính JSON đó nên hai file không thể lệch (đúng luật 40 của dự án).
3. Trong renderer có **bộ lọc chống tự mâu thuẫn**: cặp nào đã nằm ở `danh_sach_cap` thì bỏ khỏi
   `cap_tuong_thich` (lượt này 5 cặp vừa "tương thích" vừa "mức nhẹ" — hai bảng nói ngược nhau).
   In danh sách đã bỏ ra `meta.ghi_chu_bang_tuong_thich`.
4. Sau khi render: tự kiểm bằng code — đủ 7 khoá mỗi cặp, `muc_do`/`muc_bang_chung` thuộc enum,
   `ket_luan_dong_goi` có đủ 3 khoá, `pmid_verify` toàn `hitCount==1 && pmid_khop`, và các bảng
   không trùng cặp.
5. **Đừng `rm` renderer trước khi chốt deliverable.** Lượt này xoá `_render_batch_B.py` rồi phải
   sửa nhãn hiển thị bằng chứng → phải **viết lại renderer từ đầu, chỉ dựa vào file JSON**. Cách
   chữa đúng: giữ renderer tới khi ký chốt, hoặc viết nó ngay từ đầu theo kiểu "đọc JSON → render"
   để có thể tái tạo bất cứ lúc nào.

## Bẫy môi trường tái xác nhận lượt này

- `read_file` báo **binary** cho file `.md` 191 KB sinh trong repo này (đúng pitfall 1). File
  thật sự sạch: 0 byte NUL, 0 control byte, `utf-8` decode OK, `file` nhận "UTF-8 text, very long
  lines". Đọc bằng `python`/`sed`/`grep` theo dải dòng — **đừng kết luận file hỏng, đừng viết lại**.
- Cửa sổ hiển thị của `terminal` nén output dài thành "1 lines output": mọi con số kiểm tra phải
  **in ra file hoặc in 1 dòng tổng kết ngắn** rồi đọc lại, đừng tin payload hiển thị.
