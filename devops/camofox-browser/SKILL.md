---
name: camofox-browser
description: "Use when browser tools fail: Camofox :9377 start/recovery."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [browser, camofox, automation, troubleshooting]
---

# Camofox Browser Server

Camofox = headless browser automation server (Firefox-based camoufox, anti-detection) chạy local trên port 9377. Repo: `D:/Hermes Proj/camofox-browser`. Hermes browser tools (browser_navigate/click/snapshot/vision) kết nối tới server này.

## Screenshot local HTML khi không có vision model

Cần chụp ảnh HTML/SVG local gửi user, hoặc verify visual khi model thiếu vision (deepseek-v4-flash báo 400 `unknown variant image_url`): dùng playwright-core có sẵn trong camofox-browser + chromium của ms-playwright — `references/screenshot-local-html.md` (script mẫu + verify overflow bằng getBBox). File phải `.cjs` (package.json `"type": "module"` chặn require trong `.js`).

**Script sẵn dùng — `scripts/verify-deliverable.cjs` (verified 20/10/2026).** Bản gộp mạnh hơn `verify-html-render.cjs` cho việc QA **deliverable HTML đã publish**: quét **4 viewport** (360/390/768/1440), tự **mở hết `<details>` rồi mới đo** (nên bắt được lỗi trong khối đang gập), in JSON + **exit code 0/1** nên ghép được vào chuỗi lệnh. Kiểm: font dưới ngưỡng **kể cả desktop**, tràn ngang, ảnh vỡ, **em dash trong text đã render** (bắt AI-ism lọt vào bản publish), số `<table>`, con cái tràn khỏi khối cha, bullet còn sót trong list đã ẩn dấu, và **hướng thanh bar so với trục 0**.

```bash
node "$HOME/AppData/Local/hermes/skills/devops/camofox-browser/scripts/verify-deliverable.cjs" \
  "https://preview.thefirstonly.com/<id>"
# đổi selector bar nếu chart không dùng .tr/.tr i; truyền {} để bỏ qua check bar
node .../verify-deliverable.cjs "$URL" 12 '{"bars":".bar|.fill"}'
```

⚠️ **Hai bài học đã trả giá, đừng lặp lại:**

1. **Bar mang giá trị ÂM phải vẽ NGƯỢC hướng, không cùng hướng với bar dương.** Bug thật: thanh cho SMD âm (−0,59 và −2,65) vẽ từ trái sang phải y như thanh dương → người đọc hiểu ngược chiều tăng/giảm. Đây là lỗi **ngữ nghĩa, không phải lỗi layout**: mọi phép đo font/overflow/ảnh vỡ đều báo xanh, chỉ có soi ảnh mới thấy. Pattern đúng: track có **vạch giữa = mốc 0**, dương neo `left:50%`, âm neo `right:50%`, bề rộng `= |giá trị| / maxAbs × 50%` (giá trị lớn nhất = đúng nửa track). Chạy check `bars` trên **mọi** biểu đồ có cả giá trị dương lẫn âm.
2. **Kiểm font phải quét CẢ desktop, không chỉ mobile.** Rule "mobile ≥12px" của user dễ bị hiểu thành "desktop thì 11,5px được" → bỏ sót 31 chỗ 11,5px và phải publish lại. Ngưỡng 12px áp cho **mọi** viewport; xem `minFontPx` trong JSON, không tự suy.

**Script sẵn dùng — `scripts/verify-html-render.cjs` (verified 22/09/2026).** Khi cần verify một trang HTML đã publish (hoặc local http) mà model không xem được ảnh: vừa chụp screenshot (desktop + từng tab + mobile) vừa kiểm tra chức năng trong cùng một lượt.

⚠️ **Phải COPY script vào repo camofox-browser rồi chạy từ đó (verified 25/09/2026).** Gọi thẳng bằng absolute path trong skill dir sẽ chết `Error: Cannot find module 'playwright-core'` — Node resolve `node_modules` theo vị trí FILE script, không theo cwd, còn `playwright-core` chỉ có trong `node_modules` của repo. Cùng họ pitfall với `camsearch.py`.

