---
name: pubmed-evidence-research
# Support files — Europe PMC verification recipe + gotchas: references/europepmc-rest-quirks.md
# Mechanical PMID/number audit before shipping: scripts/verify_pmid_claims.py
description: "Use when research needs verified PubMed PMID/DOI citations."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [PubMed, NCBI, E-utilities, Evidence, Citations, Literature-Review, Vietnamese]
    category: research
    related_skills: [grounded-citations, web-research, research-reporting]
---

# PubMed Evidence Research

Structured scientific literature research where every cited PMID/DOI is verified against NCBI before it goes into the deliverable, and each claim carries an explicit evidence grade. Produces reliable, auditable evidence bases (JSON knowledge bases, regulatory/veterinary/medical reports, ingredient-safety briefs) — often in Vietnamese for Vietnamese clients.

## When to use
- Compound/element/drug × species/effect review tables (e.g., "tác dụng/độc tính của X trên heo") where each row = 1 form × 1 effect.
- Any deliverable whose references MUST be real (client reports, regulatory contexts, safety claims). "KHÔNG bịa PMID" is the standing rule.
- Multi-group projects (NHÓM 1..N) where later groups reuse earlier verified findings.

## Core rules
1. **Never invent a PMID, DOI, or patent number.** No data for a specific species/form → write `Không có bằng chứng trực tiếp` (no direct evidence) + cite a general review on the topic. An empty `pmid`/`doi` field beats a guessed one.
   - **Xếp hạng nguồn rủi ro của một PMID (từ tệ nhất):** (1) **PMID nhớ ra từ trí nhớ** — hạng SAI cao nhất, và nguy hiểm vì nó *cảm thấy* chắc chắn; (2) PMID suy ra từ "số gần đúng"; (3) PMID gán theo **vị trí trong hit list**; (4) PMID đã đọc title trong chính session này. Chỉ (4) được vào deliverable.
   - Ca thật 18/10/2026 (fixgby `08-hanh-vi-giu-ma-giam`): **6/126 PMID nhớ-ra tra ra bài hoàn toàn khác chủ đề.** `30004572` "nhớ là" Cochrane NRT 2018 → thật là bài **antiphospholipid**; *Cochrane NRT đúng là **29852054***. Các ca khác cùng lượt: kombucha SCOBY (`34068887`), kháng kháng nấm (`32301159`), azole-sulfonamide (`38989985`), cold-plasma ung thư phổi (`30342190`), chất lượng môi trường trong nhà (`38732999`), van động mạch chủ (`38093919`). **Luật: resolve MỌI PMID qua Europe PMC và đọc title THẬT trước khi viết — kể cả (nhất là) PMID bạn "chắc chắn đúng".** Một PMID nhớ ra mà sai thì tìm lại bằng `TITLE:`/`TITLE_ABS:`, **không** đoán số gần đúng.
2. **Never claim relevance from a search hit list.** Triage titles first — PubMed hits are noisy ("gadolinium pig" returns MRI contrast studies, "holmium pig" returns lasers and fiber optics). Concrete case (16/08/2026): PMID 32992929 "Effects of Dietary Andrographolide Levels on Growth Performance, Antioxidant Capacity, Intestinal Immune Function and Microbioma..." (Animals 2020) looked like a pig trial but the abstract shows RICE FIELD EEL (Monopterus albus) — species must come from the abstract, never the title.
3. **Record species/model/dose from the abstract**, not the title. A mouse-colitis paper is NOT pig evidence — say so in the row. **Homonym species names are the single biggest search trap in pig/livestock work: `guinea pig` = chuột lang (*Cavia porcellus*), NOT heo (*Sus scrofa*).** Queries containing `pig` / `piglet*` match thousands of "guinea pig" papers (pharmacology, otology, myopia, sleep, depression models). Verified 18/10/2026: `TITLE_ABS:(piglet* OR piglets) AND TITLE_ABS:("maternal separation" OR "early weaning")` returned guinea-pig-pup "depressive-like behaviour" papers — PMIDs 37529896, 27374759, 35191529, 40059538, 30666192 — that read exactly like piglet depression models. Same contamination in `TITLE_ABS:(cortisol OR corticosterone) AND pig`. Guard: after triage, require `Sus scrofa` / `swine` / `porcine` / `minipig` / `Göttingen` / `Yorkshire` / `Bama` / `Yucatan` / `Landrace` in the ABSTRACT, and drop anything naming *Cavia porcellus* or "guinea pig". Say in the deliverable that you screened for this, so the client knows it was checked.
4. **Patents**: verify via the Google Patents XHR endpoint (`https://patents.google.com/xhr/query?url=q%3D<kw>%26oq%3D<kw>`) — its JSON carries id, title, assignee and priority_date in `results.cluster[0].result[].patent`, which is enough to verify a patent WITHOUT fetching the detail page. The XHR rate-limits hard after ~3–4 requests (empty responses) — run all queries in one script with sleep ≥3s and use quoted phrase queries (`'"production of tannin" extract wood'`) because keyword search is full-text fuzzy and very noisy. The detail HTML pages (`patents.google.com/patent/...`) are the part that returns the ~1KB "Sorry" block; if blocked there, keep the XHR-verified metadata and write `trang chi tiết bị chặn` in the note — never guess abstract/claims content. If even XHR is blocked, write `chưa verify` and include NO patent numbers.
5. **For supplement/TPBVSK actives, verify the HUMAN RCT — don't trust "known/traditional" recall.** Familiar botanicals can be weak or negative on check: shilajit BPH data is RAT-only (drop), saw palmetto 320mg failed big trials (Bent 2006 NEJM, no benefit vs placebo), silymarin lowers enzymes but missed the histology endpoint (Kheong 2017 — enzyme-only, not "reversal"), oral GABA barely crosses BBB (drop). Prefer the human-solid hero (beta-sitosterol for BPH, ashwagandha+L-theanine for stress, bacopa 300mg for cognition but slow 8–12wk, carrageenan nasal, ivy-leaf EA575+honey for kids' cough). Full bank + correction case: `references/human-supplement-actives-evidence.md`.
6. **Tồn tại ≠ đúng chỗ. Kiểm TRA CẢ HAI cổng.** Cổng 1 = PMID có thật (Europe PMC `hitCount==1`). Cổng 2 = **title khớp claim mà nó chống đỡ**. Cổng 1 tự động được; cổng 2 là chỗ lỗi thật sự xảy ra và là cổng hay bị bỏ qua nhất.
   - Ca thật 18/10/2026 (07b fixgby): **153/153 PMID tồn tại thật**, nhưng audit title-vs-claim bắt **~12 citation gắn sai hoàn toàn chủ đề** — `17456850` ghi là "occludin knockout" nhưng thật là Cani *metabolic endotoxaemia*; `28654658` ghi là "LBP" nhưng thật là butyrate→AMPK→TJ trên tế bào ruột HEO; `22410503` ghi là "LPS/sCD14" nhưng thật là IgA/IgM ở trầm cảm; `21151103` ghi là "AMPK/PGC-1α" nhưng thật là autophagy→mtDNA→miễn dịch bẩm sinh; `7678183` ghi là "IL-6 rò rỉ" nhưng thật là TNF-α từ mô mỡ.
   - **Nguyên nhân gốc:** gán PMID theo **vị trí trong danh sách kết quả tìm kiếm**, không theo title đã đọc. Deliverable vẫn "verify sạch" nếu chỉ đếm tồn tại → lỗi đi thẳng tới khách hàng.
   - **Luật:** ghi cặp `(pmid → title thật)` **ngay lúc retrieve** (Europe PMC trả title trong cùng response — không tốn thêm call), và chỉ dựng claim từ title **đã đọc trong chính session**. Hit list chỉ để triage, không bao giờ để gán.
   - **Trước khi bỏ một PMID vì "sai chủ đề", luôn đọc title của nó** — nhiều bài "thừa" hoá ra **tốt hơn** bài định dùng (17456850 hoá ra đúng là bài gốc của trục gut→endotoxaemia; 28654658 hoá ra là nguồn **trên heo** cho cạnh butyrate→AMPK→TJ). Gán lại rẻ hơn đi tìm bài mới; không có bài nào chống đỡ thì xoá dòng và ghi `CHƯA CÓ NGUỒN (tag H)`.
   - **Dòng KHUNG/ĐỊNH NGHĨA hút PMID sai mạnh nhất — vì chúng không đo kết cục nào cả.** Ca thật 18/10/2026 (`08-hanh-vi-giu-ma-giam`), 4 ca mis-assign trong chính bản nháp ĐẦU: `28441725` (thụ thể ngọt ruột **chuột**) bị gắn vào dòng *"cửa 5 — cơ thể tự sinh"*; `25332472` (thay NƯỚC cho SSB) gắn vào dòng *"dạng rắn vs dạng lỏng"*; `26636424` (OmniCarb, bài về **acid uric**) viết thành *"GI thấp KHÔNG cải thiện yếu tố nguy cơ tim mạch"* — abstract cho chiều **NGƯỢC** (GI thấp **giảm** uric −0,24 mg/dl); `22104550` (DiOGenes) viết thành *"đạm cao giữ cân"* trong khi kết luận nằm ở **giảm viêm mức thấp**. **Ba loại dòng dễ dính nhất: dòng mô tả KHUNG ("cửa 5", "lỏng vs rắn", "đạm cao"), dòng CƠ CHẾ SUY LUẬN, và dòng kiểu *"xác nhận N1"*. Với những dòng này TAG H là câu trả lời đúng, không phải bài gần giống nhất.**
   - Recipe audit đầy đủ (dump `PMID | title thật | dòng thật trong file`, xử lý report 14 KB, và **bẫy**: heuristic "token overlap" flag oan 127/155 vì dòng danh sách `**(f) PMID chủ đạo**: ...` không chứa từ cơ chế nào) + cách bulk-edit tài liệu lớn: `references/citation-attribution-audit.md`.
7. **Cổng 2 có HAI lớp lỗi — lớp thứ hai là SAI MÔ, và nó sống sót qua audit chủ đề.** Xong lớp 1 (title khớp chủ đề) chưa phải xong:
   - **Lớp 1 — sai chủ đề:** title thật nói chuyện khác hẳn (xem bảng §1 trong reference).
   - **Lớp 2 — sai MÔ:** title đúng chủ đề, cơ chế đúng, nhưng nguồn đo ở **cơ quan khác** với cơ quan tài liệu đang nói tới. Claim đọc lên vẫn hoàn toàn đúng nên mắt người gật. Ca thật 18/10/2026 (`07b`): `29410610` gán cho "thiếu máu-tái tưới máu **gan/thận**" nhưng thật là **phù não do ngộ độc 1,2-dichloroethane**; `37245680` gán cho ruột nhưng thật là **tế bào ốc tai**; `25063198` gán cho "occludin → hàng rào **ruột**" nhưng thật là bài **ĐIẾC ở chuột thiếu occludin (tai trong)**. Cột `(I)/(A)/(R)` là *loại đối tượng*, KHÔNG phải *mô* — hai chiều độc lập, phải ghi cả hai.
   - **Lớp 3 — sai CHẤT ANH EM trong cùng một lô (mới, 19/10/2026).** Khi một lô chứa nhiều chất **cùng nhóm dược lý / cùng dấu hiệu**, nguồn của chất này bị gán cho chất kia. Lớp lỗi này **sống sót qua cả cổng 1 lẫn cổng 2 lớp 1** vì chủ đề, cơ chế, mô và loài đều ĐÚNG — chỉ sai *phân tử*. Ca thật (fixgby `09-tra-cuu-duong-di` lô B: sắt · canxi · curcumin · paracetamol · ibuprofen): **`30562214`** — title thật *"…self-adjusted **ibuprofen** dose in the Coriell Personalized Medicine Collaborative"* (n=445) — bị gán cho **chặng 8 của PARACETAMOL**, kèm câu *"no early signs of acute kidney injury"* (câu đó thuộc bài ibuprofen). Bài này **đã** được gán đúng ở một chỗ khác trong cùng file ⇒ lỗi là **tham chiếu chéo giữa hai chất cùng lô**, không phải PMID hỏng. **Cách bắt:** render bảng **`PMID | title thật | tên chất mà dòng đó nói tới`** rồi kiểm tên CHẤT trong title có khớp khối chứa nó không; grep tên các chất anh em (ibuprofen / paracetamol / APAP / acetaminophen) trên toàn tài liệu và xem dòng nào nằm sai khối. **Bẫy trá hình:** rất nhiều tên chất **không xuất hiện nguyên dạng trong title** (tiêu đề chỉ ghi "calcium", "heme-iron", "claudin-2") nên cờ *"tên chất không có trong title"* là **dương tính giả** — phải đọc ABSTRACT mới phân xử, đừng xoá nguồn chỉ vì cờ đó (lô B: 38 cờ, chỉ **1** là lỗi thật).
   - **Luật:`số nguồn` KHÔNG phải `điểm bằng chứng`.** Khi một cạnh có N nguồn nhưng chỉ k nguồn đo ở **đúng mô đích**, chấm theo **k** và ghi rõ `k/N nguồn đúng mô`. Ca thật: cạnh `C1` có **3 nguồn** và đang xếp "ĐÃ CHỨNG MINH", sau audit **chỉ 1/3 là ruột** → phải hạ xuống "**CHỨNG MINH MỘT PHẦN**". Ngoại suy liên cơ quan là **giả định**, không phải chứng minh — viết thẳng câu đó vào dòng.
   - **Audit đúng nguồn có thể ĐẢO CHIỀU kết luận, không chỉ hạ bậc.** Ca thật: tài liệu dùng chuột thiếu occludin để chống đỡ điểm chạm "KÍCH tổng hợp occludin"; title thật của nguồn thay thế (`11102513`, `9548718`) cho thấy **mất occludin KHÔNG phá được tight junction** (tế bào gốc phôi thiếu occludin vẫn tạo được TJ) ⇒ occludin là protein **điều hoà**, không phải protein chịu lực duy nhất ⇒ **cả một hướng điểm chạm đi sai**. Luôn hỏi: nguồn này có đang chống đỡ được chiều mình muốn không, hay chỉ chống đỡ được **cơ chế** mà thôi.
   - **Đừng tin danh sách đã sửa của lượt trước.** Ở lượt QC này, một PMID mà phiên trước đã "sửa cho đúng" (`25063198`) hoá ra chính nó lại sai mô. Lượt audit sau phải kiểm lại **cả những PMID đã được sửa**.
   - **Quét MÂU THUẪN NỘI BỘ sau mọi lượt bulk-edit (bước bắt buộc, hay bị bỏ):** bulk-edit sửa từng dòng độc lập nên **bảng tóm tắt cuối tài liệu thường còn bản CŨ**. Ca thật: `F.2` trong **cùng một câu** vừa nói "6/6 cạnh có bằng chứng" vừa kết "4/6"; bảng tra nhanh vẫn ghi 4/6 trong khi bảng cạnh `A.4.3` đã thành 5/6; `A.4` dùng "**đã chứng minh**" cho một vòng xoáy mà chính tài liệu ghi là chưa ai chứng minh. Checklist 5 bước (grep mọi con số đếm rồi so nhau; đối chiếu bảng cuối vs thân bài; hạ động từ khẳng định về mức bằng chứng thật; `tag H` ở thân phải xuất hiện lại ở kết luận; mục "còn mở" phải liệt kê đủ khoảng trống): §5 reference.
   - **Tự công bố GIỚI HẠN của chính phép verify, ngay trong deliverable.** `verified N/N` rất dễ bị đọc thành "tài liệu này đã đúng" ⇒ viết thẳng khối "GIỚI HẠN CỦA CHÍNH PHÉP VALIDATE NÀY" (những gì đã kiểm / chưa kiểm) + **danh sách đánh số các chỗ đã sửa** ở lượt QC. Nguyên mẫu khối này: §6 reference.
