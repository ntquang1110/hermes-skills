# First-Principles 5-Part Format (Quang yêu cầu 2026-08-23)

Dùng khi Quang nói "đi từ ví dụ... first principle" hoặc muốn bài ngắn gọn hơn v3.
Mỗi phần = 1 đoạn, **có nhãn tên phần đầu đoạn**, tổng ≤ 450 từ.

## Cấu trúc 5 phần

1. **Ví dụ:** — mở bằng tình huống đời thường cụ thể, dễ hình dung, gần gũi
2. **Nêu vấn đề:** — từ ví dụ, nêu rõ vấn đề tâm lý con người hay gặp, đào sâu cơ chế bên trong (không dừng ở mệt mỏi bề mặt)
3. **Vấn đề gốc rễ:** — phân tích nguyên nhân gốc rễ, nối với nguồn gốc con người/xã hội/tiến hóa
4. **First principle:** — đi sâu nguyên lý khoa học nền tảng, **kể tên cơ chế cụ thể** (dopamine, cortisol, PFC, amygdala, GABA, norepinephrine, nervus vagus, parasympathetic...), giải thích vì sao nó vận hành như vậy
5. **Giải pháp:** — giải pháp thực tế áp dụng được ngay, gắn thẳng vào cơ chế phần 4, có bước cụ thể

## Quy tắc bắt buộc

- Tiếng Việt CÓ DẤU đầy đủ, không sai chính tả
- **KHÔNG** em dash (—), KHÔNG en dash (–), KHÔNG emoji
- **KHÔNG** ký tự ngoài Latin thuần Việt (Hán, Nhật, Trung, mũi tên →)
- Giọng tự nhiên, không sáo rỗng, khoa học chính xác
- Kết bằng câu chốt sắc, **KHÔNG "tóm lại"**, KHÔNG kết "tương lai tươi sáng"
- Mỗi phần là 1 đoạn riêng (cách dòng)

## Mẫu thực tế — psy_1 "Lo âu và kỹ thuật hạ nhiệt thần kinh" (2026-08-28)

**Ví dụ:**
Mình ngồi trước màn hình báo cáo tài chính nửa đêm, tay run khi chuột trỏ vào nút "Gửi". Tim đập nhanh, hơi ngắn, não liên tục lặp lại kịch bản tồi tệ nhất: sai số, bị phạt, đối tác quay lưng. Mình không đang gặp nguy hiểm thực — chỉ là một file Excel. Nhưng cơ thể phản ứng như thể đang đối mặt con dữ.

**Nêu vấn đề:**
Đây không phải lo lắng thông thường. Lo âu kích hoạt hệ thống báo động sinh tồn, bypass thẳng prefrontal cortex (PFC) — trung tâm lý trí. Amygdala chiếm quyền điều khiển, nhồi nhét cortisol, adrenaline vào máu. PFC bị "tắt máy" tạm thời, không còn cấm hết suy nghĩ bi quan. Kết quả: não chạy vòng lặp dự đoán thảm họa, người ta bị tê liệt quyết định ngay khi cần cold head nhất.

**Vấn đề gốc rễ:**
Từ góc nhìn tiến hóa, lo âu là cơ chế bảo vệ: não tiên tổ quét liên tục mối đe dọa để đàn sống sót. Ngày nay, "con dữ" thay bằng deadline, nợ vay, đánh giá xã hội. Não không phân biệt được nguy hiểm vật lý và đe dọa xã hội — cùng một đường thần kinh, cùng một đợt cortisol. Vấn đề không phải lo âu, mà là não lạm dụng cơ chế sinh tồn cho stress tâm lý.

**First principle:**
Cơ chế "hạ nhiệt thần kinh" thực chất là kích hoạt lại PFC để ức chế amygdala. Khi PFC online trở lại, nó gửi tín hiệu GABA ức chế amygdala, hạ cortisol, cân bằng norepinephrine. Kỹ thuật hít thở 4-7-8, cold exposure (rửa mặt nước lạnh), hoặc grounding 5-4-3-2-1 đều khai thác đường thần kinh ngược: từ cơ thể (xương sống, da, cơ hô hấp) kích hoạt nervus vagus → tăng hoạt động parasympathetic → PFC lấy lại quyền điều khiển. Dopamine và serotonin sau đó ổn định, cho phép tư duy logic quay lại.

