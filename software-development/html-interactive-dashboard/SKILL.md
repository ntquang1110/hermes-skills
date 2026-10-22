---
name: html-interactive-dashboard
description: Build single-page HTML dashboards with tab navigation, localStorage persistence, JSON export/import, and progress tracking — for coaching, learning, habit tracking, or self-management tools.
platforms: [windows, macos, linux]
---

# HTML Interactive Dashboard

Build a self-contained, zero-dependency single-page HTML dashboard that serves as an interactive tool for coaching, learning programs, habit tracking, or personal management.

## When to use this

- User wants an interactive tool they open in a browser, fill out, and come back to
- Needs to persist data across sessions (localStorage)
- Needs to be portable (single HTML file, no server, no build step)
- Multiple sections/tabs that the user navigates between
- User wants to see progress over time
- **User wants the SAME single-file HTML in multiple languages (VI/EN/ZH) with a switcher button** — see `references/i18n-multilang-switch.md` for the full proven pattern (I18N dict injection, WeakMap original-text preservation, deep links `?lang=#case-xxx`, scan-PDF reality)

## Architecture

```
Single HTML file
  ├── CSS (embedded <style>, dark theme)
  ├── HTML structure (tabs, panels)
  └── JavaScript (embedded <script>)
        ├── Data model (JSON object with defaults)
        ├── Persistence (localStorage save/load)
        ├── Export/Import (JSON file download/upload)
        ├── Tab system (switchTab + render functions)
        ├── Each tab = render* function
        └── Stats bar (auto-updated)
```

## Requirements

- Single HTML file — no external dependencies (no React, no jQuery, no CDN)
- All JS in a single `<script>` block
- Dark theme CSS (matching Hermes visual style)
- Responsive layout (desktop + mobile)
- Auto-save on input (`input` event → `persist()`)
- Export/Import as JSON (for data portability + mentor review)
- Stats bar in header showing key counts

## Tab System Pattern

```javascript
const TABS = [
  { id:'canvas', icon:'📋', label:'Canvas' },
  { id:'journal', icon:'📓', label:'Nhật ký' },
  // ...
];

let currentTab = 'canvas';

function renderTabs() { /* render tab bar */ }
function switchTab(id) { currentTab=id; renderTabs(); renderContent(id); }
function renderContent(id) {
  const m = { canvas:renderCanvas, journal:renderJournal, ... };
  if (m[id]) m[id](el);
}
function renderAll() { renderTabs(); renderContent(currentTab); updateStats(); }
```

## Data Persistence Pattern

```javascript
function load() {
  const raw = localStorage.getItem('dashboard_key');
  if (raw) { try { return JSON.parse(raw); } catch(e) {} }
  return JSON.parse(JSON.stringify(DEFAULT_DATA));
}
function persist() {
  localStorage.setItem('dashboard_key', JSON.stringify(data));
  updateStats();
}
function exportAll() {
  // download as JSON file
  const blob = new Blob([JSON.stringify(data,null,2)], {type:'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `data-${new Date().toISOString().slice(0,10)}.json`;
  a.click();
}
function importData(str) {
  try { data = JSON.parse(str); persist(); renderAll(); }
  catch(e) { /* error handling */ }
}
```

## Default Data Pattern

Use `DEFAULT_DATA` as a seed with pre-filled example values so the user sees a non-empty page on first load. The `load()` function should fall back to `JSON.parse(JSON.stringify(DEFAULT_DATA))`.

**⚠️ Migration:** When loading old localStorage data, merge non-empty fields rather than overwriting, so pre-filled defaults aren't lost:

```javascript
if (o.canvas) {
  for (let k of Object.keys(o.canvas)) {
    if (o.canvas[k] && o.canvas[k].trim()) d.canvas[k] = o.canvas[k];
  }
}
```

## Link & Button Patterns

### DO NOT use `<a href="javascript:...">` for in-page navigation
This breaks in modern browsers. Instead:

**For external links (open in new tab):**
```html
<a href="https://..." target="_blank" rel="noopener" class="btn">📊 Open →</a>
```

**For in-page tab switching — PREFERRED: `<button>` + `data-*` + `addEventListener`**

The safest pattern avoids inline `onclick` entirely because `\"` inside backtick template literals produces literal `\` + `"` (two chars), not a quote:

```javascript
// RENDER: emit a <button> with a data attribute
`<button data-tab="${s.tabId}" class="btn">${label} →</button>`
```

```javascript
// AFTER RENDER: attach listeners programmatically
el.querySelectorAll('[data-tab]').forEach(btn => {
  btn.addEventListener('click', function() {
    switchTab(this.getAttribute('data-tab'));
  });
});
```

**AVOID — inline onclick in template literals** (fragile quoting):
```html
<!-- BAD -- \" inside backtick becomes literal backslash+quote -->
<a onclick="switchTab('${id}')" class="btn">Go →</a>
```

## Progress/Stats Pattern

Show a compact stats bar in the header with key counts (entries, completions, streak). Update it in `persist()` and `updateStats()`:

```javascript
function updateStats() {
  document.getElementById('statJournal').textContent = data.journal.length;
  document.getElementById('statActions').textContent = `${done}/${total}`;
}
```

For daily streak tracking:
```javascript
const allDays = Object.keys(dayLog).sort().reverse();
let streak = 0;
for (let i = 0; i < allDays.length; i++) {
  const steps = Object.values(dayLog[allDays[i]]).filter(Boolean).length;
  if (steps === totalSteps) streak++; else break;
}
```

## Sticky Tabs + Reload Persistence Pattern

User expectation (TFO dashboard): tab bar stays visible when scrolling, and reload/F5 returns to the SAME tab they were viewing. Both are cheap and expected — add them by default.

**Sticky tab bar under a sticky header:** header is `position:sticky; top:0; z-index:100`; the tab bar also needs `position:sticky` but its `top` must equal the header's real height, or it hides UNDER the header. Measure it in JS (don't hardcode px — padding/font changes break it):

⚠️ **Nếu header KHÔNG sticky thì `top` của thanh tab phải là `0`.** Gán `top = header.offsetHeight` khi header trôi bình thường là bug thật (gặp 08/10/2026 trên trang tăng vốn Manna Đất Vàng): thanh tab bị đẩy xuống thấp hơn đầu viewport mỗi lần cuộn, tạo khoảng trống phía trên mà nội dung vẫn lướt qua. Verify bằng `getComputedStyle(tabbar).top === '0px'` và `getBoundingClientRect().top === 0` sau `scrollTo(0, document.body.scrollHeight)`.

```css
.tab-bar { position: sticky; top: 0; z-index: 95; background: var(--black); }
```
```javascript
(function stickyTabs() {
  const header = document.querySelector('.header');
  const tabbar = document.querySelector('.tab-bar');
  if (header && tabbar) {
    const setTop = () => { tabbar.style.top = header.offsetHeight + 'px'; };
    setTop();
    window.addEventListener('resize', setTop);
  }
})();
```

**Reload-persist active tab:** write to localStorage inside `switchTab`, restore in `init()`:

```javascript
function switchTab(tab) {
  // ...toggle views + .active classes...
  try { localStorage.setItem('tfo_tab', tab); } catch (e) {}
}
function init() {
  // ...load data...
  try {
    const saved = localStorage.getItem('tfo_tab');
    if (saved && ['dashboard','calendar','projects','kanban','agent','system'].includes(saved)) switchTab(saved);
  } catch (e) {}
}
```

## Gist Deployment

After building the HTML:

1. Save to a file under the project directory
2. Upload to GitHub Gist (private) using the `upload-online-link` skill
3. Preview via `https://htmlpreview.github.io/?{raw_url}`
4. Optionally create a Notion page with the preview link

**⚠️ Gist PATCH trả 404 — gist đã chết:** khi update gist cũ mà `PATCH /gists/<id>` nhận 404, gist đã bị xoá hoặc không thuộc account hiện tại (hay gặp khi ID ghi trong state file đã lâu). Không đoán ID: `GET https://api.github.com/gists?per_page=100` list toàn bộ để tìm, không thấy → tạo gist mới và BÁO RÕ user "link preview đổi". Verify sau khi tạo: `curl -s https://preview.thefirstonly.com/<gist_id> | grep -o '<chuỗi đặc trưng>'` để chắc worker trả đúng HTML, không bị route về KFlow tunnel.

## Computed aggregates PHẢI guard trường hợp thiếu dữ liệu (NaN)