8. **Chấm điểm BẰNG CHỨNG, không chỉ kiểm PMID tồn tại — bốn bẫy thẩm định hay gặp nhất (20/10/2026).** Cả bốn đều sống sót qua `hitCount==1` và qua cả cổng title-khớp-claim, vì chúng sai ở tầng *thiết kế nghiên cứu*, không phải tầng *trích dẫn*:
   - **B1 — liều của SẢN PHẨM ≠ liều HOẠT CHẤT.** Phụ gia thương mại thường chỉ chứa 5–30 % hoạt chất. Ca thật: hai nghiên cứu "200 mg/kg" ra dương tính thực chất chỉ đưa **~18 mg đất hiếm/kg** (sản phẩm 5,1–5,7 % La + 3,3 % Ce + chitosan/diatomite), tức **1/10–1/20** liều một nghiên cứu Đức "200 mg/kg premix đậm đặc" ra **âm tính**. Hệ quả lập luận: nếu hiệu quả có thật thì rất có thể đến từ **chất mang**, và nhánh đối chứng "chỉ chất mang" hầu như luôn thiếu. **Luật: quy MỌI liều về `mg hoạt chất/kg` trước khi so sánh; số quy đổi ghi rõ "tính của tôi từ % công bố", không trình bày như số của bài gốc.**
   - **B2 — trùng công bố (duplicate publication) làm 2 nghiên cứu thành 1.** Cùng nhóm tác giả + **cùng con số đầu bài** (ca thật: 19 % ADG & 11 % FCR xuất hiện y nguyên ở bài 2001 và 2002 của cùng nhóm) ⇒ gần như chắc chắn một bộ dữ liệu in hai lần. Đếm thành "hai nguồn độc lập" là thổi bằng chứng gấp đôi. **Cách bắt: so cặp (nhóm tác giả, con số) giữa các hit rồi gộp dòng.**
   - **B3 — "không tồn dư / negligible" mà KHÔNG có số thì không phải bằng chứng, và review sẽ lan truyền nó.** Ca thật: nghiên cứu n=14 khẳng định "very low" mà không in một con số nào; nghiên cứu GLP n=128 ICP-MS cho thấy **gan tăng ≈10 lần**; một review vẫn lặp lại luận điểm "no residual" dựa trên bài n=14. **Luật: thấy claim định lượng không kèm số ⇒ đi tìm nghiên cứu GLP có bảng số, và ghi thẳng mâu thuẫn vào deliverable thay vì chọn bên thuận.**
   - **B4 — "không có MRL/ADI" ≠ an toàn.** Phải viết hệ quả vận hành: không có ngưỡng ⇒ **không có chỉ tiêu để phòng kiểm nghiệm bắt lỗi, và không có vạch để doanh nghiệp chứng minh mình trong giới hạn**. Đừng để câu "không tìm thấy giới hạn" trôi thành "yên tâm".
   - **Kèm luật chấm cơ chế:** đừng chấm theo **số lần được nhắc**. Ca thật: cơ chế được viện dẫn nhiều nhất (ổn định hệ vi sinh) lại là cơ chế **bị chính nghiên cứu mạnh nhất phủ định**, còn cơ chế có bằng chứng mạnh nhất lại là **tác dụng BẤT LỢI**. Trong JSON, mỗi cơ chế phải có **`bang_chung_phan_bac`** bên cạnh `bang_chung_ung_ho`.
   - **Phép tính của chính mình phải dán nhãn.** Khi so NOAEL với liều thực tế (vd "heo 20 kg ăn 1 kg/ngày ⇒ 1,06 mg La/kg thể trọng/ngày ⇒ ~29× NOAEL chuột"), ghi rõ `phep_tinh_cua_toi` + `canh_bao` rằng đây là so sánh khác loài/khác đường phơi nhiễm, **không** dùng để kết luận "gây tổn thương". Người đọc sau phải phân biệt được số của bài với số của agent.
   - Bank đầy đủ + ca mẫu (đất hiếm cho heo, 21 PMID): `references/rare-earth-feed-additive-pigs-notes.md`.

## Publish rule (bắt buộc)
Khi một deliverable nghiên cứu hoàn thành (bài phân tích, brief, report, bất kể có PMID hay không): **publish lên server của mình và trả link `preview.thefirstonly.com` bằng KV `POST /api/store`** (KHÔNG trả link gist — user dùng preview.domain, không xài gist. **SỬA LỖI 12/10/2026:** câu cũ "HÀNG RÀO: KHÔNG dùng script `content-upload.py` vì nó CHỈ tạo GitHub Gist" là SAI. Verify trên máy Quang: `content-upload.py` mặc định gọi `upload_to_kv()` tức POST thẳng `/api/store`, `--gist` mới là opt-in. Câu cũ đã gỡ. Có thể dùng script bình thường, chỉ là `--file` đọc file tiếng Việt tốt hơn stdin. **Bẫy thật duy nhất:** `upload_to_kv` dùng `requests.post()` trần, không truyền proxy → SSL handshake treo rồi `ReadTimeout` 30s. Cùng POST đó chạy được với `requests.post(..., proxies={"http": None, "https": None})`, tức proxy env đang nhiễu `requests` nhưng không nhiễu `curl`.). Cách đúng: build HTML (Premium B/W/Y), ghi payload `json.dumps({'content':...,'title':...})` ra file, rồi `curl -s -X POST https://preview.thefirstonly.com/api/store -H "Content-Type: application/json" --data-binary @payload.json` → trả `preview_url`. Luôn dùng `curl`, python urllib bị 403. Xem `references/markdown-to-preview.md` để biết bước convert markdown→HTML (worker preview chỉ serve `index.html`; `.md`/`.txt` trả 404). Verify HTTP 200 (`curl -s -o /dev/null -w "%{http_code}" "<url>?bust=1"`) trước khi báo xong. KHÔNG tự ý đăng lên Threads account — bài research lệch 3 kênh Threads đang chạy (tâm lý / MIT macro / HLL podcast). Chỉ khi user chỉ định tên kênh cụ thể mới định tuyến sang Threads.

## Workflow
1. **Batch esearch** (`execute_code` looping `curl`):
   `esearch.fcgi?db=pubmed&term=<url-encoded>&retmax=15&retmode=json`
   URL-encode synonyms: `cerium+oxide+nanoparticle+AND+(pig+OR+swine+OR+porcine)`.
   **Sleep ≥0.7s between calls** — unauthenticated limit is 3 req/s; exceeding it returns `{"error":"API rate limit exceeded"}`.
2. **Triage with esummary** (one call, comma-joined ids):
   `esummary.fcgi?db=pubmed&retmode=json&id=1,2,3` → title/journal/pubdate per PMID. Discard false positives here.
3. **Verify with efetch**:
   - Abstracts: `efetch.fcgi?db=pubmed&rettype=abstract&retmode=text|xml&id=...`
   - Exact DOIs: **cheapest path is esummary JSON, not efetch** — each record's `articleids` list carries `{"idtype":"doi","value":"10.xxxx/..."}`. One esummary call does triage + DOI extraction:
     `dois=[a['value'] for a in r.get('articleids',[]) if a['idtype']=='doi']`.
     Fall back to efetch XML (`<ELocationID EIdType="doi">`) only when esummary lacks the DOI (old papers).
   - **Abstract missing or too thin → pull open-access full text** (reviews often carry the exact numbers the abstract truncates or omits): `https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC<id>/unicode` (PMC id from the `PMCID: PMCxxxxx` line). Strip tags with regex, then grep for `inactiv|chlorine|°C|freez|surviv|sediment|ppm` — this recovered 100 ppm NaOCl/10 min, 10-month soil persistence, and 70 ppm formalin numbers from one review's full text.
4. **Cite only what you read**, with a `note` stating what the paper actually showed (species, dose, direction of effect).
5. **Write the deliverable** with the conventions below; put the verification date + method in a `verification` field per row.
6. **Self-check before finishing** (run `scripts/check_deliverable_pmids.py`): every `pmid` in the output JSON must be in the set of PMIDs actually efetched THIS session. An esummary title alone is NOT a verified citation — if a fact needs a paper you only triaged, efetch it before writing the JSON (observed: a temperature-stress fact nearly shipped on title-only; caught and re-verified). Also: briefs often cite classic papers with wrong year/author metadata (e.g. "Huang 2014 clathrin" was actually Huang J 2015 PMID 26397221 + Huang ZJ 2013 PMID 23747417; "Yi 2004" = PMID 15607033). Resolve via `Author[Author] AND topic` esearch, then note the corrected mapping in the deliverable's `note`/`verification` field.

## Europe PMC REST — the faster verify path (use alongside E-utilities)
For deliverables that need MANY PMIDs read (50-100 abstracts), the E-utilities chain (esearch→esummary→efetch) is 3 calls per paper. **Europe PMC returns the full abstract in the search response itself** — 1 call. No API key, no observed rate limiting.
```
https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=<url-encoded>&format=json&pageSize=1&resultType=core
```
- `resultType=lite` → titles only, small payload → use for **triage** (`pageSize=8..15`, `&sort=CITED%20desc` to surface landmark reviews instead of the newest noise).
- `resultType=core` → also returns `abstractText`, `doi`, `pmcid`, `journalInfo` → use for **verification**. Query one PMID at a time with `EXT_ID:<pmid>`; batch several with `EXT_ID:a OR EXT_ID:b` (batch ~40 per call is comfortable — 101 PMIDs verified in 3 calls; see `scripts/validate_pmids_batch.py`). **Build that batch query with `urllib.parse.urlencode` on a dict — do NOT hand-quote a curl string:** verified 18/10/2026, `curl -s '...query=EXT_ID:a OR EXT_ID:b&...'` written inline inside `execute_code` returned an EMPTY body (the shell ate the nested quotes) and `json.loads` then died with `Expecting value: line 1 column 1 (char 0)` — which reads as a network/API failure but is a **quoting** failure. The identical query via `urllib.request.Request` + `urlencode({"query": ...})` worked first try. If an inline curl returns empty while the URL looks correct, suspect quoting before suspecting the endpoint.
- Field-scope every query (`TITLE_ABS:"..."`, `TITLE:"..."`) or `hitCount` explodes into recent irrelevant records.
- **Two parse traps:** (a) a 10-result `core` payload is ~20KB → captured stdout truncates → save to file; (b) abstracts contain raw control characters → **`json.loads(s, strict=False)`**. Full recipe, cookbook and working helper: `references/europepmc-rest-verification.md`.
- Preprints surface here with no `pmid` and a DOI like `10.1101/...` / `10.64898/...` — cite the DOI and **flag them as not peer-reviewed**; never let one carry a load-bearing claim.
- `NO ABSTRACT` is a real outcome (conference abstracts/editorials) → verify title+DOI and say in the deliverable that only metadata was confirmed.

