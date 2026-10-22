# Pattern K — Chiến lược + Phản biện + Bảng dữ liệu lớn

CSS component + spec cột cho brief ra quyết định (bản đồ bệnh → chiến lược → phản biện).
Chạy OK: `D:/Hermes Proj/ban-do-benh-lon-vietnam.html` (20 tác nhân, 6 SVG, 2 bảng lớn, 68KB → publish OK).

## 1. CSS component (copy nguyên khối vào `<style>`)

Design system nền: Premium B/W/Y (`--bg:#0D0D0D`, `--surface:#1B1B1D`, `--surface2:#252528`, `--yellow:#FFD600`, `--radius:24px`).

```css
/* Bảng dữ liệu lớn — cuộn ngang trên mobile, KHÔNG bóp cột */
.twrap{overflow-x:auto;margin:10px 0;border-radius:12px;border:1px solid var(--line)}
.dtable{width:100%;border-collapse:collapse;font-size:11px;background:var(--surface2);min-width:640px}
.dtable th{background:#1F1F22;color:var(--yellow);font-weight:600;text-align:left;
  padding:8px 8px;border-bottom:1px solid var(--line);white-space:nowrap;font-size:10px;position:sticky;top:0}
.dtable td{padding:7px 8px;border-bottom:1px solid var(--line);color:var(--gray);vertical-align:top;line-height:1.45}
.dtable tr:last-child td{border-bottom:none}
.dtable tr:hover td{background:rgba(255,214,0,.03)}
.dtable .tname{color:var(--white);font-weight:600;white-space:nowrap}
.dtable .num{font-family:var(--mono);text-align:right;white-space:nowrap}
.dtable .tcost{color:var(--yellow);font-family:var(--mono);text-align:right;white-space:nowrap}
/* Mã màu mức độ — dùng NHẤT QUÁN cho cả bảng */
.dtable .r-hi{color:#FF5050;font-weight:600}   /* nghiêm trọng / chết cao */
.dtable .r-mid{color:#FFB400}                  /* trung bình */
.dtable .r-lo{color:#00C878}                   /* thấp / đã kiểm soát */
.dtable .ttype{font-size:8.5px;padding:1px 5px;border-radius:999px;white-space:nowrap}
.rank-badge{display:inline-block;width:16px;height:16px;line-height:16px;text-align:center;
  border-radius:50%;background:rgba(255,214,0,.15);color:var(--yellow);font-size:9px;font-weight:700;font-family:var(--mono)}

/* Khối phản biện — 4 biến thể màu theo vai trò */
.crit{background:var(--surface2);border-radius:12px;padding:14px;margin:8px 0;border-left:3px solid var(--yellow)}
.crit.blue{border-left-color:#00C8FF}    /* bằng chứng khoa học ĐÃ CÓ */
.crit.red{border-left-color:#FF5050}     /* rủi ro / giới hạn / phản biện */
.crit.green{border-left-color:#00C878}   /* hiệu quả dự kiến / kết luận */
.crit .ctitle{font-size:13px;font-weight:700;margin-bottom:6px;color:var(--white)}
.crit .cbody{font-size:11.5px;color:var(--gray);line-height:1.6}
.crit .cbody strong{color:var(--white)}

/* Thanh hiệu quả định lượng */
.eff-bar{display:flex;align-items:center;gap:6px;margin:6px 0}
.eff-bar .eb-label{font-size:10px;color:var(--gray);min-width:110px}
.eff-bar .eb-track{flex:1;height:8px;background:rgba(255,255,255,.06);border-radius:4px;overflow:hidden}
.eff-bar .eb-fill{height:100%;border-radius:4px}
.eff-bar .eb-val{font-size:10px;font-family:var(--mono);min-width:34px;text-align:right}

/* Dải giai đoạn (lifecycle) */
.lifecycle{display:flex;align-items:center;gap:0;margin:10px 0;border-radius:10px;overflow:hidden;height:50px}
.lc-phase{flex:1;height:100%;display:flex;align-items:center;justify-content:center;
  font-size:9px;font-weight:600;text-align:center;padding:0 4px;line-height:1.2}

/* Card 3 vùng địa lý — viền trên màu phân biệt */
.rgrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin:8px 0}
@media(max-width:560px){.rgrid{grid-template-columns:1fr}}
.rc{border-radius:12px;padding:12px;font-size:11px;background:var(--surface2);border:1px solid var(--line)}
.rc-north{border-top:3px solid #00C8FF}
.rc-central{border-top:3px solid #FFB400}
.rc-south{border-top:3px solid #FF5050}
```

Quy tắc dùng màu `r-hi/r-mid/r-lo`: **cùng một chỉ số phải cùng một màu trên toàn trang** (tỉ lệ chết cao = đỏ ở mọi bảng). Đừng đổi nghĩa màu giữa các bảng.

## 2. Spec cột bảng

### Bảng so sánh tác nhân (sortable theo mức nghiêm trọng)

Sort **giảm dần theo tỉ lệ chết**, không sort alphabet, không sort theo phổ biến.

| # | Tác nhân | Loại | Cơ quan tấn công | Phổ biến | Chết | Chi phí |
|---|---|---|---|---|---|---|
| rank-badge | tname (nowrap) | badge VIRUS/VI KHUẨN/KÝ SINH | liệt kê 2-4 cơ quan | `r-hi/r-mid/r-lo` | `r-hi/r-mid/r-lo` | tcost |

Footnote bắt buộc dưới bảng khi số liệu phụ thuộc nhóm tuổi: `* Tỉ lệ chết cao ở con non; trưởng thành thấp hơn nhiều. Chi phí là ước lượng điều trị + thiệt hại tăng trưởng.`

