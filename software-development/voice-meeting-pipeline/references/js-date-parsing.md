# JS date parsing — V8 pitfall (đã debug 05/08/2026)

## Bug gốc
`new Date(chuỗi_text)` trên V8 (Chrome/Node) **nhặt SỐ trong chuỗi làm month**:
```js
new Date('Thứ 7')        // → Sun Jul 01 2001  (số 7 → tháng 7!)
new Date('Tuần 1')       // → Mon Jan 01 2001  (số 1 → tháng 1!)
new Date('Thứ 7 (mùng 8)') // → Sun Jul 01 2001
```
Hệ quả: deadline là text ("Thứ 7", "Tuần 1", "Tuần 12") → tất cả bị tính thành quá hạn 2001.
Thêm: `new Date('05/08/2026')` trên V8 = **May 8** (US format MM/DD/YYYY), không phải 5/8/2026 (VN).

## Fix chuẩn — chỉ parse ngày cụ thể, KHÔNG fallback new Date(s)
```js
const parseDate = d => {
  if (!d) return null;
  const s = String(d).trim();
  let m;
  // dd/mm/yyyy — thứ tự NGÀY/THÁNG VN
  if ((m = s.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/))) {
    const dt = new Date(+m[3], +m[2]-1, +m[1]);
    return isNaN(dt) ? null : dt;
  }
  // yyyy-mm-dd hoặc yyyy-mm-dd HH:MM
  if ((m = s.match(/^(\d{4})-(\d{2})-(\d{2})(?:[ T].*)?$/))) {
    const dt = new Date(+m[1], +m[2]-1, +m[3]);
    return isNaN(dt) ? null : dt;
  }
  return null; // "Thứ 7", "Tuần X" → mốc tương đối → KHÔNG tính quá hạn
};
```

## Quy tắc
- Mốc tương đối ("Thứ 7", "Tuần 1", "cuối tuần") → `null` → bỏ qua quá hạn.
- Deadline nên lưu ngày cụ thể `dd/mm/yyyy` khi có thể; text mốc chỉ hiển thị.
- KPI "Task quá hạn" chỉ đếm task có deadline ngày cụ thể < hôm nay.
