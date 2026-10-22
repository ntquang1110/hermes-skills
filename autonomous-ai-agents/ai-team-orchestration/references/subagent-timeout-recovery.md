# Subagent Timeout Recovery (delegated research/build)

Phân loại trước khi kết luận "mất kết quả" hay "chạy lại".

## Hai pha chết khác nhau, cách xử khác nhau

| Pha chết | Triệu chứng trong live transcript | Dữ liệu còn? | Cách xử |
|---|---|---|---|
| **Pha RESEARCH** | log dừng ở giữa chuỗi `esearch`/`curl`/`terminal`, chưa có script build | Một phần (JSONL/JSON từng query) | Đọc file trung gian đã ghi, tự tổng hợp — xem pitfall SALVAGE trong SKILL.md |
| **Pha BUILD** | log cho thấy đã xong hết research, đang `write_file(build_report.py)` hoặc `patch(...)` | **Đầy đủ** trên disk | Re-dispatch scope hẹp (dưới) |

Dấu hiệu pha BUILD: `status=interrupted`, duration 1300-2000s, summary chỉ còn một câu mô tả đang viết dở kiểu *"Now writing build_part2.py with sections 4-7 + JS + assembly:"*.

## Quy trình 3 bước khi chết ở pha BUILD

### 1. Đọc pha cuối của transcript

```bash
tail -20 ~/AppData/Local/hermes/cache/delegation/live/<delegation_id>/task-N.log
```

Tìm dòng `think` / `tool` cuối. Nếu thấy `write_file(...build_report.py)` đã `ok` → dữ liệu và script build đều còn.

### 2. Xác nhận file trung gian

```bash
ls -la "<project>/data/"
```

Phải thấy các file research đã hoàn tất (`pubmed_out.json`, `pubchem_out.json`, `physchem.json`, ...). Kích thước lớn (hàng trăm KB) là dấu hiệu đã ghi đủ, không bị cắt.

### 3. Re-dispatch với goal HẸP

Không chạy lại từ đầu. Goal mẫu:

> *Build và publish HTML báo cáo toàn diện nhóm X từ dữ liệu đã có. Không cần fetch thêm dữ liệu. Trả link.*

`context` phải chứa:
- **Đường dẫn tuyệt đối** tới từng file data (`D:\...\<project>\data\*.json`) kèm mô tả nội dung + số lượng bản ghi.
- **Design tokens** đã dùng (palette hex, font) để không phải suy lại.
- **Template mục lục** (danh sách section) để không phải tự thiết kế lại.
- Câu chốt: **"KHÔNG fetch thêm dữ liệu."**

## Kết quả đã kiểm chứng

Session 10/2026, batch 3 subagent viết báo cáo hợp chất thiên nhiên:

| Subagent | Kết quả lần 1 | Sau xử lý |
|---|---|---|
| Saponin | hoàn thành bình thường (~27 phút) | publish OK |
| Alkaloid | interrupted sau 21 phút ở pha build | re-dispatch scope hẹp → xong trong ~13 phút |
| Terpenoid | interrupted sau 32 phút ở pha build | re-dispatch scope hẹp → xong trong ~11 phút |

Không mất dữ liệu nào. Không cần chạy lại pha research.

## Nguyên tắc thiết kế rút ra

Với báo cáo lớn (data >500KB, 15+ bảng, nhiều section), **tách pha thu thập và pha build thành 2 delegation riêng**. Gộp chung trong một task thì task cuối batch gần như luôn chết — batch chạy song song nên subagent cuối chịu độ trễ tích lũy.

Cách tách:

```
Task A (data collection)  → ghi ra <project>/data/*.json, KHÔNG viết HTML
Task B (build + publish)  → đọc <project>/data/*.json, KHÔNG fetch
```

Task B luôn chạy được cả khi Task A bị interrupt giữa chừng, miễn file data đã kịp ghi.
