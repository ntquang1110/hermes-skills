// Dem DOM de VERIFY mot trang da publish khi tool `browser_*` hong.
//
// Dung khi: Camofox `/tabs` tra 500 (loi da gap nhieu lan) khien browser_navigate /
// browser_console khong dung duoc, nhung van phai chung minh trang tuan thu spec
// bang so lieu DOM chu khong bang anh chup.
//
// Usage:
//   cd "D:/Hermes Proj/camofox-browser"
//   node verify-dom-count.cjs <url> "<sel1>,<sel2>,..." [minFontPx]
//
// Vi du:
//   node verify-dom-count.cjs https://preview.thefirstonly.com/xxx "table,details.deep,.rung,.kpi > div" 12
//
// In ra 3 dong: desktop / mobile360 / mobile-kiem.
// Phai dat: tables=0 (neu spec cam bang), nOverflow=0, smallText=0, minFontPx >= nguong.
//
// Luu y: selector dem duoc la danh sach phan cach bang dau phay, moi cai tra ve 1 con so.
// Ten selector khong duoc chua dau phay.

const { chromium } = require("playwright-core");
const fs = require("fs");

const CHROME =
  process.env.HERMES_CHROME ||
  "C:/Users/NTQUANG_DELL/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe";

const url = process.argv[2];
const sels = (process.argv[3] || "table").split(",").map((s) => s.trim()).filter(Boolean);
const minFont = parseFloat(process.argv[4] || "12");

if (!url) {
  console.error("usage: node verify-dom-count.cjs <url> \"<sel1>,<sel2>\" [minFontPx]");
  process.exit(1);
}
if (!fs.existsSync(CHROME)) {
  console.error("Khong thay Chromium tai: " + CHROME);
  console.error("Dat bien moi truong HERMES_CHROME tro toi chrome.exe that.");
  process.exit(2);
}

const SELS = JSON.stringify(sels);
const report = (l, o) => console.log(l + ": " + JSON.stringify(o));

const COUNT = `(() => {
  const d = document, sels = ${SELS};
  const out = { tables: d.querySelectorAll("table").length };
  sels.forEach(s => { out[s] = d.querySelectorAll(s).length; });
  out.bodyH = d.body.scrollHeight;
  out.docW = d.documentElement.clientWidth;
  out.scrollW = d.documentElement.scrollWidth;
  return out;
})()`;

const AUDIT = `(() => {
  const d = document;
  const bad = [];
  d.querySelectorAll("body *").forEach(e => {
    const r = e.getBoundingClientRect();
    if (r.width > 0 && r.right > d.documentElement.clientWidth + 1) {
      bad.push((e.className && String(e.className).slice(0, 40)) || e.tagName);
    }
  });
  let small = 0, minPx = 999;
  d.querySelectorAll("body *").forEach(e => {
    if (e.children.length || !e.textContent || !e.textContent.trim()) return;
    const fs = parseFloat(getComputedStyle(e).fontSize);
    if (fs < minPx) minPx = fs;
    if (fs < ${minFont}) small++;
  });
  return { nOverflow: bad.length, overflowSample: bad.slice(0, 6),
           smallText: small, minFontPx: minPx };
})()`;

(async () => {
  const b = await chromium.launch({ executablePath: CHROME });

  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  await p.goto(url, { waitUntil: "load", timeout: 60000 });
  await p.waitForTimeout(1200);
  report("desktop", await p.evaluate(COUNT));

  // Mo het <details> roi dem lai: noi dung that su ton tai, khong bi an rong
  const nDet = await p.evaluate(
    () => document.querySelectorAll("details").length
  );
  if (nDet) {
    await p.evaluate(() => document.querySelectorAll("details").forEach((x) => (x.open = true)));
    await p.waitForTimeout(400);
    report("mo-het-details", await p.evaluate(COUNT));
  }

  const errs = [];
  p.on("pageerror", (e) => errs.push(e.message));
  report("jsErrors", errs);

  const m = await b.newPage({ viewport: { width: 360, height: 800 } });
  await m.goto(url, { waitUntil: "load", timeout: 60000 });
  await m.waitForTimeout(1200);
  report("mobile360", await m.evaluate(COUNT));
  report("mobile-kiem", await m.evaluate(AUDIT));

  await b.close();
  console.log("DONE");
})().catch((e) => {
  console.error("ERR", e.message);
  process.exit(1);
});
