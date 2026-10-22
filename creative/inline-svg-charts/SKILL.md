---
name: inline-svg-charts
description: "Use when charting data in published HTML (SVG)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [html, svg, chart, data-viz, mobile, publish, verification]
    related_skills: [diagram-catalog, publish, executive-visual-report, html-interactive-dashboard]
---

# Biểu đồ SVG nội tuyến trong trang HTML publish

Dùng khi biểu đồ phải **nằm trong chính trang HTML** (một file, publish lên preview, mở trên điện thoại
của người quyết định) và dữ liệu là số thật do model sinh ra. Khác `matplotlib` (ra PNG, không co theo
khung, không sửa được nhãn sau khi chụp) và khác `diagram-design` (vẽ sơ đồ, không vẽ dữ liệu).

Chọn đường này khi cần: nhiều chuỗi trên cùng một trục, nhãn trục phải là số tròn đọc được, chú thích
màu khớp với đường, và trang phải đọc được trên điện thoại ở khổ 320 px.

## Luật gốc: chữ trong SVG CO THEO SVG

Đây là lỗi số một và nó không tự lộ ra khi xem trên desktop.

`<svg viewBox="0 0 360 250" class="chart">` với `.chart{width:100%}` thì mọi `font-size` trong SVG là
**đơn vị viewBox, không phải px**. Hệ số co = `bề rộng khung chứa / bề rộng viewBox`.

Quy tắc: `font_units × (khung_hẹp_nhất / viewBox_width) ≥ 12 px`.

Kinh nghiệm đã đo thật, viewBox rộng 360, khung chứa 264–360 px (điện thoại 320 px):

| font_units | khung 264 | khung 300 | khung 360 | desktop |
|---|---|---|---|---|
| 14 | 10,3 px ✗ | 11,7 ✗ | 14 ✓ | 14 |
| 19 | 13,9 ✓ | 15,8 ✓ | 19 ✓ | 19 |
| 20 | 14,7 ✓ | 16,7 ✓ | 20 ✓ | 20 |

Chọn **viewBox rộng bằng đúng `max-width` desktop của biểu đồ** (ví dụ 360) để hệ số co trên desktop = 1,
rồi đặt font 19–20 đơn vị. Đừng đặt viewBox 720 rồi font 16: desktop đẹp nhưng điện thoại còn 7 px.

### Cắt thêm bề rộng cho biểu đồ trên điện thoại

Trong `@media (max-width:430px)`, cho biểu đồ tràn ra khỏi padding của card thay vì bó trong đó —
mỗi bên lấy lại ~11 px, đủ để hệ số co vượt 12 px:

```css
@media (max-width:430px){
  .wrap{padding-left:10px;padding-right:10px;}
  .chart{max-width:none;width:calc(100% + 22px);margin-left:-11px;}
}
```

## Verify bằng cách bơm CSS, không cần đổi viewport

Không resize được cửa sổ trình duyệt thì **bơm một thẻ `<style>` mô phỏng đúng luật mobile rồi đo**.
Cách này cho số thật, nhanh hơn dựng trang iframe:

```js
const st = document.createElement('style');
st.textContent = `.wrap{max-width:280px!important;padding-left:10px!important;padding-right:10px!important}` +
                 `.chart{max-width:none!important;width:calc(100% + 22px)!important;margin-left:-11px!important}`;
document.head.appendChild(st);
const s = document.querySelector('svg.chart');
const scale = s.getBoundingClientRect().width / 360;   // 360 = viewBox width
const tick_px = 20 * scale;                            // 20 = font_units
st.remove();
```

Lặp cho 280 / 300 / 340 px. Đo kèm:

```js
document.documentElement.scrollWidth === document.documentElement.clientWidth   // không tràn ngang
Math.min(...[...document.querySelectorAll('p,li,span,b,h1,h2,h3,h4')]
  .map(e => parseFloat(getComputedStyle(e).fontSize)))                          // chữ HTML ≥ 12px
document.querySelectorAll('svg.chart path').length                              // số path = số chuỗi
```

