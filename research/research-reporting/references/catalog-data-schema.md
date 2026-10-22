# Catalog Data Schema & Build Flow (multi-compound catalog)

Verified 12/08/2026 — catalog 40 hoạt chất trị tiêu chảy heo con, mobile-first, 1 file HTML (~200KB), publish preview + KFlow thành công.

## JSON schema mỗi chất (truyền đầy đủ cho subagent research)

```json
{
  "id": "slug-ngan",
  "name_vi": "Tên tiếng Việt",
  "name_en": "English name",
  "latin": "Tên khoa học / nguồn",
  "category": "Tannin|Polyphenol|Alkaloid|Tinh dầu|Probiotic|Prebiotic|Organic acid|MCFA|Khoáng|Clay hấp phụ|Kháng thể|Phi dược|Thảo dược|Khác",
  "summary": "1-2 câu tổng quan",
  "mechanism": ["cơ chế 1", "cơ chế 2"],
  "evidence_level": "Mạnh|Vừa|Sơ bộ",
  "dosage_ref": "Liều tham chiếu trong cám",
  "side_effects": ["tác dụng phụ 1"],
  "extraction": {
    "method": "SOP chính: dung môi, tỉ lệ nguyên liệu:dung môi, nhiệt độ, thời gian, số lần chiết",
    "variants": ["phương pháp khác"],
    "yield_tips": "Cách chiết hiệu suất + chất lượng tốt nhất",
    "quality_control": "Hàm lượng hoạt chất, độ ẩm, tổng vi sinh, KLN",
    "risks": ["oxy hóa, nhiệt phân hủy, cặn dung môi..."],
    "mold_prevention": "Chống mốc/ổn định dạng lỏng hoặc bột",
    "equipment": "Thiết bị cần"
  },
  "production": {
    "method": "Quy trình lên men/bào chế chính",
    "stability": "Nhiệt ép viên, ẩm, hạn dùng",
    "risks": ["nhiễm tạp, chết men >70°C..."],
    "quality_control": "Đếm CFU, độ ẩm..."
  },
  "references": [
    {"type": "paper", "label": "Tác giả, Tạp chí, Năm", "pmid": "", "doi": "", "note": "phát hiện chính"},
    {"type": "patent", "number": "", "title": "", "note": "điểm mấu chốt"}
  ],
  "verification": "Ghi rõ đã verify PMID nào (efetch), patent nào tìm thấy, cái gì chưa"
}
```

Quy tắc:
- Chất chiết xuất thực vật → dùng `extraction`; chất lên men/khoáng/bào chế → dùng `production`.
- MỌI PMID phải efetch verify (abstract thật, đúng chủ đề). KHÔNG bịa PMID/patent.
- Patent không verify được → `number=''` + `note='chưa verify'` thay vì bịa số.
- Output tiếng Việt có dấu.

## JSON schema ROW-LEVEL (khi 1 chất × nhiều tác dụng — REE đất hiếm 12/08/2026)

Dùng khi user muốn bảng "mỗi dòng = 1 nguyên tố/dạng × 1 tác dụng" (1 chất lặp nhiều lần, mỗi lần 1 tác dụng khác nhau). Đây là schema KHÁC hẳn schema compound ở trên — đừng trộn:

```json
{
  "id": "slug-ngan",
  "element": "La",
  "element_vi": "Lantan",
  "name_en": "Lanthanum",
  "effect": "Tăng trọng (ADG) heo con cai sữa",
  "group": "LREE|REE nặng|Nano REE|Hỗn hợp/Quy định",
  "mechanism": "Mô tả cơ chế cụ thể",
  "evidence_level": "Mạnh|Vừa|Sơ bộ|Không có bằng chứng trực tiếp",
  "dosage_ref": "Liều/ngữ cảnh",
  "side_effects": ["độc tính/tác dụng phụ"],
  "references": [{"type":"paper|patent","label":"...","pmid":"","doi":"","number":"","note":""}],
  "verification": "Đã verify PMID nào, patent nào, cái gì chưa"
}
```

