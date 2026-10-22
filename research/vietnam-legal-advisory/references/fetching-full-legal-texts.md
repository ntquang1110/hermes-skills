# Recipe: tải toàn văn luật VN để trích nguyên văn (đã kiểm chứng 10/2026)

Khi cần **trích nguyên văn điều khoản** (bắt buộc cho hồ sơ tư vấn / đơn tố cáo), đừng search rồi đoán.
Tải toàn văn, grep theo số điều, đọc TÊN ĐIỀU để xác nhận.

## 1. Nguồn hoạt động: `hethongphapluat.com`

**Pattern 1 — trang index của cả bộ luật (chứa TOÀN VĂN, tốt nhất):**
```
https://hethongphapluat.com/<slug>          # ví dụ: /luat-dat-dai-2024, /bo-luat-dan-su-2015
```
Trả về **toàn văn luật** (~400KB text cho BLDS 2015, ~944KB cho LĐĐ 2024). Đây là nguồn ưu tiên #1
khi cần tra nhiều điều trong cùng một bộ luật — 1 request = cả luật.

**Pattern 2 — trang từng điều (nhanh, đúng 1 điều):**
```
https://hethongphapluat.com/<slug>/dieu-<N>  # ví dụ: /bo-luat-dan-su-2015/dieu-129
```

URL slug của các luật hay dùng: `bo-luat-dan-su-2015`, `luat-dat-dai-2024`, `luat-dat-dai-2013`.
Nếu slug sai → 0 chars (không phải HTTP error). Thử `luat-<tên>` rồi `bo-luat-<tên>`.

**Quy tắc tìm điều trong file toàn văn:** mỗi điều xuất hiện **2 lần** —
lần đầu là mục lục/giải thích, lần sau là **thân điều khoản thật**. Luôn lấy lần xuất hiện
sau cùng, hoặc lần có tiếp ngay sau là nội dung khoản (không phải tiêu đề điều kế tiếp):
```python
hits = [i for i, l in enumerate(lines) if re.match(rf'^Điều {N}\.\s', l)]
body = [h for h in hits if h > 3000] or hits   # với BLDS 2015; ngưỡng tuỳ độ dài file
```

## 2. Script tải + strip (dùng lại nhiều lần, đừng viết lại)

Xem `scripts/fetch_legal_text.py` trong skill này. Gọi:
```bash
python scripts/fetch_legal_text.py "<url>" <outname>    # -> <outname>.txt + <outname>.html
python scripts/fetch_legal_text.py "<url>" <name> m      # 'm' = mobile UA (một số site chặn desktop)
```
Strip bằng regex (bỏ script/style/noscript, `<br>`→newline, block tags→newline, rồi `html.unescape`),
dedupe dòng liên tiếp trùng nhau → file text sạch, grep được.

## 3. Nguồn dự phòng (thứ tự thử)

| Nguồn | Tình trạng 10/2026 |
|---|---|
| `hethongphapluat.com` | ✅ Hoạt động, cả desktop UA. **Dùng cái này trước.** |
| `thuvienphapluat.vn` (kể cả `m.`) | ❌ HTTP 403 Cloudflare với cả desktop lẫn mobile UA. Không lãng phí thời gian bypass. |
| `vbpl.vn` (CSDLQG) | ⚠️ Trang tìm kiếm là Next.js SPA — HTML trả về **không chứa kết quả**. Phải dùng browser (render JS) hoặc `congbao.chinhphu.vn`. |
| `luatvietnam.vn` | ⚠️ URL phải đúng; đoán bừa → 404 hoặc redirect sang văn bản khác. Có giá trị cho mục "Tin pháp luật" (bài tổng hợp văn bản mới). |
| `congbao.chinhphu.vn` | ✅ Mở được bằng curl, nhưng endpoint search `tim-kiem.htm?...&type=vanban` trả về **không có dữ liệu**. Chỉ dùng để tra metadata khi đã biết tên/số hiệu. |

## 4. Xác minh hiệu lực — chạy code, đừng nhớ

```bash
python scripts/legal_kb.py check --doc "91/2015/QH13"
python scripts/legal_kb.py check --doc "43/2024/QH15"
python scripts/legal_kb.py find --topic "dat dai chuyen nhuong so do" --verbose
```
KB ở `~/.claude/skills/vietnam-legal-advisory/scripts/legal_registry.json` của session cha.
Nếu `check` trả `unknown` → **KHÔNG tự đoán số hiệu**, tra nguồn rồi `--add`.

## 5. Bẫy: công cụ search bị chặn → đừng dùng curl DDG/Bing

`lite.duckduckgo.com` trả CAPTCHA ("Select all squares containing a duck") sau ~3 request;
`bing.com/search` HTML mà `execute_code` parse được trả **0 kết quả** (selector `b_algo` không khớp).
**Khi cần search trong script, hãy dùng `browser_navigate` tới `lite.duckduckgo.com/lite/?q=...`
và đọc snapshot** — tránh hết quota curl nhanh, tránh CAPTCHA.

## 6. Nếu vẫn không xác minh được → nói thẳng

Ví dụ session 10/2026: không tìm ra được văn bản nào sửa **Điều 134** BLDS 2015 năm 2025.
Kết luận đúng: nêu rõ "**chưa xác minh được**, cần tra CSDLQG", đưa danh sách nguồn đã thử,
và **không** dự đoán số hiệu. Điều này bảo vệ hồ sơ khách hàng tốt hơn nhiều so với việc
đoán rồi bị sửa sai số hiệu.