**Giải pháp:**
Làm ngay ba việc khi lo âu đánh trúng:
1. Rửa mặt nước lạnh 30 giây hoặc chườm khăn lạnh lên cổ — kích hoạt phản xạ diving, hạ nhịp tim tức thì.
2. Hít 4 giây, nín 7 giây, thở ra 8 giây, lặp 4 chu kỳ — ép buồng ngực kích hoạt vagus, PFC online trở lại.
3. Viết ra ba kịch bản: xấu nhất, tốt nhất, thực tế nhất — PFC ép amygdala đối mặt dữ liệu thay vì tưởng tượng.
Đơn giản, không thuốc, hiệu quả trong 2-3 phút.

## Chuyển thể sang Threads (giọng mình/anh, 3 post)

- POST 1: Ví dụ + Nêu vấn đề (gộp, ~360 ký tự)
- POST 2: Vấn đề gốc rễ + First principle (gộp, ~498 ký tự)  
- POST 3: Giải pháp (đánh số 1./2./3., ~393 ký tự)
- Mỗi post ≤ 500 ký tự, tách bằng 1 dòng trống
- Xưng hô: người kể = "mình", người đọc = "anh"
- Verify trước khi gửi: python count chars, count diacritics ≥20, scan em dash/emoji/CJK = 0

## Verify script (chạy qua terminal, KHÔNG execute_code trong cron)

Script tái dùng: `scripts/verify_thread_draft.py <path>` — in từng post chars + dấu VN + scan em-dash/en-dash/arrow/CJK/emoji + check ngôi mình/anh (chặn "tôi"/"bạn"); exit 0 PASS / 1 FAIL. Nhận CẢ file KFlow 5-part lẫn file thread (tự nhận nhãn `**Ví dụ**` và bỏ qua floor dấu VN cho bản KFlow nhưng vẫn scan ký tự lạ). Viết qua write_file rồi run `python` — đừng gõ `python -c` inline dài dòng escape, và KHÔNG xài `execute_code` trong cron (bị `BLOCKED: approvals.cron_mode`).

Inline tương đương (nếu chưa copy script):
```bash
python -c "
text = open('D:/Hermes Proj/psy/threads_drafts/psy_N_thread.txt', encoding='utf-8').read()
posts = [p for p in text.split('\n\n') if p.strip()]
for i, p in enumerate(posts, 1):
    print(f'Post {i}: {len(p)} chars')
diacritics = 'àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ'
print(f'Diacritics: {sum(1 for c in text if c in diacritics)}')
print(f'Em dash: {\"—\" in text}')
print(f'En dash: {\"–\" in text}')
print(f'Uses mình: {\"mình\" in text}')
print(f'Uses anh: {\"anh\" in text}')
"
```

**⚠️ SCRUB CẢ BẢN KFLOW (`psy_N.txt`) chứ không chỉ bản thread (gặp psy_2 2026-08-28, psy_1 2026-08-31):** bản 5 đoạn nguồn KFlow viết xong cũng dính em dash + mũi tên (`—`/`→`) từ câu nối kiểu "Tự thưởng ... biến phần thưởng thành điều kiện tất yếu → dopamine sụt". Trước khi lưu phải thay hết `—` thành dấu phẩy/dấu chấm và `→` thành dấu phẩy, rồi verify LẠI cả `psy_N.txt` lẫn `psy_N_thread.txt` (0 em dash, 0 arrow, dấu VN đủ). psy_2 ban đầu có 8 em dash + 3 arrow; psy_1 (2026-08-31) ban đầu cũng có `—` và `→` trong phần First principle (mesolimbic `VTA → nucleus accumbens → PFC`). Chạy 1 lệnh python `content.replace('\\u2014', ', ').replace('\\u2013', ', ').replace('\\u2192', ', ')` cho CẢ FILE rồi đọc lại bằng python (read_file báo "Binary file" false positive cho UTF-8 có `—`). Sau scrub verify lại BOTH: word-count ≤450 (cắt thêm nếu vượt) VÀ charset sạch (0 em/en dash, 0 arrow, 0 CJK). Luôn chạy qua `terminal` — `execute_code` bị chặn trong cron mode.

**⚠️ PITFALL — Blank line = post separator; đếm nhầm số post (gặp psy_1 2026-08-31):** khi chuyển thể sang thread, yêu cầu "tách bằng dòng trống" + "2-3 post". MỌI blank line bên trong = 1 post rời. Bản thread psy_1 ban đầu viết 1 block lớn không blank line → poster không split được; sau đó gom lại thành 1 post duy nhất >1300 ký tự. Quy tắc: (1) Gom content thành ĐÚNG N block (2-3) KHÔNG blank line trong từng post; (2) Sau khi viết, chạy python `[p for p in text.split('\\n\\n') if p.strip()]` đếm block, phải = đúng số post task yêu cầu, mỗi ≤500; (3) Lệch sai số → merge bằng write_file lại (không patch tay từng chỗ). Block 300-450 là vừa, post "main" (hook + nhân vật) hợp nhất với phần "cơ chế" một dòng liền.

