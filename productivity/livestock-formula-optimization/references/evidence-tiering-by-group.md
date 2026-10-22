# Phân tầng bằng chứng theo NHÓM, và luật "riêng chất ≠ dạng hỗn hợp"

Dùng khi phải trả lời *"nhóm nào đã chứng minh được trên loài đích ở điều kiện nhiễm bệnh thật, nhóm nào
chỉ có in vitro, nhóm nào chỉ chứng minh được ở dạng hỗn hợp"*.

## Thang bậc

| Bậc | Nghĩa | Cách đếm tự động |
|---|---|---|
| **L4** | Nhiều thử nghiệm đối chứng ngẫu nhiên ở nhiều trại, hoặc tổng quan hệ thống / meta-analysis | có meta-analysis hoặc ≥ nhiều RCT nhiều trại |
| **L3** | Thử nghiệm trên **trại thật** (đàn nhiễm tự nhiên) có nhóm đối chứng, không gây nhiễm nhân tạo | `loai == in_vivo_heo` VÀ regex tự nhiên/trại dương tính/outbreak |
| **L2** | `in_vivo` trên loài đích **có gây nhiễm nhân tạo** (nêu chủng/liều) | `loai == in_vivo_heo` VÀ regex gây nhiễm/challenge/inoculat |
| **L1** | Chỉ `in_vitro` — **hoặc** `in_vivo` trên loài đích nhưng **không gây nhiễm và không đo chỉ số bệnh** (chỉ đo năng suất/niêm mạc/miễn dịch) | không thỏa L2, L3, L4 |
| **L0** | Chỉ có cơ chế suy luận/lý thuyết, chưa thí nghiệm nào đo — **hoặc** KHÔNG TÌM THẤY thí nghiệm nào đo trên đúng đối tượng/hỗn hợp đang xét | không tìm thấy |

Điểm dễ sai nhất: thí nghiệm `in_vivo` trên heo **chỉ đo ADG/FCR** đã bị chấm **L1**, không phải L2. Nếu
người dùng hỏi "đã thử trên heo chưa thì vẫn là thử trên heo", phải nói rõ hai cách chấm và **ghi cách nào
đang dùng**.

## Luật quan trọng nhất: chấm HAI cột

Với mỗi nhóm phải chấm **cả hai**: bậc cao nhất **theo từng chất** và bậc cao nhất **theo dạng hỗn hợp**.

Lý do: ở phần lớn nhóm, **bằng chứng của hỗn hợp mạnh hơn bằng chứng của từng chất**. Bằng chứng tốt nhất
của "acid hữu cơ + monoglyceride MCFA" là bằng chứng trên **chính hỗn hợp đó**, không tách được phần đóng
góp của từng thành phần.

Ba hệ quả không được quên khi lập công thức:

1. **Không cộng điểm từng thành phần rồi coi như đã chứng minh cả hỗn hợp.**
2. **Không được giảm liều từng chất** để tiết kiệm — không biết chất nào tạo tác dụng.
3. **Không được bỏ một chất để giảm giá**, và **không bảo vệ được công thức khi nhà cung cấp đổi nguyên
   liệu**, vì tác dụng nằm ở cả hỗn hợp.

## Bảng đo thật 15 nhóm (ca đã chạy)

| Nhóm | Bệnh | Riêng chất | Hỗn hợp | Gây nhiễm | Trại thật |
|---|---|---|---|---|---|
| Acid hữu cơ chuỗi ngắn (formic, lactic, propionic, benzoic, K-diformat) | tiêu chảy | **L3** | **L3** | có | có |
| Butyrate + MCFA (Ca-butyrate, Na-butyrate bọc, tributyrin, monoglyceride C8–C10, monolaurin) | tiêu chảy | L2 | L2 | có | không |
| Prebiotic / oligosaccharide (MOS, GOS, scFOS) | tiêu chảy | L2 | **L0** | có | không |
| Acid amin và dinh dưỡng dễ tiêu (L-threonine, L-glutamate, Gly-Gln, SDPP, protease bọc) | tiêu chảy | L2 | L1 | có | không |
| Khoáng và hấp phụ (kẽm lactate, ZnO vi nang/cơ học hoá, attapulgite, bentonite, humate) | tiêu chảy | L2 | L2 | có | có |
| Tanin (chestnut, quebracho) | tiêu chảy | **L3** | L2 | có | có |
| Kháng thể uống IgY (K88) | tiêu chảy | L2 | L1 | có | không |
| Men vi sinh (Bacillus subtilis, Akkermansia) | tiêu chảy | **L4** | L2 | có | không |
| Thảo dược alkaloid/flavonoid (berberine, baicalin, houttuynia, yucca) | tiêu chảy | L1 | **L3** | không | có |
| Đất hiếm (lanthanide; chelate đất hiếm–chitosan) | tiêu chảy | L1 | L1 | không | không |
| Tinh dầu phenol và terpene (thymol, carvacrol, eucalyptol, limonene, pinene, acid rosmarinic) | hô hấp | **L3** | **L3** | không | có |
| Alkaloid/flavonoid chống viêm hô hấp (baicalin, glycyrrhizin, berberine, protoberberin) | hô hấp | L2 | L2 | có | có |
| Hỗn hợp phytogenic + MCFA + men vi sinh | hô hấp | **L0** | L2 | có | không |
| Acid hữu cơ trong **cám** dùng cho hô hấp (acid benzoic) | hô hấp | **L0** | **L0** | có | có |
| Chitosan | hô hấp | L1 | **L0** | không | không |

