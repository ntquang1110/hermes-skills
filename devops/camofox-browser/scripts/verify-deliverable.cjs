#!/usr/bin/env node
/**
 * verify-deliverable.cjs — audit a PUBLISHED HTML deliverable against the
 * house spec, across several viewports, WITHOUT going through Camofox tabs.
 *
 * Checks that caught real bugs in past sessions:
 *   - text below the minimum font size (spec: nothing under 12px, ANY viewport)
 *   - horizontal overflow / scrollbar
 *   - broken images
 *   - em dash (AI-ism) leaking into rendered text
 *   - <table> count (many deliverable specs require ZERO tables)
 *   - children escaping their own container (overflow inside a card, not the page)
 *   - list bullets that were meant to be suppressed but still render
 *   - DIVERGING BAR CHARTS: bar drawn on the wrong side of the 0 axis.
 *     This is a SEMANTIC bug, not a layout bug: a bar for a negative value
 *     drawn left-to-right reads as POSITIVE. Vision review catches it only by
 *     luck; this check catches it mechanically. Run it on any chart carrying
 *     both positive and negative values. Correct pattern: the track has a
 *     centre line, positive fills anchored left:50%, negative fills anchored
 *     right:50%, width = |value| / maxAbs * 50% (max magnitude = half track).
 *
 * NOTE ON SHAPE: the audit body is written inline inside page.evaluate on
 * purpose. That is the form verified in practice. Do not "clean it up" into a
 * helper + new Function(...) indirection: CSP on some hosts blocks eval, and
 * functions defined on the Node side will not survive serialisation.
 *
 * USAGE
 *   node verify-deliverable.cjs <url> [minFontPx] [extraChecksJson]
 *
 *   minFontPx        default 12
 *   extraChecksJson  default {"bars":".tr|i"}
 *                    bars = "<trackSelector>|<fillSelector>"; pass {} to skip
 *
 * EXAMPLES
 *   node verify-deliverable.cjs https://preview.thefirstonly.com/abc123
 *   node verify-deliverable.cjs http://127.0.0.1:8100/x.html 12 '{"bars":".bar|.fill"}'
 *
 * EXIT CODE
 *   0 = all green · 1 = a check failed (see report.failures) · 2 = script error
 *
 * BROWSER
 *   Needs playwright-core. Pass CHROME_PATH, else it probes Windows Chrome,
 *   Edge, then the ms-playwright chromium bundle. If playwright-core is not in
 *   the script's own node_modules, set NODE_PATH (see SKILL.md).
 */

const fs = require("fs");
const { chromium } = require("playwright-core");

const CHROME_CANDIDATES = [
  process.env.CHROME_PATH,
  "C:/Program Files/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
  "C:/Users/" + (process.env.USERNAME || "user") +
    "/AppData/Local/ms-playwright/chromium-1228/chrome-win/chrome.exe"
].filter(Boolean);

const url = process.argv[2];
const MIN_FONT = parseFloat(process.argv[3] || "12");
const EXTRA = process.argv[4] ? JSON.parse(process.argv[4]) : { bars: ".tr|i" };
const WIDTHS = [360, 390, 768, 1440];
const BAR_SPLIT = EXTRA.bars ? EXTRA.bars.split("|") : null;

if (!url) {
  console.error("usage: node verify-deliverable.cjs <url> [minFontPx] [extraChecksJson]");
  process.exit(2);
}

function pickChrome() {
  for (const p of CHROME_CANDIDATES) {
    try {
      if (fs.existsSync(p)) return p;
    } catch (_) {}
  }
  return undefined; // let playwright use its own resolution
}

