# Vua Kiềm — Trial pipeline (as of 2026-08-14)

## Hoàn cảnh

- **Bên cung cấp:** Công ty Vua Kiềm (tên công ty: Manna Đất Vàng). Sản phẩm thử nghiệm: Kiềm EZ Tái Sinh 80 (EZ80), liều 5 kg/tấn (0,5%), giá bán 125.000đ/kg.
- **Đối tác thử nghiệm:** Công ty Cổ phần Xuân Thiện Thanh Hóa — closed herd, nuôi từ nái → heo con → thịt xuất bán.
- **Đề cương v2** (bản đầy đủ, đã tạo): `D:\VuaKiem\portfolio\De_cuong_thu_nghiem_EZ80_Xuan_Thien_v2.docx` — script tạo: `make_decuong.py` cùng thư mục.
- Trello card: "TSK - Đề cương thử nghiệm EZ80 tại Xuân Thiện" (board Vua Kiềm - Execution, To Do) — docx đã đính kèm lên card.

## Đề cương v2 đã bổ sung so với bản gốc MANNA-XT

| Khoản mục | Bản gốc | v2 |
|---|---|---|
| Chỉ số ASF | Không | PCR định kỳ 2 tuần/lần cả 2 lô, ghi ngày dương tính đầu tiên |
| Quy mô | Để trống | Nái 20/lô (2 ô × 10), thịt 60/lô (3 ô × 20) |
| Giai đoạn | Mơ hồ | Nái 2 tháng → thịt 4 tháng (đủ vòng nuôi) |
| An toàn | Không | Dư lượng, chất lượng thịt |
| Thống kê | Không | T-test/ANOVA, p<0,05 |
| Tiêu chí thành công | Không | FCR −3%, ADG +3%, thú y −10% |
| Dữ liệu & công bố | Không | Sở hữu chung, công bố cần 2 bên đồng ý |
| Chi phí | Mơ hồ | Vua Kiềm: sản phẩm + PCR; Xuân Thiện: chuồng/giống/TACN/nhân công |
| Xử lý dịch ASF | Không | Dừng thử khi công bố dịch, giữ số liệu trước khi dừng |

## Các trial khác trên board (context)

- PRJ - Thử nghiệm InVitro / InVivo anh Lâm VNUA (đang Doing)
- PRJ - Thử nghiệm phòng Dịch tả nội bộ (Blocked, due 31/10)
- PRJ - Thử nghiệm phòng XYZ nội bộ, PRJ - Thử nghiệm InVivo anh Lâm VNUA (To Do)

Kết quả lab VNUA 2022 + lứa thực địa âm tính = bằng chứng hiện có (dùng trong hồ sơ nhà đầu tư).

## Số liệu thị trường (tính TAM — đã dùng cho investor profile)

- TACN hỗn hợp VN 2025: 22,12 triệu tấn (+2,9%) — nguồn Cục Chăn nuôi & Thú y.
- Thức ăn cho lợn: 52,3% ≈ 11,57 triệu tấn/năm.
- TAM (liều 0,5%): ~58.000 tấn/năm ≈ **7.250 tỷ đ/năm** (giá 125.000đ/kg).
- Công suất hiện tại 300 tấn/tháng = 3.600 tấn/năm ≈ 450 tỷ đ/năm tiềm năng = ~6% TAM.
- Khách hiện tại: 57 người, 20 trang trại dùng thường xuyên; trại thử <100 con.

## Trial EZ-CT888 — Xử lý nước phân thải tại Xuân Thiện (thêm 2026-09-08)

- **Ngữ cảnh:** Khu Biogas, Công ty CP Xuân Thiện Thanh Hóa (xã Minh Tiến, Ngọc Lặc, Thanh Hóa). Báo cáo giai đoạn 1, mốc Ngày 15 (20/08–04/09/2026). Sản phẩm: Bột kiềm EZ-CT888 xử lý nước thải chăn nuôi; CT1 100kg/1.000m³, CT2 150kg/1.000m³, ĐC không xử lý. Giá 180.000đ/kg.
- **Thiết kế:** 3 công thức song song; điểm lấy mẫu M1 (sau tách phân), M2A/M2B (hồ lắng), M3A/M3B (hồ sục khí); mốc đo Ngày 1, 7, 15; chỉ tiêu pH, BOD5, COD, TSS, Tổng N. Cán bộ theo dõi: Phạm Văn Tiến, Lê Ngọc Quân; người viết: Lương Quang Hiệp.
- **Kết quả chính CT2 (ngày 15):** BOD5 M1 220→91 (N1→N15 -59%; riêng N7→N15 785→91 = -88%); TSS M1 1.070→455 (-57%); COD M1 7.580→1.236 (-84%); Tổng N M2A 830→65 (-92%). CT2 tốt hơn ĐC 26/40 lượt so sánh (65%), CT1 16/40 (40%). Chi phí xử lý 27.000đ/m³ vs >50.000đ/m³ hóa chất đang dùng (tiết kiệm ~46%).
- **Nguồn số liệu đầy đủ:** DOCX `doc_22fc7aaf583f_ngày_15_..._CT888.docx` (trong `~/AppData/Local/hermes/cache/documents/`), 14 bảng. Ma trận N1/N7/N15 × ĐC/CT1/CT2: bảng 3=pH, 5=BOD5, 7=COD, 9=TSS, 11=Tổng N; bảng chẵn = % vượt đối chứng; bảng 1 = KPI chính.
- **Bản web:** thư mục `D:/Hermes Proj/xuanthien/` — File B `CT888_baocao_visual.html` (đã thêm mốc Ngày 1 vào 4 biểu đồ + bảng pH đủ N7/N15), publish https://preview.thefirstonly.com/8gkgjtjqbmpn.
