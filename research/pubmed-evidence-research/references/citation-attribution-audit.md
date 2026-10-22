# Audit attribution của PMID + bulk-edit tài liệu bằng chứng lớn

Nguồn: session fixgby `07b-research-co-che-goc-va-duong-di` (18/10/2026). Tài liệu 155 PMID,
~95 KB, tiếng Việt có dấu, CRLF, dùng U+2011 (non-breaking hyphen) và backtick trong ô bảng.

---

## 1. Lỗi thật KHÔNG phải "PMID bịa" — mà là "PMID thật gắn SAI claim"

`verify_pmids.py` / `validate_pmids_batch.py` chỉ chứng minh **PMID tồn tại** (`hitCount == 1`).
Trong session này **153/153 PMID tồn tại thật**, nhưng audit title-vs-claim phát hiện **~12 citation
gắn sai hoàn toàn chủ đề**. Đây là failure mode chính khi dựng tài liệu bằng chứng lớn.

Nguyên nhân: PMID được gán vào claim **theo vị trí trong danh sách kết quả tìm kiếm**, không theo
title đã đọc. Tài liệu vẫn "verify sạch" nếu chỉ đếm tồn tại.

### Ca thật (đã verify title qua Europe PMC `resultType=core`)

| PMID | Tài liệu ghi là | Title THẬT |
|---|---|---|
| 17456850 | "occludin knockout → hàng rào ruột" | Cani — *Metabolic endotoxaemia initiates obesity and insulin resistance* |
| 25063198 | (phiên trước đề nghị dùng thay) | ❌ **SAI MÔ** — *Deafness in occludin-deficient mice with dislocation of tricellulin and progressive apoptosis of the **hair cells*** → **tai trong**, KHÔNG phải hàng rào ruột. Xem §1b. |
| 28654658 | "LBP huyết thanh" | Butyrate → AMPK → tight junction trên **IPEC-J2 (tế bào ruột HEO)** |
| 22410503 | "LPS / sCD14 metabolic endotoxaemia" | IgA/IgM against gut commensals in chronic **depression** |
| 22457829 | "keratins as regulators of barrier function" | Gut permeability + **mesenteric fat inflammation** |
| 21151103 | "AMPK/PGC-1α" **và** "IL-6 → ectopic lipid" | Autophagy inhibits release of **mitochondrial DNA** → innate immunity |
| 7678183 | "IL-6 là cytokine rò rỉ" | **TNF-α from adipose tissue** → obesity-linked insulin resistance |
| 28914882 | "MMP-13, ADAMTS-4/5" | **SIRT3/SOD2** maintains osteoblast differentiation via mitochondrial stress |
| 39695103 | "độ dày sụn (MRI)" | **Hydroxyurea blunts mitochondrial energy metabolism** in osteoblast/osteoclast |
| 42761225 | "GLUT4 cần cho ống thận" | GFR estimation in **nephrotic** patients |
| 29962601 | "đề kháng insulin & mạch máu nhỏ não" | Intraperitoneal bupivacaine (Anesthesia Essays Res) |
| 36624273 | "toan chuyển hoá / bài tiết acid" | **FGF23** production & phosphate metabolism, bone-kidney |

Sinh ra 2 lesson dương tính:
- Nhiều bài "thừa" hoá ra **tốt hơn** bài định dùng cho claim đó (17456850 = bài gốc của trục
  gut→endotoxaemia→viêm; 28654658 = nguồn **HEO** cho cạnh G1↔G3 qua butyrate→AMPK).
  **Luôn đọc title trước khi bỏ một PMID** — gán lại thường rẻ hơn đi tìm bài mới.
- Claim không có bài nào chống đỡ → ghi `CHƯA CÓ NGUỒN (tag H)` và **xoá dòng**, không để nguyên.

### Quy tắc phòng ngừa (rẻ nhất)
Ghi cặp `(pmid → title thật)` **ngay lúc retrieve** (Europe PMC `resultType=core` / `lite` đã trả
title trong cùng response). Chỉ dựng claim từ title **đã đọc trong chính session**. Không bao giờ
gán PMID theo thứ tự dòng trong hit list — hit list chỉ để triage.

---

## 1b. Lớp lỗi THỨ HAI: PMID đúng CHỦ ĐỀ nhưng sai MÔ (tissue mismatch)

