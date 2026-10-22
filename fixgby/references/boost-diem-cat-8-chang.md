# Boost "điểm cắt" còn thiếu cho bản đồ 8 chặng (docs/11-duong-di-benh/)

Quy trình điền các ô (mầm × chặng) còn trống trong bản đồ 'đường đi của bệnh' và ghi ra
file boost riêng, có PMID verify.

## 0. Xác định đúng file nguồn (đừng tin tên file trong đề bài)
Thư mục `D:/Hermes Proj/fixgby/docs/11-duong-di-benh/` — batch chia theo **đường lây**, không
theo chủ đề:
- `batch-a-tieu-chay-vi-khuan.json`
- `batch-b-tieu-chay-virus-ky-sinh.json`
- `batch-c-ho-hap.json`   ← hô hấp (virus + vi khuẩn)

Đề bài đã từng ghi `batch-b-ho-hap.json` — **file này không tồn tại**; file hô hấp thật là
`batch-c-ho-hap.json`. LUÔN `ls` thư mục trước rồi mới đọc. Ghi tên file thật vào trường
`nguon_file` của output.
Ngoài ra còn: `01-schema.md`, `00-master-list.md`, `_build.py`, `_verify.py`, `audit-benh.py`,
`qc-benh.py`, `_verified_abstracts.json` (dùng tham chiếu khi cần).

## 1. Schema (đọc read-only, KHÔNG sửa file nguồn)
File nguồn: `{"batch","nhom","loai","doc_ngay","benh":[...],"yeu_to_anh_huong"}`;
mỗi `benh` có `id, ten, ten_en, nhom_benh, loai_tac_nhan, tuoi_mac, muc_pho_bien, chang,
diem_cat, bat_kha, da_that_bai, chi_dau_do_duoc, muc_bang_chung, tag_H, pmids`.
Mỗi phần tử `diem_cat` dùng: `chang, node, diem, kha_thi, ly_do, da_co_gi, pmid`.
→ Output boost nên **giữ thêm `node`** để tương thích, bên cạnh các trường mở rộng
(`mam, mam_ten, loai, loai_chi_tiet, da_verify`).

8 chặng: `1_xam_nhap, 2_qua_hang_rao, 3_bam_cu_tru, 4_nhan_len, 5_lan_he_thong,
6_tin_hieu_hai, 7_hau_qua, 8_thai_lay`.

## 2. Bước chốt "ô nào còn trống" (làm trước, in ra bảng)
In `id | ten | loai_tac_nhan | số diem_cat` và **danh sách `chang` đã có** cho từng mầm →
ô trống = 8 chặng trừ đi set đã có. Đối chiếu với danh sách ô mà đề bài yêu cầu; lệch số
thì tin vào file, không tin vào đề bài.

## 3. Từ khoá tra Europe PMC theo CHẶNG (đã dùng được)
Ghép `<mầm>` + nhóm từ khoá của chặng:
- **1_xam_nhap** — `vaccination`, `sow`, `colostrum`, `maternal immunity`, `aerosol`,
  `airborne`, `transmission`, `biosecurity`, `infectious dose`
- **3_bam_cu_tru** — `adherence`, `adhesin`, `colonization`, `tonsil`, `niche`,
  `receptor`, `fimbriae`
- **4_nhan_len** — `MIC`, `antimicrobial susceptibility`, `isolates`, `inhibitory`,
  `zinc`, `organic acid`, `plant extract`, `essential oil`, `challenged`
- **5_lan_he_thong** — `septicemia/septicaemia`, `pleuritis`, `pleurisy`, `systemic`,
  `bacteremia`, `spread`
- **6_tin_hieu_hai** — `toxin`, `LPS`, `cytokine`, `inflammasome`, `NLRP3`, `ROS`,
  `tight junction`, `Apx`, `dermonecrotoxin`
- **7_hau_qua** — `lesion`, `meningitis`, `arthritis`, `acute phase protein`,
  `diagnostic`, `pathology`, `slaughter`
