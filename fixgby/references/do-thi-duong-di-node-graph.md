# Đồ thị đường đi — visualize N chất trên 8 chặng (node graph)

Dựng 19/10/2026: `visual/do-thi-duong-di.html` + `visual/build-do-thi-duong-di.py` + `visual/extract-canh.py`
+ `data/nodes-dict.json` (129 node) + `data/canh.json`. Live: `preview.thefirstonly.com/rxttazm8vmpr`, commit `d6ac49c`.

## Câu hỏi phải trả lời (nguyên văn yêu cầu của Quang)

> "anh có 100 chất hay 1.000 chất… nó sẽ giao nhau như nào, có tín hiệu nào có thể can thiệp…
> chất nào chùng con đường nào, giao nhau ở đâu."

Ba câu, ba tầng trả lời khác nhau — đừng gộp:

| Câu hỏi | Trả lời ở tầng | Không được trả lời bằng |
|---|---|---|
| Chất nào chùng đường | **NODE** (đếm chất/node) | đếm theo chặng |
| Giao nhau ở đâu | **NODE** + vai trò | "cùng chặng 3" |
| Tín hiệu can thiệp | **cặp (chất ức chế node) × (chất đi qua node)** | danh sách chất |

**Luật gốc: giao nhau = trùng node, không phải trùng chặng.** Hai chất cùng chặng 3 mà một đứa qua
CYP2E1, đứa kia qua CYP3A4 thì KHÔNG giao. Đây là câu phải nói ngay đầu trang, nếu không user đọc
ma trận chặng và tưởng đã hiểu.

## Vì sao mô hình chịu được 1.000 chất

Số chất tăng vô hạn; **số điểm chạm sinh học có trần** (enzyme · bơm · thụ thể · cửa thải ≈ vài nghìn).
Ma trận chất × node là **thưa** → thêm 1.000 chất chỉ làm chấm dày lên, bản đồ không phình.
Hệ quả kỹ thuật, phải làm đúng:
- Vẽ **node**, không vẽ đường của từng chất.
- `on.length <= 60` thì vẽ cạnh nối; trên 60 tự tắt cạnh (chỉ còn mật độ). Trang phải nói rõ luật này.
- Trần node mỗi hàng: `CAP = boxW < 520 ? 10 : 60`, phần dư in `+N điểm chạm nữa` (không ẩn im lặng).

## Mô hình dữ liệu — 1 dòng = 1 CẠNH

`data/canh.json`: `[chat, chang_idx, node, vai_tro, trang_thai, pmid, cau_goc]`

- `vai_tro`: `di_qua` · `bi_chuyen_hoa` · `day_ra` · `gan_vao` · `dich` · `thai` · `tao_ra` · `uc_che`
- `trang_thai`: `co` (có tác động) · `khong` (đã tra, không xảy ra) · `chua_tra` (tag H)

**Vai trò lấy theo Ý NGHĨA CỘT, không đoán từ khoá.** Bản đầu dò từ khoá trong câu → `bi_chuyen_hoa`
chỉ được 1 dòng vì đa số ô enzyme chỉ là nhãn rời ("CYP3A4 · CYP2E1"), không có động từ.
Bảng field → vai trò: `(gan_lan_dau,enzyme)→bi_chuyen_hoa`, `(gan_lan_dau,san_pham)→tao_ra`,
`(ra_khoi_te_bao,bom)→day_ra`, `(gan_de_di,bam_protein)→gan_vao`, `(toi_mo,mo_dich|thu_the)→dich`,
`(thai,co_quan)→thai`, `(qua_hang_rao,phan_tu)→di_qua`. Fallback theo `tang` của node trong từ điển.
`uc_che` là **override từ khoá** duy nhất, và phải siết: chỉ tính khi **chính chất đó** là chủ thể
(chính tên chất nằm trong ±30 ký tự quanh chữ "ức chế"), nếu không sẽ bắt sai câu
"chứng minh bằng ức chế itraconazol" / "ức chế P-gp bằng Brij 35" (chất thứ ba, không phải chất đang xét).

