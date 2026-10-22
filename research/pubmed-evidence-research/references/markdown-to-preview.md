# Publish bài nghiên cứu → link preview.thefirstonly.com (không phải gist)

Người dùng (Quang) KHÔNG dùng link gist. Cứ publish bài nghiên cứu xong: ra link **preview.thefirstonly.com**, verify HTTP 200 trước khi báo xong.

## Quy tắc quan trọng nhất: preview worker CHỈ serve file tên `index.html`

Worker `preview.thefirstonly.com/<gist_id>` fetch `gistusercontent.com/.../raw/index.html`. Bất kỳ tên file nào khác (`.md`, `.txt`) đều trả **HTTP 404**:
```
404 — Not found. https://gist.githubusercontent.com/.../raw/index.html
```

→ Muốn nội dung `markdown` hiện trên preview.thefirstonly.com, phải **convert markdown → HTML** rồi upload với `--name index.html`.

## Các bước (script `content-upload.py` nhận `--name` để ép tên file)

```bash
# 1. Convert markdown -> HTML (lib `markdown` có sẵn trong venv)
python -c "import markdown; print(markdown.markdown(open('doc.md',encoding='utf-8').read()))"
# wrap body trong trang HTML có <meta charset="utf-8"> + <title> + CSS

# 2. Upload với --name index.html (bắt buộc, không để auto-detect ra .md/.txt)
python content-upload.py --file out.html --title "Tiêu đề" --name index.html
# -> preview_url = https://preview.thefirstonly.com/<gist_id>
```

## Verify
- `curl -s -o pv2.txt -w "HTTP %{http_code}" "https://preview.thefirstonly.com/<gist_id>"` phải trả 200, nội dung HTML đúng title.
- Gist vừa tạo đôi khi chậm replicate → wait ~5s rồi retry 1 lần trước khi kết luận 404.

## Vì sao NOT nên dùng các đường khác
- Auto-detect markdown → `document.md` → script trả `gist_url` (github.com) — đúng cái user không dùng.
- `--name document.txt` → vẫn 404 vì worker chỉ fetch `raw/index.html`.
- Đính gist URL vào reply = sai chuẩn, user phải nhắc lại.

## Ghi chú triển khai
- Quy tắc publish nằm ở mục `## Publish rule` của `pubmed-evidence-research` SKILL.md (đã patch). Ấn định: publish bằng skill content-publish → link preview.thefirstonly.com; không tự ý đăng Threads (research lệch 3 kênh tâm lý/macro/podcast).
- File `content-publish/scripts/content-upload.py` là user-owned — không tự patch được; chỉ dùng qua `--name`.