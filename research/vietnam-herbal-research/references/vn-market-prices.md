# Giá thị trường VN cho nguyên liệu thảo dược/hoạt chất (TĂCN, thú y)

Session 08/2026 (piglet-diarrhea-compounds, task prices_A.json — 14 hoạt chất chống tiêu chảy heo con). Bị gián đoạn bởi tool-iteration limit sau khi verify 1 giá + xác nhận pipeline. Trạng thái: file `data/prices_A.json` CHƯA được ghi — session kế tiếp phải tiếp tục research 13 chất còn lại.

## ✅ ĐÃ HOÀN THÀNH (bổ sung 15/08/2026 — đọc kỹ, đè trạng thái cũ)

Research giá cho cả 40 chất ĐÃ XONG, ghi vào `D:/Hermes Proj/piglet-diarrhea-compounds/data/prices_{A,B,C}.json`:
- **prices_A.json** (14 botanicals) — 12/14 verified giá thật (tannic acid 1.3tr/kg, curcumin 95% 385-500k/kg, tinh dầu oregano 1.4-1.5tr/kg sỉ, cinnamaldehyde 550-800k/kg, berberine viên 7-78k/hộp, vỏ lựu 180k/kg...)
- **prices_B.json** (13 probiotic/acid) — 2/13 verified (Bacillus subtilis 280-480k/kg @10^10-10^11 CFU/g; citric 27-40k/kg bao 25kg); formic/lactic có giá lab; còn lại "Chưa có giá công khai" (feed-grade nhập khẩu qua đại lý TACN)
- **prices_C.json** (13 khoáng/clay) — 5/13 verified (ZnO 95-115k/kg, CuSO4 80-90k/kg, bentonite 2-3.5tr/tấn, zeolite 2-4.5tr/tấn, ORS 5-15k/gói); còn lại chưa verify
- Google Sheet đã thêm 3 cột (Mức độ hiệu quả/ưu tiên mua A/B/C, Giá thị trường, Nơi bán) + 2 cột tính lượng mua (Liều tính g/kg, Lượng mua = TỔNG CÁM × liều / 1000) + block tham số (Số con, Cám/con/ngày, Số ngày → TỔNG CÁM). Sheet: `<SHEET_ID>`.
- Priority map: `priority_map.json` (A=12 chất mua trước, B=20 cân nhắc, C=8 thử nghiệm — ZnO liều cao CẤM EU nằm C). Liều tính: `dose_map.json`.

## Pipeline tìm giá (đã chứng minh hoạt động)

1. **Search bằng DDG qua Camofox** — Google/Bing/curl-DDG đều chặn từ IP VN:
   `python scripts/camsearch.py "<query tiếng Việt>" 10` (skill camofox-browser, scripts/camsearch.py)
2. **Mở từng URL kết quả bằng `page_text()`** để trích giá thật (₫/kg, ₫/lít, nồng độ).
3. Ghi vào JSON schema bên dưới; mọi con số phải có `price_source` là URL đã mở được.
4. Nếu không tìm được giá công khai: `price_range_vnd="Chưa có giá công khai"`, `verified=false`, availability ước lượng hợp lý ("Đặt hàng riêng"/"Nhập khẩu").

## Schema JSON (prices_A.json)

```json
{"id":"slug", "name_vi":"Tên", "effectiveness":"Cao|Trung bình|Thấp",
 "price_range_vnd":"khoảng giá VNĐ/kg hoặc VNĐ/lít",
 "price_source":"URL nguồn giá", "suppliers_vn":["Tên công ty - website hoặc TP.HCM/Hà Nội"],
 "availability":"Dễ mua|Phổ biến|Đặt hàng riêng|Nhập khẩu|Khó tìm",
 "notes":"ghi chú ngắn", "verified":true/false}
```

## Giá đã verify (URL đã mở thật)

- **Tannic acid 95%** (CAS 1401-55-4, Acros, lab-grade): **1.300.000₫/kg chưa VAT 8%** (quy cách 500g/1kg/5kg). Nguồn: https://hoachatthinghiem.org/product/tannic-acid-95-cas1401-55-4/ — Hóa Chất Thí Nghiệm (SBC Vietnam), 568/52 Lê Văn Việt, Long Thạnh Mỹ, Q9, TP.HCM, hotline <PHONE>. Lưu ý: đây là axit tannic phòng thí nghiệm, KHÔNG phải tannin hạt dẻ feed-grade.
- **Silvafeed / SilvaFeed Nutri P** (tannin hạt dẻ tự nhiên feed-grade, Italy): phân phối VN qua **Công ty TNHH MTV Dinh Dưỡng Ánh Dương Khang** (anhduongkhang.com/san-pham/silvafeed-nutri-p/). ĐC: 90/19 Đường số 2, KP.1, P. Phú Mỹ, Quận 7, TP.HCM. Hotline: 0938.171.477. Có VP Bắc: 105 Hoàng Văn Thái, Tân Bình, Hải Dương. Giá: "Liên hệ". Availability: Đặt hàng riêng.

## NCC đã verify — hoạt chất tinh khiết (09/2026)

### Eucalyptol / 1,8-cineole (CAS 470-82-6, C₁₀H₁₈O)
- **VietPlantEx** (sản xuất tại VN) — vietplantex.vn/eucalyptol-98/ — Eucalyptol 98%
- **Tinh Dầu Thảo Dược** — tinhdauthaoduoc.com/san-pham/eucalyptol-1-lit/ — Eucalyptol 99.6-99.8%, 1 lít
- **Tinh Dầu Dược Phẩm** — tinhdauduocpham.com/san-pham/tinh-dau-tram-99-eucalyptol-gia-si/
- **Tinh Dầu Facare** — tinhdaufacare.com.vn/san-pham/eucalyptol-99-cineole-99/
- **Theorem Chemical** (TQ, có VN page) — theoremchem.com/vi/eucalyptol/

