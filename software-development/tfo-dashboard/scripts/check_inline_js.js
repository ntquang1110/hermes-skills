#!/usr/bin/env node
/**
 * check_inline_js.js — kiểm tra cú pháp toàn bộ <script> inline trong file HTML.
 * Bắt lỗi JS trước khi deploy mà không cần mở browser.
 *
 * Dùng:
 *   node check_inline_js.js app/static/index.html
 *   node check_inline_js.js app/static/index.html app/static/guide.html   (nhiều file)
 *
 * Exit code: 0 = tất cả OK, 1 = có lỗi cú pháp.
 * Lưu ý: chỉ bắt SyntaxError lúc parse — lỗi runtime (undefined function, typo trong
 * template string) phải verify bằng browser console.
 */
const fs = require('fs');

function checkFile(file) {
  let html;
  try {
    html = fs.readFileSync(file, 'utf8');
  } catch (e) {
    console.error(`[${file}] KHÔNG ĐỌC ĐƯỢC: ${e.message}`);
    return 1;
  }
  // Match <script> không có thuộc tính src (inline scripts only)
  const re = /<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;
  const blocks = [];
  let m;
  while ((m = re.exec(html)) !== null) {
    blocks.push(m[1]);
  }
  if (blocks.length === 0) {
    console.log(`[${file}] 0 script inline — bỏ qua`);
    return 0;
  }
  let bad = 0;
  blocks.forEach((code, i) => {
    try {
      // new Function parse toàn bộ body — không thực thi, chỉ bắt SyntaxError
      new Function(code);
      console.log(`[${file}] script ${i} OK`);
    } catch (e) {
      bad++;
      const line = code.slice(0, 200).replace(/\n/g, ' ');
      console.log(`[${file}] script ${i} LỖI: ${e.message}`);
      console.log(`         → ${line}...`);
    }
  });
  console.log(`[${file}] ${blocks.length} script blocks, ${bad} lỗi`);
  return bad ? 1 : 0;
}

const files = process.argv.slice(2);
if (files.length === 0) {
  console.error('Dùng: node check_inline_js.js <file.html> [file2.html ...]');
  process.exit(2);
}
let code = 0;
for (const f of files) {
  const c = checkFile(f);
  if (c !== 0) code = c;
}
process.exit(code);
