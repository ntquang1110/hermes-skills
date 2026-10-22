# VN Market Price Research (Camofox + DDG pipeline)

Dùng khi: Quang cần "research giá thị trường + nơi bán" cho danh sách nguyên liệu/hoạt chất tại Việt Nam. Verified 15/08/2026 trên 40 hoạt chất chống tiêu chảy heo con (nhóm A botanicals / B probiotic-acid / C khoáng-clay).

## Pipeline đã chứng minh

1. **Chia nhóm → delegate 3 subagents song song** (A/B/C). LƯU Ý: subagent hay hết tool-iteration cap (50 calls) TRƯỚC khi ghi file → parent phải tự assembly từ inline summary + chạy loop local cho phần thiếu. Luôn kiểm tra file tồn tại, đừng tin subagent báo "đã ghi".
2. **Loop local (đáng tin nhất)**: pattern `research_groupA3.py` — mỗi query: `POST /tabs` tạo tab MỚI → navigate DDG → evaluate JS trích link → mở 2 URL trích giá → ghi JSONL ngay sau mỗi item → `DELETE /sessions/<user>` reset giữa chừng. KHÔNG dùng chung 1 tab cho toàn loop (tab Camofox chết sau 1-2 navigate, các query sau trả urls=0).
3. Ghi kết quả `prices_{A,B,C}.json` với `verified:true/false` cho từng chất.

## Nguồn giá hoạt động (08/2026)

- **websosanh.vn** — curl được, parse giá thật (vd B. subtilis 280–480k/kg @10^11 CFU/g, acid citric 27–40k/kg bao 25kg)
- **hoachatthinghiem.org, oilcare.vn, kobi.vn, tinhdauylang.com, nhathuoclongchau.com.vn, pharmacity.vn, trungtamduoclieu.vn** — mở qua Camofox được
- **alibaba.com/vietnamese** — giá FOB tham khảo
- **CHẶN (đừng tốn turn)**: thegioihoachat.com.vn (403), vietnamchemicals.vn (DNS chết), chodansinh.vn (DNS chết), Google (CAPTCHA), Bing (kết quả rác), Shopee/Tiki search (login-gated)

## Regex trích giá VNĐ

```python
r'([\d.,]+)\s*(?:đ|VNĐ|vnd|₫)\s*(?:/|per\s*)?\s*(kg|k|g|lit|l|100g|500g|1kg|chai|hộp|bao|tấn)'
```

## Quy tắc trung thực (bắt buộc)

- `verified:true` chỉ khi mở được URL thật và thấy giá trong trang
- Không tìm được giá công khai → `price_range_vnd='Chưa có giá công khai'`, `availability='Đặt hàng riêng'/'Nhập khẩu'/'Khó tìm'`
- KHÔNG bịa tên công ty, không bịa giá. Phân biệt giá dược phẩm/TPBVSK vs giá nguyên liệu feed-grade (thường "Liên hệ" qua đại lý TACN)

## Quy đổi đơn vị (khi merge vào sheet tính lượng mua)

- mg/kg → g/kg (×0.001); % khẩu phần → g/kg (×10); ppm = mg/kg
- Probiotic CFU/kg → g premix/kg: giả định premix chuẩn 10^10 CFU/g, ghi chú "kiểm tra CFU/g thực tế"
- ORS không trộn cám — tính riêng theo thể trọng (50–100 ml/kg/ngày)
- Chất có 2 dạng (chiết xuất vs bột thô) → ghi note hệ số nhân

## Google Sheets merge (thêm cột tính lượng mua)

- **sheetId KHÔNG phải 0** — fetch metadata (`spreadsheets().get()`) lấy sheetId thật trước khi batchUpdate format
- Công thức sống: `=IF(ISNUMBER(J2),ROUND($K$50*J2/1000,2),"")` — anchor tuyệt đối trỏ TỚI ô TỔNG CÁM
- **PITFALL #REF!**: đặt block tham số ở dòng 47–50 rồi viết `=K48*K49*K50` ngay trong ô K50 = self-reference → #REF!. Đúng: tổng cám ở K50 tham chiếu `=K47*K48*K49` (3 ô NHẬP ở trên), data K2:K41 tham chiếu `$K$50`
- Format: `updateDimensionProperties` (pixelSize), `repeatCell` (wrapStrategy, backgroundColor), freeze header qua `updateSheetProperties.gridProperties.frozenRowCount`
- Google API có thể timeout (WinError 10060) → retry 1 lần là OK
