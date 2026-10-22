# Lô hoạt chất mở rộng (`docs/12-hoat-chat-mo-rong/`) — convention + checklist

Áp dụng khi được giao "tìm N hoạt chất cho CỬA X" trong dự án fixgby.

## 1. Đọc trước, đúng thứ tự (bắt buộc)

1. `docs/12-hoat-chat-mo-rong/00-cua-mo.md` — bản đồ cửa mở (A–E), **VÙNG CẤM**, danh sách **26 nguyên liệu nhà**.
2. `docs/12-hoat-chat-mo-rong/01-schema-hoat-chat.md` — schema JSON + luật cứng.

Không tự đặt schema mới; không tự nghĩ ra tên cửa.

## 2. Ranh giới lô

- **1 lô = 1 cửa.** Không nhét cửa khác vào mảng `cua` kể cả khi hoạt chất có tác dụng phụ
  (ví dụ acid formic acid hóa nước uống cũng ảnh hưởng Cửa D — vẫn ghi `["A"]` và nêu
  ở `rui_ro`/`ly_do_lan`). Parent ráp trang, không phải mình.
- Không viết file tổng hợp. Chỉ 2 file: `batch-lo-<k>-<ten>.md` + `.json`.

## 3. JSON là nguồn duy nhất, MD sinh ra từ JSON

Dựng dict dữ liệu → `json.dump` → render MD bằng template vòng lặp. Khi phải sửa một trường
(số liệu, mức bằng chứng), sửa dict rồi sinh lại cả hai file — không sửa tay MD rồi lệch JSON.
Chuẩn hoá số (dấu thập phân, dấu nghìn) bằng hàm trên cả cây dict, không bằng sed lên text.

## 4. Checklist luật cứng — chạy TRƯỚC khi ghi file

- [ ] Mọi PMID verify qua Europe PMC (`hitCount == 1`, pmid khớp) — dùng
      `pubmed-evidence-research/scripts/verify_pmid_claims.py --pmids ...`. PMID bịa = loại cả lô.
- [ ] Mọi con số trong `mo_ta`, `lieu`, `hieu_qua_dinh_luong`, `co_che` khớp `abstractText`
      của **chính** PMID được trích (chạy chế độ `--claims`/`entries` của script trên).
      Cẩn thận: có số nằm ở ô cảnh báo (`rui_ro`) nhưng trích từ bài khác trong entry — phải
      thêm bài đó vào `bang_chung` của entry, nếu không là trích dẫn mồ côi.
- [ ] `in_vivo_heo` chỉ khi có thí nghiệm trên heo sống. Thử trên *hỗn hợp chứa* hoạt chất
      vẫn tính, nhưng phải nói rõ là hỗn hợp/pha trộn.
- [ ] `nham_diem_cat` phải là **một dòng nguyên văn** trong mục CỬA X của `00-cua-mo.md`
      (kiểm tự động: `line in open("00-cua-mo.md").read()`).
- [ ] Đích chặn thuộc MẦM hoặc LÒNG RUỘT, không phải phân tử cấu trúc của tế bào heo (VÙNG CẤM).
- [ ] Không đề xuất kháng sinh / hormone / chất cấm. Được phép *mô tả* đối chứng dương của bài
      (ví dụ colistin 40 mg/kg) như số liệu của nghiên cứu, nhưng không được đề xuất dùng.
- [ ] ≥15 hoạt chất, ≥5 `in_vivo_heo`.
- [ ] `trong_26` đối chiếu danh sách 26 nguyên liệu nhà ở cuối `00-cua-mo.md`.
- [ ] Mọi ô ghi trong `tag_H` thì giá trị của ô đó **phải chứa `chua_co`** (chuẩn hoá: prepend
      `chua_co — ` giữ phần giải thích). Đếm `so_o_tag_H` và ghi vào header MD.

## 5. Trung thực khi khớp một phần (điểm dễ nói quá nhất)

Nhiều dòng điểm cắt hẹp hơn bằng chứng (ví dụ dòng nói *lớp nhầy/mucin* nhưng bài chỉ đo
liên kết chặt, `MUC2`, tế bào hình đài, chiều cao nhung mao). Cách xử lý đúng:

- Giữ nguyên văn dòng điểm cắt làm `nham_diem_cat` (để khớp luật), mô tả `dich_chan` đúng
  thứ được đo, và ghi thẳng vào `rui_ro`: *"khớp một phần: điểm cắt nói về lớp nhầy, bài chỉ đo
  X — cần thử in vivo có đọc mucin"*.