**Phân 3 trạng thái ở tầng MỆNH ĐỀ, không ở tầng ô.** Ô kiểu
`"Sữa: CHƯA CÓ NGUỒN (tag H)"` hay `"Phổi: glucose không bay hơi"` nếu phân theo ô thì thành "có tác động" hết.
Tách mệnh đề bằng `; · . \n`, **đổi `:` thành `" - "` (giữ nhãn dính với phần sau, đừng split tại `:`)`**,
rồi trong mệnh đề chứa node: `tag H` → `chua_tra`; `không/chưa/chẳng` đứng **trước** node, hoặc
`không bay hơi|không qua|không thải` đứng **sau** node trong ~45 ký tự → `khong`; còn lại `co`.

## Từ điển node = tài sản chính (không phải code)

`data/nodes-dict.json`: `nodes{ID: {ten, tang, chang_mac_dinh, do_duoc}}` + `alias{CHUỖI BỎ DẤU: ID}`.
129 node phủ 22 chất. Khoá chuẩn = gene symbol HGNC (SLC5A1, ABCB1, CYP3A4); không có gene thì tên
protein viết hoa (ALB, LIPOPROTEIN, THAN, MAT_PHAN).

Luật alias bắt buộc:
1. **Biên từ cho MỌI alias** (không chỉ alias ngắn): `(?<![a-z0-9])key(?![a-z0-9])`. Thiếu → `NAT` khớp
   trong "natri", `PROT` trong "protein", `UGT` trong "…CYP/UGT", `PHOI` trong "phối tử".
2. **Node id làm alias chỉ khi len ≥ 4** (nếu không `PROT` tự khớp "protein").
3. **Bảng loại trừ theo từ ĐỨNG SAU** (chặn từ ghép cùng gốc): `phan → tu|giai|nhom|bo|tich|hoi|ung|loai|phoi`,
   `phoi → tron|hop|lieu|mau`, `sua → chua|doi|sai|la`, `mat → khac|do|thi|di|nhieu`.
4. **Bảng CHẶN TỪ ĐỒNG ÂM** — bỏ dấu làm nhiều từ tiếng Việt đụng nhau, đây là bẫy chết người:

   | node | phải "gạch bỏ" trước khi bỏ dấu | vì |
   |---|---|---|
   | `MAT_PHAN` (phân) | `phần`, `mất`, `mặt` | "phần còn lại", "mất 0,7 %" |
   | `THAN` (thận) | `thần` | "thần kinh" |
   | `PHOI` (phổi) | `phối` | "phối tử", "phối trộn" |
   | `SUA` (sữa) | `sửa` | "sửa" |
   | `DA_MO_HOI` (da) | `dạ`, `đã` **+ bỏ alias `da` trần** | "dạ dày", "đã chứng minh" |

   Cách làm: thay từ sai bằng `~` trên chuỗi **có dấu** rồi mới bỏ dấu.
5. **Mẫu từ khoá phải bỏ dấu trước khi so** — nếu `low = nd(seg)` mà pattern vẫn viết `r"ức chế"` thì
   KHÔNG BAO GIỜ khớp (im lặng, không exception). Lượt này `uc_che` và phủ định đều ra 0 vì lỗi đó.
   Sửa: `PAT_ND = [(role, [nd(p) for p in pats])]`.

## Layout (đã đo, không đoán)

- Hàng = chặng (8 hàng). Cột nhãn chặng **ngoài SVG**, `#labels` 150px + `paddingTop=14px`
  (thiếu 14px này → nhãn trượt dần, đo được lệch 1px/hàng).
- Node **wrap trong hàng** (không cuộn ngang): `if(x + pw > boxW-6 && x>6){line++;x=6}`;
  `rowH = (line+1+off)*LINEH + 16`, `LINEH=48`, `PILLH=40`.
- Bề rộng pill theo chữ: `pw = clamp(80, 210, 20 + 6.7 * max(len(id), 0.78*len(sub)))`.
- Mobile (<520px): `body.narrow` ẩn `#labels`, chèn nhãn chặng **trong** SVG làm dòng tiêu đề, `off=1`.
  Thiếu bước này: 150 + 300 = tràn ngang đúng 130px ở 360px.
