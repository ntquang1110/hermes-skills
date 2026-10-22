---
name: competitor-catalog-audit
description: "Use when auditing a competitor's product catalog site."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [competitor, woocommerce, wordpress, crawl, catalog, analysis, sitemap, vietnam]
    related_skills: [corporate-executive-html-report, publish, web-research, vietnam-corporate-research]
---

# Quét và phân tích danh mục sản phẩm của đối thủ

## Trigger

- User đưa 1 URL (thường `/san-pham/`, `/products/`, `/cua-hang/`) và hỏi "bên này có gì", "bán được thì tại sao"
- Cần bản phân tích danh mục đối thủ: tổng quan tới chi tiết, cấu trúc sản phẩm, tín hiệu bán hàng
- Cần so sánh danh mục đối thủ với danh mục của mình

## Bước 0: Chẩn đoán truy cập TRƯỚC khi crawl

Rất nhiều site SME Việt Nam **hết hạn chứng chỉ SSL**. Triệu chứng và cách xử lý:

```bash
nslookup <domain>                                    # DNS có resolve không
curl -sS -m 20 -o gt.html -w "%{http_code} %{errormsg}\n" "https://<domain>/"
```

| Kết quả | Nghĩa | Xử lý |
|---|---|---|
| `schannel: SEC_E_CERT_EXPIRED` / `certificate has expired` | SSL hết hạn | **Dùng `curl -sk`** hoặc Python `ssl._create_unverified_context()`. Đây là finding đáng ghi vào báo cáo (site không ai chăm) |
| `http=000`, DNS vẫn OK | SSL fail hoặc chặn | thử `http://` xem có 301 sang https không |
| DNS NXDOMAIN | domain chết | dừng, báo user |

**`web_extract` và TinyFish `fetch_content` đều trả `target_unreachable` khi SSL hết hạn** (chúng verify cert). Đừng kết luận site chết. Luôn thử `curl -sk` trước khi bỏ.

⚠️ **MSYS/Windows pitfalls:**
- `/tmp` KHÔNG tồn tại. Dùng `~/httptmp` (tạo bằng `mkdir -p`).
- `curl -o /dev/null` báo `Failed writing received data to disk/application`. Luôn ghi ra file thật rồi đọc.

## Bước 1: Sitemap trước, đừng phân trang

Nhanh hơn phân trang rất nhiều và lấy được **toàn bộ** sản phẩm trong 1 request.

```bash
for f in robots.txt sitemap.xml product-sitemap product_cat-sitemap page-sitemap post-sitemap; do
  curl -skL -m 30 -A "$UA" "https://<domain>/$f" -o "gt_$f" -w "$f: %{http_code} %{size_download}\n"
done
```

`robots.txt` → tìm dòng `Sitemap:`. `sitemap.xml` (sitemapindex) → liệt kê các sitemap con. WordPress + Yoast/SEOPress thì gần như luôn có `product-sitemap.xml`.

```bash
grep -oE '<loc>[^<]+</loc>' gt_product-sitemap.xml | sed 's/<[^>]*>//g' | wc -l
```

Nếu không có sitemap: parse listing page tìm `href` khớp regex sản phẩm, và đọc số trang (`/san-pham/page/2/` ... ).

## Bước 2: Crawl chi tiết

Dùng `scripts/crawl-catalog.py` (đã chạy thật, 77 trang):

```bash
python scripts/crawl-catalog.py --domain greentechvs.com \
  --sitemap product-sitemap.xml --out greentech_products.json
```

Script tự: bật SSL unverified, lấy danh sách URL từ sitemap, crawl song song có retry, trích các field WooCommerce, lưu JSON, in bảng tóm tắt.

### Field WooCommerce cần trích

