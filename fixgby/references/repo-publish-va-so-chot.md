# fixgby — repo, số chốt, publish (cập nhật 20/10/2026)

## Repo đã đóng gói + ĐÃ publish private

`D:/Hermes Proj/fixgby` — git repo, 176 file track, 11,4MB, không có token/key lọt.
**Đã push private: `github.com/ntquang1110/fixgby`** — branch `main`, HEAD `9f754e0`. Verify bằng API (không mở trình duyệt): `GET /repos/ntquang1110/fixgby` → `private=true`, `default_branch=main`; `GET .../commits/main` sha **trùng `git rev-parse HEAD`**; `GET .../git/trees/main?recursive=1` → 176 blob, đủ 7 file `data/*`.

Auth (20/10/2026): PAT đã có sẵn trong `~/AppData/Local/hermes/.env` khoá `GITHUB_PAT_B64` (base64) → giải mã rồi `gh auth login --with-token` (token qua **stdin**, không để lộ argv) + `gh auth setup-git`. **Không dùng device flow / mở trình duyệt** — Quang đã bác đúng cách đó.
Lịch sử dọn + push: `699599a` (4 file data vào version, `.gitattributes`, README viết lại) → `9cb4806` (giữ script lieu-san) → `5e2a017` (sửa 52 điểm giao + nhãn print) → `6dd26a7` (bỏ đường dẫn tuyệt đối) → `9f754e0` (mục 12 của `09-lieu-san.md`).

**Hoàn chỉnh = clone sạch build lại ra ĐÚNG hash.** Đã kiểm bằng `git clone` **từ chính GitHub** rồi chạy 4 script trong bản clone; sha256 bản clone == bản gốc:

```
do-thi-duong-di-benh.html   411302a7c092   = gốc
do-thi-duong-di.html        6b4d94fccd5a   = gốc
hoat-chat-mo-rong.html      1c579bb51b1d   = gốc
lieu-san-cong-thuc.html     91ff9c3242af   = gốc (chạy 3 lần, cùng hash)
repo gốc sau khi chạy script ở bản clone: git status RỖNG
log: mầm 28 | điểm cắt 238 (70/87/75) | điểm neo 2 bên 17 | PMID 287
```

## Lỗi đường dẫn tuyệt đối (vá 20/10 — lỗi im lặng, tệ hơn file rác)

`visual/_gen-lieu-san.py` hardcode `CB = r"D:/Hermes Proj/fixgby/docs/14-cong-thuc-co-ban"`; `visual/_gen_hoat_chat.py` hardcode cả input lẫn output. Hệ quả: chạy trong **bản clone** mà vẫn ghi ngược về **repo gốc** (xảy ra thật: file trong repo gốc bị sửa lúc 13:09), log in ra số y hệt nên nhìn không thấy.

Đã vá thành `os.path.join(D, "..", "docs", ...)` với `D = os.path.dirname(os.path.abspath(__file__))`. Quét lại toàn repo: **0 đường dẫn tuyệt đối**. Script mới trong `visual/` phải dùng `__file__`, không bao giờ viết `D:/...`. Sau khi vá, phép thử "chạy trong clone → repo gốc còn sạch" là bằng chứng bắt buộc.

## 4 file data PHẢI vào version (từng bị `.gitignore` chặn → clone về trang trắng)

```
data/diem-neo.json        454 KB   cầu nối bệnh ↔ chất (17 neo)
data/node-glossary.json    20 KB   từ điển mã điểm chạm
data/tuong-tac.json        38 KB   49 cặp tương tác
data/o-trong.json           3 KB   ô trống theo chặng
```
`.gitignore` giữ `data/*` rồi whitelist từng file (`!data/...`) — thêm file data mới thì phải thêm dòng `!` tương ứng, không thì build ở bản clone thiếu dữ liệu mà không báo lỗi.
Giữ luôn: `visual/_gen-lieu-san.py`, `visual/_build-lieu-san.py`, `visual/_duong-cong.json`, `visual/lieu-san-cong-thuc.html`.

## Số chốt 20/10/2026 (dùng để đối chiếu, đừng chép lại số khác)

