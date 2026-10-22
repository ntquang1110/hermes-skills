# Bản đồ trường khi crawl site WordPress / WooCommerce

Dùng kèm `scripts/crawl_wp_catalog.py`. Mục đích: trích **cấu trúc** của danh mục,
không chỉ trích nội dung.

## 1. Phát hiện nền tảng

Dấu hiệu WooCommerce: có class `woocommerce-`, `product_title`, `add-to-cart`,
`woocommerce-loop-product__title`, `rel="tag">` cho danh mục.
Dấu hiệu WordPress: sitemap do plugin Yoast sinh (`wp-content/plugins/wordpress-seo/css/main-sitemap.xsl`),
`wp-json` trong link, `/wp-admin/` trong robots.txt.

## 2. Sitemap — nguồn kiểm kê

| File | Cho biết |
|---|---|
| `robots.txt` | dòng `Sitemap:` trỏ tới sitemap index |
| `sitemap.xml` | index: liệt kê các sitemap con |
| `product-sitemap.xml` | **tổng số sản phẩm thật** (đếm `<loc>`) |
| `product_cat-sitemap.xml` | danh mục sản phẩm, tức định vị của họ |
| `page-sitemap.xml` | trang giải pháp / giới thiệu / chính sách |
| `post-sitemap.xml` | **chiến lược nội dung** (tiêu đề bài = câu khách hỏi) |

Sitemap còn có `<lastmod>` — dùng để phát hiện site còn được cập nhật hay bỏ không.
Nếu `blocks-sitemap` hoặc `product-sitemap` có `lastmod` gần đây mà cert SSL đã hết hạn,
đó là tín hiệu "có người làm nội dung nhưng không ai chăm hạ tầng".

## 3. Bản đồ trường trên trang sản phẩm

| Trường | Regex / dấu hiệu | Ghi chú phân tích |
|---|---|---|
| `title` | `<title>(.*?)</title>` | tiêu đề SEO, thường khác tên hiển thị |
| `name` | `class="product_title[^"]*"[^>]*>(.*?)</h1>` (fallback `<h1>`) | **tên hiển thị mới là thứ đáng phân tích** |
| `price` | `<bdi>(...)<span class="woocommerce-Price-currencySymbol">` | rỗng ở mọi trang = B2B, không phải lỗi crawl |
| `cats` | `rel="tag">([^<]+)</a>` | cả danh mục lẫn tag đều ra ở đây, đừng tách |
| `short` | `woocommerce-product-details__short-description` | mô tả ngắn, hay chứa tên hoạt chất |
| `desc` | `id="tab-description"` | mô tả dài, cắt ~5000 ký tự là đủ |
| `attrs` | `woocommerce-product-attributes-item__label` + `__value` | thường rỗng; nếu có thì là bảng hàm lượng |
| `sku` | `class="sku">([^<]+)<` | rỗng là chuyện thường với site catalogue |
| ảnh | `wp-content/uploads/.*\.(jpg\|png\|webp)` | **số ảnh/trang là chỉ báo mức đầu tư nội dung** |

`add-to-cart` có mặt **không** có nghĩa là bán online. Kiểm thêm:
- có `woocommerce-Price-amount` không? (không có = không niêm yết giá)
- nút ghi gì? `Thêm vào giỏ` vs `Liên hệ` / `Yêu cầu báo giá`
- có `wpcf7` / `contact-form` không?

Tổ hợp "giỏ hàng + không giá + nút Liên hệ + form liên hệ" = **catalogue B2B**, không phải cửa hàng.

## 4. Các tín hiệu phải ĐẾM (đây là phần tạo ra phân tích)

Đếm và nêu tỷ lệ, đừng chỉ mô tả:

- `Σ sản phẩm` và `Σ có giá` → tỷ lệ niêm yết giá
- `Σ desc chứa cụm liều dùng` (`liều|hòa|trộn|ml/|g/|kg thể trọng|nước uống`) → mức độ bán bằng tư vấn
- `Σ desc chứa số điện thoại` → tín hiệu chốt đơn qua kênh người
- `Σ có thành phần thảo dược` (`thảo dược|chiết xuất|dịch chiết|tỏi|nghệ|oregano|quế|gừng`) → dòng định vị
- `Σ nêu tên nhà cung cấp ngoại` (`nhập khẩu.*(Bỉ|Pháp|Mỹ|Ý|Hàn)`, tên hãng) → mượn uy tín quốc tế
- `Σ sản phẩm mỗi loài` (từ `cats`) → **trọng tâm thật**, thường lệch hẳn so với menu quảng cáo
- `Σ bài viết` trong `post-sitemap.xml` → độ dày nội dung
- `Σ danh mục rỗng` (mở ra nhưng 0 sản phẩm) → tham vọng chưa làm tới
- `Σ ảnh/trang sản phẩm` → mức đầu tư hình ảnh

Cụm regex dùng lại được:

```python
import re
LIEU  = r"(liều|hòa|trộn|ml/|g/|kg thể trọng|nước uống)"
PHONE = r"(?:0\d{2,3}[\.\s]?\d{3}[\.\s]?\d{3,4}|02\d{2}[\.\s]\d{3}[\.\s]\d{3,4})"
THAOD = r"(thảo dược|chiết xuất|dịch chiết|thảo mộc|tỏi|nghệ|oregano|quế|gừng)"
NK    = r"nhập khẩu[^\.]{0,35}(Bỉ|Pháp|Mỹ|Ý|Hàn|Trung)"
```

## 5. Phát hiện "hai hệ đặt tên" (tín hiệu giá trị cao nhất)

Tách tên sản phẩm thành 2 nhóm bằng regex:

```python
# Ten theo hoa chat: có chữ số + % hoặc tên hoạt chất quốc tế
HOA_CHAT = r"(?i)(\d+\s*%|\bs\b\s*$|doxy|florfenicol|enrofloxacin|diclazuril|sulphatrim|tylosin|amoxicillin|colistin)"
# Ten theo loi ich: từ chỉ kết quả nhìn thấy được
LOI_ICH  = r"(?i)(vỗ béo|tăng trọng|kích lườn|trổ mã|đẹp mã|dày lườn|nặng cân|kích đẻ|thay lông|mượt lông|nở ức|bung đùi)"
```

Hai nhóm này xuất hiện **cùng trong một danh mục** là dấu hiệu công ty chạy hai dòng song song:
dòng nhà (kể chuyện, biên cao) và dòng phân phối (hàng thương mại, giữ dòng tiền).
Đây là phát hiện đáng đưa lên đầu báo cáo.

## 6. Bẫy khi parse

- **Mô tả dài bị tag lồng**: `id="tab-description"` thường là `div` bọc nội dung WordPress
  đã render. Cắt tới cuối trang rồi giới hạn ký tự, đừng cố đóng thẻ.
- **`rel="tag"` gộp cả category lẫn tag** — không cố tách, chỉ đếm tần suất.
- **Giá có thể ở `content` attribute nếu thiếu `<bdi>`** — luôn có nhánh fallback regex thứ 2.
- **HTML entity**: nhiều site encode cả dấu tiếng Việt → luôn `html.unescape` trước khi phân tích.
- **Nhiễu số điện thoại**: bỏ `<script>/<style>` trước khi regex số điện thoại,
  không thì CSS pixel value sẽ khớp giả hàng loạt.
