# Đường đi của BỆNH — 8 chặng, tầng bệnh (docs/11)

Tầng **BỆNH** khác tầng **CHẤT**. Đừng lẫn khoá chặng: tầng chất dùng
`cua_vao · qua_hang_rao · gan_lan_dau · gan_de_di · toi_mo · ra_khoi_te_bao · thai · o_lai`
(xem `references/duong-di-8-chang-phan-tu.md`). Tầng bệnh dùng bộ khoá dưới đây.

## Vị trí và trạng thái

- Thư mục: `D:/Hermes Proj/fixgby/docs/11-duong-di-benh/`
- `00-master-list.md` — danh sách tác nhân gốc (23 bệnh: 14 tiêu chảy + 11 hô hấp). Đọc trước.
- `01-schema.md` — schema bắt buộc. Subagent **không được tự đổi khoá**.
- Đã xong: `batch-a-tieu-chay-vi-khuan` (8), `batch-b-tieu-chay-virus-ky-sinh` (9),
  `batch-c-ho-hap` (11) = **28 tác nhân**.
- Mỗi lô 2 file: `batch-<x>-<slug>.md` (đọc được) + `.json` (đúng schema).

## 8 chặng của BỆNH

```
1_xam_nhap       vào bằng cửa nào (mũi, miệng, khí dung, tinh dịch, kim tiêm)
2_qua_hang_rao   vượt hàng rào đầu tiên (lớp nhầy, lông mao, pH, IgA mẹ, bổ thể)
3_bam_cu_tru     bám thụ thể nào / cư trú tế bào nào
4_nhan_len       nhân lên ở đâu
5_lan_he_thong   lan ra hệ thống (huyết, hạch, lách, não, khớp, bào thai)
6_tin_hieu_hai   phát tín hiệu hại (độc tố, cytokine, apoptosis)
7_hau_qua        hậu quả trên con vật
8_thai_lay       ra ngoài / lây
```

Top-level JSON: `batch · nhom · loai · doc_ngay · benh[] · yeu_to_anh_huong[]`.
Mỗi `benh`: `id · ten · ten_en · nhom_benh · loai_tac_nhan · tuoi_mac · muc_pho_bien ·
chang{8 khoá, mỗi khoá {mo_ta, node[], pmid[]}} · diem_cat[] · bat_kha[] ·
da_that_bai[] · chi_dau_do_duoc[] · muc_bang_chung · tag_H[] · pmids[]`.

`diem_cat` = `{chang, node, diem, kha_thi: cao|trung|thap, ly_do, da_co_gi, pmid[]}`.
`chi_dau_do_duoc` = `{chi_dau, o_chang_nao, lay_o_dau: máu|phân|dịch mũi|mô, pmid[]}`.

## Quy trình đã chạy tốt (batch C, ~20 tool-call)

1. Đọc `00-master-list.md` + `01-schema.md` trước, không đoán schema.
2. Fetch Europe PMC theo **cụm query riêng cho từng tác nhân** (2–3 query/tác nhân,
   `resultType=core&pageSize=6-8&sort=CITED desc`), cache ra `epmc_cache*.json`.
   Query theo `TITLE_ABS:"<bệnh>" AND TITLE_ABS:<cơ chế>` hiệu quả hơn query trần.
3. **Lọc theo abstract, không theo tên bài.** Nhiều hit đúng tên nhưng lạc đề
   (vd query PRV trả về 8 bài transsynaptic tracing trên chuột).
4. Viết dữ liệu thành **module Python** (`_data_virus.py`, `_data_bacteria.py`,
   `_data_env.py`) rồi `_build.py` sinh **cả .md và .json từ một nguồn**. Không viết
   tay 2 file song song — chúng sẽ lệch nhau.
5. `_verify.py` chạy 3 phép kiểm (xem dưới). Sửa về 0 cờ rồi mới nộp.
6. Dọn `epmc_cache*.json`, `_fetch_*.py`, `__pycache__`; giữ `_data_*.py`, `_build.py`,
   `_verify.py`, cache abstract để audit lại offline.

## 3 phép kiểm bắt buộc (đừng rút gọn)

| Phép kiểm | Bắt được lỗi gì |
|---|---|
| `EXT_ID:<pmid>&resultType=core`, so `res[0].pmid == pmid` | PMID bịa / PMID gõ sai |
| Đối chiếu **từng con số** với `abstractText` của chính PMID được trích | số bịa, số lấy từ bài khác, làm tròn sai |
| Cấu trúc: đủ 8 chặng, `tag_H` khớp đúng các ô `chưa có nguồn`, mọi PMID trong `pmids` verify được | chặng bị ẩn, tag H trang trí |

