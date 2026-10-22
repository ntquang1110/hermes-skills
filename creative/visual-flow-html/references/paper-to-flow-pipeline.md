# Paper → Flow HTML: recipe đầu-cuối (verified 12/10/2026)

Case gốc: user gửi link `https://pubmed.ncbi.nlm.nih.gov/41086516/` kèm yêu cầu "giải thích cho em hiểu nhanh, visualize cái gì chặn cái gì, cái gì tác động cái gì".
Deliverable: 1 file HTML 7 phần + link preview + 2 ảnh (desktop/mobile).

## 0. Resolve nguồn TRƯỚC, đừng đoán từ tên chất

User hay mô tả bài bằng giọng nói (STT) → thuật ngữ bị bóp méo ("ori minxinil") và có thể KHÔNG phải chất của bài.
Bài thật là berberine hydrochloride × PEDV, không phải oridonin như tên đoán ban đầu.
**Luật:** có PMID/link thì đọc nguồn trước khi dựng bất cứ thứ gì; chốt đúng tên chất + cây nguồn rồi mới chọn thuật ngữ.
Nếu buộc phải đoán, nói rõ "nghe giống X, em kiểm lại" và verify bằng nguồn thứ hai (vd PMC review về nguồn gốc thực vật).

## 1. Lấy abstract khi trang PubMed chặn cookie

`web_extract` trên `pubmed.ncbi.nlm.nih.gov/<PMID>/` có thể trả "Cookies must be enabled" (rỗng nội dung).
Đường đi thẳng, không cần cookie — E-utilities:

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=41086516&rettype=abstract&retmode=text"
```

Trả full abstract + journal/year/volume/DOI/PMID/conflict statement — đủ để dựng cả bài, không cần full text.
(Full text OA khi cần số chi tiết: `pmcoa.cgi/BioC_xml/PMC<id>/unicode` — xem skill `pubmed-evidence-research`.)

## 2. Chọn nguyên liệu trước khi viết HTML

Từ abstract, rút ra ĐÚNG 8 thuật ngữ và 1 chuỗi cơ chế 5 khâu. Ví dụ đã dùng (berberine × PEDV):

| Loại | Ví dụ |
|---|---|
| Chất | berberine hydrochloride (BBH) |
| Cây nguồn | Coptis chinensis / Berberis vulgaris (hoàng đằng, hoàng liên) |
| Dòng tế bào | Vero-E6 (thận khỉ) |
| Protein đo | N protein (nucleocapsid) |
| Marker | LC3-II |
| Chất công cụ | rapamycin (bật autophagy để làm rescue experiment) |
| Phương pháp | time-of-addition |
| Tăng/giảm | titer virus, viral load ruột non (tá tràng/hỗng tràng/hồi tràng) |

Chuỗi 5 khâu: bám (attachment) → nội bào hóa → bật autophagy → sao chép + lắp N protein → tổn thương ruột → tiêu chảy → chết.
Mắt xích vàng = khâu có rescue experiment chứng minh quan hệ nhân quả.

## 3. Cấu trúc HTML (7 phần, mobile-first)

1. Hero: tag `PMID ... · Journal Year;Vol:Page`, H1 có 1 cụm tô vàng, dòng nguồn có link DOI.
2. 3 stat: nồng độ an toàn tế bào / con số hiệu quả in vivo / số khâu bị chặn.
3. Card "chất này là cây nào" (1 đoạn, nói rõ chưa phải thuốc chính quy nếu bài gọi là adjunctive).
4. `<dl>` 8 thuật ngữ (dt vàng, dd xám).
5. Flow dọc: mỗi node = step label + tên khâu + 1 câu mô tả + chip `⊣ BBH chặn`. Node chặn viền đỏ, node quyết định viền vàng + chip `★`.
6. Card rescue experiment: câu hỏi → cách kiểm → kết quả → kết luận (kết luận nêu "chỉ một phần").
7. Card in vivo + card phê bình (đánh số 1..3) + 3 tầng màu (xanh/da cam/xanh lá) + footer nguồn.

CSS dùng token `dashboard-design-system`: `#0D0D0D` nền, `#1B1B1D` surface, `#FFD600` vàng, radius 18–22, breakpoint 420px hạ stats 3 cột → 1 cột.

