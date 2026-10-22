# Legibility & verification cho SVG/diagram trong HTML

Case chứng minh: `fixgby/visual/ban-do-co-che-goc.html` (18/10/2026) — sơ đồ vòng 3 node, preview https://preview.thefirstonly.com/upglf9wtcb8u

Áp dụng khi: HTML có **inline SVG** (sơ đồ vòng/chuỗi/ma trận, dashboard có graphic) và người đọc chính là **điện thoại**.

---

## 1. Vấn đề gốc — viewBox rộng bị ép vào container → chữ co

```
scale      = containerWidth / viewBoxWidth      (px CSS)
chữ thật   = font-size(SVG) × scale
```

Case thật: `viewBox="0 0 940 380"` layout ngang, container nội dung 649px → **scale 0,69** → font 11px hiển thị còn **7,6px**. Không lỗi JS, không thiếu element, `browser_snapshot` trả đủ heading → **pass mọi check thô, nhưng không đọc được trên điện thoại.**

Đây là loại lỗi im lặng: chỉ lộ ra khi ĐO.

## 2. Quy tắc

1. **viewBox width ≤ container width.** Container nội dung trên máy Quang ~650px → giữ **viewBox 600–700** ⇒ scale ≈ 1. viewBox 900–1000+ cho một diagram nhỏ là lỗi, không phải "cho thoáng".
2. **Chữ nhỏ nhất SAU scale ≥ 12px.** Nghĩa là `font-size ≥ 12 / scale`. Với viewBox 620 thì font 12–13px trong SVG là ổn.
3. **Nhiều nhãn → layout DỌC, không xếp ngang.** Chuỗi/vòng 3 node: node xếp trên→dưới cùng `x` (vd x=144), cung quay về đi **bên phải** (x=470), nhãn cạnh đặt lệch phải (x=214) hoặc canhlề-phải (`text-anchor="end"`, x=452). Layout ngang 3 node + nhãn hai bên cần viewBox ≥ 900 → vi phạm quy tắc 1.
4. **Mũi tên phải nổi.** `markerWidth/Height 11`, `refX 9`, `refY 5.5`, fill trùng màu stroke. Trên nền tối (#0D0D0D–#12161b) dùng stroke sáng **#8b9aa8**; xám tối (#39424d, #6d7c8a) bị chìm, vision cũng sẽ phàn nàn đúng.
5. **Chừa ≥ 18px giữa mép phải nhãn và đường kẻ dọc** gần nhất, nếu không nhãn "dính" vào đường.
6. Không dùng `<table>` — Quang yêu cầu **0 bảng**, diagram thay bảng.

## 3. Verify bằng ĐO, không bằng mắt

Sau `browser_navigate(preview_url)`, chạy `browser_console(expression=...)`:

```js
const svg=document.querySelector('svg');
const r=svg.getBoundingClientRect(), vb=svg.viewBox.baseVal;
const scale=r.width/vb.width;
const T=[];
svg.querySelectorAll('text').forEach(t=>{const b=t.getBBox();
  T.push({t:t.textContent.slice(0,20),x1:b.x,x2:b.x+b.width,y1:b.y,y2:b.y+b.height,
          eff:+(parseFloat(getComputedStyle(t).fontSize)*scale).toFixed(1)});});
const col=[];for(let i=0;i<T.length;i++)for(let j=i+1;j<T.length;j++){
  const a=T[i],b=T[j];
  if(a.x1<b.x2&&b.x1<a.x2&&a.y1<b.y2&&b.y1<a.y2)col.push(a.t+' x '+b.t);}
JSON.stringify({scale:+scale.toFixed(2), minEff:Math.min(...T.map(x=>x.eff)),
  maxRight:Math.round(Math.max(...T.map(x=>x.x2))),
  outOfFrame:T.filter(x=>x.x2>vb.width||x.x1<0||x.y2>vb.height||x.y1<0).map(x=>x.t),
  collisions:col, tables:document.querySelectorAll('table').length});
```

Đọc kết quả:

| Chỉ số | Ngưỡng |
|---|---|
| `scale` | ≈ 1 OK · ≤ 0,75 = chữ đang bị co, **sửa viewBox** |
| `minEff` | ≥ 12px (đọc được trên điện thoại) |
| `collisions` | phải **rỗng** |
| `outOfFrame` | phải **rỗng** |
| `maxRight` | cách đường kẻ dọc gần nhất ≥ 18px |
| `tables` | = 0 |

## 4. Cái KHÔNG được làm

- **KHÔNG tin vision model cho hình học.** Case này vision (aux) báo sai 2 lần: (a) **bịa ra nhãn không tồn tại trong file** ("tăng nội nhiệt → thụ thể nhiệt", "nơi giữ lửa được nuôi"); (b) khẳng định 3 node "lệch trục, G3 hơi cao hơn G1" trong khi cả ba cùng `cy="150"` — đo được, thẳng hàng tuyệt đối. Vision chỉ dùng để đánh giá **tương phản / thẩm mỹ**; mọi con số, toạ độ, va chạm phải đo bằng `getBBox()` / `getBoundingClientRect()`.
- **KHÔNG tin "snapshot đủ element + 0 lỗi JS".** Đủ element vẫn có thể vô dụng trên điện thoại. Phải thêm một lượt đo hình học trước khi báo xong.
- **KHÔNG kết luận từ screenshot ở đầu trang.** `browser_vision` chụp viewport hiện tại — phải `scrollIntoView({block:'center'})` lên phần tử cần xem rồi mới chụp, nếu không sẽ soi nhầm section 01 và tưởng diagram sai.

## 5. Vòng publish + verify đã dùng

`content-upload.py --file <html>` → `browser_navigate(preview)` → `browser_console` ĐO → sửa → upload lại → đo lại → mới báo xong.

Case này: 3 lần upload (`fjd93tp0uuc1` → `b9l1ilwwhcb7` → `upglf9wtcb8u`), trong đó **2 lần sửa là do lỗi hình học thật** (viewBox quá rộng; nhãn đè cung; mũi tên thiếu tương phản), không phải do cảm tính. Sửa bằng `patch` replace_all theo từng thuộc tính SVG (`font-size="11.5"` → `"12.5"`, `#6d7c8a` → `#8b9aa8`) nhanh hơn viết lại cả block `svg`.