Kèm **short list 3 nhóm ưu tiên** ngay dưới bảng (3 khối `.crit`):
- **Ưu tiên 1** — nghiêm trọng nhất, khó can thiệp nhất → chiến lược chặn ngoài
- **Ưu tiên 2** — phổ biến cao + chết thấp → dễ can thiệp bằng hoạt chất, thị trường lớn nhất về số lượng
- **Ưu tiên 3** — chi phí điều trị cao nhất → nơi tiết kiệm nhiều nhất nếu có thay thế

### Bảng thị trường

| Đối tượng | Giải pháp hiện dùng | Hiệu quả | Vì sao đúng mức đó | Chi phí/đơn vị | Tần suất |
|---|---|---|---|---|---|

- **Hiệu quả** ghi dải (`40-60%`), tô màu theo mức.
- **"Vì sao"** là cột giá trị nhất. Mọi lý do phải là cơ chế cụ thể: đề kháng kháng sinh leo thang, chủng virus mới không khớp vaccine, tồn dư/áp lực pháp lý, vi khuẩn yếm khí khó tiếp cận, tái phát sau khi ngừng thuốc. Không viết "do bệnh phức tạp".
- Xếp bảng theo **nhóm bệnh** (hô hấp / tiêu chảy / toàn thân), không xếp theo chữ cái.

Kèm 1 SVG biểu đồ ngang quy mô thị trường từng nhóm + dòng tổng, để user thấy ngay nhóm nào lớn.

## 3. Diagram SVG hay dùng (inline, không ảnh ngoài)

Không dùng `<img>`, không dùng ảnh base64 — mọi diagram là `<svg viewBox="0 0 680 H">` inline, `width:100%;height:auto`.

| Diagram | viewBox gợi ý | Nội dung |
|---|---|---|
| Lifecycle 4 giai đoạn | `0 0 680 180` | 4 cột, mỗi cột liệt kê bệnh của giai đoạn, mũi tên → giữa các cột |
| Bản đồ 3 vùng | `0 0 640 120` | 3 hộp: khí hậu + nguyên nhân + hệ quả |
| Cơ chế diệt mầm bệnh | `0 0 640 130` | Chuỗi 4-5 bước: tác nhân → cơ chế → hệ quả → chết |
| Biểu đồ thị trường | `0 0 680 200` | Bar ngang + nhãn số + đường phân cách + dòng TỔNG |
| Hệ phân tầng phòng thủ | `0 0 680 270` | 4 hộp xếp dọc, mũi tên ▼, mỗi hộp có % mục tiêu canh phải |

Mẹo: mọi `<text>` cần `font-family` kế thừa từ CSS `.diagram text` — set 1 lần trong `.diagram text`, sau đó chỉ override `font-size`/`fill` inline. Đặt `font-size` tối thiểu 9px, nhãn phụ 9.5-10px để còn đọc được trên mobile.

## 4. Publish — recipe đã chạy ổn định

```bash
python -c "
import json
content = open('D:/Hermes Proj/<file>.html', encoding='utf-8').read()
payload = json.dumps({'content': content, 'title': '<short ascii title>'}, ensure_ascii=False)
open('C:/Users/NTQUANG_DELL/hermes-temp/payload.json','w',encoding='utf-8').write(payload)
print('payload size:', len(payload))
"
curl -s -X POST "https://preview.thefirstonly.com/api/store" \
  -H "Content-Type: application/json" --data-binary @"C:/Users/NTQUANG_DELL/hermes-temp/payload.json"
# → {"id":"...","preview_url":"https://preview.thefirstonly.com/...","size":N}
curl -s -o /dev/null -w "%{http_code}" "https://preview.thefirstonly.com/<id>"   # phải là 200
```

- Ghi payload ra file rồi `--data-binary @file` — không nhúng HTML inline vào command (vỡ quote, ARG_MAX).
- Title để ASCII không dấu, ngắn.
- **Verify HTTP 200 trước khi báo done.** Model `deepseek-v4-flash` không có vision nên `browser_vision` trả 404 — verify bằng `browser_navigate` (đọc accessibility snapshot) + `grep -o "<svg" file.html | wc -l` để đếm diagram, đừng cố chụp ảnh.
- Bản cũ vẫn còn trên URL cũ sau khi update — luôn trả **link mới**, đừng hứa link cũ tự cập nhật.

## 5. Pitfall riêng của Pattern K

1. **Đừng viết mục phản biện bằng lời lẽ trung tính.** User yêu cầu phản biện là để *tự đập* phương án của chính mình. Mỗi khối "bằng chứng" phải đi kèm khối "rủi ro" tương ứng, không có mục nào chỉ toàn điểm mạnh.
2. **Đừng gộp phản biện vào phần chiến lược.** User yêu cầu riêng một mục — phải là heading `<h2>` riêng, có sub-heading A/B cho từng hàng rào, và có mục C "hệ phân tầng" kết lại.
3. **Đừng để cột "Vì sao" trống hoặc chung chung** trong bảng thị trường — đó là cột user hỏi riêng.
4. **Đừng bỏ callout cảnh báo khoa học ở cuối.** Phải nói rõ số liệu nào là ước lượng từ in vitro/loài khác và chưa có thử nghiệm đối chứng trên đối tượng thật. Đây là ranh giới giữa tư vấn và bịa.
5. **Kiểm tra lại mâu thuẫn nội bộ sau khi thêm mục phản biện.** Bản đầu của mục chiến lược hay viết "kiềm sinh học an toàn, không tồn dư" — trong khi mục phản biện lại nói "pH 13-14 gây bỏng kiềm". Phải sửa mục chiến lược cho khớp và trỏ sang mục phản biện, không để hai chỗ nói ngược nhau.