| Chỉ số | Số đúng | Ghi chú |
|---|---|---|
| Mầm × chặng | 28 × 8 | 224 ô, **0 ô trống** |
| Điểm cắt | **238** | 70 cắt được · 87 một phần · 75 khó cắt · **6 ô tag H** |
| Neo nối 2 tầng | **17** | trước 14 |
| Neo một bên | **5** | APN · TLR4 · NF-κB · bổ thể · kênh |
| PMID tầng bệnh | **287** mã duy nhất trong dữ liệu | 21/10/2026: con số **288 là ĐẾM SAI** — file đối chiếu có khoá rác `"287"` (một số đếm lọt vào trường `pmid`) và 1 PMID thật 6 chữ số (`905119`) bị regex `\d{7,8}` bỏ qua im lặng. Đã bỏ khoá rác, verify lại **287/287 tồn tại**. Trang in "287" là ĐÚNG |
| Tầng chất | 40 chất · **766** cạnh · 122 điểm chạm đặt tên | |
| Điểm bị ≥2 chất chạm | **52** | KPI thật; từng báo sai 119 vì đọc `len(giao[:160])` |
| Công thức | 26 nguyên liệu · 23 công thức / 5 dòng | |

6 ô tag H giữ nguyên, không lấp: TGEV lan hệ thống · RVC nhân lên · RVC lan hệ thống · PCV3 xâm nhập · SIV hậu quả · ký sinh thiếu số đo trên trại công nghiệp.

## Publish preview

- Bệnh 28×8: `https://preview.thefirstonly.com/6wja2542rq49`
- Chất 40 chất: `https://preview.thefirstonly.com/gopr1s8m0rf5`
- Slug chốt ở `visual/preview-links.json`. KV store **không lưu slug** → phải publish theo vòng: build → publish → ghi link vào `preview-links.json` → build lại → publish lại. Không suy ra link từ URL.
- `content-upload.py` dùng `timeout=180` (30s làm đứt kết nối với payload ~650KB+). Lỗi `TimeoutError`/`ConnectionReset` là do timeout, **không phải file quá lớn** — đừng minify để chữa.
- Bảng câu chung đã gom (443 câu dùng lại) → payload 991KB còn 749KB, không mất nội dung.

## Cổng kiểm + CI (21/10/2026)

- `tools/kiem-so-lieu.py` — copy repo ra chỗ tạm, build lại 4 trang, so **từng ký tự** với bản trong repo (bỏ qua ngày tháng), in dòng đầu tiên khác nhau, exit 1 khi lệch. Bắt cả HTML sửa tay lẫn số lệch do đổi dữ liệu nguồn.
- `.github/workflows/kiem-so-lieu.yml` — mỗi push lên `main` chạy 2 cổng: so 4 trang + verify toàn bộ PMID Europe PMC (`resultType=core`).
- `tools/verify-pmid.py` nay coi PMID **sai định dạng** (không phải 6–8 chữ số) là LỖI và exit 1 — không bỏ qua im lặng. Đừng nới lỏng lại: chính chỗ bỏ qua đó đã làm lọt khoá rác và nuốt PMID 6 chữ số.
- **Kiểm cổng phải kiểm CẢ HAI CHIỀU.** Đã làm: commit cố tình sửa 1 số trong HTML → CI đỏ, log chỉ đúng dòng 92 (`repo '99' | build '52'`) và bước PMID bị skip; revert → CI xanh (`4/4 trang khớp`, `287/287 PMID`). Chỉ đọc `conclusion: success` là chưa chứng minh gì — bước vẫn có thể chạy mà không làm gì.
- **Đọc log THẬT, đừng tin kết luận job:** `gh run view <id> --log | grep -E "trang khop|ton tai:|LECH"`; chờ bằng `gh run watch <id> --exit-status`; xem bước nào chạy bằng `gh run view <id> --json jobs -q '.jobs[0].steps[]'`. Endpoint `/actions/jobs/{id}/logs` trả redirect sang blob và **từ chối header Bearer** → dùng `gh run view --log`, đừng loay hoay với API.
- Push private: PAT base64 ở `~/AppData/Local/hermes/.env` (`GITHUB_PAT_B64`) → `gh auth login --with-token` + `gh auth setup-git`; URL remote giữ trơn, kiểm `.git/config` không dính token.
- Chuỗi commit tiếp: `68c9a87` (thêm cổng kiểm + workflow) → `cfbfb01` (sửa 288→287, verify-pmid báo lỗi định dạng, README thêm mục cổng kiểm) → `6d1bb2c` (TEST cố tình sai) → `11c08b2` (revert) → HEAD `1afac94`. CI xanh ở lần push cuối.

## Tool trong repo

- `tools/verify-pmid.py` — kiểm PMID theo Europe PMC (`--file <json|html>` quét PMID trong file, `--out` ghi kết quả, `--workers`).
- `docs/11-duong-di-benh/_verify-pmid-toan-trang.json` — evidence 288 PMID.
- `docs/14-cong-thuc-co-ban/verify-so-lieu-pmid.py` — kiểm **số liệu cụ thể** trong abstract (mỗi PMID kèm danh sách chuỗi số phải xuất hiện).