Đây là lớp lỗi khó hơn §1 và **sống sót qua cả audit chủ đề**. Claim đọc lên hoàn toàn đúng, cơ chế
cũng đúng, title cũng thuộc đúng chủ đề — nhưng nguồn đo ở **cơ quan khác** với cơ quan mà tài liệu
đang nói tới. Ca thật 18/10/2026 (cùng tài liệu `07b`, phát hiện ở lượt QC lại sau khi subagent khai
"đã complete and verified"):

| PMID | Tài liệu gán cho | Title THẬT nói | Loại sai |
|---|---|---|---|
| 29410610 | "thiếu máu-tái tưới máu ở **gan/thận**, nơi ATP sụp là sự kiện đầu" | *Disruption of Intracellular ATP Generation and Tight Junction Protein Expression during the Course of **Brain Edema** Induced by Subacute Poisoning of 1,2-Dichloroethane* | sai mô **và** sai nguyên nhân (ngộ độc, không phải thiếu máu) |
| 37245680 | "ATP ngoại bào → giảm ZO-1" (ngầm hiểu = ruột) | *…in hypoxic **cochlear strial marginal cells** in neonatal rats* | sai mô (ốc tai) |
| 25063198 | "chuột thiếu occludin → hỏng hàng rào ruột" | *Deafness in occludin-deficient mice … apoptosis of the **hair cells*** | sai mô (tai trong) |

### Hệ quả nghiêm trọng: ĐẾM NGUỒN ≠ CHẤM ĐIỂM BẰNG CHỨNG

Cạnh `C1 (G1→G3)` trong tài liệu có **3 nguồn** và được xếp "ĐÃ CHỨNG MINH". Sau audit: **chỉ 1/3
nguồn là ruột** (28366985, Caco-2 — đúng), 1 là hàng rào máu-não, 1 là tế bào ốc tai. Đúng ra phải
hạ bậc xuống **"CHỨNG MINH MỘT PHẦN"**.

**Luật rút ra:**
1. Mỗi dòng bảng bằng chứng phải ghi **MÔ + LOÀI CỦA NGUỒN**, không chỉ PMID. Cột `(I)/(A)/(R)` là
   *loại đối tượng*, KHÔNG phải *mô* — hai chiều độc lập, phải ghi cả hai.
2. Khi một cạnh có N nguồn nhưng chỉ k nguồn đo ở **đúng mô đích**, chấm điểm theo **k**, và ghi rõ
   `k/N nguồn đúng mô`. Ngoại suy liên cơ quan là **giả định**, không phải chứng minh.
3. Câu chữ phải nói ra giới hạn đó ngay trong dòng, ví dụ:
   `"⚠️ 3 nguồn nhưng chỉ 1 nguồn là RUỘT — ngoại suy sang ruột là giả định, không phải chứng minh."`

### Kết luận có thể bị ĐẢO CHIỀU (không chỉ hạ bậc)
Audit đúng nguồn có thể lật ngược kết luận và **giết cả một hướng can thiệp**. Ca thật:
tài liệu dùng chuột thiếu occludin để chống đỡ điểm chạm "KÍCH tổng hợp occludin". Title thật của
nguồn thay thế: `11102513` (*Complex phenotype of mice lacking occludin*, Mol Biol Cell 2000) và
`9548718` (*Occludin-deficient embryonic stem cells **can differentiate** into polarized epithelial
cells **bearing tight junctions***, J Cell Biol 1998) ⇒ **mất occludin KHÔNG phá được tight junction**;
occludin là protein **điều hoà**, không phải protein chịu lực duy nhất. ⇒ đề xuất "KÍCH occludin đơn
lẻ" **chết**. Không đọc title thật thì cả một hướng điểm chạm đi sai.

### Vì sao lớp lỗi này lọt
- Search `TITLE_ABS:"tight junction" AND ATP` trả về đúng chủ đề, chỉ khác mô — mắt người đọc title
  thấy "tight junction + ATP" là gật.
- Subagent tự khai *"verified N/N"* — con số đó **chỉ là cổng tồn tại**, không liên quan gì tới mô.
- Mô thường chỉ nằm trong **title hoặc abstract**, hiếm khi ở journal/từ khoá ⇒ phải đọc title thật.

---

## 2. Recipe audit: dump (PMID | title thật | dòng thật trong file)

Script 1 — với mỗi PMID nghi ngờ, in ra **title thật** + **mọi dòng trong file chứa PMID đó**:

