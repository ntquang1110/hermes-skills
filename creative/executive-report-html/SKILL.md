---
name: executive-report-html
description: "Build formal executive HTML reports for C-level readers."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [html, report, executive, corporate, vietnam, design, trial]
    related_skills: [visual-academic-html, impeccable, publish, claude-design]
---

# Executive Report HTML (báo cáo gửi lãnh đạo / đối tác lớn)

## Trigger

User có tài liệu nguồn (báo cáo thử nghiệm DOCX, bảng số liệu) và muốn làm bản trình bày
đẹp, formal để gửi Chủ tịch / CEO / đối tác lớn (vd: báo cáo thử nghiệm EZ-CT888 gửi
Chủ tịch Xuân Thiện). Dấu hiệu: "bản Visualize", "gửi cho Chủ tịch", "formal mà dễ hiểu".
KHÔNG dùng cho bài học thuật KFlow (xem `visual-academic-html`).

## Nguyên tắc gốc — người đọc là người ra quyết định

Chủ tịch tập đoàn KHÔNG đọc báo cáo, ông đọc quyết định. Thứ gửi vào tay ông phải 30 giây
ra quyết định. Cấu trúc "bán ngược" 3 lớp:

1. **Lớp 1 — Kết quả trước**: con số lớn giảm %, sau bao lâu. Đủ để kết luận "có tác dụng".
2. **Lớp 2 — Cách dùng đơn giản hóa**: liều, cách triển khai, không đổi hạ tầng. Ông chỉ cần
   biết "dễ hay khó".
3. **Lớp 3 — Vì sao hiệu quả** (khoa học 1 đoạn, không hơn): cơ chế ngắn + "tích lũy theo thời gian".

Sau đó (nếu có số liệu kinh tế) chèn khối tiền: chi phí hiện tại vs chi phí mới, % tiết kiệm
trực tiếp — đây là đường chốt nhanh nhất với lãnh đạo.

## Định dạng — 2 file, không 1

- **File A — 1 trang tổng kết (A4, in được 1 mặt)**: thứ duy nhất lãnh đạo cần mở. Tiêu đề 1 dòng
  mang con số, 4 số lớn, khối tiền, 1 đoạn ý nghĩa với khách, footer formal.
- **File B — Báo cáo đầy đủ**: cho cấp kỹ thuật/ban môi trường hoặc khi lãnh đạo hỏi sâu.
  Đầy đủ bối cảnh, charts từng chỉ tiêu, bảng so sánh, kết luận, bước tiếp theo.

## Design system (theme corporate sáng — KHÔNG dùng B/W/Y tối của bài academic)

Đã verify với Chủ tịch Xuân Thiện 09/2026. Dùng Be Vietnam Pro (hỗ trợ tiếng Việt đủ dấu):

```yaml
colors:
  forest: "#1D5C3E"        # primary (xanh rừng)
  forest-deep: "#143F2B"   # footer / block đậm
  gold: "#C89B3C"          # accent (thương hiệu Đất Vàng)
  paper: "#FBFBF8"         # nền giấy
  ink: "#16211C"           # text chính
  ink-alt: "#2E3B34"
  muted: "#5C6B63"
  line: "#E5E7E0"          # hairline
  line-strong: "#D3D8D2"
typography:
  font: "'Be Vietnam Pro', system-ui, sans-serif"   # google fonts link trong <head>
  display: 800, letter-spacing -0.02em..-0.03em
  body: 400/500, 12.5-13.5px
radius: 12 (gom, không lộn xộn)
elevation: hairline chia phần — KHÔNG vừa border vừa shadow (ghost card)
```

Chống AI-tells (đi qua skill `impeccable`):
- KHÔNG kicker/eyebrow trên heading (bỏ "KẾT QUẢ SƠ BỘ GIAI ĐOẠN 1" thành dòng doc trong masthead)
- KHÔNG số section 01/02/03
- KHÔNG emoji; ✓ dùng SVG circle check inline
- KHÔNG card lồng card; KPI = strip kẻ hairline, số lớn ~30px
- KHÔNG text < 10px; font-size tối thiểu 10.5px cho meta

## Charts — SVG inline, không CSS bars

```js
const CFG = { bod5: {groups: [['Ngày 7',[780,1140,785]],['Ngày 15',[146,122,91]]], max:1200} };
// svgBar(): viewBox 620x240, padL 46, gridlines 4 nấc, 3 cột/group, legend màu:
// ĐC #9DA89F · CT1 #8FBBA4 · CT2 #1D5C3E
```
Mỗi chart 1 khối: h3 + csub (mg/L + ý chính) + svg + note (số đối chiếu + tần suất so đối chứng).
SVG có gridline + trục mg/L + giá trị trên cột + legend — trình bày số thật, không để trống.

## Kiểm tra A4 (File A)

`.page{width:210mm}` — pageH tính được = 1123px @96dpi (297mm A4). Nếu pageH > 1123px tức
tràn sang trang 2 khi in: giảm gap/padding hoặc rút copy.

## Workflow

1. **Đọc nguồn đầy đủ** (read_file docx, đọc cả phần sau nếu truncated) — mọi con số phải từ nguồn.
2. **Hỏi 2-3 con số kinh tế chưa có trong báo cáo**: chi phí hiện tại đơn vị gì (đ/m³?), giá SP,
   công suất xử lý. KHÔNG bịa ra. Tính % tiết kiệm minh bạch (vd 50.000 → 27.000 = ~46%).
