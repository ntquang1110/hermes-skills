# Hợp đồng file nguồn `src/<slug>.txt` — khung 8 chặng

Áp cho các thư mục lô trong fixgby: `docs/09-tra-cuu-duong-di/`, `docs/10-cong-thuc-23/` (lô A `src/`,
lô B `src-b/`). Một **nguyên liệu = một file nhỏ 12–24 KB ≈ 65 dòng**. Mẫu chuẩn để chép: `src/thymol.txt`.

> ⚠️ **Đọc mục "Trạng thái lô" ở cuối file này TRƯỚC khi research** — file trạng thái cũ
> (`lop-a-12-nguyen-lieu-8-chang.md`) đã từng ghi "batch-a chưa tồn tại, 5/12 chất" trong khi thực tế
> builder đã chạy và 9/12 chất đã xong. Trạng thái trong dự án này đổi mỗi lượt; **đừng research lại chất đã ✅**.

## Định dạng bắt buộc

Mỗi dòng `KEY: value`. Khoá đầu file **phải khớp `^[A-Z_]+$`** (chữ hoa + gạch dưới, không số).
Dòng bảng có **đúng 5 dấu `|`** = 6 cột:

```
phát biểu | số/chi tiết | đường vào | mức bằng chứng | mô & loài | PMID
```

**Ba luật mà bộ parse phụ thuộc vào — sai một cái là hỏng im lặng:**

1. Dòng bảng **KHÔNG được bắt đầu bằng `|`**. Bộ parse **bỏ qua** mọi dòng bắt đầu bằng `|` (đó là chỗ
   dành cho dòng kẻ bảng của builder).
2. Đúng **5** dấu `|` — 4 hoặc 6 dấu thì dòng bị coi là không hợp lệ và chặng đó rỗng trên `batch-*.md`.
3. Giá trị của khoá đầu file **không được chứa `|`** (nó sẽ bị hiểu thành phân cách cột).

## ⚠️ Khoá `S_THAI_TY_LY` (spec) ≠ `S_THAI_TY_LE` (builder) — field RỖNG mà exit 0

**Đây là bẫy hợp đồng nguy hiểm nhất của file này, dính thật 19/10/2026.**

Đề bài giao subagent liệt khoá `S_THAI_TY_LY`, nhưng `_build.py` sinh tên khoá từ list `SCALARS`
(`"thai.ty_le"` → `S_THAI_TY_LE`) và đọc bằng `head.get(k, "")`. Viết đúng theo đề bài ⇒ builder
**không báo lỗi**, chỉ lặng lẽ ghi `thai.ty_le: ""` vào JSON, vẫn in `ingredients=N`, vẫn `exit 0`.
2/3 file của lô A dính đúng lỗi này.

**Luật: phát CẢ HAI khoá, giá trị y hệt.**

```
S_THAI_TY_LE: <cùng nội dung>
S_THAI_TY_LY: <cùng nội dung>
```

`parse()` nhận mọi khoá khớp `^[A-Z_]+$` nên khoá thừa vô hại; thiếu khoá thì mất dữ liệu im lặng.

**Trước khi viết, diff đề bài với builder** — hai nguồn sự thật khác nhau và không ai bắt chúng khớp:

```python
import re
src = open("_build.py", encoding="utf-8").read()
sc  = re.search(r"SCALARS\s*=\s*\[(.*?)\]", src, re.S).group(1)
need = {"S_" + k.strip().strip('"').replace(".", "_").upper()
        for k in re.findall(r'"[a-z_]+\.[a-z_]+"', sc)}
print(sorted(need))   # đối chiếu với danh sách khoá trong đề bài
```

Cùng họ với pitfall 27 của `fixgby` ("builder im lặng làm rơi trường là kiểu hỏng tệ nhất").

## Kiểm TRƯỚC khi chạy builder (bắt buộc)

```python
L = open(p, encoding="utf-8").read().splitlines()
print("lines:", len(L))
bad = [i+1 for i,l in enumerate(L)
       if l.strip() and not l.startswith(("@","#")) and "|" in l
       and not l.startswith("|") and l.count("|") != 5]          # bad PHẢI là []
blocks = [l for l in L if l.startswith("@")]                     # PHẢI đúng 8 tên viết hoa
assert blocks == ["@CUA_VAO","@QUA_HANG_RAO","@GAN_LAN_DAU","@GAN_DE_DI",
                  "@TOI_MO","@RA_KHOI_TE_BAO","@THAI","@O_LAI"], blocks
```

Tên khoá sai chính tả (vd `@RA_KHOI_TEBAO`) hoặc một dòng 7 cột làm chặng **biến mất khỏi `batch-*.md`**
mà builder vẫn `exit 0`. Không có phép kiểm này thì lỗi chỉ lộ ra khi đọc trang HTML thành phẩm.