```python
# .tmp_sus.py  (đọc danh sách PMID từ argv-file để khỏi phải sửa code)
import urllib.request, urllib.parse, json
P = r"D:/.../07b-....md"
lines = open(P, encoding="utf-8").read().split("\n")
BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
for pmid in [l.strip() for l in open("sus.txt") if l.strip()]:
    q = urllib.parse.urlencode({"query": f"EXT_ID:{pmid}", "format": "json",
                                "resultType": "core"})
    d = json.loads(urllib.request.urlopen(BASE + "?" + q, timeout=45).read()
                   .decode("utf-8", "replace"), strict=False)
    r = (d.get("result") or [{}])[0]
    print(f"PMID {pmid} | {r.get('pubYear')} | {r.get('title','')[:110]}")
    for j, L in enumerate(lines):
        if pmid in L:
            print(f"   F{j+1}: {L[:150]}")
```

Chạy theo lô **8–9 PMID** (report ~14 KB → vượt ngưỡng hiển thị nếu dài hơn): ghi report ra file,
rồi in từng nửa qua một script `show(a, b)` nhỏ. Gọi 2 terminal song song cho 2 nửa.

**Bản nhanh hơn (dùng ở lượt QC này):** validate theo lô 25 qua `EXT_ID:a OR EXT_ID:b …` với
`resultType=lite`, gom `{pmid: title}` vào 1 dict, rồi in **title của đúng danh sách PMID trụ cột**
(những PMID gánh claim chính, không phải toàn bộ danh sách tham chiếu). 165 PMID → **~12 giây**,
và dict title giữ lại được để đối chiếu tiếp. Đây là cách rẻ nhất để bắt lớp lỗi §1b.

**Bẫy heuristic — đừng dùng "token overlap" tự động:**
Thử so token Latin giữa title và dòng chứa PMID → **127/155 bị flag oan**, vì nhiều dòng chỉ là
danh sách `**(f) PMID chủ đạo**: [PMID:a] · [PMID:b] · ...` (không có từ cơ chế nào). Heuristic
overlap chỉ dùng được nếu loại trước các dòng "danh sách PMID". Cách chắc ăn: **audit bằng mắt**
trên dump ở trên, với danh sách nghi ngờ lấy từ các dòng có claim khớp *chủ đề gần* nhưng *mô hình
khác* (nephrotic, bupivacaine, hydroxyurea, FGF23…) — tức các PMID "trông hợp lý nhưng lệch".

**Đừng tin danh sách flag của lượt trước.** Ở lượt QC này, một PMID **đã được phiên trước "sửa đúng"**
(`25063198`, đề nghị dùng thay cho 17456850) hoá ra chính nó lại sai mô. Lượt audit sau phải kiểm lại
**cả những PMID đã được sửa**, không chỉ những PMID mới.

---

## 3. Bulk-edit tài liệu lớn: THAY THEO DÒNG bằng marker, không thay chuỗi dài

### Vì sao replace theo chuỗi chính xác thất bại ở đây
File có **CRLF**, **U+2011** (`‑`, non-breaking hyphen) trong `PGC‑1α`, `G1‑G3`, `IL‑6`, và
**backtick** trong bullet. Chuỗi `old` dựng lại từ trí nhớ/escape `\u2011` **không khớp** —
8/8 edit đầu tiên trả `NOTFOUND`, dù mắt thấy y hệt.

### Cách chạy được: JSON {marker, new_line} + applier theo dòng
Marker = **một đoạn plain-text duy nhất trong dòng** (tránh backtick/U+2011 trong marker).
Applier tìm dòng **duy nhất** chứa marker rồi thay **cả dòng**:

```python
# .tmp_apply2.py
import json
P = r"D:/.../07b-....md"
lines = open(P, encoding="utf-8").read().split("\n")
E = json.load(open(r"D:/.../.tmp_edits.json", encoding="utf-8"))
rep = []
for k, e in enumerate(E):
    hit = [i for i, L in enumerate(lines) if e["m"] in L]
    if not hit:      rep.append(f"NOTFOUND #{k} :: {e['m'][:70]}")
    elif len(hit)>1: rep.append(f"AMBIG #{k} ({len(hit)}) :: {e['m'][:70]}")
    else:
        lines[hit[0]] = e["n"]; rep.append(f"OK #{k} line {hit[0]+1}")
out = "\n".join(lines)
if not out.endswith("\n"): out += "\n"
open(P, "w", encoding="utf-8", newline="\r\n").write(out)   # GIỮ CRLF
print("applied", sum(r.startswith("OK") for r in rep), "of", len(E))
print("\n".join(r for r in rep if not r.startswith("OK")))
```

