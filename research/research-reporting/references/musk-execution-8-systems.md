# Musk 8-System Execution Playbook — Verified 09/2026

**Source file:** `elon-musk-he-thong-van-hanh.md` (30KB, 8 chương + lộ trình 90 ngày)
**Brief that triggered it:** "Research Elon Musk's execution methods ... 8 items" — Vietnamese founder running multiple businesses, needs actionable patterns not theory. Research EN, output VI.
**Reuse:** Khi brief yêu cầu playbook hành động 8 hệ thống vận hành của Musk (hoặc founder khác dùng khung tương tự), đây là nguồn neo + cấu trúc deliverable.

## Khung B — 8 hệ thống (đối chiếu Khung A chiến lược tổng thể trong founder-strategy-profile.md)

| # | Hệ thống | Mantra / Quy tắc chuẩn | Ví dụ neo (năm + con số phải giữ) |
|---|---|---|---|
| 1 | The Algorithm 5 bước | Question → Delete → Simplify → Accelerate → Automate. Sai lầm phổ biến: làm ngược (Automate trước). Isaacson 2023 + email Tesla 2020 | Model Y gigacasting xóa 370 chi tiết → 1 tấm đúc; Starship thép 304L xóa 90% mối hàn; Production Hell 2018: tự động hóa quá sớm → tháo robot |
| 2 | Điều hành họp | 6 quy tắc email 4/2017: tránh họp lớn, được rời họp, cấm acronym, giao tiếp xuyên cấp, common sense > quy tắc, không PowerPoint (demo phần cứng) | SpaceX họp 7h quanh tên lửa Starbase; X 11/2022 hủy họp định kỳ → war room nửa đêm 10-15 người |
| 3 | Tuyển dụng | Evidence of exceptional ability > bằng cấp; câu hỏi tủ "vấn đề khó nhất — kể từng bước chi tiết" + câu đố Cực Bắc (test tư duy, không phải đáp án) | Shotwell Microcosm $18M; Straubel garage Stanford; X 2022 hardcore: review code trực tiếp, không commit 2 tuần → out |
| 4 | Đặt mục tiêu | Deadline = vật lý tối thiểu ×1.2; trễ 50% vẫn thắng nếu nhanh gấp 3 lần ngành; nếu <30% team thấy điên rồ → chưa đủ tham vọng | Falcon 9 landing hứa 2013 → đạt 12/2015; Model 3 5k/tuần hứa 12/2017 → đạt 7/2018 (báo chí gọi thất bại nhưng nhanh hơn ngành 3 năm) |
| 5 | Quản trị khủng hoảng | Pattern 5 bước: có mặt tại xưởng → cắt war-time (giữ 30-90 ngày sống) → all-in có tính toán → brutal honesty → nâng chuẩn (giữ 50% kỷ luật thời chiến) | 24/12/2008 Tesla $40M + SpaceX NASA $1.6B cùng ngày (cách nhau giờ); lều GA4 3 tuần 2018; X 7.5k→1.5k (-80%) + cắt 70% cloud |
| 6 | Giao tiếp | Email <5 câu, shortest-path (xuyên cấp), mass-email toàn công ty, thưởng báo tin xấu sớm (carrot & stick) | "Acronyms Seriously Suck" 2010; email xuyên cấp 2017; X hardcore 2h sáng 11/2022 click Yes/No |
| 7 | Quản lý thời gian đa cty | Time block 5 phút (thực hành 30 phút), 80% engineering, single-threaded "công ty của tuần" 60-70%, Gemba walk 1h/ngày, sprint 3-4 tuần + 1 tuần nhẹ, ngủ 6h | Lịch Isaacson: T2-3 Starbase, T4-5 Giga Texas/Fremont, T6 X+xAI |
| 8 | Delete Step | "Không thêm lại 10% = chưa xóa đủ" (All-Hands 2019) — xóa trước tối ưu; mọi quy trình phình to theo thời gian | Van SpaceX $10k→$200; dây Model S 3km→Model Y 100m (-95%); X microservices 200→40 (-80%) |

## Deliverable shape (đã chốt)

- File markdown tiếng Việt, 8 chương, mỗi chương = cơ chế + ví dụ năm/con số + điểm mù/thất bại + checklist ✅ cho founder Việt (vốn mỏng/lao động VN).
- Lộ trình 90 ngày: Tháng 1 Xóa & Đơn giản (Algorithm + Delete Friday + quy tắc họp) → Tháng 2 Tốc độ & Tuyển dụng (aspirational deadline + JD mới + time blocking) → Tháng 3 Khủng hoảng & Giao tiếp (#tin-xau + mass email + diễn tập war-time).
- Dòng vàng xuyên suốt: "Tốc độ > Hoàn hảo. Xóa > Tối ưu. Hiện trường > Phòng họp. Bằng chứng năng lực > Bằng cấp."

## Thu thập — workaround đã verify (đừng lặp lại sai lầm)

- **SearXNG :8888 HTTP 000 (down):** fallback browser Wikipedia + Jina Reader, không block pipeline.
- **Báo Mỹ 403 (BusinessInsider/CNBC/Teslarati) + Wikipedia API 429:** đừng retry curl mãi; Wikipedia Business_career_of_Elon_Musk + Leadership_style + Twitter_under_Elon_Musk + SEC/NASA filings + Isaacson quotes đã đủ dựng 8 chiều. Ghi paywall thay vì bịa.
- **Snapshot truncate (500 phần tử):** dùng `browser_console` JS trích trực tiếp: `document.getElementById('Leadership_style')?.parentElement?.parentElement?.innerText` hoặc loop `querySelectorAll('h2')` + `nextElementSibling` gom `<p>` — đã cứu session 09/2026.
- **python vs python3 trên Windows host:** `python` = 3.11.15 chạy được; `python3` = missing (Microsoft Store alias). Dùng `python` cho mọi script.