## Kiểm SAU khi chạy builder

`python _build.py src a` chỉ in ra `ingredients=N unique_pmids=M` — **không** chứng minh mọi chất vào được
output. Xác nhận trên `batch-a.md`:

```python
t = open("batch-a.md", encoding="utf-8").read()
print(t.count("|---|---|---|---|---|---|"))   # ≈ số chất × 8 bảng chặng
print(t.count("<slug>"))                     # >= 1
```

`|---|---|---|---|---|---|` là dấu vân tay của bảng 6 cột. Đếm bằng tay trên bảng markdown kiểu `| ... |`
sẽ sai (mỗi dòng có 6 dấu `|`, không phải 5) — đếm bằng số bảng, không đếm dòng.

**Và phải assert mọi field scalar ĐÃ ĐIỀN** — `exit 0` chỉ chứng minh parse được, không chứng minh có dữ liệu
(bẫy `S_THAI_TY_LY` ở trên):

```python
import json
d = json.load(open("_batch_a_raw.json", encoding="utf-8"))
for c in d["chat"]:
    empty = [f"{s}.{k}" for s in ("cua_vao","qua_hang_rao","gan_lan_dau","gan_de_di",
                                  "toi_mo","ra_khoi_te_bao","thai","o_lai")
                   for k, v in c[s].items() if k != "pmid" and not v]
    print(c["chat"], "EMPTY:", empty or "none",
          "| pmids/chặng:", [len(c[s]["pmid"]) for s in
          ("cua_vao","qua_hang_rao","gan_lan_dau","gan_de_di","toi_mo","ra_khoi_te_bao","thai","o_lai")])
```

`EMPTY` phải là `none` ở mọi chất, và mọi chặng phải có ≥1 PMID (chặng 0 PMID = chặng rỗng trên trang HTML).

## Bẫy `_epmc` đã dính (dùng lại, đừng dựng mới)

- **Response Europe PMC dùng khoá `resultList`, KHÔNG phải `resultSet`.** Viết sai khoá ném
  `KeyError: 'resultSet'` — rất dễ chẩn đoán oan thành "query quá dài" hoặc "mạng hỏng" rồi đi giảm số id
  mỗi lô vô ích. **Khi batch `EXT_ID` trả rỗng, kiểm TÊN KHOÁ trước tiên.**
- **Cache hỏng khi >1 tiến trình ghi đồng thời — và ">1 tiến trình" gồm cả 2 tool-call SONG SONG trong
  CÙNG một session** (dính 19/10/2026: hai lệnh `terminal` chạy parallel, cả hai gọi `_epmc.search()`).
  `_epmc` ghi `_hits.json` sau MỖI lần search ⇒ hai `json.dump` chồng nhau, file thành `{...}{...}`, lượt
  sau chết với **`Extra data: line 4223 column 2 (char 1055960)`** — đọc lên như cache/API hỏng vĩnh viễn.
  Gán cache riêng TRƯỚC khi fetch, **và** đừng gọi helper ghi-cache từ hai tool-call song song (gộp mọi
  query vào một script tuần tự):
  ```python
  _epmc.HITS = os.path.join(_epmc.HERE, "_hits_<slug>.json")
  _epmc.ABS  = os.path.join(_epmc.HERE, "_abs_<slug>.json")
  ```
  Cứu file: cắt về `}` hợp lệ cuối rồi `json.loads`; lùi mãi vẫn fail thì **reset `{}`** — cache chỉ là
  tiền tốc độ, mất rẻ hơn sửa sai.
- Gom **~15 PMID / lô** trong một query `EXT_ID:a OR EXT_ID:b ...` là vùng an toàn.

## Luật `DA_THAT_BAI`: ID bạn KHAI ĐÃ LOẠI cũng phải verify

`DA_THAT_BAI` là chỗ rửa nguồn bịa dễ nhất: liệt một PMID **không tồn tại** kèm lý do loại nghe hợp lý thì
**không phép kiểm nào ở trên bắt được** — mọi checker chỉ đi tìm PMID *được TRÍCH*. Phải verify cả danh sách
loại, và phải khớp **lý do loại** với `title` thật:

```python
ids = [...]            # MỌI id nằm trong DA_THAT_BAI của MỌI chất trong lô
for i in range(0, len(ids), 8):                       # 8 id/lô là vùng an toàn
    q = " OR ".join("EXT_ID:%s" % x for x in ids[i:i+8])
    url = base + urlencode({"query": "(" + q + ")", "format": "json",
                            "resultType": "core", "pageSize": "25"})
    d = json.load(urllib.request.urlopen(url, timeout=60))
    got = {str(r.get("pmid") or r.get("id")): r.get("title", "")
           for r in d.get("resultList", {}).get("result", [])}    # resultList, KHÔNG resultSet
    for x in ids[i:i+8]:
        print(x, "|", got.get(x, "*** NOT FOUND ***"))             # sentinel BẮT BUỘC
```

`*** NOT FOUND ***` **phải bằng 0**. Rồi tự đọc `title` và hỏi *"tiêu đề này có đúng lý do mình loại không"* —
**loại-theo-loài chỉ hợp lệ khi loài nằm NGAY TRONG TITLE** (`... on broilers`, `... in lambs`,
`... from Apis mellifera`). Lượt 20/10/2026: **33/33 id loại/giới hạn verify đạt** (31 PMID + 2 id `IND*` —
endpoint `EXT_ID` trả được **cả** id `IND*` của Europe PMC, không chỉ PMID), 0 cái phải sửa.
Tiêu đề hay dính HTML **hai lớp** — `&lt;i&gt;Bacillus subtilis&lt;/i&gt;` **và** `<i>…</i>`:
`html.unescape` → strip → lặp lại trước khi so chữ.

## Bẫy escape: `write_file` làm lọt gạch-chéo-ngược + nháy kép vào `.txt`

Lượt 20/10/2026, `src-b/bacillus-subtilis.txt` ra đời với **7 chỗ escape nguyên xi** ở đúng những ngoặc kép
lẽ ra phải sạch. File vẫn parse sạch, builder vẫn `exit 0` — **lỗi chỉ lộ khi grep**. Kiểm ngay sau write
đầu tiên của mỗi chất:

```bash
grep -c '\\"' src-b/<slug>.txt      # PHẢI = 0
```

Có thì sửa bằng `patch(old_string='\"', new_string='"', replace_all=True)` rồi **chạy lại builder** — sửa
nội dung SAU khi build xong là build hết hiệu lực (số dòng trong báo cáo cũng phải đọc lại). Muốn tránh
hẳn: **đừng dùng ngoặc kép trong value** — thay bằng `'…'` hoặc `«…»`; văn phong tài liệu không cần `"`.

## Trạng thái lô A `10-cong-thuc-23` (chốt 19/10/2026, cuối lượt)

**`batch-a.md` + `_batch_a_raw.json` ĐÃ TỒN TẠI** — `python _build.py src a` →
`ingredients=10 unique_pmids=87` (cập nhật 19/10/2026, sau khi xong Ích mẫu). **10/12 chất đã có `src/*.txt`.**
2 chất còn thiếu: Huyết dụ (*Cordyline terminalis*) · Dịch chiết lá hẹ (*Allium tuberosum*).

| # | Chất | File | Trạng thái |
|---|---|---|---|
| 1 | Thymol | `src/thymol.txt` | ✅ 14,6 KB |
| 2 | Carvacrol | `src/carvacrol.txt` | ✅ 12,5 KB |
| 3 | Eucalyptol | `src/eucalyptol.txt` | ✅ 13,5 KB |
| 4 | Propolis | `src/propolis.txt` | ✅ 14,5 KB |
| 5 | Glycyrrhizin | `src/glycyrrhizin.txt` | ✅ 17,1 KB |
| 6 | Berberine | `src/berberine.txt` | ✅ 18,3 KB |
| 7 | Hoàng liên | `src/hoang-lien.txt` | ✅ 16,7 KB |
| 8 | Tannin Chestnut | `src/tannin-chestnut.txt` | ✅ 23,6 KB / 66 dòng |
| 9 | Tannin Quebracho | `src/tannin-quebracho.txt` | ✅ 22,1 KB / 65 dòng |
| 10 | Ích mẫu | `src/ich-mau.txt` | ✅ 14,6 KB / 59 dòng |
| 11 | Huyết dụ | — | ❌ |
| 12 | Dịch chiết lá hẹ | — | ❌ |

Bank bằng chứng của 2 chất tannin: `pubmed-evidence-research/references/feed-additive-8stage-tannin-notes.md`
(32 PMID verify 32/32, 9 PMID heo in-vivo, danh sách nguồn bị loại vì sai mô/loài).