- **8_thai_lay** — `shedding`, `transmission`, `persistence`, `carrier`, `prevalence`,
  `density`, `eradication`

### Mẹo cặp (mầm × chặng) dễ "trắng nguồn"
- Chặng 1 và 4 của hầu hết mầm **không có thử nghiệm can thiệp on-farm** → đừng cố ép:
  chặng 1 lấy được từ **tiêm phòng heo nái + hệ vi sinh/cư trú ở heo con**; chặng 4
  thường chỉ có **MIC in-vitro** → `loai="R"`, `kha_thi="thap"`.
- Chặng 8 hay dùng **thí nghiệm lây thiết kế** (carrier → contact) hơn là survey dịch tễ:
  nó cho số liệu can thiệp được, còn survey chỉ cho tỷ lệ.
- Chặng 5 của vi khuẩn hô hấp phần lớn là **viêm màng phổi/đa viêm thanh mạc**, KHÔNG phải
  nhiễm khuẩn huyết thật (trừ *P. multocida* / *S. suis*) → không gán bừa "septicemia".
- Bằng chứng âm cũng là điểm cắt tốt: ví dụ vaccine không hạ được cư trú/lây → ghi vào
  `da_that_bai` rồi nêu "phải cắt ở chỗ khác, không chỉ dựa kháng thể".

## 4. Quy tắc gán nhãn
- `loai`: **A** = đã đo trên heo · **R** = in-vitro/cơ chế (ghi rõ loài trong `loai_chi_tiet`).
  Ưu tiên A; chỉ hạ xuống R khi thật sự không có nguồn heo.
- `kha_thi`: `cao` = can thiệp trên heo có kết quả đo · `trung` = bằng chứng gián tiếp /
  động vật lớn / in-vivo không phải heo · `thap` = chỉ in-vitro/cơ chế.
- Ô không tìm được nguồn: `diem="CHƯA CÓ NGUỒN (tag H)"`, `kha_thi="chua"`, `pmid=[]`, và
  ghi vào `ly_do` **những từ khoá đã thử** + liệt kê ô đó trong `bat_kha`.
- `ly_do` phải nêu được: loài, cỡ mẫu/số liệu, và **hạn chế** (chưa có in-vivo, chưa đo
  tải khuẩn, chưa có can thiệp định lượng…).

## 5. Ghi file — AN TOÀN TRƯỚC, ĐẸP SAU
Ghi `json.dump(..., ensure_ascii=False, indent=1)` **ngay sau khi xong mỗi mầm** (rewrite
toàn bộ list từ biến trong bộ nhớ), không đợi hết 6 mầm — mất context giữa đường vẫn còn
dữ liệu đã ghi. Mỗi lần ghi in ra số ô để tự kiểm tra tiến độ.

## 6. Pass kiểm tra cuối (bắt buộc)
```python
want = {"mhp": ["1_xam_nhap", "3_bam_cu_tru", ...], ...}   # lấy từ bước 2
got  = {}                                                  # gom từ file output
assert {k: sorted(v) == sorted(want[k]) for k, v in got.items()}
assert all(c["pmid"] for c in cells)                       # trừ ô tag H
assert not any(w in blob for w in ["chữa", "trị bệnh"])     # từ cấm
```
Rồi chạy lại verify batch toàn bộ PMID (xem
`pubmed-evidence-research/references/europepmc-batch-pmid-verification.md`).

## 7. Văn phong (bắt buộc)
- Tiếng Việt **có dấu đầy đủ**.
- **CẤM** `chữa` / `trị bệnh` — đây là bản đồ cơ chế + TĂBS, dùng
  `can thiệp / chặn / giảm / hạ mức / ức chế`.

## 8. Báo cáo cuối — trung thực, không tô hồng
Nêu: đường dẫn file · số ô điền được **có PMID** · số ô tag H · số PMID đã verify
(duy nhất + số lượt trích) · **danh sách kết quả ÂM** (không tìm được gì, từ khoá đã thử) ·
và các ô **chỉ có bằng chứng in-vitro** để người đọc biết mức độ tin cậy.