3. Xác nhận cấu trúc với user TRƯỚC khi code (user thích duyệt "triển khai đi").
4. Dựng File A + File B theo design system trên, dữ liệu thật từ source.
5. **Audit** (bắt buộc): serve http.server background → browser_navigate → browser_console
   với nội dung `impeccable/scripts/ui-audit.js` → mục tiêu `tells: []`, bodyContrast ≥ 4.5.
6. **Screenshot cho user**: playwright-core .cjs (xem camofox-browser skill) chụp fullPage
   cả 2 file → gửi MEDIA:.
7. **Publish**: `publish` skill scripts/content-upload.py --file (KV). Lưu ý script tự unslop
   (`unslopped: true`) — vẫn OK với thiết kế này. Verify preview HTTP 200 + grep font/svg.

## Pitfalls (thực tế đã gặp)

- **Vision model hết hạn/không nhận image** → đừng bỏ dở audit: chạy ui-audit.js qua
  browser_console (deterministic), screenshot qua playwright, gửi user xem.
- **Browser backend lỗi 500** (localhost:9377): thử DELETE /sessions/<userId> rồi retry;
  port http.server bị 2 PID giữ → kill cả 2 rồi start lại.
- **file:// bị chặn** — luôn serve qua `python -m http.server <port> --bind 127.0.0.1`.
- **content-upload.py tự unslop HTML** — kiểm tra bản publish bằng curl grep (font, svg)
  trước khi báo xong, vì unslop có thể sửa markup.
- User feedback "trông xấu quá" 09/2026 = bản đầu dùng Segoe UI + card + shadow + kicker.
  Từ đó: design system trên là CHUẨN cho mọi báo cáo gửi lãnh đạo. KHÔNG quay lại kiểu cũ.
- Khi hỏi chi phí kinh tế, hỏi ĐƠN VỊ rõ (đ/m³? đ/kg? đ/bao?) — mơ hồ dẫn đến tính sai rồi
  phải hỏi lại. Xác nhận bằng "đúng không?" trước khi đưa vào tài liệu.
- **KHÔNG claim "đạt chuẩn xả thải" khi chưa đạt QCVN** — đối chiếu chuẩn
  (references/qcvn62-wastewater.md) và nói đúng mức: "giảm 84–92% tải ô nhiễm ở đầu hệ thống",
  nêu rõ chỉ số nào đã dưới chuẩn, chỉ số nào còn trên chuẩn. Tránh bị đối tác bắt bài về chuẩn.
- **User nói "giải thích cho anh hiểu"** → publish thành trang HTML riêng (structure: def box +
  cơ chế từng bước + bảng chuẩn), KHÔNG nhúng vào tài liệu gửi đối tác trừ khi user yêu cầu.
- **User hỏi sâu cơ chế sản phẩm** ("tại sao giảm COD/BOD/TSS", "có cách tối ưu không hóa
  chất") → làm 1 trang research riêng với bảng phân loại mức tin cậy từng thành phần
  (ĐÃ CHỨNG MINH / KHẢ DĨ / CẦN KIỂM CHỨNG) — đừng hứa cơ chế chưa có bằng chứng công bố
  (vd: kim loại hiếm La/Ce có tiềm năng nhưng chưa có nghiên cứu ở nước thải chăn nuôi).
  Xem references/ct888-mechanism-and-optimization.md.
- **Ký tự `·` (middle dot) trong --title phá pipeline bash** (`&&` + `grep` → exit 1, mất output).
  Chạy 1 lệnh/1 file hoặc bỏ dấu chấm giữa khỏi title.
- **Đừng dùng urllib POST thẳng /api/store** (bị CF chặn → 403). LUÔN đi qua
  `publish/scripts/content-upload.py` (requests, tự unslop, tự lấy preview_url).

## Điều tra cơ chế + đề xuất thí nghiệm (khi user muốn sâu hơn báo cáo)

Sau khi có báo cáo kết quả, user hay hỏi tiếp: "cơ chế nào làm được việc" và "ngoài tăng liều
ra còn cách tối ưu nào". Pattern đã chạy OK 09/2026:

1. Research cơ chế từng thành phần (web + nguồn mở PMC/nghiên cứu), phân loại mức tin cậy.
2. Giải thích hiện tượng "bất thường" (vd hồ sục khí COD đi ngang) bằng cơ chế sinh khối —
   nhiễu đo, không phải sản phẩm yếu.
3. Đề xuất thí nghiệm so sánh: 4 bể song song (đối chứng / +sục khí / +vi sinh / +liều),
   cùng nguồn nước, đo mốc 0/7/15/30, tiêu chí quyết định từng kịch bản, bảng chi phí.
4. Visualize cơ chế thành trang "chuyện gì xảy ra khi đổ sản phẩm vào bể" — dòng chảy
   Nước bẩn → Rắc SP → Nước sạch hơn, mỗi thành phần 1 thẻ icon + vai trò 1 câu.

## References

- `references/xuan-thien-ct888-case.md` — case cụ thể: báo cáo EZ-CT888 ngày 15 gửi Chủ tịch
  Xuân Thiện (số liệu, cấu trúc 2 file, số kinh tế đã chốt).
- `references/qcvn62-wastewater.md` — QCVN 62-MT:2016/BTNMT (nước thải chăn nuôi): bảng giá trị
  Cột A/B chuẩn BOD5/COD/TSS/Tổng N; cơ chế vì sao BOD/COD/TSS cao là hại (đã research có nguồn).