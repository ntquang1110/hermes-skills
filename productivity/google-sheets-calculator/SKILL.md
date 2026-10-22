---
name: google-sheets-calculator
description: "Use when adding live calculation columns to a Google Sheet."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [google-sheets, calculator, formulas, batchUpdate, vietnamese]
---

# Google Sheets — thêm cột tính toán sống

Pattern cho yêu cầu kiểu "thêm cột để tính lượng mua dự kiến", "tính tổng tiền", "tính theo số con / cám / ngày" trên một Google Sheet đã có sẵn. Kết quả phải là CÔNG THỨC SỐNG (user đổi tham số là tự tính lại), không phải giá trị tĩnh.

## Workflow chuẩn (đã chứng minh 15/08/2026 — sheet <SHEET_ID>)

1. **Lấy dữ liệu gốc + map id**: đọc sheet hiện tại (values().get), xác định thứ tự các dòng. Nếu data từ JSON (như groupA/B/C), build `id_map` tên-chất → id JSON.
2. **Build mapping giá trị tính trước khi đụng API**: với mỗi dòng, chốt 1 con số "liều tính" (giữa khoảng khuyến nghị, chuẩn hóa đơn vị: mg/kg→g/kg = /1000, %→g/kg = ×10, CFU→g premix theo giả định CFU/g). Ghi ra `dose_map.json` — đây là nguồn chân lý cho cả sheet lẫn script.
3. **Xác định tham số đầu vào** (người dùng sẽ sửa): ví dụ Số con, Cám/con/ngày (kg), Số ngày dùng. Đặt ở block riêng cuối sheet (vd J47:K50), nền vàng nhạt để dễ thấy, label bold.
4. **Công thức tổng** (vd TỔNG CÁM = K47×K48×K49) — đặt ở K50. **Công thức từng dòng**: `=IF(ISNUMBER(J{r}),ROUND($K$50*J{r}/1000,2),"")` — tham chiếu tuyệt đối `$K$50`.
5. **Write với `valueInputOption='USER_ENTERED'`** — bắt buộc để công thức được Google đánh giá, không bị lưu dạng chuỗi.
6. **Format bằng batchUpdate**: độ rộng cột, wrap text, top-align, màu header, màu block tham số, freeze dòng 1.
7. **Verify**: đọc lại bằng `valueRenderOption='FORMATTED_VALUE'` (không phải FORMULA), tính nhẩm 1-2 dòng đối chiếu (vd 100 con × 0,5 kg × 30 ngày = 1500 kg cám; liều 2,25 g/kg → 1500×2,25/1000 = 3,38 kg).

## Pitfalls (đã dính thật)

- **sheetId KHÔNG phải 0**: batchUpdate mà hardcode `sheetId: 0` → `HttpError 400 "No grid with id: 0"`. Phải gọi `spreadsheets().get()` lấy `meta['sheets'][0]['properties']['sheetId']` (sheet này = 1887479623). LUÔN lấy động.
- **Công thức tự tham chiếu → #REF!**: viết `=K48*K49*K50` VÀO ô K50 là self-reference → #REF!. Tổng phải nằm ở ô KHÁC với các ô tham số, và tham chiếu các ô tham số (K47,K48,K49).
- **Tham chiếu tuyệt đối trong công thức hàng loạt**: phải dùng `$K$50` không phải `K50`, nếu không khi Google giãn cột sẽ lệch tham chiếu.
- **ISNUMBER guard cho dòng đặc biệt**: chất không tính theo cám (vd ORS tính theo thể trọng) → ghi chuỗi "— (tính riêng)" thay vì số, công thức dòng đó dùng IF(ISNUMBER...) để không hiện 0/lỗi.
- **Network timeout WinError 10060** khi gọi Sheets API từ VN — retry 1 lần là đủ, không phải bug.
- **Phân biệt FORMULA vs FORMATTED_VALUE**: khi verify phải dùng FORMATTED_VALUE để thấy kết quả tính, FORMULA chỉ thấy chuỗi công thức.
- **Đơn vị khác nhau giữa các dòng** (g/kg vs CFU/kg vs ml/kg): phải chuẩn hóa hết về 1 đơn vị tính (g/kg TĂ) trong dose_map trước, ghi chú quy đổi vào notes. Không trộn đơn vị trong cột số.

## Liên quan
- google-workspace skill: cách gọi API Sheets cơ bản (values get/update, batchUpdate). Skill này bổ sung pattern tính toán + pitfalls.
- Credentials: `C:/Users/NTQUANG_DELL/AppData/Local/hermes/google_token.json` (OAuth2, auto-refresh).