Lưu ý row-level:
- `group` là key filter — phải khớp EXACT (case + dấu) với chip filter: "REE nặng" ≠ "HREE", "Clay hấp phụ" ≠ "Clay". Kiểm tra bằng `Counter(group)` trước khi chốt CATS.
- `evidence_level` có thêm giá trị 4: **"Không có bằng chứng trực tiếp"** — bắt buộc dùng khi nguyên tố không có trial trên heo (Pr, Nd, Sm, Eu...). Màu đỏ trong UI, khác 3 mức kia.
- Nguyên tố không có dữ liệu → vẫn tạo dòng, ghi rõ "Không có bằng chứng trực tiếp" + mechanism mô tả khoảng trống tri thức. Đừng bỏ sót vì user muốn biết CÁI GÌ KHÔNG CÓ.
- Group "Hỗn hợp/Quy định" cho các dòng pháp lý (EU/EFSA, MOA, FDA, GB 2762) — nguồn là văn bản luật không có PMID, để pmid trống + ghi nguồn/URL trong note (không bịa).

## Build flow (3 subagents song song → 1 file HTML)

1. Subagents (parallel, max 3) ghi `data/groupA_*.json`, `groupB_*.json`, `groupC_*.json` — mỗi group 1 nhóm chất (~13-14 chất/group). Truyền schema JSON đầy đủ + PMID gợi ý đã verify từ session trước (subagent tự efetch lại).
2. `template.html`: 1 file self-contained với placeholder `__DATA__` + JS render (list/filter/search/detail hash routing `#/ct/<id>` để share URL). Layout mobile: sticky header + search + filter chips scroll-x + card list + bottom nav.
3. `build.py`: gom các group JSON (xử lý cả dạng list lẫn `{"compounds":[...]}`), normalize field thiếu, inject vào template → 1 file final. Publish preview chỉ nhận 1 file HTML.
4. Browser verify: serve HTTP bằng `python -m http.server` (camofox chặn file:// — xem skill camofox-browser), check JS + overflow bằng browser_console, screenshot mobile 390px bằng playwright-core khi model không vision (deepseek-v4-flash không nhận image_url).
5. Publish preview (`curl --data-binary @payload.json` cho file >50KB) + KFlow, verify card qua `/api/cards`.

## Chống mốc extract lỏng (case "pep green" bị mốc — kinh nghiệm thực tế trại)

- Ethanol ≥20% v/v (lý tưởng 25-30%) — nấm mốc/men ngừng phát triển ở cồn ≥15-20%
- Hạ pH ≤4.5 bằng acid citric/lactic — mốc ưa pH trung tính
- Preservative hiệp đồng: kali sorbat 0.1-0.3% + natri benzoat 0.05-0.1% (hiệu quả nhất ở pH<4.5)
- Vô trùng: lọc 0.45µm rồi 0.22µm, hoặc thanh trùng 80-85°C/15-30 phút trước khi đóng
- Bao bì kín, thủy tinh tối màu / PE-PP thực phẩm, đổ đầy tới miệng giảm khoảng trống oxy, có thể xả khí N2
- Kho mát 15-25°C, tránh ẩm và nắng; hạn dùng 3-6 tháng, kiểm tra mùi/vị/độ đục định kỳ

## PMID khuyến nghị chính (đã verify, tái dùng được cho catalog heo con)

- Tannin: 29799865 (Girard 2018), 32106264 (Girard 2020), 40061905 (Ollagnier 2025), 38397834 (Nuamah meta 2024), 39852918 (Sall trial trại 2025), 34204108 (Dell'Anno 2021)
- S. boulardii: 37576772, 26159939, 34572682, 36630002; probiotic nhiệt diệt: 39272313
- Tinh dầu: 38359649 (meta 2024), 35760400; butyrate coated: 39795009, 33670980 (Towards Zero Zinc Oxide)
- Cơ chế ETEC F4: 38800731