Bất kỳ chỉ số nào tính từ dữ liệu người dùng nhập (trung bình, chênh lệch,
phần trăm hoàn thành) đều có thể gặp mẫu số = 0 khi dữ liệu CHƯA đủ. Chia cho 0
ra `NaN`, và `NaN` lan ra toàn bộ UI thành `"— NaN điểm · cơ sở NaN"`.

Đo thật (bảng chấm articulation, 4 checkpoint × 5 chỉ số): khi chỉ chấm vài chỉ
số rời rạc, vòng lặp `if (!bv || !lv) return;` bỏ qua hết các cặp chưa đủ → `n = 0`
→ `bSum/n` = NaN.

**Luật: đếm số cặp hợp lệ TRƯỚC, rồi mới chia; `n === 0` thì render thông báo rõ,
không render số.**

```javascript
let bSum = 0, lSum = 0, n = 0;
METRICS.forEach(([mk]) => {
  const bv = base[mk] || 0, lv = last[mk] || 0;
  if (!bv || !lv) return;        // cặp chưa đủ → bỏ qua
  bSum += bv; lSum += lv; n++;
});
if (!n) {                        // ← BẮT BUỘC
  el.innerHTML = '<p class="hint">Cần chấm đủ cả 5 chỉ số ở mốc gốc và mốc này mới so sánh được.</p>';
  return;
}
const avg = bSum / n;
```

Chốt bằng probe: chấm 3/5 chỉ số ở một checkpoint → assert UI **không chứa chuỗi
`NaN`**. Đây là bài test rẻ nhất bắt được lớp lỗi này.

## Ba lỗi wiring chỉ lộ khi LÁI DOM, không lộ khi nhìn code

Cùng một file articulation, ba bug sống sót qua "đọc code thấy đúng" và chỉ hiện
khi drive DOM bằng console:

1. **Trạng thái do người dùng bật bị gate sau cờ runtime không liên quan.** Class
   `done` của từng bước được set bên trong `if (running)`, nên bấm vào bước khi
   timer CHƯA chạy → không có phản hồi thị giác nào. Tách 2 nguồn trạng thái ra:
   ```javascript
   // user-marked (marks) và timer-derived (idx) là HAI nguồn riêng, đừng gate chung
   li.classList.toggle('done', marks.has(i) || (running && i < idx));
   ```
2. **`render()` chỉ được gọi trong `setInterval`.** Nhãn phase không đổi cho tới
   tick 1 giây sau khi bấm Bắt đầu. Gọi `render()` NGAY trong hàm `start()` —
   đừng để UI phụ thuộc vào nhịp interval.
3. **Toggle-off trả giá trị 0 chứ không xoá key.** Bấm lại đúng ô điểm đang chọn →
   set về `0` (bỏ chọn). Hợp lý về UX nhưng chính là nguồn sinh `n = 0` ở mục trên
   → hai thứ phải sửa cùng nhau.

**Probe tối thiểu trước khi publish — lái từng chuyển trạng thái và assert giá trị:**
trạng thái rỗng (guard có hiện không), chấm một phần, chấm đủ, toggle off, reset,
đổi tab. Assert vào giá trị DOM/localStorage chứ không assert "không có lỗi console"
— cả ba bug trên đều im lặng, console sạch.

## Biến thể CATALOGUE: trình bày danh mục lớn (inventory) thay vì form nhập liệu

Cùng hạ tầng tab + search + filter, nhưng dữ liệu là một DANH SÁCH lớn sinh ra
từ Python (danh mục skill, tài liệu, sản phẩm, hồ sơ) thay vì người dùng nhập.
Dùng khi danh mục quá dài để gửi trong chat và user cần tự chọn/lọc.

Bố cục đã dùng (189 skill): 3 tab **Đã cài / Nên viết thêm / Bỏ qua**, chip lọc
theo nhóm chuyên môn, ô search, mỗi card 1 nút chọn.

### ⚠️ Đừng sinh HTML bằng f-string Python

JS trong `<script>` đầy `{}` → `f"...{...}"` nổ `SyntaxError` hoặc ăn mất dấu
ngoặc. Đây là lỗi build-time, khác hẳn các pitfall quoting runtime ở trên.
Dùng template + `.replace()` với placeholder `__X__`:

```python
TPL = open("tpl.html", encoding="utf-8").read()      # HTML+JS tĩnh, 0 dấu {}
out = (TPL.replace("__DATA__", json.dumps(rows, ensure_ascii=False))  # JSON vào JS
          .replace("__N_TOTAL__", str(len(rows))))
open("out.html", "w", encoding="utf-8").write(out)
```

