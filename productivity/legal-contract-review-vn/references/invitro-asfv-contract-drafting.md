# Hợp đồng thử nghiệm In vitro ASFV — Drafting Template

## Bối cảnh

- **Bên A:** Công ty CP Manna Đất Vàng
- **Bên B:** Học viện / Viện nghiên cứu
- **Mục đích:** Đánh giá hiệu quả diệt virus ASF (genotype II + tái tổ hợp I/II) trên mô hình In vitro
- **Sản phẩm:** Kiềm EZ80 (bột) + Kiềm EZ67 (dung dịch)
- **Giá trị tham khảo:** 115.800.000 đồng

## Nguồn tham khảo

- Hợp đồng gốc Học viện Nông nghiệp gửi: `22. HĐ mana đất vàng chất sát trùng.doc`
- Hợp đồng cũ Manna với Prof Phan: `15_05_2026_HỢP_ĐỒNG_NGHIÊN_CỨU_VIRUS_ASF_DTLCP_PROF_PHAN.docx`
- File soạn: `HD_NC_InVitro_ASF_Manna.docx` (11 điều, in vitro thuần túy)

## Cấu trúc hợp đồng In vitro tiêu chuẩn (11 Điều)

| Điều | Nội dung | Ghi chú |
|:----:|----------|---------|
| 1 | Mục tiêu, phạm vi In vitro, tiến độ | Nồng độ cụ thể, virus, tế bào, số lần lặp |
| 2 | Quyền & Nghĩa vụ Bên A | Giám sát, chứng kiến, nghiệm thu |
| 3 | Quyền & Nghĩa vụ Bên B | Báo cáo 7 ngày/lần, 24h nếu sự cố |
| 4 | SỞ HỮU KẾT QUẢ | Tuyệt đối thuộc Bên A + cấm reverse engineering |
| 5 | Kinh phí & Thanh toán | Trọn gói, 50% cọc + 50% sau nghiệm thu |
| 6 | Bảo mật | 5 năm sau chấm dứt + phạt |
| 7 | Xử lý vi phạm | Chậm tiến độ 0,5%/ngày, bảo mật 200tr |
| 8 | Hiệu lực & Chấm dứt | Tối đa 12 tháng |
| 9 | Bất khả kháng | |
| 10 | Giải quyết tranh chấp | TAND Hà Nội |
| 11 | Điều khoản chung | |

## Nồng độ thử nghiệm In vitro tham khảo

| Sản phẩm | Nồng độ (pha nước cứng) |
|:---------:|:-----------------------:|
| EZ80 (dạng bột) | 0,3% — 0,5% — 0,7% |
| EZ67 (dạng lỏng) | 1% — 2% — 5% — 10% |

- Đo pH ở các nồng độ đã pha loãng
- Thời gian tiếp xúc với virus: 30, 60, 120 phút ở 37°C
- Lặp lại ít nhất 03 lần
- Tế bào: PAM (đại thực bào phế nang lợn) + hồng cầu lợn

## Chuyển đổi từ hợp đồng hỗn hợp (In vitro + In vivo) sang thuần In vitro

Khi user có hợp đồng cũ bao gồm cả in vitro và in vivo, muốn tách riêng phần in vitro:

1. Lấy scope in vitro từ hợp đồng cũ (EZ67 trên tế bào PAM)
2. Bỏ scope in vivo (lợn thật, challenge virus)
3. Điều chỉnh giá (tham khảo: 115.8tr cho in vitro vs 500tr cho cả combo)
4. Mở rộng thêm sản phẩm nếu cần (VD: thêm EZ80 vào in vitro)
5. Giữ nguyên các điều khoản bảo vệ từ hợp đồng cũ: SHTT, bảo mật, phạt, giám sát

## Kỹ thuật: Trích xuất text từ .doc (OLE2) cũ

Khi user gửi file `.doc` (định dạng Word 97-2003 cũ, không phải `.docx`):

```python
import olefile, re
FILE = 'sample.doc'
ole = olefile.OleFileIO(FILE)
data = ole.openstream('WordDocument').read()
ole.close()
text = data.decode('utf-16-le', errors='replace')
segments = re.findall(r'[A-Za-zÀ-ỹ0-9\s.,;:()\-/\%"\'\u2013\u2014\u2018\u2019\u201c\u201dđ]+', text)
for seg in segments:
    s = seg.strip()
    if len(s) > 10:
        print(s)
```

Cần cài: `pip install olefile`

## Xử lý mẫu hợp đồng do đối tác gửi — Chiến thuật

Khi đối tác gửi hợp đồng mẫu (thiếu nhiều điều khoản):

1. **Phát hiện điều khoản THIẾU** — đây là thủ thuật: bên soạn "quên" đưa điều khoản có lợi cho bên kia. Checklist:
   - Sở hữu kết quả? (🔴 tử huyệt)
   - Cấm reverse engineering? (🔴 tử huyệt)
   - Bảo mật sau chấm dứt? (thời hạn?)
   - Quyền giám sát/chứng kiến?
   - Thời gian cam kết rõ ràng?
   - Chế tài sai sót?
   - Ngưỡng kết luận?

2. **Sửa trên nền hợp đồng của họ** — trình bày dưới dạng "bổ sung/sửa đổi" để đối tác dễ chấp nhận hơn là soạn hợp đồng mới

3. **Đánh dấu thay đổi** — dùng màu xanh cho bổ sung, gạch ngang đỏ cho xóa, ghi chú [SỬA] trong ngoặc

## Đặt tên hợp đồng

User có thể yêu cầu tên hợp đồng "kêu" hơn, mang tính cam kết. Các phương án đã dùng:

- "Hợp đồng Cam kết Trích thưởng" (thiện chí)
- "Hợp đồng Nguyên tắc Hợp tác Nghiên cứu Khoa học" (trung tính)
- "Hợp đồng Phân tích" (kỹ thuật)
- "Hợp đồng Hợp tác Thương mại" (thương mại)