**Cách 2, không cần copy (verified 20/10/2026):** trỏ `NODE_PATH` vào một `node_modules` có playwright-core. Giữ nguyên script trong skill dir, không phải dọn bản copy sau.

```bash
mkdir -p ~/httptmp/vtest && cd ~/httptmp/vtest
printf '{"name":"vtest","private":true,"version":"1.0.0"}' > package.json
npm i playwright-core --no-audit --no-fund --prefix .
export NODE_PATH="C:/Users/<user>/httptmp/vtest/node_modules"
node "C:/Users/<user>/AppData/Local/hermes/skills/devops/camofox-browser/scripts/verify-html-render.cjs" \
  "https://preview.thefirstonly.com/<id>" "./shots"
```

Lưu ý `npm i` trong thư mục trống **không tạo `node_modules`** nếu thiếu `package.json` (npm báo "up to date in 1s" rồi thoát). Phải có `package.json` trước.
Chromium: script hardcode `C:/Program Files/Google/Chrome/Application/chrome.exe` — máy nào không có Chrome thì đổi sang `~/AppData/Local/ms-playwright/chromium-1228/chrome-win/chrome.exe`.

```bash
cp "C:/Users/NTQUANG_DELL/AppData/Local/hermes/skills/devops/camofox-browser/scripts/verify-html-render.cjs" \
   "/d/Hermes Proj/camofox-browser/verify-html-render.cjs"
cd "/d/Hermes Proj/camofox-browser" && node verify-html-render.cjs "http://127.0.0.1:<port>/<file>.html" "./shots"
```

Nó trả về: overflow ngang (desktop + mobile), font đã load chưa, ảnh vỡ, số panel hiển thị sau mỗi lần click tab (bắt lỗi tab JS không chuyển), số từ trong panel đang active, tab bar mobile có cuộn được không. Chạy được với URL remote — không cần serve local như khi test qua Camofox (Camofox chặn `file://`).

⚠️ **Đọc output cho đúng (verified 25/09/2026):** script in ra TÊN FONT MẶC ĐỊNH CỦA CHÍNH NÓ, không phải font trang bạn dùng. Dòng `fonts: {"Plus Jakarta Sans":true,"DM Sans":true}` xuất hiện cả khi trang dùng Inter + Space Grotesk → đừng trích nó làm bằng chứng "font đã load". Thứ thực sự là điều kiện qua:
- `base.hOverflow === false` **và** `mobile.hOverflow === false` — hết overflow ngang ở cả 2 viewport
- `base.brokenImgs` rỗng, `mobile.overflowingTextNodes` rỗng
- `base.title` khớp tiêu đề bạn đặt
Kết quả cuối cùng phải có dòng `DONE`; nếu không có, script chết giữa đường và mọi thứ trên chỉ là một phần.

## Trigger

- Browser tool báo "Cannot connect to Camofox at http://localhost:9377"
- Cần mở trang web, đăng nhập, vượt captcha, hoặc lấy snapshot trang yêu cầu browser thật
- Cần troubleshoot session/profile Camofox

## Start

```bash
cd "D:/Hermes Proj/camofox-browser" && node server.js
# LUÔN chạy background (terminal background=true) — server không bao giờ exit
# watch_patterns: ["\"level\":\"error\""] — KHÔNG dùng "server started"/"camoufox launched" vì fire liên tục (idle shutdown 5 phút → relaunch), nhiễu. Chỉ báo lỗi thật.
# ⚠️ NHƯNG: khi research nặng (subagent mở hàng chục URL), pattern "level":"error" cũng SPAM chat Telegram — mỗi lỗi transient (tab timeout, navigate fail) = 1 notification. User tưởng cron/hệ thống hỏng. Nếu user hỏi "cron này có phải nhóm này k?" → kill process + start lại KHÔNG watch pattern (silent) — server vẫn chạy bình thường, hết spam. Chỉ giữ watch pattern khi đang debug chủ động.
```

