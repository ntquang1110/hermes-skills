---
name: livestock-formula-optimization
description: "Use when designing/scoring livestock additive formulas."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [livestock, formula, premix, scoring, optimization, evidence-tier, feed-additive]
    related_skills: [livestock-trial-protocol, livestock-product-lifecycle, feed-additive-sourcing-vn, iterative-optimization-loop]
---

# Thiết kế và tối ưu công thức phụ gia chăn nuôi

Dùng khi phải trả lời: *"công thức nào hiệu quả nhất, tỉ lệ bao nhiêu, và chứng minh tại sao"* cho một
bệnh hoặc một chức năng (tiêu chảy, hô hấp, sinh trưởng, stress nhiệt, giải độc, khoáng...).

Nguyên tắc gốc: **công thức không được chấm bằng cảm nhận.** Phải có một bộ chấm chạy được, tái lập
được, và phải tự nói ra chỗ nào bộ chấm của mình không đáng tin.

## Quy trình 8 bước

1. **Chốt cửa trước, chất sau.** Vẽ đường đi bệnh thành các chặng, mỗi chặng là một cửa. Chất chỉ
   được đặt vào cửa, không được quét chất rồi đi tìm chỗ dùng.
2. **Gắn nhãn bệnh cho từng nguyên liệu** (danh sách riêng cho từng bệnh). Không có nhãn này thì bộ
   tối ưu sẽ nhét hoạt chất tiêu chảy vào công thức hô hấp chỉ vì chúng cùng tên cửa.
3. **Lập bảng nguyên liệu**: bậc bằng chứng (0–4), dải liều đã có người thử trên đúng loài, cơ chế
   tác động, thứ bậc giá, cờ ổn định (acid tự do / muối acid / khoáng sét / kiềm / tinh dầu / đã bọc).
4. **Chấm hai trục ngang nhau**: hiệu quả trên vật chủ `E` và ổn định sản phẩm `S`.
   `Tổng = 0,5·E + 0,5·S`. Chi tiết công thức: `references/scoring-engine-design.md`.
4b. **Kiểm nồng độ đạt được so với MIC** cho mọi chất định ghi là "kháng khuẩn": liều trộn cám → nồng độ
   lòng ruột → so với MIC. `nồng độ/MIC < 1` thì **cấm ghi cơ chế kháng khuẩn**, và chất đó phải được xếp
   lại vào cửa hậu quả. Công thức tính và ca berberine: `references/scoring-engine-design.md`.
5. **Chạy leo dốc từng bước**: đổi liều → thêm → bỏ, mỗi vòng một thay đổi, chỉ giữ nếu điểm tăng,
   dừng khi không còn bước nào cải thiện. Ghi log từng vòng.
5b. **Chẩn đoán trần — đọc điểm TỪNG CỬA, không chỉ đọc tổng.** Cửa nào đã chạm trần 0,95 thì thêm chất
   nữa là vô ích; cửa nào bằng 0 là chỗ đáng dồn tiền. Nếu tổng điểm ở 10 và 20 kg/tấn giống nhau thì
   **đừng bán bản 20 kg/tấn** — nó chỉ mua thêm giá vốn.
6. **Chạy lại ở nhiều ngân sách** (5 / 10 / 20 kg/tấn) và cả một bao lẫn tách gói. Cùng một công thức
   ở ba ngân sách là ba công thức khác nhau, không phải ba phiên bản.
6b. **Quét CẢ HAI CHIỀU, quét xuống sàn trước.** Chốt theo "điểm bão hoà" khi chỉ quét từ trên xuống là
   sai: bão hoà thật thường nằm thấp hơn ngân sách mình giả định. Quét 0,5 → 8,0 kg/tấn bước 0,5, tìm
   đỉnh, rồi mới chọn. Ca thật: TC-1 bão hoà ở **2,5 kg/tấn** chứ không phải 5; HH-1 ở **4,5** chứ
   không phải 7,5 — nửa số kg ở bản chốt đầu là tiền đổ đi.
   **Sàn kỹ thuật** = tổng kg nhỏ nhất mà MỌI nguyên liệu vẫn nằm trong dải liều đã có người thử trên
   đúng loài. Dưới sàn thì điểm chỉ đúng trên giấy: ở 1,0 kg/tấn TC-1 cho 84,80 điểm nhưng tannin trong
   đó chỉ còn 52% liều thấp nhất đã thử ⇒ **không dùng con số đó để bán**.
