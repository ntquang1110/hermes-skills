# Merge pattern: nhiều agent HTML → 1 file multi-tab (proven 14/09/2026)

Khi dispatch N subagent viết N brief HTML riêng (mỗi agent 1 file), sau đó ghép thành 1 file multi-tab:

## Quy trình

1. **Mỗi agent ghi file riêng**: `brief-sow-agent.html`, `brief-asf-agent.html`, `brief-grow-agent.html` (path Windows native `C:/...`, không dùng MSYS `/c/...`).
2. **Extract body**: regex lấy nội dung trong `<div class="wrap">...</div>` (hoặc `<body>...</body>` fallback). Không lấy `<head>/<style>` của agent.
3. **Strip style blocks lạ**: agent HTML có thể chứa `<style>` riêng xung đột với template CSS → `re.sub` xóa style blocks trong body trước khi ghép.
4. **Template master**: 1 file HTML với CSS B/W/Y + Google Sans + JS `switchTab`, các placeholder `{{SOW_CONTENT}}`, `{{ASF_CONTENT}}`... trong từng `<div id="tab-x" class="tab-content">`.
5. **Merge script python**: đọc template + từng body, replace placeholder, ghi file cuối. In số chars mỗi phần để bắt lỗi 0-content trước khi publish.
6. **Publish + verify**: upload qua `publish` skill (KV), verify bằng curl `grep -c` các keyword chính (số hits > 0) thay vì browser khi Camofox treo.

## Pitfalls đã gặp

- Agent ghi file nhưng main session đọc quá sớm → file chưa tồn tại. Chờ delegate result re-enter (không poll liên tục), check file size > 0 trước khi merge.
- Body quá lớn (~60-70K chars/agent): tổng file cuối ~230K chars — vẫn publish KV OK (<1MB).
- Verify browser fail khi Camofox 500 (tab accumulation) → fallback: `curl | grep -c` keyword. Đừng retry browser_navigate liên tục (loop warning).
