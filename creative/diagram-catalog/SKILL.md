---
name: diagram-catalog
description: "Router 45 loại biểu đồ → skill/tool + format output chuẩn."
version: 1.0.0
author: Hermes Agent (Quang)
license: MIT
platforms: [linux, macos, windows]
---

# Diagram Catalog — Router 45 loại biểu đồ

## Khi nào dùng

- Người dùng nhờ vẽ một sơ đồ/biểu đồ/infographic, không nói rõ dùng công cụ nào.
- Đang visualize nội dung (bài KFlow, nghiên cứu, giải thích cơ chế) và cần chọn đúng kiểu trình bày.
- Muốn đảm bảo output là HTML/SVG độc lập mở được ngay, không cần phần mềm.

## Nguyên tắc cốt lõi (đã duyệt)

1. **`diagram-design` là skill tổng hợp** — mã được 25+ loại diagram, output HTML/SVG độc lập. Phủ ưu tiên số 1 cho mọi loại kỹ thuật.
2. **`architecture-diagram`** — chuyên infra/cloud (dark-themed SVG-HTML).
3. **`dashboard-design-system` + `html-interactive-dashboard`** — card/scorecard/quadrant/comparison.
4. **`visual-academic-html`** — explainer, code-to-outcome, học thuật 2 tab.
5. **`excalidraw`** — concept/relationship/ecosystem map (hand-drawn).
6. **`matplotlib`** (qua terminal Python) — chart cần dữ liệu thật.
7. Còn lại vẽ thẳng HTML — không cần skill mới.

## Bảng 45 loại → skill + format

Tên tiếng Việt khớp danh sách 45 loại chuẩn (post "Agent native" ảnh 01/09).

| # | Loại (VI) | Loại (EN) | Skill/Tool chính | Format |
|---|-----------|-----------|------------------|--------|
| 1 | Trước-Sau | Before-and-After | diagram-design | HTML |
| 2 | Nguyên Nhân-Hậu Quả | Cause-and-Effect | diagram-design (fishbone) | HTML |
| 3 | Kiến trúc Hệ thống | System Architecture | architecture-diagram | SVG-HTML |
| 4 | Bản đồ Mạng | Network Map | architecture-diagram | SVG-HTML |
| 5 | Luồng Dữ liệu | Data-Flow Diagram | diagram-design (data flow) | HTML |
| 6 | Luồng Thông tin | Information-Flow | diagram-design (flow) | HTML |
| 7 | Vòng Xoay | Flywheel | diagram-design (loop/flywheel) | HTML |
| 8 | Vòng Phản hồi | Feedback Loop | diagram-design (loop) | HTML |
| 9 | Phân cấp | Hierarchy | diagram-design (nested/tree) | HTML |
| 10 | Sơ đồ Tổ chức | Organization | diagram-design (org chart) | HTML |
| 11 | Sơ đồ Tư duy | Mind Map | diagram-design (spider/radial) | HTML |
| 12 | Bản đồ Khái niệm | Concept Map | excalidraw / HTML | JSON/HTML |
| 13 | Bản đồ Quan hệ | Relationship Map | excalidraw / HTML | JSON/HTML |
| 14 | Bản đồ Hệ sinh thái | Ecosystem Map | excalidraw / HTML | JSON/HTML |
| 15 | Bản đồ Bên liên quan | Stakeholder Map | diagram-design (quadrant) | HTML |
| 16 | Bản đồ Phụ thuộc | Dependency Map | diagram-design (tree) | HTML |
| 17 | Bản đồ Hành trình | Journey Map | diagram-design (swimlane+timeline) | HTML |
| 18 | Luồng Người dùng | User-Flow | diagram-design (flowchart) | HTML |
| 19 | Lộ trình | Roadmap | diagram-design (timeline) | HTML |
| 20 | Cột mốc | Milestone | diagram-design (timeline) | HTML |
| 21 | Gantt | Gantt-style | diagram-design (Gantt) | HTML |
| 22 | Làn bơi | Swimlane | diagram-design (swimlane) | HTML |
| 23 | Sankey | Sankey-style | matplotlib (cần data nguồn) | PNG/SVG |
| 24 | Venn | Venn | diagram-design (venn) | HTML |
| 25 | Bảng So sánh | Comparison Table | HTML design system | HTML |
| 26 | Ma trận So sánh | Comparison Matrix | dashboard-design-system | HTML |
| 27 | Góc phần tư | Quadrant | diagram-design (quadrant) | HTML |
| 28 | Ưu-Nhược | Pros-and-Cons | HTML design system | HTML |
| 29 | Kim tự tháp | Pyramid | diagram-design (pyramid/funnel) | HTML |
| 30 | Sơ đồ Lớp | Layer Diagram | diagram-design (layer stack) | HTML |
| 31 | Phổ | Spectrum | diagram-design / HTML | HTML |
| 32 | Mô hình Trưởng thành | Maturity Model | diagram-design (layer/quadrant) | HTML |
| 33 | Tiến trình | Progression | diagram-design (timeline) | HTML |
| 34 | Bảng điểm | Scorecard | dashboard-design-system | HTML |
| 35 | Thẻ Thống kê | Statistic Cards | dashboard-design-system | HTML |
| 36 | Cột (Bar) | Bar Chart | matplotlib / HTML chart | PNG/HTML |
| 37 | Đường (Line) | Line Chart | matplotlib / HTML | PNG/HTML |
| 38 | Vành khuyên (Donut) | Donut | matplotlib / HTML | PNG/HTML |
| 39 | Phân tán (Scatter) | Scatter Plot | matplotlib / diagram-design | PNG/HTML |
| 40 | Bản đồ Nhiệt | Heat Map | matplotlib (cần ma trận data) | PNG/SVG |
| 41 | Giao diện Chú thích | Annotated Interface | HTML (mockup + annotation) | HTML |
| 42 | Giao diện Tách lớp | Exploded Interface | HTML (mockup + explode note) | HTML |
| 43 | Mã nguồn→Kết quả | Code-to-Outcome | visual-academic-html | HTML |
| 44 | Giải thích Cách hoạt động | How-It-Works Explainer | visual-academic-html (2 tab) | HTML |
| 45 | Tái hiện Sự cố | Incident Reconstruction | diagram-design (timeline) | HTML |

