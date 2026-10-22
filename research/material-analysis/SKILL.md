---
name: material-analysis
description: "Use when: identifying what's inside a raw material sample."
version: 1.0.0
author: Quang
license: MIT
metadata:
  hermes:
    tags: [analytical, chemistry, material, ingredient, sample, lab, spectroscopy]
    category: research
---

# Material Analysis — Phân tích thành phần nguyên liệu

Nạp từ Quang 03/10/2026. Khi cần biết bên trong1 nguyên liệu có gì.

---

## Flow tổng quát

```
1. Xác định câu hỏi: nguyên tố? hợp chất? hoạt chất? định lượng?
2. Lấy mẫu đại diện, đồng nhất, chia mẫu, lưu mẫu gốc
3. Tiền xử lý: nghiền, sấy, chiết, phân hủy, lọc, ly tâm, derivatization
4. Screening nhanh: pH, độ tan, màu, mùi, FTIR, XRF, TLC
5. Tách: GC, HPLC, LC, SPE, sắc ký cột, chưng cất
6. Đo / định danh: MS, NMR, ICP, XRD, SEM-EDS
7. Xác nhận bằng chất chuẩn / database
8. Định lượng + kiểm soát chất lượng + báo cáo
```

---

## I. Flow theo câu hỏi

| Muốn biết | Flow | Kỹ thuật chốt |
|---|---|---|
| **Nguyên tố** | Quan sát → XRF/EDX → phân hủy mẫu → ICP-OES/MS hoặc AAS → IC/CHNS → XRD nếu cần pha tinh thể | XRF, ICP-MS, XRD, IC |
| **Hợp chất** | Độ tan/mùi/pH → FTIR/Raman → TLC → GC-MS hoặc LC-MS → NMR/HRMS → so chuẩn → HPLC/GC định lượng | FTIR, GC-MS, LC-MS/MS, NMR |
| **Hoạt chất** | Bioassay → chiết phân đoạn → sắc ký cột/HPLC → LC-MS/MS + HRMS → NMR → assay định lượng hoạt tính | Bioassay-guided fractionation, LC-MS/MS, NMR |

---

## II. Flow theo loại nguyên liệu

### 1. Nguyên liệu VÔ CƠ

Kim loại, muối, khoáng, oxit, ceramic, thủy tinh.

```
Quan sát: rắn/lỏng, màu, pH, độ tan, từ tính, dẫn điện
XRF/EDX → nguyên tố chính
Nếu cần hàm lượng: phân hủy acid/kiềm nóng chảy → ICP-OES/MS, AAS
Anion: IC, chuẩn độ
Pha tinh thể: XRD
Bề mặt/hình thái: SEM-EDS, XPS
Kết luận: nguyên tố, pha, hàm lượng
```

**Lưu ý:** Hợp kim dùng OES/XRF · Khoáng dùng XRD · Anion dùng IC.

### 2. Nguyên liệu HỮU CƠ

Dung môi, dầu, polymer, chất hoạt động bề mặt, dược phẩm, thuốc BVTV.

```
Độ tan, mùi, khả năng cháy, pH
FTIR/Raman → nhóm chức
Nếu bay hơi: GC-MS
Nếu không bay hơi: LC-MS/MS
Tách: TLC, HPLC, GC, sắc ký cột
Cấu trúc: NMR, HRMS
Định lượng: HPLC/GC với chuẩn
Nếu polymer: GPC/SEC, TGA/DSC, Py-GC/MS
Kết luận: hợp chất, nhóm chức, phân tử lượng, phụ gia
```

**Lưu ý:** GC mạnh cho tinh dầu, dung môi, fatty acid · LC mạnh cho dược phẩm, flavonoid, metabolite.

### 3. Nguyên liệu SINH HỌC

Thực vật, vi sinh, enzyme, protein, DNA/RNA, metabolite.