**⚠️ PITFALL — Post cuối (giải pháp + chốt) hay >500, phải trim lặp 2-3 lượt (gặp psy_1 2026-08-31):** post 3 (giải pháp + câu chốt gộp) thường vượt 500. Đừng patch tay từng câu — dùng write_file viết lại cả block, cắt: bỏ phụ từ lặp ("cũng"), gộp ý mệnh đề, rút danh từ dài. Sau mỗi lần trim chạy lại verify cho ra con số chính xác. Cũng đảm bảo đếm ĐÚNG số post: nếu để dòng chốt cách dòng trống riêng thì thành 1 post thừa, phải gộp chốt vào block cuối để thành 2-3 post đúng như yêu cầu.

**⚠️ PITFALL — CJK lọt là từ thay thế ngữ nghĩa, không chỉ rác (gặp psy_3 2026-08-30, psy_1 2026-08-31):** model local không chỉ để lọt cụm CJK thừa, mà còn chèn CJK VÀO ĐÚNG CHỖ của từ Việt khi không nhớ ra chữ (vd "không thưởng cho sự so sánh" — 奖励 = thưởng; "tự chiếu" → 自参照). Rà CW: nếu từ Việt gần CJK xuất hiện cùng, thay bằng từ Việt đúng nghĩa. RIÊNG lớp rác thứ hai: Latin-extended không thuộc tiếng Việt (`ż` trong "gặm rżen", `ð` trong "cðn thêm béo") — những ký tự này category `Ll` nên regex CJK `[\u4e00-\u9fff...]` KHÔNG bắt. Muốn chặn cả 2 lớp: quét cả CJK LẪN scan mọi char có category `Ll`/`Lo`/`M` không nằm trong tập dấu VN chuẩn và không ascii.

## Bổ sung verify — psy_4 "Quản lý cảm xúc và điều tiết phản ứng khi bùng nổ" (2026-10-13)

Bản này là variant **nhãn TÊN IN ĐẬM** (`**Ví dụ**`, `**Nêu vấn đề**`, `**Vấn đề gốc rễ**`, `**First principle**`, `**Giải pháp**`), chủ đề đọc từ dòng `4.` của `topics_today.txt`.

**(a) 🔴 Công thức đếm dấu tiếng Việt — `unicodedata.combining()` NỔ `TypeError`.**
`unicodedata.normalize("NFD", "ắ")` trả về CHUỖI 2 ký tự, nên `unicodedata.combining(normalize(...))` báo
`TypeError: combining() argument must be a unicode character, not str`. Công thức chạy được:
```python
dia = sum(1 for c in s if len(unicodedata.normalize("NFD", c)) > 1 or c in "ăâđêôơưĂÂĐÊÔƠƯ")
```
(`đ`/`Đ` không tách được qua NFD nên phải liệt kê tay.) psy_4: thread 237 dấu, `bad=[]` cả 2 file.

**(b) Nhãn phần có 3 kiểu — checker phải nhận cả 3.** `**Tên**` (psy_4 2026-10-13), `Tên` trần (psy_2 2026-10-13), `N. Tên` (lô cũ). Script đếm theo regex `^[1-5]\.` sẽ ra `labels=0` cho 2 kiểu đầu → FAIL GIẢ. Verdict thật chỉ dựa `words<=450` + `forbidden=none` + `diacritics>=20`. TUYỆT ĐỐI không thêm số vào nhãn chỉ để chiều script.

**(c) Script check ad-hoc phải ghi vào `%TEMP%` prefix `hermes-verify-` ngay từ lần đầu.** psy_4 lỡ ghi `D:/Hermes Proj/psy/_verify_tmp.py` trong project dir rồi xoá → bị runtime flag "changed path without evidence". Đường đúng:
`C:/Users/NTQUANG_DELL/AppData/Local/Temp/hermes-verify-psyN.py` → `python "<file>"` → `rm -f` (và dọn luôn file lỡ tạo trong project) → xác nhận `ls` không còn. Runtime ghi nhận là bằng chứng hợp lệ: `verification_evidence: {status: passed, kind: ad_hoc, scope: targeted}`.

