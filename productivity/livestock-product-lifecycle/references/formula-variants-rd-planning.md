# Formula Variants & R&D Planning Pattern

Created 17/09/2026 — after writing 5 product briefs (RESP-HP, GUT-HP, METRI-HP, GROW-HP, GROW-SLEEP-HP) with formula variants.

## When to use

When user asks for R&D direction alongside product briefs: "có bao nhiêu công thức để thử nghiệm", "lên định hướng nghiên cứu phát triển". Create a variant matrix per product line with screening gates.

## Pattern: Variant matrix per product line

Each product line gets 3-5 formula variants that vary 1-2 parameters (ingredient type, dosage, presence/absence of key component). All variants share the same Kiềm Thảo Dược base.

### Template

| CT | Variable A | Variable B | Variable C | Ghi chú |
|----|-----------|-----------|-----------|---------|
| XX-01A | Base dose | Ingredient X | - | Công thức nền |
| XX-01B | High dose | Ingredient X | - | Tăng liều |
| XX-01C | Base dose | Ingredient Y | - | Thay thế thành phần |
| XX-01D | Base dose | Ingredient X | + Additive Z | Thêm bổ sung |
| XX-01E | - | Ingredient X | - | Giảm giá (bỏ component đắt) |

### Screening criteria (G1-G3)

1. **G1 (Nghiên cứu):** Xác định nguồn nguyên liệu, báo giá, lead time
2. **G2 (Phòng thí nghiệm):** Phối trộn thử, kiểm tra pH, độ hòa tan, cảm quan (>=30 người)
3. **G3 (Thử nghiệm trên heo):** Thử trên 10-20 con/CT, đo FCR/ADG/tỷ lệ bệnh

### Ngân sách tham chiếu

~15-25 triệu đ/CT x N CT cho toàn bộ G1-G3.

## Worked example: 5 product lines (17/09/2026)

### 1. RESP-HP (Hô hấp — Bột)
**Thành phần cốt lõi:** Kiềm thảo dược base + Thymol/Eucalyptol + Glycyrrhizin + Propolis

| CT | Tinh dầu | Glycyrrhizin | Propolis | Bổ sung |
|----|----------|-------------|----------|---------|
| RS-01A | Thymol 0.03% + Eucalyptol 0.02% | 0.3% | 0.2% | - |
| RS-01B | Carvacrol 0.03% + Eucalyptol 0.02% | 0.3% | 0.2% | - |
| RS-01C | Thymol 0.03% + Eucalyptol 0.02% | 0.5% | 0.3% | Vitamin C 0.1% |
| RS-01D | Dịch chiết lá hẹ (Allium tuberosum) | 0.3% | 0.2% | - |

**Số CT: 4**

### 2. GUT-HP (Tiêu chảy — Bột)
**Thành phần cốt lõi:** Kiềm thảo dược base + Tannin chestnut + Berberine + Butyrate + Probiotic

| CT | Tannin | Berberine | Butyrate | Probiotic |
|----|--------|-----------|----------|-----------|
| GT-01A | Chestnut 0.2% | 0.10% | 0.15% | - |
| GT-01B | Chestnut 0.3% | 0.15% | 0.2% | - |
| GT-01C | Chestnut 0.2% | 0.10% | 0.15% | Bacillus 10^8 |
| GT-01D | Quebracho 0.2% | 0.10% | 0.15% | - |
| GT-01E | Chestnut 0.2% | - | 0.15% | Bacillus 10^8 |

**Số CT: 5**

### 3. METRI-HP (Viêm tử cung — Nước)
**Thành phần cốt lõi:** EZ67 base + Ích mẫu + Propolis + Curcumin + Vit E/Se

| CT | Thảo dược | Propolis | Curcumin | Bổ sung |
|----|----------|----------|----------|---------|
| MT-01A | Ích mẫu 1% | 1% | 0.3% | Vit E+Se |
| MT-01B | Ích mẫu 1% + Hoàng liên 0.5% | 1% | 0.3% | Vit E+Se |
| MT-01C | Ích mẫu 1% | 2% | 0.5% | Vit E+Se |
| MT-01D | Huyết dụ 1% + Hoàng liên 0.5% | 1% | 0.3% | Vit E+Se |

**Số CT: 4**

### 4. GROW-HP (Sinh trưởng — Bột)
**Thành phần cốt lõi:** Kiềm thảo dược base + Phytase/Xylanase + Betaine + Bacillus

| CT | Enzyme | Betaine | Probiotic | Acid |
|----|--------|---------|-----------|------|
| GR-01A | Phytase+Xylanase | 0.1% | Bacillus 10^8 | - |
| GR-01B | Phytase+Xylanase | 0.15% | Bacillus 10^8 | - |
| GR-01C | Phytase+Xylanase | 0.1% | - | Citric 0.2% |
| GR-01D | Phytase+Protease | 0.1% | Bacillus 10^8 | - |
| GR-01E | Phytase+Xylanase | - | Bacillus 10^8 | Citric 0.2% |

**Số CT: 5**

### 5. GROW-SLEEP-HP (Sinh trưởng + Dễ ngủ — Bột)
**Thành phần cốt lõi:** Kiềm thảo dược base + L-Tryptophan + Mg + Betaine + Enzyme

| CT | L-Trp | Mg | Betaine | Enzyme |
|----|-------|-----|---------|--------|
| GS-01A | 0.15% | MgO 0.1% | 0.1% | Phytase+Xylanase |
| GS-01B | 0.25% | MgO 0.1% | 0.1% | Phytase+Xylanase |
| GS-01C | 0.15% | Mg chelate 0.08% | 0.1% | Phytase+Xylanase |
| GS-01D | 0.15% | MgO 0.1% | - | Phytase+Xylanase |
| GS-01E | 0.15% | MgO 0.1% | 0.15% | Phytase+Xylanase+Protease |

**Số CT: 5**

## Tổng hợp

| Dòng | Mã | Dạng | Số CT |
|------|----|------|-------|
| Hô hấp | RS-01 | Bột | 4 |
| Tiêu chảy | GT-01 | Bột | 5 |
| Viêm tử cung | MT-01 | Nước | 4 |
| Sinh trưởng | GR-01 | Bột | 5 |
| Sinh trưởng + Dễ ngủ | GS-01 | Bột | 5 |
| **Tổng** | | | **23** |
