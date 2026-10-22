# Lô 1 — CỬA A (hàng rào ruột heo) · giao 20/10/2026

File deliverable: `docs/12-hoat-chat-mo-rong/batch-lo-1-hang-rao-ruot.md` + `.json`
(18 hoạt chất · 17 `in_vivo_heo` · 24 PMID verify 24/24 · 18/18 dòng cắt khớp nguyên văn ·
33 ô `tag_H` · 2 trùng 26 nguyên liệu nhà · generator dict → dump `.json` → render `.md`).

## Danh sách đã chốt (18)

| Nhóm | Hoạt chất | Dòng điểm cắt Cửa A | PMID |
|---|---|---|---|
| acid hữu cơ | formic · fumaric · lactic · propionic | pH/ABC dạ dày (formic → "hàng rào acid dạ dày ở heo đang lớn") | 37760214, 42462087, 40980502, 40075985 |
| butyrate | Ca-butyrate (trong 26) · Na-butyrate bọc · tributyrin | dòng mucin | 34237915, 24304918, 41739762, 42280427, 41265486, 42866580 |
| MCFA | monoglyceride C8–C10 · GML | giảm CPB tự do trong lòng ruột non | 40133511, 42520576, 36425847 |
| khoáng | kẽm (ZnO vi nang liều thấp / kẽm lactate) | dòng mucin | 40718813, 42467834 |
| acid amin | L-threonine · glycyl-glutamine | dòng mucin | 35158594, 40941369 |
| oligosaccharide | MOS · GOS · scFOS (→ IgA sữa mẹ) | dòng mucin · IgA sữa | 42638140, 42284521, 42105244 |
| kháng thể | IgY lòng đỏ trứng | dòng mucin | 42399933, 40740302 |
| men vi sinh | B. subtilis cho nái (trong 26) · A. muciniphila | dòng mucin · sIgA sữa (trục gut–mammary) | 40431582, 41611668 |

## Hai kết luận quan trọng nhất

1. **Điểm nghẽn mapping: 11/18 chất dồn vào ĐÚNG MỘT dòng điểm cắt (lớp nhầy).** Cửa A có 19
   dòng cắt nhưng dòng mucin hút gần hết, vì đó là dòng duy nhất mô tả đúng cái mà nhóm
   butyrate/prebiotic/acid amin làm được. Hệ quả phải nói thẳng trong `.md`: *nhiều hoạt chất
   nhưng cùng một mắt xích* — đề cương thử nghiệm **phải đo mucin trực tiếp** (không chỉ đọc
   chỉ số phụ như tế bào hình đài / chiều cao nhung mao).
2. **Điểm cắt pH/ABC dạ dày là chỗ có bằng chứng heo in-vivo mạnh + định lượng được**, còn
   nhóm 3 dòng cắt "miễn dịch sữa" (IgA/sIgA) chỉ đạt mức **gián tiếp**: scFOS làm tăng **IgG và
   TGF-β1 sữa đầu** (không phải IgA), A. muciniphila chứng minh cơ chế trên **chuột** (nái chỉ là
   quan sát liên quan). Đừng gộp nhóm này thành "đã chặn được điểm cắt miễn dịch".

## Phát hiện âm tính đã loại (giữ trong Phụ lục B của file lô)

- **Acid lauric trần 2%** (256 heo, PMID 42467834): không cải thiện hàng rào — TER *xu hướng giảm*
  (P=0.071), không tăng khối lượng (chỉ ZnO vi nang tăng, P=0.0001 ngày 28). → **không** tính là
  hoạt chất; hạ thành cảnh báo có nguồn trong entry MCFA + ghi vào Phụ lục B, kèm khuyến nghị chỉ
  dùng dạng monoglyceride/vi nang.
- ZnO liều dược lý (hàng nghìn ppm) bị EU cấm từ 2022 → chỉ đề xuất vi nang liều thấp / kẽm
  lactate 600–800 ppm, và ghi rõ trong `rui_ro`.

## Bẫy đã dính trong lô này

- **p-value bị Europe PMC cắt ký hiệu**: `abstractText` trả `"...reduced (p"` — mất cả `<0.05`
  (34237915, 41265486). Hai ô `hieu_qua` đầu tiên trích p-value ⇒ phải viết lại thành "có ý nghĩa
  thống kê theo bài" không kèm số. Xem `pubmed-evidence-research/references/europepmc-rest-quirks.md`.
- **Chuẩn hoá dấu nghìn theo hướng ngược lại**: bài viết `1500 ppm` (không dấu phẩy) trong khi hàm
  chuẩn hoá của mình biến `1500` → `1,500` ⇒ cờ "số không có nguồn" giả. Phải chép **đúng cách
  bài viết** con số, không chuẩn hoá máy móc.
- **Cỡ mẫu viết bằng chữ** (Ninety-six / Seventy-two / Eighteen / Forty / Twenty-four) ⇒ audit số
  phải có map chữ↔số, và ghi chú lại điều này trong `.md` để người sau không tưởng bịa.
- **`nham_diem_cat` khớp MỘT PHẦN phải khai ra**: dòng cắt nói *lớp nhầy* nhưng bài chỉ đo liên kết
  chặt (ZO-1/occludin/claudin), MUC2, tế bào hình đài hay chiều cao nhung mao → giữ nguyên văn dòng
  cắt làm `nham_diem_cat` (để khớp luật 9) và ghi thẳng vào `rui_ro`: *"khớp một phần: điểm cắt nói
  về lớp nhầy, bài chỉ đo X"*. Cấm nâng ngầm từ "tăng tế bào hình đài" thành "dày lớp nhầy".
- **Số nằm trong ô cảnh báo vẫn là số được trích** ⇒ phải thêm PMID nguồn vào `bang_chung` của entry
  đó, nếu không audit sẽ báo trích dẫn mồ côi (đã xảy ra với 42467834 khi nó chỉ nằm trong `rui_ro`).

## Tái dùng được

- `pubmed-evidence-research/scripts/verify_pmid_claims.py` — 1 lệnh verify `hitCount == 1` + audit
  từng token số theo `mo_ta`/`lieu`/`hieu_qua` (`--claims` cho từng trích dẫn, `entries` cho union
  theo entry, `--strict` để fail khi còn số chưa khớp).
- `scripts/check-cut-lines.py` — kiểm `nham_diem_cat` khớp nguyên văn dòng cắt (lô 1: 18/18).