### Thymol (CAS 89-83-8, C₁₀H₁₄O)
- **Hóa Chất Nam Định** (VMC Group) — hoachatnamdinh.com/san-pham/thymol-c10h14o-dv/
- **Đông Nam Lab** — dongnamlab.com/san-pham/75740/
- **Theorem Chemical** (Thượng Hải, có VN page) — theoremchem.com/vi/thymol-98/ — Thymol 98%
- **Food Sweeteners / Newseed Chemical** (TQ) — foodsweeteners.com/vi/products/thymol-vi/ — ***có mẫu free 100-500g, chỉ trả ship***
- **Uniproma** — vi.uniproma.com/profuma-tml-thymol-product/
- **Shopee VN** — Qinghekang Thymol 99% (500g-1000g)

### Berberine HCl (CAS 633-65-8, C₂₀H₁₈ClNO₄)
- **Công ty XNK Xuân Dương** (Hoài Đức, Hà Nội) — trangvangvietnam.com/sp/55266/berberin-hcl
- **Thạch An** — thachan.com — Berberine Hydrochloride
- **Collagensei** — collagensei.com/vi/nha-cung-cap-chiet-xuat-thao-moc/bot-berberine-hcl/
- **SOST** — sostapi.com/vi/berberine-hydrochloride-powder/
- **Sun Life Company** — đăng bán trên FB group Hội Hóa Chất VN

### Propolis extract (keo ong)
- **Unilab Vietnam** — unilabvietnam.vn/product/chiet-xuat-keo-ong-propolis-extract/
- **MKVN Chemicals** — mkvn-chemicals.com — chiết xuất keo ong
- **Nguyên Liệu Y Dược** — nguyenlieuyduoc.com.vn/chiet-xuat-keo-ong-propolis-extract
- **Nguyên Liệu Làm Mỹ Phẩm HCM** — nguyenlieulammyphamhcm.com — chiết xuất keo ong Hàn Quốc

### Tannin chestnut (feed-grade)
- **Ánh Dương Khang** — anhduongkhang.com/san-pham/silvafeed-nutri-p/ — SilvaFeed Nutri P (Italy)
- **Hóa Chất Thí Nghiệm** — hoachatthinghiem.org/product/tannic-acid-95-cas1401-55-4/ — tannic acid 95% lab-grade (KHÔNG phải feed-grade, giá 1.3tr/kg)

### Glycyrrhizin / Glycyrrhizic acid
- Dược liệu VN: các công ty dược liệu như Nam Hà, Dược liệu TƯ2 (cần search lại link cụ thể)
- Thường bán dưới dạng "cam thảo bột" hoặc "glycyrrhizin extract", giá ~200-400k/kg

## Site chặn / domain chết (verified 09/2026)

- thegioihoachat.com.vn → 403 cả curl lẫn browser
- vietnamchemicals.vn → không kết nối được
- **baothy.vn** → HTTP 000 (domain chết). Từng được ghi là NCC Thymol/Carvacrol — KHÔNG còn tồn tại.
- **senvang.com** → HTTP 000 (domain chết). Tương tự baothy.vn.
- hoachatthinghiem.org, shopee.vn, nhathuocbachmai.vn, nhachannuoi.vn, anhduongkhang.com → mở được.

## Search fallback (khi Camofox browser bị lỗi)

Khi Camofox (port 9377) không tạo được tab (500/503/timeout) mà cần research VN supplier gấp:
1. **Dùng Hermes browser tool trực tiếp** — navigate `https://duckduckgo.com/?q=<query>&ia=web` (DDG không chặn qua Hermes browser).
2. Đọc snapshot để lấy link kết quả, click từng link để verify.
3. **websosanh.vn** vẫn hoạt động qua curl đơn thuần (`urllib` Python) — dùng để tra giá và tìm supplier.
4. Nếu cần search nhiều query: mỗi query tạo 1 tab mới (browser_navigate), không dùng chung tab.

## Pitfall: Feed mills ≠ Raw material suppliers

Khi ghi NCC cho nguyên liệu TĂCN: **GreenFeed, Dabaco, Japfa, Cargill, De Heus** là nhà máy sản xuất thức ăn chăn nuôi — họ **mua** nguyên liệu chứ **không bán**. Tuyệt đối không ghi các công ty này làm NCC cho hoạt chất/thảo dược nguyên liệu. Nhà cung cấp thực tế là các công ty thương mại/nhập khẩu hóa chất, dược liệu (vd Anh Dương Khang, Hóa Chất Nam Định, Đông Nam Lab, VietPlantEx...).

## Ghi chú theo chất (đã biết từ groupA_botanicals.json)

- Curcumin: phân biệt bột nghệ (vài chục nghìn/kg) vs curcuminoid 95% (đắt hơn nhiều) — ghi cả 2 nếu tìm được.
- Tinh dầu (oregano/cinnamaldehyde/eugenol/menthol): ghi giá theo lít kèm nồng độ hoạt chất (vd carvacrol %, cinnamaldehyde %).
- Berberine: tìm "berberine HCl giá" (dạng HCl tan tốt hơn, thường dùng).
- Sanguinarine: tìm "macleaya cordata extract" / "sanguinarine price" — chủ yếu nhập khẩu (Alibaba FOB).
- **Phytase/Xylanase coated**: MOQ 5kg từ Kemin/DSM/Novus. Với quy mô nhỏ (<50 heo), lượng cần chỉ ~20-30g — không đủ MOQ. Giải pháp: mua 5kg dùng dần, hoặc tìm NCC bán lẻ.
