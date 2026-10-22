# UI compact audit — TFO dashboard (15/09/2026)

Kết quả audit theo 3 câu hỏi của Quang: list đã rút ngắn chưa, record đã gọn chưa,
view vấn đề nhanh nhất chưa. Giữ lại làm checklist tái dùng cho mọi lần audit UI sau.

## Checklist 3 câu (chạy grep, không cần mở browser)

1. **List đã rút ngắn chưa** — mọi list phải `slice(0, 5)` + nút "Xem thêm/Thu gọn"
   (tool list: 8). Grep: `slice(0, 5)|slice(0, 8)|Xem thêm|ShowAll|toggle.*\(\)`.
   Chuẩn TFO: Hôm nay, Cần chú ý, Lịch sử họp, Meeting meTelligent, Task — tất cả limit 5.
2. **Record đã gọn chưa** — flow ghi âm phải: auto-fill ngày giờ + tiêu đề mặc định,
   1 hàng nút + expand chi tiết (upload zone, progress, result box thu gọn).
   Gõ tay tiêu đề/ngày giờ mỗi lần ghi = chưa gọn.
3. **View vấn đề nhanh nhất chưa** — mở app thấy ngay: KPI 4 thẻ → Hôm nay → Cần chú ý,
   không cuộn. Mọi view phụ phải reachable trong ≤1 click từ Tổng quan.

## Lỗi cấu trúc đã bắt (đừng lặp lại)

- **Task nằm 3 nơi** (Dashboard Việc cần làm + tab Kanban + tab Agent): 1 loại info = 1 đường
  chính, các nơi khác chỉ link tới, không render list riêng.
- **2 tab cùng tên khác ruột** (sub-tab Hệ thống trong Dashboard vs tab Hệ thống riêng):
  cấm trùng tên; gộp hoặc đổi tên cho khỏi nhầm.
- **Sub-tab đè chức năng tab chính** (Meeting/Việc cần làm/Hệ thống vs Lịch họp/Kanban/Hệ thống):
  >6 tab + 4 sub-tab = 10 view là quá nhiều; xóa sub-tab trùng, giữ 1 đường duy nhất.
- **Dead card sau pivot**: feature đã kill (vd card Meeting meTelligent sau quyết định bỏ
  Android) phải gỡ ngay trong cùng commit pivot — "chết mà chưa chôn" gây rối UI.
- **Live card không floating thật**: element realtime phải luôn thấy khi active (fixed góc phải),
  không nằm cuối trang bắt user cuộn. `#liveCard` PHẢI là con trực tiếp của `<body>`
  (15/09: đã dời ra khỏi `#viewDashboard` vì switchTab đặt parent display:none giết fixed
  element — pitfall cũ chỉ đúng nửa chừng: overlay modal như `#taskOverlay` giữ trong view
  container được, còn floating panel sống qua tab thì ra `<body>`).
- **stopLiveStream phải ẩn card + clear handler**: xóa `onclose`/`onerror` trước `close()`
  để tránh báo lỗi nhiễu khi stop chủ động; ẩn `#liveCard` về `display:none` khi dừng.
  Nếu không, card floating treo lại trên mọi tab sau khi dừng nói chuyện.
- **setLiveState đổi màu + tốc độ dot theo state**: listening xanh lá 1.2s,
  thinking vàng 0.6s, working cam 0.8s, speaking xanh dương đứng yên, waiting xám.
  Dot query qua `#liveCard .card-header span:first-child`.
- **Responsive 700px**: tab-bar/subtab-bar `overflow-x:auto` + nút `nowrap/flex-shrink:0`,
  `.dash-actions` column + `.dash-action{width:100%}`, `.record-btn{width:100%`.
  Live card media 480px full-width (left/right 8px, bottom 8px).

## Quy trình audit song song

Khi user bảo "vừa code vừa check UI": chạy audit grep/read song song với task code,
không đợi code xong mới audit. Audit xong báo 3 mục (list/record/view-nhanh) + đề xuất
rút gọn đánh số để user chốt từng mục — KHÔNG tự sửa UI khi chưa chốt.