6c. **Quét lại ở ba tương quan trọng số** (0,5/0,5 · 0,7/0,3 · 0,3/0,7) để kiểm điểm bão hoà có bất biến
   không. Nếu một trục bị ghim (S = 100 suốt dải liều) thì đổi trọng số chỉ **dịch đường cong lên
   xuống**, không đổi hình dạng — đừng bán "phân tích độ nhạy" bằng ba đường song song. Hình dạng chỉ
   đổi khi trục kia thật sự thay đổi. Ca thật: TC-1 bất biến ở 2,5 kg với cả ba cách cân; HH-1 thì coi
   nặng ổn định chỉ mua thêm 0,4 điểm từ 4,5 lên 8 kg, còn coi nặng hiệu quả mua được 2,0 điểm ⇒ chỗ
   dừng của HH-1 phụ thuộc ưu tiên, **phải chốt trọng số trước khi viết cứng vào đề cương thử nghiệm**.
6d. **Biên giá trị mỗi kg là con số quyết định, không phải điểm.** Tính Δ điểm / Δ kg khi hạ một mức
   ngân sách. Ca thật: TC-1 từ 2,5 xuống 2,0 mất 0,25 điểm mỗi kg; HH-1 từ 4,5 xuống 4,0 đã mất 2,00
   ⇒ TC-1 rẻ điểm gấp 8 lần, cắt ngân sách thì cắt ở TC-1 trước.
7. **Ép biến thể** (nếu khách yêu cầu thêm nhóm cố định) và **đo giá của việc ép** bằng Δ điểm so với
   bản không ép. Đây là con số phải nói ra, không được giấu.
8. **Viết báo cáo 3 tầng**: kết luận + tỉ lệ kg/tấn (5 giây) → tại sao tỉ lệ đó + Δ của biến thể (1 phút)
   → phản biện chính model (đọc kỹ). Không bảng rộng, không tính từ khen.

## Phép toán ngân sách liều — chỗ hay sai nhất

Ngân sách là mức đưa premix vào cám: 0,5% = 5 kg/tấn · 1% = 10 kg/tấn · 2% = 20 kg/tấn.

Liều hiệu quả đã có người thử của phần lớn acid hữu cơ, butyrate, huyết tương là **0,3–6% khẩu phần**.
Nghĩa là một nguyên liệu duy nhất đã ăn hết ngân sách 0,5% trước khi kịp thêm bất cứ thứ gì.

Luôn kiểm câu này trước khi khen một công thức: *liều đã chứng minh có nhét vừa ngân sách đang bán không?*
Nếu không vừa thì nói thẳng: **bán liều thấp hơn liều trong tài liệu là bán cảm giác, không bán hiệu quả.**
Hoặc thiết kế một sản phẩm đậm đặc chỉ 2 nguyên liệu mạnh nhất ở đúng liều.

## Phân tầng bằng chứng (thay cho chữ "lâm sàng")

Đừng gọi "có bằng chứng lâm sàng" khi thực chất là thử trên heo vài chục con một trại. Bốn tầng:

| Tầng | Nghĩa | Cách đếm tự động |
|---|---|---|
| 1 | Đo trên đàn nhiễm tự nhiên ngoài trại | `loai == in_vivo_heo` VÀ regex tự nhiên/trại dương tính |
| 2 | Gây nhiễm chủ động rồi đánh giá | `loai == in_vivo_heo` VÀ regex gây nhiễm/challenge |
| 3 | In vivo đúng loài, đo chỉ tiêu | `loai == in_vivo_heo` |
| 4 | Chỉ in vitro | không có `in_vivo_heo` |

Kinh nghiệm thực tế: 57 hoạt chất, 64 PMID verify 64/64 → chỉ **2 chất tầng 1**, **2 chất tầng 2**,
48 chất tầng 3, 5 chất tầng 4. Con số này là kết quả đúng, đừng làm tròn lên cho đẹp.

**Nhóm mạnh hơn từng chất.** Bằng chứng tốt nhất của một hỗn hợp là bằng chứng trên chính hỗn hợp;
không tách được phần đóng góp từng thành phần. Vì thế **không được cộng điểm từng thành phần rồi coi
như đã chứng minh cả hỗn hợp.**

Bắt buộc chấm **hai cột cho mỗi nhóm**: bậc cao nhất *theo từng chất* và bậc cao nhất *theo dạng hỗn hợp*,
rồi nói rõ đang lấy cột nào khi chấm điểm `E`. Ba hệ quả phải nói ra: không giảm được liều từng chất,
không bỏ được một chất để giảm giá, và không bảo vệ được công thức khi nhà cung cấp đổi nguyên liệu.
`hỗn hợp = L0` nghĩa là ghép nhóm đó là **bước vào vùng chưa có bằng chứng** — vẫn ghép được nhưng phải
nói thẳng. Bảng 15 nhóm kèm số đo thật: `references/evidence-tiering-by-group.md`.