## Chọn loại theo MỤC ĐÍCH diễn giải (intent-first)

Đừng bắt đầu từ tên loại. Bắt đầu từ câu hỏi "muốn người xem hiểu/want làm gì sau khi nhìn". Nhóm theo intent, rồi thu hẹp trong nhóm.

| Mục đích (intent) | Câu hỏi cốt lõi | Nhóm loại |
|---|---|---|
| **So sánh** | Đối chiếu mấy thứ hơn/kém, hay/dở, trước/sau | Comparison Table, Comparison Matrix, Pros-and-Cons, Quadrant, Before-and-After, Spectrum, Maturity Model, Venn |
| **Cấu trúc/quan hệ** | Ai thuộc ai, cái này nối cái gì, nằm trong/lớp nào | Hierarchy, Org, Mind Map, Concept Map, Relationship Map, Ecosystem Map, Stakeholder Map, Dependency Map, Layer Diagram, Pyramid, Flywheel |
| **Luồng/tiến trình** | Đi từ A qua B rồi C thế nào, ai làm bước nào | Data-Flow, Information-Flow, User-Flow, Journey Map, Swimlane, Sequence, Feedback Loop |
| **Thời gian** | Việc gì xảy ra khi nào, theo thứ tự nào | Roadmap, Milestone, Timeline, Progression, Gantt |
| **Dữ liệu số** | Con số cao thấp, phân bố, tương quan | Bar, Line, Donut, Scatter, Heat Map, Sankey, Statistic Cards, Scorecard |
| **Giải thích hoạt động** | Máy/hệ/hàm này chạy ra sao, input → mà outcome | How-It-Works Explainer, Code-to-Outcome, Annotated/Exploded Interface, System Architecture, Network Map |

### Thu hẹp trong nhóm — cặp hay nhầm

