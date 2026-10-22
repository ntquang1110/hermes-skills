# Tra nguyên liệu TĂCN trên sàn TMĐT VN (Shopee)

Tra ngày 14/10/2026, phiên Vua Kiềm R&D — 23 công thức, 22 nguyên liệu.
Dùng kèm mục **Kênh D** trong SKILL.md.

## 1. Bề mặt nào bị chặn, bề mặt nào dùng được

| Cách | Kết quả |
|---|---|
| `api/v4/search/search_items?keyword=...` | ❌ `HTTP 403`, body `{"error":90309999,"redirect_to_error_page":true}` — chặn anti-bot |
| `web_extract(<url sản phẩm Shopee>)` | ❌ `error: "bot_blocked"`, content rỗng |
| `browser_navigate` vào Shopee | ✗ trang render JS nặng, không đọc được nội dung sản phẩm |
| `web_search` với `site:shopee.vn` | ✅ trả link sản phẩm thật + tên + giá (từ snippet) |
| **TinyFish `search` + `include_domains="shopee.vn"`** | ✅✅ **tốt nhất** — snippet dày hơn `web_search`, có cả giá lẫn trạng thái `Đã bán hết`. Xem mục 1b |
| TinyFish `fetch_content(<url Shopee>)` | ❌ `bot_blocked` từng URL |
| Camofox / Obscura (browser thật) | ❌ redirect `/unsupported.html` — chặn cứng cả browser thật |
| `curl` web shop hóa chất VN | ✅ đọc được địa chỉ + giá (nguyenquan.vn, vdchem.com, hoachatdalat.com, kimmachem.com) |
| `tiki.vn/api/v2/products?q=...` | ✅ API trả JSON nhưng **0 kết quả** với mọi nguyên liệu B2B — Tiki là sàn tiêu dùng |

**Hệ quả:** chỉ đọc được *link + tên + giá + trạng thái kho* (từ snippet). **Không** đọc được: **nơi bán**, quy cách chính xác, giá sau voucher. Ranh giới đúng để nói với user:

> Em KHÔNG verify được **nơi bán** (tỉnh/thành) — anh dùng bộ lọc **"Nơi bán: Hà Nội"** trên Shopee.

Đừng nói "không check được tồn kho" — tồn kho check được, xem mục 1b. Nói sai ranh giới làm user tưởng phải tự đi kiểm tay.

## 1b. Verify tồn kho / giá bằng snippet (đây là món mới, quan trọng)

Shopee chặn cứng mọi đường đọc trang, nhưng **snippet của TinyFish `search` nhúng sẵn trạng thái kho**:

```
mcp__tinyfish__search(
  query="<tên mặt hàng> <quy cách>",
  include_domains="shopee.vn",
  location="VN",
  language="vi",
  purpose="Kiểm tra trạng thái tồn kho ..."
)
```

Ví dụ nguyên văn snippet trả về:

- `"...túi 1kg- Hàng nhập khẩu. 1/3. Đã bán hết. 185.000₫."` → **HẾT HÀNG**
- `"...1 Kg Vi Sinh Nguyên Liệu Bacillus Subtilis 100 Tỷ Cfu/gr. 1/3. 480.000₫."` → **CÒN HÀNG**

Bảng phân loại:

| Dấu hiệu trong snippet | Kết luận |
|---|---|
| `Đã bán hết` / `Hết hàng` | HẾT → loại |
| Có giá + không có chữ "Đã bán hết" | CÒN → giữ |
| `Hàng Đặt Trước (có hàng sau N ngày)` | CÒN nhưng phải chờ → giữ, ghi rõ |
| `Chọn loại hàng` + nhiều mức giá | CÒN, nhiều quy cách → giữ |
| URL không còn xuất hiện ở bất kỳ kết quả nào | Link bị xoá/ẩn → loại |
| Chỉ trả về `/blog/`, `/list/`, `/search?` | Nhiễu, không phải sản phẩm → bỏ |

Cách chạy cho một danh sách link có sẵn:

