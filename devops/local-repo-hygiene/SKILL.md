---
name: local-repo-hygiene
description: Triage git clones for cleanup; package a repo to publish private.
---

# Local Repo Hygiene

When the user asks "which repos can I delete to free disk space" (or "các repo nên xóa đi để tiết kiệm dung lượng"), the goal is to separate **active repo/current work** from **disposable research clones** (repos cloned to read a technique and already absorbed into a skill or abandoned), then propose deletion for review **before** `rm -rf`.

Trigger: "xóa repo", "free disk", "tiết kiệm dung lượng", "which repos to delete", cleaning up git clones.

## Workflow (validated 08/2026)
1. **List `.git` dirs first — do NOT `du` the whole drive.** `find /d -maxdepth 3 -type d -name ".git" | sed 's/\/.git//'` returns instantly. `du -sh` over an entire drive times out (180s+) because it walks everything. List first, then size individually.
2. **Size + last-modified per repo** (one loop, avoid re-scanning the tree):
   `du -sh "$r"` + `stat -c '%y' "$r"` (last-modified of the dir).
3. **Classify each repo.** Two buckets:
   - **ACTIVE / keep:** repo backing a running service or current work — e.g. `volden-ops-web`, `ai-company`, `meTelligent`, `searxng`, `camofox-browser`, `knowledge-flow`, `theliems`. Do not touch without explicit instruction.
   - **DISPOSABLE research clone:** cloned to read/absorb a technique. Confirm by checking whether its knowledge already lives in a Hermes skill (e.g. `impeccable`, `diagram-design`, `unslop`/`html-unslop` were absorbed into skills of the same name → the source clone is dead weight). Check `README.md` head + last-modified to confirm it's a research artifact, not work.
4. **Present a table** — size | last-modified | *why* it's disposable (which skill absorbed it, or it's a `*_tmp` / review clone). Reclaim figure on the relevant drive.
5. **Get explicit approval before deleting.** This is destructive; Quang's rule is propose → "duyệt" → execute. Confirm the disk-health context: check `df -h /c /d` and report which drive is actually the bottleneck before selling a specific reclaim target.
6. **Delete + verify every path** is gone (`[ -e "$r" ] && echo CÒN || echo gone`).

## Đóng gói repo để publish private lên GitHub (validated 10/2026, dự án fixgby)

Trigger: *"dự án này đã thành repo hoàn chỉnh để publish lên GitHub chưa"*, *"publish private cho anh"*, *"repo đã sạch chưa"*.

**Định nghĩa "hoàn chỉnh" = clone sạch ra thư mục khác rồi build lại ra ĐÚNG kết quả.** `git status` sạch KHÔNG chứng minh được gì. Bước 5 là bước bắt buộc — không có nó thì không được nói "hoàn chỉnh".

1. **Quét nền repo trước**: số file track, top 10 file lớn nhất, tổng dung lượng. Quét secret: `ghp_|github_pat_|sk-|AIza|xox[bp]-|-----BEGIN|service_role|password\s*=|token\s*=`. Nếu repo đã có `.git` + lịch sử commit thì phần "tạo repo" xong rồi, chỉ còn remote.
2. **Tìm file INPUT bị `.gitignore` chặn — lỗi chết người của lớp này.** Script đọc `data/*.json` nhưng `.gitignore` có `data/*` thì clone về build ra **trang trắng** mà log không báo lỗi. Cách tìm: lấy mọi chuỗi tên file (`xxx.json`, `xxx.txt`) trong các script đang track rồi đối chiếu `git ls-files`. Vá bằng whitelist: `data/*` + `!data/diem-neo.json` (mỗi file một dòng `!`), rồi `git add -A`.
3. **Không để file mồ côi**: output (`*.html`) đã track thì script sinh ra nó + dữ liệu sinh (`_duong-cong.json`) cũng phải track. Ngược lại, script scratch không sinh ra gì thì ignore/đưa về đúng hộ (`docs/<vòng>/`), đừng để ở gốc repo.
4. **Thêm `.gitattributes`** (`* text=auto` + `*.json text eol=lf`) — repo Windows hay CRLF, tránh diff giả.
5. **Bằng chứng bắt buộc — clone sạch rồi build lại, và so hash chứ đừng so mắt**:
   ```bash
   git clone <repo> ../_clonetest && cd ../_clonetest
   python <build-1>.py && python <build-2>.py   # chạy MỌI script sinh output
   sha256sum <output>.html                      # so với bản gốc: phải TRÙNG
   ```
   Chạy lại script lần 2 trong clone → hash phải y hệt (kiểm tính tất định; khác nhau là script có phần tử ngẫu nhiên/thời gian).
   **Và kiểm repo gốc sau khi chạy script trong clone: `git status --short` phải RỖNG.** Đây là phép thử bắt lỗi nặng nhất — xem mục 5b. So số in ra (KPI, số dòng) là chưa đủ: script có đường dẫn tuyệt đối vẫn in số y hệt trong khi ghi nhầm vào repo gốc.
