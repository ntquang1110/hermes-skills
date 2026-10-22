/* Kiểm tra tab switching + render bảng + console error trên trang đã publish. */
const { chromium } = require('playwright-core');

const CHROME = "C:/Users/NTQUANG_DELL/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe";
const URL = process.argv[2] || 'https://preview.thefirstonly.com/hcg4mx9ziuhw';

function countTables() {
  return document.querySelectorAll('.panel.on table').length;
}

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });

  await page.goto(URL, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(1200);

  const step = async (label) => {
    const r = await page.evaluate(() => {
      const on = document.querySelector('.panel.on');
      const btns = Array.from(document.querySelectorAll('.tab-btn'));
      return {
        activePanel: on ? on.id : null,
        activeBtn: (document.querySelector('.tab-btn.on') || {}).getAttribute
          ? document.querySelector('.tab-btn.on').getAttribute('data-tab') : null,
        activeTables: on ? on.querySelectorAll('table').length : 0,
        activeSections: on ? on.querySelectorAll('section').length : 0,
        activeWords: on ? (on.innerText || '').trim().split(/\s+/).filter(Boolean).length : 0,
        activeVisible: on ? (on.offsetHeight > 0 && getComputedStyle(on).display !== 'none') : false,
        btnCount: btns.length,
        btnLabels: btns.map(b => b.textContent.trim()),
        roles: btns.map(b => b.getAttribute('role')),
        fontsLoaded: {
          bricolage: document.fonts.check('800 24px "Bricolage Grotesque"'),
          beVietnam: document.fonts.check('400 16px "Be Vietnam Pro"'),
        },
        bodyBg: getComputedStyle(document.body).backgroundColor,
        hOverflow: document.documentElement.scrollWidth > window.innerWidth,
      };
    });
    console.log(label, JSON.stringify(r, null, 1));
    return r;
  };

  console.log('=== TẢI TRANG ===');
  const a = await step('dehieu:');
  console.log('  errors sau load:', errors.length ? errors : '(không có)');

  console.log('\n=== CLICK TAB CHI TIẾT ===');
  await page.click('.tab-btn[data-tab="chitiet"]');
  await page.waitForTimeout(700);
  const b = await step('chitiet:');
  console.log('  errors:', errors.length ? errors : '(không có)');

  console.log('\n=== CLICK LẠI TAB DỄ HIỂU ===');
  await page.click('.tab-btn[data-tab="dehieu"]');
  await page.waitForTimeout(700);
  const c = await step('dehieu2:');

  console.log('\n=== KẾT LUẬN ===');
  const checks = [
    ['tab button có 2', a.btnCount === 2],
    ['tab 1 active khi tải', a.activePanel === 'tab-dehieu' && a.activeBtn === 'dehieu'],
    ['bấm CHI TIẾT -> panel đổi', b.activePanel === 'tab-chitiet' && b.activeBtn === 'chitiet'],
    ['CHI TIẾT có bảng render', b.activeTables > 0],
    ['CHI TIẾT có >1500 chữ', b.activeWords > 1500],
    ['bấm DỄ HIỂU -> đổi lại', c.activePanel === 'tab-dehieu'],
    ['DỄ HIỂU có bảng render', c.activeTables > 0],
    ['DỄ HIỂU có >800 chữ', c.activeWords > 800],
    ['font Bricolage load', a.fontsLoaded.bricolage],
    ['font Be Vietnam Pro load', a.fontsLoaded.beVietnam],
    ['nền cream', a.bodyBg === 'rgb(252, 250, 245)'],
    ['không overflow ngang', a.hOverflow === false && b.hOverflow === false],
    ['không lỗi JS', errors.length === 0],
  ];
  let pass = 0;
  checks.forEach(([k, v]) => { console.log((v ? '  OK   ' : '  FAIL ') + k); if (v) pass++; });

  console.log('\n=== KIỂM TRA STICKY ===');
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(600);
  const sticky = await page.evaluate(() => {
    const t = document.querySelector('.tabbar');
    const r = t.getBoundingClientRect();
    return {
      cssPosition: getComputedStyle(t).position,
      cssTop: getComputedStyle(t).top,
      viewportTop: Math.round(r.top),
      height: Math.round(r.height),
      inlineStyle: t.getAttribute('style') || '(không có)',
      visibleAtBottom: r.top >= 0 && r.top < window.innerHeight,
    };
  });
  console.log(' ', JSON.stringify(sticky));
  const stickyOk = sticky.cssPosition === 'sticky' && sticky.cssTop === '0px'
    && sticky.viewportTop === 0 && sticky.visibleAtBottom;
  console.log((stickyOk ? '  OK   ' : '  FAIL ') + 'thanh tab dính đỉnh viewport khi cuộn xuống đáy');
  if (stickyOk) pass++;
  checks.push(['thanh tab sticky top:0', stickyOk]);

  console.log(`\n>>> ${pass}/${checks.length} đạt`);

  console.log('\n=== ẢNH CHỤP ===');
  await page.screenshot({ path: 'shots/manna-dehieu.png', fullPage: false });
  await page.click('.tab-btn[data-tab="chitiet"]');
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'shots/manna-chitiet.png', fullPage: false });
  const mob = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await mob.goto(URL, { waitUntil: 'networkidle', timeout: 60000 });
  await mob.waitForTimeout(900);
  await mob.screenshot({ path: 'shots/manna-mobile.png', fullPage: false });
  console.log('  đã lưu shots/manna-dehieu.png, manna-chitiet.png, manna-mobile.png');

  await browser.close();
  process.exit(pass === checks.length ? 0 : 1);
})().catch(e => { console.error('SCRIPT ERROR:', e.message); process.exit(2); });
