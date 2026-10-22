# Screenshot HTML/SVG local bằng playwright-core (không cần vision model)

Dùng khi cần chụp ảnh HTML/SVG local để gửi user xem, hoặc verify visual mà không có vision model (deepseek-v4-flash hiện KHÔNG nhận image_url — browser_vision/vision_analyze trả 400 `unknown variant image_url`).

## Cách đúng (verified 11/08/2026)

Dùng `playwright-core` có sẵn trong camofox-browser + executable chromium của ms-playwright. Không dùng python playwright (greenlet hỏng trên Python 3.14 → `ModuleNotFoundError: No module named 'greenlet._greenlet'`; đừng mất thời gian cài lại, dùng node path này).

1. Viết script `.cjs` (BẮT BUỘC — camofox-browser `package.json` có `"type": "module"`, file `.js` bị đối xử ESM → `ReferenceError: require is not defined`):
```js
const { chromium } = require("playwright-core");
(async () => {
  const browser = await chromium.launch({
    executablePath: "C:/Users/NTQUANG_DELL/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe"
  });
  const page = await browser.newPage({ viewport: { width: 1400, height: 900 }, deviceScaleFactor: 2 });
  await page.goto("file:///D:/Hermes Proj/<path>.html");
  await page.waitForTimeout(1500);
  await page.screenshot({ path: "D:/Hermes Proj/<out>.png", fullPage: true });
  await browser.close();
  console.log("screenshot saved");
})().catch(e => { console.error(e.message); process.exit(1); });
```

2. Chạy:
```bash
cd "D:/Hermes Proj/camofox-browser" && node tmp-shot.cjs
```

3. Dọn file temp sau khi xong.

## Verify layout khi không có vision

Mở file qua browser_navigate (nhớ serve HTTP — camofox chặn file://, xem SKILL.md camofox-browser), rồi dùng browser_console chạy JS đếm overflow:
```js
(() => {
  const svg = document.querySelector('svg');
  const vb = svg.viewBox.baseVal;
  const texts = [...svg.querySelectorAll('text')].map(t => { const b = t.getBBox(); return { txt: t.textContent.slice(0,15), right: Math.round(b.x+b.width), bottom: Math.round(b.y+b.height) }; });
  return { viewBox: {w: vb.width, h: vb.height}, overflow: texts.filter(t => t.right > vb.width-2 || t.bottom > vb.height-2) };
})()
```
Nếu overflow có phần tử → kéo dài viewBox hoặc dịch element. Cách này bắt được lỗi "legend tràn viewBox" mà mắt thường dễ bỏ.

**browser_console bị 500-loop (verified 12/08/2026):** khi session Camofox hỏng, `/tabs/:id/evaluate` trả 500 liên tục. Đừng retry cùng args — chuyển hẳn sang script .cjs playwright-core để chạy FUNCTIONAL checks (filter/expand/search count + overflow) chứ không chỉ screenshot. Skeleton: skill `research-html-catalog` → `references/subagent-schema-and-build.md` mục 4.

## Paths
- playwright-core: `D:/Hermes Proj/camofox-browser/node_modules/playwright-core`
- chromium executable: `C:/Users/NTQUANG_DELL/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe` (tìm lại: `find "$LOCALAPPDATA/ms-playwright" -name "chrome.exe"`)
- Google Fonts cần mạng: nếu chụp offline, fonts không load nhưng layout vẫn đúng.