## Tương kỵ: thứ tự ưu tiên cách xử lý

1. **Bỏ một trong hai.** Xung đột acid tự do ↔ nền kiềm KHÔNG chữa được bằng bao bì, vì hai thứ vẫn
   gặp nhau trong dạ dày. Cách duy nhất là **dùng muối acid** (K-diformat, Ca-propionate, Na-butyrate)
   thay acid tự do, hoặc bỏ kiềm.
2. **Đổi dạng bào chế:** bọc lipid cho butyrate, bọc/nano cho tinh dầu, bọc cho enzyme và protease.
3. **Tách gói.** Chỉ gỡ được phần xung đột xảy ra *trong bao*. Xung đột xảy ra *trong lòng ruột* vẫn
   còn nguyên — khi mô hình hoá, tách gói chỉ gỡ ~60%, không bao giờ gỡ 100%.
4. **Giảm liều / hạ tầng suất.**

Bản đồ cặp tương kỵ và mức độ: `references/incompatibility-map.md`.

## Từ "giá bậc 1–5" sang GIÁ VỐN VND — bước bắt buộc trước khi chốt bán

Cột "giá bậc 1–5" chỉ là **thứ bậc**, không dùng được để định giá. Muốn ra giá vốn thật thì:

1. Quy đổi định mức về **kg nguyên liệu / kg premix** (`= kg/tấn cấm ÷ liều kg/tấn`), rồi nhân đơn giá VND/kg.
2. Đơn giá lấy từ **giá niêm yết B2B có URL + ngày + MOQ** — cách tra ở `feed-additive-sourcing-vn` mục *Lấy giá để ĐỊNH GIÁ VỐN*.
3. Không có nguồn → `chua_co_nguon`, **không suy đoán**. Thành phần ghép (`thymol/acid rosmarinic`) thì giả định tỷ lệ **và khai ra**, đừng im.
4. Đối chiếu trần công ty: **giá vốn ≤ 27% giá bán lẻ** ⇒ giá bán tối thiểu `= giá vốn / 0,27`. Nói rõ đạt/không đạt, và chỉ ra **đòn giảm chi phí lớn nhất** (nguyên liệu nào chiếm % giá vốn cao nhất).
5. Nêu rõ giá niêm yết **chưa gồm vận chuyển + thuế + phí** ⇒ giá vốn landed cao hơn **15–30%**.

**Cờ đỏ phải báo ngay — hoạt chất TINH KHIẾT CAO ở liều kg/tấn.** Ca thật (20/10/2026, TC-1/HH-1 heo con):
acid glycyrrhizic 98% giá **3,31 triệu VND/kg** ⇒ một mình nó chiếm **>90% giá vốn HH-1**, cho ra
**9,51 triệu VND nguyên liệu/tấn cám** — **phi thực tế về thương mại**. Kết luận đúng không phải là
"báo giá vốn rồi im", mà là *"công thức phải chuyển sang chiết xuất chuẩn hoá nồng độ thấp"* (cùng họ
nguyên liệu, giá thấp hơn 5–7 lần: chiết xuất cam thảo 18–20 USD/kg thay GA 98%, chiết xuất hoàng cầm
18–24 USD/kg thay baicalin 85%) — lúc đó HH-1 rơi từ 2.113.619 xuống **457.651 VND/kg premix**.

Đọc bảng giá vốn **cùng với** bảng biên giá trị mỗi kg (bước 6d): nguyên liệu vừa đắt vừa ở cửa đã chạm trần là chỗ cắt đầu tiên.
Số đầy đủ của ca TC-1/HH-1: `fixgby/references/no-02-gia-von-tannin-va-gia.md`.

## Pitfalls

- **Cho tách gói xoá sạch hình phạt** → mọi công thức đều đạt ổn định 100, thang đo mất khả năng phân
  biệt. Tách gói phải còn tồn dư.
- **Không phạt nhiệt ép viên 70–90 °C** → công thức chứa men vi sinh và tinh dầu trần vẫn được điểm cao.
- **Không thưởng cơ chế dự phòng** → bộ tối ưu luôn chọn một chất rẻ nhất cho mỗi cửa, ra công thức
  mỏng và dễ sụp khi một cơ chế hỏng.
