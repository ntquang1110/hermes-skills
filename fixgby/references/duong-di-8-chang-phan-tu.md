# Đường đi của chất — 8 chặng, mức phân tử (nền tảng tầng DECIDE)

Bản đồ: `visual/ma-tran-duong-di.html`. Mọi số dưới đây đã **đọc abstract thật** và đã đối chiếu từng chữ số, không chép tài liệu quảng cáo. Ngày đo: 18/10/2026.

## Vì sao có khung 8 chặng

Các nguồn đường đi hiện có (Reactome/KEGG/WikiPathways/Recon3D/HMDB/ChEBI) bắt đầu ở **tầng phân tử** và kết thúc ở **tầng phản ứng**. Chúng thiếu **2 ĐẦU**:
- hành vi/triệu chứng nào dẫn tới chất nào;
- một cá thể cụ thể đang ở trạng thái nào.

Số **chặng** thì hữu hạn (8), nên dùng được để ra quyết định. Số **phản ứng** thì không — xem mục "Bất khả".

## 8 chặng

| # | Chặng | Câu hỏi | Họ phân tử làm việc | Số thật |
|---|-------|---------|---------------------|---------|
| 1 | VÀO | vào bằng cửa nào? | *không có enzyme* — vật lý quyết định | 4 cửa + 1 cửa tự sinh |
| 2 | QUA HÀNG RÀO | tế bào có cho qua? | **SLC** (bơm vào) | 384 chuỗi, ít nhất 46 họ gen |
| 3 | GAN LẦN ĐẦU | bị sửa thành gì? | **CYP** (pha I, oxy hoá) | 57 gen chức năng |
| 4 | GẮN ĐỂ ĐI | làm sao tan trong máu? | enzyme liên hợp (pha II) + **albumin** (chở) | chỉ phần KHÔNG bám albumin mới tác động |
| 5 | TỚI MÔ ĐÍCH | tới được chỗ nào? | thụ thể / mô đích | 13.543 phản ứng · 4.140 chất · 3.288 gen = **17 %** gen người |
| 6 | RA KHỎI TẾ BÀO | đưa ra bằng cách nào? | **ABC** (bơm ra) | 48 gen · đột biến gây 21 bệnh/rối loạn Mendel |
| 7 | THẢI | rời cơ thể qua đâu? | bơm hấp thu ống thận + transporter mật | GFR 120 mL/phút = 180 L/ngày |
| 8 | Ở LẠI BAO LÂU | tích luỹ hay không? | *không có enzyme riêng* — t½ là **kết quả của 7 chặng trên** | — |

**Chặng 8 là chặn hiểu sai phổ biến nhất:** t½ không phải thuộc tính của chất. Cùng một chất, đổi cửa vào là đổi chặng 3, và chặng 8 đổi theo — dù chất không hề đổi.

## 5 cửa thải

1. **Thận → nước tiểu** — cửa lớn nhất. Lọc 180 L/ngày **nhưng lọc chưa đủ**: mô phỏng 30.000 thuốc ảo cho thấy thải ròng chỉ xảy ra khi **có bơm hấp thu ở màng đáy tế bào ống thận**; không bơm thì chất quay lại máu. Nước tiểu < 1,5 L/24 h bị coi là thấp.
2. **Gan → mật → phân** — một phần ra thẳng theo phân, một phần **bị hấp thu lại** rồi quay về gan (vòng ruột–gan), làm thời gian ở lại dài hơn tính toán đơn thuần.
3. **Phổi → hơi thở** — khí và chất bay hơi; không qua gan, không qua thận. *chưa có nguồn (tag H)*
4. **Da → mồ hôi** — cửa thải nhỏ, nhưng **da là cửa vào đồng thời**; da không phân biệt hướng. *chưa có nguồn (tag H)*
5. **Sữa** — chỉ ở phụ nữ đang cho con bú. Cửa thải duy nhất mà chất rời **người này vào thẳng người khác**. *chưa có nguồn (tag H)*

## 3 cách một chất đi trong máu

- **Tan tự do** — tới mọi mô, và **đây là phần tác động**.
- **Bám albumin** — nằm chờ, nhả dần. Đo tổng nồng độ sẽ **cao hơn** phần thực sự tác động.
- **Bám lipoprotein** — chất tan mỡ đi theo hạt mỡ, tới thẳng mô mỡ và gan theo đường riêng. *chưa có nguồn (tag H)*

## Số đã verify cho nicotine (mẫu đã audit từng chữ số)

