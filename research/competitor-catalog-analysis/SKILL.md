---
name: competitor-catalog-analysis
description: "Use when analyzing a company's web product catalog."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [competitor, catalog, web-scraping, woocommerce, market-analysis, vietnam, portfolio]
---

# Quét danh mục sản phẩm một công ty và dựng bản phân tích

Dùng khi user đưa link website của một công ty (đối thủ, NCC, đối tác) và hỏi kiểu
*"scan toàn bộ sản phẩm bên này và cho anh bản phân tích"*, *"bên này có gì"*,
*"tại sao bên này bán được hàng"*.

Khác với `project-reconnaissance` (audit codebase) và `vietnam-corporate-research` (hồ sơ pháp nhân).
Skill này lo **danh mục sản phẩm + mô hình kinh doanh suy ra từ cấu trúc web**.

Sản phẩm cuối: báo cáo HTML (design + publish theo `corporate-executive-html-report` và `publish`).

## Bước 0 — Mở được site trước đã (đừng bỏ qua bước này)

Web công ty VN nhỏ rất hay gặp **chứng chỉ SSL hết hạn**. Triệu chứng rất dễ chẩn đoán nhầm thành "domain chết":

| Công cụ | Kết quả khi cert hết hạn |
|---|---|
| `web_extract` | `target_unreachable` |
| TinyFish `fetch_content` | `target_unreachable` (từng URL) |
| `curl` https | `000` + `schannel: SEC_E_CERT_EXPIRED` |
| `curl` http | `301` sang https rồi fail |
| `ping` / `nslookup` | **Vẫn OK** — domain sống, chỉ cert hỏng |

→ Phân biệt bằng `nslookup` + đọc kỹ mã lỗi curl. Nếu là cert: **`curl -skL`** (bỏ verify) là vào được ngay.
Đừng kết luận "site chết" chỉ vì `web_extract` báo `target_unreachable`.

```bash
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
curl -skL -m 40 -A "$UA" -H 'Accept-Language: vi,en' "https://<domain>/" -o home.html -w "%{http_code} %{size_download}\n"
```

Ghi lại việc cert hết hạn như **một phát hiện phân tích**, không chỉ là chướng ngại kỹ thuật: nó là bằng chứng công ty không chăm kênh online.

## Bước 1 — Sitemap trước, listing sau

Đừng crawl trang danh mục từng trang một. Hầu hết site thương mại VN là WordPress + WooCommerce và có sitemap đầy đủ.

```bash
curl -skL "https://<domain>/robots.txt"        # tìm dòng Sitemap:
curl -skL "https://<domain>/sitemap.xml"       # sitemap index
curl -skL "https://<domain>/product-sitemap.xml"
```

Sitemap index thường tách: `product-sitemap.xml`, `product_cat-sitemap.xml`, `page-sitemap.xml`, `post-sitemap.xml`.
Đếm `<loc>` trong `product-sitemap.xml` là ra **tổng số sản phẩm thật** (một lần gọi, không phân trang).

Dùng `product_cat-sitemap.xml` + `page-sitemap.xml` để biết họ **định vị theo danh mục nào** và có trang giải pháp riêng không.
Dùng `post-sitemap.xml` để đọc chiến lược nội dung (xem bước 4).

## Bước 2 — Crawl từng trang sản phẩm, trích trường cố định

Script sẵn dùng: `scripts/crawl_wp_catalog.py` (chạy được, đã verify trên site 77 sản phẩm).
Gọi: `python scripts/crawl_wp_catalog.py https://<domain> out.json`

Bản đồ trường cần trích và regex tương ứng: `references/woocommerce-catalog-extraction.md`.

Trích tối thiểu: tên, giá, danh mục, mô tả, thành phần, liều dùng, SKU, ảnh.
Lưu JSON ngay, in tiến độ mỗi 10 trang — crawl 70+ trang không nên mất dữ liệu nếu đứt giữa đường.

## Bước 3 — Phân loại, đừng chỉ liệt kê

Liệt kê 77 tên sản phẩm là vô giá trị. Phải gom nhóm.

- **Theo chức năng** — match keyword trên tên + danh mục + 400 ký tự mô tả. Chấp nhận một sản phẩm vào nhiều nhóm; công ty VN hay viết công dụng rộng.
- **Theo loài / đối tượng** — đếm số sản phẩm gắn thẻ mỗi loài để tìm ra **trọng tâm thật**. Thẻ menu có thể ghi 4 loài nhưng 75/77 sản phẩm chỉ thuộc 1 loài.
- **Theo vòng đời** — sắp sản phẩm lên trục thời gian của một vụ nuôi. Nếu phủ được từ đầu tới cuối vụ thì đó là chiến lược giữ khách, phải nêu.
- **Danh mục rỗng** — trang danh mục mở ra nhưng 0 sản phẩm là tham vọng chưa làm tới. Luôn kiểm và nêu.

## Bước 4 — Suy mô hình kinh doanh từ CẤU TRÚC, không từ lời tự khai

Đây là phần giá trị nhất. Đọc các tín hiệu cấu trúc, không đọc trang "Giới thiệu":

