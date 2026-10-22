# Tra cứu toàn văn văn bản pháp luật / QCVN / TCVN chính thức (workflow đã kiểm chứng)

Mục tiêu: lấy **toàn văn tin cậy, có dấu, đúng điều khoản** của văn bản quy phạm pháp luật & quy chuẩn kỹ thuật (QCVN, TCVN, Thông tư, Nghị định, Quyết định) của Việt Nam — đặc biệt các bảng chỉ tiêu có số cụ thể (mg/L...).

## ⭐ Nguồn chính thức tốt nhất: vbpl.vn (CSDL quốc gia về pháp luật — Bộ Tư pháp)

Trong khi thuvienphapluat.vn bị **Cloudflare chặn** và vanbanphapluat.co trả HTTP 500 qua proxy browser (và curl chết im lặng), thì **vbpl.vn hoạt động ổn định, không cần đăng nhập, hiển thị cả bản scan Công báo đầy đủ (kèm bảng Phụ lục)**. Đây là nguồn chính thức nhất.

### Các bước (đã kiểm chứng 08/2026 cho QCVN 6-1:2010/BYT):

1. **Vào trang tìm kiếm:** `https://vbpl.vn/van-ban/trung-uong` (Văn bản pháp luật Trung ương).
   - Có sẵn radio search: **Nội dung / Tiêu đề / Số hiệu**; default là "Tiêu đề".
2. **Tìm theo TIÊU ĐỀ, KHÔNG theo số hiệu QCVN.**
   - ⚠️ Search theo số hiệu `QCVN 6-1:2010/BYT` → **trả 0 kết quả** (số hiệu QCVN không được index ở trường tên).
   - Thay vào đó search từ khóa tiêu đề, ví dụ `nước khoáng thiên nhiên` → tìm ra văn bản ban hành: *Thông tư số 34/2010/TT-BYT (Bộ Y tế, 02/6/2010, hiệu lực 01/01/2011)*.
   - Kết quả hiển thị: tên văn bản, trạng thái hiệu lực, ngày ban hành/hiệu lực — đủ để xác nhận văn bản gốc.
3. **Mở trang chi tiết:** các dòng kết quả là **React SPA, tiêu đề KHÔNG phải thẻ `<a>`** — nó là `<span class="cursor-pointer">`. Để mở, dùng JS trong browser console:
   ```js
   Array.from(document.querySelectorAll('span')).find(s=>/34\/2010\/TT-BYT/.test(s.textContent)).click()
   ```
   → chuyển tới URL dạng `https://vbpl.vn/van-ban/chi-tiet/thong-tu-so-34-2010-tt-byt-...-<id>?tabs=...`.
4. **Lấy toàn văn:** vào tab **"Văn bản gốc"** → trình xem PDF hiển thị nguyên bản Công báo. Section dạng `region "Page N"` chứa toàn văn (kể cả bảng Phụ lục mg/L).
   - **Mẹo quan trọng:** snapshot live của trang hiển thị PDF **bị cắt cụt** (truncated). Đọc file snapshot đầy đủ đã được lưu để lấy hết các trang: `C:\Users\<user>\AppData\Local\hermes\cache\web\browser-snapshot-*.txt`.
5. **Trích dẫn:** ghi rõ số hiệu văn bản gốc + cơ quan + ngày + Mục/Khoản/Điểm/Phụ lục. Ví dụ "QCVN 6-1:2010/BYT, Mục I.1 phạm vi; II.3.3 ghi nhãn; Phụ lục I/II chỉ tiêu hóa học".

#### Bài học 10/2026 — click tiêu đề trên vbpl.vn đôi khi không điều hướng, và cách đi vòng
Tiêu đề là `<span class="cursor-pointer">`. `dispatchEvent` với chuỗi đầy đủ
`pointerdown→mousedown→pointerup→mouseup→click` **không điều hướng**: URL đổi nhưng `location.href` giữ nguyên.
Lặp lại vô hạn không giúp (đúng như cảnh báo bên dưới).
**Đường đi hiệu quả khi click chết — không cần click ở vbpl.vn:** lấy URL chuẩn từ **LuatVietnam search**
(mở bằng `browser_navigate` để JS render, rồi đọc `href` thật trong DOM bằng `browser_console`), sau đó **curl URL đó**.
```js
// trên trang search LuatVietnam — lấy URL chuẩn, đừng click
Array.from(document.querySelectorAll('a[href]'))
  .map(a => a.getAttribute('href'))
  .filter(h => h && /dat-dai\/.*-d1\.html/.test(h) && !/#/.test(h))
  .slice(0, 10)
```
⚠️ `<id>` LuatVietnam cũng là **số tự tăng — đoán thì ra văn bản khác**: đoán `luat-dat-dai-2003-so-03-2003-qh11-108793-d1.html`
→ trả về **QĐ 14/2016/QĐ-UBND Vĩnh Long**. Phải lấy href từ danh sách, không bao giờ tự chế URL.