- Sinh khả dụng **uống 40 %** vs **dán da 76 %** (PMID 33354734) → chênh 36 điểm phần trăm **do cửa vào**, không do liều.
- Máu **động mạch cao hơn tĩnh mạch hơn 2 lần** ngay sau khi hút → xét nghiệm lấy ở tay luôn **đo thấp hơn** thứ não thực nhận (PMID 8370337).
- Xịt mũi: đỉnh ở **động mạch 5 phút** vs **tĩnh mạch 18 phút**, p<0,01 (PMID 9357397).
- Máu động mạch đạt đỉnh ~1 phút; **não đạt đỉnh ở 5 phút** (PMID 7862909).
- Truyền TM 1 / 5 / 10 phút: giảm thèm **chỉ đạt ở 1 và 5 phút**, nhưng bơm nhanh nhất làm **tăng nhịp tim và huyết áp nhiều hơn** (PMID 31996940).
- Dán thuốc: lưng 102 %/106 %, **bụng 75 %** so với cánh tay (PMID 16291714).
- Bằng chứng âm tính: **vaccine nicotine thất bại** — giữ được phân tử ở ngoại biên mà hành vi hút không đổi (PMID 24894625).
- Cùng chất khác quần thể khác kết quả: cytisine 40 % vs NRT 31 % ở người hút thường (PMID 25517706), nhưng ở **bệnh nhân lao** 32,4 % vs 29,7 %, chênh 2,68 %, p = 0,114 → **thất bại** (PMID 33069301).
- EAGLES (PMID 27116918): lo ngại varenicline gây biến cố tâm thần kinh **bị bác bỏ** — 1,3 % vs 2,4 % giả dược, RD −1,28 (KTC −2,40 tới −0,15).

## Cái đã có sẵn — đừng xây lại

Đo lại bằng API ngày 18/10/2026:

- **Reactome v97** — 2.883 đường ở người (đếm từ file gốc 23.603 dòng toàn loài)
- **KEGG** (mã `hsa`) — 372 đường người
- **WikiPathways** — 1.131 đường người
- **ChEBI** — 200.956 thực thể hoá học
- **HMDB 5.0** — 217.920 chất (tăng từ 114.100), PMID 34986597
- **Recon3D** — 13.543 phản ứng · 4.140 chất · 3.288 ORF (**17 %** gen người có chú giải chức năng) · 12.890 cấu trúc protein, PMID 29457794
- **UniProt** human reviewed — 20.431

Mẹo gọi API (đã chạy được): Reactome `https://reactome.org/download/current/ReactomePathways.txt` rồi đếm dòng kết thúc bằng `Homo sapiens`; KEGG `https://rest.kegg.jp/list/pathway/hsa` đếm dòng; WikiPathways `https://www.wikipathways.org/json/listPathways.json` → `json["organisms"]` rồi tìm entry `latin == "Homo_sapiens"` → `pathways`; ChEBI `https://www.ebi.ac.uk/chebi/backend/api/public/es_search/?size=1` → `totalElements`; UniProt `https://rest.uniprot.org/uniprotkb/search?query=(organism_id:9606)+AND+(reviewed:true)&size=1&format=json` → header `x-total-results`. **HMDB chặn truy cập tự động (403)** → lấy số từ bài HMDB 5.0 thay vì crawl web.

## Bất khả — không được viết ngược lại

1. Mô hình đầy đủ nhất cũng chỉ phủ **17 %** gen người có chú giải. 83 % còn lại không nằm trong bản đồ nào.
2. Hiểu toàn bộ mạng là **bất khả về TOÁN HỌC**, không phải kỹ thuật: mạng JAK-STAT/MAPK/NF-κB **không xác định được** ngay cả khi đo được mọi biến trạng thái (PMID 19426527). Thêm cảm biến không giải quyết khoảng cách này.
3. Điền số vào ô trống bằng suy luận = **tự tạo dữ liệu**. Chỗ chưa có nguồn ghi thẳng `tag H`.

## Ranh giới pháp lý khi trình bày

Ở lại **tầng cơ chế**: chất gõ vào cửa nào, đi qua đâu, chặn ở đâu. Không biến thành tài liệu hướng dẫn dùng chất. Sản phẩm thuộc nhóm TĂBS — **cấm claim trị bệnh**, nói "chỉ số" không nói tên bệnh.

## Việc còn thiếu (tag H, đã ghi thẳng trên trang)

Bơm ABC cụ thể cho nicotine · tỉ lệ thải qua thận so với chuyển hoá ở gan · cửa thải phổi · da/mồ hôi · sữa · chất tan mỡ đi theo lipoprotein.