Bank của **Berberine · Hoàng liên · Ích mẫu** (42 PMID verify 42/42, 19/10/2026):
`pubmed-evidence-research/references/feed-additive-8stage-berberine-coptis-leonurus-notes.md`.
⚠️ Trong đó có **tương tác nội công thức phải xử lý trước khi chốt liều**: dịch chiết **cam thảo
(glycyrrhizin, nguyên liệu #5 cùng lô) tạo tủa với hoàng liên**, làm AUC berberine ở tuần hoàn cửa
425,8 → 270,4 ng·h/mL và ở gan 29.500,8 → 15.422,4 (`32087732`) ⇒ nếu hai nguyên liệu nằm chung một
premix thì phải tách bao/granulation hoặc kiểm lại liều, đừng chỉ cộng hàm lượng.

## Ngân sách viết một chất

- **~14 KB bài viết ≈ 20 tool-call.** Chất phải phủ định nhiều `tag H` (tannin, enzyme) tốn hơn.
- **Ngân sách ĐỌC ≤ ~6–8 PMID/chất** khi chất đã có cụm bằng chứng heo in-vivo. Bằng chứng thứ 11 cho
  cùng một luận điểm gần như không tăng giá trị — và đọc mãi rồi hết lượt là kiểu thất bại tệ nhất
  (đã xảy ra 2 lần trong dự án: 0 byte deliverable sau 8 vòng truy vấn).
- **Ghi file ngay sau CHẤT ĐẦU TIÊN**, rồi `write_file` lại sau mỗi chất. Chạy builder ngay khi còn ngân
  sách — `batch-a.md`/`json` do builder sinh, **không tự viết tay**.
- Một `write_file` 12–24 KB qua sạch; một write ~51 KB bị cắt còn 260 byte. Đừng gộp lô vào một write khổng lồ.

## Trạng thái lô B `10-cong-thuc-23` (chốt 20/10/2026) — **ĐỦ 7/7**

`python _build.py src-b b` → **`ingredients=7  unique_pmids=80`**, exit 0. `batch-b.md` có **56 khối**
`## a)` … `## h)` = 7 chất × 8 chặng.

| # | Chất | File | Trạng thái |
|---|---|---|---|
| 1 | Phytase (coated) | `src-b/phytase.txt` | ✅ 67 dòng |
| 2 | Xylanase (coated) | `src-b/xylanase.txt` | ✅ 65 dòng |
| 3 | Protease (coated) | `src-b/protease.txt` | ✅ 68 dòng |
| 4 | Acid citric | `src-b/acid-citric.txt` | ✅ 28.147 byte |
| 5 | Betaine HCl 98 % | `src-b/betaine-hcl.txt` | ✅ 33.633 byte |
| 6 | *Bacillus subtilis* (bào tử) | `src-b/bacillus-subtilis.txt` | ✅ 70 dòng · 8/8 khối |
| 7 | Calcium butyrate | `src-b/ca-butyrate.txt` | ✅ 77 dòng · 8/8 khối |

Bank bằng chứng cả 7 chất (kể cả 2 chất chốt 20/10 — §2.9):
`pubmed-evidence-research/references/feed-additive-8stage-enzyme-probiotic-notes.md`.

**Luật riêng của lô này — KHÁC lô A.** Nguyên liệu **không hấp thu vào máu**; mô đích thật là
**LÒNG RUỘT + VI SINH RUỘT** ⇒

1. Chặng 2 **phải nêu CƠ CHẤT tác động** (phytate→inositol phosphate · xylan→xylose/AXOS · protein→peptide)
   hoặc **cơ chế lên hệ vi sinh** (cạnh tranh chỗ bám · sinh acid hữu cơ · bacteriocin · điều hoà miễn dịch
   niêm mạc). Chặng 2 để trống cơ chất = file vô nghĩa.
2. **Vi sinh phải ghi CHỦNG ở MỌI nguồn** (DE111 · DSM 5750 · MB40 · PB6 · B.S-Dia · 87Y · 1BP1Co1 · DB9011 ·
   541 · M2). Cùng loài khác chủng = khác kết quả ⇒ 1 dòng không có chủng là 1 dòng không kiểm chứng được.
3. Với vi sinh, chặng 6 và 8 **gần như luôn `tag H`** — và phải phân biệt **bơm xuất bacteriocin của
   VI KHUẨN** với **bơm ABC của tế bào ruột HEO**; gán lẫn hai cái là lỗi mô nghiêm trọng.
   **Đừng mặc định cả lô là tag H**: calcium butyrate CÓ bơm ra thật (BCRP/ABCG2 + MCT4, `41596106`).
4. `MUC` khai theo cấp cao nhất THẬT của chính loài và **phải nói rõ "chưa có cấp A trên HEO"** khi cấp A
   đến từ chuột/gà/C. elegans.
5. Duyệt cuối: `python _build.py src-b b`, tự kiểm thêm **8 khối `@` mỗi file**, **mọi dòng bảng đúng 5 dấu
   `|`**, và `grep -c '\\"'` = 0 (bẫy escape ở mục trên).
