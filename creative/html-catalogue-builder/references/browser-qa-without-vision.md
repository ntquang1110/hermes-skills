# QA trang web bằng console khi không chụp ảnh được

Khi công cụ chụp ảnh trang không chạy (vision backend hết quota, endpoint model 404,
Camofox không đọc được file), **đừng dừng**. Mọi thứ cần kiểm về bố cục đều đo
được bằng JavaScript trả về JSON.

Cách dùng: dán vào `browser_console` với `expression`, hoặc nhúng thành một
probe tự chạy khi QA tự động.

## Bố cục

```js
JSON.stringify({
  docW: document.documentElement.scrollWidth,
  winW: window.innerWidth,
  hOverflow: document.documentElement.scrollWidth > window.innerWidth + 2,
  cards: document.querySelectorAll('.card').length,
  overWideCards: [...document.querySelectorAll('.card')]
    .filter(c => c.scrollWidth > c.clientWidth + 2).length
})
```

- `hOverflow` true: có phần tử tràn ngang, thường là bảng rộng hoặc
  `white-space: nowrap` chưa bọc.
- `overWideCards` > 0: thẻ con tràn ra ngoài thẻ cha, thường do chuỗi dài
  không có `word-break`.

## Mọi tab phải bấm được và trả số đúng

```js
(function(){
  var out = {};
  document.querySelectorAll('.tab').forEach(t => {
    t.click();
    var pane = document.getElementById('pane-' + t.dataset.p);
    out[t.dataset.p] = {
      visible: pane.classList.contains('on'),
      cards: pane.querySelectorAll('.card').length,
      rows: pane.querySelectorAll('tbody tr').length
    };
  });
  return JSON.stringify(out);
})()
```

Số phải khớp số liệu đã chốt ở generator. Lệch là dữ liệu sai.

## Ô tìm kiếm

```js
(function(){
  var q = document.getElementById('q');
  var out = {};
  ['hợp đồng','lao động','thuế','bảo vệ dữ liệu','zzz-khong-co'].forEach(function(t){
    q.value = t; q.dispatchEvent(new Event('input'));
    out[t] = {
      n: document.querySelectorAll('.card').length,
      empty: !!document.querySelector('.empty')
    };
  });
  q.value = ''; q.dispatchEvent(new Event('input'));
  return JSON.stringify(out);
})()
```

Cần thấy:
- từ khoá có dấu ra kết quả (kiểm tra bộ lọc tiếng Việt)
- từ khoá bùa hiện trạng thái rỗng, không trang trắng
- xoá ô tìm thì về đủ tổng số bản ghi

## Bộ lọc viên/chip

```js
(function(){
  var chips = [...document.querySelectorAll('.chip')];
  var out = { count: chips.length, overflow: chips.filter(c=>c.scrollWidth>c.clientWidth+2).length };
  chips.forEach(c => { c.click(); out[c.dataset.g || 'ALL'] = document.querySelectorAll('.card').length; });
  chips[0].click();
  return JSON.stringify(out);
})()
```

## Tiếng Việt còn nguyên

```js
JSON.stringify({
  h1: document.querySelector('h1').textContent,
  hasRawTag: document.body.innerHTML.includes('<script>'),
  amp: document.body.innerHTML.match(/&[a-z]{2,4};/g)?.slice(0,5)
})
```

`hasRawTag` true nghĩa là script chưa được JS render, thường là dữ liệu JSON
nhúng bị lỗi cú pháp. Kiểm tra thêm:

```js
JSON.stringify({
  ready: typeof DATA_READY !== 'undefined' ? DATA_READY.length : 'UNDEF',
  want:  typeof DATA_WANT  !== 'undefined' ? DATA_WANT.length  : 'UNDEF'
})
```

## Dữ liệu nhúng có đúng không

```js
JSON.stringify({
  firstRecord: DATA_READY[0],
  noTags: DATA_READY.filter(x => !x.vi || !x.vi.length).map(x => x.name),
  avgTags: (DATA_READY.reduce((a,x)=>a+(x.vi?x.vi.length:0),0)/DATA_READY.length).toFixed(1)
})
```

`noTags` dài = bảng từ khoá tiếng Việt chưa phủ, tìm kiếm tiếng Việt sẽ hụt.
`avgTags` quá cao (> 8) là bảng khớp rác, phải siết word-boundary.

## Bắt lỗi JS khi backend không trả console

Backend Camofox không trả `console_messages`. Tự bắt:

```js
window.__err = [];
window.addEventListener('error', e => window.__err.push(String(e.message)));
// thao tác xong:
JSON.stringify(window.__err)
```

## Chụp màn hình khi muốn có

`browser_vision` trả `screenshot_path` kèm kết quả. Dùng đường dẫn đó để gửi
ảnh cho anh qua `MEDIA:`. Nếu vision backend lỗi, đừng gọi lại, chỉ tốn thêm
vòng và ra cùng một lỗi.