### Toàn văn + BẢNG SỐ: `PMC<id>/fullTextXML` (không key, không CAPTCHA)
Khi abstract không có số định lượng (rất hay gặp ở bài động vật học), đừng dừng ở abstract và đừng mở browser:
```
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC<pmcid>/fullTextXML
```
`pmcid` lấy từ chính response `resultType=core` (`x.get('pmcid')`). Trả JATS XML đầy đủ, kể cả `<table-wrap>`. Nhanh hơn `pmcoa.cgi` và không cần key.
- **Bẫy: strip tag thành DẤU CÁCH làm bảng dính thành văn xuôi không đọc được.** Để giữ ô bảng, thay tag bằng **`|`** rồi gộp `|+` → `|`:
  ```python
  t = re.sub(r'<[^>]+>', '|', xml); t = html.unescape(t); t = re.sub(r'\|+', '|', t)
  i = t.find('Performance of nursery pigs')   # caption bảng
  print(t[i:i+1800])                          # -> 'RECC0|RECC200|...|ADG (g/d)|395.14 ± 4.78|c|446.25 ± 3.04|a|...'
  ```
  Ca thật 20/10/2026: `web_extract` trên trang MDPI render ra `Table 1.` **rỗng** (bảng là ảnh/JS), trong khi JATS XML cho đúng ADG `395,14 → 446,25 g/ngày` và tiêu chảy `18,39 % → 5,89 %` — chính hai con số mà deliverable cần.
- **Bảng có thể VẮNG trong XML** (hình ảnh, hoặc chỉ có trong PDF). Khi đó ghi `số tuyệt đối trong Bảng X của bài, không trích được từ XML` và chỉ báo **chiều + p-value**. Tuyệt đối không dựng lại số từ trí nhớ hay từ hình.
- EFSA FEEDAP opinion trên Europe PMC cũng đi đường này: cho đúng **bảng thành phần** (vd `La 8,5 % · Ce 16,3 % · Pr 2,0 %`), **bảng tồn dư theo mô/ngày**, và **bảng NOAEL** — spec công nghiệp + liều + độc tính trong một lần gọi.

### Văn bản pháp lý bị chặn → đường vòng đã kiểm chứng
- **EUR-Lex `eli/.../oj/eng` trả `bot_blocked`** (cả trang `annex`). Dùng mirror Anh: `https://www.legislation.gov.uk/eur/<year>/<number>/introduction/adopted/data.html` → ra đúng phần "Whereas" + ngày + tên chủ giấy phép. Nếu annex cũng chặn, trích **số văn bản + ngày + nội dung từ phần introduction** rồi ghi rõ mức chắc chắn.
- **Công báo/quy chuẩn VN**: tải PDF gốc rồi `pymupdf` + regex cụm từ khoá, **in ra số trang** — đây là bằng chứng mạnh hơn "tôi nhớ là có trong Phụ lục VI". Ca thật: xác nhận "Lanthanide" (tr.20) và "Lanthanum carbonate octahydrate" (tr.21) trong Phụ lục VI TT 21/2019.
- **Danh mục TQ** (《饲料添加剂品种目录》) không có trang tra cứu mở; xác nhận gián tiếp qua **PDF văn bản hướng dẫn thi hành của địa phương** dẫn chiếu danh mục — và ghi `mức chắc chắn: trung bình`.

## Output conventions (JSON knowledge-base style)
One row per compound-form × effect:
```json
{"id":"slug","element":"...","element_vi":"...","name_en":"...","effect":"...","group":"...","mechanism":"...","evidence_level":"Vừa","dosage_ref":"...","side_effects":["..."],"references":[{"type":"paper","label":"...","pmid":"","doi":"","note":"..."}],"verification":"..."}
```
- `evidence_level` ∈ {`Mạnh` (strong: reviews/human+animal corroboration), `Vừa` (moderate: direct trials, n≥1), `Sơ bộ` (preliminary: single model / rodent only), `Không có bằng chứng trực tiếp` (no direct evidence — state what the closest evidence is)}.
- Keep Vietnamese diacritics; write `ensure_ascii=False` when dumping JSON.
- File layout: `os.makedirs(data_dir, exist_ok=True)`; one JSON per group; print row count + verified-PMID count + path at the end.
- Template: `templates/evidence_row_template.json`.

### Second shape: Q&A review markdown (khi brief là câu hỏi, không phải bảng)
Khi deliverable là "trả lời N câu hỏi về chủ đề X" (review khoa học, đánh giá mô hình), dùng cấu trúc đã kiểm chứng 18/10/2026 thay vì row JSON:
checklist table mở đầu (câu hỏi × có nguồn trực tiếp?) → một `##` mỗi câu, mỗi claim có `[PMID:...]`/`[DOI:...]` inline → rating tin cậy **CAO/TRUNG BÌNH/THẤP kèm lý do** → bảng đối chiếu cuối theo từng cơ chế → `## References` đánh số → **`## PHỤ LỤC` liệt kê mọi claim đã xác nhận `KHÔNG CÓ NGUỒN`**.
Hai điểm bắt buộc: (a) ghi rõ **nghiên cứu ÂM TÍNH** khi có — một mô hình thất bại là evidence hạng nhất, không được bỏ; (b) gắn cờ **preprint** riêng và không để nó gánh claim chính. Phụ lục "không có nguồn" chính là phần được đánh giá cao nhất — luôn giữ.

### Third shape: khung 8 chặng "đường đi phân tử" (`cua_vao` → `o_lai`)
Khi câu hỏi là *"chất này đi đường nào trong cơ thể"* (không phải *"có tác dụng gì"*), deliverable là **mỗi CHẤT = một khối 8 mục a→h, mỗi dòng một sự kiện**, không viết văn. Tám khoá đúng thứ tự:
`cua_vao` (4 cửa + `first_pass`) · `qua_hang_rao` (bơm ĐƯA VÀO, họ SLC/OATP) · `gan_lan_dau` (CYP pha I) · `gan_de_di` (liên hợp pha II + **bám protein chở**) · `toi_mo` (mô đích + thụ thể) · `ra_khoi_te_bao` (bơm ĐẨY RA, họ ABC/MATE) · `thai` (5 cửa ra: thận/mật→phân/phổi/da/sữa, ghi % nếu có) · `o_lai` (t½ + tích luỹ). File `batch-*.json` = MẢNG object, mỗi chất một object.
Ba cặp dễ lẫn phải giữ tách: **2 ≠ 6** (vào vs ra), **3 ≠ 4** (CYP vs UGT/SULT), và **thụ thể ≠ enzyme** (statin/biguanid đích là ENZYME — HMG-CoA reductase / complex I; chỉ melatonin MT1/MT2 và omega-3 GPR120 mới có GPCR thật ⇒ đừng bịa "thụ thể" cho chất không có).
Ba khoá đời luôn phải điền: `bat_kha` (chất KHÔNG làm được gì) · `da_that_bai` (**bằng chứng ÂM TÍNH thật**) · `chi_dau_do_duoc` (chỉ số đo lặp lại trên cùng một cá thể).
Schema đầy đủ + trap + bank 46 PMID 5 chất: `references/molecule-pathway-8-stage-notes.md`.

**Nguyên liệu THÔ (dược liệu) hầu như KHÔNG có PK ⇒ cách viết đã kiểm chứng (20/10/2026, fixgby lô A: huyết dụ + lá hẹ):**
chặng nào không nguồn thì ghi **đúng một dòng** `CHƯA CÓ NGUỒN (tag H)` — không bỏ dòng, không suy diễn; nhưng vẫn
**chèn dòng "tham chiếu LOÀI KHÁC"** để giữ phần cơ chế đáng giá, với điều kiện **tên loài + mô của nguồn nằm ngay
trong cột "mô & loài" VÀ trong ô mức bằng chứng** (`(R) in-vitro — LOÀI KHÁC: C. stricta, LÁ`; `(A) in-vivo —
LOÀI KHÁC: gà thịt Ross 308`). Ví dụ đã dùng: β-glucosidase của *E. faecalis* phân lập từ ruột **chuột cống** cho
việc cắt đường của saponin; PK của SAC thuộc **TỎI** cho "họ hợp chất lưu huỳnh". Không có nhãn loài thì dòng tham
chiếu bị đọc thành số liệu của chính nguyên liệu đang viết — đó là lớp lỗi SAI LOÀI (§7 lớp 2), không phải sai chủ đề.
Kèm luật: **`muc_bang_chung` khai theo cấp cao nhất THẬT của chính loài đó** và phải nói rõ "chưa có cấp A trên HEO"
(không có nghiên cứu *A. tuberosum* nào trên heo; không có nghiên cứu *Cordyline* nào trên heo) — nếu không, người
đọc thấy `(A)` là tưởng đã có dữ liệu heo. Với nguyên liệu thô, `DANG_DUNG` là chỗ bắt buộc ghi rủi ro đã có nguồn:
lá tươi vs đã đun nóng (hẹ: `28216165` — mẫu tươi độc tế bào gan/thận chuột cống in-vitro, mẫu hấp thì an toàn) và
**lẫn rễ/thân vào lá** (huyết dụ: `34624728` — 10 glycosid từ RỄ vs 4 từ phần trên mặt đất).

**Shape thứ tư — 8 chặng của MẦM BỆNH** (không phải chất): `1_xam_nhap` → `8_thai_lay`
(`vào cửa nào · qua hàng rào · bám thụ thể/tế bào đích · nhân lên · lan hệ thống · tín hiệu hại · hậu quả · thải/lây`),
mỗi chặng có `node` sờ được + `pmid`, cộng `diem_cat` (kèm `kha_thi cao/trung/thap` và lý do kỹ thuật),
`bat_kha`, `da_that_bai`, `chi_dau_do_duoc`. Ranh giới: tầng bệnh **cấm đề xuất sản phẩm/chất** — chỉ vẽ
đường đi và chỉ điểm cắt. Schema + bank 39 PMID (5 virus + 4 ký sinh tiêu chảy heo) + 4 nút thắt:
skill `fixgby` → `references/duong-di-8-chang-cua-benh.md`.
**Ngân hàng lô nguyên liệu premix heo (7 chất, 61 PMID verified 61/61 — 19/10/2026) + kỹ thuật tăng hấp thu
(curcumin nano / TPGS ức chế P-gp) + Se hữu cơ vs vô cơ (thải qua SỮA) + MgO vs chelate (bằng chứng ÂM TÍNH):
`references/feed-additive-8stage-absorption-notes.md`.** Lô B **cùng thư mục** (nhóm enzyme · vi sinh · acid
hữu cơ: phytase/xylanase/protease dạng coated · *Bacillus subtilis* bào tử · calcium butyrate · acid citric ·
betaine HCl 98 %) có bank riêng, kèm **phán quyết về cảnh báo "enzyme mất 50–80 % hoạt tính ở pH 8–9"** và
cách khung 8 chặng áp cho chất KHÔNG hấp thu:
`references/feed-additive-8stage-enzyme-probiotic-notes.md`. Trước khi ship `batch-*.json`: chạy
`scripts/check_batch_schema.py <file>` — assert đủ 20 khoá + `pmid` trong cả 8 chặng, và in ra **|set PMID
duy nhất|** (con số đúng cho `verified N/N`; xem pitfall đếm hai lần).

## Pitfalls
- **Trang PubMed chặn cookie khi user dán link (verified 12/10/2026):** `web_extract` trên `pubmed.ncbi.nlm.nih.gov/<PMID>/` trả "Cookies must be enabled" — nội dung rỗng, tưởng như phải mở browser. Không cần: gọi thẳng E-utilities bằng PMID
  `curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=<PMID>&rettype=abstract&retmode=text"`
  → full abstract + journal/năm/volume/DOI/PMID/conflict statement. Đây là đường nhanh nhất cho câu hỏi kiểu "bài này nói gì, chất nào, cây nào, tác động đường nào" — không cần full text.