Ưu điểm: `AMBIG` bắt được marker trùng; `ok/fail` in ra ngay trong stdout (ngắn, không bị cắt);
luôn ghi `newline="\r\n"` để không đổi line-ending của tài liệu Windows.

Trước khi chạy applier, chạy script **kiểm marker tồn tại** (in `FOUND line N` / `MISSING` cho
từng marker) — nhanh hơn là chạy applier rồi mới phát hiện 8 dòng NOTFOUND.

**`NOTFOUND` không luôn là lỗi — phải xem nó là dòng nào.** Ở lượt này 66/67 edit khớp; edit duy nhất
NOTFOUND (#56, danh sách PMID của mục XƯƠNG KHỚP) hoá ra **đã đúng sẵn** (cùng tập PMID, khác thứ tự)
vì lượt applier trước đã sửa nó. Trước khi coi NOTFOUND là thất bại, in **dòng thật hiện tại** ra so
với nội dung mong muốn — khác thứ tự ≠ sai nội dung.

### CRLF: mode ĐỌC và mode GHI phải KHỚP NHAU
`newline="\r\n"` khi ghi **chỉ đúng khi đọc bằng text mode** (mặc định universal-newlines: CRLF được
dịch thành `\n` lúc đọc, rồi dịch ngược lại lúc ghi). Nếu đọc bằng **bytes** (`open(P,"rb").read()`)
thì `\r` vẫn còn trong dữ liệu; ghi text với `newline="\r\n"` sẽ thành **`\r\r\n`** (nhân đôi CR, file
phình ra và mọi diff vỡ). Cặp an toàn khi muốn tự kiểm soát line-ending:

```python
raw = open(P, "rb").read(); crlf = b"\r\n" in raw          # dò kiểu xuống dòng
t = raw.decode("utf-8").replace("\r\n", "\n")              # chuẩn hoá về \n
...
out = "\n".join(lines)
open(P, "wb").write((out.replace("\n", "\r\n") if crlf else out).encode("utf-8"))
```
Kiểm chứng 18/10/2026: file 198 dòng / 20.623 bytes sau khi ghi, `head`/`tail` đúng, CRLF nguyên vẹn.

---

## 4. Hai bẫy đọc/ghi file đã dính trong session này

- **`read_file` trên file lớn trả về bản ĐÃ TÓM TẮT, không verbatim.** Đọc 400 dòng (~42 KB) cho ra
  một rendering có "…" và chi tiết **bị tái tạo** — đủ để mình tưởng nội dung là X trong khi file
  ghi Y, rồi dựng sai toàn bộ chuỗi `old` để patch. **Luật: không bao giờ xây chuỗi exact-match từ
  một lần đọc lớn.** Đọc theo khoảng nhỏ (`read_file(offset, limit)` ≤ ~60 dòng cho vùng cần sửa),
  hoặc `search_files` để lấy dòng thật, hoặc `python .tmp_p.py <a-b>` in đúng dải dòng cần.
  Dấu hiệu nhận biết: `read_file` báo `read ... from line 1 (42,158 chars)` nhưng nội dung hiện ra
  có dấu hiệu lược bớt.
- **`execute_code` chứa code dài bị HARNESS CẮT giữa chừng**, không phải lỗi cú pháp: thân code bị
  thay bằng literal `...[truncated]` và script chạy thiếu đoạn cuối (im lặng, exit 0). Gặp lại
  nhiều lần trong session này. **Fix: ghi script ra đĩa bằng `write_file` rồi chạy
  `python .tmp_x.py` qua terminal.** Script ghi ra đĩa không bị cắt; cũng cho phép truyền tham số
  (`python .tmp_p.py 36-78`) để không phải viết lại code mỗi lần.

---

## 5. Quét MÂU THUẪN NỘI BỘ sau mọi lượt bulk-edit (bước bắt buộc, hay bị bỏ)

Bulk-edit sửa từng dòng độc lập, nên **bản tóm tắt ở cuối tài liệu thường còn bản CŨ** trong khi
phần thân đã sửa. Đây là lỗi do *quy trình*, không do nguồn — không cổng verify nào bắt được.

Ca thật `07b` sau khi áp 67 edit: 3 chỗ tự mâu thuẫn, phát hiện khi **đọc lại** chứ không phải khi sửa:

| Chỗ | Mâu thuẫn |
|---|---|
| `F.2` (kết luận bằng số) | trong **cùng một câu** vừa nói "6/6 cạnh có bằng chứng riêng lẻ" vừa kết "4/6 chứng minh, 2/6 tag H" |
| Bảng tra nhanh (dòng `VÒNG XOÁY`) | vẫn ghi **4/6** (C6 = tag H) trong khi bảng cạnh `A.4.3` đã sửa thành **5/6** |
| `A.4` kết luận | dùng "**đã chứng minh**" cho một vòng xoáy mà chính tài liệu ghi là chưa có nguồn nào mô tả |

**Checklist quét (chạy trên chính file, không cần mạng):**
1. Grep **các con số đếm** (`N/M`, `k/N`, `x/y nguồn`, `tag H`) → liệt kê **mọi chỗ xuất hiện** và so
   chúng với nhau. Bất kỳ cặp nào lệch ⇒ sửa cho khớp bảng gốc.
2. Đối chiếu **bảng tóm tắt cuối tài liệu** với **phần thân** theo từng dòng chủ đề.
3. Soát **động từ khẳng định** ở phần kết luận (`đã chứng minh`, `xác nhận`, `rõ ràng`) — chúng
   thường mạnh hơn mức bằng chứng thật. Hạ về mức trung thực: `có bằng chứng riêng lẻ`, `chứng minh
   một phần`, `giả thuyết heuristic`.
4. Mọi `tag H` ở phần thân phải **xuất hiện lại** trong phần kết luận/bảng cuối. Tag H bị mất khi
   đi qua bảng tóm tắt = che giấu khoảng trống.
5. Nếu tài liệu có mục "còn mở / chưa có nguồn", kiểm nó có **liệt kê đủ** các khoảng trống đã ghi
   rải rác ở phần thân không.

---

## 6. Tự công bố GIỚI HẠN của chính phép verify, ngay trong deliverable

`verified N/N` rất dễ bị đọc thành "tài liệu này đã đúng". Vì vậy phần validate trong tài liệu phải
nói thẳng nó **không** chứng minh gì. Khối đã dùng ở `07b` (PHẦN G), dùng lại nguyên mẫu:

```
> ⚠️ **GIỚI HẠN CỦA CHÍNH PHÉP VALIDATE NÀY — đọc trước khi trích dẫn.**
> Europe PMC chỉ xác nhận **PMID TỒN TẠI**, KHÔNG xác nhận **phát biểu gán cho nó là đúng**.
> Kiểm tra `verified=165/165` chỉ chứng minh không có PMID bịa. Nó KHÔNG chứng minh 165 phát biểu
> đều khớp nguồn.
> Vì vậy đã chạy thêm một lượt **đối chiếu TIÊU ĐỀ THẬT vs PHÁT BIỂU** trên các PMID trụ cột, và
> lượt đó **phát hiện lỗi gán sai** — đã sửa 12 chỗ (danh sách dưới). Những lỗi này **không thể
> phát hiện** bằng phép đếm `hitCount`.
>
> **RỦI RO CÒN LẠI:** 165 PMID mới chỉ được xác nhận tồn tại + đối chiếu tiêu đề ở nhóm trụ cột.
> Các PMID phụ trong danh sách "(f) PMID chủ đạo" **chưa** được đối chiếu tiêu đề từng cái.
> **Muốn trích dẫn ra ngoài: cần một lượt audit 165/165 tiêu đề-vs-phát biểu nữa.**
```

Kèm **danh sách đánh số các chỗ đã sửa** ở lượt QC (1. PMID X bị gỡ khỏi vị trí sai; 2. kết luận Y bị
đảo chiều; …). Người đọc sau cần biết **cái gì đã được kiểm và cái gì chưa**, không chỉ biết "đã verify".

---

## 7. Tự kiểm việc commit của chính mình (đừng suy đoán)

Sau khi `git add -A && git commit`, **đừng kết luận từ output ngắn của chuỗi lệnh** — một chuỗi `&&`
in ra 1 dòng không phải bằng chứng commit đã chạy hay chưa. Chạy kiểm riêng:

```
git log --oneline -3 ; echo "--- status:"; git status --short
```

`git log` hiện hash = đã commit; `git status --short` rỗng = sạch. Ở phiên này một chẩn đoán sai
("commit không chạy") tốn một vòng suy luận, trong khi `git log` cho thấy commit **đã** tồn tại.
