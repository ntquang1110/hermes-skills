# Google Docs API — Pitfall khi tạo tài liệu trực tiếp qua API

Ba lỗi này làm hỏng 3 lần thử tạo tài liệu (verify 10/2026). Ghi lại để khỏi lần sau lại mò.

> ⚠️ Skill `google-workspace` là **bundled** — không patch được. Các bài học này nằm đây.

## 1. Không set được chiều rộng bảng

`updateTableColumnProperties` bị Google từ chối ở **mọi** giá trị `unit` đã thử:

```
400 Invalid value at 'requests[N].update_table_column_properties
    .table_column_properties.width.unit' (google.apps.docs.v1.Unit), "EMU"
400 Invalid value at 'requests[N].update_table_column_properties
    .table_column_properties.width_type'
    (google.apps.docs.v1.TableColumnProperties.WidthType), "DIA"
```

**Cách xử lý:** bỏ hẳn việc set chiều rộng bảng. `insertTable` với width mặc định hiển thị bình thường. Đừng mất 4 lần thử.

```python
# KHÔNG LÀM
fill.append({'updateTableColumnProperties': {
    'tableStartLocation': {'index': tstart}, 'columnIndices': [ci],
    'tableColumnProperties': {'width': {'magnitude': w, 'unit': 'EMU'},
                              'widthType': 'DIA'},
    'fields': 'width,widthType'}})  # → 400
```

## 2. Quota 60 write request / phút

```
429 Quota exceeded for quota metric 'Quota group for write operations'
    and limit 'Quota group for write operations per minute per user'
    ... WriteRequestsPerMinutePerUser
```

Mỗi `insertText` nếu gọi `batchUpdate` riêng = 1 write request. Tài liệu 60 đoạn = 60 request = chạm quota ngay, chưa kể các request cho bảng và định dạng.

**Cách xử lý:** đếm số write request ước tính **trước khi chạy**. Gộp text thành ít chunk nhất, mỗi chunk ≤ 40 request. Buffer thay vì gọi API mỗi đoạn:

```python
class _Doc:
    def __init__(self):
        self.buf = []
        self.pos = None   # index chèn kế tiếp, tự track

    def _derive_pos(self):
        cur = _retry(docs.documents().get(documentId=doc_id))
        self.pos = cur['body']['content'][-1]['endIndex'] - 1

    def add_text(self, text):
        if self.pos is None:
            self._derive_pos()
        self.buf.append((self.pos, text))
        self.pos += len(text)      # tự track, KHÔNG cần GET mỗi lần

    def flush(self):
        if not self.buf:
            return
        reqs = [{'insertText': {'location': {'index': i}, 'text': t}} for i, t in self.buf]
        self.buf = []
        for k in range(0, len(reqs), 40):      # mỗi batch ≤ 40 request
            _retry(docs.documents().batchUpdate(
                documentId=doc_id, body={'requests': reqs[k:k + 40]}))
        self.pos = None          # buộc derive lại sau mỗi flush
```

Chỉ `flush()` khi gặp `insertTable` (bảng làm thay đổi index) hoặc ở cuối `body_builder`.

## 3. ConnectionResetError không được retry

```
ConnectionResetError: [WinError 10054] An existing connection was
forcibly closed by the remote host
```

`googleapiclient` có retry nội bộ, nhưng nó cạn rồi vẫn **raise**. Retry chỉ bắt `HttpError 429` thì bỏ sót lỗi mạng này.

**Cách xử lý:** bọc `req.execute()` bằng retry bắt cả `Exception`:

```python
def _retry(req, tries=8, base=15):
    from googleapiclient.errors import HttpError
    for i in range(tries):
        try:
            return req.execute()
        except HttpError as e:
            if getattr(e.resp, 'status', None) == 429 and i < tries - 1:
                time.sleep(base * (i + 1)); continue   # 429: chờ đủ phút
            raise
        except Exception:
            if i < tries - 1:
                time.sleep(base * (i + 1) / 2); continue  # lỗi mạng: chờ ngắn hơn
            raise
    return None
```

Sau khi sửa quota bằng cách gộp, mỗi `sleep` chỉ cỡ 15-45 giây thay vì 120 giây.

## 4. `replaceAllText` sửa lỗi trên tài liệu đã tạo

Khi phát hiện sai sót trong doc đã tạo (sai số, sai dấu câu), dùng `replaceAllText` thay vì tạo lại:

```python
docs.documents().batchUpdate(documentId=doc_id, body={'requests': [
    {'replaceAllText': {'containsText': {'text': 'cũ', 'matchCase': True},
                        'replaceText': 'mới'}}
]}).execute()
```

Một request sửa **hết** các chỗ khớp trong cả tài liệu.

⚠️ Chú ý thứ tự: `replaceAllText` thay mọi chỗ khớp. Chuỗi ngắn như `"71.429"` có thể nằm trong chuỗi dài hơn `"1.671.429"` → dùng chuỗi đủ dài để khớp duy nhất.

## 5. Thứ tự build tài liệu có bảng

```
1. create document                          → 1 request
2. buffer text, flush (≤40 req/batch)       → 1 GET + nhiều batchUpdate
3. insertTable                              → 1 GET (lấy index) + 1 batchUpdate
4. fill cells bảng đó                      → 1 GET (tìm table) + nhiều batchUpdate
5. lặp lại 2-4 cho mỗi bảng
6. flush text còn lại
7. GET + style pass (updateTextStyle/updateParagraphStyle)  → 1 GET + 1 batchUpdate
8. drive.permissions().create (share writer) → 1 request
```

Sau mỗi `insertTable` phải **GET lại** document vì index bị thay đổi. Đừng tự track index qua bảng.

Fill cell bảng: mỗi cell có paragraph đầu tiên, lấy `startIndex` của nó rồi `insertText` vào đó. Header row (`ri == 0`) thêm `updateTextStyle` bold.

## 6. Verify sau khi tạo

Không tin kết quả khi chưa đọc lại:

```python
doc = docs.documents().get(documentId=doc_id).execute()
paras  = sum(1 for e in doc['body']['content'] if 'paragraph' in e)
tables = sum(1 for e in doc['body']['content'] if 'table' in e)
```

Kiểm tra thêm các dòng bold/center nếu có pass định dạng. Và đọc lại **nội dung** các dòng quan trọng — lần tạo đầu có thể sinh bảng nhưng chữ trong bảng trống, hoặc sinh số liệu sai.

## 7. Windows + python

`sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')` ở đầu script để in tiếng Việt không lỗi. Nhưng nếu `exec()` một module có dòng này thì nó **đóng stdout của session hiện tại** → `ValueError: I/O operation on closed file`. Khi test riêng phần hàm, copy hàm ra thay vì `exec` cả file.

Dùng `PYTHONUTF8=1` khi chạy qua `terminal` trên Windows.