- **Chốt danh tính bài TRƯỚC khi dựng deliverable (verified 12/10/2026):** user thường mô tả bài bằng giọng nói (STT) nên thuật ngữ bị bóp méo — "ori minxinil" nghe như oridonin (đã verify oridonin từ *Rabdosia rubescens*), nhưng PMID user gửi sau đó hoá ra là **berberine hydrochloride × PEDV** (PMID 41086516). Luật: có PMID/link thì đọc nguồn trước, KHÔNG dựng glossary/flow quanh tên đoán; nếu buộc phải đoán thì nói rõ đang đoán và verify bằng nguồn thứ hai (vd PMC review về nguồn gốc thực vật).
- **Retracted papers hide in esearch hits**: an on-topic hit can be retracted years later (observed 2026-09: PMID 28898824, Bioresour Technol 2017, retracted 2025 — visible only in the efetch record as `RETRACTED ARTICLE` / `Retraction in ...`, never in esummary titles). Before writing the deliverable, grep every fetched abstract for `RETRACTED`/`Retraction in` and drop matches.
- **PubMed rate limit** → sleep ≥0.7s between calls; batch all searches in one execute_code run. Despite sleeps, `HTTP 429 Too Many Requests` still occurs — wrap every esearch/esummary/efetch call in a retry loop (backoff 2s, 4s, 6s, … up to ~4 attempts) instead of letting one 429 fail the whole batch. Note: the error surfaces either as `{"error":"API rate limit exceeded"}` in the JSON body or as an HTTP 429 at the urllib layer.
- **PMC ID ≠ PMID (namespace trap)**: `db=pmc` esearch returns PMC IDs, NOT PMIDs. Efetching a PMC ID against `db=pubmed` silently returns an unrelated old record (observed: PMC 13151647 looked like the EFSA Diarr-Stop opinion, but efetch db=pubmed returned a 1954 Brazilian hospital paper). Always resolve the real PMID via esearch db=pubmed with title terms, then efetch that.
- **EFSA FEEDAP opinions = industrial-spec goldmine**: feed-additive safety opinions (e.g. quebracho extract e07699, chestnut-tannin Diarr-Stop S Plus e04472) are indexed in PubMed/PMC, open full text via `pmcoa.cgi/BioC_xml/PMC<id>/unicode`, and carry production-process descriptions + batch-analysis tables (tannin % by ISO 14088 hide powder, moisture, ash, protein). Best verified source for commercial product specs (observed: chestnut extract 75.3% hydrolysable tannins / 17% non-tannins / 7.1% moisture; quebracho ~79% condensed tannins). Find them: esearch db=pmc with `"product name"`, then resolve the PMID via db=pubmed title search.
- **Parallel-session file races (multi-group projects)**: sibling NHÓM sessions write to the SAME `data/` directory and may delete/rename your temp files mid-session (observed: a parallel session removed my `_abstracts/` dir between two execute_code calls → FileNotFoundError on the next read, forcing a full re-fetch). Mitigations: (a) fetch abstracts in-memory and build the deliverable in ONE execute_code call, printing condensed summaries rather than persisting files; (b) if you must persist, use a uniquely-prefixed dir (`_g<N>_abs/`) and re-check `os.path.exists` before reading; (c) only ever delete YOUR OWN temp files; (d) expect pre-existing files from sibling groups (e.g. `group1_virology.json`, `_tmp/`) — never clobber or rename them.
- **Truncated tool output** (execute_code stdout ~50KB cap; terminal output cut) → `curl -s URL -o file` then parse the file; never `json.loads` on raw captured stdout of a large response.
- **Windows/MSYS path trap**: bash `/tmp/...` is NOT visible to the execute_code Python sandbox (FileNotFoundError). Use workspace-relative temp paths (e.g. `D:/.../data/_tmp_esummary.json`) and delete them after.
- **Windows/MSYS drive-prefix trap (`/c/...` → `D:\c\...`).** Verified 18/10/2026: with the session cwd on a NON-C drive (`/d/Hermes Proj/fixgby`), invoking a script by an MSYS-style path — `python "/c/Users/.../content-upload.py"` — got rewritten to `D:\c\Users\...` and died with `can't open file ... [Errno 2] No such file or directory`, even though the file plainly existed. Neither `$HOME/...` nor `/c/...` is safe once cwd sits on another drive. **Fix: pass the quoted native path form** `python 'C:/Users/NTQUANG_DELL/.../content-upload.py' --file 'D:/.../x.html'`. Symptom to recognise: the error message shows the right path with a bogus drive letter glued to the front.
- **Never count/validate PMIDs with `grep` — use `scripts/validate_pmids_batch.py`.** A prefix-based `grep -oE 'PMID[ :=]*[0-9]{7,8}'` silently MISSES PMIDs sitting in markdown table cells (very common: `| ... | 41513748, 42218208 |`), so it reports a plausible-but-wrong total. Documented case: a prefix grep confirmed only **40 of 101** and still reported "all verified". In this session the same grep returned **100** against a subagent's claimed **101** — close enough to look like a rounding artefact and get waved through. The script scans every bare 7–8 digit candidate instead, so a fabricated number cannot hide in a table cell.
  - **Bẫy đếm khi deliverable CHỦ Ý liệt kê PMID đã bị loại.** Quét `\b(\d{7,8})\b` trên cả file sẽ tính **cả** PMID nằm trong bảng "PMID bị loại / không dùng" → con số `N` trong `verified N/N` bị hiểu sai. Ca thật 18/10/2026: **126 token = 120 PMID dùng làm bằng chứng + 6 PMID ở bảng bị loại**. Luật: khi tài liệu có bảng loại-bỏ, khối validate phải **ghi rõ cấu trúc** (`N token, M dùng làm bằng chứng, K ở bảng bị loại`), và **danh sách PMID cuối bài chỉ liệt kê M** — người đọc sau không được thấy PMID bị loại lẫn trong danh sách trích dẫn.
- **JSONDecodeError has TWO distinct root causes — diagnose before fixing (verified 18/10/2026).** (a) **Truncation**: error offset near ~20000 chars and the string ends mid-token — a 10-result `resultType=core` Europe PMC payload is ~20KB+, so captured stdout gets cut. Fix: `curl -s URL -o file` then parse the file. (b) **Control characters**: the JSON looks complete but fails early with `Invalid control character at: line 1 column ...` — raw control chars live inside `abstractText`. Fix: `json.loads(s, strict=False)`. Applying the wrong fix wastes a cycle; check the error offset first.
- **Cache pickle keyed bằng `int` nhưng tra bằng `str` ⇒ miss im lặng (verified 18/10/2026).** Khi cache bản ghi Europe PMC theo `int(pmid)` rồi một hàm sau đó lookup bằng chuỗi `"30004572"`, `cache[p]` ném `KeyError` / in ra rỗng dù batch đã fetch thành công trước đó — dễ bị chẩn đoán oan là "mạng hỏng / batch không trả về". Luật: **chuẩn hoá key ở MỌI chỗ đọc** (`int(str(p).strip())`), và nếu một batch in ra trống dù đã fetch, **nghi key-type trước khi nghi endpoint**.
- **Old papers have no DOI** (pre-2000, some journals) → leave `doi: ""`, keep the PMID.
- **Classic papers may be entirely absent from PubMed** (aquaculture journals like *Aquaculture*, early *DAO*, some pre-2000 reviews — e.g. Lo 1996 WSBV PCR, Chang 1998 WSSV inactivation, Satheeshkumar 2012 all return empty author searches). Empty esearch = possibly not indexed, not "doesn't exist". Cross-check by title/author terms; if still absent, cite the closest indexed review for the fact and state in `verification` that the classic source is not on PubMed. Never attach a guessed PMID.
- **Citation-only records** (e.g. J Fish Dis 2006 inactivation study, PMID 16948707): efetch returns no `<Abstract>` tag. Verify the title, then either pull PMC OA full text or write "citation-only, số liệu không verify được từ PubMed" — do NOT derive numbers from the title.
- **Document-based facts have no PMID** (OIE Aquatic Manual "90+ species host range", QCVN standards): cite the document with `pmid: ""` and say so; never borrow a PMID from a related paper.
- **Search-term drift**: small `retmax` + generic terms return recent-but-irrelevant hits; add species synonyms (pig/OR swine/OR porcine) and refine with `AND accumulation` / `AND (liver OR tissue)`.
- **Distinguish "studied" from "safe"**: evidence exists ≠ safe. For Gd, e.g., strong human data on retention/NSF exists but zero pig-toxicity data — both facts belong in the row.
- **Never invent a numeric ADI.** When the ask is a regulatory/ADI safe level (JECFA/EFSA/FDA/WHO), the honest answer is often "JECFA set **no ADI** ('ADI not specified')" for physiological/self-limiting substances. Do not convert that into a guesstimated mg/kg. See `references/food-additive-regulatory-adi.md` for the full retrieval playbook (WHO IRIS bitstream PDFs, the eCFR versioner API that bypasses the eCFR CAPTCHA, r.jina.ai for Cloudflare-blocked FAO pages, Crossref for resolving EFSA DOIs).
- **Don't guess EFSA DOI article numbers** — resolve via Crossref
  (`api.crossref.org/works?query.bibliographic=...`). Guessed `10.2903/j.efsa.2013.3161`
  was an EPA health-claim opinion, not sodium carbonates. Also: PubMed esearch and
  Europe PMC generally do NOT index EFSA E-series food-additive re-evaluation opinions
  (E500/E501 → 0 hits); search `JOURNAL:"EFSA Journal"` for those that ARE indexed.
- **Verify dấu tiếng Việt + mojibake trên HTML ĐÃ publish, không chỉ local (verify 12/10/2026).**
  HTTP 200 và ảnh render đẹp KHÔNG đủ — file UTF-8 có thể mất dấu ở khâu đọc/ghi/upload.
  ```python
  plain = re.sub(r'<[^>]+>', ' ', r.text); plain = html.unescape(plain)
  has_dia = bool(re.search(r'[ăâđêôơưáàảãạấầẩẫậéèẻẽẹíìỉĩịóòỏõọúùủũụýỳỷỹỵ]', plain, re.I))
  moji   = len(re.findall(r'Ã.|â€|Ä.|ï¿½', plain))
  ```
  `has_dia` phải True, `moji` phải 0. Hard constraint của user. Ngoài ra so sánh đếm
  `<h1>`/`<section>`/`<table>` trên bản đã upload với bản local để bắt upload bị cắt giữa chừng.
- **Tool-call token cap ~8K** (thực tế dính 12/10/2026 với `execute_code`): một `write_file` hay
  `execute_code` chứa cả nghìn dòng sẽ bị stream timeout TRƯỚC khi tới server. Chia nhỏ: ghi
  deliverable lớn thành 3-4 file con rồi gộp, mỗi call một phần. Ghi nhận triệu chứng là
  "Your previous tool call was too large and the stream timed out", không phải lỗi code.
- **Biến thể IM LẶNG: `execute_code` bị cắt giữa chừng mà vẫn `exit 0`** (dính nhiều lần 18/10/2026).
  Thân code bị thay bằng literal `...[truncated]`, script chỉ chạy phần đầu → output thiếu, tưởng như
  logic sai. Đây là bẫy nguy hiểm vì nó không báo lỗi. **Fix đã kiểm chứng: ghi script ra đĩa bằng
  `write_file` rồi chạy `python .tmp_x.py` qua terminal** — script trên đĩa không bị cắt, và cho phép
  truyền tham số (`python .tmp_p.py 36-78`, `python .tmp_show.py 1 8`) nên không phải viết lại code
  mỗi lần đọc một dải dòng khác. Cũng giữ được output ngắn (chỉ in `OK/NOTFOUND` trên stdout, report
  dài ghi ra file) nên không vướng cap hiển thị.
- **`execute_code` bị cắt → output ĐẦY ĐỦ vẫn còn trên đĩa: `~/.hermes/observations/<hash>.json` (verified 19/10/2026).**
  Khi thân code bị chèn `...[truncated]` (bẫy "IM LẶNG" ngay trên), kết quả tool chỉ hiện vài dòng kèm
  `[observation saved to ~/.hermes/observations/<hash>.json — use read_file to recall]`. **ĐỪNG fetch lại
  từ mạng** — đọc chính file đó:
  ```python
  import json, os
  d = json.load(open(os.path.expanduser('~/.hermes/observations/<hash>.json'), encoding='utf-8'))
  c = d.get('content') or json.dumps(d)          # field thật là 'content'
  print(c[offset:offset+8000])                    # đọc theo dải, tránh vượt cap hiển thị
  ```
  Ca thật lô B: **9 lượt `execute_code` liên tiếp** trả về "1 lines output" (fetch 71 PMID + abstract) —
  toàn bộ dữ liệu nằm nguyên trong các file observation; đọc lại là đủ, **không tốn thêm một call mạng nào**.
  Đây là đường hồi phục **rẻ hơn** cách "ghi script ra đĩa rồi chạy lại" ⇒ thử nó TRƯỚC. Ghi nhớ kèm:
  `~/.hermes/observations/` là kho tạm của session, đọc xong nên dọn file rác của mình.
