# Dashboard Mục tiêu Q4 — Pattern

Pattern cho Quang khi cần build executive dashboard từ Google Sheets data, trình bày cho chủ tịch hoặc hội đồng quản trị.

## Trigger

- Quang hỏi "visualize cho anh toàn bộ mục tiêu để trình bày cho chủ tịch"
- Quang gửi link sheet + nói "lên dashboard HTML"
- Quang nói "cập nhật nội dung phần tổng quan, chỉ lấy A và B thôi"

## Steps

### 1. Đọc sheet trước

Không build HTML từ giả định. Đọc dữ liệu thật từ sheet trước:

```python
r = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range="'Tổng quan'!A1:N40").execute()
rows = r.get('values', [])
for row in rows:
    print(row)  # kiểm tra cột nào có data thật, cột nào trống
```

Pitfall: Quang sẽ phát hiện ngay nếu em không đọc lại file ("em chưa đọc lại file à").

### 2. Cấu trúc HTML dashboard

4 section, Inter font, cards + tables:

**A. Kinh doanh** — 4 KPI cards (nhân sự, điểm trải nghiệm, đại lý, doanh thu) + bảng sales 3 vùng (Trại/Đại lý/B2B) + thanh doanh thu T10→T12

**B. R&D** — KPI cards (tuyển lab, EZ80 Baby tiến độ, hoàn thiện lab, tổng công thức) + bảng 5 nhóm công thức (EZ80 Baby, Hô hấp, Tiêu chảy, Diệt khuẩn, Tiêu hóa-sinh trưởng, 3in1) + 3 SP kiểm chứng (RESP-HP, GUT-HP, METRI/GROW/GS) + timeline lab

**C. Tổng quan** (khi được yêu cầu) — 3 cards kết luận. Nếu Quang nói "chỉ lấy A và B thôi" thì bỏ Tài chính, Tổng quan chỉ tổng hợp từ KD + RD.

### 3. Component code

Cards:
```html
<div class="cards">
  <div class="card">
    <div class="label">Nhân sự sale</div>
    <div class="value">0</div>
    <div class="detail">Mục tiêu: 3 → 5 → 7</div>
    <div class="traffic">T10: 3 · T11: 5 · T12: 7</div>
  </div>
</div>
```

Progress bars:
```html
<div class="progress-bar"><div class="progress-fill pf-green" style="width:25%"></div></div>
```

Badges: green (hoàn thành), yellow (đang triển khai), gray (chưa bắt đầu), blue (đang làm), red (quá hạn).

### 4. Mỗi RD mục là 1 dòng riêng

Không gộp "3 MVP" làm 1 bảng và "công thức" làm bảng khác. Sheet có 5 RD mục (RD3, RD5, RD6, RD7, RD8) + EZ80 Baby (RD2) = 6 dòng trong 1 bảng. Mỗi dòng có: Mã RD, tên nhóm, mục tiêu, kết quả, hạn chót, progress bar, trạng thái.

### 5. Card thống kê sau bảng

Sau bảng công thức, thêm 3 card:
- Tổng công thức: 0 / 25 (5 nhóm × 5 CT)
- Đang triển khai: 4 / 5 nhóm
- Chưa bắt đầu: 2 / 5 nhóm

### 6. Publish

Dùng KV:
```bash
python "skills/productivity/publish/scripts/content-upload.py" --file "path/to/dashboard.html" --title "Vua Kiem Dashboard ..."
```

## Pitfalls

1. **Luôn đọc sheet trước.** Dữ liệu trong sheet có thể đã thay đổi so với lần cuối. Nếu không đọc, sẽ visualize sai (ví dụ: thiếu 2 nhóm công thức trong R&D).
2. **Quang muốn "draft trước" rồi mới sửa.** Không publish final luôn. Gửi draft link → chờ feedback.
3. **Khi Quang nói "chỉ lấy A và B thôi"**, bỏ hẳn section Tài chính và Tổng quan cũ. Tổng quan mới chỉ tổng hợp từ KD + RD.
4. **Dùng mã RD đúng từ sheet** (RD3, RD5, RD6, RD7, RD8), không đặt tên tự do. Thứ tự sắp xếp theo hạn chót gần nhất.
5. **Publish HTML thay vì gửi text.** Quang xem trên điện thoại, cần link preview.