| Field | Selector / regex |
|---|---|
| Tên | `class="product_title..."` trong `<h1>`, fallback `<title>` |
| Giá | `woocommerce-Price-amount` + `woocommerce-Price-currencySymbol` |
| Danh mục | `<a rel="tag">` trong khối `posted_in` |
| Mô tả ngắn | `woocommerce-product-details__short-description` |
| Mô tả đầy đủ | `id="tab-description"` hoặc `woocommerce-Tabs-panel--description` |
| Thuộc tính | `woocommerce-product-attributes-item__label` + `__value` |
| SKU | `class="sku"` |
| Nút mua | tìm `add-to-cart`, `Thêm vào giỏ`, `Liên hệ`, `Yêu cầu báo giá` |
| Số ảnh | đếm `wp-content/uploads/*.{jpg,png,webp}` |

## Bước 3: Đọc ra tín hiệu, đây mới là phần giá trị

Đừng dừng ở bảng danh sách. Các tín hiệu dưới đây là thứ user thực sự cần:

### 3.1 Không có giá = mô hình B2B, không phải lỗi

Nếu `0/N` sản phẩm có giá và nút mua là "Liên hệ" kèm form liên hệ trên mọi trang → **catalogue, không phải cửa hàng**. Hệ quả: không so giá được, đại lý không bị ép biên, khách buộc phải gọi. Ghi đây là **lựa chọn chiến lược**, không phải thiếu sót.

### 3.2 Hai hệ đặt tên = hai dòng sản phẩm = hai cách bán

Dấu hiệu mạnh nhất khi quét danh mục. Tách tên sản phẩm thành 2 nhóm:

| Dòng | Đặc điểm tên | Vai trò |
|---|---|---|
| Nhà / thương hiệu | Tên tiếng Việt theo **lợi ích nhìn thấy** ("Trổ mã", "dày lườn", "vỗ béo", "năng suất") | Kể chuyện, tạo uy tín, ăn xu hướng |
| Phân phối / thương mại | Tên theo **hoạt chất + nồng độ** ("Doxy 50%", "Flor 20%") | Dòng tiền hiện tại, cạnh tranh bằng giá |

Nếu cùng 1 site có cả hai → họ **không tự trói mình vào một lập trường**. Ví dụ đã gặp: marketing toàn bộ nói "thay thế kháng sinh" nhưng danh mục vẫn có 23 sản phẩm kháng sinh.

### 3.3 Vai trò của hotline và bảng liều dùng

Đếm tỷ lệ sản phẩm có: hướng dẫn liều dùng chi tiết, và số điện thoại kỹ thuật in trong mô tả. Tỷ lệ cao (vd 75/77) = **bán bằng tư vấn kỹ thuật**, website chỉ đưa khách tới cuộc gọi. Đây là mô hình khó copy (phải có người) và giữ khách tốt.

### 3.4 Bằng chứng xã hội nằm ở đâu trong menu

User hỏi "vì sao bán được" → kiểm tra mục "Phản hồi / Đánh giá / Khách hàng" có phải **mục menu chính** hay chỉ là trang phụ. Đặt ngang hàng Sản phẩm = coi trọng bằng chứng xã hội.

### 3.5 Kênh ngoài web: hội thảo, đại lý, báo ngành

Crawl thêm `page-sitemap` + `post-sitemap` và grep: `hội thảo`, `tri ân`, `đại lý`, `hội nghị`. Với ngành nông nghiệp/B2B Việt Nam, đây thường là kênh chốt đơn thật.

### 3.6 Tìm pháp nhân và lịch sử

```
web_search: "<tên công ty đầy đủ>" mã số thuế
```
`masothue.com` / `thongtincongty.vn` cho: MST, ngày cấp, người đại diện, tên giao dịch. **Đối chiếu năm bản quyền web với năm đăng ký** — lệch nhau (web 2019, đăng ký 2023) là tín hiệu tái cấu trúc hoặc thương hiệu cũ, ghi lại nhưng không suy diễn.

### 3.7 Tìm hiện diện PR ngành

Grep tên công ty + domain trong kết quả tìm kiếm của tạp chí ngành. Xuất hiện chung trang quảng cáo với công ty lớn = uy tín B2B mà quảng cáo Facebook không mua được.

