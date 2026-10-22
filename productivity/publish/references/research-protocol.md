# Research Protocol — Evidence-Level Critical Review

Format chuẩn cho các bài research sâu trong nhóm "Hermes- research" và các research khác.

## Cấu trúc bài research chuẩn

### 1. Header
```
🔬 RESEARCH — Tên đề tài | Phản biện độc lập
Badge: LEAD RESEARCH · CÓ TRÍCH DẪN · KHÔNG BIAS
```

### 2. Mục lục
Danh sách các phần chính (có anchor link).

### 3. Nội dung chính — 3 loại block

**📌 CLAIM (Tuyên bố)**
```html
<div class="claim">
  <div class="lab">📌 TUYÊN BỐ</div>
  <p>Nội dung tuyên bố từ nguồn tham khảo hoặc từ thiết kế cũ.</p>
</div>
```

**⚡ REFUTE (Phản biện)**
```html
<div class="refute">
  <div class="lab">⚡ PHẢN BIỆN</div>
  <p>Phân tích phản biện — chỉ ra lỗi logic, thiếu bằng chứng, mâu thuẫn.</p>
</div>
```

**📊 EVIDENCE (Dẫn chứng)**
```html
<div class="evidence">
  <div class="lab">📊 DẪN CHỨNG</div>
  <p>• Tác giả (năm). "Title." <em>Journal</em>, volume: pages.</p>
</div>
```

### 4. Evidence-level Tags (cho mỗi hoạt tính/tuyên bố)

| Tag | HTML | Ý nghĩa |
|-----|------|---------|
| ✅ ĐÃ XÁC NHẬN | `<span class="tag proven">ĐÃ XÁC NHẬN</span>` | Nhiều RCT, meta-analysis, dùng lâm sàng |
| ⚠️ MỘT PHẦN | `<span class="tag partial">MỘT PHẦN</span>` | Có RCT nhỏ, in vitro + in vivo, cần thêm |
| ❌ SUY DIỄN | `<span class="tag speculative">SUY DIỄN</span>` | In vitro, chọn lọc công bố, chưa in vivo |
| 💊 DÙNG LÂM SÀNG | `<span class="tag clinical">CÓ RCT</span>` | Có thử nghiệm lâm sàng |
| 💰 THỊ TRƯỜNG | `<span class="tag market">Thị trường</span>` | Có giá trị thương mại |

### 5. Bảng so sánh cuối bài

Mỗi bài research có bảng tóm tắt "Tỉ lệ tín/tạp":

| Thành phần | % | Phân loại |
|---|---|---|
| Phần đã biết/đúng | 10-30% | Mô tả ngắn, nguồn |
| Phần suy diễn/tranh cãi | 50-80% | Mô tả, mức bằng chứng |
| Phần sai/thương mại hóa | 5-20% | Cảnh báo |

### 6. Citation format

```
<div class="cite">[Tác giả (năm), <em>Journal</em>, volume: pages]</div>
```

Luôn ưu tiên:
- Peer-reviewed journals (Nature, Science, J. Hazardous Materials, v.v.)
- Sách giáo trình chuẩn (Feynman, Griffiths, Atkins, v.v.)
- WHO/EPA/EFSA reports cho QCVN
- Tránh: blog, Wikipedia (dùng để tra cứu nhanh, không dùng làm dẫn chứng chính)

## Quy tắc phản biện

1. **Phân biệt "hiện tượng có thật" với "giải thích cơ chế".** Hiện tượng có thể đúng, nhưng cách giải thích có thể sai.
2. **Luôn đưa ra giải thích thay thế** (Occam's razor). Nếu lý thuyết đã biết giải thích được, không cần giả thuyết mới.
3. **Chỉ ra mâu thuẫn nhiệt động lực học** — đây là điểm yếu phổ biến của các giả thuyết phi chuẩn.
4. **Phân biệt mức bằng chứng:** in vitro ≠ in vivo ≠ RCT ≠ meta-analysis ≠ lâm sàng.
5. **Cảnh báo thương mại hóa** — nếu có sản phẩm bán ra trước khi có bằng chứng độc lập, đó là RED FLAG.

## Mẫu verdict cuối bài

```html
<div class="verdict">
  <h3>🎯 KẾT LUẬN</h3>
  <p>Kết luận ngắn gọn, có con số tỉ lệ phần trăm.</p>
</div>
```

## Mobile-Formatting Rules (quan trọng — user yêu cầu)

**User đã nhiều lần phàn nàn về table ngang trên mobile.** Tuân thủ tuyệt đối:

1. **Card layout thay vì table.** Biến mỗi mục thành `div.card` với border-left màu (xanh dương=thông tin, vàng=giá trị, đỏ=cảnh báo). Mỗi card chứa: `.t` (tiêu đề), `.m` (mô tả), `.v` (giá trị).

2. **Table chỉ dùng cho &lt;5 dòng dữ liệu đơn giản** (2-3 cột). Nếu table &gt;5 dòng hoặc &gt;3 cột → phải chuyển thành card.

3. **Responsive breakpoints:**
   - Mặc định: card 1 cột (mobile-first)
   - &gt;700px: card có thể flex-wrap 2 cột nếu ngắn
   - &gt;1000px: card 3 cột

4. **CSS tối thiểu cho mobile:**
   ```css
   * { box-sizing: border-box; }
   body { font-size: 15px; line-height: 1.6; padding: 0 0 30px; }
   .card { padding: 10px 12px; margin: 5px 0; border-radius: 8px; border-left: 3px solid ...; }
   ```

5. **KHÔNG dùng:**
   - `overflow-x: scroll` trên table (user ghét phải kéo ngang)
   - Bảng có &gt;3 cột trên mobile
   - Font-size &lt;13px

## Google Sheet Export Workflow

Khi user yêu cầu tạo Google Sheet với dữ liệu tabular, tuân thủ:

1. **Dùng tiếng Việt cho tiêu đề cột và nội dung** (user đã yêu cầu rõ). Không pha tiếng Anh.
2. **Đơn chất (nguyên tố), KHÔNG phải oxide.** VD: Ca, Mg, K — không phải CaO, MgO, K₂O.
3. **Phân nhóm theo chủ đề** (Khoáng / Hóa lý / KLN / Đất hiếm / Kim loại quý).
4. **Kèm cột chi phí kiểm nghiệm** (user muốn biết giá từng mục).
5. **Dùng tài khoản @kiemsaphia.com** — cần kiểm tra token trước, refresh nếu hết hạn.
6. **Tạo 1 file nhiều sheet** — không tạo nhiều file riêng lẻ.
7. **Cấu trúc sheet điển hình:** (a) dữ liệu chính, (b) dữ liệu phụ, (c) tổng hợp & hướng dẫn sử dụng.
8. **Khi tạo SOW cho phòng thí nghiệm:** thêm cột "Phương pháp phân tích", "PP phá mẫu", "QC yêu cầu", "LOD".