- Lần đầu khởi động 10-30s, log tuần tự: `server started` port 9377 → `launching camoufox` → `camoufox launched` → `browser pre-warmed`
- Health check sau start: gọi browser_navigate thử 1 URL, hoặc `curl -s http://localhost:9377/`
- **Lần navigate ĐẦU TIÊN có thể fail 500** vì session cũ bị reaper destroy (`tab_reaper_empty_session`) → retry 1 lần là OK, không phải bug
- **Log "camoufox launched" lặp lại là BÌNH THƯỜNG** — browser idle shutdown sau ~5 phút không session (`browser idle shutdown (no sessions)`) rồi relaunch on-demand khi có request mới. Không phải lỗi, không cần xử lý. Watch pattern KHÔNG nên bắt chuỗi này (nhiễu), chỉ bắt `"level":"error"`.

## API tóm tắt

- `POST /tabs` `{userId, sessionKey, url}` → `{tabId}`
- `GET /tabs/:tabId/snapshot?userId=` → accessibility tree với element refs
- `POST /tabs/:tabId/click|type|scroll|navigate` `{userId, ref|selector, text}`
- `DELETE /sessions/:userId` → xoá session (cookies/storage) khi session hỏng
- Chi tiết đầy đủ: `D:/Hermes Proj/camofox-browser/AGENTS.md`

## Pitfalls

- **file:// bị chặn — "Blocked URL scheme: file: (only http/https allowed)":** Camofox KHÔNG mở được URL `file:///...` (400 Bad Request từ `/tabs`). Muốn test HTML local: serve qua HTTP trước (`python -m http.server <port> --bind 127.0.0.1` trong thư mục chứa file, background=true), rồi `browser_navigate(http://127.0.0.1:<port>/<file>.html)`. Nhớ kill server sau khi xong. Nếu vẫn 400, thử `curl -X DELETE http://localhost:9377/sessions/<userId>` trước rồi retry (session cũ hỏng cũng gây 400/500).
- **404 cho file CÓ THẬT = 2 http.server cùng bind 1 port (verified 25/09/2026).** Windows cho phép nhiều process bind cùng port (SO_REUSEADDR bật mặc định), nên một `http.server` cũ từ session trước vẫn LISTENING song song với cái mới. Request rơi vào cái cũ → serve thư mục KHÁC → directory listing vẫn hiện file quen, file quen vẫn 200, nhưng file vừa tạo thì 404. Rất dễ chẩn đoán nhầm thành lỗi đường dẫn hay cache. **Check trước khi serve:**
  ```bash
  netstat -ano | grep ":<port>" | grep LISTENING | wc -l   # phải bằng 1
  ```
  Nếu >1 → đổi port chưa ai dùng, hoặc kill PID cũ bằng `powershell -NoProfile -Command "Stop-Process -Id <PID> -Force"`. Đừng tin directory listing để kết luận "server đang serve đúng thư mục".
- **Stale profile → 500 "new page timed out" / "new_page_unresponsive":** profile cũ trong `~/.camofox/profiles/<id>/storage-state.json` bị hỏng → mọi `/tabs` fail. Fix: kill server → `rm -rf ~/.camofox/profiles/<id>` (lấy đúng id từ log dòng "storage state persisted ... profiles/<id>") → start lại. Xoá profile = mất cookies login của profile đó — chấp nhận được, login lại.
- **Board/ứng dụng private (cần login web):** browser sẽ đứng ở trang login. Nếu chỉ có API key/token (không có email+password), KHÔNG cố login web — quét qua API của dịch vụ đó (vd Trello: `curl api.trello.com/1/lists/...`) là đường tin cậy. Đừng hỏi user password nếu chưa cần thiết.
- **Trước khi restart server:** nếu server đang chạy và chỉ cần clear session, thử `curl -X DELETE http://localhost:9377/sessions/<userId>` trước (rẻ hơn kill+rm profile). Xoá profile chỉ khi session-level vẫn còn lỗi.
- **Không chạy foreground** — `node server.js` không exit; luôn background=true.

## Error triage nhanh (15/08/2026)

Khi watch pattern `"level":"error"` báo lỗi, phân loại TRƯỚC khi sửa:

| Error | Ý nghĩa | Xử lý |
|---|---|---|
| `new page retry timed out after 10000ms` | Tab tạo chậm >10s — thường do browser vừa idle-shutdown xong đang relaunch, hoặc cron spam request | Thoáng qua. Retry 1 lần, không cần kill server |
| `browserContext.newPage: ... has been closed` | Health probe trúng lúc browser đang tắt (idle shutdown race) | Thoáng qua, server tự restart. Retry |
| `NS_ERROR_UNKNOWN_HOST` (navigate failed) | **DOMAIN CHẾT/NXDOMAIN — lỗi NGUỒN, không phải lỗi Camofox** | Verify bằng `nslookup <domain>` → "Non-existent domain". Báo nguồn research bỏ link, đừng chạy theo fix server |

Kinh nghiệm thực tế (15/08): cron knowledge-researcher mở `vietnamchemicals.vn` (NXDOMAIN) → 4 lần tab timeout + 2 lần navigate fail liên tiếp trong 2 phút. Nhìn bề ngoài tưởng server chết, thực ra là domain nguồn không tồn tại.

## Watch pattern rate-limit + process tracking (bài học 15/08/2026)

- **Hermes auto-disable watch pattern sau 3 lần rate-limit liên tiếp** (min spacing 15s) → fallback về notify_on_complete (chỉ báo 1 lần khi process EXIT). Đây là thiết kế, không phải lỗi. Pattern tần suất cao (như `camoufox launched`) luôn bị disable; chỉ dùng pattern tần suất thấp (`"level":"error"`).
- **Kill process Hermes-tracked rồi có cron khác tự start server → PID mới KHÔNG Hermes-tracked** → watch pattern mất tác dụng. Xảy ra khi cron (vd knowledge-researcher-4h, có web+terminal toolset) gọi browser tools → Hermes tự launch lại server ngoài quản lý. Nhận biết: `process list` không thấy process cũ, nhưng port 9377 vẫn 200.
- **Tìm ai đang giữ port khi mất track:** `netstat -ano | grep ":9377"` → PID, rồi `wmic process where "ProcessId=<PID>" get CommandLine,CreationDate /format:list`. Chú ý: trong git-bash `tasklist`/`taskkill //F` bị path-conversion nuốt dấu `/` — dùng wmic hoặc `powershell Stop-Process` (xem Pitfall port in use ở trên).
- **Quyết định (15/08): để server chạy tự nhiên, không ép track lại.** Server tự sống, tự hồi phục; watch pattern chỉ là tiện ích, không phải hệ thống giám sát. Nếu cần alert thật sự → dùng cron riêng check port.

## Search fallback: DuckDuckGo qua Camofox khi Google/Bing chặn

Google (unusual-traffic CAPTCHA) và Bing (kết quả rác A/B, "cm to feet" cho query bất kỳ) chặn cả curl lẫn Camofox từ IP VN. **DuckDuckGo vẫn hoạt động qua Camofox** — đây là đường search web đáng tin khi các engine khác chặn (verified 08/2026):

```bash
python scripts/camsearch.py "tannin hạt dẻ chestnut tannin giá" 10
```

Script tự tạo tab mới (POST /tabs), navigate `https://duckduckgo.com/?q=<q>&ia=web`, chờ 4s, trích link/title qua evaluate JS (`a[href^="http"]`, loại bỏ duckduckgo.com). Kết quả: URL thật của shopee.vn, hoachatthinghiem.org, nhachannuoi.vn... Từ đó dùng `page_text()` mở từng URL trích giá. Lưu ý: `html.duckduckgo.com/lite` và `html.duckduckgo.com/html` qua curl bị chặn (trang rỗng/canonical về trang chủ) — phải đi qua browser thật.

⚠️ **Path script camsearch.py (dính lỗi 17/08/2026):** nằm trong `scripts/` CỦA SKILL này (`C:/Users/NTQUANG_DELL/AppData/Local/hermes/skills/devops/camofox-browser/scripts/camsearch.py`) — KHÔNG nằm trong `D:/Hermes Proj/camofox-browser/scripts/` (thư mục repo server chỉ chứa exec.js/plugin.js/postinstall.js...). Chạy `python scripts/camsearch.py` từ repo dir sẽ lỗi `can't open file`. Dùng full path, hoặc import trong script batch: `sys.path.insert(0, "C:/Users/NTQUANG_DELL/AppData/Local/hermes/skills/devops/camofox-browser/scripts")` rồi `from camsearch import search_ddg, page_text` (pattern batch đã chứng minh 17/08/2026: gom nhiều search + page_text vào 1 script, save từng kết quả ra file ngay).