### 3.8 Cấu trúc phủ vòng đời

Xếp sản phẩm theo giai đoạn khách hàng: mới bắt đầu → tăng trưởng → trước khi bán → sinh sản → kết thúc. Phủ hết = giữ khách suốt vụ bằng độ phủ danh mục.

## Bước 4: Trung thực về cái KHÔNG chứng minh được

Bắt buộc có mục riêng, nêu rõ **không có**: doanh thu, số đại lý, thị phần, giá bán thật, sản phẩm nào bán chạy.
Site không giá + không đơn hàng = **không có tín hiệu số nào**. Không suy đoán, không bịa.

Rồi đưa **4 bước kiểm chứng** user tự làm được: gọi hotline đóng vai người mua → ghé cửa hàng bán lẻ địa phương → hỏi vài khách hàng cuối → xin phiếu kiểm nghiệm.

## Bước 5: Dựng báo cáo

Load `corporate-executive-html-report` lấy design tokens (nền `#FBFBF8`, accent forest `#1D5C3E`, gold `#C89B3C`, Be Vietnam Pro, elevation = hairline KHÔNG shadow) và cấu trúc "kết quả trước".

Cấu trúc 8 phần đã dùng:
1. Masthead (ai, loại tài liệu, ngày quét, nguồn)
2. Statement 1 dòng (kết luận sắc nhất, không dẫn dắt)
3. KPI strip 4 ô
4. Tổng quan pháp nhân (bảng)
5. Danh mục phân theo chức năng (bar chart, đếm thật)
6. Kiến trúc hai dòng sản phẩm (bảng 2 cột)
7. Chi tiết cấu trúc trang sản phẩm (bảng)
8. Vì sao bán được (N luận điểm, mỗi cái kèm 1 khối bằng chứng)
9. Điểm yếu khai thác được (2 cột)
10. Cái không chứng minh được + cách kiểm chứng
11. Đặt cạnh danh mục của mình + bài học lấy được
12. Footer nêu nguồn

Mỗi luận điểm "vì sao" **phải kèm 1 khối bằng chứng** trích từ dữ liệu crawl. Không có bằng chứng thì bỏ luận điểm.

Publish: skill `publish`, `content-upload.py --file "C:/.../report.html"`. Đường dẫn phải kiểu Windows có ổ đĩa.

Verify sau publish:
```bash
grep -c '—' report.html                       # phải 0 (Quang không dùng em dash)
cp <skill camofox>/scripts/verify-html-render.cjs "/d/Hermes Proj/camofox-browser/v.cjs"
cd "/d/Hermes Proj/camofox-browser" && node v.cjs "<preview_url>" ./shots
rm -f "/d/Hermes Proj/camofox-browser/v.cjs"
curl -s -o /dev/null -w "%{http_code}\n" "<preview_url>"
```
Điều kiện qua: `hOverflow:false` ở cả base và mobile, `brokenImgs:[]`, có dòng `DONE`, preview HTTP 200. Dòng `fonts:` trong output là font mặc định của script, KHÔNG phải font trang, đừng trích làm bằng chứng.

## Script `scripts/crawl-catalog.py`: cách dùng và kết quả đã kiểm

```bash
# Luon truyen --listing la URL nguoi dung dua. Script tu suy ra --prefix tu do.
python scripts/crawl-catalog.py --domain greentechvs.com --listing /san-pham/ --out out.json

# Khong co prefix thi de script tu do; nhung PHAI kiem tra so luong tim duoc
python scripts/crawl-catalog.py --domain example.com --out out.json
```

| Site | Sitemap chon | URL tim duoc | Ghi chu |
|---|---|---|---|
| greentechvs.com | product-sitemap.xml | 77 | WooCommerce, SP o slug goc + slug toan so |
| vinavetco.com.vn | product-sitemap.xml | 228 | SP o /san-pham/<slug>, domain doi .com.vn sang .com |