1. Nhóm link theo mặt hàng — một search phủ nhiều link cùng chất.
2. Chạy 6–8 query song song mỗi lượt (`include_domains="shopee.vn"`, `location="VN"`, `language="vi"`).
3. Khớp URL trả về với danh sách gốc **theo đuôi `-i.<shopid>.<itemid>`** — phần percent-encode tiếng Việt có thể khác nhau giữa hai lần trả, đuôi `-i.` thì ổn định.
4. Loại link hết hàng, **và giữ luôn link mới tìm được mà còn hàng**. Đây không chỉ là lọc, mà là bổ sung lựa chọn thay thế — làm user thấy được việc.
5. Ghi lại thành 2 khối: `CÒN HÀNG` + `ĐÃ LOẠI` (kèm mã `i.<shopid>.<itemid>` và lý do). Gạch ngang khối đã loại để user đối chiếu.

### ⚠️ Tồn kho bán lẻ TRÔI — luôn re-verify trước khi chốt danh sách mua

Đo thật 14/10/2026 trên 43 link: **7 link chết** (6 sold out + 2 link tannin bị xoá hẳn khỏi Shopee), tức khoảng **1/6 danh sách hỏng trong một vòng tra**.

Vì vậy:
- Bảng ở **mục 4 dưới đây là ảnh chụp tại một thời điểm**, không phải bảo đảm. Phải chạy lại mục 1b trước khi đưa user đi mua.
- Khi một món hết hàng, **đừng chỉ xoá dòng** — đi tìm link thay thế. Ví dụ thật: Phytase 10.000 U/g hết → đã thay bằng bộ enzyme đơn dòng 1 kg (có cả Protease) và Phytase 100.000 U/g (dùng 1/10 lượng, bù nồng độ).
- Món có nguy cơ **mất sạch link** cao nhất là mặt hàng hiếm: tannin nguyên chất. Đã có lúc cả 2 link tannin biến mất cùng lúc. Với món hiếm, luôn có phương án kênh A/B dự phòng trong output, đừng để user mất cả hai đầu.


## 2. Query ăn / query chết

Ăn (1–3 từ, một từ khóa một lần):
```
site:shopee.vn "phytase"
site:shopee.vn "bacillus subtilis"
site:shopee.vn "magie oxit"
site:shopee.vn "acid citric" 1kg
site:shopee.vn "tinh bột nghệ" curcumin 1kg
site:shopee.vn "hoàng liên" bột
site:shopee.vn eucalyptol
site:shopee.vn "sodium ascorbyl phosphate"
site:shopee.vn "bột tannin"
site:shopee.vn "L-tryptophan" nguyên liệu bột
```
Chết (trả rác, mất toán tử `site:`):
```
site:shopee.vn thymol 99% bột nguyên chất     → trả về pubmed, oxfam, podcast
site:shopee.vn "cao cam thảo" hoặc "bột cam thảo"   → "hoặc" phá query
site:shopee.vn "dung dịch acid lactic" thực phẩm 1 lít  → 0 kq
site:shopee.vn "xylanase" enzyme 1kg chăn nuôi  → 0 kq
```
Bài học: query 5+ từ hoặc có `hoặc`/`OR` → backend trả về kết quả *ngữ nghĩa* bỏ qua `site:`. Giữ 1–3 từ.

## 3. Xử lý URL — bắt buộc full

Link Shopee dạng: `https://shopee.vn/<slug>-i.<shopid>.<itemid>`

- **Không slice.** `url[:150]` cắt mất `-i.<shopid>.<itemid>` → link không định danh được sản phẩm nào.
- Ghi ra JSON file rồi nạp lại (`json.dump`), không giữ trong biến rồi in cụt.
- Lọc bỏ rác: `*/list/*`, `*/search?*`, `ads.shopee`, `/blog/`, shop landing page không phải sản phẩm. Chỉ giữ URL khớp `-i\.\d+\.\d+$` hoặc `/product/`.
- **Suy URL shop:** `...-i.1129318902.51660140469` → `https://shopee.vn/shop/1129318902`

## 4. Bản đồ thực nghiệm (14/10/2026)

### ✅ CÓ trên Shopee, đúng túi 1 kg — mấy món dùng nhiều nhất đều có