**(d) 🔴 TÁI PHẠM LẦN 3 — viết thread thành 7 đoạn rồi mới gộp 3 block.** Bản `write_file` đầu lại tách mỗi ý một đoạn cách dòng trống, tốn thêm 1 vòng. Luật: lần `write_file` ĐẦU TIÊN phải ra ĐÚNG 3 block, mỗi block MỘT đoạn liền, không blank line bên trong; verify `text.split("\n\n")` == 3 ngay sau đó. Số đo bản đúng psy_4: 349 / 398 / 332 = 1083 ký tự, dư chỗ rất nhiều so với trần 500/post và 1300 tổng — không cần nhồi, chỉ cần không xé đoạn.

**(e) Đụng lại file CÙNG TÊN cũ trong `threads_approved/` → phải NÊU cho Quang kèm đề xuất.** psy_4 gặp `threads_approved/psy_4_thread.txt` từ 28/08 mang chủ đề khác hẳn. `os.path.exists` cho FAIL giả; chỉ so NỘI DUNG mới đúng. Vì poster pick theo TÊN file, bản cũ cùng tên có nguy cơ bị đăng nhầm khi Quang gõ "duyệt thread psy_N_thread" → phải báo rõ trong phần trả bài và đề xuất đổi tên bản cũ thành `psy_N_thread_YYYYMMDD.txt`. (`psy_threads_pick.py` có key theo tên file hay không vẫn CHƯA kiểm chứng — đọc script trước khi khẳng định.)

**(f) Viết có ý thức tránh dash/CJK từ đầu thì bỏ được cả lượt scrub.** psy_4 ra `bad=[]` ngay bản đầu (0 em/en dash, 0 CJK, 0 arrow) — không phải `.replace('\u2014', ', ')` như các lần trước, tiết kiệm 1-2 vòng write_file + verify.

## Bổ sung verify — psy_4 (2026-10-14 chiều, "Sự ảnh hưởng và đòn bẩy tâm lý")

**(a) 🔴 TÁI PHẠM LẦN 3 — tự viết checker vào Temp thay vì gọi script skill, dính 2 VÒNG FAIL GIẢ vì SAI DẢI KÝ TỰ "non-Vietnamese".**
Đây đúng cái pitfall SKILL.md đã cấm (`⛔ ĐỪNG tự viết checker vào %TEMP% nữa`), vẫn bị lặp. Hai vòng sai liên tiếp:
1. Vòng 1 chỉ nhận ASCII + `U+1EA0–U+1EF9` + vài chữ precomposed → **mọi nguyên âm dấu kiểu Latin-1 (`à á ã é ì í ò ó ù ú ý`) bị liệt là rác**, bài sạch vẫn FAIL.
2. Vòng 2 thêm `U+00C0–U+00FF` + `U+0100–U+017F` → **`ơ` (U+01A1) và `ư` (U+01B0) lại bị liệt là rác** vì nằm ở Latin Extended-B, ngoài cả 2 dải vừa thêm.

Dải ĐÚNG (dùng khi buộc phải tự viết):
```python
def hop_le_tieng_viet(c):
    o = ord(c)
    return (c.isascii() or 0x00C0 <= o <= 0x00FF      # Latin-1 Supplement: à á ã é ì í ò ó ù ú ý
            or 0x0100 <= o <= 0x017F                  # Latin Extended-A:  ă â đ ê ô
            or 0x0180 <= o <= 0x024F                  # Latin Extended-B:  ơ U+01A1, ư U+01B0
            or 0x1EA0 <= o <= 0x1EF9)                 # Latin Extended Additional: ạ ả ấ ầ ậ ệ ộ ớ ở ợ ụ ủ ứ ừ ữ ự
```
Rác thật chỉ là: CJK/Hangul/Kana, fullwidth `U+FF00–U+FFEF`, emoji (`ord(c) > 0x2600`), `U+2013 U+2014 U+2022 U+2190–U+21FF`. Thứ tự đúng: (1) gọi `python "<skill_dir>/scripts/verify_psy_plainname.py" "<draft>" "<thread>"`, đọc `RESULT PASS|FAIL`; (2) chỉ tự viết khi script thiếu, khi đó ghi vào `C:/Users/NTQUANG_DELL/AppData/Local/Temp/hermes-verify-psyN.py` rồi `rm -f`, báo cáo là ad-hoc verification. Lần này agent còn lưu checker vào project dir (`D:/Hermes Proj/psy/_verify_psy4.py`) rồi mới dọn — sai chuẩn, dính cờ "changed path without evidence"; lần tới để trong Temp ngay từ đầu.