Script: `scripts/verify-benh-batch.py <đường-dẫn.json>` — chạy được cho mọi lô bệnh.

### Regex đếm số đã sửa (quan trọng)

Bản cũ `re.findall(r"\d+(?:[.,]\d+)?")` bắt cả số trong `CD163`, `H1N1`, `IL-8`,
`ApxII` → sinh dương tính giả và phải soi tay. Bản đúng:

```python
NUM = re.compile(r"(?<![A-Za-z0-9])(\d+(?:[.,]\d+)?)(?![A-Za-z0-9])")
```

Chỉ lấy token số **đứng riêng**. Vẫn bỏ token 1 chữ số (khớp quá dễ, không có tín hiệu).
Batch C: 0 cờ trên 53 điểm cắt / 112 PMID sau khi dùng regex này.

## Bài học nội dung (tái dùng cho lô sau)

- **"Đi qua" ≠ "cắt được".** Đếm 2 thứ riêng: số tác nhân có mặt ở chặng, và số điểm cắt
  khả thi cao/trung ở chặng đó. Batch C: chặng 3 có 11/11 tác nhân và 11 điểm cắt nhưng
  chỉ 4 khả thi (36%) vì thứ cần chặn là **phân tử của tế bào chủ** (CD163, axit sialic,
  nectin-1, đầu lông mao). Chặng 8 chỉ 8 điểm cắt nhưng 7 khả thi (87%) — vì đó là
  "heo mang trùng", cắt được bằng quản lý. Chặng 5 tệ nhất: 6 điểm cắt, 1 khả thi (16%).
  → Kết luận dùng chung phải nói theo **mật độ khả thi**, không theo số tác nhân.
- **Cùng một node có thể đòi hai hướng ngược nhau.** Đại thực bào phổi (PAM): PRRSV/PCV2
  cần nó sống để nhân lên; APP ly giải nó bằng ApxI; H. parasuis và S. suis kháng thực bào.
  Vì vậy "tăng hoạt hóa đại thực bào" **không** là điểm cắt dùng chung — đúng cho mầm này,
  sai cho mầm kia. Trước khi gộp node, kiểm xem các mầm cần node đó **sống hay chết**.
- **Nguồn không phải trên heo thì không dùng để đỡ cơ chế trên heo.** H2S: chỉ có nghiên
  cứu chuột lang/người; đã bỏ PMID đó và ghi thẳng "chưa có nghiên cứu trên heo xác định
  ngưỡng" thay vì mượn cơ chế. Nguyên tắc "số không nguồn = không số" áp cả cho **cơ chế**,
  không chỉ cho con số.
- **PCV3 là lô có lỗ thật:** chưa xác định đường vào, tế bào đích, cơ chế tín hiệu hại;
  virus có mặt ở heo hoàn toàn khỏe (59,46% mẫu trong một khảo sát). Đừng lấp bằng suy luận
  từ PCV2 — khác loài, khác bệnh. Ghi `chưa có nguồn` + `tag_H`.
- **Đừng để `tuoi_mac` / metadata chứa số không nguồn.** Verifier chỉ soi `mo_ta` /
  `diem_cat` / `da_that_bai`; số trong metadata sẽ lọt. Hoặc bỏ số, hoặc thêm PMID.

## Pitfalls kỹ thuật

1. `_data_*.py` viết bằng `write_file` dài ~40 KB mỗi file là ổn; đừng nhồi cả 11 tác nhân
   vào một file — dễ vượt giới hạn và khó sửa từng chỗ.
2. Sửa dữ liệu bằng `patch` trên module rồi **chạy lại `_build.py`**; sửa trực tiếp `.json`
   sẽ bị lần build sau ghi đè.
3. `execute_code` + `patch` với chuỗi tiếng Việt: dùng triple-quote, đừng nối `\n` trong
   string literal một dòng — đã gặp SyntaxError vì thừa `\n  '`.
4. Trong lúc làm, subagent khác có thể ghi `batch-a` / `batch-b` vào cùng thư mục. Trước khi
   kết luận "thư mục trống/only me", `ls` lại; và **đọc `batch-a.json` để khớp convention**
   (`batch`, `nhom`, `loai` top-level) thay vì tự đặt.
5. `grep -c "chưa có nguồn"` trên .md đếm cả dòng intro/tag_H note → không dùng để đếm ô
   thiếu nguồn. Đếm bằng JSON.