- **So sánh**: 2 mục → Comparison Table hoặc Pros-and-Cons (Table nếu nhiều tiêu chí so sánh được, Pros-and-Cons nếu chỉ 1 món + ưu/nhược). 4 mục có 2 trục → Quadrant. Trước/sau cùng 1 đối tượng → Before-and-After. Nhiều mục 1 thang đo → Comparison Matrix hoặc Spectrum.
- **Cấu trúc**: quan hệ thuộc-của phân cấp → Hierarchy. Quan hệ ngang lỏng lẻo giữa ý → Concept/Relationship Map. Các thành phần chồng lớp → Layer Diagram / Pyramid (Pyramid khi có thứ bậc trên-dưới). Vòng tự củng cố → Flywheel / Feedback Loop.
- **Luồng**: 1 tác nhân đi qua bước → User-Flow (đơn giản) hay Journey Map (nhiều staging + cảm xúc). Nhiều tác nhân song song → Swimlane. Luồng dữ liệu/hệ thống → Data-Flow.
- **Thời gian**: mốc vài điểm → Milestone/Timeline. Tổng thể dài hạn theo pha → Roadmap. Task song song vs thời gian → Gantt.
- **Dữ liệu số**: 1 chuỗi → Bar/Line. Phần-trong-tổng → Donut. Tương quan 2 biến → Scatter. Ma trận 2D + cường độ → Heat Map. Dòng chảy số lượng giữa 2 đầu → Sankey. Số + mục tiêu cần bảng điều khiển → Scorecard/Statistic Cards.
- **Giải thích hoạt động**: input → thuật → output → Code-to-Outcome (nếu là code) hoặc How-It-Works (nếu là cơ chế). Chỉ ra bộ phận → Annotated/Exploded Interface. Toàn hệ phân tán → System Architecture / Network Map.

### Luật quyết định nhanh (default)

1. Có **số liệu thật** → nhóm Dữ liệu số. Chưa có → hỏi trước, đừng tự bịa.
2. Có **thời gian/trật tự** → nhóm Thời gian.
3. Có **quy trình nhiều bước** → nhóm Luồng.
4. Có **thành phần-lớp-thuộc về** → nhóm Cấu trúc.
5. Có **2 thứ trở lên đối chiếu** → nhóm So sánh.
6. Muốn **người xem hiểu một hệ/cơ chế hoạt động** → nhóm Giải thích hoạt động.
Hai intent trùng (vd vừa so sánh vừa thời gian) → chọn intent chính mà người xem cần hành động, không vẽ 2 thứ lộn xộn trong 1 hình.

## Quy trình triển khai

1. Nghe yêu cầu → xác định **loại** từ cột "Loại" (tên gọi có thể lệch: "trình bày trước sau" = Before-and-After, "vẽ quy trình" = Data-Flow/User-Flow).
2. Tra bảng → lấy **skill chính**. Load skill đó bằng `skill_view(name)`.
3. Tập hợp đủ dữ liệu thật cần thiết (timeline, ma trận, dữ liệu chart). Đừng bịa số liệu.
4. Dựng output HTML/SVG độc lập. Mở kiểm tra qua browser hoặc vision.
5. Trao file kèm `MEDIA:<path>` nếu cần xem.

## Bẫy

- **Đừng gọi sai skill.** Architecture/cloud → `architecture-diagram`, không phải `diagram-design`. Chart có số liệu → `matplotlib`, không vẽ tay.
- **Loại cần + dữ liệu thật** (23 Sankey, 40 Heat Map, 17 Journey, 45 Incident): hỏi người dùng lấy data/timeline trước, đừng tự bịa.
- **Diễn giải tên lệch**: "biểu đồ kim tự tháp" = Pyramid, "diễn giải trước/sau" = Before-and-After, "luồng thông tin" = Information-Flow. Khi phân vân, ưu tiên skill có template phù hợp nhất ngữ nghĩa, không phải tên trùng.
- **32 Maturity Model**: nếu là 5 bậc theo cột → layer stack; nếu 2×2 → quadrant. Chọn theo không gian trình bày.

## Verify

- File .html mở được bằng trình duyệt (không lỗi JS, không copy ngoài path).
- Với chart dữ liệu: khớp số liệu nguồn, có label + đơn vị.
- Với diagram: node/liên kết đầy đủ, không thiếu nhánh so với nội dung gốc.