**(b) 🔴 NHÃN PHẦN 4 — task ghi `First principle` thì dùng ĐÚNG chữ đó, đừng Việt hoá âm thầm.** psy_4 chọn `4. Nguyên lý nền tảng` để né luật "chỉ dùng chữ Latin thuần tiếng Việt". Về gate charset thì PASS (không lẫn ký tự lạ) nhưng LỆCH mẫu đã duyệt và lệch tên phần task liệt kê. Chốt: `First principle` là nhãn tiếng Anh DUY NHẤT được phép vì task ghi đúng chữ đó (đã quyết 2026-10-13). Nếu đã Việt hoá thì phải NÊU RÕ trong phần trả bài để Quang chọn, không đổi âm thầm.

**(c) Nhãn `1. Tên` / `Tên` trần / `**Tên**` — psy_4 dùng kiểu ĐÁNH SỐ + tên Việt** (`1. Ví dụ` … `5. Giải pháp`). Cả 3 kiểu đều pass; đừng thêm/bớt số chỉ để chiều script.

**(d) Ngân sách từ xác nhận lần nữa.** Bản đầu 472 từ (>450, tính cả 5 nhãn) → 1 lượt `write_file` cắt gộp còn **445 từ**, PASS ngay, không vá từng câu. Nhắm 420-440 ngay bản đầu; khi lệch <10 từ thì viết lại cả file rẻ hơn patch nhiều lượt.

**(e) Thread viết 1 lượt, ra đúng 3 post.** 372 / 301 / 427 ký tự (tổng 1105 ≤ 1300), dấu tiếng Việt 57 / 53 / 73 (≥20). Cách làm ăn được: TRONG mỗi post xuống dòng bằng MỘT `\n` (dòng đơn), GIỮA các post để dòng trống `\n\n` → `text.split("\n\n")` ra đúng 3 block mà mỗi post vẫn nhiều đoạn dễ đọc. Không cần `\n\n\n`.

**(f) Verify xong thì DỌN file check tạm và nói rõ verdict.** Báo cáo gọn: số từ, số nhãn, ký tự mỗi post, tổng, số dấu, 0 forbidden — kèm 1 câu nói rõ đây là script ad-hoc (không phải test suite) và file tạm đã xoá.

## Bổ sung verify — psy_4 (2026-10-15, "Thoát khỏi vòng lặp trì trệ")

**(a) 🔴 PITFALL MỚI — bản thread có thể THIẾU HẲN đại từ người kể "mình".**
Viết thread theo lối nói thẳng vào người đọc ("Không phải anh lười. Là não anh đang né.") dễ ra bản có "anh" mà KHÔNG có một chữ "mình" nào. Cổng verify ngôi FAIL (`FAIL thread has 'minh' narrator`) trong khi 22 check còn lại PASS — vì check ngôi chỉ đếm "tôi"/"bạn" = 0 thì không phát hiện được. Template chốt người kể = "mình", người đọc = "anh", nên thiếu "mình" là lỗi THẬT, không phải FAIL giả.
Sửa rẻ nhất, ĐỪNG `write_file` lại cả file: `patch mode=replace` chèn "của mình"/"mình" vào một câu đã có sẵn. psy_4: "Cơ chế cũ, môi trường mới, thành cái bẫy." → "…thành cái bẫy của mình." (+8 ký tự, post 2 từ 426 lên 435, vẫn ≤500, câu chốt còn nguyên). Chọn mệnh đề sở hữu/nhận định để không phá nhịp.
Kiểm: `grep -oE '\bmình\b' <file> | wc -l` ≥ 1 VÀ `\banh\b` ≥ 1. Đừng chỉ xác nhận "tôi"/"bạn" = 0 rồi tưởng đạt.

**(b) 🔴 PITFALL MỚI — dọn rác verify: CHỈ xoá file do CHÍNH LƯỢT NÀY tạo.**
Sau khi chạy script tạm, `ls | grep -i verify` vẫn thấy `_verify_psy4.py` (14/10) trong `D:/Hermes Proj/psy/` và `hermes-verify-benbi.py` trong `%TEMP%` — rác của các JOB KHÁC, không phải lượt này. Đừng `rm -f *_verify*` theo tên khớp mờ: đối chiếu mtime, chỉ xoá đúng file mình vừa tạo, và nói rõ file còn lại thuộc job nào để Quang không tưởng còn sót lỗi của mình. Cùng luật với check `threads_approved/` ở mục (e) dưới: xác minh bằng mtime/nội dung, KHÔNG bằng `exists`.