| Tín hiệu cấu trúc | Suy ra |
|---|---|
| Có giỏ hàng nhưng **0 sản phẩm có giá**, nút toàn ghi "Liên hệ" | B2B, bán qua tư vấn/đại lý. Không niêm yết giá là **chủ đích** (đối thủ không so giá, đại lý giữ biên), không phải sơ suất |
| Hotline kỹ thuật in trong **mô tả từng sản phẩm** | Người chốt đơn là cán bộ kỹ thuật; web chỉ để đưa khách tới cuộc gọi |
| Số điện thoại + bảng liều dùng trên gần như mọi trang | Bán bằng tư vấn, mô hình khó copy vì cần người thật |
| **Hai hệ đặt tên cùng tồn tại** | Hai dòng sản phẩm, hai kiểu khách. Tên theo *lợi ích tiếng bản địa* = dòng nhà/dòng kể chuyện; tên theo *hoạt chất + nồng độ* = dòng phân phối/hàng thương mại |
| Tên sản phẩm là từ chỉ TIỀN (cân nặng, ngoại hình, số trứng) | Bán kết quả bán được, không bán khái niệm sức khỏe |
| Tiêu đề bài viết là nguyên văn câu khách hỏi + có tên sản phẩm | Content là phễu về từng SKU, không phải blog |
| Có mục "Phản hồi khách hàng" **ngang cấp menu chính** | Bằng chứng xã hội là kênh chốt đơn chủ lực |
| Nhà máy là công ty khác | Gia công ngoài → không kiểm soát năng lực, công thức dễ lộ |
| Email là Gmail cá nhân | Quy mô nhỏ, chưa chuyên nghiệp hoá |
| Tên công ty xuất hiện trong tạp chí ngành | PR B2B, không chỉ digital |

Nguyên tắc: **mỗi luận điểm phải kèm bằng chứng trích được từ web** (số đếm, câu nguyên văn, tên trường).
Đừng viết "họ marketing tốt" — viết "menu có mục Phản hồi ngang hàng Sản phẩm, gồm N video".

## Bước 5 — Bắt buộc có mục "Những gì chưa chứng minh được"

User này làm việc theo nguyên tắc **số không nguồn = không số**. Bịa doanh thu/thị phần là lỗi nặng.

Phải tách rõ 2 loại trong output:
- **Chứng minh được** — đếm/trích từ web (số sản phẩm, tỷ lệ có giá, số bài viết, tín hiệu cấu trúc).
- **Không chứng minh được** — doanh thu, số đại lý, thị phần, giá bán thật, SKU bán chạy. Ghi `Không có` kèm lý do, **không đoán**.

Kèm luôn bảng **"cách kiểm chứng nếu muốn số thật"** (gọi hotline đóng vai người mua, ghé cửa hàng địa phương, hỏi chủ trại, xin phiếu kiểm nghiệm). Đây là thứ biến báo cáo từ suy đoán thành kế hoạch hành động.

## Bước 6 — Nối về việc của user

Báo cáo chỉ có giá trị khi trả lời được "vậy mình làm gì khác". Thêm một mục cuối đặt cạnh doanh nghiệp của user:
- Học được gì **không tốn tiền** (cách đặt tên, in hotline cạnh bảng liều, trang phản hồi thật).
- Mình có gì họ không có (tự sản xuất vs thuê gia công, tự chiết vs nhập).
- Lỗ hổng của họ mà mình đánh vào được.

## Output

Báo cáo HTML theo `corporate-executive-html-report` (tokens + cấu trúc "kết quả trước"), publish theo `publish`.
Bố cục đã dùng tốt cho dạng bài này:

1. Masthead + **1 câu statement** chốt bản chất (không phải mô tả)
2. Dải 4 KPI số lớn (dùng con số gây bất ngờ, vd `0/77 sản phẩm có giá niêm yết`)
3. Tổng quan pháp nhân + hạ tầng (bảng)
4. Danh mục phân theo chức năng (bar chart) + theo vòng đời (bảng)
5. Kiến trúc dòng sản phẩm (2 cột đối chiếu)
6. Chi tiết cấu trúc trang sản phẩm
7. **Vì sao bán được** — grid thẻ, mỗi thẻ 1 luận điểm + 1 khối bằng chứng
8. Điểm yếu khai thác được (2 cột)
9. **Chưa chứng minh được** + cách kiểm chứng
10. Đặt cạnh doanh nghiệp user
11. Footer nêu nguồn + ngày quét

## Pitfalls

- **Đừng kết luận "site chết" từ `target_unreachable`.** Kiểm `nslookup` + mã lỗi curl trước; cert hết hạn rất phổ biến và `curl -skL` xử lý được.
- **Đừng crawl listing phân trang khi có sitemap.** Phí hàng chục request và dễ sót.
- **Đừng bỏ trang `page-sitemap.xml` và `post-sitemap.xml`.** Trang giải pháp và bài viết là nơi lộ chiến lược, sản phẩm không nói ra.
- **Đừng để mất toàn bộ dữ liệu crawl vì một trang lỗi.** Ghi JSON ngay, in tiến độ, có retry.
- **Đừng slice URL/percent-encode khi in ra** — mất phần định danh. In full hoặc ghi file rồi đọc lại.
- **Đừng trình bày luận điểm "vì sao bán được" mà không có bằng chứng.** Mỗi luận điểm 1 dòng trích dẫn từ web.
- **Đừng bịa doanh thu / thị phần / giá bán.** Không có nguồn thì ghi rõ là không có.
- **Đừng quên cert hết hạn, menu rỗng, Gmail cá nhân, gia công ngoài.** Đây là 4 loại lỗ hổng hay bị bỏ sót nhất.
- **Đừng tự khen kết quả.** Báo cáo bằng số và bằng chứng, không bằng tính từ.

## Support files

- `scripts/crawl_wp_catalog.py` — crawler WordPress/WooCommerce: sitemap → từng trang sản phẩm → JSON.
- `references/woocommerce-catalog-extraction.md` — bản đồ trường + regex + tín hiệu cần đếm.