- **Lấy max thay vì max + dự phòng khác cơ chế** → không phân biệt được công thức 1 chất và 3 chất.
- **Để seed vượt ngân sách mà không chặn** → in ra công thức 1,0% nằm trong ngân sách 0,5%.
- **Không giới hạn số nguyên liệu** → ra công thức 9–10 thành phần, không trộn đều được, dễ phân tầng.
- **Gán sai cửa** (chất tác động trong lòng ruột bị xếp vào cửa chặn mầm trong cám) → sai toàn bộ
  trọng số. Kiểm lại từng chất: nó tác động ở đâu, không phải nó được bán để làm gì.
- **Cho trần điểm 1,0** → công thức nào cũng "hoàn hảo". Luôn để trần ~0,95; không công thức nào đáng
  điểm tuyệt đối.
- **Đếm bằng chứng bằng regex trên cả khối JSON** → bài in vitro có chữ "trại" bị tính là nhiễm tự
  nhiên. Chỉ chạy regex trên các bản ghi `in_vivo_heo`.
- **Báo cáo bằng tính từ** ("tối ưu", "mạnh mẽ") thay bằng số (điểm, Δ, kg/tấn, số PMID). Người dùng
  đọc số, không đọc lời khen.
- **TIN LUẬT TƯƠNG KỴ TỰ NGHĨ RA.** Đây là lỗi nặng nhất và đã xảy ra thật: sáu cặp hình phạt đoán mò bị
  bằng chứng bác bỏ (acid tự do + muối kẽm hữu cơ và tanin + ion kim loại **trung tính**; MCFA C8–C10 +
  canxi **trung tính**; acid tự do + bào tử Bacillus **trung tính**; acid tự do + tinh dầu phenol là
  **hiệp lực +8**; IgY hỏng vì **pH dạ dày 2–4** chứ không phải vì acid trong bao). Sau khi thay bằng
  luật có bằng chứng, Δ của biến thể bị ép xấu đi từ −41 thành −44,2. **Mọi hình phạt/luật cộng phải đối
  chiếu bản đồ có PMID trước khi dùng để chốt công thức.** Danh sách 6 cặp đã bác: `incompatibility-map.md`.
- **Chỉ chấm hình phạt mà không chấm hiệp lực** → bộ tối ưu luôn ra công thức mỏng. Có cặp cộng điểm thật
  (acid hữu cơ + tinh dầu phenol +8, in vivo heo). Xem bảng hiệp lực trong `scoring-engine-design.md`.
- **Đọc tổng điểm mà không đọc điểm từng cửa** → bỏ mất kết luận đáng tiền nhất: mọi cửa đã chạm trần thì
  thêm nguyên liệu là vô ích, tiền phải dồn vào cửa trống. Ca thật: tăng ngân sách từ 10 lên 20 kg/tấn
  **không đổi một điểm nào**.
- **Xếp một chất vào đúng cửa theo CƠ CHẾ ĐO ĐƯỢC, không theo cơ chế bài báo ghi.** Berberine bị gọi là
  "kháng khuẩn" nhưng nồng độ/MIC chỉ 0,08 ⇒ hiệu quả đo được đến từ điều hoà kênh nước (AQP8, SLC9A3).
  Xếp nó cùng nhóm ORS, không xếp vào nhóm kháng khuẩn.
- **Lấy bậc bằng chứng của NHÓM rồi gán cho từng CHẤT mà không nói rõ.** Phải chấm hai cột (riêng chất và
  dạng hỗn hợp) và ghi rõ đang lấy cột nào: `references/evidence-tiering-by-group.md`.
- **Giữ một chất trong công thức dù nhóm của nó là L0 cho đúng bệnh đó.** Ca thật: acid hữu cơ trong cám
  cho hô hấp = L0 ⇒ phải bỏ acid benzoic và kali diformat khỏi công thức hô hấp, dù chúng rất mạnh cho
  tiêu chảy.
- **Chốt liều bằng cách chỉ quét một chiều từ trên xuống.** Đã xảy ra thật: bản chốt đầu là 5,0 và 7,5
  kg/tấn; quét xuống sàn mới thấy đỉnh nằm ở 2,5 và 4,5. Luôn quét tới sàn trước khi khen một con số.
- **Tin điểm của bộ leo dốc ở ngân sách sát sàn.** Leo dốc kẹt cực trị địa phương: ở 0,70 kg/tấn nó ra
  75,3 điểm trong khi bài toán phủ tập hợp ra **79,70 điểm** với cùng lượng kg (chênh 4,4 điểm). Bắt
  buộc đa điểm xuất phát, và **chạy thêm một lượt phủ tập hợp** cho các mức sát sàn; chênh lệch giữa
  hai cách giải phải vẽ ra thành ký hiệu riêng, không được giấu.
