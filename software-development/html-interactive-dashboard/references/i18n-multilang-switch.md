# I18N Multi-Language Switch (VI/EN/ZH) cho Single-File HTML

Pattern đã verify trên hồ sơ sản phẩm Kiềm Saphia (11/08/2026, gist 3d581a3444296042579d49722d4d85fe, 3 ngôn ngữ 294+ text nodes, không dùng framework). Đáp ứng yêu cầu "1 file, nút chuyển ngôn ngữ, dịch toàn bộ".

## Cấu trúc

```
1 file HTML
  ├── topbar: nút VI / EN / 中 (.lang-btn[data-lang])
  ├── body: text nodes TIẾNG VIỆT GỐC (mặc định)
  └── <script> cuối: const I18N = {"vi text": {en: "...", zh: "..."}} + applyLang()
```

File scripts tham chiếu: `D:/Hermes Proj/kiem-saphia/scripts/` — `extract_texts.py` (html.parser → danh sách text node unique), `merge_i18n.py`, `build_workbench.py`, `gen_i18n_js.py`, `inject_i18n.py` (chèn dict + logic vào HTML trước </body>). Workbench md: `i18n-workbench.md` (key | vi | en | zh).

## Quy trình 6 bước

1. **Extract text nodes**: dùng `html.parser` handle_data (KHÔNG dùng regex `<(tag)>(.*?)</tag>` — regex lồng nhau gộp cả parent+child thành 1 blob). Bỏ qua script/style/svg. Dedupe giữ thứ tự → `i18n-texts.json`.
2. **Dịch dict**: vi → (en, zh giản thể). Giữ số liệu, đơn vị, tên riêng (EZ80, VNUA, DABACO, Kiềm EZ, Vua Kiềm). Dịch toàn bộ, không bỏ sót.
3. **Merge + verify**: đối chiếu dict vs text nodes — phải 0 missing (294/294). Thêm text node mới (vd nhãn "Tài liệu gốc (VI) ↗") → chạy lại extract trước.
4. **Inject JS**: chèn `<script>` trước `</body>` chứa `const I18N = {...}` + `applyLang()`. Sau mỗi lần inject → PATCH gist.
5. **Verify browser 3 ngôn ngữ**: h1, tabs, bảng, sub-tabs, footer, title đổi đúng; chuyển qua lại en→vi→zh→vi→en; localStorage nhớ.
6. **Workbench md** cho agent khác review bản dịch: `build_workbench.py` sinh bảng 3 cột.

## ⚠️ BUG CRITICAL: mất key gốc sau khi đổi ngôn ngữ

Sau lần `applyLang('en')` đầu, text nodes ĐÃ bị thay bằng tiếng Anh → lần `applyLang('vi')` sau không match key tiếng Việt nữa (dict key = text VI gốc). Fix: lưu bản gốc vào **WeakMap** khi quét lần đầu, luôn đọc từ bản gốc:

```javascript
const ORIG = new WeakMap();
// trong applyLang:
let raw = ORIG.get(n);
if (raw === undefined) { raw = n.nodeValue; ORIG.set(n, raw); }
const key = raw.trim();
if (!key || !I18N[key]) return;
const m = raw.match(/^(\s*)([\s\S]*?)(\s*)$/);
n.nodeValue = (m ? m[1] : '') + (lang === 'vi' ? key : (I18N[key][lang] || key)) + (m ? m[3] : '');
```

## Title ngoài body

`<title>` không nằm trong body nên TreeWalker không đụng tới. Lưu `ORIG_TITLE = document.title` lúc khởi tạo, đổi trong applyLang:

```javascript
const tKey = ORIG_TITLE.trim();
if (I18N[tKey]) document.title = lang === 'vi' ? ORIG_TITLE : (I18N[tKey][lang] || ORIG_TITLE);
```

## LocalStorage + URL param

- `localStorage['ks_lang']` nhớ ngôn ngữ, khôi phục khi reload.
- URL `?lang=en#case-xxx` — đọc `URLSearchParams(location.search).get('lang')` TRƯỚC localStorage (param thắng), validate chỉ nhận vi/en/zh.

## Deep link tới từng case (click link mở đúng case + đúng ngôn ngữ)

Yêu cầu Quang: "phần chữ đậm trỏ bản xem theo ngôn ngữ, phần original giữ drive gốc". Mỗi case 2 link:

```html
<tr id="case-lab-2">
  <td class="lead">
    <a class="case-link" data-case="lab-2" href="https://preview.thefirstonly.com/<gist>#case-lab-2" target="_blank">Tên case ↗</a>
    <a class="doc-orig" href="https://drive.google.com/file/d/<id>/view" target="_blank">Tài liệu gốc (VI) ↗</a>
  </td>
</tr>
```

- Click `.case-link` → JS rewrite href: base + `?lang=<lang hiện tại>#case-xxx` trước khi mở (mở bản xem đúng ngôn ngữ, nhảy đúng case).
- On load với hash `#case-xxx`: click tab Khảo nghiệm (`.tab-btn[data-tab="tab4"]`) + sub-tab đúng (prefix `lab` → lab, ngược lại field) + `scrollIntoView({block:'center'})` + highlight nền vàng 2.6s.
- Nhãn `.doc-orig` cũng nằm trong dict i18n (dịch "Tài liệu gốc (VI)" / "Original doc (VI)" / "原始文件（VI）") — nhớ thêm cả mũi tên "↗" vào key nếu nó nằm trong text node.

## Scan PDF — không dịch tự động được

Scan PDF = ảnh, không có text layer. Không hứa "bản dịch tự động". PA2 (đã chốt): giữ link drive scan gốc làm bằng chứng, gắn nhãn "(VI)" tự dịch theo ngôn ngữ, nội dung chính đã dịch sẵn trên trang. Không tạo file dịch từ scan (mất giá trị chứng cứ, tốn 1-2 ngày OCR+dịch 16 file).

## Verify cache khi PATCH gist

Sau PATCH gist, `preview.thefirstonly.com` có thể trả bản CŨ do cache:
- Gist raw CDN: `Cache-Control: max-age=300` (5 phút) — verify bằng `?cb=<số>`.
- Preview worker: `max-age=3600` (1 giờ) — verify bằng `?bust=<số>`, nếu vẫn cũ thì đợi TTL; browser Camofox cũng cache session → `curl -X DELETE http://localhost:9377/sessions/hermes` rồi navigate lại.
- Quy tắc: verify GIST RAW trước (đúng = code OK), preview chỉ chậm cache, không phải lỗi code.