```
Đồng nhất mẫu, chiết nước/cồn/dung môi hữu cơ
Nếu tìm hoạt chất: bioassay-guided fractionation
Phân đoạn: lỏng-lỏng, SPE, sắc ký cột, HPLC
Hoạt chất: LC-MS/MS, HRMS, NMR
Protein/enzyme: SDS-PAGE, Western blot, LC-MS/MS proteomics, enzyme assay
DNA/RNA: PCR/qPCR, sequencing, điện di
Vi sinh: nuôi cấy, MALDI-TOF, 16S/ITS
Kết luận: loài, hoạt chất, protein, gen, hoạt tính
```

**Lưu ý:** Mẫu sinh học dễ hỏng — cần lạnh, chống phân hủy, kiểm soát vô trùng.

### 4. Hỗn hợp PHỨC TẠP

Thực phẩm, đất, môi trường, dịch chiết, sản phẩm tự nhiên.

```
Lấy mẫu đại diện, đồng nhất, chia phần
Screening: pH, độ ẩm, tro, FTIR, XRF, TLC
Tách sơ bộ: QuEChERS, SPE, lỏng-lỏng, chưng cất
Đa chỉ tiêu: GC-MS/MS, LC-MS/MS, ICP-MS, IC
Non-targeted: HRMS + database + molecular networking
Chemometrics: PCA, PLS-DA để phân nhóm, tìm marker
Xác nhận bằng chuẩn, định lượng
Kết luận: thành phần chính, vi chất, chất ô nhiễm, marker
```

**Lưu ý:** Matrix phức tạp gây nhiễu — phải có blank, spike, nội chuẩn.

### 5. Vật liệu KỸ THUẬT

Hợp kim, composite, bán dẫn, pin, xúc tác, polymer kỹ thuật.

```
Kiểm tra cơ lý, dẫn điện/nhiệt, từ tính
FTIR/Raman, XRD, XRF/EDX
Hình thái: SEM/TEM, AFM
Bề mặt: XPS, Auger
Nhiệt: TGA/DSC, DMA
Cơ học: kéo, nén, uốn, mài mòn
Nguyên tố vết: ICP-MS, GD-MS, SIMS
Polymer/composite: Py-GC/MS, GPC/SEC
Kết luận: thành phần, cấu trúc, pha, tính chất
```

**Lưu ý:** Vật liệu kỹ thuật thường cần cả phân tích thành phần và phân tích tính chất.

---

## III. Flow chọn nhanh

| Tình huống | Dùng |
|---|---|
| Chưa biết gì | Quan sát + XRF + FTIR + TLC |
| Rắn vô cơ | XRF → XRD → ICP |
| Lỏng bay hơi | GC-MS |
| Lỏng không bay hơi | LC-MS/MS |
| Có hoạt tính sinh học | Bioassay → LC-MS/MS → NMR |
| Polymer/vật liệu | FTIR + TGA/DSC + SEM + GPC |
| **Mẫu pháp lý** | **Phương pháp chuẩn ISO/ASTM/USP/EP/AOAC · Lab ISO/IEC 17025 · Chất chuẩn · Kiểm soát chất lượng** |

---

## Pitfalls

1. **Không có blank/spike/nội chuẩn** → kết quả không kiểm chứng được, especially matrix phức tạp.
2. **Mẫu sinh hỏng** → cần lạnh, chống phân hủy, kiểm soát vô trùng ngay từ bước lấy mẫu.
3. **Dùng GC cho chất không bay hơi** → mất mẫu, kết quả sai. LC cho chất không bay hơi.
4. **Bỏ qua screening** → đi thẳng LC-MS tốn kém, dễ miss thành phần chính.
5. **Không có chất chuẩn** → định danh dựa trên library match, sai số cao. Luôn confirm bằng chuẩn.
6. **Mẫu pháp lý thiếu ISO/ASTM** → kết quả không có giá trị pháp lý. Dùng phương pháp chuẩn, lab ISO/IEC 17025.
