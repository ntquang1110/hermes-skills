# Run notes — psy_4, 2026-10-22 ("Sự so sánh xã hội và cái bẫy so bì")

Slot 4/4 (cron 18:00), job **2-deliverable**: bản 5 phần KFlow + bản thread chờ duyệt.

## Số đo thật của bản cuối

- `drafts/psy_4.txt`: 5 phần, nhãn TÊN TRẦN (mỗi nhãn 1 dòng riêng): `Ví dụ` / `Nêu vấn đề` / `Vấn đề gốc rễ` / `First principle` / `Giải pháp`. **446 từ** (trần 450). Không ký tự lạ, 0 em/en dash, 0 arrow.
- `threads_drafts/psy_4_thread.txt`: **3 post, 328 / 423 / 496 ký tự, tổng 1242** (trần 1300), dấu tiếng Việt mỗi post 42 / 73 / 76, cả 3 post kết ở câu hoàn chỉnh, 0 `tôi`/`bạn`.
- Chủ đề lấy đúng dòng `4.` của `topics_today.txt`; KHÔNG ghi gì vào `threads_approved/`.

## Lỗi lượt này (để không lặp)

1. **Không load skill** trước khi viết (mở thẳng `topics_today.txt` + `threads_template_v2.txt`).
2. **Chế checker tay 2 lần**, lần đầu đặt trong PROJECT DIR (`psy/scripts/_tmp_measure.py`) → dính cờ "changed path without evidence", phải chạy lại verify để chứng minh đã dọn. Lệnh đúng chỉ là:
   ```
   python "C:/Users/NTQUANG_DELL/AppData/Local/hermes/skills/productivity/psychology-learning-pipeline/scripts/verify_psy_plainname.py" "D:/Hermes Proj/psy/drafts/psy_4.txt" "D:/Hermes Proj/psy/threads_drafts/psy_4_thread.txt"
   ```
3. **`execute_code` bị chặn trong cron** (`BLOCKED: approvals.cron_mode`) — gặp lại, đúng như skill đã ghi. Đường đi dùng được: `write_file` ra file `.py` (nếu buộc phải script) rồi `terminal python <path>`, hoặc gọi thẳng script có sẵn.
4. **"bạn" dạng danh từ**: "bạn cấp ba" bị gate `\bbạn\b` bắt → đổi thành "cậu học cùng cấp ba". Viết tránh token ngay từ bản đầu.
5. File `drafts/psy_4.txt` và `threads_drafts/psy_4_thread.txt` bị job song song đụng (write_file báo "modified by sibling subagent"): coi bản trên disk là bản chốt, đọc lại trước khi dán vào chat.

## Kỹ thuật đã dùng (giữ lại)

- `write_file` trên Windows ghi CRLF; trước khi `split('\n\n')` phải `.replace('\r\n','\n')` (script chuẩn tự lo, checker tay thì không).
- Ngân sách viết-thẳng-đạt-luôn cho slot này: Ví dụ ~70 từ, Nêu vấn đề ~75, Gốc rễ ~80, First principle ~100 (mỗi cơ chế = tác giả + năm + 1 mệnh đề), Giải pháp ~105, 5 nhãn ~11 → ~445. Thread: chia 3 post, **post mang cơ chế là post hay vượt nhất** (lượt này 496), phân bổ ≤490 ngay từ bản đầu.
- Đổi ngách khi chủ đề đã có bản cũ: xem bảng trong `references/topic-mechanism-swaps.md` (lượt này dùng Festinger 1954 + Takahashi 2009 + Dickerson & Kemeny 2004 + Sapolsky).

## Nợ cần trả ở lượt sau

- Chưa grep/đọc bản cũ `drafts/review/psy_2_20260928_so-sanh-xa-hoi-va-cai-bay-so-bi.txt` → chưa chắc không trùng ngách.
- 4 tác giả của lượt này CHƯA verify Crossref/PubMed.