### Bài học 10/2026 — nghi ngờ số hiệu thì tìm theo TIÊU ĐỀ, không theo số hiệu
Tìm theo "Số ký hiệu" `03/2003/QH11` trả về **hai dòng gần trùng nhau** (`Luật Kế toán số 03/2003/QH11`
+ một dòng chỉ ghi `Luật 03/2003/QH11`) → rất dễ kết luận nhầm. Đổi sang tìm theo **"Tiêu đề"** `Luật Đất đai`
→ ra ngay **13/2003/QH11** kèm luôn chuỗi ngày ban hành / hiệu lực / hết hiệu lực ngay trên danh sách kết quả,
lộ ra cả chuỗi LĐĐ 1980/1993 → 13/2003 → 45/2013 → 31/2024 mà không cần mở tab Thuộc tính nào.
Đọc metadata vòng đời ngay trên list là **bước xác minh hiệu lực rẻ nhất** — làm trước khi cân nhắc mở tab.

## Pitfalls khi dùng vbpl.vn
- Bộ lọc (Nhóm văn bản, Cơ quan, Hình thức) mở sẵn và dài; bỏ qua, chỉ cần khung search.
- Nhấn nút "PDF"/"Lược đồ"/"Tải về" từ list có thể không điều hướng tới toàn văn — cách chắc ăn là **click trực tiếp vào tiêu đề** (bước 3) rồi mở tab "Văn bản gốc".
- Số hiệu văn bản quy phạm (Thông tư/Nghị định) có thể tra theo "Số hiệu", nhưng **số hiệu QCVN/TCVN thì không** — luôn dùng tiêu đề.
- ⚠️ **Đừng đoán `<id>` ở cuối URL chi tiết.** URL dạng `.../chi-tiet/<slug>--<id>`. Đoán số ID sẽ **âm thầm tải ra văn bản KHÁC HOÀN TOÀN** (đã kiểm chứng: đoán `--154233` trả về QĐ 11/2022/QĐ-UBND Bắc Giang thay vì Luật Đấu thầu) chứ không báo lỗi → rất dễ trích nhầm căn cứ pháp lý mà không nhận ra. Luôn lấy URL bằng cách click từ danh sách kết quả tìm kiếm.
- Click tiêu đề bằng JS đôi lúc **không điều hướng** (URL đổi nhưng `location.href` không đổi / độ dài `document.body.innerText` không đổi). Dấu hiệu nhận biết: sau khi `.click()`, `location.href` vẫn là `/van-ban/trung-uong`. Khi đó **đừng lặp lại vô hạn** (cũng không giúp) — quay lại danh sách kết quả và click lại lần nữa, hoặc điều hướng bằng URL chi tiết đã lấy được ở lần trước.
- Với ô tìm kiếm React, `browser_type` có thể trả lỗi 422 — set giá trị qua JS rồi mới click nút "Tìm kiếm":
  ```js
  const inp=document.querySelector('input[placeholder*="từ khóa"]');
  Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value')
    .set.call(inp,'24/2024/NĐ-CP');
  inp.dispatchEvent(new Event('input',{bubbles:true}));
  Array.from(document.querySelectorAll('button'))
    .filter(x=>/Tìm kiếm/.test(x.textContent))[0].click();
  ```
  Và **phải chọn radio "Số hiệu"** trước khi tìm theo số hiệu, nếu không tìm theo "Tất cả" sẽ ra nhiều kết quả nhiễu.

## ⭐ Xác minh HIỆU LỰC THẬT của văn bản — 2 tab bắt buộc (đã kiểm chứng 10/2026)

Trang chi tiết vbpl.vn có 5 tab: **Nội dung | Thuộc tính | Lược đồ | Lịch sử | Văn bản gốc**.

**Không bao giờ kết luận "còn hiệu lực" chỉ từ tiêu đề / ngày ban hành.** Phải mở **Thuộc tính** và **Lịch sử**.

### Tab "Thuộc tính" — trạng thái hiệu lực

| Trường | Dùng để |
|---|---|
| Ngày ban hành | — |
| Ngày có hiệu lực | có thể **≠** ngày ban hành; đọc thêm Điều "Hiệu lực thi hành" trong thân văn bản |
| **Tình trạng hiệu lực** | `Còn hiệu lực` / `Hết hiệu lực toàn bộ` / `Hết hiệu lực một phần` |
| **Ngày hết hiệu lực** | ngày chính xác văn bản chết — dùng cho hồ sơ có yếu tố thời điểm |

### Tab "Lịch sử" — nguồn quan trọng nhất và hay bị bỏ qua

Bảng 3 cột: `Thời gian | Trạng thái | Văn bản nguồn`. Trả lời 3 câu:

1. Văn bản đã bị **sửa đổi, bổ sung** bởi văn bản nào, từ ngày nào?
2. Văn bản đã bị **thay thế** bởi văn bản nào, từ ngày nào?
   → dòng dạng `Văn bản hết hiệu lực toàn bộ | <ngày> | <số hiệu văn bản thay thế>`
3. Luật còn hiệu lực nhưng **một phần** → tồn tại **Văn bản hợp nhất** (`NN/VBHN-VPQH`) → **phải trích dẫn bản hợp nhất**, không trích bản gốc.

Mở tab bằng JS:
```js
Array.from(document.querySelectorAll('[role=tab],.ant-tabs-tab'))
  .find(e => /Lịch sử/.test(e.textContent)).click();

// đọc panel đang hiện (lọc offsetParent để loại panel ẩn)
Array.from(document.querySelectorAll('[role=tabpanel]'))
  .filter(p => p.offsetParent !== null)
  .map(p => p.innerText.replace(/\s*\n\s*/g, ' | '));
```

### Bài học cốt lõi: số hiệu trong đề bài có thể đã chết

**Đã kiểm chứng 10/2026 — Nghị định 24/2024/NĐ-CP** (quy định chi tiết Luật Đấu thầu về lựa chọn nhà thầu):

| Mục | Kết quả |
|---|---|
| Số hiệu | `24/2024/NĐ-CP` (đúng năm 2024) |
| Ban hành / hiệu lực | 27/02/2024 — Điều 134 khoản 1: *"có hiệu lực thi hành kể từ ngày ký ban hành"* |
| Quan hệ NĐ 63/2014/NĐ-CP | **THAY THẾ** (Điều 134 khoản 1 điểm a) — không phải kế thừa |
| Sửa đổi | NĐ **17/2025/NĐ-CP** (06/02/2025) |
| **Hết hiệu lực toàn bộ** | **04/08/2025** — bị **NĐ 214/2025/NĐ-CP** thay thế |

→ Trích dẫn NĐ 24/2024 như còn hiệu lực là **sai thời điểm**. Với hồ sơ thi hành dân sự phát sinh từ giao dịch cũ, phải tra văn bản **theo thời điểm sự kiện**, không phải thời điểm hôm nay.

### Cross-validate số hiệu Luật bằng văn bản hướng dẫn nó

Khi nghi ngờ số hiệu Luật, mở toàn văn một nghị định/thông tư hướng dẫn nó. Phần **"Căn cứ ..."** và các câu dẫn chiếu trong thân văn bản ghi **tên + ngày + số hiệu luật** — đây là bằng chứng độc lập từ nguồn chính thức, mạnh hơn tin tức hay trang thứ ba.

Đã kiểm chứng: NĐ 24/2024 dẫn *"Căn cứ Luật Đấu thầu ngày 23 tháng 6 năm 2023"* và trong thân văn ghi rõ *"Luật Đấu thầu số **22/2023/QH15**"*. Số hiệu giao trong đề bài là `43/2023/QH15` → **SAI**. Nếu dùng số hiệu sai trong văn bản tư vấn / đơn tố cáo là **hỏng hồ sơ**.

## Các nguồn khác — kinh nghiệm thực tế (08/2026)
- **thuvienphapluat.vn** — blocked bởi Cloudflare ("Performing security verification"); snapshot chỉ hiện trang challenge. Có thể thử lại (cf token sinh lại mỗi lần) nhưng không đáng chờ.
- **vanbanphapluat.co** — HTTP 500 qua proxy browser; `curl` trả HTTP 000 (chết). Bỏ qua.
- **luatvietnam.vn** — truy cập được nhưng **URL đoán bừa có thể redirect sang văn bản khác** ranh như nhau; tốt hơn dùng vbpl.
- **Bing/DDG/Mojeek** (HTML/curl) — không surface đúng tài liệu cụ thể cho QCVN; bỏ công để filter.
- **searxng-search local** (127.0.0.1:8888) — có thể chưa chạy; kiểm tra `/config` trước khi phụ thuộc.

## Lưu ý pháp lý
- QCVN/TCVN là văn bản kỹ thuật; bảng chỉ tiêu (giới hạn tối đa) nằm ở **Phụ lục** của QCVN, không phải thân văn bản — phải lấy được Phụ lục mới đủ số liệu mg/L.
- Phân biệt "giới hạn tối đa an toàn thực phẩm" với "yêu cầu ghi nhãn": QCVN 6-1:2010/BYT chỉ giới hạn các chất độc/kim loại nặng (Phụ lục), còn pH/TDS/Na/K/Ca/Mg/HCO3 chỉ là yêu cầu **ghi nhãn**, không có giới hạn tối đa trong QCVN. Đọc kỹ để không bịa số.

## Nguồn chính thức khác đáng thử
- Công báo điện tử viết trên vanban.chinhphu.vn / Cổng TTĐT Chính phủ.
- vbpl.vn là chuẩn vàng cho toàn văn.
