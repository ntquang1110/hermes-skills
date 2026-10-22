# Vietnam market price research (giá thị trường VN) — verified workflow (08/2026)

Goal: tìm giá thật + nhà cung cấp cho nguyên liệu/hóa chất bán tại VN, mọi con số phải trace về URL đã mở được, không bịa.

## Search strategy (các engine bị chặn)
- Google: CAPTCHA "lưu lượng truy cập bất thường" ngay cả qua Camofox browser (IP bị flag) → không retry >2 lần.
- Bing qua browser: kết quả chung chung/kiểu từ điển với query sản phẩm tiếng Việt → bỏ.
- **HOẠT ĐỘNG TỐT: DuckDuckGo HTML qua Camofox browser** — `browser_navigate("https://html.duckduckgo.com/html/?q=<từ khóa>")`. Snippet thường chứa NGUYÊN bảng giá (listing Shopee/Lazada) — snippet chính là bằng chứng; URL result là price_source. (DDG html qua curl bị chặn — phải qua browser thật.)
- Curl trực tiếp chạy tốt trên nhiều site hóa chất VN (WordPress server-rendered) → verify giá bằng cách curl chính trang sản phẩm/bài giá.

## Query patterns cho ra giá
- "<chất> giá bao nhiêu 1kg/1 tấn", "giá <chất> mới nhất", "mua <chất> giá bán"
- Khoáng sản khối lượng lớn (bentonite/zeolite/kaolin/than hoạt tính): "giá bao nhiêu 1 tấn" → công ty khai thác/phân phối VN, giá theo tấn.
- **Trang bài "giá X mới nhất là bao nhiêu" là mỏ vàng**: hoachatthienvinh.com/gia-kem-oxit..., khainhat.vn/gia-dong-sunfat/, hoachatvietmy.vn/gia-bentonite-moi-nhat..., memart.vn/bao-gia-zeolite-hat... → khoảng giá có ngày, dạng "95.000 – 115.000 VNĐ/kg" (dấu chấm phân tách nghìn, en-dash).

## Site verify OK qua curl (08/2026)
vietchem.com.vn (nhiều sp chỉ "Liên hệ"), hoachatvietmy.vn, khainhat.vn, hoachathaidang.vn, hoachatthienvinh.com, itaco.com.vn, memart.vn, vtchemical.com, hoachattrantien.com, commerce.hanteco.vn, dapchem.com, michem.vn, thinhphucgroup.vn, hoangphatjsc.com, apcchem.vn, latacita.vn, sannhakhoa.vn.

## Site chết/chặn (đừng tốn turn)
hoachat.vn, hoachatthanhtri.vn, hoachat24h.com.vn, sieuthihoachat.com.vn, hcmchem.com, vietnamchemicals.vn, dongduongchem.vn, megavchem.com, chodansinh.vn, khoangsanviet.vn, vinavico.vn (curl 000/timeout); thegioihoachat.com.vn = chemworld.vn shell cũ (HTTP 200 nhưng trang 7398-byte, search `/?s=` luôn trả trang chủ, `/tim-kiem` 404); hoachatvn.com = site bài viết không bán hàng.

## Kênh giá tổng hợp: websosanh.vn (curl thuần, KHÔNG cần login) — ưu tiên #1
- URL: `https://websosanh.vn/s/<urlencode-query>.htm` — vd `.../s/acid%20citric%2025kg.htm`. Chạy tốt bằng curl + UA Chrome desktop, không CAPTCHA, không login.
- Tổng hợp giá Shopee/Tiki/Lazada; link "Tới nơi bán" trỏ thẳng listing gốc → dùng làm price_source.
- **Mẹo giá sỉ**: thêm quy cách vào query (`acid citric 25kg`, `Bacillus subtilis`, `men tiêu hóa chăn nuôi`) để ra giá bao 25kg/nguyên liệu thay vì lẻ 1kg/hộp tiêu dùng.
- Parse: strip tag → regex `([A-ZÀ-Ỹ][^.]{10,150}?)\s*([\d][\d.,]*\s*(?:đ|₫))` → lọc nhiễu mỹ phẩm/TPBVSK (serum, toner, tẩy da, peeling, viên uống, kẹo, kem, gel, sữa rửa, dầu gội, nước hoa, dưỡng).
- Shopee search trực tiếp bị login-gate → websosanh là đường thay thế xem giá Shopee.
- DDG html qua curl: query ĐẦU có thể ra kết quả, sau đó rate-limit trả trang rỗng (sleep 3-4s + retry không cứu) → nếu cần nhiều query, dùng websosanh hoặc browser thật.

## Trích xuất giá
Python: strip tags → `html.unescape` → collapse whitespace → regex
`.{50}(?:\d{1,3}\.\d{3}\s*[-–]\s*\d{1,3}\.\d{3}|\d{1,3}\.\d{3}\s*(?:đồng|₫|VNĐ))` → in ±200 ký tự ngữ cảnh.
Format VN: "80.000 – 90.000 VNĐ/kg", "2.000.000 – 3.500.000 đ/tấn".

