# Team Architecture Patterns (adapt từ revfactory/harness, Apache-2.0)

6 pattern kiến trúc team + decision tree + phase selection matrix + vòng tiến hóa.
Adapt cho Hermes: "team mode" = orchestrator agent + delegate_task batch, "sub-agent mode" = delegate_task leaf đơn.
Lưu ý giới hạn Hermes: leaf không delegate tiếp, max 3 concurrent (delegation.max_concurrent_children), max_spawn_depth=1 nên orchestrator bị ép thành leaf.

## 6 Pattern

| Pattern | Mô tả | Dùng khi | Mode phù hợp trên Hermes |
|---------|-------|----------|--------------------------|
| **Pipeline** | Tuần tự, output bước trước là input bước sau | Các bước phụ thuộc chuỗi mạnh (phân tích → thiết kế → code → test) | delegate tuần tự, mỗi task nhận output task trước qua context. Team mode ít lợi, trừ khi có đoạn song song trong pipeline |
| **Fan-out/Fan-in** | Song song độc lập rồi gộp | Nhiều góc nhìn/nguồn độc lập trên cùng đầu vào (research đa nguồn, review nhiều khía cạnh) | **delegate_task batch (tối đa 3 concurrent)** + 1 task gộp. Pattern tự nhiên nhất cho team mode |
| **Expert Pool** | Router chọn chuyên gia theo loại input | Input khác loại → xử lý khác nhau (code review: security/perf/arch) | sub-agent đơn: agent chính tự chọn skill/subagent theo loại. Không cần team thường trực |
| **Producer-Reviewer** | Tạo → kiểm duyệt → tạo lại nếu fail | Chất lượng quan trọng, tiêu chí khách quan kiểm được | delegate task tạo + task review riêng (agent khác, không tự review). Giới hạn retry 2-3 lần, tránh loop vô hạn |
| **Supervisor** | Trung tâm giữ state, phân việc động theo tiến độ | Khối lượng biến thiên, phân bổ runtime (migration nhiều file) | orchestrator giữ task list, dispatch theo kết quả từng bước. Khác fan-out: fan-out chia cố định từ đầu, supervisor điều chỉnh khi chạy |
| **Hierarchical Delegation** | Phân cấp đệ quy, trên giao việc cho dưới | Vấn đề phân rã tự nhiên theo cấp (fullstack: lead → frontend/backend team) | **Cẩn thận:** Hermes max_spawn_depth=1, leaf không delegate. Flat hóa thành 1 tầng hoặc dùng nhiều orchestrator session tuần tự. Độ sâu ≥3 tầng = trễ + mất context, tránh |

## Decision Tree (chọn pattern)

```
Có ≥2 agent tham gia?
├── Yes → Các agent cần trao đổi/đối chiếu/feedback nhau?
│         ├── Yes → TEAM mode (orchestrator + batch delegate)
│         │         └── Chọn pattern theo tính chất:
│         │             song song độc lập → Fan-out/Fan-in
│         │             tạo rồi kiểm duyệt → Producer-Reviewer
│         │             phân việc động theo tiến độ → Supervisor
│         │             chuỗi phụ thuộc → Pipeline
│         └── No (chỉ cần trả kết quả) → SUB-AGENT mode (batch delegate độc lập)
│             └── Expert Pool / Fan-out đơn giản
└── No (1 agent) → sub-agent đơn, không cần team
```

**Nguyên tắc:** team mode là mặc định khi ≥2 agent cần tương tác. Chọn sub-agent khi "agent có thực sự cần nói chuyện với nhau không?" là No.

## Composite Patterns

| Tổ hợp | Cấu trúc | Ví dụ |
|--------|----------|-------|
| Fan-out + Producer-Reviewer | Tạo song song → từng cái review riêng | Dịch 4 ngôn ngữ song song → từng bản native review |
| Pipeline + Fan-out | Tuần tự, có đoạn song song | Phân tích (tuần tự) → implement (song song) → test tích hợp (tuần tự) |
| Supervisor + Expert Pool | Supervisor phân loại → gọi đúng chuyên gia | Xử lý ticket: phân loại → gán đúng expert |

## Phase Selection Matrix (build mới / mở rộng / bảo trì)

Trước khi sửa hệ thống agent/skill, audit hiện trạng rồi route:

| Loại thay đổi | Audit hiện trạng | Thiết kế team | Agent def | Skill | Orchestrator | Verify |
|---------------|------------------|---------------|-----------|-------|--------------|--------|
| Build mới | Bắt buộc (đếm agent/skill sẵn có) | Bắt buộc | Bắt buộc | Bắt buộc | Bắt buộc | Bắt buộc |
| Thêm agent | Bỏ qua (dùng audit) | Chỉ chọn mode | Bắt buộc | Chỉ khi cần skill riêng | Sửa | Bắt buộc |
| Thêm/sửa skill | Bỏ qua | Bỏ qua | Bỏ qua | Bắt buộc | Chỉ khi liên kết đổi | Bắt buộc |
| Đổi kiến trúc | Bỏ qua | Bắt buộc | Chỉ agent bị ảnh hưởng | Chỉ skill bị ảnh hưởng | Bắt buộc | Bắt buộc |

## Reuse Review (trước khi tạo agent/skill mới)

Tạo mới dễ tích tụ trùng lặp dưới tên khác. Check trước:

| Tình huống | Hành động |
|------------|-----------|
| Agent/skill cũ phủ hoàn toàn vai trò mới | Không tạo, dùng lại |
| Phủ một phần + generalize được | Generalize cái cũ rồi mở rộng |
| Phủ một phần + cố ý domain-specific | Tạo mới, giữ riêng |
| Hoàn toàn khác | Tạo mới |

Khi generalize agent/skill cũ: check dependency (orchestrator/team nào đang dùng nó), sau khi đổi chạy dry-run giữ nguyên hành vi cũ.

## Evolution Loop (vòng tiến hóa)

Hệ thống agent/skill là hệ sống, không phải artifact tĩnh. Sau mỗi run hỏi feedback; nếu không có thì thôi, không ép.

| Feedback type | Sửa chỗ nào |
|---------------|-------------|
| Kết quả kém | Skill của agent đó (thêm tiêu chí chất lượng) |
| Thiếu vai trò | Agent definition (thêm agent) |
| Sai thứ tự workflow | Orchestrator (đổi phase) |
| Team sai (nên gộp/tách) | Orchestrator + agent defs |
| Trigger không bắt | Skill description (mở rộng trigger keyword) |

Change history: ghi mọi thay đổi vào bảng 4 cột (ngày, nội dung, đối tượng, lý do). Chống regression và thấy hướng tiến hóa.

Tự đề xuất tiến hóa khi (không cần user yêu cầu):
- Cùng 1 feedback lặp ≥2 lần
- Agent fail lặp lại cùng pattern
- User bỏ qua orchestrator, làm tay

## Pitfalls

- **Depth ≥3 tầng hierarchical** → trễ + mất context. Flat hóa.
- **Retry Producer-Reviewer vô hạn** → loop tốn token. Cứng 2-3 lần.
- **Review do chính agent tạo ra tự review** → dễ tự pass. Luôn route sang agent khác.
- **Tạo agent mới không check reuse** → tích tụ trùng lặp. Luôn chạy reuse review.