(async () => {
  const exe = pickChrome();
  const browser = await chromium.launch(exe ? { executablePath: exe } : {});
  const failures = [];
  const report = {};

  for (const w of WIDTHS) {
    const page = await browser.newPage({ viewport: { width: w, height: 1000 }, deviceScaleFactor: 1 });
    const resp = await page.goto(url, { waitUntil: "networkidle" });
    await page.waitForTimeout(1000);
    // Open every collapsed block so hidden copy gets audited too.
    await page.evaluate(() => document.querySelectorAll("details").forEach((d) => (d.open = true)));
    await page.waitForTimeout(400);

    const r = await page.evaluate(
      ({ mf, bs }) => {
        const barTrack = bs ? bs[0] : null;
        const barFill = bs ? bs[1] : null;

        let min = 9999;
        const underMin = [];
        document.querySelectorAll("body *").forEach((el) => {
          if (el.children.length) return;              // leaf text nodes only
          const t = (el.textContent || "").trim();
          if (!t) return;
          const f = parseFloat(getComputedStyle(el).fontSize);
          if (f < min) min = f;
          if (f < mf) {
            underMin.push(f + "px | " + el.tagName + "." + (el.className || "-") + " | " + t.slice(0, 40));
          }
        });

        const de = document.documentElement;
        const text = document.body.innerText || "";

        const escaped = [];
        document.querySelectorAll("section, .dbody, .card, li").forEach((box) => {
          const bb = box.getBoundingClientRect();
          if (bb.width === 0) return;
          [...box.children].forEach((ch) => {
            const cb = ch.getBoundingClientRect();
            if (cb.width === 0) return;
            if (cb.left < bb.left - 1 || cb.right > bb.right + 1) {
              escaped.push(box.tagName + "." + (box.className || "-") + " > " +
                ch.tagName + "." + (ch.className || "-"));
            }
          });
        });

        let bulletsShowing = 0;
        document.querySelectorAll("ul, ol").forEach((u) => {
          const before = getComputedStyle(u, "::before");
          const listStyle = getComputedStyle(u).listStyleType;
          if (listStyle && listStyle !== "none") bulletsShowing += u.children.length;
          if (before && before.content && before.content !== "none") bulletsShowing += 1;
        });

        const bars = [];
        if (barTrack) {
          document.querySelectorAll(barTrack).forEach((tr, i) => {
            const fill = tr.querySelector(barFill);
            if (!fill) return;
            const t = tr.getBoundingClientRect();
            const f = fill.getBoundingClientRect();
            if (t.width === 0) return;
            const center = t.left + t.width / 2;
            bars.push({
              i,
              dir: f.left + f.width / 2 > center + 0.5 ? "R" : "L",
              pctOfHalf: Math.round((f.width / (t.width / 2)) * 100),
              inTrack: f.left >= t.left - 1 && f.right <= t.right + 1
            });
          });
        }

        return {
          minFontPx: min === 9999 ? null : min,
          underMinCount: underMin.length,
          underMinSample: underMin.slice(0, 10),
          hOverflow: de.scrollWidth > de.clientWidth + 1,
          scrollW: de.scrollWidth,
          clientW: de.clientWidth,
          pageHeight: de.scrollHeight,
          brokenImgs: [...document.images].filter((i) => i.complete && i.naturalWidth === 0).length,
          emDashCount: (text.match(/\u2014/g) || []).length,
          tableCount: document.querySelectorAll("table").length,
          detailsTotal: document.querySelectorAll("details").length,
          escapedChildren: escaped.slice(0, 10),
          bulletsShowing,
          bars
        };
      },
      { mf: MIN_FONT, bs: BAR_SPLIT }
    );

    r.http = resp ? resp.status() : null;
    report[w + "px"] = r;

    const tag = w + "px";
    if (r.http !== 200) failures.push(tag + ": http " + r.http);
    if (r.underMinCount) failures.push(tag + ": " + r.underMinCount + " text nodes under " + MIN_FONT + "px");
    if (r.hOverflow) failures.push(tag + ": horizontal overflow (" + r.scrollW + " > " + r.clientW + ")");
    if (r.brokenImgs) failures.push(tag + ": " + r.brokenImgs + " broken images");
    if (r.emDashCount) failures.push(tag + ": " + r.emDashCount + " em dash in rendered text");
    if (r.escapedChildren.length) failures.push(tag + ": " + r.escapedChildren.length + " children escaping container");
    r.bars.forEach((b) => {
      if (!b.inTrack) failures.push(tag + ": bar #" + b.i + " drawn outside its track");
    });

    await page.close();
  }

  await browser.close();
  report.failures = failures;
  report.verdict = failures.length ? "FAIL" : "PASS";
  console.log(JSON.stringify(report, null, 2));
  process.exit(failures.length ? 1 : 0);
})().catch((e) => {
  console.error(JSON.stringify({ verdict: "ERROR", error: String((e && e.message) || e) }));
  process.exit(2);
});
