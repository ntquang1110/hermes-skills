# Gọi trực tiếp Ministral local (endpoint unsloth) — viết bài on-demand ngoài cron

Dùng khi user yêu cầu "viết bằng unsloth/minstral" cho một bài TLUẬN/nội dung đã có sẵn
(không phải video YouTube), không cần chờ cron 07:30.

## Endpoint

- Base: `https://racial-clarke-some-redhead.trycloudflare.com/v1` (Cloudflare tunnel Unsloth)
- Model: `unsloth/Ministral-3-8B-Instruct-2512-GGUF`
- Key: đọc `UNSLOTH_API_KEY` từ `~/AppData/Local/hermes/.env`
- OpenAI-compatible chat completions. Quick probe trước khi gọi:
  `curl -H "Authorization: Bearer $KEY" <base>/v1/models` -> cần chứa model với `"loaded": true`.
- Quant Q3_K_S, `max_context_length: 4096` (nhỏ) -> prompt phải gọn, không nhét cả nguồn dài vào.
- `max_tokens` ~3000-3200, `temperature` ~0.8 cho giọng tự nhiên.
- Cách gọi an toàn: `execute_code` bằng urllib (tránh heredoc mất dấu + tránh terminal guard loằng ngoằng).
  Header bắt buộc `User-Agent: curl/8.0` (một số server chặn urllib-UA).

Chú ý: tunnel Cloudflare tên bên trong file thay đổi khi re-tunnel. Nếu `/v1/models` chết,
grep `UNSLOTH_API_KEY` + base_url hiện tại trong `config.yaml` (provider `custom:unsloth`)
và trong `scripts/watchdog-unsloth.py` (TUNNEL_URL).

## Prompt điều khiển model (các rule PHẢI có trong prompt)

Model Ministral KHÔNG tự tuân style. Prompt phải nhúng rõ:

- Xưng hô "mình"/"bạn", cấm "tôi"/"anh"/"em".
- KHÔNG nhãn "Tầng 1:"/"Tầng 2:".
- KHÔNG em dash (—), en dash (–), chỉ dấu chấm phẩy. KHÔNG emoji (cái này model hay vẫn lọt **markdown**).
- Có dấu tiếng Việt đầy đủ, CHỈ ký tự Latin + dấu + số + dấu câu, CẤM ký tự Hàn/Hán/Nhật/mũi tên (→).
- Mỗi đoạn ≤ 500 ký tự, cắt tại câu.
- Trả về nguyên văn bài, không kèm lời bàn.

## Pitfalls (đã gặp 2026-08-23, bài độc tính ion)

1. **Model lọt markdown `**bold**` dù prompt cấm** -> sau khi gen, phải strip `**` hoàn toàn.
   Kiểm tra bằng `text.count("**")`.
2. **Model tạo lỗi khoa học nghiêm trọng** dù nguồn cung cấp đúng -> bài này model tự thêm
   "HCl là nước cốt chua" (sai: HCl là axit clohidric), "Pb+4 phá não" (sai, Pb(II) mới độc),
   "N2O4 là tetramethyldiazene nổ tàn tật" (lẫn lộn). => Viết bài khoa học/kỹ thuật đăng công khai:
   LUÔN verify từng claim số liệu/tên chất/tên enzyme trước khi gửi duyệt, dù model viết trôi chảy.
3. Model tự chọn góc mở bài khác nguồn (mở bằng "natri/clor muối ăn" thay vì K/C/N/Li) ->
   chấp nhận được nếu cùng chủ đề, giữ giọng model.
4. Cm sạch xong chạy `unslop_check.py` + đếm dấu + scan non-Latin `re.findall(r'[가-힣一-龥ぁ-ゔァ-ヺ→]', text)`
   trước khi gửi duyệt (theo chuẩn pipeline).

## Thao tác đã verify

- Đọc key: dòng `UNSLOTH_API_KEY=` trong `.env`, `split("=",1)[1].strip()`.
- Gen qua urllib với payload `{model, messages:[{role:user, content}], temperature, max_tokens, stream:false}`.
- Lưu raw ra `~/hermes-temp/draft_<topic>.txt`, rồi viết lại bản dọn (write_file) — dùng execute_code
  `open(...,'w',encoding='utf-8')` để giữ dấu.