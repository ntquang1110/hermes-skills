# Tích hợp deliverable research vào tài liệu dự án (append-only) — quy trình + verify

**Lớp việc:** một research file MỚI hoàn thành (vd `06a-research-*.md`) cần được **tích hợp vào một PLAN/SPEC đang chờ duyệt** (vd `05-plan-*.md`) mà **không viết lại cấu trúc plan**, rồi cập nhật nhật ký và commit. Đã chạy thật 18/10/2026 cho dự án **fixgby**.

Nguyên tắc: bên nhận yêu cầu (thường là subagent) phải trả về **bằng chứng thật** (diff stat + commit hash), không bao giờ báo "xong" khi chưa có commit.

## 1. Quy tắc bắt buộc khi viết mục bổ sung

- **CHỈ THÊM**: mục mới ở CUỐI file, đặt tên dạng `## Phụ lục A — Bằng chứng từ research <mã> (bổ sung DD/MM/YYYY)`.
- **Mọi số liệu phải truy được về 1 trong 2 nguồn**: file research mới, hoặc chính plan. Không có nguồn ⇒ ghi **`chưa có nguồn (tag H)`** thay vì khẳng định. **Không bịa PMID/DOI/tên bài/số liệu.**
- Khi đề xuất **đổi số của plan** (trọng số, ngưỡng): ghi rõ đây là *đề xuất/quyết định kỹ thuật của dự án*, **không phải** số liệu lấy từ research — vì tài liệu research thường KHÔNG công bố trọng số/ngưỡng nào.
- Nếu bằng chứng **ủng hộ giữ nguyên** thì phải ghi rõ "giữ nguyên, vì …" — không được im lặng bỏ qua.
- Thêm ghi chú "nếu phụ lục mâu thuẫn với câu nào ở trên thì **phụ lục này thắng** cho tới khi user duyệt bản sửa chính thức" — để không phải sửa thân plan.
- Cấu trúc 5 mục đã kiểm chứng: **A.0** quy ước nhãn · **A.1** bảng bằng chứng theo đối tượng (kết luận ngắn TỐT / CÓ ĐIỀU KIỆN / KHÁC + tầng mạnh/yếu + cảnh báo + citation) · **A.2** cảnh báo BẮT BUỘC phải phản ánh vào công thức (đánh mã R1..Rn) · **A.3** đề xuất chỉnh ngưỡng/trọng số (kèm lý do + tổng vẫn = 100%) · **A.4** việc cần verify trước khi chốt (đánh mã V1..Vn, trỏ về mã K# của file research) · **A.5** đối chiếu nhanh từng mục của plan (mục nào được ủng hộ, mục nào cần kèm điều kiện).

## 2. Quy trình ghi file (append-only, giữ nguyên nội dung cũ)

```python
# 1) ghi phần mới ra file tạm (write_file), rồi mới append — KHÔNG dùng write_file đè cả file plan
ap = open('.tmp-appendix-A.md', encoding='utf-8').read()
ap = ap.replace('\r\n','\n').replace('\n','\r\n')   # khớp line-ending của file đích
p  = 'docs/05-plan-....md'
t  = open(p, encoding='utf-8').read().rstrip('\r\n')
assert 'Phụ lục A' not in t, 'appendix already present'   # chống append 2 lần
open(p,'w',encoding='utf-8',newline='').write(t + '\r\n\r\n---\r\n\r\n' + ap.rstrip('\r\n') + '\r\n')
```

Verify sau khi ghi (bắt buộc):

```bash
git diff --numstat        # cột thứ 2 (deletions) PHẢI = 0 → chứng minh "chỉ thêm"
git diff --stat           # số insertions khớp số dòng phụ lục
```

Đối chiếu lại vài heading gốc còn nguyên (`## 1.`, `## 10. …`, câu chốt cuối file) trước khi commit.

- Git trên Windows hay báo `warning: LF will be replaced by CRLF` — **vô hại**, bỏ qua nếu numstat deletions = 0.
- File tiếng Việt của user thường **line-ending hỗn hợp từ trước** (`re.findall(r'(?<!\r)\n', head)` > 0 ở phần cũ, = 0 ở phần mình thêm là bình thường). Đừng "chuẩn hoá" cả file — sẽ tạo diff khổng lồ giả.

## 3. Cổng chống bịa citation — chạy TRƯỚC cổng mạng

Trước khi tin (và trước khi trả báo cáo), chạy **offline set-diff** giữa mục vừa viết và file research nguồn:

```bash
python scripts/check_citations_against_source.py docs/05-plan-....md docs/06a-research-....md
```

Nó trích mọi `PMID:<số>` / `DOI:10.…` trong cả 2 file và **exit 1 nếu bản tích hợp chứa citation không có trong nguồn**. Ca thật 18/10/2026: 43/43 PMID + 3/3 DOI khớp — đây là bằng chứng "không bịa" rẻ nhất, chạy trước `verify_pmids.py` (cổng mạng, chậm hơn và chỉ kiểm citation có tồn tại thật, không kiểm nó có thuộc nguồn hay không).

## 4. Nhật ký + commit (báo cáo phải kèm bằng chứng thật)

- Thêm 1 entry ngắn vào CUỐI `02-conversation-log.md`: ngày + việc + nội dung 5 mục + số bytes file research. Ghi kèm "còn mở sau bước này".
- `git add` cả file mới untracked của research, rồi commit message tiếng Việt CÓ DẤU: `docs: tích hợp bằng chứng <mã> vào plan <số> (phụ lục <X>)`.
- **KHÔNG push** trừ khi user yêu cầu.
- Báo cáo cuối phải có: `git log --oneline -1`, `git show --stat HEAD`, và **trích 15–25 dòng đầu** của mục vừa thêm. Nếu bước nào fail → nói rõ fail ở đâu, **không được báo "xong" khi chưa có commit**.

## 5. Bank — nội dung đã tích hợp cho fixgby (18/10/2026)

Nguồn: `docs/06a-research-do-trung-khop-co-quan.md` (78.276 bytes, 62/62 citation khớp PMID↔DOI↔title). Đích: `docs/05-plan-do-trung-khop-co-quan.md` → **Phụ lục A**, 148 dòng thêm, commit `f17d6d4`.

- **Xếp hạng 06A (định tính):** CAO = GAN, TIM, RUỘT; TRUNG BÌNH = THẬN, MÁU, MÔ MỠ, DA, CƠ XƯƠNG; THẤP/THIẾU = PHỔI, XƯƠNG-KHỚP, TUỴ. ⇒ chỉ **3/10** ⇒ cảnh báo trước rằng cổng "≥4/10 cơ quan ≥55" của plan **có nguy cơ fail** ⇒ chuẩn bị sẵn Kịch bản B.
- **8 luật R1–R8 phải đưa vào công thức CS** (rút từ C10.1–C10.6, C11.1–C11.2 của 06A): gene family/enhancer không chuyển (chỉ 2,86% regulatory element bảo tồn chéo loài, 16,35% Suidae-specific — PMID:42121716); trần T2 cho mô mà **chuột thắng heo** (da, thận, tuỵ — PMID:42801618); CYP phải theo **từng chất nền** (CYP2C9/diclofenac không tương quan — PMID:21447389); **loại readout miễn dịch** khỏi ngoại suy (PMID:39317190, 42218200, 39730996); điều kiện loại phenotype đã chứng minh **ngược chiều** (heo kháng gan nhiễm mỡ, cơ xương + béo phì — PMID:40658709); vi giải phẫu nephron (PMID:35297098); **phân ly tầng ⇒ chặn trần 74** (PMID:40116025 + 42801618); batch effect/ortholog conjecture (preprint không PMID → chỉ dùng làm cảnh báo phương pháp).
- **Đề xuất trọng số:** giữ T1 10%, T4 15%, **T5 30%** (tầng bằng chứng mạnh nhất: gan 171 ngày ở người sống PMID:41076089), T6 5%; **đổi T2 25%→20%, T3 15%→20%**. Ngưỡng 75/55/45 **giữ nguyên số** nhưng ghi rõ `chưa có nguồn (tag H)`.
- **Phát hiện lặp lại được:** tài liệu research dạng này **luôn** thiếu 1 phần số liệu (corCor tuyệt đối nằm ở Figure/Table S3 không trích được qua API) ⇒ luôn để mục "việc cần verify trước khi chốt" thay vì bỏ qua khoảng trống.