**(c) TÁI PHẠM LẦN 4 — blank line trong post làm split ra 8 block.**
Bản `write_file` đầu vẫn tách mỗi đoạn trong cùng một post bằng dòng trống → `text.split("\n\n")` ra **8 block** thay vì 3. Sửa bằng 1 lượt `write_file` lại: TRONG mỗi post xuống dòng bằng MỘT `\n`, GIỮA các post để `\n\n`. Ra đúng 3 post **416 / 435 / 468 = 1319 ký tự**. Luật cũ vẫn đúng và vẫn bị vi phạm liên tục: viết ĐÚNG N block ngay từ lần `write_file` đầu, verify `text.split("\n\n")` ngay sau đó.

**(d) Check "KHÔNG ghi vào `threads_approved/`" phải so MTIME, không so `exists`.**
`threads_approved/psy_4_thread.txt` có từ **28/08** (chủ đề khác) → check `not os.path.exists(...)` báo FAIL GIẢ, dễ tưởng mình lỡ tay rồi đi xoá nhầm bài đã duyệt thật. Verdict đúng: `getmtime(approved) < getmtime(draft)` là đạt (file cũ, không phải do lượt này tạo). Vẫn phải NÊU cho Quang file trùng tên trong `threads_approved/`.

**(e) Chạy đúng trình tự 2-deliverable, không dừng sau bước 1.**
Task yêu cầu 3 việc theo thứ tự: (1) `write_file` bài 5 đoạn → `drafts/psy_N.txt`; (2) chuyển thể thread → `threads_drafts/psy_N_thread.txt`; (3) TRẢ VỀ CHAT **cả 2 bản** kèm 2 dòng nhắc duyệt. Không dừng sau (1). Word-count lần này về ngay **409 từ** ở bản đầu (nhãn 5 phần tên trần: `Ví dụ / Nêu vấn đề / Vấn đề gốc rễ / First principle / Giải pháp`), thread 0 em/en dash + 0 CJK ngay bản đầu — nhắm 400-430 từ và tránh dash từ lúc viết thì bỏ được cả lượt scrub.

## Bổ sung verify — psy_1 (2026-10-16, "Quản lý năng lượng thay vì quản lý thời gian")

**(a) 🔴 TÁI PHẠM LẦN 5 — blank line trong post → split ra 9 block.** Nguyên nhân LẦN NÀY là mới và đáng nhớ: agent BẮT CHƯỚC CÁCH NGẮT DÒNG của `threads_template_v2.txt` (mẫu cũ để blank line giữa các đoạn trong cùng một post), rồi viết 9 đoạn cách dòng trống → `text.split("\n\n")` = 9 post, phải `write_file` lại toàn bộ.
LUẬT: mẫu chỉ dùng để học GIỌNG + NHỊP CÂU, KHÔNG copy cách ngắt dòng. TRONG mỗi post xuống dòng bằng một `\n`; GIỮA các post mới dùng `\n\n`. Verify `len([p for p in text.split("\n\n") if p.strip()])` NGAY sau lần `write_file` ĐẦU TIÊN, trước khi làm bất cứ việc gì khác.

**(b) 🔴 TÁI PHẠM — tự chế checker dù script có sẵn.** Lượt này tạo `D:/Hermes Proj/psy/scripts/verify_psy1.py` trong khi `scripts/verify_psy_plainname.py` đã có sẵn ĐÚNG cho variant nhãn tên trần (nhận cả nhãn tên trần lẫn đánh số, in `RESULT PASS|FAIL`). Hệ quả: 2 vòng verify thừa, bị runtime flag "changed path without evidence" 2 lần, để lại file rác trong `psy/scripts/`.
LUẬT: variant nhãn tên trần → gọi NGAY `python "<skill_dir>/scripts/verify_psy_plainname.py" "<draft>" "<thread>"`. CẤM tạo file `.py` mới trong `D:/Hermes Proj/psy/scripts/` hoặc `%TEMP%`.

**(c) ⚠️ `$TEMP` trong git-bash = `D:\tmp`, KHÔNG phải Windows temp.** `python "$TEMP/hermes-verify-psy1-final.py"` → `can't open file 'D:\\tmp\\hermes-verify-psy1-final.py'` (exit 2) dù file đã ghi thành công vào `C:/Users/NTQUANG_DELL/AppData/Local/Temp/`. Nếu buộc có script tạm: ghi ĐƯỜNG DẪN TUYỆT ĐỐI `C:/Users/NTQUANG_DELL/AppData/Local/Temp/hermes-verify-<slot>.py`, gọi y nguyên path đó (đừng dùng `$TEMP`/`/tmp`), và cho script tự `os.remove(__file__)` ở cuối để tự dọn — lượt này làm vậy và runtime ghi nhận `verification_evidence: passed / ad_hoc`.