- Font: `.nlab 13.5px · .nsub 12.5px · .changlab 12.5px · .pm 12.5px`. Không có gì dưới 12.5.

## Số verification của bản đã publish

Desktop: 180 pill · 147 path · font min **12.50px** · tràn ngang **0** · 29 thẻ điểm giao · 6 ô can thiệp.
Mobile 360 (iframe): 0 phần tử chữ < 12px · tràn ngang **0** · `narrow=1` · 79 pill (cap 10/hàng).
Chồng pill trong cùng dòng: **0** (đo bằng sort theo x rồi so `x[i] < x[i-1]+w`).

## Kết quả nội dung (22 chất, 94 node)

- Chùng đường: `THAN` 16 chất · `MAT_PHAN` 12 · `SUA` 7 · `PHOI` 5 · `UGT` 5 · `SULT` 5 · `ABCB1` 4 · `CYP3A4` 4.
- Ô can thiệp thật: curcumin ức chế **ABCB1** trong khi atorvastatin/paracetamol/VitE-TPGS đi qua ABCB1;
  curcumin ức chế **UGT** (IC50 58 µM); ibuprofen ức chế COX-1 mạnh hơn COX-2.
- 6 ô, **5 đúng / 1 sai** (paracetamol–ABCB1: câu gốc nói ức chế bằng Brij 35). Trang phải ghi rõ
  "cờ ức chế là cờ cần kiểm, đọc câu gốc" + giữ nguyên câu gốc + PMID trong từng thẻ.

## Pitfalls riêng của trang này

1. **SVG sinh ra phải giữ `id="svg"`.** Bản đầu đặt `id="g"` trong khi `render()` gọi
   `getElementById("svg")` → lần vẽ ĐẦU chạy, mọi lần sau trả `null` → TypeError. Trang trông vẫn đẹp
   nhưng chết ngay sau tương tác đầu tiên (chip, tìm kiếm, click node đều gọi `render`).
   **Test bắt buộc: gọi `render()` 2 lần rồi mới kết luận.**
2. **`browser_console` trả 500 thường là exception TRONG TRANG, không phải lỗi transport.** Lượt này
   500 xuất hiện đúng với các lệnh gọi `render()`; sửa `id` xong là hết. Đừng kết luận "tool hỏng" —
   thu nhỏ expression về 1 biểu thức đơn để khoanh vùng.
3. **`drawnList()` ở chế độ gộp phải trả TẤT CẢ chất.** Bản gốc `if(mode==="chon" && !ids.length) return []`
   làm chế độ gộp không vẽ một đường nào (`path=0`) — mất đúng thứ user cần. Kiểm bằng
   `document.querySelectorAll('#svg path').length` phải ≈ 7 × số chất.
4. **Ô tìm ghi "chất hoặc điểm chạm" thì phải tìm được cả node.** Nếu chỉ lọc chip chất là hứa sai;
   và dòng `+N điểm chạm nữa (gõ vào ô tìm)` cũng thành lời hứa rỗng. Lọc node: nếu `q` khớp ≥1 node thì
   `perChang = perChang.map(a => a.filter(n => n.includes(q)))`, ngược lại giữ nguyên (để tìm chất vẫn chạy).
5. **Đừng dùng `browser_navigate` để kiểm trang này.** Snapshot toàn trang ~40k ký tự, mỗi lần điều hướng
   là một lần đốt context. Dùng `browser_console` với `location.href='<url>'` rồi đo bằng DOM.

## Rerun khi batch research về

```bash
python visual/extract-canh.py        # docs/09 + docs/10 -> data/canh.json
python visual/build-do-thi-duong-di.py   # -> visual/do-thi-duong-di.html
```
In ra `chat N | canh M | node dung X / tu dien Y | diem giao Z | o can thiep W` — đối chiếu N với số chất
mong đợi trước khi tin. Lô A (12 nguyên liệu) + lô B (7) chưa về → hiện 15 chất người + 7 nguyên liệu lô C.
