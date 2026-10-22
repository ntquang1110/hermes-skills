# Inline diagram QA — verify hình học, không chỉ cấu trúc (verified 18/10/2026)

Case gốc: HTML giải thích vật lý hạt nhân (rào cản Coulomb, thang năng lượng eV/MeV, lưới 118 nguyên tố).
File validate **sạch**: `size 29530`, `sec 8/8`, `div` cân bằng, `table` cân bằng, `CJK none`, `has_diacritics True`, `mojibake 0`, `HTTP 200`.
Nhưng `browser_vision` vẫn bắt được **label "RÀO CẢN" đè lên nét cung đỏ** và caption đỏ trên nền hồng không đọc được.

**Bài học:** cấu trúc đúng ≠ hình đúng. Đây là lớp lỗi mà grep/DOM-audit KHÔNG BAO GIỜ bắt được.

## Loop 5 bước

```
publish → browser_navigate(preview_url)
        → browser_console("document.querySelector('.TARGET').scrollIntoView({block:'center'})")
        → browser_vision(question = hỏi TỪNG label một)
        → patch CSS
        → publish lại → verify lại
```

`scrollIntoView({block:'center'})` là mấu chốt: ảnh chụp mặc định chỉ thấy đầu trang, biểu đồ nằm giữa file thì phải tự cuộn tới trước khi gọi `browser_vision`.

## Hỏi gì trong browser_vision

Hỏi **từng phần tử cụ thể**, không hỏi chung "trang này ổn không":

> "Label X có đè lên nét cong/đường kẻ không? Chữ Y có đọc được trên nền màu đó không? Có phần nào bị cắt (clipping) không?"

Câu trả lời dạng "chip nằm rõ phía trên cung, có khoảng hở" hoặc "text mờ, tương phản kém" mới hành động được.
Hỏi chung chung thì model chỉ trả "trang render tốt" và mình publish luôn bản lỗi.

## Fix chuẩn cho label chip đè hình

| Lỗi | Fix |
|---|---|
| Chip `top:-Npx` đè lên đỉnh cung/nét | Cho chip **nền đặc + viền**, đẩy ra ngoài hình, tăng `margin-top` của container để chip có chỗ |
| Chữ trần (không nền) trên vùng tint nhạt | Bọc thành chip: `background: cream; border: 1.5px solid <tương phản>; padding: 3px 12px` |
| Nhiều label tranh nhau một vùng | Mỗi label **một dải dọc riêng** (trên / giữa / dưới). Đừng để hai label cùng dải |
| Chip tràn xuống block dưới | Tăng `margin-bottom` container bằng đúng phần tràn (`bottom:-40px` → cần ≥ 50px) |
| Vỡ trên mobile | Override lại toàn bộ offset trong `@media(max-width:620px)`: giảm font chip, giảm `bottom`, thu nhỏ hình |

Thêm dải đo khoảng cách: `border-top:1.5px dashed` + 2 tick dọc ở hai đầu, thay vì chỉ viết text khoảng cách suông.

## Hình sinh bằng JS — snapshot không thấy màu

`browser_snapshot` chỉ trả text. Muốn biết **màu thật** có phân biệt được không, dùng `browser_console` + `getComputedStyle`:

```js
// đếm phần tử theo class (kể cả class ghép)
JSON.stringify({
  cells: document.querySelectorAll('.ecell').length,
  syn:   document.querySelectorAll('.ecell.syn').length,
  rad:   document.querySelectorAll('.ecell.rad').length,
  ga:    document.querySelectorAll('.ecell.ga').length
})
// đọc màu thật của từng loại
getComputedStyle(document.querySelector('.ecell.syn')).backgroundColor
```

Lần này tint `rgba(179,38,30,.14)` trả về đúng nhưng **quá nhạt để đọc trên ảnh chụp** → phải đẩy lên `.30` + viền `.6` + đổi màu chữ đậm hơn, rồi mới publish.

Quy tắc: hình sinh bằng JS phải verify bằng **console** (đếm + màu), còn hình vẽ tay bằng CSS/SVG phải verify bằng **vision** (hình học). Hai lớp này không thay thế nhau.

## Thứ tự làm để không phải publish nhiều lần

`POST /api/store` tạo **id mới mỗi lần**, không ghi đè. Nên: QA hết trên bản local/publish đầu, gom sửa một lượt, rồi publish lần cuối. Nếu buộc phải publish lại, **id cuối cùng mới là bản đúng** — đưa user id đó và fetch-back verify lại, đừng đưa id lần đầu.

## Checklist trước khi báo xong

- [ ] `scripts/validate-html.py` (nếu có) hoặc grep: CJK, từ Anh lọt, tag balance
- [ ] `browser_navigate` + fetch-back: HTTP 200, dấu tiếng Việt còn nguyên, mojibake 0
- [ ] Cuộn tới **từng** hình, `browser_vision` hỏi từng label
- [ ] Hình JS: `browser_console` đếm + `getComputedStyle` màu
- [ ] Mobile 390px: không overflow, chip không đè
- [ ] URL trả cho user là id **cuối cùng**