5b. **Quét đường dẫn tuyệt đối trong mọi script đang track** — lỗi im lặng, tệ hơn file rác:
   ```bash
   grep -rn 'D:/Hermes\|C:/Users\|/home/' --include=*.py .   # hoặc quét bằng python
   ```
   Script hardcode `D:/Proj/x/docs/...` thì clone về máy khác **không hỏng ngay** mà ghi ngược vào repo gốc (đã gặp: `_gen-lieu-san.py` sửa file trong repo gốc lúc 13:09 khi đang chạy trong bản clone). Vá: `os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", ...)`. Chú ý `dirname(__file__)` là thư mục chứa script, đừng `dirname()` thêm lần nữa. Vá xong chạy lại 5 để chứng minh.
6. **Push private — dùng TOKEN có sẵn, ĐỪNG mở trình duyệt.** Quang chốt 20/10/2026: *"Sao k dùng api đi, vào trình duyệt làm gì"*. Device flow (`gh auth login --web`) bắt user mở URL + nhập mã — chỉ dùng khi máy **thật sự không có** token nào. Thứ tự:
   1. Tìm token: `$GITHUB_TOKEN`/`$GH_TOKEN` → `~/AppData/Local/hermes/.env` (Windows; Linux/mac: `~/.hermes/.env`) khoá `GITHUB_TOKEN` / `GITHUB_PAT_B64` (base64) → `~/.config/gh/hosts.yml` → `~/.git-credentials`.
   2. Kiểm token sống + scope: `GET https://api.github.com/user` (đọc `x-oauth-scopes`); cần scope `repo` để tạo repo private.
   3. Nạp **không tương tác**, token đi qua **stdin** (không để lộ trong argv/log):
      ```python
      import base64, io, subprocess
      # đọc .env -> env{}
      tok = base64.b64decode(env["GITHUB_PAT_B64"]).decode()
      subprocess.run(["gh","auth","login","--hostname","github.com","--with-token"], input=tok, text=True)
      subprocess.run(["gh","auth","setup-git"])   # git dùng credential helper của gh
      ```
   4. Tạo + push: `gh repo create <name> --private --source=. --push` (hoặc `POST /user/repos {"private":true}` qua API rồi `git push origin HEAD:main`).
   5. **Verify bằng API, không mở trình duyệt**: `GET /repos/<o>/<r>` → `private=true`, `default_branch`; `GET /repos/<o>/<r>/commits/main` → sha phải **trùng `git rev-parse HEAD`**; `GET /repos/<o>/<r>/git/trees/main?recursive=1` → đếm blob + xác nhận các file data trọng yếu có mặt.
   6. Dọn link clone test sau khi xong (`rm -rf ../_clonetest`).

Chi tiết dự án fixgby (số chốt, whitelist data, preview slug): `skill_view('fixgby', 'references/repo-publish-va-so-chot.md')`.
Probe tự động: `scripts/check-repo-ready.py` (liệt kê file lớn, quét secret, tìm input bị ignore, đếm file track).
Bằng chứng "clone về chạy được": `scripts/verify-clone-build.py` — clone ra thư mục tạm, chạy mọi lệnh build, so sha256 với bản gốc, kiểm tính tất định (`--twice`), và **bắt buộc repo gốc còn `git status` sạch** (đây là phép thử bắt lỗi đường dẫn tuyệt đối). Chạy nó trước khi dám nói "repo hoàn chỉnh":
```bash
python scripts/verify-clone-build.py --repo "D:/Proj/x" --clone "D:/Proj/_clonetest" \
  --cmd "python visual/build-a.py" --artifact visual/a.html --twice
```

