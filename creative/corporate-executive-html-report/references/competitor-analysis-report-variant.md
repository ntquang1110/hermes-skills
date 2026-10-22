# Variant: báo cáo PHÂN TÍCH ĐỐI THỦ / danh mục sản phẩm

Dùng khi user đưa link website một công ty khác và hỏi *"scan toàn bộ sản phẩm bên này và cho anh
bản phân tích"*, *"bên này có gì"*, *"tại sao bên này bán được hàng"*.

Đây **không phải** báo cáo A4 một trang. Loại này dài, có mục lục ngầm, cuộn được.
Vẫn dùng tokens forest + gold + nền giấy của SKILL.md, nhưng bố cục khác hẳn báo cáo trial.

**Quy trình quét website (sitemap, bypass SSL hết hạn, crawl từng trang sản phẩm, bản đồ trường
WooCommerce): skill `competitor-catalog-analysis`.** File này chỉ nói về phần BỐ CỤC BÁO CÁO.

## Bố cục 11 khối (đã dùng tốt, 14/10/2026)

| # | Khối | Luật riêng |
|---|---|---|
| 1 | Masthead | Tên tài liệu + tên đối tượng + ngày quét + nguồn. Hairline dưới |
| 2 | **Statement 1 câu** | Phải là **kết luận về bản chất**, không phải mô tả. Vd *"Họ không bán sản phẩm. Họ bán phác đồ cho từng giai đoạn đàn vật nuôi."* Sai: *"Greentech có 77 sản phẩm."* |
| 3 | Dải 4 KPI | Chọn con số **gây bất ngờ**, không chọn con số to. Vd `0/77 sản phẩm có giá niêm yết` mạnh hơn `77 sản phẩm` |
| 4 | Tổng quan pháp nhân + hạ tầng | Bảng 2 cột. Bắt buộc có cả **hạ tầng** (nhà máy, cert, email, nền tảng web), không chỉ pháp lý |
| 5 | Danh mục theo chức năng | Bar chart CSS (`.bar` grid 3 cột: nhãn / thanh / số). Cộng bảng theo vòng đời |
| 6 | Kiến trúc dòng sản phẩm | Grid 2 cột đối chiếu, hai nền khác nhau |
| 7 | Chi tiết cấu trúc trang sản phẩm | Bảng: thành phần trang → nội dung + tác dụng bán hàng |
| 8 | **Vì sao bán được** | Grid thẻ 2 cột. Mỗi thẻ: số thứ tự gold + tiêu đề + đoạn lý giải + **khối bằng chứng riêng** |
| 9 | Điểm yếu khai thác được | Grid 2 cột, nền gold-soft. Tách "lỗ hổng kỹ thuật/vận hành" vs "lỗ hổng nội dung/đo lường" |
| 10 | **Chưa chứng minh được** | Bắt buộc. Bảng: chỉ tiêu → `Không có` + lý do. Kèm bảng **cách kiểm chứng** (bước 1..n) |
| 11 | Đặt cạnh doanh nghiệp user | Bảng 3 cột so sánh + callout "học được gì không tốn tiền" |

Footer: tên người viết + nguồn dữ liệu liệt kê cụ thể + câu *"Mọi con số đều truy được về nguồn"*.

## Luật cứng riêng cho loại báo cáo này

1. **Mỗi luận điểm "vì sao bán được" phải kèm 1 khối bằng chứng trích được từ web.**
   Không viết "họ marketing tốt". Viết *"menu có mục Phản hồi ngang hàng Sản phẩm, gồm N video"*.
   Bằng chứng để trong `<span class="ev">` nền forest-soft cho dễ phân biệt với lý giải.

2. **Khối 10 (chưa chứng minh được) là bắt buộc, không được bỏ.**
   Quang làm việc theo nguyên tắc *số không nguồn = không số*. Doanh thu / thị phần / số đại lý /
   giá bán thật gần như luôn là `Không có` — ghi thẳng, **không đoán, không nội suy**.
   Nhãn trong bảng dùng `<span class="tagline r">Không có</span>` (đỏ) vs `.tagline g` (vàng) cho suy luận.

3. **Bắt buộc có bảng "cách kiểm chứng nếu muốn số thật".**
   Đây là thứ biến báo cáo từ suy đoán thành kế hoạch hành động. Bước hay dùng: gọi hotline đóng vai
   người mua, ghé cửa hàng đại lý địa phương, hỏi chủ trại quen, xin phiếu kiểm nghiệm.

4. **Khối 11 phải trả lời "vậy mình làm gì khác".** Báo cáo đối thủ không có mục này thì chỉ là
   bài đọc cho biết, không ra được quyết định.

5. **Biến chướng ngại kỹ thuật thành phát hiện phân tích.** Vd chứng chỉ SSL hết hạn (khiến
   `web_extract` báo `target_unreachable`) không chỉ là lỗi cần bypass — nó là **bằng chứng công ty
   không chăm kênh online**, phải đưa vào bảng hạ tầng ở khối 4.

6. **Viết ở ngôi "em", gọi user là "anh"** trong phần chat giao hàng. Nhưng báo cáo HTML viết ở
   ngôi trung tính, không xưng hô với người đọc.

## Đừng lặp lại các lỗi này

- **Đừng liệt kê 77 tên sản phẩm rồi gọi đó là phân tích.** Phải gom nhóm và nêu tỷ lệ.
- **Đừng tự khen báo cáo.** Báo cáo bằng số và bằng chứng, không bằng tính từ.
- **Đừng slice URL percent-encode khi in ra** — mất phần định danh sản phẩm.
- **Đừng bỏ khối 10 vì "báo cáo trông thiếu".** Thiếu dữ liệu là sự thật, phải nói.
- **Đừng dùng `web_extract` cho site WooCommerce nhiều trang** — sitemap + curl nhanh và đầy đủ hơn.

## Verify sau khi publish

```bash
cp "C:/Users/<user>/AppData/Local/hermes/skills/devops/camofox-browser/scripts/verify-html-render.cjs" \
   "/d/Hermes Proj/camofox-browser/verify-<x>.cjs"
cd "/d/Hermes Proj/camofox-browser" && node verify-<x>.cjs "<preview_url>" "./shots-<x>"
rm -f "/d/Hermes Proj/camofox-browser/verify-<x>.cjs"
```

Điều kiện qua: `base.hOverflow === false` **và** `mobile.hOverflow === false`, `brokenImgs` rỗng,
`title` khớp, có dòng `DONE`. Dòng `fonts:` là font mặc định của chính script, **không phải** bằng
chứng font trang đã load — đừng trích nó.
