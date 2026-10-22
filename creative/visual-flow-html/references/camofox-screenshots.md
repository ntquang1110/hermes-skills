# Camofox full-page screenshots (API)

Context: Hermes `browser_vision` / `vision_analyze` fail khi model active không có vision
(lỗi: `unknown variant image_url` / `Failed to deserialize the JSON body ... unknown variant`).
Fallback tin cậy: gọi thẳng Camofox API (`http://localhost:9377`, skill `camofox-browser`).

## Recipe

1. **Tạo tab riêng** (userId tự đặt, không đụng session Hermes của browser tool):
```bash
curl -s -X POST "http://localhost:9377/tabs" -H "Content-Type: application/json" \
  -d '{"userId":"hermes-shot","sessionKey":"<task>","url":"http://127.0.0.1:<port>/<file>.html"}'
# → {"tabId":"..."}  (bắt buộc URL http/https — file:// bị chặn trả 400)
```
2. **(Tùy chọn) set viewport** — mobile 390x844 cho kiểm tra mobile-first:
```bash
curl -s -X POST "http://localhost:9377/tabs/<tabId>/viewport" -H "Content-Type: application/json" \
  -d '{"userId":"hermes-shot","width":390,"height":844}'
```
3. **Screenshot full-page**:
```bash
curl -s "http://localhost:9377/tabs/<tabId>/screenshot?userId=hermes-shot&fullPage=true" \
  -o "C:/Users/<user>/hermes-temp/<name>.png"
# fullPage=false nếu chỉ cần viewport hiện tại
```
4. **Verify PNG hợp lệ** (đọc IHDR đúng offset — width ở byte 8..12, height ở 12..16 của chunk IHDR, tức data[8:12]/data[12:16] sau khi đọc sig 8 byte + 16 byte tiếp):
```python
import struct
with open(p,'rb') as fh:
    sig = fh.read(8); data = fh.read(16)
w = struct.unpack('>I', data[8:12])[0]
h = struct.unpack('>I', data[12:16])[0]
# Mobile 390px full-page thường cao 5000-10000px — bình thường.
```
Lỗi cũ hay gặp: đọc nhầm `data[16:24]` → ra số khổng lồ (134 triệu px) — đó là CRC/IDAT, không phải kích thước.

5. Session timeout 30 phút inactivity. Xóa session nếu cần: `DELETE /sessions/<userId>`.

## Endpoints (server.js, repo D:/Hermes Proj/camofox-browser)
| Endpoint | Dòng | Ghi chú |
|----------|------|---------|
| `POST /tabs` | ~3060 | tạo tab, trả tabId |
| `POST /tabs/:tabId/viewport` | ~3914 | set kích thước viewport |
| `GET /tabs/:tabId/screenshot?userId=&fullPage=` | ~4428 | trả PNG trực tiếp (Content-Type image/png) |
| `GET /tabs?userId=` | ~5401 | list tabs của userId |
| `GET /tabs/:tabId/snapshot?includeScreenshot=true` | ~3106 | snapshot + base64 PNG trong JSON |

## Pitfalls
- `file://` URL bị chặn (400 Bad Request /tabs) → serve qua `python -m http.server` (background), rồi navigate tới `http://127.0.0.1:<port>/<file>`.
- Lần navigate đầu tiên có thể fail 500 (session reaper) → retry 1 lần là OK.
- Model không vision → không dùng browser_vision để "xem" ảnh; verify layout bằng browser_console DOM audit (scrollWidth > innerWidth, phần tử tràn), gửi PNG cho user xem.