- **Coi S = 100 là sản phẩm ổn định.** Ở mọi nghiệm tối ưu tự do, S đứng 100 suốt dải liều vì engine
  không tìm thấy cặp tương kỵ nào trong tổ hợp đó. Muốn thấy S rơi phải ép nền kiềm + nền khoáng vào:
  khi đó S của TC-1+2 rơi từ 88 xuống 70 rồi lên 82, và E không bao giờ bằng bản tự do.
- **Chốt công thức mà không tính giá vốn VND, hoặc để giá vốn vượt trần 27% mà không nói.** Cột "giá bậc"
  không phải giá VND (xem mục *Từ "giá bậc 1–5" sang GIÁ VỐN VND*). Ca thật: HH-1 giá vốn 2.113.619
  VND/kg premix ⇒ giá bán tối thiểu 7,83 triệu VND/kg — gấp ~22 lần TC-1 và không bán được.
- **Nhận liều nguyên liệu mà không hỏi TITER/HÀM LƯỢNG THẬT.** Liều ghi cho "tannin hạt dẻ" chỉ có nghĩa
  khi biết titer: hàng thật trải **40% → 55% → 73±2% → 75%**, polyphenol Folin chỉ ~36%, và cùng một nhà
  SX (Tanin Sevnica) có cả dòng 73±2% lẫn dòng 40%. Sai titer gần 2 lần ⇒ sai liều gần 2 lần. Luôn ghi
  trong công thức "**quy về titer 75%**" và đòi CoA ghi hàm lượng + phương pháp định lượng.
  Và **`tannic acid` (gallnut, CAS 1401-55-4) KHÔNG phải tannin hạt dẻ** — bẫy cả khi mua lẫn khi tra giá.

## Bắt buộc nói ra trước khi bị hỏi

Kết thúc mọi báo cáo công thức phải có mục **"phản biện lại chính model"**, nêu rõ:

- Trọng số cửa và các hệ số là do người dựng đặt, không phải hằng số sinh học. Đổi trọng số là đổi
  công thức.
- `S = 100` chỉ có nghĩa "không biết xung đột nào", **không** có nghĩa "sản phẩm ổn định". Muốn biết
  thật phải chạy gia tốc 40 °C / 75% RH trong 3 và 6 tháng rồi đo lại hoạt chất.
- Nồng độ/MIC nếu chỉ có cho vài chất thì phần còn lại là **ân hạn**, không phải bằng chứng.
- Giá bậc 1–5 là thứ bậc, không phải giá VND. Muốn nói giá bán thì phải đi qua bước tính giá vốn VND
  (mục *Từ "giá bậc 1–5" sang GIÁ VỐN VND*), kèm trần 27% và cảnh báo landed +15–30%.
- Chưa tính tương tác ba chiều.
- Luôn kèm ba con số theo thứ tự này: **điểm bão hoà + sàn kỹ thuật + biên giá trị mỗi kg**. Nói rõ chỗ
  dừng nào phụ thuộc trọng số (phải để người quyết chốt ưu tiên ổn định hay hiệu quả) và chỗ dừng nào
  bất biến. Bảng số đầy đủ của ca TC-1/HH-1: `references/dose-floor-and-weight-sweep.md`.

## File hỗ trợ

- `references/scoring-engine-design.md` — công thức điểm E và S, bảng hệ số, bảng hình phạt + hiệp lực đã
  đối chiếu bằng chứng, phép kiểm nồng độ/MIC, chẩn đoán trần theo từng cửa, cách đọc kết quả.
- `references/incompatibility-map.md` — các cặp tương kỵ hoá lý, cơ chế, cách xử lý, kèm bảng 6 cặp luật
  đoán đã bị bằng chứng bác bỏ.
- `references/evidence-tiering-by-group.md` — thang L0–L4, luật chấm hai cột (riêng chất vs hỗn hợp), bảng
  15 nhóm kèm số đo thật, bẫy khi đọc abstract.
- `references/dose-floor-and-weight-sweep.md` — số liệu quét liều hai chiều (TC-1, HH-1), sàn kỹ thuật,
  quét ba tương quan trọng số, biên giá trị mỗi kg, trần không phá được bằng kg, danh sách script.
- `templates/formula-engine.py` — khung engine chấm điểm + leo dốc, thay bảng nguyên liệu là chạy.

## Liên quan

- `livestock-trial-protocol` — bước sau khi chốt công thức: đề cương khảo nghiệm, nghiệm thức, chỉ tiêu.
- `feed-additive-sourcing-vn` — giá và nguồn nguyên liệu thật để thay cột "giá bậc".
