# Mobile overflow ngang — checklist fix (dính 15/08, tái dính nhiều lần)

Triệu chứng: scroll ngang trên mobile, `docW > winW`.

## Cách đo chuẩn (KHÔNG đo trang desktop)
Tạo iframe 390px trong console load trang, so `documentElement.scrollWidth` với `innerWidth`,
rồi quét element có `getBoundingClientRect().right > winW + 1`. Đo trên desktop **không phản ánh
mobile** — nên nhiều lần tưởng đã hết lỗi.

## Thủ phạm + fix (đều đã verify)

1. **Header-right tràn** (TFO badge + budget + updated-at + Refresh nằm 1 hàng, gap 20px):
   `@media(max-width:600px)` → `.header{flex-wrap:wrap}`,
   `.header-right{flex-wrap:wrap;gap:8px;width:100%;justify-content:flex-end}`,
   `.updated-at{display:none}`.

2. **`.agent-role` flex không co** (text dài đẩy cả row tràn): thiếu `min-width:0` — thêm vào
   flex child có `flex:1` + `text-overflow:ellipsis`.

3. **Grid `1fr` = `minmax(auto,1fr)`** — `auto` min theo nội dung nên không co dưới content rộng:
   đổi thành `grid-template-columns: minmax(0, 1fr)` + `.agent-item{max-width:100%}`.

4. **Tab bar / menu tabs tràn** (TFO web `app/static/index.html`):
   `.tab-bar{overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none}`
   + `.tab-bar::-webkit-scrollbar{display:none}`
   + `.tab-btn{flex-shrink:0;white-space:nowrap}` (nút không bị co, menu scroll ngang).
   Media mobile: `.tab-btn{padding:10px 14px;font-size:13px}`.
   Verify: `tabBar.clientW < tabBar.scrollW` + `overflowX=auto` → menu scroll được, `docW == winW`.

5. `body{overflow-x:hidden}` chặn hậu quả cuối — **biện pháp tạm**, không thay thế 1-4.

## Verify sau mỗi fix
Đo lại bằng cách chuẩn ở trên (iframe 390px). Không tin "nhìn không thấy tràn nữa" bằng mắt.