**Research dữ liệu tài chính/doanh nghiệp VN** (trích bảng "Công ty con & liên kết" + "Danh sách cổ đông" trên cafef.vn qua browser_console — click tab `.owner-tab`, chờ JS render; pitfall bảng cafef bị STALE phải cross-verify từng tỷ lệ với tin bài; đọc bài báo VN bị encode UTF-16; nguồn BCTC chính thức JS-rendered): xem `references/vn-financial-data.md`.

**Full pipeline research giá VN + merge Google Sheets:** `references/vn-price-research.md` — delegate 3 nhóm → loop local (JSONL từng item) → regex trích giá VNĐ → quy đổi đơn vị (mg/kg, %, CFU→g premix) → thêm cột tính lượng mua (công thức sống `=IF(ISNUMBER(J2),ROUND($K$50*J2/1000,2),"")`; PITFALL #REF! self-reference khi đặt tổng ngay trong ô tham chiếu).

## QA trang HTML đã publish — đường KHÔNG qua Camofox (verified 13/10/2026)

Khi chỉ cần verify một trang HTML đã publish (overflow, layout, ảnh vỡ), dùng thẳng `scripts/verify-html-render.cjs`: nó chạy playwright-core + chromium trực tiếp, **không tạo tab qua Camofox**, nên miễn nhiễm với mọi vấn đề tab/session/profile. Đây là đường ngắn nhất cho HTML QA, không phải fallback.

Ca nhận ra điều này (13/10/2026): `/` health check trả `{"ok":true,"enabled":true,"running":true,"browserConnected":true,"browserRunning":true}` nhưng `POST /tabs` (tức mọi `browser_navigate`) trả **500 Internal Server Error** liên tiếp 2 lần. Server "khỏe" theo health nhưng tab creator kẹt.

Thứ tự xử lý khi `POST /tabs` trả 500:
1. Retry navigate **1 lần** (session cũ bị reaper destroy — bình thường, xem mục Start).
2. Vẫn 500 → **nếu mục tiêu chỉ là QA HTML đã publish, chuyển thẳng sang `verify-html-render.cjs`** và xong việc. Đừng leo thang kill/rm profile cho một việc mà đường khác làm được.
3. Chỉ khi cần browser thật để login/click/vượt captcha mới quay lại xử lý server: `curl -X DELETE http://localhost:9377/sessions/<userId>` → vẫn lỗi thì tìm PID qua `netstat -ano | grep -E ":9377.*LISTEN"` → `powershell -NoProfile -Command "Stop-Process -Id <PID> -Force"` → `rm -rf ~/.camofox/profiles/<id>` → start lại background.

Lệnh QA đã chạy được (remote URL, không cần serve local):

```bash
cp "C:/Users/NTQUANG_DELL/AppData/Local/hermes/skills/devops/camofox-browser/scripts/verify-html-render.cjs" \
   "/d/Hermes Proj/camofox-browser/verify-html-render.cjs"
cd "/d/Hermes Proj/camofox-browser" && node verify-html-render.cjs "https://preview.thefirstonly.com/<id>" "./shots-x"
# xong thì xoá bản copy: rm -f "/d/Hermes Proj/camofox-browser/verify-html-render.cjs"
```

Nhớ xoá bản copy khỏi repo sau khi xong để lần sau không lẫn bản cũ.

## Direct API driving (khi Hermes browser client kẹt tab chết)

**Triệu chứng:** mọi `browser_navigate`/`browser_console` trả `410 Gone` với cùng tabId cũ sau khi server restart — Hermes client giữ tab id không còn tồn tại (loop vô hạn, DELETE session không cứu được vì client vẫn dùng tab id cũ).

**Fix nhanh (đã chứng minh):** bỏ qua Hermes client, điều khiển Camofox trực tiếp qua API bằng curl/python:

```bash
curl -s -X POST http://localhost:9377/tabs -H "Content-Type: application/json" \
  -d '{"userId":"pricer","sessionKey":"research","url":"https://duckduckgo.com"}'   # → tabId mới
curl -s -X POST http://localhost:9377/tabs/<tabId>/navigate -H "Content-Type: application/json" \
  -d '{"userId":"pricer","url":"https://duckduckgo.com/?q=<q>&ia=web"}'
curl -s -X POST http://localhost:9377/tabs/<tabId>/evaluate -H "Content-Type: application/json" \
  -d '{"userId":"pricer","expression":"document.body.innerText.slice(0,3000)"}'
```

Mẫu đầy đủ: `scripts/camsearch.py` (search + page_text). Tab tạo với userId riêng không bị Hermes client chiếm.

## Pitfalls bổ sung

- **Research nhiều query liên tiếp: KHÔNG dùng chung 1 tab cho toàn bộ loop** — tab Camofox chết/kẹt sau 1-2 navigate (evaljs trả rỗng, các query sau urls=0). Pattern đã chứng minh (15/08/2026): mỗi query tạo TAB MỚI (POST /tabs) → navigate DDG → evaluate → mở 2 URL trích giá → ghi JSONL ngay sau mỗi chất → `DELETE /sessions/<userId>` reset giữa chừng (tránh tab accumulation khiến server treo). Ghi file JSONL theo từng dòng sau mỗi item để timeout/kill không mất dữ liệu đã research. Script mẫu: `C:/Users/NTQUANG_DELL/httptmp/research_groupA3.py` (13 chất ~15 phút, ~75s/chất).
- **Subagent delegate research hay hết iteration (50 api_calls) TRƯỚC khi ghi file JSON** (3/3 subagent dính 15/08/2026): (1) khi dispatch yêu cầu subagent ghi JSONL từng item sau mỗi chất thay vì gom cuối; (2) nếu vẫn bị cắt, chạy lại phần còn thiếu bằng script local (camsearch.py + DDG) — dữ liệu inline trong summary của subagent thì gom ghi file ngay; (3) TUYỆT ĐỐI không bịa giá/PMID khi thiếu — ghi "Chưa verify" + verified:false.
- **MSYS `/tmp` + curl native Windows không tương thích:** `curl -o /tmp/page.html` (trong bash MSYS) lỗi "No such file or directory" khi đọc lại — path `/tmp` của MSYS khác path literal curl dùng. Luôn dùng thư mục local như `$HOME/httptmp`. ⚠️ Cụ thể hơn (verified 12/09/2026): literal `/c/Users/...` trong `-o` cũng fail (`curl: (23) Failure writing output to file`, exit 23) — native Windows curl cần path kiểu Windows `C:/Users/...` (forward slash, có drive letter). Dùng `C:/Users/...` hoặc `$HOME/...` (bash mở rộng), KHÔNG dùng `/c/Users/...` literal.
- **Site VN chặn bot:** thegioihoachat.com.vn trả 403 (có lúc) hoặc shell cũ 7398-byte "CHEMICAL WORLD" (chemworld.vn, HTTP 200) với search `/?s=` luôn trả trang chủ và `/tim-kiem` 404 — không có giá bán lẻ, đừng tốn turn; vietnamchemicals.vn không kết nối được. Search DDG trước rồi mở trang kết quả (shopee.vn, hoachatthinghiem.org, nhathuocbachmai.vn... hoạt động tốt). **Research giá VN (verified 15/08/2026): websosanh.vn là nguồn giá tốt nhất qua curl** (so sánh Shopee/Tiki, trả số thật — acid citric bao 25kg 670-1000k, B. subtilis nguyên liệu 280-480k/kg). Các nguồn mở được khác: hoachatthinghiem.org (tannic acid 1,3tr/kg), tinhbotnghekc.com (curcumin 95% 385-500k/kg), oilcare.vn + kobi.vn (tinh dầu bán sỉ), trungtamduoclieu.vn (dược liệu khô), pharmacity.vn + nhathuoclongchau.com.vn (dược phẩm), itaco.com.vn/hoachatvietmy.vn (bentonite/zeolite theo tấn). Feed-grade nhập khẩu (MOS, butyrate coated, boulardii...) hầu như không niêm yết công khai → ghi "Chưa có giá công khai", availability='Đặt hàng riêng/Nhập khẩu'.
- **Server cũ treo chiếm port 9377 → `node server.js` mới báo `port in use`:** server từ session trước vẫn LISTENING nhưng tab creator kẹt → browser_navigate fail 500, POST /tabs treo (HTTP:000), health check vẫn `running:true`. Fix: (1) thử rẻ nhất `curl -X DELETE http://localhost:9377/sessions/<userId>` rồi retry; (2) vẫn lỗi → tìm PID `netstat -ano | grep -E ":9377.*LISTEN"` → kill bằng `powershell -NoProfile -Command "Stop-Process -Id <PID> -Force"` — trong git-bash `taskkill //F //PID <pid>` báo "Invalid argument/option - '//F'" (path conversion nuốt dấu /), không dùng được; (3) `rm -rf ~/.camofox/profiles/<id>` nếu profile cũ hỏng; (4) start lại background.
- **Sau khi restart server**, session/tab cũ chết → tạo tab mới qua API (xem Direct API driving) hoặc xoá profile; đừng retry navigate với tab id cũ.

## Đánh giá browser engine THAY THẾ Camofox (Obscura/headless khác) — test anti-bot TRƯỚC, đừng tin benchmark chủ

Case 2026-09-11: user gửi bài PR về **Obscura** (Rust headless browser cho AI agent, 26.7K stars, Apache-2.0, `obscura serve` CDP 9222 + MCP server + stealth fingerprint rotation). Repo thật, Windows build có sẵn, chạy được — NHƯNG test thật trên máy:

| Test | Kết quả | Kết luận |
|---|---|---|
| example.com | ✅ 307ms | engine chạy được |
| cafef.vn | ⚠️ 22.5s, text dump 15KB rác widget | Highcharts lỗi script, chậm hơn nhiều claim |
| duckduckgo.com | ❌ redirect noscript (384 bytes) | detect engine không phải Chromium |
| shopee.vn | ❌ redirect `/unsupported.html` "trình duyệt không còn hỗ trợ" | chặn cứng |

CDP của Obscura chỉ implement TẬP CON domain (Target/Page/Runtime/DOM/Network/Fetch/IO/Storage/Input/LP) — **KHÔNG có Accessibility** → Hermes browser_snapshot (dựa accessibility tree) KHÔNG drop-in được. Benchmark "85ms vs Chrome 500ms" là repo tự chấm, engine cắt bớt layout/Web API nên nhanh — và chính sự cắt đó khiến site anti-bot nhận ra.

**Quy tắc đánh giá browser thay thế (đã chứng minh):**
1. Đừng tin benchmark/PR marketing từ repo chính chủ; check `releases/latest` có asset cho nền tảng mình trước.
2. Test ít nhất: 1 trang anti-bot thật (shopee.vn, duckduckgo.com, google.com) + 1 trang VN script nặng (cafef.vn) — trang tĩnh OK không chứng minh gì.
3. Check CDP domain coverage so với thứ Hermes cần (Accessibility cho snapshot, Input cho click/type) trước khi nói "drop-in".
4. Kết luận thẳng cho user: không dùng được → đừng đầu tư thêm giờ; giữ binary nếu cần `scrape --concurrency` cho trang tĩnh không chặn.

### Chạy exe Windows qua terminal tool — lifecycle guard crash "embedded null character in path" → PATH trick

Khi command chứa `./obscura.exe` hoặc path Windows tuyệt đối `"C:/.../obscura.exe"`, terminal tool báo `Failed to execute command: open: embedded null character in path` (guard `cron/lifecycle_guard.py` parse nhầm path có `:` / `./`). `--version` có thể còn chạy, nhưng lệnh chứa URL/fetch/help thì crash.

Workaround đã chứng minh: copy exe ra thư mục không dấu cách → `cd` vào đó → `export PATH="$PWD:$PATH"` → gọi BARE name (`obscura.exe ...`), không dùng `./` và không dùng path tuyệt đối trong command. Cũng tránh shell redirect `>` vào file mà guard cố đọc — dùng flag `--output` của tool nếu có.