So luong crawl duoc co the thap hon so luong tim thay 1 hoac 2 do trang fetch loi. Script co log dong `LOI`. Do la binh thuong, khong phai bug.

### Thu tu uu tien khi chon URL (da tra gia bang loi that)

1. **Sitemap tu ten la sitemap san pham** thi tin tuyet doi moi `<loc>`, chi tru trang danh muc goc.
   Dat TRUOC bo loc prefix. Da dinh loi: loc prefix truoc lam vinavetco bi cat 228 xuong 97.
2. **Bo loc prefix** (`/san-pham/`), dung khi site khong co sitemap ten "product".
   Can `>= 3` ket qua moi dung, neu khong thi roi xuong buoc sau.
3. **Heuristic slug**: chap nhan duong dan nhieu cap duoi `/san-pham/`, `/thuoc/`, `/product/`; chap nhan slug 1 cap.
4. **Host chiem uu the** trong chinh sitemap. Day la buoc cuoi, script in `[warn]` vi CO THE LAN BAI VIET.

### Ba loi da dinh, dung sua lai

- **Khong duoc ap heuristic slug len sitemap ten "product".** WooCommerce hay dat san pham o slug
  toan so (`/1175/`, `/738/`) hoac slug ngan. Ap heuristic lam mat 4 san pham: 77 xuong 73.
- **Khong duoc loc theo domain nguoi dung nhap.** Nhieu site doi domain (vinavetco.com.vn sang
  vinavetco.com). Phai lay host tu chinh cac `<loc>` trong sitemap.
- **Khong duoc tra ve sitemap dau tien fetch duoc.** Mot lan fetch loi se khien script chon nham
  `page-sitemap.xml` va bo sot gan het san pham: 77 xuong 3. Phai thu het roi uu tien ten co "product".

### Gioi han da biet

- **Site dung JS (Next.js, React) hoac HTML tinh khong WordPress**: tu dong do duoc khong dang tin.
  Da thu vemedim.com (sitemap-0/sitemap-1 kieu Next.js): do ra hang nghin URL lan ca trang tin.
  Truong hop nay **phai** truyen `--prefix` va **kiem tra tay**: so sanh so luong script bao voi so
  san pham hien tren trang danh muc.
- **Site chan bot**: neu crawl xong ma ten san pham rong hang loat, mo bang browser that.
- **Server se cham dan neu bi goi don dap.** Khong chay nhieu lan crawl day du lien tiep mot site.
  Giam `--workers` (mac dinh 8, thu 4) hoac dung `--limit` khi chi kiem tra.

## Pitfalls

- **Dung `read_file` doc HTML crawl ve** se tra kem so dong va hong parse.
  Dung `open(f, encoding='utf-8', errors='ignore')` trong Python.
- **Menu có danh mục rỗng.** Đếm sản phẩm thật trên từng trang danh mục, đừng tin menu. Danh mục 0 sản phẩm = dấu hiệu mở rộng dàn trải, ghi vào phần điểm yếu.
- **Site phân trang 12 sản phẩm/trang** — nhưng sitemap đã có hết, dùng sitemap.
- **Mô tả sản phẩm trùng lặp giữa các sản phẩm** (cùng 1 template) — đếm số sản phẩm có field, đừng đếm số lần xuất hiện chuỗi.
- **Số điện thoại trong HTML bị nhiễu** bởi CSS/JS (regex bắt được `045 1.584 0.132` từ code). Nếu cần số thật, giới hạn regex vào phần text mô tả sản phẩm, không quét cả file.
- **Phân loại chức năng làm thủ công bằng keyword sẽ chồng nhóm** (1 sản phẩm vào 3 nhóm). Đó là đặc trưng thật của danh mục (họ cố ý viết công dụng rộng), nêu trong báo cáo chứ đừng cố ép về 1 nhóm.
- **Không bịa số.** Mọi con số trong báo cáo phải truy được về JSON crawl hoặc trang nguồn.
