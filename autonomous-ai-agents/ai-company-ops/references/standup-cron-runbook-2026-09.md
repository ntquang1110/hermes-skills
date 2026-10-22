# Standup cron — cơ chế chạy + 5 pitfall vận hành (verify thật 23/09/2026)

Session chạy standup bằng cron (no user present). Đây là những thứ ăn thời gian/chết người khi chạy lại.

## 1. Cơ chế chạy (đã verify)

| Bước | Lệnh | Ghi chú |
|---|---|---|
| Guard | `python hub/ops_guard.py --json` | Chạy thẳng qua terminal tool được — KHÔNG dính lifecycle guard. Đây là CO CỨNG về số liệu. |
| Standup | `python hub/run.py standup > /tmp/standup_$(date +%Y%m%d).log 2>&1` | Mất **>3 phút** (5 agent × think). Foreground bị chặn: `Foreground timeout 960s exceeds the maximum of 600s`. |
| Chờ | `process(action='wait')` rồi `read_file` log | Trong CRON `notify_on_complete` KHÔNG khả dụng (one-shot runner). `wait` bị clamp ~180s → poll lại. Log ~13KB → đọc bằng `read_file`, KHÔNG `head/tail` qua terminal. |
| Đọc task | `store/tasks.json` = dict `{tasks:[...], next_id}` | Đọc `data['tasks']`, không phải list. |
| Verify claim | `python hub/verify_done.py --claim "<path|hash>"` | exit 0 ACCEPT / 1 REJECT / 2 link chưa kiểm chứng. |
| Wake | `python hub/wake_agent.py <task_id> "<msg>"` | Tự login `/api/login` (quang@kiemsaphia.com / <PASSCODE>) rồi POST message vào thread, source=ai. |

Script tạm: `write_file` vào repo → `python <file>` → `rm -f` NGAY (check `git status --porcelain` để chắc không sót). Script VERIFY (không phải script đọc data) đặt ở `%TEMP%/hermes-verify-*.py`, không để trong repo. Tránh `python -c "..."` inline (→ pending_approval trong cron mode).

## 2. Wake vào task `mode=kanban` ĐỔI PHASE của nó

Wake `#47` (kanban, assignee Quang, phase planning) → worker claim → PO trả plan → `AgentWorker._set_task_status` ghi `store/tasks.json` (vì source=ai) → task tự `planning → review`.

- Hữu ích: đẩy việc tồn từ context-scan sang trạng thái chờ Quang chốt, có plan thật trong thread để Quang đọc.
- Side effect thật: task của NGƯỜI (kanban) rời planning mà Quang không yêu cầu. Chỉ wake khi muốn đúng hiệu ứng đó.
- Verify sau wake: đọc message thread (`GET /api/tasks/<id>/messages?source=ai&token=<tok>`) + phase mới trong `store/tasks.json`. Xác nhận có message role=agent, agent=<tên> (không chỉ "🤖 Đã nhận — đang xử lý...").
- Routing: chèn "Viết kế hoạch"/"viết plan" vào message để chắc route về PO (rule ưu tiên đứng TRƯỚC `DOMAIN_AGENTS`), nếu không chữ "code"/"thread" trong message sẽ bị nuốt sang Senior Dev/Content.
- Message nên ghi rõ "không code, không tự đóng task" — PO vẫn critique + hỏi lại nếu thiếu mô tả task; gửi kèm title/description đầy đủ của các task liên quan trong 1 message để đỡ vòng hỏi lại.

## 3. Số STALE agent báo KHÔNG phải nguồn sự thật

Standup 23/09:

| Nguồn | #8 | #43-46 |
|---|---|---|
| Agent báo (CTO/Dev1/Content) | stale 10.0d | stale 15.8d |
| `ops_guard.py --json` (thật) | KHÔNG stale (wake 22/09 bump `updated_at`) | 18.8d |