`__X__` an toàn hơn `{X}` (không đụng cú pháp JS) và `json.dumps(..., ensure_ascii=False)`
giữ nguyên tiếng Việt có dấu trong dữ liệu nhúng.

**`str.format()` hỏng y hệt — và đừng "sửa" bằng cách nhân đôi ngoặc.** Template dài
viết bằng `.format(css=..., data=...)` nổ `ValueError: unexpected '{' in field name`
ngay tại dòng đầu tiên có `${...}` hoặc `{` không nhân đôi. Cách chữa SAI (đã thử,
đừng lặp lại): nhân đôi mọi `{{` `}}` rồi `re.sub` trả về ngoặc đơn — regex không
phân biệt được `{{` của Python với `}}` của JS lồng nhau, phá code mà không báo lỗi.
Chữa đúng: **bỏ hẳn `.format()`, `.replace()` cho MỌI biến, kể cả CSS**:

```python
html = TPL
for k, v in [("@@CSS@@", css), ("@@DATA@@", json.dumps(rows, ensure_ascii=False)),
             ("@@N_TOTAL@@", str(len(rows)))]:
    html = html.replace(k, v)
```

`@@X@@` nhỉnh hơn `__X__` một chút: không đụng `__init__`/`__name__` trong JS/HTML.
Kiểm tra còn placeholder sót: `re.findall(r"@@[A-Z_]+@@", html)` phải rỗng.

### Test bộ dựng mà KHÔNG đụng repo (và khi subagent đang ghi cùng thư mục)

Script dựng thường tính `ROOT` từ `__file__`. Muốn test an toàn: **copy script + mọi
file nó phụ thuộc + dữ liệu giả vào một thư mục tạm giữ nguyên cấu trúc**, chạy ở đó,
rồi xoá. Repo không bị chạm nên không đụng độ với subagent đang ghi file song song:

```python
T = os.path.expandvars(r"%LOCALAPPDATA%/Temp/mt-test")     # không dùng /tmp trên Windows
shutil.copy("visual/build.py",  T + "/visual/build.py")    # ROOT tự trỏ về T
shutil.copy("visual/base.html", T + "/visual/base.html")   # file nó đọc để lấy CSS
os.makedirs(T + "/docs/09-...", exist_ok=True)
open(T + "/docs/09-.../batch-a.json", "w", encoding="utf-8").write(json.dumps(fake, ensure_ascii=False))
subprocess.run(["python", "visual/build.py"], cwd=T, capture_output=True, text=True, encoding="utf-8")
```

Dữ liệu giả phải phủ **cả ô trống** (một bản ghi chỉ có 2/8 trường) — đó là cách bắt
lỗi render trước khi có dữ liệu thật, và là cách duy nhất test được lúc 3 subagent còn
đang ghi.

### Xem trang vừa dựng: phục vụ qua HTTP, đừng mở file trực tiếp

`browser_navigate` tới `file:///C:/...` không đáng tin. Cách chạy được:
`python -m http.server 8899 --bind 127.0.0.1` (background) trong thư mục tạm, rồi
navigate `http://127.0.0.1:8899/visual/out.html`. Xong thì `process(action="kill")` +
`shutil.rmtree`. Đây cũng là đường duy nhất để `browser_console` soi DOM thật — đo
được số card, số dòng/bản ghi, trạng thái sau khi bấm nút lọc và gõ ô search.

### Renderer theo dữ liệu: ĐỪNG ẩn ô trống

Khi render N mục cố định từ dữ liệu (N chặng, N bước, N chỉ số), bỏ qua mục không có
dữ liệu làm **mục đó biến mất khỏi trang** — user tưởng khung chỉ có 7 phần trong khi
spec là 8. Luôn render đủ N; ô trống ghi rõ lý do (`chưa có nguồn (tag H)`) và làm mờ
(`.miss-row{opacity:.55}`). Trạng thái trống là thông tin, không phải chỗ để giấu.
Cùng họ với luật "số không nguồn = không số".

**Test nút lọc/search bằng cách LÁI nó, không đọc code** — inject một truy vấn rồi
assert kết quả:

```js
(() => { const q=document.getElementById('q'); q.value='cyp1a2';
  q.dispatchEvent(new Event('input'));
  const hit=[...document.querySelectorAll('#list .sitem')].map(e=>e.querySelector('.sname').textContent);
  document.querySelectorAll('.fbtn')[0].click();          // reset
  return JSON.stringify({hit, so_dong: document.querySelector('#list .sitem').querySelectorAll('.r').length});
})()
```

Đây là probe rẻ nhất bắt được: nhãn lộ khoá thô (`chi_tiet` in ra mặt vì thiếu map
nhãn), mục rỗng bị ẩn, nút lọc không reset.

### ⚠️ Search tiếng Việt trên nội dung tiếng Anh phải map từ khoá + word-boundary

Nếu desc là tiếng Anh ("Contracts, clauses, MSAs") thì gõ "hợp đồng" ra **0 kết
quả** — search chạy không lỗi nhưng vô dụng. Thêm map VN→EN, match cả tên + desc
+ nhóm:

```python
VN_KEYWORDS = {"hợp đồng": "contract clause agreement", "lao động": "employment labour", ...}
```

Và **match phải word-boundary, KHÔNG substring**. Bản dùng `tok in blob` khiến
`"tax"` khớp `taxonomy` và `"ip"` khớp mọi từ chứa "ip" → truy vấn "thuế" trả
41 kết quả rác (lẫn cả `dpia-documenter`):

```python
for tok in en.split():
    if len(tok) < 4:            # chặn token ngắn gây nhiễu
        continue
    if re.search(r"\b" + re.escape(tok) + r"\b", blob):
        hits.append(vi); break
```

41 rác → 38 hợp lý. **Luôn in số kết quả của vài truy vấn mẫu rồi soi tay**;
search im lặng ≠ search đúng.

### ⚠️ Assert bất biến phân hoạch

Khi chia danh mục thành các tab loại-trừ-nhau, tổng các phần PHẢI bằng tổng gốc
— nếu không là có mục rơi mất hoặc bị đếm 2 lần, và user sẽ không bao giờ biết:

```python
assert len(ready) + len(want) + len(skip) == total, (len(ready), len(want), len(skip), total)
```

### Verify bản catalogue trước khi publish

Đếm bằng DOM thật, đừng tin mắt: số card mỗi tab = số dữ liệu, số chip, search
ra kết quả đúng cho vài truy vấn VN, và `scrollWidth > innerWidth` = false.
Đổi tab rồi đếm lại — bug hay nằm ở tab thứ 2/3 chứ không phải tab đầu.

## Common Pitfalls

