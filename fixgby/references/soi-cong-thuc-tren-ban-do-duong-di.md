# Soi 23 công thức trên bản đồ đường đi

Mục đích: chốt **định mức** bằng bằng chứng, không bằng giá và kinh nghiệm. Công thức = danh sách
nguyên liệu × tỷ lệ để đạt **một chức năng**. Việc phải làm: soi từng công thức trên bản đồ đường đi,
xem các nguyên liệu **có thật sự cộng lại hay triệt nhau** — rồi mới chốt định mức.

## Hai tầng, đừng lẫn

| | CÔNG THỨC | KHO CHẤT |
|---|---|---|
| Vai trò | đầu ra | đầu vào |
| Số lượng | 23, đóng | mở, tới 1.000 |
| Câu hỏi | tổ hợp này có trùng chức năng không | thư viện phình thì bản đồ còn đọc được không |

Chỗ nối: một công thức là **tập con** của kho chất. Nên câu hỏi "chất nào chùng đường" là câu hỏi
**cấu trúc dữ liệu đầu vào**; nó phục vụ việc CHỌN nguyên liệu, không phải việc chốt định mức.

Lượt 19/10/2026 Quang chất vấn cụm `100 / 1.000 chất` trong follow-up relay vào nhóm R&D — chữ đó
là **nguyên văn voice note của chính anh** (21/09), em chỉ chuyển nhóm theo lệnh anh. Trả lời đúng
là truy nguồn, không phải giải thích ý nghĩa.

## Nguyên tắc 1 — giao nhau tính ở tầng NODE, không phải tầng CHẶNG

Hai chất cùng chặng 3 nhưng một đứa qua CYP2E1, đứa kia qua CYP3A4 thì **KHÔNG giao nhau**. Nhìn ma
trận 8 chặng sẽ tưởng là trùng và cắt nhầm. Ví dụ thật: curcumin và thìa canh đều "chặng gan", khác
enzyme → không cộng hưởng.

## Nguyên tắc 2 — số node có TRẦN, số chất thì không

Node = enzyme · bơm/kênh · thụ thể · cửa thải ≈ vài nghìn. Nên ma trận chất × node là **thưa**: thêm
1.000 chất chỉ làm các chấm **dày lên**, không làm bản đồ phình ra. Trên ~60 chất thì tắt đường nối và
chuyển sang **tô mật độ** — vẫn đọc được, không rối.

## 4 câu phải trả lời cho MỖI công thức

| Câu | Cách đọc trên bản đồ | Hành động |
|---|---|---|
| Có ai thừa? | 2 nguyên liệu đụng **cùng 1 node** | cắt 1, giữ đứa rẻ/bền hơn |
| Có ai triệt nhau? | A **ức chế** đúng node mà B cần đi qua | cắt hoặc tách liều |
| Có chặng nào trống? | không nguyên liệu nào chạm chặng đó | bổ sung nhánh còn thiếu |
| Có dồn 1 cửa thải? | mọi đứa cùng ra thận/mật | tăng liều vô ích, chỉ tăng tải cơ quan |

## 3 phép nhìn chéo cả 23 công thức

1. Nguyên liệu **lặp ở nhiều công thức** → gom mua, một MOQ, một ô kho, một lần kiểm nghiệm.
2. Công thức **trùng node** với nhau → gộp SKU, bớt dây.
3. Nguyên liệu **chỉ dùng 1 lần** → cân nhắc bỏ: chi phí kho + MOQ ăn hết lãi.

## ĐO COVERAGE TRƯỚC — không hứa rồi mới đo

Số đo 19/10/2026 (đếm bằng code, không đếm mắt):

- `docs/10-cong-thuc-23/cong-thuc-23.json` — 23 công thức, **26 nguyên liệu duy nhất**, lô 2 kg, trộn 5 kg/tấn.
- `visual/do-thi-duong-di.html` (142 KB, dựng 19/10, **chưa publish**) — payload: **21 chất · 94 node · 342 cạnh · 29 điểm có ≥2 chất chùng**.
- Giao hai tập: **7/26** nguyên liệu công thức đã có bản đồ. **Thiếu 19.**
  - Mất trắng nhóm enzyme/probiotic/acid: Phytase, Xylanase, Protease, Bacillus subtilis, Betaine HCl, Acid citric.
  - Mất gần hết nhóm thảo dược: Thymol, Carvacrol, Eucalyptol, Glycyrrhizin, Propolis, dịch chiết lá hẹ,
    Tannin Chestnut, Tannin Quebracho, Berberine, Ích mẫu, Hoàng liên, Huyết dụ.

Coverage theo dòng: GR-01 sinh trưởng **0/4** · GT-01 tiêu chảy **0/3** · RS-01 hô hấp **0–1** ·
GS-01 stress **2** · MT-01 viêm tử cung **3**. → **3/5 dòng chưa soi được gì.**

## Thứ tự việc

1. Tra 19 nguyên liệu còn thiếu vào 8 chặng / node, có PMID. Ưu tiên GR-01 và GT-01 (đang 0/4 và 0/3).
2. Dựng bảng: 23 công thức × (NL → node → vai trò → trùng / đối kháng / trống).
3. Từ bảng đó mới ra đề xuất cắt–giữ–bổ sung theo từng công thức, kèm tiết kiệm định mức.

Chưa tra 19 nguyên liệu kia thì bảng định mức lập ra chỉ là con số, không phải bằng chứng.

## Kỹ thuật trên chính file

- Dựng trang: `visual/build-do-thi-duong-di.py` → `visual/do-thi-duong-di.html`.
- Đọc payload để đếm, khỏi mở trình duyệt:
  `re.search(r'var D = (\{.*?\});\s*var NODE', html, re.S)` → `chats` · `nodes` · `canh` · `giao` · `can_thiep` · `thieu`.
- Sinh script mới thì đặt `SRC = os.path.dirname(os.path.abspath(__file__))`, không hardcode `docs/<batch>` (pitfall 21).
- Đếm giao hai tập tên: chuẩn hoá bỏ dấu **cả hai phía** + bỏ hậu tố ngoặc, và **in danh sách CHƯA KHỚP** (pitfall 20).

## Bug builder đã gặp và đã vá (đừng tái phạm)

- `drawnList()` trả rỗng ở chế độ gộp → **không vẽ đường nào**. Chế độ gộp phải trả `Object.keys(byChat)`.
- SVG sinh ra mang `id="g"` nhưng render gọi `getElementById("svg")` → **văng JS sau tương tác đầu tiên**, trang đứng im mà trông như không có lỗi.
- Cột nhãn ngoài SVG thiếu đệm `paddingTop = "14px"` → nhãn trượt dần theo hàng.