## Đọc bảng này ra quyết định

- **`hỗn hợp = L0` ⇒ ghép nhóm đó là bước vào vùng trống.** MOS đứng một mình thì L2, nhưng ghép MOS với
  scFOS vào cùng công thức là L0 — chưa ai thử hỗn hợp oligosaccharide. Vẫn ghép được, nhưng phải nói rõ
  là chưa có bằng chứng, không được trình bày như đã chứng minh.
- **Nhóm có `riêng chất = L0` cho đúng bệnh đó thì BỎ khỏi công thức bệnh đó.** Ca thật: acid hữu cơ
  trong cám cho **hô hấp** = L0 tuyệt đối ⇒ phải **bỏ acid benzoic và kali diformat khỏi công thức hô
  hấp**, dù chúng rất mạnh cho tiêu chảy. Nếu bản công thức trước còn hai chất này trong công thức hô
  hấp thì đó là lỗi, không phải lựa chọn.
- **Nhóm `riêng chất = L0` nhưng `hỗn hợp = L2`** thì claim thuộc về **hỗn hợp**, không thuộc về thành
  phần. Viết hồ sơ theo hỗn hợp.
- **Nhóm `riêng chất = L4`** là nhóm đáng chú ý nhất vì bậc cao nhất tài liệu thường nằm ở tổng quan hệ
  thống (ca thật: Bacillus subtilis L4, 29 nghiên cứu). Kiểm xem tổng quan đó có đo **đúng chỉ tiêu mình
  cần** không — bậc L4 cho tiêu chảy **không** tự động nghĩa là đã đo IgA tiết.
- **Kết quả nông suất mâu thuẫn giữa hai thí nghiệm ⇒ không kết luận được.** Ca thật đất hiếm: một bài
  dương trên 80 heo con, một bài không khác biệt và **FCR xấu đi 8% (p=0,01)** trên 112 heo con. Ghi
  "không thể quyết định giữ hay bỏ từ dữ liệu này", không chọn bên nào cho đẹp.

## Thí nghiệm bù nhanh nhất khi khoảng trống lớn

Khoảng trống đáng tiền nhất thường là **không biết chất nào tạo tác dụng trong hỗn hợp**. Cách bù rẻ nhất:

- **Leave-one-out trên mô hình gây nhiễm** (ví dụ challenge ETEC F4): chạy hỗn hợp đủ, rồi chạy lại thiếu
  từng chất một. Cho biết chất nào gánh, chất nào vô ích.
- Với nhóm chỉ có bằng chứng ở chuồng thí nghiệm, chạy **1 challenge** đúng mầm bệnh đang nhắm (APP hoặc
  Mhp cho hô hấp) để đẩy nhóm lên L2 và trả lời được câu "công thức hô hấp dựa vào cái gì".

## Bẫy khi đọc abstract

- Câu mâu thuẫn thuận nghịch ("higher ADG and FCR" — FCR cao hơn là **xấu đi**) ⇒ không dùng con số đó.
- `p = 0,06 / 0,08 / 0,10` chỉ là **xu hướng**, không phải khác biệt có ý nghĩa. Đừng viết thành "giảm rõ".
- Có bài tác giả tự gọi là "trends" dù `p = 0,03` ⇒ đọc theo số, không theo chữ tác giả.
- Đếm bằng chứng bằng regex trên **cả khối JSON** sẽ tính bài `in_vitro` có chữ "trại" thành nhiễm tự
  nhiên. Chỉ chạy regex trên các bản ghi `in_vivo` của đúng loài.
