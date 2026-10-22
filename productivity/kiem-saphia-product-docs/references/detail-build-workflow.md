# Detail build workflow — template-based local pages (12/08, tested Greenfeed + Tuấn)

Workflow để dựng trang detail 3 ngôn ngữ (VI/EN/ZH) từ `detail-template.html`, lưu local `detail/<case>.html`, KHÔNG push gist. Đã dùng thành công cho `greenfeed-300-2025.html` + `tuan-8-con-asf-2025.html`.

## 1. Đọc file gốc (docx/doc)

- `scripts/read_docx.py` **TRUNCATE** output: paragraph 120 ký tự, cell 40 ký tự → chỉ đủ xem cấu trúc, KHÔNG đủ dữ liệu. Phải dump full:
```python
import docx
d = docx.Document(path)
for p in d.paragraphs: print(p.text.strip())          # full paragraphs
for i, tb in enumerate(d.tables):
    ncols = len(tb.columns)
    cells = tb._cells                                  # grid-expanded
    for r in range(len(tb.rows)):
        print(" | ".join(cells[r*ncols+c].text.strip() for c in range(ncols)))
```
- **Ô MERGED**: `r.cells` trả cell lặp lại nhưng python-docx dedupe khi in trực tiếp (`" | ".join(...)` qua `c.text` ở cùng row chỉ in 1 giá trị) → **bắt buộc dùng `tb._cells`** (mỗi vị trí grid 1 cell, merged lặp giá trị). Thiếu bước này sẽ mất giá trị cột 2 của hàng merged (VD "Số lượng ban đầu | 150 | 150" in thành "150" 1 lần).
- File `.doc` có thể thực chất là `.docx` (header PK zip) → python-docx đọc bình thường, đừng đổi công cụ.
- Chạy bằng `python3.14` (có python-docx), heredoc qua terminal.

## 2. Build HTML

- Copy skeleton từ `detail-template.html` (CSS, topbar, lang-switch, backlink, JS block applyLang/WeakMap ORIG/localStorage `ks_lang`/`?lang=` override). Placeholder: `@@TITLE@@`, `@@BODY@@`, `@@I18N@@` (hoặc theo tên trong template).
- **I18N dict**: viết Python dict `D[vi_text] = {"en": ..., "zh": ...}` rồi `json.dumps(D, ensure_ascii=False, separators=(',',':'))` chèn vào `const I18N = <json>;` — KHÔNG viết tay JSON 1 dòng (escape sai = trang chết âm thầm). Thêm key identity (`en`/`zh` = chính text) cho: nút ngôn ngữ (VI/EN/中), tên sản phẩm (Kiềm EZ 80, Kiềm DL), cell thuần data chứa ký tự Việt (VD "8.606.250 VND ... 57.375 VNĐ/con").
- **execute_code sandbox cwd = `D:\Hermes Proj`** (workspace root), KHÔNG phải project dir → luôn ghi file bằng ABSOLUTE path + `os.makedirs(outdir, exist_ok=True)`. File tạm cũng rơi vào cwd — dọn sau.
- Mọi text node tiếng Việt trong body CẦN key: badge, h1, meta, docnote, footer, h2/h3, mọi ô bảng có chữ Việt. Quy ước dịch: giữ số liệu/đơn vị/tên riêng; EN đổi dấu phẩy thập phân sang chấm (98,67% → 98.67%); ZH giản thể.

## 3. Verify tĩnh (bắt buộc — camofox hay kẹt, và nhanh hơn browser)

- html.parser thu text node leaf (skip script/style bằng depth counter):
```python
class Collector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.nodes=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.skip += 1
    def handle_endtag(self, tag):
        if tag in ('script','style') and self.skip: self.skip -= 1
    def handle_data(self, data):
        if self.skip == 0 and data.strip(): self.nodes.append(data.strip())
```
- Mọi node có dấu tiếng Việt (regex `[àáảãạ...đĐ...]`) HOẶC CJK phải có key → missing = 0. Node thuần data (số/đơn vị/ngày/"-") không cần key.
- Mô phỏng applyLang trong Python: với từng lang en/zh, thay node theo dict rồi check target không còn dấu Việt — ngoại lệ hợp lệ: tên riêng giữ nguyên (Kiềm EZ, Vua Kiềm...). Cái này bắt được lỗi "bản EN/ZH còn tiếng Việt" mà không cần browser.
- Đếm entry I18N: `grep -c '"en":'` SAI với JSON minified 1 dòng (grep -c đếm DÒNG, file chỉ có 1 dòng JSON) → dùng Python `len(re.findall(r'"en":', html))` (phải = số key, en = zh).
- Check: title key có trong dict, `<div>` = `</div>`, link Drive đúng id.

## 4. Browser test (khi cần xác nhận visual/JS thật)

