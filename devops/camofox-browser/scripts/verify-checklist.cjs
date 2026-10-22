/* Verify checklist hồ sơ tăng vốn: render, tích chọn, tiến độ, filter, search, lưu trữ, tab. */
const { chromium } = require("playwright-core");
const CHROME = "C:/Users/NTQUANG_DELL/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe";
const URL = process.argv[2];

(async () => {
  const b = await chromium.launch({ executablePath: CHROME });
  const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
  const p = await ctx.newPage();
  const errors = [];
  p.on("pageerror", e => errors.push("pageerror: " + e.message));
  p.on("console", m => { if (m.type() === "error") errors.push("console: " + m.text()); });

  await p.goto(URL, { waitUntil: "networkidle", timeout: 60000 });
  await p.waitForTimeout(1200);

  const snap = () => p.evaluate(() => {
    const on = document.querySelector(".panel.on");
    return {
      panel: on ? on.id : null,
      groups: document.querySelectorAll("#groups .grp").length,
      items: document.querySelectorAll("#groups .item").length,
      checked: document.querySelectorAll('#groups input[type=checkbox]:checked').length,
      pDone: (document.getElementById("pDone") || {}).textContent,
      pTotal: (document.getElementById("pTotal") || {}).textContent,
      pPct: (document.getElementById("pPct") || {}).textContent,
      fillW: (document.getElementById("pFill") || {}).style ? document.getElementById("pFill").style.width : null,
      mini: document.querySelectorAll(".mini-c").length,
      chipAll: (document.getElementById("cAll") || {}).textContent,
      chipDone: (document.getElementById("cDone") || {}).textContent,
      chipPend: (document.getElementById("cPend") || {}).textContent,
      bodyText: (on ? on.innerText : "").slice(0, 400),
      hasNaN: /\bNaN\b/.test(on ? on.innerText : ""),
      lsKeys: Object.keys(localStorage).length,
    };
  });

  console.log("=== 1. TẢI TRANG (tab Checklist) ===");
  let s = await snap();
  console.log(JSON.stringify(s, null, 1));

  console.log("\n=== 2. TÍCH 5 HẠNG MỤC ĐẦU ===");
  for (let i = 0; i < 5; i++) {
    // người dùng bấm vào ô vuông (label), không bấm thẳng input ẩn
    await p.locator('#groups label.cb').nth(i).click();
    await p.waitForTimeout(150);
  }
  const cbState = await p.evaluate(() => Array.from(
    document.querySelectorAll('#groups input[type=checkbox]')).slice(0,6).map(e => e.checked));
  console.log('  trạng thái 6 ô đầu:', JSON.stringify(cbState));
  s = await snap();
  console.log("  đã tích:", s.checked, "| hiển thị:", s.pDone + "/" + s.pTotal, "|", s.pPct, "| fill:", s.fillW);
  console.log("  chip: tất cả", s.chipAll, "| đã xong", s.chipDone, "| chưa xong", s.chipPend);
  console.log("  NaN trong giao diện:", s.hasNaN);
  console.log("  localStorage keys:", s.lsKeys);

  console.log("\n=== 3. RELOAD — có nhớ không ===");
  await p.reload({ waitUntil: "networkidle" });
  await p.waitForTimeout(1000);
  s = await snap();
  console.log("  sau reload đã tích:", s.checked, "|", s.pDone + "/" + s.pTotal, "|", s.pPct);
  const persisted = s.checked === 5;

  console.log("\n=== 4. NHẬP THỜI HẠN + GHI CHÚ ===");
  await p.locator('[data-tog]').first().click();
  await p.waitForTimeout(250);
  await p.locator('[data-dl]').first().fill("05 ngày làm việc từ T0");
  await p.locator('[data-nt]').first().fill("đã nhận bản gốc 08/10");
  await p.waitForTimeout(300);
  await p.reload({ waitUntil: "networkidle" });
  await p.waitForTimeout(900);
  const savedFields = await p.evaluate(() => {
    const raw = localStorage.getItem("manna_agt_checklist_v1");
    const o = raw ? JSON.parse(raw) : {};
    return { dl: (o.deadline || {})["i1"], nt: (o.note || {})["i1"] };
  });
  console.log("  thời hạn đã lưu:", JSON.stringify(savedFields.dl));
  console.log("  ghi chú đã lưu:", JSON.stringify(savedFields.nt));

  console.log("\n=== 5. FILTER ===");
  await p.locator('.chip[data-f="done"]').click();
  await p.waitForTimeout(350);
  const doneN = await p.evaluate(() => document.querySelectorAll("#groups .item").length);
  await p.locator('.chip[data-f="pending"]').click();
  await p.waitForTimeout(350);
  const pendN = await p.evaluate(() => document.querySelectorAll("#groups .item").length);
  await p.locator('.chip[data-f="all"]').click();
  await p.waitForTimeout(350);
  const allN = await p.evaluate(() => document.querySelectorAll("#groups .item").length);
  console.log("  đã xong:", doneN, "| chưa xong:", pendN, "| tất cả:", allN);
  const filterOk = doneN === 5 && pendN === 24 && allN === 29;

  console.log("\n=== 6. SEARCH ===");
  await p.locator("#q").fill("sáng chế");
  await p.waitForTimeout(500);
  const s1 = await p.evaluate(() => document.querySelectorAll("#groups .item").length);
  await p.locator("#q").fill("dieu le");
  await p.waitForTimeout(500);
  const s2 = await p.evaluate(() => document.querySelectorAll("#groups .item").length);
  await p.locator("#q").fill("zzzzz");
  await p.waitForTimeout(500);
  const s3 = await p.evaluate(() => document.querySelectorAll("#groups .item").length);
  const emptyShown = await p.evaluate(() => getComputedStyle(document.getElementById("empty")).display !== "none");
  await p.locator("#q").fill("");
  await p.waitForTimeout(500);
  console.log("  'sáng chế':", s1, "| 'dieu le' (không dấu):", s2, "| 'zzzzz':", s3);
  console.log("  thông báo rỗng hiện:", emptyShown);
  const searchOk = s1 > 0 && s2 > 0 && s3 === 0 && emptyShown;

  console.log("\n=== 7. TAB THAM CHIẾU ===");
  await p.locator('.tab-btn[data-tab="thamchieu"]').click();
  await p.waitForTimeout(600);
  const ref = await p.evaluate(() => ({
    panel: document.querySelector(".panel.on").id,
    principles: document.querySelectorAll("#refPrinciples li").length,
    issues: document.querySelectorAll("#refIssues li").length,
    milestones: document.querySelectorAll("#refMilestones .ms-row").length,
    notes: document.querySelectorAll("#refNotes .note").length,
    words: document.querySelector(".panel.on").innerText.trim().split(/\s+/).length,
  }));
  console.log(JSON.stringify(ref));
  await p.locator('.tab-btn[data-tab="checklist"]').click();
  await p.waitForTimeout(500);
  const back = await p.evaluate(() => document.querySelector(".panel.on").id);

  console.log("\n=== 8. STICKY + OVERFLOW ===");
  await p.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await p.waitForTimeout(600);
  const st = await p.evaluate(() => {
    const t = document.querySelector(".tabbar");
    const r = t.getBoundingClientRect();
    return { pos: getComputedStyle(t).position, top: getComputedStyle(t).top, vt: Math.round(r.top),
             hOverflow: document.documentElement.scrollWidth > window.innerWidth };
  });
  console.log("  desktop:", JSON.stringify(st));

  const mob = await ctx.newPage();
  await mob.setViewportSize({ width: 390, height: 844 });
  await mob.goto(URL, { waitUntil: "networkidle", timeout: 60000 });
  await mob.waitForTimeout(1000);
  const mo = await mob.evaluate(() => {
    const bad = [];
    document.querySelectorAll("body *").forEach(e => {
      const r = e.getBoundingClientRect();
      if (r.width > 0 && r.right > window.innerWidth + 1) bad.push(e.className || e.tagName);
    });
    return {
      hOverflow: document.documentElement.scrollWidth > window.innerWidth,
      overflowing: bad.slice(0, 6),
      items: document.querySelectorAll("#groups .item").length,
      tabBtns: document.querySelectorAll(".tab-btn").length,
    };
  });
  console.log("  mobile:", JSON.stringify(mo));

  console.log("\n=== ẢNH CHỤP ===");
  await p.locator('.chip[data-f="all"]').click();
  await p.waitForTimeout(300);
  await p.screenshot({ path: "shots/ck-desktop.png" });
  await mob.screenshot({ path: "shots/ck-mobile.png" });
  await p.locator('.tab-btn[data-tab="thamchieu"]').click();
  await p.waitForTimeout(500);
  await p.screenshot({ path: "shots/ck-thamchieu.png" });
  console.log("  đã lưu shots/ck-desktop.png, ck-mobile.png, ck-thamchieu.png");

  console.log("\n=== KẾT LUẬN ===");
  const checks = [
    ["7 nhóm render", s.groups === 7],
    ["29 hạng mục render", allN === 29],
    ["tổng đúng 29", s.pTotal === "29"],
    ["tích chọn -> tiến độ nhảy", s.checked === 5],
    ["thanh tiến độ có width", s.fillW && s.fillW !== "0%" && s.fillW !== ""],
    ["lưu qua reload", persisted],
    ["lưu thời hạn", !!savedFields.dl],
    ["lưu ghi chú", !!savedFields.nt],
    ["filter đúng số", filterOk],
    ["search + không dấu + rỗng", searchOk],
    ["tab tham chiếu đủ 4 mục", ref.principles === 4 && ref.issues === 10 && ref.milestones === 5 && ref.notes === 2],
    ["đổi tab về được", back === "tab-checklist"],
    ["không NaN", !s.hasNaN],
    ["sticky top 0", st.pos === "sticky" && st.top === "0px" && st.vt === 0],
    ["không overflow desktop", st.hOverflow === false],
    ["không overflow mobile", mo.hOverflow === false && mo.overflowing.length === 0],
    ["không lỗi JS", errors.length === 0],
  ];
  let pass = 0;
  checks.forEach(([k, v]) => { console.log((v ? "  OK   " : "  FAIL ") + k); if (v) pass++; });
  console.log("\n>>> " + pass + "/" + checks.length + " đạt");
  if (errors.length) console.log("\nLỖI:", errors.slice(0, 6));

  await b.close();
  process.exit(pass === checks.length ? 0 : 1);
})().catch(e => { console.error("SCRIPT ERROR:", e.message); process.exit(2); });