- **Nested tab selector bên trong tab panel — phải dùng class + handler RIÊNG:** khi thêm bộ chọn thứ 2 (vd switcher sản phẩm EZ80/EZ67) nằm TRONG một tab panel, KHÔNG được dùng lại class `.tab-btn`/`.panel` và cùng vòng `forEach` — outer tabs và inner tabs sẽ đánh nhau (click 1 cái toggle cả 2). Pattern chuẩn (đã dùng OK trên hồ sơ sản phẩm Kiềm Saphia): prefix class riêng `.prod-btn`/`.prod-panel`/`.prod-switch`, `data-prod` thay vì `data-tab`, và 1 khối JS riêng `const prodBtns = document.querySelectorAll('.prod-btn')` với listener độc lập. Verify bằng browser_console: click button → check `classList.contains('active')` của cả 2 panel + trạng thái button, đảm bảo cái này bật cái kia tắt đúng.
- **⚠️ CSS class-order kills `.hidden` on overlay/modals:** if `.hidden { display:none }` is declared BEFORE a component class that sets `display:flex` (e.g. `.overlay`), the later declaration WINS at equal specificity — adding/removing the `hidden` class does NOTHING and the popup never hides. Fix: `.hidden { display:none !important; }`. When verifying show/hide logic, check **computed style** (`getComputedStyle(el).display`), not just `classList.contains` — classList reflects intent, not rendered state. (Observed on dictation.html: "bấm Xem lại popup không hạ" — root cause was `.hidden` declared before `.overlay`.)
- **⚠️ Browser mic (`getUserMedia`) requires HTTPS (secure context):** a page served over plain `http://192.168.x.x` loads fine but `navigator.mediaDevices` is `undefined` → `Cannot read properties of undefined (reading 'getUserMedia')`. This is NOT a code bug — the browser blocks mic on insecure origins. For phone testing, the page MUST be HTTPS: Cloudflare tunnel subdomain, loca.lt, or localhost (localhost is exempt). LAN IP HTTP is only for non-mic dev.
- **⚠️ V8 date parsing của chuỗi mốc thời gian (deadline text):** `new Date('Thứ 7')` → **Jul 01 2001**, `new Date('Tuần 1')` → **Jan 01 2001**. V8 nhặt số trong chuỗi làm month — KHÔNG bao giờ fallback `new Date(s)` cho deadline kiểu text tiếng Việt ("Thứ 7", "Tuần X", "cuối tuần"). Hậu quả thực tế: dashboard đếm toàn bộ task có deadline text là "quá hạn". Fix: chỉ parse bằng regex NGÀY CỤ THỂ, mọi thứ khác → `null` (mốc tương đối, không tính quá hạn):
  ```javascript
  const parseDate = d => {
    if (!d) return null;
    const s = String(d).trim();
    let m;
    if ((m = s.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/))) {   // dd/mm/yyyy
      const dt = new Date(+m[3], +m[2]-1, +m[1]);
      return isNaN(dt) ? null : dt;
    }
    if ((m = s.match(/^(\d{4})-(\d{2})-(\d{2})(?:[ T].*)?$/))) { // yyyy-mm-dd[ HH:MM]
      const dt = new Date(+m[1], +m[2]-1, +m[3]);
      return isNaN(dt) ? null : dt;
    }
    return null; // "Thứ 7", "Tuần 1", text khác → không phải ngày cụ thể
  };
  ```
  Lưu ý: `05/08/2026` trong `new Date('05/08/2026')` bị hiểu là May 8 (US format) — dùng `new Date(y, m-1, d)` thay vì chuỗi để tránh.
- **line-number prefix corruption:** `read_file` prepends "1|", "2|"... to content. When re-uploading HTML, use `terminal("cat path")` to get raw content, NOT `read_file`.
- **`javascript:` links:** Don't use `href="javascript:..."` — they can break with escaped quotes. Use `onclick` with `cursor:pointer` instead.
- **⚠️ Xung đột tên hàm popup trong app ĐÃ có modal (gặp 15/08 trên TFO):** khi thêm popup/list mới vào dashboard đã tồn tại `openTaskModal(taskId)` / `closeTaskModal()` (edit task) — hàm trùng tên ghi đè im lặng (silent override), nút mới gọi nhầm hàm cũ → popup không mở, KHÔNG có lỗi console. TRƯỚC khi đặt tên popup: `grep -n "function open\|function close" index.html`; dùng prefix riêng (`openTaskListModal`/`closeTaskListModal`). Verify sau khi build: gọi hàm mới → check `classList.contains('open')` + `getComputedStyle(overlay).display`.
- **⚠️ Hàm render item dùng chung board + popup PHẢI global:** nếu `taskItemHtml(t)` khai báo bên trong `render()` (closure) thì popup (global scope) gọi → ReferenceError. Đặt ở top-level script, cả 2 nơi dùng chung.
- **⚠️ "Xem thêm" + popup infinite scroll (pattern đã dùng 15/08 trên TFO + AI Company):** render `list.slice(0, 10)` + nút "Xem thêm N task →" nếu còn ẩn; popup bottom-sheet (`position:fixed; inset:0; align-items:flex-end`) chứa list `overflow-y:auto; -webkit-overflow-scrolling:touch`, batch 30 (`scrollTop+clientHeight >= scrollHeight-120` → load thêm). Đóng bằng ✕ hoặc click overlay (`onclick="if(event.target===this)closeX()"`). Test bằng cách inject 120 phần tử giả → verify đếm tăng 30→60→120.
- **⚠️ Mobile overflow: dùng iframe 360–390px để phát hiện tràn ngang, nhưng ĐO BẰNG MÉP PHẢI PHẦN TỬ — `scrollWidth` báo SAI trong iframe.** Inject `<iframe width=360 height=2400 src=...>` (đặt `position:fixed;left:-9999px`) rồi ở lượt gọi sau đo `contentDocument`. Nguyên nhân thường gặp: (a) header/thanh tab không wrap — thêm `flex-wrap:wrap` + ẩn phần tử phụ (`display:none`) trong `@media (max-width:600px)`; (b) flex child có ellipsis thiếu `min-width:0` → text dài đẩy container; (c) grid `1fr` = `minmax(auto,1fr)` không co được → dùng `minmax(0,1fr)`; (d) thêm `body { overflow-x:hidden }` như chặn cuối, fix gốc vẫn phải làm.
  **Bẫy min-content: MỘT token dài làm CẢ CỘT phình, và mọi thẻ cùng grid phình theo.** `repeat(auto-fill,minmax(320px,1fr))` khi khung chỉ còn 320px: `auto` = **min-content**, nên một từ không ngắt được (hoặc `white-space:nowrap` sót lại) kéo cột lên 341–388px — nhìn tưởng "thẻ này lỗi", thực ra cả grid sai. Vá đúng: `grid-template-columns:repeat(auto-fill,minmax(min(320px,100%),1fr))` **cộng** `.card{min-width:0;overflow-wrap:anywhere}` **cộng** `.card *{min-width:0;overflow-wrap:anywhere}` (con cháu cũng phải sửa, `dt`/`dd` giữ `nowrap` là vẫn tràn).
  **Phép đo đúng:** `document.querySelectorAll('body *')` lọc `getBoundingClientRect().right > width+1` → **0 mới là đạt**, và đếm chữ `< 12px` → **0**. ĐỪNG dùng `documentElement.scrollWidth > clientWidth` trong iframe đo: thực đo được `sw=402 / cw=360` trong khi `max(right) = 360` — không phần tử nào tràn, con số 402 là ảo giác của Gecko với trang nằm trong iframe ẩn. Đo sai thì đi tìm một lỗi không tồn tại. Trên trang THẬT ở desktop thì `scrollWidth == clientWidth` mới là phép kiểm đúng.
  Nit mỹ thuật hay bị bỏ: highlight `<h1>em{background:var(--yellow)}` cần `padding:.04em .2em` + `border-radius` + `box-decoration-break:clone`, nếu không nền vàng dính sát chữ đứng trước. `browser_vision` bắt được nit này nhưng **mọi con số phải đo bằng `browser_console`** (vision đọc sai dấu tiếng Việt và từng báo typo không tồn tại).