- Không nâng cấp ngầm từ "tăng tế bào hình đài" thành "dày lớp nhầy".

## 6. Phát hiện âm tính không được làm hoạt chất

Nếu bài cho thấy hoạt chất **không** cải thiện đích (ví dụ acid lauric trần 2%: TER xu hướng
giảm, P=0.071, PMID 42467834): **không** liệt kê nó như một hoạt chất. Đưa thành cảnh báo có
nguồn nằm trong `bang_chung` + `rui_ro` của entry họ hàng (MCFA/monoglyceride) và ghi lại ở
`## Phụ lục B — PMID dùng làm cảnh báo`. Danh sách ngắn mà thật tốt hơn danh sách đủ số mà độn.

## 7. Khung file

MD: header (số hoạt chất · số `in_vivo_heo` · số ô `tag_H` · số PMID verify) → bảng tổng hợp
(#, tên, nhóm, điểm cắt nhắm, mức bằng chứng, trong 26, PMID) → mỗi hoạt chất một mục
(tên khác, nhóm/cửa/chặng/trong_26, điểm cắt nhắm nguyên văn, đích chặn, cơ chế, mức bằng chứng,
đã bán ở, đường dùng, tên thương mại, lý do lân, liều đã dùng, hiệu quả định lượng, chi phí,
bằng chứng theo PMID, rủi ro, tag_H) → Phụ lục A (các dòng điểm cắt đã dùng) → Phụ lục B
(cảnh báo) → Ghi chú lô (các giới hạn kiểm chứng: số viết bằng chữ trong abstract, p-value bị
Europe PMC cắt ký hiệu, v.v.).

## 8. Rủi ro đã gặp ở Lô 1 (Cửa A)

- Cửa A chỉ có 19 điểm cắt, trong đó **11/18 hoạt chất cùng dồn vào dòng mucin** → MD phải nêu
  rõ đây là điểm nghẽn: nhiều hoạt chất nhưng cùng một mắt xích, thí nghiệm in vivo trong dự án
  nên đo mucin trực tiếp chứ không chỉ đọc chỉ số phụ.
- Nhóm "miễn dịch sữa (IgA/sIgA)" ở **Lô 1** chỉ đạt mức gián tiếp (scFOS làm tăng IgG/TGF-β1
  sữa đầu, không phải IgA; A. muciniphila cơ chế trên chuột) → đừng gộp chung nhóm này vào kết
  luận "đã chặn được điểm cắt miễn dịch".
  **CẬP NHẬT 21/10/2026 — câu này KHÔNG được đọc thành "không chất nào có IgA niêm mạc".**
  Rà lại toàn bộ thì **Bacillus phủ được cửa C ở bậc L2** (3 nghiên cứu đo IgA tiết trong PHÂN
  trên heo), nên định đề "57 hoạt chất không có chất nào có L2 cho miễn dịch niêm mạc" đã hết
  đúng. Xem mục 9.
- ZnO liều dược lý bị EU cấm từ 2022 → chỉ đề xuất vi nang liều thấp / kẽm lactate 600–800 ppm
  và ghi rõ trong `rui_ro`.

## 9. Cửa C đã có bằng chứng — và "câu hỏi BẰNG CHỨNG cho một CỬA" là một loại việc riêng

Chi tiết đầy đủ (bảng PMID, liều, chỉ tiêu thay thế từng bài, số chốt):
`references/no-01-bacillus-iga-bang-chung-cua-c.md`.

**Chốt:** Bacillus probiotic **đã được đo IgA tiết trong phân trên HEO** — 3 nghiên cứu, 2 bài có
*B. subtilis* đích danh. Mạnh nhất `40821810`: *B. subtilis* DSM5750 + DSM27273 + *B. licheniformis*
DSM5749 (2:1:1), 360 heo con cai sữa, **liều 200 mg/kg cám = 0,20 kg/tấn cám trùng đúng liều
premix của dự án**, sIgA phân bằng ELISA ↑ ngày 42 (P = 0,014). ⇒ **Bacillus đứng được ở cửa C ở
bậc L2**; các cửa A/B/D vẫn phủ như cũ.

**Luật khi nhận một câu hỏi bằng chứng cho một cửa** (khác hẳn việc đi tìm hoạt chất mới):

1. **Thang 4 MỨC, không trộn:** IgA tiết trong phân (mức 1, tính cho cửa C) > IgA đặc hiệu kháng
   nguyên trong phân do **vắc-xin** (mức 2, KHÔNG tính) > sIgA mô/chất chứa ruột (mức 3) >
   IgA huyết thanh/huyết tương (mức 4). Cùng thang này dùng cho mọi chỉ tiêu niêm mạc khác.
2. **"Bài tổng quan CÓ TỒN TẠI" ≠ "bài tổng quan CÓ ĐO chỉ tiêu mình cần" — hai phép kiểm riêng.**
   Khi đề bài nói *"có một bài tổng quan nói X"*, phải (a) verify sự tồn tại bằng `EXT_ID`
   (không thấy thì viết thẳng **KHÔNG TÌM THẤY**, cấm bịa); (b) lấy `fullTextXML` của PMCID rồi
   **đếm cụm từ** của chỉ tiêu đó **cộng một cụm đối chứng rộng**. Bài `42450761` (tổng quan
   29 nghiên cứu *B. subtilis*, *Animals* 2026, PMC13359635) **có thật** nhưng toàn văn có
   **0 lần** `fecal IgA` / `sIgA` / `secretory` — 41 lần `fecal` đều là *score/microbiota/
   shedding/SCFA*. ⇒ Trích bài đó cho tăng trọng–tiêu chảy thì đúng; trích cho miễn dịch niêm mạc
   thì **SAI**. Bằng chứng cửa C nằm ở các bài **độc lập, ngoài** 29 nghiên cứu đó.
3. **Chỉ được kết luận ở mức "bài KHÔNG BÁO CÁO chỉ tiêu X".** Muốn nói "không nghiên cứu gốc nào
   đo X" thì phải mở dữ liệu gốc của từng bài — không được nâng cấp suy đoán.
4. **Hit trong truy vấn chủ đề ≠ nghiên cứu đo chỉ tiêu đó.** `31282365` khớp truy vấn
   "fecal sIgA + Bacillus" và có chữ "phân", nhưng đó là **IgA đặc hiệu PEDV do vắc-xin** (mức 2).
   Phải ghi cảnh báo trong cả `.md` và `.json`, không để người đọc sau tự nhầm.
5. **Đối chứng kỹ thuật rất đáng giá:** một bài **không phải Bacillus** đo cùng chỉ tiêu trên cùng
   loài (`39528052` — *Akkermansia*, SIgA phân heo con, **7,59 µg/mg**, P = 0,002) chứng minh
   **phép đo khả thi và có đơn vị định lượng**. Đưa vào bảng nhưng ghi rõ "không phải Bacillus".
6. **Mâu thuẫn giữa loài thì GHI RA, không chốt chiều:** Bacillus **tăng** IgA phân ở heo
   (`17760301`) nhưng **giảm 24,24%** ở người (`40826150`). Đây là câu hỏi bằng chứng — cấm suy từ
   cơ chế sang kết luận. Đưa vào mục "Việc còn nợ".
7. **Liều không có trong abstract ⇒ `chua_co_nguon`**, không suy từ chủng hay từ bài khác; và
   luôn **đổi liều về kg/tấn cám** để đối chiếu được với premix của dự án (mg/kg cám × 1 = kg/tấn).

## 10. Khung báo cáo cho câu hỏi bằng chứng theo cửa

Đặt ở `docs/14-cong-thuc-co-ban/`, tên `no-<NN>-<chủ-đề>.md` + `.json` cùng tên. MD ~80–150 dòng:
**kết luận 3 dòng ở đầu** → bảng Markdown **tối đa 7 cột** chia nhóm (A loài đích có đo chỉ tiêu ·
B loài đích chỉ có chỉ tiêu thay thế · C loài khác · D bài tổng quan) → mục **"Đọc bảng này thế
nào"** (thang 4 mức + cảnh báo từng bài dễ đọc nhầm) → mục **"Việc còn nợ"**. JSON: mỗi bài một
object với `pmid` · `tieu_de` · `loai` · `chung` · `lieu` · `do_iga_tiet_trong_phan` (+ alias
`do_iga_phan`) · `chi_tieu_thay_the` · `ket_qua` · `da_verify_pmid`. Cấm bảng HTML (luật 0 bảng
của dự án) — nhưng trong **tài liệu `.md`** cho người đọc nội bộ thì bảng Markdown là đúng định dạng.
