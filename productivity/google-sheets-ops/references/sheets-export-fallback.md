# Sheets export fallback (khi Sheets API refresh token timeout)

Dùng khi `svc...execute()` / `google_api.py` fail LẶP LẠI ở bước refresh token
(`TimeoutError: [WinError 10060]` trong `reauth.refresh_grant` /
`_token_endpoint_request_no_throw`), trong khi docs.google.com vẫn mở được
(`curl https://www.google.com` → 200). Chẩn đoán nhanh:

```bash
nslookup oauth2.googleapis.com   # timeout = DNS oauth2 chết, không phải sai auth
curl -s -o /dev/null -w "%{http_code}\n" --max-time 15 https://www.google.com  # 200 = mạng OK
```

Chỉ retry API 1 lần theo pitfall 6. Nếu vẫn timeout ở lần 2 → chuyển sang
export fallback ngay, đừng retry tiếp (session thực tế: fail 4 lần liên tiếp).

## Điều kiện

Sheet phải bật link sharing "Anyone with link" (snapshot browser hiện
`Chia sẻ. Bất kỳ ai có đường liên kết đều có thể truy cập`). Nếu sheet private
hoàn toàn thì fallback này không dùng được.

## Recipe

```bash
ID=<SPREADSHEET_ID>
mkdir -p sheet_dump && cd sheet_dump

# 1. Liệt kê mọi gid (kể cả tab trống mà metadata API cũng không thấy)
curl -sL --max-time 20 "https://docs.google.com/spreadsheets/d/$ID/htmlview" -o view.html
grep -o 'gid=[0-9]*' view.html | sort -u   # bỏ qua dòng 'gid=' rỗng

# 2. Export từng tab ra CSV (giữ nguyên giá trị hiển thị)
for gid in <gid1> <gid2> ...; do
  curl -sL --max-time 20 \
    "https://docs.google.com/spreadsheets/d/$ID/export?format=csv&gid=$gid" \
    -o "tab_$gid.csv"
done

# 3. Export full workbook xlsx (1 lần, lấy hết mọi tab + công thức)
curl -sL --max-time 30 \
  "https://docs.google.com/spreadsheets/d/$ID/export?format=xlsx" -o wb.xlsx
```

## Đọc nội dung (giữ công thức)

Tên tab thật nằm trong `xl/workbook.xml` của file xlsx (`<sheet name=...>`).
Map gid→tên tab bằng thứ tự sheet trong workbook + thứ tự gid tìm được,
hoặc đọc trực tiếp bằng openpyxl:

```python
import openpyxl
wb = openpyxl.load_workbook('wb.xlsx', data_only=False)  # False = giữ công thức
print(wb.sheetnames)
for name in wb.sheetnames:
    ws = wb[name]
    for r in ws.iter_rows(values_only=True):
        if any(v is not None and str(v).strip() != '' for v in r):
            print(list(r))  # cell công thức hiện dạng '=SUM(...)'
```

## Pitfalls của chính fallback này

- **Đừng dùng `/tmp` với `curl -o` trên git-bash Windows.** Đã gặp:
  `curl -o /tmp/x.csv` báo SIZE > 0 nhưng `head /tmp/x.csv` → No such file.
  Fix: `mkdir -p sheet_dump && cd sheet_dump`, dùng relative path, verify bằng `ls -la`.
- **Export size 0 = tab trống, không phải lỗi.** (VD tab "Chi tiết Tháng 2"
  trống hoàn toàn → `tab_<gid>.csv` 0 byte.) Đối chiếu với xlsx trước khi kết luận.
- **CSV chỉ có giá trị, mất công thức.** Muốn audit công thức (VD phát hiện
  `H11=SUM(G10:H10)` sai, đúng phải `SUM(B11:G11)`) thì đọc từ xlsx với
  `data_only=False`.
- **Fallback này chỉ đọc.** Ghi/formatting vẫn cần Sheets API → chờ mạng
  ổn lại, hoặc làm file local trước rồi đẩy lên sau.
- Xem `scripts/sheets_export_fallback.py` — script chạy 1 lần ra hết
  (enumerate gids → CSV từng tab → xlsx → dump nội dung giữ công thức).
