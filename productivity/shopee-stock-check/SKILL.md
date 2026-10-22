---
name: shopee-stock-check
description: "Use when checking Shopee VN stock/price at scale."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [shopee, vietnam, ecommerce, stock, tinyfish, procurement]
---

# Kiểm tra tồn kho / giá Shopee VN khi Shopee chặn hết

## Trigger

- User yêu cầu "check link Shopee nào còn hàng / hết hàng"
- Cần giá, quy cách đóng gói, tình trạng còn/hết của nhiều sản phẩm Shopee
- Cần lọc danh sách link Shopee đã thu thập trước đó

## Thực tế: Shopee chặn CỨNG mọi đường (verified 14/10/2026)

| Đường | Kết quả |
|---|---|
| `curl` API `shopee.vn/api/v4/search/search_items` | HTTP 403, body `{"error":90309999,"redirect_to_error_page":true}` |
| `web_extract` | `bot_blocked` |
| TinyFish `fetch_content` | `bot_blocked` (từng URL) |
| Camofox browser (`browser_navigate`) | `POST /tabs` 500; skill camofox ghi nhận Shopee redirect `/unsupported.html` |
| Obscura (Rust headless) | redirect `/unsupported.html` "trình duyệt không còn hỗ trợ" |

→ **Đừng tốn turn thử browser.** Không có đường nào đọc được trang sản phẩm Shopee từ môi trường này.

## Đường chạy được: snippet search có chứa trạng thái tồn kho

Snippet của TinyFish search (và đôi khi `web_search`) **có nhúng giá và chữ "Đã bán hết"** — đây là nguồn duy nhất đọc được tồn kho.

```
mcp__tinyfish__search(
  query="<tên mặt hàng> <quy cách>",
  include_domains="shopee.vn",
  location="VN",
  language="vi",
  purpose="Kiểm tra trạng thái tồn kho ..."
)
```

Ví dụ snippet trả về:
- `"...túi 1kg- Hàng nhập khẩu. 1/3. Đã bán hết. 185.000₫."` → **HẾT HÀNG**
- `"...1 Kg Vi Sinh Nguyên Liệu Bacillus Subtilis 100 Tỷ Cfu/gr. 1/3. 480.000₫."` → **CÒN HÀNG**

### Quy tắc phân loại

| Dấu hiệu trong snippet | Kết luận |
|---|---|
| `Đã bán hết` / `Hết hàng` | HẾT → loại |
| Có giá (`185.000₫`) + không có chữ "Đã bán hết" | CÒN → giữ |
| `Hàng Đặt Trước (có hàng sau N ngày)` | CÒN nhưng phải chờ → giữ, ghi rõ |
| `Chọn loại hàng` + nhiều mức giá | CÒN, có nhiều quy cách → giữ |
| URL không còn xuất hiện trong bất kỳ kết quả nào | Link biến mất → loại |
| Chỉ trả về `/blog/`, `/list/`, `/search?` | Nhiễu, không phải sản phẩm → bỏ |

### Cách làm chuẩn cho 1 danh sách link

1. Nhóm link theo mặt hàng (1 search phủ nhiều link cùng chất).
2. Chạy `mcp__tinyfish__search` song song 6–8 query/lượt (`include_domains="shopee.vn"`, `location="VN"`, `language="vi"`).
3. So khớp URL trả về với danh sách gốc **theo đuôi `-i.<shopid>.<itemid>`** (phần encode tiếng Việt có thể khác nhau, đuôi `-i.` thì ổn định).
4. Loại link hết hàng; **giữ luôn link mới tìm được mà còn hàng** → đây là giá trị cộng thêm, không chỉ là lọc.
5. Ghi lại sheet: khối "CÒN HÀNG" + khối "ĐÃ LOẠI" kèm mã `i.<shopid>.<itemid>` và lý do. Gạch ngang khối đã loại.

## Pitfalls

- **Không verify được "Nơi bán" (tỉnh/thành).** Snippet không chứa địa chỉ shop. Nếu user cần ưu tiên Hà Nội → phải nói thẳng là không lọc hộ được và bảo user dùng bộ lọc `Nơi bán: Hà Nội` trên Shopee. Đôi khi snippet của trang `/list/` có `location-icon Thành phố Hà Nội` — nhưng đó là trang danh sách, không gắn được vào từng sản phẩm.
- **Snippet không phải lúc nào cũng có trạng thái.** Nhiều listing snippet chỉ có mô tả marketing. Thiếu dữ liệu thì ghi "chưa xác minh", KHÔNG suy đoán còn/hết.
- **Link có thể biến mất khỏi index** (shop xoá/ẩn sản phẩm). Không tìm thấy ≠ hết hàng, nhưng vẫn nên loại khỏi danh sách mua.
- **Đừng dùng `web_extract` cho Shopee** — luôn `bot_blocked`, phí turn.
- **Search `site:shopee.vn "<từ khoá>"` qua `web_search` chỉ ăn khi query NGẮN** (1–3 từ). Query dài trả kết quả rác ngoài Shopee. TinyFish với `include_domains` ổn định hơn nhiều.
- Product URL dạng `shopee.vn/product/<shopid>/<itemid>` cũng hợp lệ — không phải chỉ dạng slug.

## Lấy danh sách link ban đầu (khi chưa có)

`web_search` với `site:shopee.vn "<tên mặt hàng>"` (ngắn) hoặc TinyFish search `include_domains="shopee.vn"`. Loại bỏ `/list/`, `/search?`, `/blog/`, shop rác (`ads.shopee.vn`, `mac_official_store`, `phongvu_*`). Kiểm tra URL khớp regex `-i\.\d+\.\d+$`.