| Món | Quy cách | Giá |
|---|---|---|
| Phytase | Enzyme Phytase 10.000 U/g, túi 1 kg, nhập khẩu | — |
| Phytase + Protease | Bộ enzyme đơn dòng Amylase/Cellulase/Protease/Phytase 1 kg | — |
| Phytase | Phytase 100.000 U/g, bột 1000 g | — |
| Phytase | 25 kg cho heo/bò/gà/vịt | 3.750.000đ |
| Phytase + Xylanase | ZYME FISH+ 1 kg | 115.000đ |
| **Bacillus subtilis** | **1 kg, 100 tỷ CFU/gr** | **480.000đ** |
| Bacillus subtilis | túi 200 g | ~100.000đ |
| **Betaine HCl 98%** | hàng chăn nuôi/thủy sản | — |
| Betaine HCl | CAS 590-46-5 | — |
| L-Tryptophan | bán buôn cấp thực phẩm | — |
| MgO | 1 kg (Gốm LaTacita) | 114.000đ |
| MgO | túi 250 g, có CAS 1309-48-4 | 130.000đ |
| Magiê Citrate | CAS 7779-25-1 | — |
| Acid citric | 1 kg | từ 65.000đ |
| Polysorbate 80 | 100 g (Rumilab) | 45.000đ |
| Sodium ascorbyl phosphate | 10–50 g (Chemielab) | — |
| Beta-glucan | dạng tỏi, cho vật nuôi | 167.000đ |
| Tannin | bột 99%, 100 g | — |
| Eucalyptol | = tinh dầu tràm 99%, 0.5–1 lít, **có phiếu kiểm nghiệm** | — |
| Curcumin | tinh bột nghệ nano, 500 g / 1 kg | — |
| Berberine | bột hoàng đằng (nam hoàng liên), 100 g / 500 g / 1 kg | — |
| Carvacrol | tinh dầu oregano | — |

### 🏆 Shop vàng — bán buôn nguyên liệu cấp thực phẩm
`https://shopee.vn/shop/1129318902` — có **4 món cùng lúc**: Phytase 100.000 U/g, Betaine HCl (CAS 590-46-5), Magiê Citrate (CAS 7779-25-1), L-Tryptophan. Ghi riêng trong output như mục "vào đây trước".

### ❌ KHÔNG có trên Shopee (11 món) — phải đi kênh A / nhập

| Món | Tình hình |
|---|---|
| **Thymol** | Chỉ có tinh dầu cỏ xạ hương; **không có thymol tinh thể**. Lưu ý "xạ hương" trên Shopee phần lớn là **musk** (nước hoa), không phải thyme |
| **Vitamin E TPGS** | Không có — nhập PMC Isochem (Pháp) / alphahi-tech (TQ) |
| **Acid lactic** | Chỉ có mỹ phẩm / kẹo |
| **Butyrate (Ca/Na)** | Không có — xin mẫu Acare / ICFOOD |
| **Tannin Chestnut** | Không đúng loại Silvafeed — Ánh Dương Khang |
| **Glycyrrhizin chiết** | Chỉ có "bột cam thảo" = rễ nghiền, KHÔNG phải glycyrrhizin |
| Selenium yeast | Không có |
| Propolis bột | Không có dạng bột nguyên liệu |
| Ích mẫu | Không có |
| Huyết dụ | Không có |
| Lá hẹ | Không có dạng bột nguyên liệu |

## 5. Thứ tự hành động đúng khi user cần mua nguyên liệu lô thử

1. Tính lượng cần cho toàn bộ công thức (xem mục *Toán lượng mua* trong SKILL.md) — ra con số gram.
2. Tra **kênh D trước** cho nhóm dễ (enzyme, probiotic, khoáng, acid, dược liệu, tinh dầu) — vì đây là nơi MOQ 1 kg thật.
3. Phần còn lại mới đi kênh A (hóa chất bán lẻ) → kênh B (xin mẫu) → nhập.
4. Trong output: nhóm theo trạng thái mua, mỗi món 1–4 link, tách rõ `đúng quy cách` vs `phải hỏi shop`, kèm ranh giới không-verify-được-nơi-bán.
