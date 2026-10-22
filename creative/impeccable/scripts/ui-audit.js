// UI Audit Detector — deterministic check cho HTML tĩnh, chạy trong browser.
// Cách dùng: browser_navigate tới trang → browser_console với expression = nội dung file này.
// Trả về JSON: url, tells (mảng AI-tells), fonts, radii, headings, bodyContrast, stats.
// Đây là bản "detector rules" nhẹ của impeccable — không cần node, không cần CLI.
(() => {
  const res = { url: location.href, tells: [], fonts: new Set(), radii: new Set(), headings: {}, stats: {} };

  // ── Fonts + AI-tells qua computed style ──
  document.querySelectorAll('*').forEach(el => {
    const cs = getComputedStyle(el);
    const fs = cs.fontFamily;
    if (fs) res.fonts.add(fs.split(',')[0].replace(/["']/g, '').trim());
    // gradient text
    if (cs.backgroundImage.includes('gradient') && cs.webkitBackgroundClip === 'text') res.tells.push('gradient-text');
    // glassmorphism: backdrop-filter thật (chỉ coi là tell khi dùng trang trí)
    if (cs.backdropFilter && cs.backdropFilter !== 'none') res.tells.push('glassmorphism');
    // hard offset shadow (zero blur, offset > 2px)
    const sh = cs.boxShadow;
    if (sh && sh !== 'none') {
      const m = sh.match(/(\d+)px (\d+)px 0px/);
      if (m && Math.max(+m[1], +m[2]) > 2) res.tells.push('hard-offset-shadow');
    }
    // border-radius spread
    const r = cs.borderRadius;
    if (r && r !== '0px') res.radii.add(r);
  });

  // ── Emoji thay icon system (glyph-icons rule) ──
  const emojiRe = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u;
  let emojiCount = 0;
  document.querySelectorAll('button, .icon, [class*=icon], nav a, li a').forEach(el => {
    if (emojiRe.test(el.textContent)) emojiCount++;
  });
  if (emojiCount > 3) res.tells.push(`emoji-icons:${emojiCount}`);

  // ── Headings hierarchy ──
  res.headings = {
    h1: document.querySelectorAll('h1').length,
    h2: document.querySelectorAll('h2').length,
    h3: document.querySelectorAll('h3').length,
  };
  if (res.headings.h1 > 0 && res.headings.h2 === 0) res.tells.push('flat-type-hierarchy:h1-only');

  // ── Overused font (system face làm display voice) ──
  const fonts = [...res.fonts];
  const sysFaces = ['system-ui', 'Segoe UI', '-apple-system', 'BlinkMacSystemFont', 'Arial'];
  const hasSysOnly = fonts.length > 0 && fonts.every(f => sysFaces.includes(f));
  if (hasSysOnly) res.tells.push(`overused-font:${fonts.join(',')}`);

  // ── Contrast body text vs bg (approx WCAG) ──
  const b = getComputedStyle(document.body);
  res.bodyBg = b.backgroundColor;
  res.bodyColor = b.color;
  function lum(rgb) {
    const p = rgb.match(/[\d.]+/g).slice(0, 3).map(v => { v = +v / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); });
    return 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2];
  }
  try {
    const L1 = lum(b.color), L2 = lum(b.backgroundColor);
    res.bodyContrast = ((Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05)).toFixed(2);
    if (res.bodyContrast < 4.5) res.tells.push(`low-contrast-body:${res.bodyContrast}`);
  } catch (e) { res.bodyContrast = 'n/a'; }

  res.radii = [...res.radii].slice(0, 8);
  res.fonts = fonts.slice(0, 8);
  res.tells = [...new Set(res.tells)];
  res.stats = {
    elements: document.querySelectorAll('*').length,
    buttons: document.querySelectorAll('button').length,
    links: document.querySelectorAll('a').length,
  };
  return JSON.stringify(res);
})()