## Pitfalls
- **Push bằng URL có token thì git lưu token vào `.git/config`** — không chỉ `remote.origin.url` mà cả `branch.<tên>.remote`. Lần push kèm token xong phải dọn ngay trong cùng lượt:
  ```bash
  git remote set-url origin https://github.com/<o>/<r>.git
  git config branch.<tên>.remote origin
  grep -c 'ghp_\|github_pat_' .git/config    # phải ra 0
  ```
  Cách sạch hơn: nạp token một lần qua `gh auth login --with-token` + `gh auth setup-git` rồi để credential helper lo phần còn lại, không nhét token vào URL nào.
- **URL remote sạch (không token) + chưa có credential helper = `git fetch`/`git clone` treo im lặng**, không in gì, chờ prompt username vô hình (đã bị kill ở mốc 300s). Nạp credential helper TRƯỚC lệnh git mạng đầu tiên; nếu buộc phải chạy trước thì thêm `GIT_TERMINAL_PROMPT=0` để nó fail nhanh thay vì treo.
- **Có thể có session Hermes khác đang ghi vào cùng repo giữa lượt của mình.** Dấu hiệu: file `mtime` mới hơn commit HEAD, `git status` đổi giữa hai lệnh liên tiếp, file tự "mới hơn" bản vừa commit. Cách xử: `git status` + `git log` lại ngay trước mỗi lần commit; phần việc của session kia thì commit thành **commit riêng** có ghi chú, đừng cố dọn/hoàn tác nó, và báo user biết để họ tắt session thừa.
- **Đừng đọc số từ payload đã bị cắt.** Từng báo "119 điểm giao" vì đọc `len(giao[:160])` trong khi KPI thật là **52** (số điểm bị ≥2 chất chạm). Số để báo cáo/đưa vào README phải lấy từ biến đếm thật hoặc giá trị KPI đã render, không lấy từ list bị `[:N]`.
- **README là thứ đầu tiên phải đọc khi bàn giao.** README còn ghi "chưa code" trong khi repo đã 170+ file, docs 00→14 — stale README làm câu trả lời "chưa hoàn chỉnh" thành sai hướng. Viết lại README theo số đếm được từ dữ liệu, kèm lệnh build và mục "chưa xong".
- **Trên Windows, `subprocess(..., shell=True)` chạy qua `cmd.exe`** nên `git ls-files | grep ...` trả về **RỖNG kèm lỗi bị che** — dễ kết luận sai "không thiếu gì". Dùng `subprocess.run(["git", "ls-files"], cwd=R)` (list args) hoặc `["bash","-lc", ...]`.
- **Sau khi `mv`/`cp` đổi tên file, đọc lại file trước khi patch.** Đã từng `patch` thành công 1 dòng argparse nhưng thân hàm vẫn gọi tên cũ (`a.j`) → lỗi chỉ lộ ra khi chạy. Sửa xong phải **chạy thật** tool/script, không dừng ở "lint ok".
- **Vá README/skill theo số cũ là rủi ro kép**: mỗi lần số liệu đổi phải grep toàn repo tìm số cũ (`grep -rn "<số cũ>" docs visual README.md`) để không còn 2 nguồn số khác nhau.
- **A D: free-space win is not a C: fix.** On Quang's box C: sits ~93% (the real bottleneck); research clones often live on D: which has room. Deleting D: clones is hygiene, not a drive rescue — say so plainly, and point at the true C: space hogs (large `node_modules`, dormant projects on C:) separately.
- **Don't mistake an active service repo for a clone.** Check what it actually fronts (a port, a tunnel, a running daemon) before listing it as disposable. `camofox-browser` looks optional but is the active browser tool.
- Never delete the `.venv`, `node_modules`, or runtime logs of a kept project while proposing to "clean clones" — stay scoped to the git-clone inventory.
- After the work is accepted, cleanup after yourself: a research clone kept on disk for reference should be flagged ([gbrain-tmp] was kept briefly then removed).

## Relation to other skills
- `company-brain-design` covers the GBrain/company-brain deep-dive this session produced (different class — memory-layer design, not disk triage).
- Overlapping skill noted for the curator: `ai-company`, `ai-company-ops`, `ai-company-system`, `multi-agent-company` all describe overlapping facets of the same AI-company system and are likely consolidation candidates.