- Camofox CHẶN `file://` → serve HTTP: `python -m http.server <port> --bind 127.0.0.1` (terminal background=true) trong thư mục chứa file → `browser_navigate("http://127.0.0.1:<port>/detail/<file>.html?lang=vi")`.
- `POST /tabs/:id/evaluate` có thể 500 TRANSIENT (camofox flaky) → retry 1-2 lần là OK; snapshot fallback.
- Test vòng đủ VI→EN→ZH→VI bằng `.click()` qua browser_console + đọc `document.title`, `h1`, `.badge`, `.meta`, 1-2 cell bảng. Browser_console log capture không có trên camofox backend — dùng evaluate/expression.

## 5. Data 2 case đã làm (đối chiếu file gốc, dùng để rebuild/sửa)

### Greenfeed 300 lợn thịt — `reports/thucte__Greenfeed_300_lon_2025.docx`
- Trang trại nông hộ Nguyễn Ngọc Đông, Bắc Bình – Lập Thạch – Vĩnh Phúc; giám sát Phòng khám Thú Y Petme (Phố Me – Tam Dương); 06/01–18/05/2025 (131 ngày); Greenfeed, 300 con (ĐC 150 + TN 150), 6,8 kg/con; ghi chú "trang trại mới xây dựng, đợt nuôi đầu tiên".
- Thiết kế: ĐC = kháng sinh + vắc xin; TN = không kháng sinh, Kiềm EZ 80 **3kg/tấn TĂ** + vắc xin. TĂ Greenfeed thông thường.
- Bảng sinh trưởng (16 dòng): ban đầu 150/150; chết 4/2; còn lại 146/148; sống **97,33% / 98,67%**; đầu vào 6,80/6,80; xuất chuồng 120,00/120,13; tăng trọng 113,20/113,33; ADG 0,864/0,865; cám 9 bao 25kg/con; tổng cám 32.850/33.300 kg (tính theo con sống cuối kỳ); ADFI ≈1,72; FCR **1,99/1,99**; bệnh nhẹ 20%/12%; loại thải 2,67%/1,33%.
- Bảng sức khỏe: khỏi sau điều trị >90% / ~100%; ĐC "một số con tiêu chảy, viêm hô hấp" vs TN "ít triệu chứng, tiêu hóa tốt".
- Bảng kinh tế: cám 33.750 kg cả 2; EZ80 0 vs 101,25 kg = 0 vs 8.606.250 VND (85.000đ/kg, = 57.375đ/con); KS + thuốc bổ trợ 16.500.000 (110.000đ/con) vs 4.300.000 (28.667đ/con); vắc xin như nhau. **Tiết kiệm 23.958 VNĐ/con.**
- Kết luận: EZ80 hỗ trợ thay thế MỘT PHẦN kháng sinh (chưa hoàn toàn).
- Link Drive docnote: `1LsDWPLrMJTMiCwkc-qgzTmq8nY_oJ2-R` (cha giao dùng, kèm docnote cảnh báo trỏ nhầm; file ĐÚNG thực tế `1wtPF4XnkQ4bp25N5vWDRGl7w46KI_fDC`).

### Tuấn 8 con ASF — `reports/thucte__Bao_cao_thi_nghiem_Kiem_EZ80_tren_lon_ASF_docx.doc` (thực chất .docx)
- Trang trại Phạm Văn Anh Tuấn, Xóm Thái Bình, xã Đồng Thái, Ninh Bình; 29/09–05/10/2025; 8 lợn 25±2 kg; **8/8 dương tính ASF**.
- Phác đồ: Lô 1 ĐC (4 con) không điều trị, theo dõi tự nhiên; Lô 2 TN (4 con) Kiềm EZ 80 **5kg/tấn TĂ** + Kiềm DL **25ml/con/ngày** (qua nước uống).
- Theo dõi ngày: 29/09 giảm ăn 30% → 30/09 ĐC 3/4 sốt cao bỏ ăn, TN còn ăn nhẹ → 01/10 **ĐC 4/4 chết**, TN 1 chết 3 sống (75%) → 02/10 TN 2 yếu 1 ăn nhẹ → 03/10 TN chết thêm 2 → 04/10 con cuối yếu → 05/10 con cuối chết.
- Tổng hợp: sống đến ngày 3: 0 vs 3; sống đến ngày 7: 0 vs 0; tỷ lệ chết 100% cả 2; **thời gian sống TB 2,5 vs 5,5 ngày**.
- Kết luận: hỗ trợ kéo dài 2–3 ngày, không ngộ độc/tác dụng phụ, cần nghiên cứu đàn lớn hơn. Ngày lập 06/10/2025. Link Drive: `11940Ew-gqXj4FDAmeh9en7D0GxymP3iW`.
