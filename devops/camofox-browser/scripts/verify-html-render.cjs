// Verify + screenshot an HTML page without a vision model.
// Works for a remote URL (e.g. a preview link) OR a local http server.
// Catches: horizontal overflow, missing fonts, broken images, tab panels not switching.
//
// Usage:
//   cd "D:/Hermes Proj/camofox-browser"
//   node verify-html-render.cjs <url> <outDir> [tabSelector]
//
// Example:
//   node verify-html-render.cjs https://preview.thefirstonly.com/e00o5mfkmiuf "./shots" ".tab"
//
// Must be .cjs — camofox-browser package.json has "type":"module", so a .js file
// is treated as ESM and `require` blows up with "require is not defined".
//
// Font names in the font check are page-specific; edit FONTS below per project.

const { chromium } = require("playwright-core");
const fs = require("fs");

const CHROME =
  "C:/Users/NTQUANG_DELL/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe";

// [css font shorthand, human label] — adapt per project
const FONTS = [
  ["700 16px 'Plus Jakarta Sans'", "Plus Jakarta Sans"],
  ["400 16px 'DM Sans'", "DM Sans"]
];

const url = process.argv[2];
const outDir = process.argv[3] || "./shots";
const tabSel = process.argv[4] || null;

if (!url) {
  console.error("usage: node verify-html-render.cjs <url> <outDir> [tabSelector]");
  process.exit(1);
}
fs.mkdirSync(outDir, { recursive: true });

const report = (label, obj) => console.log(label + ": " + JSON.stringify(obj));

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME });

  // ---------- desktop ----------
  const page = await browser.newPage({
    viewport: { width: 1440, height: 1000 },
    deviceScaleFactor: 2
  });
  await page.goto(url, { waitUntil: "networkidle" });
  await page.waitForTimeout(2000);

  report(
    "base",
    await page.evaluate(() => ({
      title: document.title,
      scrollW: document.documentElement.scrollWidth,
      innerW: window.innerWidth,
      hOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
      brokenImgs: [...document.images]
        .filter((i) => i.complete && i.naturalWidth === 0)
        .map((i) => i.src)
    }))
  );

  report(
    "fonts",
    await page.evaluate((pairs) => {
      const out = {};
      for (const [shorthand, label] of pairs) {
        out[label] = document.fonts.check(shorthand);
      }
      return out;
    }, FONTS)
  );

  if (tabSel) {
    const tabs = await page.$$(tabSel);
    report("tabCount", { n: tabs.length });

    for (let i = 0; i < tabs.length; i++) {
      await tabs[i].click();
      await page.waitForTimeout(600);
      report(
        "tab" + (i + 1),
        await page.evaluate((sel) => {
          const all = [...document.querySelectorAll(".panel")];
          const visible = all.filter((p) => p.offsetParent !== null);
          const active = document.querySelectorAll(sel + ".active").length;
          const shown = active === 1 ? visible.find((p) => p.classList.contains("active")) || visible[0] : visible[0];
          return {
            scrollH: document.body.scrollHeight,
            hOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
            visiblePanels: visible.length,
            activeTabs: active,
            wordsInPanel: shown ? shown.innerText.trim().split(/\s+/).length : 0
          };
        }, tabSel)
      );
      await page.screenshot({ path: `${outDir}/tab${i + 1}.png`, fullPage: true });
    }
  } else {
    await page.screenshot({ path: `${outDir}/desktop.png`, fullPage: true });
  }

  // ---------- mobile ----------
  const m = await browser.newPage({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2
  });
  await m.goto(url, { waitUntil: "networkidle" });
  await m.waitForTimeout(1500);

  report(
    "mobile",
    await m.evaluate(() => {
      const overflowing = [...document.querySelectorAll("p,li,td,th,h1,h2,h3,h4")]
        .filter((el) => el.scrollWidth > el.clientWidth + 2)
        .map((el) => el.tagName + ": " + el.innerText.slice(0, 40));
      const nav = document.querySelector("nav.tabs");
      return {
        hOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
        overflowingTextNodes: overflowing,
        tabBarScrollable: nav ? nav.scrollWidth > nav.clientWidth : null,
        tabCount: document.querySelectorAll(".tab").length
      };
    })
  );
  await m.screenshot({ path: `${outDir}/mobile.png`, fullPage: false });

  await browser.close();
  console.log("DONE");
})().catch((e) => {
  console.error("ERR", e.message);
  process.exit(1);
});