## 4. Verify trước/sau publish

```bash
# 1. soát ký tự lạ + từ Anh lọt (bắt được 3 lỗi thật lần này)
grep -nP '[\x{3000}-\x{9FFF}\x{FF00}-\x{FFEF}]' berberine-pedv-flow.html
grep -n -oE '\b(also|and|the|with|from)\b' berberine-pedv-flow.html

# 2. serve local — ĐÚNG 1 listener
netstat -ano | grep ":8412" | grep -ic listen        # phải = 1
curl -s http://127.0.0.1:8412/<file>.html | wc -c    # KHÔNG dùng -o /dev/null -w %{size_download} (trả 0 sai)

# 3. render + screenshot (không cần Camofox, không cần vision model)
cp "C:/Users/NTQUANG_DELL/AppData/Local/hermes/skills/devops/camofox-browser/scripts/verify-html-render.cjs" \
   "/d/Hermes Proj/camofox-browser/verify-html-render.cjs"
cd "/d/Hermes Proj/camofox-browser" && node verify-html-render.cjs "http://127.0.0.1:8412/<file>.html" "./shots"
# qua khi: hOverflow false ở CẢ desktop + mobile, brokenImgs rỗng, có dòng DONE
```

Publish (User-Agent là bắt buộc, thiếu → Cloudflare 1010):

```python
payload = json.dumps({"content": html}).encode()
req = urllib.request.Request("https://preview.thefirstonly.com/api/store", data=payload,
    headers={"Content-Type":"application/json",
             "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Hermes/1.0"}, method="POST")
# → {"id":"ill8perzvbp4","preview_url":"https://preview.thefirstonly.com/ill8perzvbp4","size":12391}
```

**Ba bẫy của `/api/store` (verified 18/10/2026):**

1. **Mỗi POST tạo id MỚI, không ghi đè.** Sửa CSS rồi publish lại → id khác. Publish 3 lần trong 1 phiên là bình thường. Phải đưa user **id cuối cùng** và fetch-back verify đúng URL đó — đưa id lần đầu là user xem bản chưa sửa.
2. **Có thể chạy quá 60s** (nhất là payload vài chục KB). Bản `curl` nên để trần cao hơn:
   ```bash
   curl -s --max-time 120 -X POST https://preview.thefirstonly.com/api/store \
     -H "Content-Type: application/json" --data-binary @payload.json
   ```
   với `terminal(timeout=200)`. Timeout giữa đường KHÔNG chứng minh server chưa lưu — POST lại và lấy id từ response, tuyệt đối không đoán id.
3. **Script helper phải gọi bằng đường dẫn tuyệt đối.** `~` không phải lúc nào cũng expand trong lệnh terminal (exit 2, không log gì). Dùng `C:/Users/NTQUANG_DELL/AppData/Local/hermes/scripts/make_payload.py`.

Verify bản đã upload bằng probe chuỗi, không bằng HTTP status:

```python
html = urllib.request.urlopen(req_ua("https://preview.thefirstonly.com/<id>"), timeout=60).read().decode("utf-8")
for p in ["Hoàng đằng", "⊣ BBH chặn", "66.7%", "PMID 41086516"]:
    print(p in html)                                   # tất cả phải True
print([c for c in set(html) if '\u3000' <= c <= '\u9fff'])  # phải rỗng
```

## 5. Trả lời user

Link preview + 2 ảnh `MEDIA:<path>`, kèm danh sách phần đã verify (không nói chung chung "đã kiểm tra").
Copy ảnh ra thư mục KHÔNG có dấu cách trước khi gửi (`$HOME/httptmp/...`): path có space có thể làm gãy `MEDIA:`.
Cuối cùng chốt 1 câu: bài sau gửi link, dựng cùng format.