**(d) ⚠️ CẢNH BÁO `write_file` "modified by sibling subagent ... never read it" (gặp trên `threads_drafts/psy_1_thread.txt`).** Tên file thread CỐ ĐỊNH nên nhiều instance cron (slot khác giờ, hoặc chạy chồng) ghi đè cùng file. Khi thấy cảnh báo: `read_file` lại xác nhận nội dung trên disk đúng là bản của mình, NÊU cho Quang biết, và đề xuất đổi tên thread có ngày `psy_<N>_thread_YYYYMMDD.txt` để hết tranh chấp (chưa chốt với Quang).

**(e) Ngân sách từ xác nhận lần nữa:** 472 → 461 → 447 qua 3 lượt `write_file`. Nhắm 420-435 ngay bản đầu; 5 nhãn tên trần chiếm ~12 token, chỗ phình luôn là Ví dụ mở đầu + Giải pháp.
Bản đúng lượt này: article **447 từ**; thread **280 / 372 / 370 = 1027 ký tự**, dấu tiếng Việt 51 / 78 / 75; 0 em/en dash, 0 arrow, 0 CJK/emoji ngay bản đầu.

## Bổ sung verify — psy_2 (2026-10-17, "Kiểm soát xung động và chiến thắng cám dỗ")

**(a) 🔴 TÁI PHẠM LẦN 6 — tự viết checker vào `%TEMP%` dù script có sẵn.** Viết `C:/Users/NTQUANG_DELL/AppData/Local/Temp/_chk_psy2.py` (không có prefix `hermes-verify-`, không tự dọn) để đếm từ / đếm dấu / quét charset / đếm nhãn — cả 4 việc `scripts/verify_psy_plainname.py` đã làm sẵn. Tốn 3 lượt tool (write + 2 lần chạy lại sau mỗi lần sửa bài) và không có log `verification_evidence` hợp lệ.
LUẬT (nhắc lại lần thứ 6, đọc trước khi viết bất cứ file `.py` nào):
```
python "<skill_dir>/scripts/verify_psy_plainname.py" "D:/Hermes Proj/psy/drafts/psy_<N>.txt" "D:/Hermes Proj/psy/threads_drafts/psy_<N>_thread.txt"
```
Gọi NGAY sau khi viết xong bản 5 phần (chưa cần thread) — truyền đường dẫn draft 2 lần, đọc dòng `ARTICLE`. Viết file check tay CHỈ khi script báo FAIL mà bạn nghi output sai.

**(b) 🔴 BẢN 5 PHẦN VƯỢT TRẦN 450 NẶNG NGAY BẢN ĐẦU khi viết tự do — 523 từ.** Đường trim thật: 523 → 473 (write_file cắt gộp) → 449 (1 patch xoá đúng 1 mệnh đề). Nguyên nhân: phần Ví dụ kể 8 câu, mỗi phần không có nhãn số nên không tự "thấy" mình dài tới đâu. Ngân sách phần cho variant nhãn tên trần (nhắm ngay bản đầu): Ví dụ ≤80 · Nêu vấn đề ≤75 · Vấn đề gốc rễ ≤80 · First principle ≤105 · Giải pháp ≤95 · 5 nhãn ≈11 từ → tổng ≈440.
Quy tắc cắt ở dải 450-460: cần bỏ ĐÚNG 1 mệnh đề → `patch mode=replace` một cặp old/new (mắt thấy new ngắn hơn) rồi verify 1 lần, rẻ hơn `write_file` cả file; cần bỏ ≥2 chỗ → `write_file` viết lại toàn bộ.

**(c) Tên file: theo ĐÚNG chuỗi cron prompt ghi.** Slot này ghi `drafts/psy_2.txt` (không ngày), khác quy ước dated-slug trong SKILL.md. Prompt thắng — ghi đúng path prompt yêu cầu, đừng "sửa" sang quy ước khác. Bản thread vẫn luôn là tên CỐ ĐỊNH `threads_drafts/psy_<N>_thread.txt` (đúng như prompt cũng ghi).

**(d) Thread viết 1 lượt, ra đúng 3 post ngay bản đầu.** 362 / 341 / 407 = 1110 ký tự (≤1300), dấu tiếng Việt 73 / 63 / 88 (≥20). Cách ăn được: TRONG mỗi post xuống dòng bằng MỘT `\n`, GIỮA các post `\n\n`; verify bằng `split("\n\n")` ngay sau `write_file`. Chưa lần nào phải viết lại vì blank line khi làm đúng ngay từ đầu.

