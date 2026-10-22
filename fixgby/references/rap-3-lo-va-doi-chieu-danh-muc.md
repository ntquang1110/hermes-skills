# Ráp 3 lô hoạt chất + đối chiếu danh mục nguyên liệu

Chốt 20/10/2026. Bước nối giữa 3 lô subagent (`docs/12-hoat-chat-mo-rong/batch-lo-*`) và bản chốt nghiệm thức.

## 1. Ráp lô — số phải tự đếm, không chép self-report

| Chỉ số | Giá trị thật |
|---|---|
| Chất trong 3 lô | 18 + 19 + 20 = **57** |
| Thẻ hiển thị trên trang | **58** — `hon-hop-acid-huu-co-monoglyceride` thuộc 2 cửa (C và B) nên đứng 2 chỗ; đúng thiết kế, không phải lỗi |
| PMID sau khi hợp nhất | **64** (subagent tự báo 24 + 20 + 23 = 67 — chênh 3 vì cùng một bài nằm ở nhiều lô) |
| Verify độc lập 1 vòng Europe PMC `EXT_ID` | **64/64** hitCount=1, pmid khớp |
| `in_vivo_heo` | **52 / 57** |

Trùng liên lô phải dedupe trước khi đếm: `glycyl-glutamine` (lô 1 cửa A + lô 2 cửa B), `sodium-butyrate` (lô 1 + lô 2), `MOS` (lô 1 + lô 3), `IgY` (lô 1 + lô 3), `berberine` (lô 2 + lô 3 hai entry). Berberine xuất hiện **3 entry** dưới 3 tên khác nhau ⇒ dedupe phải theo **hoạt chất gốc**, không theo `id`.

## 2. Đối chiếu danh mục — grep phải kèm ĐỌC NGỮ CẢNH

Nguồn: `docs/12-hoat-chat-mo-rong/data-phu-luc-VI-tt21-2019.txt` (Phụ lục VI TT 21/2019, trích từ bản gốc PDF). Cách làm: mỗi chất một bộ khoá, grep không phân biệt hoa thường, **in ra dòng khớp cắt 60 ký tự hai bên** rồi tự đọc.

Sáu dương tính giả đã bắt được bằng cách đọc ngữ cảnh — `re.search` trả hit cho cả 6:

| Truy vấn | Thứ thật sự khớp | Kết luận đúng |
|---|---|---|
| `Galacto` | `alpha-Galactosidase` (enzyme) | **GOS KHÔNG có tên riêng** — phải đi mục II.6 |
| `oligosaccharid` | `Mannan Oligosaccharide`, `Isomaltooligosaccharide` | **scFOS KHÔNG có tên riêng** — phải đi mục II.6 |
| `Eucalyptol` | 0 hit | nhưng **`1,8-Cineole` CÓ** trong nhóm chất tạo mùi ⇒ eucalyptol hợp lệ dưới tên 1,8-Cineole |
| `humate` | `Sodium Humate` | **CÓ** (nhóm chất kết dính) |
| `huyết` | `bột huyết` (blood meal) | SDPP / huyết tương sấy phun **không có tên riêng** ⇒ ghi "một phần" |
| `Lauric` | `Lauric acid`, `Diglycerides of Lauric acid` | monolaurin / GML **không có tên riêng** ⇒ ghi "một phần" |

Kết quả chốt 57 chất:

- **32 có tên riêng** trong PL6, dùng được ngay
- **13 đi qua dòng thảo dược mở** (`sản phẩm thảo dược, hoạt chất từ thảo dược`): tannin hạt dẻ, berberine, baicalin, houttuynia, yucca…
- **5 qua mục II.6** (nguyên liệu đang là thực phẩm hợp pháp tại VN): IgY lòng đỏ trứng, chitosan, GOS, scFOS, hỗn hợp phytogenic
- **2 qua mục III** (công nhận từ khảo nghiệm / đề tài KHCN cấp Bộ–quốc gia): Akkermansia, bacteriophage
- **5 KHÔNG phải nguyên liệu TĂCN** — là việc sát trùng, làn khác: sodium chlorate, chlorine dioxide, PPMS, acid peracetic, nước điện phân

**Luật:** đếm hit KHÔNG đủ. Phải in dòng khớp kèm ngữ cảnh và tự đọc, vì tên enzyme / tên loài / từ đồng âm nằm rải trong danh mục. Cùng họ với pitfall 20 — bảng ánh xạ im lặng là kiểu hỏng tệ nhất.

## 3. Ba nghiệm thức chốt

Tiêu chí cứng: bằng chứng **thử trực tiếp trên heo**, **có đường vào danh mục**, và **mỗi nghiệm thức là một cách chặn KHÁC NHAU** — không phải ba biến thể của cùng một cách.

| NT | Cách chặn | Thành phần | Đường vào danh mục |
|---|---|---|---|
| NT1 | Chặn bám dính (trước khi mầm bám) | MOS 2 kg/tấn + tannin hạt dẻ 1–2 kg/tấn | MOS tên riêng; tannin qua dòng thảo dược mở |
| NT2 | Chặn sau khi đã bám, sửa môi trường ruột | butyrate natri bọc lipid + monoglyceride MCFA C8–C10 | cả hai có tên riêng |
| NT3 | Miễn dịch niêm mạc (cửa vaccine tiêm không vào được) | IgY kháng ETEC K88 + scFOS giữ IgA tiết | cả hai qua mục II.6 |

Chỉ tiêu **IgA tiết trong phân** là bắt buộc cho NT3 — thiếu nó thì NT3 không chứng minh được gì.

## 4. Bảy cảnh báo chặn dùng sai (phần đáng giá nhất của lô)

1. **Acid lauric trần 2%** — 256 heo, không cải thiện hàng rào ruột, độ thấm xu hướng tăng (P=0.071). Không đưa vào danh sách.
2. **Arginine** — làm **tăng** biểu hiện gen M/N/S của PEDV. Cấm bán kèm tuyên bố chống PEDV.
3. **Glutamine tự do** trong khẩu phần lỏng cho kết quả **ngược** với dipeptide Gly-Gln. Chỉ dùng Gly-Gln.
4. **PPMS** — bằng chứng chỉ trên TGEV/PRCV, **không có trên PEDV**.
5. **ZnO liều dược lý** — EU cấm từ 2022. Chỉ kẽm lactate hoặc ZnO vi nang ≤ 800 ppm.
6. **IgY** — nhiều bài chỉ dùng kháng thể đặc hiệu một chủng (K88), không bao phủ chủng thực địa. Phải hỏi hiệu giá và chủng đích.
7. **Tannin liều cao** — trên 0,5% giảm tăng trọng và mất tác dụng chặn khuẩn. Liều hiệu quả sát liều hại.

Ba chất nằm **sát VÙNG CẤM** phải giữ bullet `rủi ro` nêu ranh giới (xem pitfall 41(d)): berberine ↔ `app` amidan, hỗn hợp phytogenic ↔ `pmult` khoang mũi, yucca ↔ `mhp` phục hồi lông mao.

## 5. File ra

- `04-bang-tong-hop.md` (84 KB) + `.json` — 57 chất, mỗi chất 1 thẻ, sinh từ một generator duy nhất (luật pitfall 40)
- `visual/hoat-chat-mo-rong.html` (91 KB, 58 thẻ, 0 bảng, mobile ≥12px) → `preview.thefirstonly.com/em5pwyrmh21q`
- `03-de-cuong-thu-nghiem-v1.md` đã gạch 2 việc "còn phải chốt" và chèn mục "Ba nghiệm thức bản chốt"
