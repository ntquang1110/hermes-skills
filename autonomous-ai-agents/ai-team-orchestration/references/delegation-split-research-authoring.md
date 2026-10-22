# Phân tách thu thập dữ liệu khỏi viết deliverable khi delegate

Bài học từ batch 01/10/2026: 3 subagent song song, mỗi agent một nhóm hợp chất (Alkaloid, Terpenoid, Saponin), goal dạng *"research toàn diện 7 mục → build HTML → publish lên preview.thefirstonly.com"*.

## Kết quả quan sát

| Agent | Goal | API calls | Thời gian | Kết quả |
|---|---|---|---|---|
| Alkaloid | Nghiên cứu + build + publish | 39 | 1290 s | **Bị ngắt** — `waiting for model response (477.3s)` |
| Saponin | Nghiên cứu + build + publish | 50 | 1630 s | Thành công |
| Terpenoid | Nghiên cứu + build + publish | 46 | 1911 s | **Bị ngắt** — `waiting for model response (474.9s)` |
| Alkaloid (re-dispatch) | **Chỉ build HTML từ data trên disk** | 50 | 792 s | Thành công |
| Terpenoid (re-dispatch) | **Chỉ build HTML từ data trên disk** | 35 | 683 s | Thành công |

1/3 goal đầy đủ chạy tới nơi. 2/2 goal hẹp re-dispatch chạy tới nơi.

## Nguyên nhân

Không phải agent hỏng. Trong cả hai case bị ngắt, **subagent đã thu thập xong hết dữ liệu** (PubMed 50-60 query + PubChem 20-52 CID) và **đang ở khâu build/publish thì model API không trả lời kịp** (477 s / 474 s chờ). Progress nằm hết trong background processes (đã hoàn tất, dữ liệu đã ghi ra file `data/*.json`).

Khi re-dispatch, goal ghi rõ **"KHÔNG fetch thêm dữ liệu"** → agent bỏ toàn bộ bước research, đi thẳng tới viết HTML. Số round-trip giảm mạnh, agent tới được khâu authoring trước khi timeout.

## Luật nên áp dụng

**Khi goal bao gồm cả research + build + publish, tách làm hai agent:**

1. **Agent thu thập** — goal hẹp: chạy script, ghi JSON vào `data/`. Không yêu cầu viết HTML. Có thể chia thành nhiều batch nhỏ chạy song song.
2. **Agent viết** — goal: *"Đọc dữ liệu đã có tại `<path>`, build HTML, publish. KHÔNG fetch thêm dữ liệu."* Đường dẫn file phải nằm trong goal.

**Khi đã lỡ dispatch goal đầy đủ và bị ngắt:** đừng dispatch lại goal y hệt. Kiểm tra thư mục `data/` của agent đó (`ls -la "D:/Hermes Proj/<slug>-report/data/"`) — nếu đã có JSON thì dữ liệu vẫn nguyên, chỉ cần dispatch lại phần build.

## Lưu ý

- Cả hai lần re-dispatch vẫn chạy ~35-50 API calls. Agent viết HTML vẫn phải đọc file dữ liệu lớn. Nên data JSON phải **tổng hợp sẵn** (mỗi hợp chất 1 object) chứ không để thô 800 KB abstract.
- Script chạy nền của subagent (`terminal background=true, notify_on_complete=true`) **hoàn thành bình thường** kể cả khi agent bị ngắt. Đừng kill process nền khi re-dispatch.
- Đọc live transcript để chẩn đoán: `<hermes cache>/delegation/live/<delegation_id>/task-0.log` — `tail` 20 dòng cuối cho biết agent đang ở bước nào.

---

# Trần tool-call của con (`delegation.max_iterations`) — ca 19/10/2026

Batch 3 con, goal *"nghiên cứu 12 / 7 / 7 nguyên liệu theo khung 8 chặng, mỗi nguyên liệu ~14 KB bài viết, ghi `<batch>.md` + `<batch>.json`"*:

| Con | Nguyên liệu | api_calls | Kết quả |
|---|---|---|---|
| A | 12 | **50 (chạm trần)** | không có file deliverable nào; chỉ 5/12 file nguồn trung gian |
| B | 7 | **50 (chạm trần)** | không có file nào; nhưng đã tích đủ ~100 abstract ra `epmc_work/work1.json` |
| C | 7 (viết theo từng nguyên liệu) | 32 | **xong**, 2 file đủ |

Cả A và B đều tự khai *"hết lượt gọi tool giữa chừng"*. Đây **không phải** timeout, **không phải** provider hỏng — là trần cứng `delegation.max_iterations`.

## Chẩn đoán trong 1 lệnh

```bash
hermes config get delegation      # -> max_iterations: 50  (mặc định)
```

Nếu `max_iterations` ≤ 50 mà con phải vừa research vừa viết nhiều file → **chắc chắn chết giữa chừng**. Nâng trước khi dispatch:

```bash
hermes config set delegation.max_iterations 140
```

(`max_tool_calls: 50` trong section `code_execution` là của `execute_code`, KHÔNG phải của subagent — đừng nhầm hai con số.)

## Luật rút ra

1. **Ước lượng ngân sách theo khối lượng viết, không theo số đầu việc.** Một đầu việc cần ~20 calls nếu vừa tra vừa viết 14 KB. Trần 50 → **tối đa 2–3 đầu việc/con**. Chia 7 đầu việc cho 1 con là tự sát.
2. **Bắt con GHI FILE NGAY sau mỗi đầu việc**, không dồn về cuối. Câu lệnh trong goal: *"viết xong 1 nguyên liệu là GHI FILE NGAY bằng write_file, rồi mới nghiên cứu cái kế. TUYỆT ĐỐI không để tới cuối mới ghi. Nếu hết ngân sách, file đã xong phải nằm trên đĩa."* Con C làm đúng và sống sót; A và B dồn về cuối và mất trắng.
3. **Đừng để con tự viết file tổng hợp.** Cho con ghi **1 file nguồn/đầu việc** (`src/<slug>.txt`) theo một **file mẫu chuẩn phải đọc trước** (`ĐỌC src/thymol.txt LÀM MẪU CHUẨN TRƯỚC KHI VIẾT`), rồi **builder deterministic của parent** gộp thành deliverable. Chết giữa chừng vẫn còn nguyên phần đã xong, parent chạy lại builder là ra kết quả.
4. **Builder phải tham số hoá** (`python _build.py <srcdir> <batch>`) để nhiều con ghi vào các thư mục khác nhau (`src/`, `src-b/`) mà không giẫm nhau.
5. **Salvage trước khi dispatch lại** — đọc transcript + `ls` thư mục đích để biết con đã tích được gì. Ca này con B đã có ~100 abstract trong `work1.json`; dispatch lại chỉ cần *"đọc `work1.json`, viết file, ĐỪNG tra lại"*.

## Pitfall của chính parent: builder im lặng làm rơi dữ liệu

Khi parent viết builder gộp file nguồn → JSON cho tầng dưới, **phải kiểm builder có giữ đủ trường mà tầng dưới đọc**. Ca thật: builder chỉ ghi `{"chi_tiet": <mô tả chặng>, "pmid": [...]}` — **câu phát biểu gốc bị rơi mất**; tầng dưới (đồ thị node) đọc JSON đó và không có gì để trích → pipeline "chạy thành công" mà kết quả rỗng.

Phép kiểm tối thiểu sau khi sửa builder: mở output, in 1 mẫu trường thật và đếm phần tử, đừng tin là đã đủ.

```python
import json, io
j = json.load(io.open(".../_batch_a_raw.json", encoding="utf-8"))
c = j["chat"][0]
print(len(c["cua_vao"]["dong"]), c["cua_vao"]["dong"][0][:70])
```

Kiểm thêm: tên file output có đúng tên loader tầng dưới tìm không (ca này loader tìm `batch-<x>.json` nhưng builder chỉ ghi `_batch_<x>_raw.json` → cả batch không bao giờ vào được đồ thị).