- **BẪY NGUY HIỂM NHẤT: output bị NUỐT ⇒ bạn viết deliverable bằng SỐ NHỚ LẠI (verified 19/10/2026).**
  Trong lô A fixgby `09-tra-cuu-duong-di`, phần lớn call `execute_code` trả về `"(1 lines output)"` +
  con trỏ `[observation saved to ...]`, và `read_file` trên file 40-50 KB trả về
  `"read ... from line 1 (43,560 chars)"` **không kèm nội dung**. Không có thông báo lỗi nào —
  agent vẫn tiếp tục như đã đọc. Bản nháp đầu tiên vì vậy chứa số liệu **nhớ lại**, đúng thứ mà
  luật "chỉ cite cái đã đọc trong session này" cấm.
  **Luật: thấy `(N lines output)` thay vì nội dung = CHƯA ĐỌC. Không được viết số từ trí nhớ.**
  Ba cách chống (đã kiểm chứng cùng session):
  1. **In chỉ câu CÓ CHỮ SỐ**: `[s for s in re.split(r'(?<=[.;])\s+', abstract) if re.search(r'\d', s)]`
     — abstract 2.500 ký tự co lại ~600, nên 3-4 bài/lượt nằm dưới ngưỡng bị nuốt và hiện ra thật.
     Sẵn trong `scripts/verify_claim_tokens.py --sentences <pmid>...`.
  2. **Fetch ghi ra ĐĨA rồi đọc lại theo dải** (JSON trên đĩa = nguồn sự thật, `read_file` chỉ là cửa sổ).
  3. **Chạy `--spec` (token checker) trên MỌI PMID trước khi ship**: khẳng định từng số/tên enzyme
     có mặt trong title+abstract thật, **chỉ in FAIL**. Ca thật: 67 PMID → **13 FAIL**, mà
     12/13 chỉ là artifact dấu câu (`first-pass` vs `First pass`, `GABA(A)` vs `GABAA`,
     `60-70%` vs `60%-70%`) ⇒ **FAIL không tự động nghĩa là nguồn sai, cũng không tự động nghĩa là nguồn
     đúng** — phải đọc abstract của đúng những bài FAIL rồi mới phán. Một ví dụ mà token check PASS
     nhưng claim vẫn phải sửa: bài `14744237` (CYP2E1) **không nói "chuyển ethanol thành acetaldehyde"**
     ⇒ câu đó phải chống đỡ bằng `12489977`, không phải bằng 14744237.
