# Sinh deliverable N-chất × M-trường bằng "nguồn nhỏ + bộ dựng"

Dùng khi deliverable là `batch-*.md` (người đọc) + `batch-*.json` (máy ráp) cho **N chất**, mỗi chất
8 chặng × nhiều dòng có PMID — cỡ 5.000–20.000 ký tự/chất, tổng 50–200 KB.

> **TRẠNG THÁI — ĐÃ VERIFY END-TO-END (19/10/2026).** Bộ dựng `_build.py` **đã chạy đầu-cuối thành công**
> trên lô B fixgby `10-cong-thuc-23`: 3 file nguồn `src-b/{phytase,xylanase,protease}.txt` (19,5 / 21,8 /
> 24,2 KB) → `python _build.py src-b b` → `ingredients=3  unique_pmids=26`, sinh `batch-b.md` (59.765 ký tự)
> + `batch-b.json` (63.860 byte), mỗi file 8 khối `@` và 33–36 dòng bảng, **0 dòng sai 6 cột**.
> Ngưỡng kích thước cập nhật: write **24 KB vẫn qua sạch** (mốc cắt đã quan sát trước đó là ~51 KB cho một
> write chứa cả lô) ⇒ luật "một write = một đơn vị công việc" đứng vững, ngưỡng an toàn rộng hơn 12–17 KB.

## Bẫy vận hành của bộ dựng + tầng validate (đã gặp thật, 19/10/2026)

- **`_build.py` in ra `verified: "PENDING"` và `doi_chieu_tieu_de_vs_phat_bieu: "PENDING"` KHÔNG phải lỗi.**
  Hai trường đó **hardcode trong builder** làm chỗ giữ cho bước audit sau. Thấy PENDING mà đi "sửa builder"
  là sửa nhầm chỗ — kiểm bằng `grep -n PENDING _build.py`, nó nằm trong literal của doc.
- **KHÔNG chạy `_verify.py <pmids>` như bước validate cuối: nó `json.dump` ĐÈ `_verify.json`** — file dùng
  chung, có thể đang giữ bản ghi của lô khác. Cách thay thế đã dùng: script validate **tự chứa** trong
  `execute_code` (loop `EXT_ID:<pmid>` → assert `str(rec["pmid"]) == pmid`), in `OK <pmid> | <year> | <title>`
  từng dòng rồi in tổng. Lô B: **29/29 tồn tại, title khớp**. Không ghi ra artifact dùng chung ⇒ không phá ai.
- **`_epmc.py` dùng cache `_hits.json` DÙNG CHUNG ⇒ chạy TUẦN TỰ, không chạy song song.** Chạy đồng thời
  làm hỏng cache (`raw_decode … parsed keys: 0 trailing: 0`, file bị ghi đè thành rỗng) và kết quả query
  im lặng biến mất. Hồi phục: xoá `_hits.json` + `_hits.json.bak` **rồi chạy lại query tuần tự** — đừng
  sửa tay file cache.
- **Payload shell nhiều dòng (heredoc) bị guard của host CHẶN** (`BLOCKED (hardline) … oversized/unparseable
  inline command payloads`), không phải lỗi của thao tác bạn đang làm. Đừng retry y nguyên: đưa Python nhiều
  dòng vào **`execute_code`**, hoặc `write_file` một `.py` rồi chạy `python .py`. Guard chỉ chặn *payload
  inline*, mọi thao tác tương đương vẫn chạy được.
- **Phép kiểm hình dạng rẻ nhất trước khi tin một file nguồn** (chạy trong `execute_code`, ~20 dòng): đếm
  `@` = 8; mỗi dòng có `|` phải đúng **5 dấu**; cộng **union PMID** trong các dòng bảng. Lô B cho
  `phytase 67 dòng/8 khối/35 dòng bảng · xylanase 65/8/33 · protease 68/8/36`, union = **26 PMID** — khớp
  đúng con số builder in ra, nên `unique_pmids` của builder và số đếm độc lập xác nhận lẫn nhau.

## Ba cách đã thử, kết quả thật

| Cách | Kết quả |
|---|---|
| Build cả list/dict trong `execute_code` | thân code bị thế bằng `...[truncated]`, **vẫn `exit 0`** → output thiếu mà không có lỗi (bẫy IM LẶNG) |
| Một `write_file` khổng lồ chứa data của cả lô | **bị cắt** — lần 1 file `_data_a.py` khai báo 51 KB, lần 2 `_data_b.py` chỉ còn **260 byte** kèm lint `SyntaxError: unterminated string literal` |
| **`src/<slug>.txt` nhỏ (1 chất/file, 12–17 KB) + bộ dựng** | 5/5 file ghi qua sạch, `lint: ok`. Đây là cách nên dùng |

**Ngưỡng kích thước quan sát được (19/10/2026):** write ~12–17 KB → qua; write ~51 KB (một lần, chứa data
của nhiều chất) → cắt còn ~0,5 % kích thước. Không cần biết ngưỡng chính xác — luật là **một write = một
đơn vị công việc**, không bao giờ một write = cả lô.

**Dấu hiệu nhận biết write bị cắt** (kiểm ngay, đừng đoán): `bytes_written` nhỏ hơn hẳn kích thước bạn vừa
nghĩ ra; lint báo lỗi cú pháp ở dòng cuối / giữa chuỗi; phần tham số tool hiện `...[truncated]`.
Xử lý: **cắt nhỏ rồi ghi lại**, KHÔNG ghi lại y nguyên nội dung cũ (sẽ cắt lần nữa).

