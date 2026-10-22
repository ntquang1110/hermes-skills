# Trang "23 công thức × 8 chặng" — dữ liệu, luật phân loại, cách verify

Trang trả lời đúng câu Quang hỏi: *mỗi công thức chạm chặng nào, chặng nào không nguyên liệu nào chạm tới*.
Bộ dựng: `visual/build-ma-tran-cong-thuc.py` → `visual/ma-tran-cong-thuc.html`.
Dữ liệu vào: `docs/10-cong-thuc-23/cong-thuc-23.json` (từ sheet) + `batch-{a,b,c}.json` (research 26 nguyên liệu).

## Hai chiều trên một trang

1. **Công thức → 8 chặng.** Mỗi công thức một thẻ: mã CT · dòng · dạng (bột/nước) · trạng thái · thành phần kèm % và gram/lô 2 kg; dưới đó **8 dòng cố định**, mỗi dòng liệt kê nguyên liệu của công thức đó có tác động ở chặng ấy.
2. **Nguyên liệu → 8 chặng.** 26 thẻ chi tiết, mỗi thẻ đủ 8 chặng + dạng dùng · tương tác · bất khả · đã thất bại ở đâu · chỉ dấu đo được · tag H.
3. **Chặng nào cả danh mục chạm tới** — stacked bar 4 màu trên toàn bộ 26 nguyên liệu. Đây là phần trả lời câu hỏi lỗ hổng danh mục.

Từ khoá lọc: 5 dòng sản phẩm + ô tìm kiếm chung (khớp cả mã CT, tên nguyên liệu, tên enzyme/bơm vì tìm trên `JSON.stringify` của cả object).

## Luật phân loại một ô (nguyên liệu × chặng) — DETERMINISTIC, không phán đoán LLM

4 trạng thái, suy ra từ dữ liệu thô, không suy diễn thêm:

| Trạng thái | Điều kiện |
|---|---|
| `co` (có tác động) | có ít nhất 1 PMID **và** câu không bắt đầu bằng `KHÔNG` |
| `khong` (đã tra, kết luận không) | câu bắt đầu bằng `KHÔNG` |
| `thieu` | không có PMID, hoặc chuỗi chứa `CHƯA CÓ NGUỒN` |
| `trong` | không có chữ và không có PMID |

```python
def classify(c, k):
    blk = c.get(k) or {}
    txt = " ".join(str(blk.get(f) or "") for f in SUB[k]).strip()
    pm = [str(x).strip() for x in (blk.get("pmid") or []) if str(x).strip()]
    if not txt and not pm:                    return "trong", txt, pm
    if pm and not txt.upper().startswith("KHÔNG"): return "co", txt, pm
    if "CHƯA CÓ NGUỒN" in txt.upper() or not pm:   return "thieu", txt, pm
    return "khong", txt, pm
```

Hệ quả bắt buộc: chặng nào không có nguyên liệu nào loại `co` thì in thẳng
**`KHÔNG có nguyên liệu nào chạm tới`** (kèm danh sách nguyên liệu `khong`/`thieu` của chính công thức đó) —
**không được ẩn dòng**. Ẩn dòng làm user tưởng khung chỉ có 7 phần, và giấu mất chính thông tin anh cần: lỗ hổng.

## Bẫy đọc sheet "Vua Kiềm — RnD + Lab"

1. **Header tab `Sẵn sàng trộn` lệch: 6 nhãn cho 8 cột.** Thực tế cột D–F là thành phần, G = hoạt chất chính, H = trạng thái. **Đọc theo vị trí, tuyệt đối không theo header.**
2. **Nhiều công thức ở trạng thái `Chưa chạy được`** → thành phần là **giả định**, không phải đã chốt. `cong-thuc-23.json` có cờ `gia_dinh` theo từng thành phần; trang in kèm chữ `(giả định)`. Không trộn chung với phần đã chốt, không dùng số gram giả định để tính định mức mua.
3. Tab `Định mức & Lượng mua` là nguồn % và gram/lô; tab `Sẵn sàng trộn` là nguồn danh sách 23 CT. Không suy ra thành phần từ tên công thức.
4. 2 cảnh báo có sẵn trong sheet, phải giữ khi viết tiếp: **Selenium Yeast khác dạng Na-selenite** (không thay thế nhau) · **Phytase/Xylanase/Protease bắt buộc dạng coated**.