- **Context COMPACTION: bản tóm tắt của phiên trước KHÔNG phải nguồn — nó cùng hạng với "số nhớ lại" (verified 20/10/2026).**
  Sau khi context bị nén, abstract của phiên trước chỉ còn là **văn xuôi tóm tắt** kèm danh sách PMID + con số, kèm câu
  "đã fetch abstract". Đọc lên rất giống "đã đọc trong session này" — nhưng nội dung đã đi qua một lần LLM tóm tắt, nên
  nó **không** thoả luật "chỉ cite cái đã đọc". Ca thật (fixgby `10-cong-thuc-23` lô A cuối — huyết dụ + lá hẹ): bản
  compaction có sẵn ~40 PMID kèm số liệu; trước khi viết đã **fetch lại 35 abstract** (`EXT_ID` theo lô, đọc `title` +
  `abstractText`) rồi mới dựng bảng — mọi số đều khớp, nhưng đó là **kết quả của phép kiểm**, không phải điều được phép
  giả định. **Luật: số liệu đến từ bản tóm tắt compaction chứ không từ tool-result đang hiện trong context ⇒ PHẢI
  re-fetch trước khi ghi.** Hai đường rẻ: (a) gộp nhiều PMID một lệnh — `EXT_ID:a OR EXT_ID:b` (~35 bài trong 5–6 call);
  (b) khi chỉ cần chốt **danh tính** bài (nhất là cho danh sách nguồn bị LOẠI) thì soát title hàng loạt bằng
  `... | grep -E "^(=====|TITLE)"`, rồi mở **full abstract** cho đúng những bài mình sắp trích số.
  Hệ quả: **câu trong `DA_THAT_BAI` cũng phải qua cổng này** — lượt này dòng loại `33066411` viết theo suy đoán
  ("chỉ có trong toàn văn") và phải fetch abstract mới xác nhận được là abstract chỉ có *Ageratum*/*Ixora*.
- **`EXT_ID:<pmid>` KHÔNG tồn tại ⇒ Europe PMC RƠI VỀ tìm kiếm text, trả bài KHÁC HOÀN TOÀN
  (verified 19/10/2026).** Tra `EXT_ID:540449` trả về *"Antenatal care uptake in Nepal"* — một PMID
  bịa/KHÔNG tồn tại **không** làm `resultList` rỗng, nó trả một bài thật nhưng sai chủ đề ⇒
  "fetch thành công" giả. **Guard bắt buộc: record trả về phải có `str(rec['pmid']) == str(pmid_yêu_cầu)`,
  nếu không thì coi là NOTFOUND.** (Đã cài sẵn trong `scripts/verify_claim_tokens.py` và
  `validate_pmids_batch.py`.) Hệ quả liên quan: bài **tồn tại mà KHÔNG có abstract** (ca thật
  `13051861` = đo natri trao đổi bằng ²⁴Na ở người, 1953) ⇒ dùng được **đúng một lần** làm ghi chú
  "đã loại: chỉ có metadata", **tuyệt đối không gánh số**, và phải ghi rõ trong bảng audit.
- **f-string Python 3.11 không chứa backslash trong biểu thức** (dính thật khi build HTML từ
  markdown): `f'<li>{re.sub(r"^\d+\.\s+", "", s)}</li>'` → SyntaxError. Tính biến tạm trước rồi
  mới f-string.
- **`·` (U+00B7 middle dot) là DẤU THẬP PHÂN trong abstract, không phải dấu ngăn cách (verified 19/10/2026).**
  Lancet và nhiều nhà xuất bản in số thập phân bằng `·`: `3·5 mg` = **3.5**. Khi grep số trong
  `abstractText` **phải `replace("·", ".")` TRƯỚC**, nếu không sẽ kết luận oan "nguồn không có con số đó"
  rồi đi tìm nguồn khác vô ích. Và **đừng mang `·` vào `value` của JSON** — người đọc sau hiểu thành
  dấu ngăn cách, số bị đọc sai.
  - **Cùng họ: dấu phân cách NGHÌN cũng làm checker báo oan.** Abstract viết `10,000` / `251,501`;
    bản tiếng Việt viết `10.000` / `251.501` ⇒ so chuỗi thô ra FAIL dù số có thật. Chuẩn hoá **cả hai
    phía** trước khi so (`re.sub(r"[.,]", "", <cụm số>)` trên từng cụm chữ số, rồi mới kiểm substring).
    Ca thật 19/10/2026 (fixgby tầng bệnh): **6/6 cờ là dương tính giả** do dấu nghìn + `·`; vá xong còn **0**.
    Đừng sửa deliverable theo cờ trước khi thử chuẩn hoá — và đừng bỏ nguồn chỉ vì cờ.
  - **Cùng họ, lớp thứ ba: `\xa0` (NBSP) nằm TRONG `abstractText`.** Abstract hay in `100\xa0mg/kg`
    bằng non-breaking space ⇒ kiểm `"100 mg/kg" in abstract` ra **False** dù số có thật. Ca thật
    20/10/2026 (fixgby lô 2): 2/40 phép kiểm báo MISS, cả hai là NBSP (`40453319`: `10\xa0g of
    L-glutamine per kg`; `42816880`: `100\xa0mg/kg COS`) — vá `.replace("\xa0", " ")` rồi
    **40/40**. **Chuẩn hoá chuỗi trước khi so phải gồm ĐỦ bốn thứ: `\xa0`→space, `·`→`.`,
    bỏ dấu nghìn, và casefold.** Thứ tự khuyến nghị:
    `a.replace("\xa0"," ").replace("·",".")` → chuẩn hoá cụm số → so substring. Đây là lần thứ ba
    một "cờ số không có nguồn" hoá ra là artifact định dạng, không phải bịa số.
- **`read_file` báo `is_binary: true` / `total_lines: 0` trên file UTF-8 HỢP LỆ (verified 19/10/2026).**
  Ca thật: `batch-c.md` dài 37.261 ký tự (tiếng Việt có dấu + `·` + `≥`) bị `read_file` trả
  `is_binary: true, total_lines: 0` dù `write_file` đã báo `bytes_written` đúng và `verified: true`.
  File **không** hỏng. **Fix — verify bằng Python, đừng viết lại file vì tưởng nó hỏng:**
  `t = open(p, encoding='utf-8').read(); print(len(t), len(re.findall(r'^#{1,3} ', t, re.M)))`
  (độ dài + số heading). Viết lại theo cảm giác "file hỏng" tốn công và dễ tạo bản kém hơn bản gốc.
- **Deliverable DÀI → ghi bằng `write_file` thẳng, đừng build trong `execute_code` (verified 19/10/2026).**
  Build dict/chuỗi dài trong `execute_code` bị cắt thân code **4 lần liên tiếp** (vẫn trả về "1 lines
  output" như đã chạy đúng — cùng họ với bẫy "IM LẶNG" ở trên). Ghi thẳng `batch-c.json` (25 KB) và
  `batch-c.md` (37 KB) bằng `write_file` thì qua ngay. Phân vai: `write_file` = ghi deliverable,
  `execute_code` = fetch/validate.
- **ĐỌC LÀ ĐỂ VIẾT — ghi deliverable TĂNG DẦN, đừng dồn tới cuối (verified 19/10/2026).** Ca thật lô B
  fixgby `10-cong-thuc-23` (7 nguyên liệu premix heo: phytase/xylanase/protease coated · *Bacillus subtilis*
  bào tử · calcium butyrate · acid citric · betaine HCl): sau **8 vòng truy vấn + đọc abstract ~100 PMID**,
  session **hết ngân sách tool-call TRƯỚC KHI ghi được một byte nào** của `batch-b.md`/`batch-b.json`.
  Không có lỗi kỹ thuật nào cả — chỉ đọc mãi rồi hết lượt; toàn bộ bằng chứng nằm trong `work1.json` nhưng
  deliverable **không tồn tại**. Đây là kiểu thất bại tệ nhất vì mọi thứ *trông* như đang tiến triển tốt.
  **Luật: (1) ngân sách đọc ≤ ~8–10 PMID/chất — bằng chứng thứ 11 cho cùng một luận điểm gần như không
  tăng giá trị; (2) ghi SKELETON ngay từ đầu — file đích chứa đủ 7 object với 20 khoá + `tag_H` rỗng,
  `write_file` một lần trước khi fetch vòng đầu (JSON hợp lệ ở mọi thời điểm, và nếu hết lượt thì cái còn
  lại vẫn đúng khung); (3) sau MỖI 2 chất, `write_file` lại file đích với các khối đã điền.** Bản dở mà CÓ
  luôn hơn bản hoàn hảo không tồn tại; lần chạy sau chỉ append chất còn thiếu. Bổ sung — không thay thế —
  pitfall "gộp 2–3 chất/lượt để tránh cắt thân code": thân `execute_code` phải NGẮN, nhưng file đích phải
  được ghi SỚM và ghi LẶP LẠI.
- **Script QC glob CẢ THƯ MỤC ⇒ report là số TỔNG, không phải số của lô bạn (verified 19/10/2026).**
  `qc-pmid-batch.py <dir>` quét **mọi** `batch-*.json` trong thư mục chứ không chỉ file vừa viết: ca thật
  chạy trên `09-tra-cuu-duong-di` bắt luôn lô A/B (sat, canxi, curcumin, paracetamol, ibuprofen) →
  `_qc-report.json` là số của **10 chất**, không phải 5 chất của lô C. **Luật: con số `verified N/N` ký
  nhận phải chạy RIÊNG trên file của mình** (loop `unique(pmid)` đọc từ chính file đó, fetch `EXT_ID:`
  từng cái, đếm thật) — không trích `_qc-report.json` làm số của lô. Nếu chỉ có số tổng thì nói rõ
  "report là số của cả thư mục" thay vì gán bừa cho lô mình.

- **Validate TỪNG PMID bằng call nhanh liên tiếp ⇒ sinh "PMID MA" (fail giả) — verified 19/10/2026.**
  Lô C fixgby `10-cong-thuc-23`: vòng validate gọi `EXT_ID` **từng cái một** trong 1 script → **11/61 báo
  BAD**, nhìn như PMID bịa. **Cả 11 đều là bài THẬT** — chính những PMID đó đã fetch `core` thành công
  vài lượt trước trong cùng session; retry với `sleep 2` + tối đa 3 lần ⇒ **61/61**.
  **Luật: một lượt fail KHÔNG BAO GIỜ đủ để kết luận PMID không tồn tại.** Phân biệt hai triệu chứng:
  (a) *fail giả* = `resultList` rỗng / payload rỗng khi gọi dồn dập → **retry có sleep**, không phải bịa;
  (b) *PMID không tồn tại thật* = record trả về có `pmid` KHÁC số yêu cầu (Europe PMC rơi về text search —
  pitfall `EXT_ID` phía trên) → cái này mới là hỏng thật. Chỉ khi đã retry mà vẫn (b) mới được ghi NOTFOUND.
- **Số `verified N/N` phải lấy từ |set PMID DUY NHẤT|, không phải tổng của hai lượt (verified 19/10/2026).**
  Ca thật: fetch 61 PMID → lượt 1 `50 pass / 11 fail`; retry 11 cái kia xong; bản nháp vẫn in
  **`verified 61/72`** vì code viết `n_tot = n_ok + len(bad)` — **11 PMID bị đếm HAI LẦN** (một lần ở
  `bad`, một lần ở `ok` sau khi retry). Sự thật là **61/61**. Luật: `N = len(set(mọi PMID trong file))`,
  và `n_ok = len(set(PMID đã fetch thành công))`, **không bao giờ cộng** con số của hai lượt chạy khác nhau.
  `scripts/check_batch_schema.py` in ra sẵn con số |set hợp| để khỏi tự cộng.
- **`execute_code` KHÔNG giữ state giữa các call ⇒ deliverable nhiều chất phải ghi FILE TẠM rồi merge
  (verified 19/10/2026).** Biến `data` build ở call trước **biến mất** ở call sau (không có lỗi nào báo —
  call sau chỉ đơn giản chạy với `data = []`). Cách đã chạy tốt cho 7 chất: chia **2–3 chất/lượt**, mỗi
  lượt `json.dump` ra `_tmp_a.json` / `_tmp_b.json` / `_tmp_c.json` (**thân code ngắn nên không bị cắt**),
  lượt cuối merge + build `.md` + ghi `batch-c.{md,json}`, rồi **xoá file tạm của chính mình**.
  Đây là cách dung hoà với pitfall "deliverable dài → ghi bằng `write_file`": luật thật là **giữ mỗi thân
  `execute_code` ngắn**, không phải tránh `execute_code`.
- **Task chốt "schema CHÍNH XÁC" ⇒ phải ASSERT khoá, không chỉ `json.load` (verified 19/10/2026).**
  Một object thiếu khoá `pmid` trong 1 chặng, hoặc thiếu hẳn 1 trong 20 khoá, vẫn parse sạch và vẫn
  "trông đúng". Chạy `scripts/check_batch_schema.py <batch-*.json>` (đòi đủ 20 khoá, `pmid` trong cả 8
  chặng, `muc_bang_chung ∈ {I,A,R}`, `tag_H` là list; nhận cả MẢNG trần lẫn dict bọc `{"chat":[...]}`)
  — exit 1 = không ship. Lô C sau kiểm: **7/7 chất `missing: none`**, 56 dòng bảng (8×7).

- **Helper module có CACHE JSON DÙNG CHUNG ⇒ gọi từ 2 tool-call SONG SONG là hỏng cache (verified 19/10/2026).**
  `_epmc.py` ghi `_hits.json` sau MỖI lần `search()`. Hai lệnh `terminal` chạy song song cùng gọi helper ⇒ hai
  `json.dump` chồng lên nhau, file thành `{...}{...}`, lần đọc sau chết với
  `Extra data: line 4223 column 2 (char 1055960)` — đọc lên như cache hỏng vĩnh viễn hoặc như API hỏng, nên
  rất dễ chẩn đoán oan sang mạng. **Luật: helper có side-effect ghi cache thì TUYỆT ĐỐI không gọi từ hai
  tool-call song song** — gộp mọi query vào MỘT script chạy tuần tự (đánh đổi vài giây, rẻ hơn nhiều).
  Cứu file: cắt về `}` hợp lệ cuối cùng rồi thử `json.loads`; nếu lùi `rfind('}')` mãi vẫn fail (đúng ca
  file bị append chồng) thì **reset `{}`** — cache chỉ là tiền tốc độ, mất rẻ hơn sửa sai.
- **Spec khoá vs builder `SCALARS` lệch nhau ⇒ builder exit 0 mà field RỖNG (verified 19/10/2026).**
  Task ghi khoá `S_THAI_TY_LY`, còn `_build.py` đọc `S_THAI_TY_LE` (sinh từ `"thai.ty_le"`); 2/3 file dùng
  đúng tên trong spec nên builder **im lặng** rơi vào `head.get(..., "")` → `thai.ty_le: ""` trong JSON,
  exit 0, `ingredients=N` in ra bình thường. **Không có lỗi nào để thấy.** Luật 3 bước: (1) **diff danh sách
  khoá trong spec với list `SCALARS` + hàm `parse()` của builder TRƯỚC khi viết** — đây là hai nguồn sự thật
  khác nhau và không ai bắt chúng khớp; (2) khi lệch, **phát cả hai khoá** (alias, giá trị y hệt) để cả
  spec-checker lẫn builder đều đọc được; (3) sau build, **assert mọi field scalar trong output JSON đều
  non-empty** rồi mới ký nhận — `exit 0` chỉ chứng minh *parse được*, không chứng minh *đã điền*. Cùng họ
  với luật "task chốt schema CHÍNH XÁC ⇒ phải ASSERT khoá, không chỉ `json.load`".
- **Tìm bài ĐO PK: `sort=CITED desc` trả về review tổng, không trả bài đo (verified 19/10/2026).**
  Với câu hỏi "chất này hấp thu / thải thế nào", sort theo trích dẫn đẩy lên đầu các review lớn có abstract
  **không chứa một con số nào**, còn bài đo thật nằm sâu. **Dùng `sort=''` (relevance) cho truy vấn dược
  động; giữ `CITED desc` cho truy vấn "tổng quan chủ đề".** Relevance vẫn nhiễu ⇒ **search n=20–25 rồi LỌC
  ABSTRACT TẠI CHỖ** thay vì mở từng bài: giữ bài mà `abstractText` vừa khớp từ khoá (`half-life`,
  `bioavailability`, `excret`, `urine`, `feces`, `bile`, `accumul`) vừa chứa `\d`, rồi in **câu** khớp
  (`re.split(r'(?<=[.;])\s+', a)`) chứ không in cả abstract. Ca thật: 4 truy vấn × 25 bài lôi ra được
  `0,26 %` / `0,37 ± 0,11 %` / `0,68 %` (sinh khả dụng berberine) và `t½ 2,48 h` / `F 0,14 %` (leonurine) —
  đúng những con số mà 8 truy vấn sort-theo-trích-dẫn trước đó không hề thấy.
  - **Ngược lại với CƠ CHẾ/BỆNH HỌC: `CITED desc` đúng, nhưng CHỈ khi query đã hẹp.** Verified 19/10/2026
    (fixgby `docs/11`): query 2 từ chung + `CITED desc` kéo lên toàn mega-review (*"Coronaviruses: an
    overview"*, *"The molecular biology of coronaviruses"*) **không chứa claim cụ thể nào**. Chuỗi hiệu quả:
    `TITLE_ABS:"<mầm>" AND (TITLE_ABS:pathogenesis OR TITLE_ABS:pathology OR TITLE_ABS:villus)` rồi
    `CITED desc` (ra bài gốc 1980s–2010s), hoặc `TITLE:"<tên bệnh>"` khi cần bài kinh điển (ra
    `1350661` Nature 1992 cho thụ thể APN của TGEV). Cũng thấy: query rộng không sort trả về **gần như
    toàn bài 2025–2026** ⇒ triệu chứng "kết quả toàn năm nay" là dấu query chưa đủ hẹp, không phải
    "lĩnh vực không có bài cũ".
- **Câu "nguồn bị loại" trong `DA_THAT_BAI` CŨNG là một claim — phải đọc abstract mới được viết.**
  Viết "abstract không nêu thành phần X" sau khi chỉ đọc TITLE là bịa cùng loại với bịa PMID, chỉ khác là
  nó nằm trong phần audit nên trông đáng tin hơn. Ca thật: 2/9 nguồn bị loại chỉ dựa vào title
  (`38136904` "fermented Chinese herbs", `40527062` motherwort) — phải fetch abstract của đúng 2 bài đó
  trước khi giữ câu loại; hoá ra cả hai câu đúng, nhưng nếu sai thì cái sai đã nằm ngay trong khối audit.
  **Luật: mỗi dòng loại-bỏ ghi rõ (a) đọc được gì từ abstract, hoặc (b) "chỉ đọc title"; loại theo title
  chỉ được dùng khi TITLE TỰ nó đủ — tức title nêu sai LOÀI/MÔ/CHẤT ("in chickens", "rumen", "Cortex
  Phellodendri", "Oregon grape"), không phải khi phải suy ra từ thành phần không được liệt kê.**

Ngân hàng lô A premix heo (berberine · hoàng liên · ích mẫu, **42 PMID verified 42/42**, 19/10/2026) +
3 kỹ thuật mới ở trên: `references/feed-additive-8stage-berberine-coptis-leonurus-notes.md`.

## Nhận deliverable từ subagent / session khác → verify TRƯỚC khi tin

Summary của một subagent (hoặc báo cáo dán vào từ chỗ khác) là **self-report**, không phải fact. Ca thật 18/10/2026: subagent khai "deliverable complete and verified, 102 PMID, đã đọc abstract 100%" — file và PMID đều thật, nhưng có **1 kết luận pháp lý lỗi thời đã bị gắn tag [F]**, suýt được relay cho founder.

Chạy tối thiểu 4 bước:
1. **`python scripts/verify_pmids.py <file.md>`** — mọi PMID phải tồn tại trên Europe PMC **và title khớp claim** mà nó chống đỡ. Exit 1 = chặn.
   > **Cảnh báo đã kiểm chứng:** script chỉ tự động hoá **cổng tồn tại**. Cổng "title khớp claim" **script KHÔNG tự làm** — nó in title ra và *chờ bạn đọc*. Đúng phần "chờ bạn đọc" đó là chỗ lỗi lọt. Ca 18/10/2026 (07b fixgby): 153/153 PMID tồn tại thật, `verify_pmids.py` pass sạch, nhưng dump `PMID | title thật | dòng claim` bắt **~12 citation gắn sai claim**. Với tài liệu >50 PMID, **bắt buộc chạy một lượt dump-and-eyeball riêng** (recipe: `references/citation-attribution-audit.md`), không được coi "script exit 0" là đã xong cổng 2.
   > **Và "verified N/N" của subagent KHÔNG phải bằng chứng đã audit.** Ca thật cùng ngày, cùng tài liệu: subagent tự khai *"153/153 PMID verified"* và *"deliverable complete"*, nhưng khi QC lại thì file còn **placeholder chưa điền**, **`.tmp_edits.json` chưa áp**, và 3 PMID gắn **sai MÔ** (không sai chủ đề — lớp lỗi khó hơn, xem §1b reference). Con số subagent đưa là con số **cổng tồn tại**; nó không nói gì về mô, về chiều kết luận, hay về việc file đã ở trạng thái ship được chưa.
2. **Kiểm kích thước file thật** (`os.path.getsize` / `os.walk`) so với con số trong summary. Lưu ý bytes ≠ chars với tiếng Việt. **Với deliverable có YÊU CẦU ĐỘ DÀI TỐI THIỂU (vd "≥ 25.000 ký tự"): đo `len(open(f,encoding='utf-8').read())` — đếm KÝ TỰ, không đếm byte, và đo LẠI SAU LẦN SỬA CUỐI CÙNG.** Sửa-bằng-patch làm đổi độ dài, nên một con số đo giữa chừng không phải bằng chứng đã đạt ngưỡng. Ca thật 18/10/2026: file `08-hanh-vi-giu-ma-giam.md` đo được 764 dòng / rất dài nhưng **lần đo độ dài cuối cùng diễn ra TRƯỚC các patch cuối** ⇒ không dám ký nhận ngưỡng 25.000 ký tự. Đo lại ở cuối là việc 5 giây; không đo được thì **nói thẳng là chưa đo**, đừng để người nhận tưởng đã kiểm.
3. **Đọc lại phần summary bị cắt** (`[... middle omitted ...]` kèm đường dẫn file cache) — thường chứa đúng danh sách điểm yếu/khoảng trống.
4. **Săn claim quyết định nhất** và tự tra nguồn gốc. Với claim pháp lý/quy định: tra **văn bản hợp nhất** (văn bản ban hành sau có dừng điều khoản đó không) — xem `vietnam-legal-advisory`.
5. **Cổng OFFLINE trước cổng mạng — mọi citation phải thuộc ĐÚNG nguồn được giao.** `verify_pmids.py` chỉ chứng minh PMID tồn tại thật, nó KHÔNG bắt được citation thật nhưng lấy từ nguồn khác. Khi deliverable là bản **tích hợp** (phụ lục/append) từ một research file cụ thể, chạy `scripts/check_citations_against_source.py <draft> <source...>` — set-diff PMID/DOI thuần, không cần mạng, exit 1 nếu có citation không nằm trong nguồn. Ca thật 18/10/2026 (fixgby: phụ lục A của `05-plan-*` ← research `06a-*`): 43/43 PMID + 3/3 DOI khớp nguồn ⇒ đây là bằng chứng "không bịa" rẻ nhất để đưa vào báo cáo cuối.
6. **Quy trình tích hợp append-only vào tài liệu dự án** (chỉ thêm, không viết lại cấu trúc plan; quy ước ghi `chưa có nguồn (tag H)` cho khẳng định thiếu nguồn; nhật ký + commit kèm diff stat/commit hash; mẹo line-ending CRLF trên Windows): xem `references/evidence-doc-integration-append-only.md`, kèm bank bằng chứng fixgby 06A (8 luật R1–R8, đề xuất trọng số CS).

Checklist đầy đủ + cách báo cáo phần verify: `ai-team-orchestration/references/delegation-output-verification.md`.

## Support files
- `references/human-supplement-actives-evidence.md` — verified human-RCT evidence bank for TPBVSK/supplement actives (beta-sitosterol/ashwagandha/L-theanine/bacopa/carrageenan/ivy-leaf = SOLID; shilajit/saw palmetto/silymarin/GABA = weak-drop) + the "verify human RCT, don't recall known botanicals" correction case. Dùng khi research hoạt chất cho SP dinh dưỡng/bổ sung người.
- `references/markdown-to-preview.md` — publish bài nghiên cứu → link preview.thefirstonly.com: convert markdown→HTML (lib `markdown`), `--name index.html` (worker chỉ serve index.html; .md/.txt→404), verify HTTP 200.
- `templates/evidence_row_template.json` — copy-ready row schema for evidence JSON deliverables.
- `references/rare-earth-pigs-group2-notes.md` — verified findings + working query patterns from the rare-earth-pigs Group 2 (heavy REE + CeO2 NP) session; reuse for Groups 3+.
- `references/rare-earth-feed-additive-pigs-notes.md` — **ca mẫu đầy đủ cho dạng câu hỏi "chất X (truyền thống TQ) có THẬT SỰ hiệu quả trên heo không"**: bank **21 PMID verified 21/21** (20/10/2026, fixgby `14-cong-thuc-co-ban` lô A) gồm **6 nghiên cứu in vivo trên HEO** (n, liều, dạng, kết quả định lượng, PMID), 4 luật thẩm định B1–B4 ở rule 8 kèm số cụ thể, bảng quy đổi **liều sản phẩm → mg hoạt chất** (200 mg/kg sản phẩm chỉ = ~18 mg REE), bảng NOAEL (La 24 · Ce 75 · **La thần kinh 0,037** mg/kg/ngày), bảng tồn dư gan 10×, **pháp lý 4 nước đã verify kèm ĐƯỜNG TRA** (EU 2020/1370 duyệt lanthanide citrate cho heo con <120 ngày ≤250 mg/kg — đừng giả định "EU cấm"; VN Phụ lục VI có tên nhưng không có liều), shape JSON brief-7-câu với `da_verify` từng dòng + `bang_chung_phan_bac` + `dieu_gi_se_doi_y`. Khác file group2 ở trên: file kia là HREE/CeO₂ cho xử lý nước thải, file này là citrate/carbonate cho hiệu quả + an toàn + luật.
- `references/pig-waste-group3-chemical.md` — verified PMID/DOI bank + QCVN 62 (2016 & 2025) tables + retrieval paths for pig-wastewater treatment Group 3; note the deliverable `group3_chemical.json` was NOT yet written when this was captured.
- `references/wssv-group3-survival-notes.md` — verified 29-PMID bank grouped by subtopic + query patterns + honest-gap notes for WSSV (white spot syndrome virus) survival/transmission/epidemiology; deliverable `group3_survival.json` written 2026-08-16.
- `references/food-additive-regulatory-adi.md` — ADI/regulatory-status retrieval playbook + verified fact bank for food-additive safety briefs: WHO IRIS bitstream PDF download, FDA eCFR versioner API (bypasses eCFR CAPTCHA), FAO JECFA "ADI not specified", EFSA authorised-additives fallback, r.jina.ai Cloudflare bypass, and the verified Na/K limits + GRAS CFR sections for carbonates/bicarbonates.
- `references/wssv-group2-infection-notes.md` — verified 32-PMID bank for WSSV infection/replication/immunity (entry routes, clathrin endocytosis, VP28, nuclear replication, shrimp innate immunity + RNAi, pathology, stress) + working query patterns + classic-paper↔PMID mapping corrections; deliverable `group2_infection.json` written 2026-08-16.
- `references/tannin-extraction-group2-notes.md` — verified 46-PMID / 7-patent bank for tannin extraction (classification HT vs CT, sources, chemistry, extraction methods, industrial powder production, purification/stabilization, feed/water/leather/wine applications) + EFSA industrial specs (chestnut 75.3% HT, quebracho ~79% CT, safe feed levels) + honest gaps; deliverable `group2_tannin.json` written 2026-08-17.
- `references/swine-h2s-manure-notes.md` — verified PMID bank + khung cơ chế H2S trong phân lợn (2 con đường: khử sulfate bởi Desulfovibrio / lysine sulfate nguồn chính + cắt amino-acid sulfur tạo CH₃SH; hướng giải triệt để 3 tầng: cắt substrate → ức chế SRB bằng inulin/thảo dược polyphenol → kết tủa FeS). Cảnh báo: "giảm odor" trong paper manure thường chỉ NH3/VFA, không đụng H2S; đơn vị ppm (khí) vs mg/L (slurry) không trộn được.\n- `references/vietnamese-web-research-wikipedia.md` — research chủ đề KHÔNG nằm trong PubMed (lịch sử, văn hóa, tín ngưỡng, nhân vật, sự kiện) qua Wikipedia MediaWiki API: triage bằng `list=search` → lấy nội dung bằng `pageids=` (TRÁNH encoded title có dấu trong URL — trap Unicode khiến curl ghi file 0 byte), `redirects=1`, cắt by-section. Publish rule bắt buộc vẫn áp dụng.\n- `references/asf-prrs-coinfection-notes.md` — verified 5-PMID bank cho đồng nhiễm Dịch tả lợn châu Phi (ASF) + Tai xanh (PRRS): cơ chế (cùng đánh đại thực bào phế nang; HP-PRRS ức chế IFN-I mở cửa ASF; ASF chuyển tropism phổi khi đồng nhiễm), đánh giá sống sót, query terms + honest gaps. Dùng khi research bệnh lợn ASF/PRRS tái phát.
- `references/saponin-berberine-swine-wastewater.md` — verified 18-PMID bank (2026-09-09) saponin + berberine thả TRỰC TIẾP vào nước thải heo: kết luận âm tính có kiểm chứng (count=1/5/0), Yucca qua thức ăn (34368272, 19897627, null 16825449/11811465), tea saponin EK bùn đô thị 36113240 + nano kháng khuẩn 34382988, cảnh báo berberine ức chế metan 37926228 + biofilm E. coli 40746958, bẫy Quillaja/tea-saponin, sai lầm feed-dose→pit-dose.
- `references/mineral-carriers-pig-wastewater-notes.md` — verified 29-PMID bank (2026-09-08) zeolite/clinoptilolite, bentonite, kaolin, talc thả TRỰC TIẾP vào nước thải heo: zeolite khử NH4+/tăng CH4/hỗ trợ nitrat hóa/cố định Cu-Zn/giảm ARG (Mạnh), bentonite 2 mặt + trial âm tính bắt buộc Jiang 2014, kaolin/talc = khoảng trống bằng chứng (honest gaps), guardrails liều-thang-g/L + cạnh tranh K+, bẫy retraction PMID 28898824.
- `references/ez80-mineral-direct-notes.md` — verified 15-PMID bank (2026-09-09) khoáng thả TRỰC TIẾP: công thức liều mg/L = mg/kg×g/L/1000, stoichiometry struvite Mg:P 1:1 / HAP Ca:P 1,67, bài toán thiếu hụt 97% ở 0,15 g/L, CaCO3 sống vs CaO nung (37532535), FeS -87% H2S (26260964), cạnh tranh Ca/Fe giết struvite (41880949), TSS ảo sau thả.
- `references/formulation-interaction-framework.md` — verified framework (09/2026) for evaluating multi-compound feed additive compatibility: 6-check system (chemical reaction, Maillard, complexation, CYP competition, CYP inhibition, absorption competition) + CYP450 pathway map for 10+ compounds (thymol→CYP2A6, eucalyptol→CYP3A4, berberine→CYP1B1, etc.) + PMID-verified interaction data for berberine-tannin supramolecular complex (delayed release, beneficial) and carvacrol-glycyrrhizin hydrogel formation. Dùng khi research tương tác giữa các hoạt chất trong 1 công thức.
- `scripts/check_deliverable_pmids.py` — run before finishing any deliverable: extracts every `pmid` from the output JSON and flags any PMID not in your efetched-this-session list (catches title-only citations).
- `scripts/verify_pmids.py` — run on any deliverable you RECEIVED (subagent/sibling session/pasted report) or before shipping your own: scans `.md`/`.json`/`.txt` for PMIDs and DOIs, queries Europe PMC one at a time, prints the **real title** so you can eyeball it against the claim, exits 1 if any PMID is missing or title-less. Separates DOI-only (preprint) citations so you remember to flag them not-peer-reviewed.
- `references/oa-fulltext-translation.md` — workflow dịch bài báo open-access sang tiếng Việt + publish: chỉ dịch bài **CC BY** (bản dịch là tác phẩm phái sinh), lấy toàn văn qua `pmcoa.cgi` (KHÔNG qua PMC website vì reCAPTCHA), parse XML phẳng `<passage>` (BioC không có `<section>` lồng nhau), lọc `section_type != "REF"`, chia 3 phần để tránh tool-call token cap, kiểm tra rò rỉ token Anh/ký tự Trung, validate tag balance, và verify dấu tiếng Việt + mojibake sau publish.
- `references/europepmc-rest-verification.md` — Europe PMC REST search+verify recipe: `resultType=lite` (triage) vs `core` (abstract in the same response), `EXT_ID:<pmid>` exact lookup, `TITLE_ABS:`/`TITLE:` field scoping, `&sort=CITED%20desc`, the two JSONDecodeError root causes with the write-to-file + `strict=False` helper, and the preprint / `NO ABSTRACT` record-integrity rules. Dùng khi cần verify 50-100 PMID bằng abstract thật.
- `references/pig-model-depression-neuroscience-notes.md` — verified 100-PMID bank (18/10/2026) cho câu hỏi "heo làm mô hình dịch chuyển cho cơ chế thần kinh/tâm thần người đến đâu, trọng tâm TRẦM CẢM": gyrification, homologue BA25/NAcc/PFC/cingulate, 11 mô hình trầm cảm-like trên heo (kèm 1 kết quả ÂM TÍNH social defeat), HPA/DST, monoamine/BDNF, neuroinflammation, gut-brain, DBS/TMS/tDCS/VNS, EEG/ERP; danh sách `KHÔNG CÓ NGUỒN` đã xác nhận + 5 khoảng trống nghiên cứu. Kèm bẫy "guinea pig ≠ heo". Dùng cho 03b/03c của dự án **fixgby** (tên cũ: hostcore).
- `references/invivo-biosensor-resolution-layers.md` — verified 101-PMID bank (18/10/2026) cho câu hỏi "device trong cơ thể đọc tín hiệu tế bào bằng cách nào, và làm sao biết VẤN ĐỀ NẰM Ở ĐÂU": thang 8 tầng độ phân giải (wearable → ISF/microneedle → CGM → implant cơ quan → fiber photometry/FRET → nội bào → neuron điện → cfDNA), trục chấm riêng **(I)/(A)/(R)** (đã-trên-người / động vật lớn / in-vitro), và 5 kết luận định lượng tái dùng được: CGM = tầng **phân tử liên tục cao nhất trên người** và cách tế bào **5–7 bậc**; wearable **13,6 bậc**; cfDNA chạm **29 mô ≈ 12,1 bậc và KHÔNG rút thêm được**; tầng nội bào **không có bậc nào** vì PMID 19426527 chứng minh mạng JAK-STAT/MAPK/NF-κB **"NOT IDENTIFIABLE even under the strong assumption that ALL system state variables are measurable"** — tức khoảng cách **toán học**, không phải kỹ thuật. Dùng khi phản biện giả định "đã đọc được tín hiệu tế bào / định vị từng tế bào", khi cần chọn tầng cảm biến khả thi cho dự án 1–2 người, hoặc khi user hỏi về giới hạn cảm biến in-vivo. Doc dự án: `07a-research-cam-bien-invivo-theo-do-phan-giai.md`.
- `references/capability-claim-rebuttal.md` — **cách phản biện một KHẢ NĂNG bằng cấu trúc, không bằng ý kiến** (user khẳng định "device đọc được tín hiệu tế bào", "học được cơ chế của từng người" — không phải hỏi một sự kiện): 4 bước — (1) ghi lại TRUY VẤN ÂM TÍNH làm bằng chứng, số truy vấn âm tính CHÍNH LÀ kết quả; (2) định lượng khoảng cách bằng BẬC ĐỘ LỚN kèm tiêu chí đo nêu trước, cấm tính từ; (3) **phân biệt khoảng cách KỸ THUẬT vs TOÁN HỌC** (kỹ thuật đóng được bằng tiền, toán học thì không — tìm chứng minh non-identifiability); (4) chấm trục **(I)/(A)/(R)** cho nghiên cứu thiết bị. Kèm mẹo tách trục (điện đạt 0 bậc ≠ phân tử đạt 0 bậc) và kiểm sự kiện bằng peer review. Dùng khi user đặt câu hỏi kiểu tầm nhìn/cách mạng cần trả lời "được hay không được, và vì sao".
- `scripts/validate_pmids_batch.py` — chạy trên deliverable TRƯỚC khi ship: quét **mọi** số 7–8 chữ số (không cần tiền tố `PMID:`) rồi validate theo lô 40 qua Europe PMC, nên không số bịa nào trốn được trong ô bảng markdown. Khác `verify_pmids.py` ở 2 điểm: nhanh hơn nhiều (~3 call cho 100 PMID thay vì 100) và bắt được PMID **không có tiền tố**. Đây là công cụ thay thế cho việc đếm PMID bằng `grep` (xem pitfall ở trên). Exit 1 = không ship.
- `references/citation-attribution-audit.md` — **audit CỔNG 2 (title khớp claim) — cả HAI lớp lỗi** + bulk-edit tài liệu lớn: bảng 12 ca PMID-tồn-tại-nhưng-gắn-sai-claim (kèm title thật để tra nhanh); **§1b lớp lỗi SAI MÔ** (3 ca thật: 29410610 = phù não/ngộ độc DCE chứ không phải gan-thận; 37245680 = tế bào ốc tai chứ không phải ruột; 25063198 = điếc/tai trong chứ không phải hàng rào ruột) + luật `số nguồn ≠ điểm bằng chứng` (cạnh 3 nguồn nhưng 1/3 đúng mô → hạ bậc) + ca **ĐẢO CHIỀU kết luận** (occludin-KO vẫn tạo được TJ ⇒ giết hướng "KÍCH occludin"); recipe dump `PMID | title thật | dòng thật trong file` theo lô 8–9 (report 14 KB → ghi file + in từng nửa) và **bản nhanh batch-25 `EXT_ID` + in title nhóm trụ cột (~12s/165 PMID)**; bẫy heuristic token-overlap flag oan 127/155; **applier thay-cả-dòng theo marker** (JSON `{m, n}` + tìm dòng duy nhất) vì replace chuỗi chính xác thất bại trên file có CRLF + U+2011 + backtick — kèm **luật mode ĐỌC và mode GHI phải khớp nhau** (đọc bytes mà ghi `newline="\r\n"` → `\r\r\n`) và cách xử lý `NOTFOUND` (khác thứ tự ≠ sai nội dung); **§5 quét MÂU THUẪN NỘI BỘ sau bulk-edit** (checklist 5 bước: bảng tóm tắt cuối vs thân bài, con số đếm, động từ khẳng định quá mạnh, `tag H` bị mất); **§6 nguyên mẫu khối "GIỚI HẠN CỦA CHÍNH PHÉP VALIDATE NÀY"** tự công bố trong deliverable; **§7 tự kiểm commit** bằng `git log`/`git status` thay vì suy đoán; và bẫy `read_file` trên file lớn trả **bản đã tóm tắt, không verbatim** (đừng dựng chuỗi exact-match từ một lần đọc lớn).
- `references/harm-reduction-keep-behavior-evidence.md` — verified bank (18/10/2026) cho lớp câu hỏi **"giữ hành vi — giảm tác động, và cái gì là BẤT KHẢ"**: nicotine (Tmax/t½ theo TỪNG đường vào + chênh động–tĩnh mạch + ảnh hưởng VÙNG DÁN tới AUC; nAChR theo từng mô kèm PMID; lập luận "phê rồi thải không chạm cơ thể" là bất khả; cytisine/varenicline + EAGLES; vaccine NicVAX âm tính; lỗi hộp đen FDA tốn 7 năm), rượu (tranh cãi first-pass dạ dày, PK dân số AUC 3,83 vs 2,34 g·h/L, acetaldehyde→adduct DNA thực quản người, L-cysteine chặn cục bộ, NNT/NNH = 12), đường/SSB (fructose vs glucose, ATP gan 31P-MRS, **acarbose HR 0,98 p=0,73 = bài học "chỉ dấu trung gian ≠ kết cục"**, chất ngọt nhân tạo âm tính), dầu chiên (TFA tổng 1,22 nhưng nhánh công nghiệp KHÔNG ý nghĩa; adduct acrylamide Hb 80 vs 29 pmol/g; vitamin E 84 RCT null; β-carotene tăng ung thư phổi; orlistat báo cáo tác dụng phụ thiên lệch), ngủ/nhịp sinh học (PRC người, ngủ bù khôi phục một phần — cortisol/LH không đổi, kính chặn ánh sáng xanh **thất bại**, đổi giờ ăn ca đêm chỉ giảm một phần) + 3 hành vi VN (natri **hình chữ J**, ngồi lâu "chưa kết luận độc lập", nước đá = tag H). Kèm §7 bẫy đặc thù: 6 PMID nhớ-ra-sai, 4 dòng-khung gắn sai PMID, bẫy đếm N/N khi có bảng loại-bỏ.
- `references/molecule-pathway-8-stage-notes.md` — **shape thứ ba: khung 8 chặng "đường đi phân tử"** (fixgby `09-tra-cuu-duong-di`): 8 khoá đúng thứ tự (`cua_vao`→`o_lai`) + bảng 4 cửa vào / 5 cửa thải / họ protein theo từng chặng (SLC·OATP cho chặng 2, CYP chặng 3, UGT/SULT chặng 4, ABC/MATE chặng 6), luật **thụ thể ≠ enzyme**, schema JSON đầy đủ (`batch-*.json` = MẢNG object), 3 khoá đời (`bat_kha`/`da_that_bai`/`chi_dau_do_duoc`), **bank LÔ C 46 PMID verified 46/46** (atorvastatin · metformin · vitamin C · omega-3 EPA/DHA · melatonin) **+ bank LÔ B 71 PMID verified 71/71** (sắt heme/non-heme · canxi · curcumin · paracetamol · ibuprofen, kèm 2 điểm bắt buộc của curcumin: sinh khả dụng "virtually zero" `22930441` + bất ổn kiềm pH 7,2 ~90 %/30 phút `9278892`, và ca sai CHẤT ANH EM `30562214`) kèm **bảng nguồn dễ gán sai MÔ** (24828044 hàng rào MÁU-NÃO ≠ ruột; 39382087 tế bào u NÃO nuôi cấy; 16150108 tế bào UNG THƯ VÚ chỉ dùng tên enzyme SULT1A1; 40858268 CYP4F nói về acid arachidonic KHÔNG nêu EPA/DHA; 10631088 ghi nhầm ký hiệu gene), con số chặng 8 đáng nhớ, và 4 mẫu **bằng chứng ÂM TÍNH** dùng cho `da_that_bai`. **Chặng 6 (bơm đẩy): ĐÃ SỬA KẾT LUẬN sau lô B** — KHÔNG còn là chặng trống nhất. Bơm đẩy CÓ nguồn thật ở curcumin (MRP2 · BCRP/ABCG2 · MRP4/ABCC4), paracetamol (MRP4/ABCC4 · MRP3/ABCC3 · P-gp) và sắt (ferroportin SLC40A1); trống ở chất VÔ CƠ/ion (canxi) và NSAID (ibuprofen). Luật rút ra: **bơm đẩy bám theo con đường LIÊN HỢP (chặng 4), không bám theo "họ thuốc"** ⇒ tra chặng 4 trước khi kết luận chặng 6 trống, và đừng suy từ chất này sang chất khác.
- `references/feed-additive-8stage-absorption-notes.md` — **ngân hàng lô premix heo 7 chất, 61 PMID verified 61/61 (19/10/2026, fixgby `10-cong-thuc-23` batch-c)**: (A) kỹ thuật tăng hấp thu — curcumin nano (≥9× · AUC ×23,2 · Cmax ×53) và **TPGS ỨC CHẾ P-gp** (demethoxycurcumin ATPase IC50 1,56 ± 0,13 µM) kèm luật "chất tăng hấp thu tác động qua bơm ABC ⇒ chặng 2 và 6 ăn vào nhau"; con số chặng 8 vitamin E (mô mỡ 1,53 µmol/g; t½ 184 ± 48 ngày; meta-analysis nái **không** tăng vitamin E trong sữa đầu); (B) **Se hữu cơ vs vô cơ** — tồn lưu mô (heo Tây Tạng, 42793988), **thải qua SỮA nái** (20717850), trứng gà (42651912, không phải heo), ngưỡng NRC/EU + sự cố Na-uy 516 nái/895 lứa nhiễm 2,47–4,70 mg/kg từ **Na-selenite**; (C) **MgO vs Mg chelate = bằng chứng ÂM TÍNH** (chuột tương đương 42589240; Caco-2 khác biệt mất khi không có thức ăn 41599937; công thức quyết định hơn loại muối 42709016; 381 heo Mg máu giảm ở MỌI nhóm, tệ nhất nhóm MgO 42277947) + câu phủ định tường minh cho chặng 3/6 của ion; (D) tryptophan (thải nước tiểu định lượng trên **HEO CON sơ sinh** 40610456; cạnh tranh hệ L 42220619; **bẫy BBB ≠ ruột** với SLC7A5) và sodium ascorbyl phosphate (EFSA 3a311; SVCT1/SLC23A1; **bẫy PMID 38683367 = LINH TRƯỞNG/CHUỘT LANG, không phải heo**; tương tác trên nái 31376718); (E) quy trình 5 bước tái dùng.
- `references/feed-additive-8stage-enzyme-probiotic-notes.md` — **lô B cùng thư mục `10-cong-thuc-23` (7 nguyên liệu nhóm enzyme · vi sinh · acid hữu cơ: phytase/xylanase/protease **coated** · *Bacillus subtilis* bào tử · calcium butyrate · acid citric · betaine HCl 98 %)**: (a) **phán quyết về cảnh báo điểm sống còn "enzyme mất 50–80 % hoạt tính ở pH 8–9" = CHƯA CÓ NGUỒN (tag H)** kèm 3 lý do có nguồn — `42462087` đo pH dịch tiêu hoá HEO là 4,0 / 6,0 / 5,9 / 5,5 (pH 8–9 **không tồn tại** nơi enzyme tác động), `30088242` giữ **>50 % hoạt tính sau 12 h ở pH 8,0**, `11195907` cho pH optimum 4,5–5,5 (nấm) / 7,0 (Bacillus) — **và bảng stress THẬT thay thế được** (ép viên 84 °C còn 53 %; conditioner 70 °C ~70 % vs ~30 %; T½ 1 h ở 70 °C; dịch vị; tồn trữ VTM 23 °C chỉ còn 60 % sau 180 ngày); (b) bank số liệu đã đọc abstract theo từng chất (phytase meta-analysis +25,6 điểm % P / bình nguyên 64,9 %; xylanase **hỗn hợp** — có thí nghiệm KHÔNG hiệu quả ở 32.000 BXU/kg; *B. subtilis* 87Y trên heo: N phân −32 %, P thải −39 %, Ca tồn lưu +187 %, AID P 47→70 %; butyrate MCT1 ruột già gấp 20 lần ruột non + **butyrate CẢM ỨNG P-gp, KHÔNG ức chế**; betaine t½ 14,38 h → **41,17 h khi lặp liều = có tích luỹ**, thải niệu 4 %; BHMT **vắng hoàn toàn ở NÃO** người/heo/chuột); (c) **bảng bẫy mô/loài** (11223388 = GÀ THỊT, 23246691 = GIÁC MẠC người, 32733389 = *B. clausii*, 30694101 = *B. coagulans*, 38547603 = CÁ BƠN, 11424701 = dạ cỏ BÒ, 38073487 = CHUỘT, 24795654 = THẬN); (d) tương tác nội công thức (betaine HCl + citric acid = tải acid; citric × phytase **không** synergy trên heo; tanin × enzyme; berberine 20 µg/mL **kích thích** *B. subtilis* nhưng >100 µg/mL mới ức chế); (e) **bản đồ 8 chặng cho chất KHÔNG hấp thu** (enzyme: chặng 3/4/6 = KHÔNG, đích = cơ chất trong thức ăn, thải = PHÂN; bào tử nảy mầm ở ruột non). **Lưu ý trạng thái: `batch-b.md`/`batch-b.json` CHƯA được ghi** — lần chạy sau bắt đầu bằng skeleton rồi điền 2 chất/lượt.
- `references/feed-additive-8stage-berberine-coptis-leonurus-notes.md` — **lô A cùng thư mục `10-cong-thuc-23` (3 nguyên liệu: berberine · hoàng liên *Coptis chinensis/teeta* · ích mẫu *Leonurus japonicus*), 42 PMID verified 42/42 (19/10/2026)**: bank số theo từng chặng (F uống 0,26/0,37/0,68 %; OCT1 KM 7,0 µM; CYP2D6→1A2>3A4; thu hồi 41,2 % + 18,6 % phân dạng berberrubine; t½ 5,77 h; leonurine F **0,14 %** · t½ 2,48 h · CL 152 mL/min/kg · <6 % thu hồi nguyên vẹn · 12 glucuronide + 12 sulfate; stachydrine ức chế co tử cung 47,1 %/40,4 %) + **bảng tương tác QUYẾT ĐỊNH Coptis × glycyrrhizin** (AUC cửa 425,8→270,4 · AUC gan 29.500,8→15.422,4 ng·h/mL do tạo tủa, `32087732`) + **bảng 13 nguồn BỊ LOẠI kèm lý do mô/loài** (Cortex Phellodendri ≠ Coptis, rumen, gà, sản phụ người, chuột viêm đường thở, in-silico) + **bản đồ 8 chặng cho dược liệu KHÔNG hấp thu** (ích mẫu: đích = niêm mạc + vi sinh ruột, toàn bộ phần heo = `tag H`) + danh sách truy vấn hiệu quả/không hiệu quả.
- `scripts/check_batch_schema.py` — assert schema deliverable `batch-*.json` khung 8 chặng: đủ 20 khoá, `pmid` có mặt trong cả 8 chặng, `muc_bang_chung ∈ {I,A,R}`, `tag_H` là list; nhận cả MẢNG trần lẫn dict bọc; **in ra |set PMID duy nhất|** = con số đúng để viết `verified N/N`. Exit 1 = không ship. Chạy trước `validate_pmids_batch.py`.
