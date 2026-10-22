# SOP Documentation HTML Pattern

Chuyển đổi bộ quy trình (SOP) dạng văn bản thành HTML tương tác với visual flow, checklist, và kịch bản hỏi đáp. Pattern này dùng cho tài liệu nội bộ, đào tạo nhân viên, chuẩn bị thanh kiểm tra.

## Khi nào dùng

- User đưa file SOP (.docx/.md) và muốn "dựng HTML cho team đọc"
- User cần tài liệu vừa có text, vừa có visualize, vừa có checklist kiểm tra
- Cần kịch bản hỏi đáp mô phỏng thanh tra kèm theo

## Cấu trúc HTML

### 1. Tab Navigation
Mỗi SOP là một tab. Dùng button + data-tab pattern:
```html
<button class="tab-btn active" data-tab="sop01">SOP 01</button>
<button class="tab-btn" data-tab="sop02">SOP 02</button>
```
Tab pane tương ứng:
```html
<div class="tab-pane active" id="sop01">...</div>
<div class="tab-pane" id="sop02">...</div>
```
JS tab switching: querySelectorAll + classList toggle.

### 2. Mỗi SOP gồm 2 cột
- **Trái:** Visual flow diagram (`.flow`) — quy trình dạng sơ đồ
- **Phải:** Text chi tiết (`.sop-text`) — bảng, trách nhiệm, biểu mẫu, checklist

### 3. Visual Flow
Dùng `.flow-steps` với numbered boxes và arrows cho flow ngang:
```html
<div class="flow-step">
  <span class="box highlight">B1</span>
  <span class="arrow">&rarr;</span>
  <span class="box">B2</span>
</div>
```
Dùng `.flow-v` với `.flow-v-row .step` cho flow dọc (nhiều nhánh).

### 4. Checklist
Mỗi SOP kết thúc bằng checklist cho kiểm tra:
```html
<div class="checklist">
  <div class="checklist-item">
    <span class="cb"></span> COA & hồ sơ pháp lý NCC đầy đủ?
  </div>
</div>
```

### 5. Biểu mẫu tags
Danh sách biểu mẫu dùng inline monospace tags:
```html
<div class="forms-list">
  <span class="fm">BM-01: Nhật ký vệ sinh</span>
  <span class="fm">BM-02: Kế hoạch HC</span>
</div>
```

### 6. Kịch bản hỏi đáp (tab riêng)
Tab cuối cùng là "KỊCH BẢN" màu đỏ, chứa collapsible Q&A:
```html
<div onclick="qa('q1')" style="cursor:pointer;...">Q1: Câu hỏi?</div>
<div id="q1" style="display:none">TL: Câu trả lời</div>
```
Mỗi đáp án gồm:
- **TL:** Câu trả lời ngắn gọn
- **HS:** Hồ sơ cần trình
- **Thực địa:** Mẹo thao tác tại chỗ

### 7. Thanh navigation trong tab kịch bản
Dùng anchor links để nhảy giữa các module (M1-M10).

## Thiết kế (Newsprint)

Dùng `newsprint-design` tokens:
- Nền `#F9F9F7`, chữ `#111`, accent `#CC0000`
- Font: Playfair Display (heading), Lora (body), Inter (UI), JetBrains Mono (data)
- Zero border radius. Border `1px solid #111`
- Dot grid texture trên nền
- Checklist dùng checkbox vuông `.cb {width:14px;height:14px;border:1px solid #111}`

## Publish

Upload bằng `publish` skill với KV backend (không Gist). Luôn verify browser trước khi báo done.

## Ví dụ

Bộ 10 SOP Manna Đất Vàng (08/2026): SOP 01-10 + Kịch bản 18 câu hỏi. Published tại preview.thefirstonly.com.