## 26 nguyên liệu — chia lô research

- **Lô A · 12 (kháng khuẩn / polyphenol / dược liệu):** Thymol · Carvacrol · Eucalyptol · Propolis · Glycyrrhizin (cam thảo) · Berberine (chiết xuất hoàng liên) · Hoàng liên (thô) · Tannin Chestnut · Tannin Quebracho · Ích mẫu · Huyết dụ · Dịch chiết lá hẹ
  → **TRẠNG THÁI 19/10/2026: `batch-a.{md,json}` CHƯA TỒN TẠI.** Đã verify 73 PMID, nguồn xong 5/12 chất
  (Thymol · Carvacrol · Eucalyptol · Propolis · Glycyrrhizin). Điểm chốt của 5 chất đầu + bẫy đã loại +
  bảng tương tác nội công thức: `references/lop-a-12-nguyen-lieu-8-chang.md`.
  **Chia nhỏ hơn khi giao lại: ≤ 5–6 nguyên liệu / subagent** — lô 12 chất đã hết ngân sách tool-call trước
  khi ghi được byte nào (xem pitfall 23 trong SKILL.md).
- **Lô B · 7 (enzyme / vi sinh / acid):** Phytase (coated) · Xylanase (coated) · Protease (coated) · Bacillus subtilis · Ca-butyrate · Acid citric · Betaine HCl 98%
- **Lô C · 7 (khoáng / vitamin / amino acid):** Curcumin nano · Vitamin E TPGS · Selenium yeast 2000 ppm · MgO · Mg chelate · L-Tryptophan 98% · Sodium ascorbyl phosphate

Schema JSON giữ y như 15 chất lô trước (8 khoá chặng + `bat_kha` / `da_that_bai` / `chi_dau_do_duoc` / `muc_bang_chung` / `tag_H` / `pmids`), thêm `dang_dung` và `tuong_tac`. Host = **heo**, ưu tiên bằng chứng trên heo; phần lớn nguyên liệu này tác động **tại ruột** — giả thuyết đó phải được nguồn xác nhận, không được mặc định.

## Alias tên tiếng Việt → slug

`ALIAS` phải được chuẩn hoá bỏ dấu **hai phía** (xem pitfall 20 trong SKILL.md). Bản dùng được:

```python
def nd(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s).strip()

ALIAS_ND = {nd(k): v for k, v in ALIAS.items()}
def slugify(name):
    a = nd(name)
    if a in ALIAS_ND: return ALIAS_ND[a]
    b = re.sub(r"\s*\([^)]*\)\s*$", "", a)   # "phytase (coated)" -> "phytase"
    return ALIAS_ND.get(b) or re.sub(r"[^a-z0-9]+", "-", a).strip("-")
```

Bộ dựng **phải in** `!! CHUA MAP: <tên> -> slug '<slug>'` cho mọi nguyên liệu không khớp và `len(load())` — đây là phép kiểm duy nhất bắt được lỗi ánh xạ.

## Số đo đã verify khi test bộ dựng (dữ liệu giả, thư mục tạm)

`tables: 0` · `23` thẻ công thức · `184` dòng (`23×8`) · font nhỏ nhất `12,8px` · không tràn · lọc `Hô hấp` → 4 CT (khớp sheet) · tìm `tannin` → 5 CT / 1 nguyên liệu · mobile iframe 360px: `gridTemplateColumns` = 1 giá trị (1 cột), font `12,8px`, `scrollWidth == clientWidth == 360`.

Luôn test bộ dựng trong thư mục tạm (`$TEMP/mt2`) bằng dữ liệu giả trước khi subagent ghi xong vào repo — tránh việc bộ dựng hỏng làm bẩn thư mục dữ liệu thật.

## Giao kết quả về nhóm Telegram

Nhóm **"hơi mệt làm rnd" = `-5090469823`** (Quang chốt 19/10/2026: research xong đổ về đó).
Cách làm: `getChat` để xác nhận bot vào được (không đoán), rồi gửi. Chi tiết + code: skill `hermes-telegram-gateway`.
