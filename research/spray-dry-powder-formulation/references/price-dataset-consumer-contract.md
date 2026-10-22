# Conforming to the price-data CONSUMER (`price_lib.py`) — the authoritative schema

Dùng khi đề bài nói "ghi ra `data/price/price_TN.json` theo đúng schema" nhưng **không có schema kèm theo**,
và các sub-agent viết `price_T1/T2/T3.json` song song mỗi người đoán một kiểu.
Chìa khoá: **schema không nằm ở file anh em — nó nằm ở CONSUMER.**

## Bước 0 — đường dẫn có dấu cách thì đừng dùng rg
`Hermes Proj` có dấu cách → `search_files`/rg báo `IO error ... cannot find the file specified (os error 2/3)`
trên đường dẫn `/d/Hermes Proj/...`. Chuyển sang `read_file` hoặc `execute_code` với
`io.open(r"D:/Hermes Proj/...")`. Đừng kết luận "không có file" chỉ vì rg fail.

## Bước 1 — tìm và đọc consumer
1. Liệt kê `*.py` ở gốc dự án; tìm module cùng họ dữ liệu (`price_lib.py`, `group_lib.py`, `build.py`).
2. Đọc **hết** module. Các tuple `ALIAS_*` ở đầu file **chính là hợp đồng tên key**. Hàm `load(dir, base)`
   cho biết nó glob file nào; `attach(rows, prices)` cho biết ghép theo khoá gì (`id`).
3. Ghi lại danh sách key trước khi viết một dòng dữ liệu nào.

## Hợp đồng `price_lib.py` (xác minh 22/10/2026)
`load(price_dir, base_dir)` glob **mọi** `data/price/price_*.json`; `attach(rows, prices)` ghép theo `id`.

| khái niệm | key được đọc |
|---|---|
| giá VN | `gia_vn_vnd_kg` (số **hoặc dict**), fallback `_spread(it)` đọc `min`/`max` |
| giá quốc tế | `gia_tq_usd_kg`, `gia_usd_kg`, `gia_quoc_te_usd_kg`, `gia_usd`, `price_cn_dkg` |
| tỷ giá | `ty_gia_vnd_usd` / `ty_gia_USD_VND` / `ty_gia` — **theo TỪNG ITEM**, mặc định **26300** |
| liều | `lieu_dung_pct_chat_kho` / `lieu_pct` / `lieu_dung_pct` |
| thu hồi | `thu_hoi_pct` / `hieu_suat_thu_hoi_pct` (số hoặc dict) |
| EE | `ee_pct` / `hieu_suat_bao_vi_nang_pct` / `EE_encapsulation` |
| đóng bao / MOQ / NCC | `quy_cach_dong_bao`, `MOQ`, `nha_cung_cap_vn` (list) |
| ngày / nguồn | `ngay_lay_gia`/`ngay`, `nguon_gia`/`nguon` |
| còn lại | `grade`, `vai_tro`, `co_che_thu_hoi`/`tuong_thich_kiem`, `anh_huong_pH`, `do_tin_cay`, `chua_co_nguon` (list), `ghi_chu`/`note`, `verification`/`kiem_chung` |

Dạng dict đầy đủ nhất cho giá VN (đặt `quy_cach` để consumer tự gọi "giá bao lớn tại VN" vs "giá lẻ tại VN"):
```json
"gia_vn_vnd_kg": {
  "vn": {"min": 1700, "max": 3500, "quy_cach": "bao 25 kg", "moq": "25 kg", "don_vi": "vnd"},
  "tq": {"min": 0.39, "max": 0.39, "don_vi": "usd"}
}
```

## SÁU BẪY PARSER (đã trả giá thật)
1. **Số có ĐÚNG 3 chữ số sau dấu chấm bị đọc thành phân nghìn.** `_to_num("0.207")` → **207**
   (`parts=["0","207"]`, mọi phần sau dấu chấm dài 3 ⇒ nối thành "0207"). Giá nhảy 5.319.900 đ/kg thay vì 5.320.
   ⇒ Ghi USD/kg bằng **≤2 số thập phân** (`0.21`, `0.27`); TRÁNH `0.207`, `0.267`, `0.155`.
