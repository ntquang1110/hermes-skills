# Kiểm một bài tổng quan có THẬT SỰ đo chỉ tiêu mình cần

Dùng khi ai đó trích một bài tổng quan (review / systematic review / meta-analysis) để nói
*"trong N nghiên cứu đó có nghiên cứu đo chỉ tiêu Y"*. Đây là **hai phép kiểm khác nhau**, và
gộp chúng là nguồn sai phổ biến nhất.

## Vì sao cần hai phép kiểm

| Phép kiểm | Câu hỏi | Cách làm | Kết luận được phép |
|---|---|---|---|
| 1. Tồn tại | Bài đó có thật không? | `EXT_ID:<PMID> AND SRC:MED`, đòi `hitCount == 1` và pmid khớp | "bài tổng quan CÓ / KHÔNG TỒN TẠI" |
| 2. Nội dung | Bài đó có **đo/báo cáo** chỉ tiêu Y không? | tải `fullTextXML`, **đếm cụm từ** | "bài KHÔNG BÁO CÁO chỉ tiêu Y" |

Phép 1 đạt **không** suy ra được phép 2. Một review 29 nghiên cứu có thể có thật, đúng chủ đề,
đúng loài — mà bên trong **không hề trích xuất** chỉ tiêu bạn quan tâm.

## Quy trình

1. **Verify tồn tại:**
   ```
   curl -s 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID%3A<PMID>%20AND%20SRC%3AMED&format=json'
   ```
   Điều kiện đạt: `hitCount == 1` và `resultList.result[0].pmid == <PMID>`. Không đạt ⇒ **KHÔNG
   TÌM THẤY** — viết thẳng ra, tuyệt đối không bịa bài/DOI/số liệu.

2. **Lấy PMCID** để có toàn văn: thêm `resultType=core` vào cùng truy vấn, đọc trường `pmcid` và
   `isOpenAccess`. Không có PMCID / không open access ⇒ không kiểm được nội dung; nói rõ giới hạn
   đó thay vì suy đoán từ abstract.

3. **Tải toàn văn và đếm cụm từ:**
   ```
   curl -s 'https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML' -o rev.xml
   ```
   Strip tag rồi `re.finditer` đếm **từng cụm từ chỉ tiêu** (`"fecal IgA"`, `"sIgA"`,
   `"secretory"`) **cộng một cụm đối chứng RỘNG** (`"fecal"`) để phân biệt *bài không nói về
   chủ đề này* với *bài nói về chủ đề nhưng không đo chỉ tiêu này*.

4. **Đọc vài đoạn khớp của cụm rộng** để xác nhận chúng thuộc loại khác (ở ví dụ thật: 41 lần
   `fecal` nhưng toàn bộ là *fecal score / microbiota / shedding / SCFA* — không có lần nào là
   `fecal IgA`).

5. **Kết luận đúng mức:**
   - Được phép: *"Bài KHÔNG BÁO CÁO chỉ tiêu Y"* / *"chỉ tiêu IgA trong bài này là IgA huyết
     thanh, không phải IgA niêm mạc"*.
   - **Cấm** nâng thành: *"N nghiên cứu gốc đều không đo Y"* — câu đó chỉ nói được sau khi mở dữ
     liệu gốc của từng nghiên cứu.

## Vì sao đếm cụm từ tốt hơn đọc abstract

- Abstract nhiều bài **không nêu** chỉ tiêu miễn dịch nhưng full text thì có, và ngược lại.
- Từ khoá có thể nằm ở **phần Phương pháp** (mô tả phép đo) mà không xuất hiện ở Kết quả — hoặc
  ngược lại. Đếm thô cả bài rồi **đọc ngữ cảnh** là cách duy nhất chắc.
- Rẻ hơn và khách quan hơn đọc lướt: cho ra một con số để đối chiếu lại sau.

## Bẫy

1. **Hit trong truy vấn chủ đề ≠ nghiên cứu đo chỉ tiêu đó.** Một bài khớp truy vấn
   `"sIgA" AND piglet` có thể chỉ đo **IgA đặc hiệu kháng nguyên do VẮC-XIN** — cùng chữ, khác
   bản chất. Luôn đọc ngữ cảnh trước khi tính nó là bằng chứng cho chất can thiệp.
2. **Chỉ tiêu "gần giống" phải gọi đúng tên, không gộp.** Ví dụ thang cho IgA niêm mạc:
   IgA tiết trong **phân** (mức 1) > IgA **đặc hiệu kháng nguyên** trong phân (do vắc-xin) >
   sIgA **mô / chất chứa ruột** > IgA **huyết thanh/huyết tương**. Ba mức sau **không** thay thế
   được mức 1.
3. **Chiều tác động có thể ngược nhau giữa loài** (cùng một chất: tăng ở loài này, giảm ở loài
   kia). Ghi cả hai ra và để vào "việc còn nợ" — đừng suy từ cơ chế sang kết luận.
4. **Cần đối chứng về chính phép đo.** Một bài **không dùng chất mình quan tâm** nhưng đo cùng
   chỉ tiêu trên cùng loài (có đơn vị định lượng) là bằng chứng quan trọng rằng **phép đo khả
   thi** — đưa vào nhưng ghi rõ nó không phải bằng chứng cho chất mình cần.
5. **Liều/đơn vị không có trong abstract ⇒ ghi rõ thiếu nguồn, không suy.** Và luôn **đổi về
   một đơn vị đích** để đối chiếu được với thiết kế đang cân nhắc (ví dụ mg/kg thức ăn → kg/tấn:
   `200 mg/kg = 0,20 kg/tấn`).
6. **Toàn văn có PMCID mới kiểm được.** Nếu không lấy được full text, hạ kết luận xuống mức
   trung thực *"chưa kiểm được nội dung"* — không đoán.
