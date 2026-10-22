# Google Forms — Full Structure Extraction (FB_PUBLIC_LOAD_DATA_)

Dùng khi user gửi link Google Forms (forms.gle / docs.google.com/forms) và yêu cầu
điền hộ, trải phẳng câu hỏi để duyệt, hoặc dựng HTML draft.
Đã verify trên form TECHFEST 2026 (94 items, 12 sections).

## Cách dump (browser session đã sign-in, đang ở viewform/formResponse)

OAuth Bearer token KHÔNG dùng được cho viewform (401 redirect login); Forms API
`forms.googleapis.com` trả 403 nếu project chưa bật. Phải đọc
`FB_PUBLIC_LOAD_DATA_` qua `browser_console`, chia lệnh nhỏ (gộp nhiều bước dễ
500 Internal Error).

```js
// 1. Kiểm tra data
typeof FB_PUBLIC_LOAD_DATA_  // phải trả về "object"

// 2. Đếm items ([1][1] là mảng items)
JSON.stringify(FB_PUBLIC_LOAD_DATA_[1][1].length)
```

```js
// 3. Liệt kê sections + câu hỏi
const d = FB_PUBLIC_LOAD_DATA_[1][1];
let result = [];
for (let i = 0; i < d.length; i++) {
  const item = d[i];
  if (!item || !Array.isArray(item)) continue;
  const type = item[3];
  const title = item[1] || '';
  if (type === 6 || type === 8) { result.push('=== ' + title + ' ==='); continue; }
  const typeNames = {0:'text',1:'paragraph',2:'radio',3:'checkbox',4:'dropdown',5:'date',7:'scale',9:'file',10:'video',13:'file-upload'};
  const required = item[4] && item[4][0] && item[4][0][2] ? ' *' : '';
  result.push(`[${typeNames[type]||type}]${required} ${title.substring(0,120)}`);
}
JSON.stringify(result.join('\n')).substring(0, 10000)
```

```js
// 4. Options của dropdown/radio/checkbox
const d = FB_PUBLIC_LOAD_DATA_[1][1];
let out = [];
for (let i = 0; i < d.length; i++) {
  const item = d[i];
  if (!item || !Array.isArray(item)) continue;
  if (item[3] === 6 || item[3] === 8) continue;
  const details = item[4] || [];
  if (details[0] && details[0][1] && Array.isArray(details[0][1]) && details[0][1].length) {
    out.push('Q: ' + (item[1]||'').substring(0,60)
      + ' → ' + details[0][1].map(o => Array.isArray(o) ? o[0] : o).join(' | ').substring(0,200));
  }
}
JSON.stringify(out.join('\n')).substring(0, 10000)
```

```js
// 5. Help text / giới hạn ký tự (item[2])
const d = FB_PUBLIC_LOAD_DATA_[1][1];
let desc = [];
for (let i = 0; i < d.length; i++) {
  const item = d[i];
  if (!item || !Array.isArray(item)) continue;
  if (item[3] === 6 || item[3] === 8) continue;
  if (item[2] && item[2].length) desc.push('Q: ' + (item[1]||'').substring(0,60) + '\n  DESC: ' + item[2].substring(0,200));
}
JSON.stringify(desc.join('\n\n')).substring(0, 10000)
```

## Type map (đã verify)

| item[3] | Nghĩa | Ghi chú |
|---|---|---|
| 6, 8 | Section header | 8 là section không mô tả, vẫn coi là header |
| 0 | text ngắn | |
| 1 | paragraph dài, giới hạn chars nằm trong item[2] | |
| 2 | radio | options ở item[4][0][1] |
| 3 | checkbox | |
| 4 | dropdown | |
| 5 / 13 | date / file-upload | file-upload có giới hạn MB + định dạng trong item[2] |

## Pitfalls (đã gặp thật, session TECHFEST 2026)

- **`browser_type` timeout ở ô password Google** (`Read timed out localhost:9377`).
  Đổi sang `browser_console`: gán trực tiếp `input[type="password"].value` +
  dispatch `input` event rồi click nút Next.
- **Radio/checkbox bị đảo trạng thái khi click lại.** Sau mỗi click, snapshot lại
  xác nhận `[checked]` đúng ý trước khi Next. Không click mù nhiều lần.
- **Draft form tự lưu theo account.** Điền thử để lướt page sẽ để lại draft trên
  account user. Nói rõ đây là draft thăm dò, chưa submit.