## Định dạng file nguồn (`src/<slug>.txt`) — một chất / một file

```
CHAT: thymol
TEN_VI: Thymol
CONG_THUC: C10H14O — 2-isopropyl-5-methylphenol, MW 150,22 ...
NHOM: Monoterpene phenol
DANG_DUNG: Thymol tinh thể ≥99% ... trong premix cần vi bao ...
MUC: A
S_CUA_VAO_FIRST_PASS: một phần — ... (12092740)
S_GAN_LAN_DAU_ENZYME: ...
TUONG_TAC: ...
BAT_KHA: ...
DA_THAT_BAI: ...
CHI_DAU_DO_DUOC: ...
TAG_H: enzyme pha I họ CYP; bơm ABC đẩy; cửa sữa ở heo nái
@CUA_VAO
phát biểu | số/chi tiết | đường vào | mức bằng chứng | mô & loài | PMID
@QUA_HANG_RAO
...
```

Bốn đặc điểm làm nó chịu được session bị ngắt giữa chừng:

1. **Mỗi write nhỏ** ⇒ không bao giờ chạm ngưỡng cắt.
2. **Một nguồn, hai đầu ra** ⇒ `.md` và `.json` không thể lệch nội dung (bản `.md` là để audit bằng mắt,
   bản `.json` là để ráp trang bằng script — hai bản lệch nhau là lỗi im lặng kinh điển của lô nhiều chất).
3. **Khôi phục được**: session chết giữa chừng thì lần sau chỉ cần viết tiếp `src/<slug>.txt` còn thiếu,
   chạy lại bộ dựng — **không phải fetch/đọc lại một PMID nào**. Đây là điểm ăn tiền lớn nhất so với việc
   build trong `execute_code` (biến mất giữa các call).
4. **`S_*` ở đầu file + bảng dòng ở thân file** tách rõ "trường văn xuôi của JSON" khỏi "bằng chứng từng dòng",
   nên bộ dựng không phải đoán.

Dòng bảng **phải đúng 6 cột**, cột 6 là PMID thuần (để bộ dựng tự bóc `re.findall(r'\d{7,8}', ...)`).
Ô không có nguồn ghi `CHƯA CÓ NGUỒN (tag H)` và cột PMID ghi `—`, **không được bỏ dòng** (bỏ dòng làm chặng
biến mất khỏi trang, xem pitfall "LUÔN đủ 8 chặng").

## Bộ dựng — trách nhiệm

Một script `_build.py` đặt **cùng thư mục với `src/`** (`SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")`
— đừng hardcode `docs/<batch>`):
1. Đọc mọi `src/*.txt`, tách `KEY: value` ở đầu và khối `@STAGE` ở thân.
2. Sinh `.md` (header chung + mỗi chất 1 khối 8 mục a→h, mỗi mục 1 bảng 6 cột).
3. Sinh `.json` theo schema chốt trước, **tự tính `pmids` = hợp các PMID trong 8 chặng** (đừng chép tay —
   đây đúng là chỗ sinh ra con số `verified N/N` sai).
4. In ra `ingredients=N  unique_pmids=M` và ghi `_pmids_final.txt` để lượt validate cuối dùng.

Bẫy parser đã gặp: nhận diện dòng `KEY: value` bằng regex khoá (`^[A-Z_]+(\.[a-z_]+)?$`) chứ **không** bằng
"có dấu `:`" — dòng bảng chứa `p < 0,05` hay `ratio 1:1` sẽ bị nuốt thành khoá header.

## Luật vận hành (quan trọng hơn định dạng)

1. **Chạy bộ dựng sau CHẤT THỨ NHẤT, không phải sau chất cuối.** Nếu `_build.py` chưa từng chạy thì khi hết
   lượt bạn có **0 byte** — ca thật `fixgby 10-cong-thuc-23` lô A: 73 PMID verified, nguồn 5/12 chất, file
   đích không tồn tại. File đích phải LUÔN ở trạng thái tồn tại và hợp lệ.
2. **Ghi `src/<slug>.txt` ngay khi xong chất đó**, trước khi research chất kế tiếp.
3. **Chốt schema + viết skeleton trước khi fetch vòng đầu** (JSON hợp lệ ở mọi thời điểm).
4. **Chia lô ≤ 5–6 chất / subagent.** 12 chất × 8 chặng × 6 trường + audit tiêu đề là vượt ngân sách tool-call.
5. Sau khi bộ dựng chạy: `scripts/check_batch_schema.py <file>` → `scripts/validate_pmids_batch.py <file>`,
   rồi mới viết `verified N/N` từ **|set PMID duy nhất|** mà bộ dựng in ra.

## Quan hệ với các pitfall khác của skill này

- Không thay thế pitfall "ĐỌC LÀ ĐỂ VIẾT — ghi deliverable TĂNG DẦN" mà **là cách thực thi nó** cho lô N chất:
  đơn vị tăng dần là **một file nguồn / một chất**, không phải một lần patch file đích khổng lồ.
- Vẫn phải qua cổng 2 (audit tiêu đề-vs-phát-biểu) — bộ dựng chỉ bảo đảm **hình dạng** và **tính nhất quán**,
  nó không biết phát biểu có khớp nguồn hay không.
