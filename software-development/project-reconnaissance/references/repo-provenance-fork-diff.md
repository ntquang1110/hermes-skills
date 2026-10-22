# Vetting nguồn gốc một repo trước khi tin nó

Dùng khi user đưa một repo/paper và hỏi kiểu *"check cái này trên GitHub xem có không, tải source về review"*,
*"code này của ai?"*, *"nó có thật không?"*, *"phân tích source này cho anh"*.

Khác với `external-framework-evaluation.md` (đánh giá **có nên adopt** không). File này là về **nguồn gốc
và độ tin**: bài toán ở đây là tách phần *nguyên bản* khỏi phần *thêm vào*, và chứng minh repo **chạy được
thật** thay vì chỉ đọc README.

Worked example: **PaperBanana** (`dwzhu-pku/PaperBanana`) vs `google-research/papervizagent`, 2026-10-21.

## Quy trình 6 bước

### 1. Xác minh sự tồn tại — cả paper VÀ repo

```bash
curl -s --max-time 20 https://api.github.com/repos/<owner>/<repo> | python -c "
import sys,json; d=json.load(sys.stdin)
for k in ['full_name','description','stargazers_count','forks_count','open_issues_count','created_at','pushed_at','license','size']:
    print(f'  {k}: {d.get(k)}')"
```

Paper thì lấy từ arXiv (abstract + HTML v2). **Repo có thật mà paper không có, hoặc ngược lại, đều là dấu hiệu.**

### 2. So `created_at` — thứ tự thời gian hay tiết lộ sự thật

PaperBanana tạo **30/01/2026**; repo Google `google-research/papervizagent` tạo **11/02/2026** — tức là
*bản "gốc" ra sau*. Nhưng README của PaperBanana lại viết *"The original version is already open-sourced
under Google-Research as PaperVizAgent. This repository forked the content of that repo."*
→ Không phải fork theo nghĩa GitHub. Đọc kỹ README phần provenance, đối chiếu với timestamp.

### 3. Diff với upstream — bước quyết định

Tải file chủ chốt của upstream rồi diff với bản local. **Đừng so kích thước file, so nội dung.**

```bash
mkdir -p /tmp/cmp && cd /tmp/cmp
for f in agents/retriever_agent.py agents/critic_agent.py utils/generation_utils.py prompts/diagram_eval_prompts.py; do
  out=$(echo "$f" | tr '/' '_')
  curl -s --max-time 25 "https://raw.githubusercontent.com/<upstream>/main/$f" -o "g_$out"
  loc=./<repo>/"$f"
  [ -s "g_$out" ] && [ -s "$loc" ] && echo "$f: $(diff <(tr -d '\r' <"g_$out") <(tr -d '\r' <"$loc") | grep -cE '^[<>]') dong khac"
done
```

Kết quả PaperBanana:

| File | Số dòng khác | Kết luận |
|---|---|---|
| `prompts/diagram_eval_prompts.py` | **0** | y nguyên của Google |
| `agents/retriever_agent.py` | 4 | chỉ đổi `model_name` → `main_model_name`, `call_gemini_with_retry_async` → `call_model_with_retry_async` |
| `agents/critic_agent.py` | 4 | cùng pattern |
| `utils/generation_utils.py` | 464 → 1189 dòng | **đây là toàn bộ giá trị gia tăng** (lớp provider) |

⚠️ **Cùng số dòng KHÔNG có nghĩa giống nhau** — 339 vs 339 dòng vẫn khác 4 dòng. Luôn phải diff nội dung.

Dấu hiệu "fork chưa rename hết": docstring `main.py` vẫn ghi `PaperVizAgent`, config template vẫn ghi
`Model and API Configuration for PaperVizAgent`.