2. **`gia_usd_kg` dạng SỐ bị đánh cờ và LOẠI khỏi điểm giá.** Số → `usd=False` → nhánh `gia_tq_vnd < 500`
   nhân tỷ giá rồi bật `tq_mo_ho` → `can_xac_nhan_don_vi_gia = True` → `_diem_gia()` bỏ qua dòng đó.
   ⇒ Ghi dạng **CHUỖI**: `"gia_tq_usd_kg": "3.00 USD/kg"` (có `$`/`usd` trong chuỗi ⇒ `usd=True`, cờ không bật).
3. **`ty_gia` đọc theo từng item, KHÔNG lấy từ `meta`.** Quên set ⇒ mặc định 26300 ⇒ mọi giá quy đổi lệch ~2,3%.
   ⇒ Set `ty_gia_vnd_usd` trong **mọi** item (và cả meta cho người đọc).
4. **`_spread` chỉ đọc `min`/`max`** (`gia_thap`/`gia_cao`/`thap`/`cao`/`tu`/`from`/`den`/`to`),
   KHÔNG đọc `price_vn_min`/`price_vn_max` — dù comment trong code viết đúng hai tên đó.
   ⇒ Ghi **cả** `min`/`max` **và** `price_vn_min`/`price_vn_max` để bất kỳ bản consumer nào cũng đọc được.
5. **Số trong `gia_vn_vnd_kg` chặn nhánh dải giá.** Có số ⇒ `_spread(it)` không chạy ⇒ `gia_thap`/`gia_cao` = None.
   Muốn dải giá nổi lên thì để `gia_vn_vnd_kg = null` và chỉ dùng `min`/`max`. Đánh đổi: giữ số đại diện
   (an toàn cho mọi phép tính số học + luôn có giá trị) rồi vẫn ghi min/max trong file — chọn cách này khi
   chưa biết consumer nào sẽ đọc.
6. **`thu_hoi_pct`/`ee_pct` phải là DICT mới mang được ghi chú.** `_doc_pct` lấy `gia_tri_dai_dien` và nối
   `dieu_kien · do_tin_cay · khoang · nguon` vào `ghi_chu_thu_hoi`/`ghi_chu_ee`. Nếu có cả `dai_dien` và
   `khoang`, code **lấy cận dưới** (an toàn hơn). Muốn EE = null MÀ vẫn giải thích lý do:
   `{"gia_tri_dai_dien": None, "dieu_kien": "…không phải chất mang vi năng…", "do_tin_cay": "không áp dụng"}`.

## Recipe verify (chạy TRƯỚC khi báo xong)
```python
import sys; sys.path.insert(0, r"D:/Hermes Proj/say-phun-kiem")
import price_lib
p = price_lib.load("data/price", ".")
rows = [{"id": i, "name_vi": i, "score": 60} for i in IDS]
price_lib.attach(rows, p)
for r in rows:
    pr = r.get("price") or {}
    print(r["id"], pr.get("gia_vn"), pr.get("gia_usd_kg"), pr.get("ee_pct"))
price_lib.summary(rows)
```
**Soát tay các giá trị vô lý** — đây là bước bắt được lỗi, không phải thủ tục cho có:
`gia_usd_kg > 50` ⇒ gần như chắc chắn đã dùng **giá lẻ lab** thay cho bulk (aerosil: 95,8 AUD/kg lẻ ⇒ 77.100
đ/kg "bulk" là SAI; bulk fumed silica ~3 USD/kg). `gia_vn` lớn bất thường ⇒ lỗi parse 1000× (bẫy 1).
Tổng kết: `price_lib.summary()` in "N/N dòng có dữ liệu | M có giá VN | K tính được chi phí" — đối chiếu
với số chất bạn cố ý để null.

Cuối cùng chạy đúng lệnh user đưa: `python -c "import json,io;d=json.load(io.open(r'…price_TN.json',encoding='utf-8'));print(len(d['items']))"`.

## Bài học chiến lược
- **Không có `price_stub.json` trên đĩa ≠ không có schema.** Schema nằm trong consumer. Đọc `price_lib.py`
  trả lời dứt khoát "dùng tên key nào", tốt hơn hẳn việc đoán union alias từ file anh em.
- Consumer có thể được **tạo trong lúc bạn đang chạy** (mtime cùng buổi). Đọc lại lần cuối ngay trước khi ghi.
- Đọc code lấy đúng tên key, nhưng **đừng tin comment trong code**: comment `price_lib.py` ghi
  "T3 ghi gia VN thanh 2 truong so sach: price_vn_min / price_vn_max" còn `_spread` lại đọc `min`/`max`.
  Tin implementation, viết cả hai.
