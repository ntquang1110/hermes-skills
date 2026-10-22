# Chất/liều BỊ CHẶN khi thiết kế nghiệm thức tiêu chảy heo con

Chốt 20/10/2026, rút từ 3 lô hoạt chất cửa mở (`fixgby/docs/12-hoat-chat-mo-rong/`). Đây là phần đáng giá nhất của một lô research: **chất đang được bán rộng rãi nhưng dữ liệu nói ngược**. Đối tác lớn sẽ hỏi đúng những chỗ này; nếu đề cương đưa chất vào mà không biết lý do bị chặn thì mất uy tín ngay ở vòng kỹ thuật.

## 7 mục phải ghi nhớ trước khi chốt danh sách chất

1. **Acid lauric trần 2% — KHÔNG cải thiện hàng rào ruột.** `42467834`, 256 heo: độ thấm ruột (TER) xu hướng **giảm**, P=0.071. Đừng đưa vào nghiệm thức; nếu cần dùng MCFA thì dùng dạng monoglyceride.
2. **Arginine — làm TĂNG biểu hiện gen M/N/S của PEDV** (`42450709`). Cấm tuyệt đối không dùng kèm tuyên bố chống PEDV. Đây là loại bẫy nguy hiểm nhất: chất có lợi cho tăng trọng nhưng đẩy nhanh virus.
3. **Glutamine tự do ≠ Gly-Gln.** Khẩu phần lỏng dùng glutamine tự do cho kết quả **ngược chiều** (`40453319`) so với dipeptide Gly-Gln (`40941369`). Chỉ dùng Gly-Gln.
4. **PPMS (potassium peroxymonosulfate) — bằng chứng chỉ trên TGEV / PRCV, KHÔNG có trên PEDV.** Không được suy rộng sang PEDV.
5. **ZnO liều dược lý (hàng nghìn ppm) bị EU cấm từ 2022.** Nếu cần kẽm: kẽm lactate, hoặc ZnO vi nang **≤ 800 ppm** (mức đã thử trên heo).
6. **IgY phải khoá CHỦNG.** Nhiều bài dùng kháng thể đặc hiệu một chủng (ví dụ ETEC K88), không bao phủ chủng thực địa. Khi duyệt đề cương: hỏi **hiệu giá + chủng đích + lô trứng**, không nhận tên chung "IgY".
7. **Tannin liều cao phản tác dụng.** Trên ~0,5% khẩu phần giảm tăng trọng và mất tác dụng chặn khuẩn — liều hiệu quả sát liều hại. Cặp đã có nguồn mạnh: Ca-butyrate + chiết tannin trên 72 heo cai sữa (`34237915`, giảm tiêu chảy tương đương colistin 40 mg/kg).

Hai mục liên quan cần nhớ khi đọc bài: **butyrate phải có vỏ** (dạng không bọc bị hấp thu/hủy trước ruột non — thiết kế đo trực tiếp độ thấm ruột ở `41739762`), và **phân biệt ZnO dược lý với ZnO cơ học hoá** trong mọi bảng liều.

## Pháp lý — 57 chất rơi vào đâu

Đối chiếu Phụ lục VI TT 21/2019 (`fixgby/docs/12-hoat-chat-mo-rong/data-phu-luc-VI-tt21-2019.txt`):

| Đường vào | Số chất | Ghi chú |
|---|---|---|
| Tên riêng trong danh mục | 32 | acid hữu cơ, MCFA C8–C10, tributyrin, MOS, kẽm, men vi sinh, khoáng sét, carvacrol, thymol, glycyrrhizin |
| Dòng thảo dược mở | 13 | tannin hạt dẻ, berberine, baicalin, houttuynia, yucca |
| Mục II.6 (thực phẩm hợp pháp tại VN) | 5 | IgY lòng đỏ trứng, chitosan, GOS, scFOS |
| Mục III (khảo nghiệm / đề tài KHCN cấp Bộ) | 2 | Akkermansia, bacteriophage |
| KHÔNG phải nguyên liệu TĂCN | 5 | sodium chlorate, chlorine dioxide, PPMS, acid peracetic, nước điện phân — là việc **sát trùng**, làn khác, không trộn vào cám |

**Khi tra danh mục, phải đọc NGỮ CẢNH dòng khớp, không đếm hit.** Sáu dương tính giả thật: `Galacto` khớp `alpha-Galactosidase` (enzyme) chứ không phải GOS · `oligosaccharid` khớp MOS/IMO chứ không phải scFOS · `Eucalyptol` 0 hit nhưng `1,8-Cineole` CÓ · `huyết` khớp `bột huyết` chứ không phải plasma/SDPP · `Lauric acid` CÓ nhưng monolaurin không có tên riêng.

## Ba nghiệm thức bản chốt (mẫu để tái dùng cấu trúc)

| NT | Cách chặn | Thành phần | Đường vào |
|---|---|---|---|
| NT1 | Chặn bám dính, trước khi mầm bám | MOS 2 kg/tấn + tannin hạt dẻ 1–2 kg/tấn | tên riêng + dòng thảo dược mở |
| NT2 | Chặn sau khi đã bám, sửa môi trường ruột | butyrate natri bọc lipid + monoglyceride MCFA C8–C10 | tên riêng |
| NT3 | Miễn dịch niêm mạc (cửa vaccine tiêm không vào) | IgY kháng ETEC K88 + scFOS giữ IgA tiết | mục II.6 |

IgA tiết trong phân là chỉ tiêu bắt buộc cho NT3 — thiếu là NT3 không chứng minh được gì.