### 4. Chạy thật — test suite là bằng chứng rẻ nhất

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv -q -r requirements.txt pytest
unset PYTHONPATH && unset PYTHONHOME        # BẮT BUỘC, xem pitfall bên dưới
.venv/Scripts/python.exe -m pytest tests/ -q -p no:cacheprovider
```

PaperBanana: **135 passed, 21 subtests, 25,9s**. Rồi kiểm CLI/import:
`.venv/Scripts/python.exe main.py --help` và `python -c "import agents, utils, prompts"`.

**Nói rõ mình CHƯA chạy gì.** Với repo cần API key để sinh output (ảnh, audio, model call), test pass chỉ
chứng minh *mã chạy*, KHÔNG chứng minh *chất lượng output*. Phải tuyên bố đúng mức đó — đừng để user hiểu
là đã kiểm chất lượng.

### 5. Quét bảo mật — 4 thứ, theo thứ tự

```bash
# (a) key lộ trong code
grep -rnE "(AIza[0-9A-Za-z_-]{30,}|sk-[A-Za-z0-9]{20,}|hf_[A-Za-z0-9]{30,})" --include="*.py" --include="*.yaml" . | grep -v "example\|xxxx\|your_"
# (b) file secret bị commit
git ls-files | grep -iE "\.env|secret|credential|token"
# (c) .gitignore có che config thật?
cat .gitignore
# (d) thực thi code không sandbox
grep -rnE "\b(eval|exec)\s*\(|os\.system|subprocess\.(call|run|Popen)" --include="*.py" . | grep -v "test_"
```

PaperBanana: (a)(b) sạch, (c) tốt. (d) tìm ra `utils/plot_execution.py:49`:
```python
exec_globals = {}
exec(code_clean, exec_globals)   # code do LLM sinh, không sandbox
```
Ghép với `Dockerfile`: `python:3.12-slim` chạy **root**, `EXPOSE 8080`, `chmod -R 777 data`.
→ Kết luận đúng phải nêu **điều kiện**: self-host công khai ra internet thì prompt injection dẫn tới chạy
lệnh trên máy chủ. Docstring tự nhận *"executed in the caller's isolated worker"* nhưng **hàm này không
cô lập gì** — đừng tin docstring tự khen.

### 6. Rút ràng buộc thực tế (phần user cần nhất)

Đọc code để tìm **cái chặn dùng thật**, không chỉ tính năng. Vd đếm prefix provider và tìm chỗ raise:

```bash
grep -oE "\"(openrouter|orcarouter|atlas|local|ollama|gemini)/" utils/generation_utils.py | sort | uniq -c
grep -nE "local/|ollama/|text-only|raise" utils/generation_utils.py
```

PaperBanana: `_LOCAL_TEXT_PREFIXES = ("local/", "ollama/")` và dòng 91 raise
*"local/ and ollama/ prefixes are text-only and cannot be used for {route_name}"*.
→ Ràng buộc thật: Planner/Critic/Retriever/Stylist chạy được trên model local, nhưng **sinh ảnh bắt buộc
Gemini hoặc OpenRouter**. Nghĩa là có chi phí API không tránh được. Đây là thông tin quyết định.

## Kiểm chứng bài viết/claim NÓI VỀ repo hoặc paper

Khi user đưa một bài viết về paper/repo (thường có hashtag, dạng đăng mạng xã hội), kiểm 6 thứ:

1. **Số có khớp nguồn không.** PaperBanana: bài viết ghi *"bộ đánh giá gồm 292 ví dụ"* nhưng benchmark là
   **584 case** (292 test + 292 reference) → sai một nửa.
2. **Có link nguồn không.** Bài về paper mà không có arXiv ID = không kiểm chứng được.
3. **Có số nào không.** Paper có 5 số (faithfulness +2,8%, aesthetics +6,6%, readability +12,9%, overall
   +17,0%, conciseness **+37,2%**) mà bài viết không nêu số nào → bỏ phí hook mạnh nhất.
4. **Ai làm.** Tổ chức + số tác giả là tín hiệu tin cậy, thiếu là tự làm yếu bài.
5. **Open source / giấy phép.** PaperBanana: Apache-2.0, 7,3k sao, có demo HuggingFace Spaces — bỏ sót là
   bỏ mất giá trị thực dụng lớn nhất.
6. **Cảnh báo pháp lý.** Repo ghi rõ: **Google đã nộp patent**, không cho dùng thương mại, không phải sản
   phẩm Google hỗ trợ chính thức. Ai định dùng cho sản phẩm phải biết trước khi đầu tư.

## Mẫu báo cáo

1. **Có thật / đang sống không** — sao, fork, ngày push cuối, license, ai làm.
2. **Bản chất: mã của ai** — bảng diff với upstream. Đây là phần "phát hiện quan trọng nhất".
3. **Đã chạy thật gì** — test pass bao nhiêu, CLI/import OK, và **rõ ràng cái CHƯA chạy**.
4. **Bảo mật** — lỗ thật + điều kiện kích hoạt, không phóng đại.
5. **Ràng buộc thực tế** — chi phí, thứ bắt buộc phải trả tiền, cái gì local được.
6. **Sức khỏe dự án** — nhịp commit, số issue mở, thành phần contributor.
7. **Kết + đề xuất bước tiếp theo cụ thể** (vd "đưa key thì em chạy end-to-end").

## Pitfalls

| Vấn đề | Cách xử lý |
|---|---|
| `pytest` fail hàng loạt `ModuleNotFoundError: pydantic_core._pydantic_core` | `PYTHONPATH` từ venv Hermes rò vào venv của repo. `unset PYTHONPATH && unset PYTHONHOME` trước khi chạy |
| `diff` báo khác nhưng nhìn không thấy khác | khác line-ending CRLF/LF. Diff qua `tr -d '\r'` như ví dụ trên |
| Chỉ so kích thước/số dòng file | Vô nghĩa — cùng số dòng vẫn khác ruột. Luôn diff nội dung |
| `search_files` (ripgrep) báo *"cannot find the path specified"* trên thư mục clone sâu | dùng `grep`/`grep -r` qua `terminal` cho các đường dẫn này |
| Tool `terminal` báo `open: embedded null character in path` khi lệnh chứa `.venv/Scripts/python.exe` | lách bằng biến shell: `P=".venv/Scripts/python.exe" && $P script.py` |
| Repo không kèm dataset/weights | Đọc `.gitignore`; nói rõ phải tải riêng ở đâu, và mất chế độ nào nếu thiếu (PaperBanana: mất few-shot của Retriever) |
| Đọc số sao/commit từ trang GitHub HTML | Dùng API (`/repos/...`, `/commits?per_page=10`, `/contributors`) — đọc được ngày, thành phần đóng góp, tỉ lệ bot |