**(e) Cảnh báo `write_file` "modified by sibling subagent … never read it" xuất hiện lại trên `threads_drafts/psy_2_thread.txt`** — bản của mình ĐÃ ghi đè thành công (`verified: true`, byte count khớp). Đúng luật (d) ở mục 2026-10-16: sau cảnh báo phải nêu cho Quang biết file trùng tên giữa `threads_drafts/` và `threads_approved/` (thư mục duyệt vẫn còn `psy_2_thread.txt` từ 16/10, chủ đề khác) để anh không lẫn bản cũ. Không xoá file trong `threads_approved/`.

## Bổ sung verify — psy_3 (2026-10-17, "Động lực nội tại và sự tự thưởng")

**(a) 🔴 TÁI PHẠM LẦN 7 — tự chế checker, lần này ghi cả vào THƯ MỤC DỰ ÁN.**
Lượt này viết `D:/Hermes Proj/psy/scripts/_check_psy3.py` (trong `psy/scripts/` là script THẬT của pipeline) rồi xoá, và thêm 2 file `%TEMP%`: `hermes-verify-psy3.py`, `hermes-verify-psy3b.py`. Tổng 3 `write_file` + 3 `terminal` đều thừa, dính cờ "changed path without evidence". Checker thứ hai phải viết lại chỉ vì checker đầu tự đặt điều kiện SAI (xem (c)).
LUẬT: chạy `python "<skill_dir>/scripts/verify_psy_plainname.py" "<draft>" "<thread>"` TRƯỚC. CẤM ghi bất kỳ file `.py` nào vào `D:/Hermes Proj/psy/scripts/`, kể cả tên có tiền tố `_`.

**(b) ✅ `patch mode=patch` CHẠY ĐƯỢC trên file bài tiếng Việt — NGOẠI LỆ so với ghi chú 2026-09-30 trong SKILL.md.**
Cắt bản 450 từ → 438 từ bằng **1 lần `patch mode=patch` với 4 hunk** trên `drafts/psy_3.txt` vừa `write_file`, không lỗi "Binary file", không cần `write_file` lại. Điều kiện ăn được: mỗi hunk có ≥1 dòng context ASCII-pure làm mốc (`**Ví dụ**`, `**Giải pháp**`), không phải vùng toàn chữ có dấu.
Kết luận đúng: `mode=patch` không "hỏng vì tiếng Việt", nó hỏng khi vùng context thiếu mốc. Dùng nó khi cắt 1-2 mệnh đề (rẻ hơn `write_file`); vẫn chọn `write_file` khi phải cắt ≥2 chỗ lệch nhiều.

**(c) 🔴 TÁI PHẠM — check `threads_approved/` bằng `os.path.exists` lại ra FAIL GIẢ.**
`threads_approved/psy_3_thread.txt` tồn tại từ **28/08** (đã có trong `threads_posted.json`) → `exists()` báo FAIL. Công thức đúng, dán thẳng:
```python
import os, time
p = r"D:/Hermes Proj/psy/threads_approved/psy_<N>_thread.txt"
if os.path.exists(p):
    age_h = (time.time() - os.path.getmtime(p)) / 3600
    # age_h > 1  -> file chu kỳ CŨ, không phải lượt này ghi vào => PASS
    # age_h <= 1 -> vừa bị ghi trong lượt này               => LỖI THẬT
```
File trùng tên ở `threads_approved/` là BÌNH THƯỜNG; soi mtime/nội dung, KHÔNG xoá, và vẫn phải NÊU cho Quang để anh không lẫn bản cũ khi gõ "duyệt thread psy_N_thread".

**(d) Ngân sách từ: bản đầu chạm ĐÚNG trần (450 từ) nên vẫn phải cắt 1 lượt.**
Variant nhãn bold `**Ví dụ**` … `**Giải pháp**` (slot này dùng kiểu này; `verify_psy_plainname.py` nhận cả nhãn trần, bold, lẫn đánh số nên không có cớ tự viết regex đếm nhãn). Nhắm **420-435 từ ngay bản đầu**; 5 nhãn bold ≈ 10 token. Bản đúng lượt này: article **438 từ**.

**(e) Thread ra đúng 3 post ngay bản đầu:** 303 / 349 / 339 = **991 ký tự** (≤1300), dấu tiếng Việt **217**, 0 em/en dash, 0 arrow, 0 CJK/emoji. Cách ăn được vẫn là: TRONG mỗi post xuống dòng bằng MỘT `\n`, GIỮA các post `\n\n`; verify `split("\n\n")` == 3 ngay sau `write_file`.