- **Template-literal quoting:** Inside backtick strings (`` ` ``), escaped double-quotes can misbehave. Avoid inline `onclick` in generated HTML — use `data-*` attributes + `addEventListener` instead.
- **Sibling-subagent file collisions on shared HTML:** when multiple agents edit the same `index.html` concurrently (e.g. AI-company team workflow), patches silently land on stale reads → duplicate `id` attributes, duplicated tab buttons, orphaned view containers, unbalanced `<div>`. After ANY batch of patches to a shared HTML file, run a structural check before restarting the server:
  ```python
  import re
  html = open('app/static/index.html', encoding='utf-8').read()
  ids = re.findall(r'id="([^"]+)"', html)
  dups = [i for i in set(ids) if ids.count(i) > 1]
  print('ID dup:', dups if dups else 'None')
  print('div balance:', html.count('<div'), '/', html.count('</div>'))
  # + JS syntax: extract <script> blocks → node --check
  ```
  If duplicates found: delete the redundant copy (keep the newest/richest), re-verify, then restart. Also re-read the file with `read_file` before the NEXT patch (the `_warning: modified by sibling subagent` in patch output is the signal).
- **Nested template literals for onclick args:** when emitting `onclick="openTaskChat(${id}, '${esc(title)}', '...', 'ai')"` from inside another backtick template, keep the inner strings `esc()`-escaped AND prefer `event.stopPropagation()` on nested buttons so card-level `onclick` doesn't fire too. `stopPropagation` is a JS event method — it will show as a "missing def" in naive grep checks; that's expected, not an error.
- **Token expiry format:** Google OAuth tokens may store `expiry` as a Unix timestamp string (e.g. `1784275931`) instead of ISO format. Fix with: `float(exp)` → `datetime.fromtimestamp(exp, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')`.
- **Overwriting pre-filled data:** When merging old localStorage data into a new DEFAULT_DATA seed, merge field-by-field with empty-check, don't replace the whole object.
- **Large HTML files:** Single-file dashboards can reach 60K+ chars. Use Python to generate the Gist JSON payload (`json.dump` to temp file), then `curl -d @file` to avoid shell escaping issues.