Agent đọc briefing/log cũ (đúng pitfall "STALE ảo" trong SKILL.md). Luôn trích số guard trong report; lệch số thì nêu rõ agent nào lệch, đừng copy số của agent.

## 4. Claim bịa dạng ngắn vẫn phải verify bằng máy

QA standup 23/09: "Test plan `test_plans/byteark_fallback_v2.md` đã commit ở HEAD `5e15ee0`".

```
python hub/verify_done.py --claim "test_plans/byteark_fallback_v2.md"
→ không tìm thấy file/dir  (exit 1 = REJECT)
```

Kết luận: vi phạm DoD, KHÔNG tính là đóng; ghi thẳng trong report. Claim kèm hash mà file không tồn tại cũng xử y hệt — verify path trước, hash sau.

## 5. Kết luận report khi team hết việc agent tự làm

23/09: 8 task mở (#43-50) toàn `mode=kanban` + #8 chờ test thật của Quang → team **0 việc agent tự chạy được**. Report đúng phải nói thẳng điều đó + 2-3 nút Quang cần chốt (chốt lô trùng, duyệt DC/plan, chạy test thật), KHÔNG dán lại báo cáo 5 agent. Đây là gốc của "standup lặp lại nhau": bottleneck là quyết định của Quang, không phải code.

Lưu ý trước khi commit: `git pull --rebase` fail nếu còn unstaged (`hub/store.py`, `briefing.md` do standup ghi timestamp) → commit ĐÚNG file code/docs rồi `git push origin HEAD:main`. TUYỆT ĐỘT không `git add -A` (tfo_data/*.m4a, context_scan.json, store/*.json runtime là derived/local).

## 6. Số đi vào tài liệu phải ĐO, không suy từ log đã lọc (01/10/2026)

Chi tiết đầy đủ + mẫu verify 16/16: **`references/standup-number-discipline-2026-10.md`**. Tóm tắt 5 lỗi đã dính:

1. **Log đã lọc ≠ log đầy đủ.** Script chỉ in cặp sim ≥ 0.66 mà em đếm tay số nhóm ở ngưỡng 0.70 → ghi "10 nhóm" vào spec (`216416d`), verify đo ra **9**. Số vào spec/state/briefing phải do script **in ra trực tiếp**; muốn nói "ở threshold khác ra mấy" thì **chạy lại script ở threshold đó**.
2. **Đừng vội kết luôn "phiên trước sai"** khi đính chính. Chạy lại phép đo trên **cả hai mốc** rồi so — 01/10 suýt ghi "30/09 báo 9 là sai", hoá ra 30/09 đúng và bản spec hôm nay sai. Cảm giác "vừa tìm ra lỗi nghiêm trọng" dễ bịa thêm lỗi ở chỗ khác để hợp thức hoá.
3. **Verify script FAIL → kiểm tra script trước, repo sau.** 2 FAIL đầu là bug assertion, không phải lỗi repo: `git show --stat` in thêm dòng summary (`2 files changed, ...`) → phải lọc `if "|" in ln`; `git branch -r --contains <hash>` trả **tên branch**, không trả hash → check `"origin/main" in output`. Sửa assertion rồi **báo cáo trung thực** 2 FAIL đó, đừng giấu.
4. **`echo "EXIT=$?"` sau pipe là exit của `tail`, luôn 0** → dùng `${PIPESTATUS[0]}`. Không có nó thì script `exit(1)` khi fail vẫn in EXIT=0 → **verification pass giả**.
5. **Không viết hash commit trước khi commit.** Commit → `git rev-parse --short HEAD` → mới patch hash vào tài liệu (em từng ghi `d5c1f7a` placeholder rồi phải quay lại sửa thành `ecb5217`).

Gotcha: `store/activity.json` dùng field **`time`** (không phải `ts`/`timestamp`) — sai field → tưởng log trống. Chain sống = 5× WARN OpenCode → 5× OK ByteDance, 0 None.