## Worked example 3 — tinh dầu / dược liệu / chiết xuất thực vật (15/08/2026, DDG qua Camofox + curl trực tiếp)
- Tinh dầu oregano/kinh giới: 650.000đ/chai (kobi.vn); bán sỉ 1.400.000–1.500.000 đ/kg/lít (oilcare.vn/san-pham/tinh-dau-kinh-gioi-gia-si).
- Tinh dầu vỏ quế: 550.000–600.000 đ/kg (tinhdauylang.com); sỉ 700.000–800.000 đ/kg (oilcare.vn).
- Eugenol/đinh hương: 45.000–180.000 đ/chai (thitruongsi.com); Kobi 350.000đ/chai.
- Menthol tinh thể: ~20.000.000 đ/kg (3cshop.vn, độ tinh khiết cao); tinh dầu bạc hà 1.500.000 đ/lít (icharm.vn).
- Vỏ lựu khô dược liệu: 180.000 đ/kg (trungtamduoclieu.vn); bột vỏ lựu xuất khẩu 175.500–198.000 đ/hộp (goce.vn).
- Curcumin 95%: 385.000–500.000 đ/kg (tinhbotnghekc.com/curcumin95); Websosanh 764.500–1.465.200 đ/kg tùy chuẩn; bột nghệ thô rẻ hơn nhiều (50–100k/kg).
- Berberin viên dược: 7.000–78.300 đ/hộp (nhathuoclongchau, pharmacity) — dạng viên, không phải giá nguyên liệu bột.
- Tannic acid 95% (CAS 1401-55-4, Acros): 1.300.000 đ/kg chưa VAT (hoachatthinghiem.org).
- Alibaba VN (vietnamese.alibaba.com/g/...): giá FOB chiết xuất thực vật ~938.000–1.018.000 đ/kg (grape seed, allicin) — ghi rõ là giá FOB nhập khẩu.
- **Feed-grade chiết xuất chuẩn hóa (Silvafeed tannin, Macleaya/sanguinarine, coated butyrate): chỉ "Liên hệ" / không niêm yết** → verified=false, availability=Đặt hàng riêng/Nhập khẩu, đừng bịa.
- Phân biệt bột thô vs chiết xuất chuẩn hóa: bột nghệ/bã trà/bã hạt nho rẻ (vài chục nghìn/kg) nhưng chiết xuất 95% đắt gấp 5-25x — ghi cả 2 mức khi tìm được.

## Luật bằng chứng
- Mọi con số giá phải trace về URL đã mở (price_source).
- Nhiều sp công nghiệp (ZnO/CuSO4 của vietchem) chỉ ghi "Liên hệ" → không có giá công khai → ghi "Chưa có giá công khai" + availability từ ai đang bán.
- Shopee JS-heavy khó mở trực tiếp → snippet DDG của listing đó là bằng chứng, ghi URL listing làm price_source.

## Worked example (8/2026 — đã mở trang verify)
- ZnO 99,8%: 95.000–115.000 đ/kg (hoachatthienvinh.com, 11/2025); Shopee lẻ 1kg ~195.000 đ.
- CuSO4.5H2O: 80.000–90.000 đ/kg công nghiệp (hoachathaidang.vn bảng giá); lẻ ~150.000 đ/kg (khainhat.vn).
- Bentonite: 2.000.000–3.500.000 đ/tấn (itaco.com.vn); API grade 1,8–1,9tr/tấn; lẻ mỹ phẩm 70.000–1.650.000 đ/kg (hoachatvietmy.vn).
- Zeolite: 2.000.000–4.500.000 đ/tấn hạt VN (memart.vn); hạt 20kg ~180.000 đ/bao, bột ~10.000 đ/kg (vtchemical.com).

## Worked example 2 — phụ gia thức ăn chăn nuôi / probiotic / acid hữu cơ (8/2026, qua websosanh)
- Bacillus subtilis bào tử nguyên liệu (10^10-10^11 CFU/g, 1kg): 280.000–480.000 đ/kg (query `Bacillus%20subtilis`) — probiotic bulk có giá công khai, báo theo CFU/g.
- Men tiêu hóa chăn nuôi premix 1kg: 100.000–334.000 đ/kg (`men%20tiêu%20hóa%20chăn%20nuôi`; vd Lacto Zyme RBS10 ~334.330đ, DR Men tiêu hóa Plus ~100.000đ).
- Acid citric bao 25kg E330 (mono + anhydrous): 670.000–1.000.000 đ/bao ≈ 27.000–40.000 đ/kg; lẻ 1kg thực phẩm 120.000–140.000 đ (`acid%20citric%2025kg`).
- Acid formic 98-100% lab 500ml: 225.600–235.710 đ; acid lactic lab 500ml: 170.000–186.120 đ — công nghiệp 85%/80% chỉ "liên hệ".
- MCT oil C8/C10 (dầu dừa phân đoạn): 250.000–880.000 đ/chai lẻ (`MCT%20dầu%20dừa`).
- S. boulardii, Lactobacillus/Bifidobacterium/E. faecium, MOS, FOS, sodium butyrate coated, tributyrin, postbiotic: chỉ có TPBVSK tiêu dùng (Normagut 242k, BodyBio butyrate 1,49–1,9tr/hộp, siro FOS Tiens 150–250k...) → feed-grade không có giá công khai → ghi "Chưa có giá công khai", availability Nhập khẩu/Đặt hàng riêng/Khó tìm, verified=false.