**Render mobile thật để chụp ảnh:** publish một trang bọc chứa `<iframe src="<link preview>"
width="360" height="1500">`. Media query bên trong iframe tính theo viewport của iframe, nên đây là bố
cục mobile thật. Khác origin nên **không đo được DOM bên trong** — chỉ dùng để chụp và soi bằng mắt.

## Nhãn trục phải là số tròn

Chia đều `(ymax-ymin)/4` sẽ ra 62 / 70,5 / 79 / 87,5 / 96. Làm thang bước rồi floor/ceil hai đầu:

```python
def _buoc(dai, n=4):
    for b in (0.1, 0.2, 0.5, 1, 2, 2.5, 5, 10, 15, 20, 25, 30, 50, 100):
        if b >= dai / n:
            return b
    return 100

b = _buoc(ymax - ymin)
ymin, ymax = math.floor(ymin / b) * b, math.ceil(ymax / b) * b
```

Trong thang **phải có 15 và 30**: thiếu chúng thì dải 0–104 nhảy lên bước 50 và ra 0/50/100/150, hoặc
dải vừa qua 20 ra bước 30 và lệch cả hình.

Kiểm ngay: nếu biểu đồ có một chuỗi mà điểm thấp nhất là 0 (ví dụ nhánh bị ép ngân sách, E = 0) thì
`ymin` phải bằng 0, không được để 30 — nếu không điểm đó bị vẽ ra ngoài khung và đè lên nhãn trục ngang.

## Ba chuỗi trên một trục: màu + kiểu nét

Ba sắc gần nhau là không đủ (in đen trắng, người mù màu). Dùng đồng thời màu và kiểu nét:

```python
{"lien": "", "dash": ' stroke-dasharray="7 5"', "dot": ' stroke-dasharray="2 5"'}
```

Chú thích phải khớp kiểu nét, không chỉ khớp màu:

```python
def _o_mau(c, k):
    if k == "dash": return f'background:repeating-linear-gradient(90deg,{c} 0 5px,transparent 5px 9px)'
    if k == "dot":  return f'background:repeating-linear-gradient(90deg,{c} 0 2px,transparent 2px 5px)'
    return f'background:{c}'
```

Điểm đến từ **cách giải khác** (nghiệm phủ tập hợp trong khi đường cong do leo dốc) thì vẽ bằng vòng
tròn rỗng ở màu riêng, một ký hiệu riêng trong chú thích. Đây là chỗ dễ giấu bất đồng nhất giữa hai
cách giải nhất, và giấu đi là tự làm hỏng độ tin của cả trang.

## Biểu đồ cột thì đừng dùng SVG

Cột ngang cho vài giá trị (biên giá trị mỗi kg, tỉ lệ đạt) làm bằng `div` + `width: %` + flex/grid:
không có chữ nào bị co, không phải canh nhãn, tự xuống dòng trên điện thoại. Chỉ dùng SVG khi cần
đường cong hoặc trục toạ độ thật.

## Publish và verify lại sau khi publish

1. Dựng file → publish bằng `content-upload.py` của skill `publish` (script nằm trong
   `<thư mục skill publish>/scripts/content-upload.py`; đọc thẳng file SKILL.md có thể ra ký tự lạ,
   cứ chạy script).
2. Tải lại link preview **rồi đo lại** `scrollWidth`, số `svg.chart`, số `path`, `font-size` — bước
   unslop của uploader có thể sửa HTML sau khi mình kiểm.
3. Ghi link đã publish vào tài liệu nguồn (kèm tên script sinh ra trang) để lần sau không dựng lại từ đầu.

## Checklist

- [ ] `font_units × (khung_hẹp_nhất / viewBox_width) ≥ 12` — đã đo, không đoán
- [ ] `viewBox width` = `max-width` desktop của biểu đồ
- [ ] Media query ≤ 430 px: chữ HTML ≥ 12 px, biểu đồ tràn padding, không tràn ngang
- [ ] Nhãn trục là số tròn; chuỗi có điểm 0 thì `ymin = 0`
- [ ] Mỗi chuỗi có kiểu nét riêng; chú thích khớp cả màu và nét
- [ ] Điểm từ cách giải khác có ký hiệu riêng
- [ ] Đã đo lại trên link đã publish, không chỉ trên file local
