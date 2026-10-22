# Gọi vốn CTCP tại VN — bút toán, luật, thuế (case học)

Case tham chiếu: vốn điều lệ 16 tỷ, định giá pre-money 112 tỷ, nhà đầu tư góp 5 tỷ.
Dùng lại phần khung + checklist khi viết tài liệu hướng dẫn kế toán cho vòng gọi vốn.

## Công thức gốc

```
Số cp phát hành   = Tiền góp / Giá mỗi cp
Giá mỗi cp        = Định giá pre-money / Số cp đang lưu hành
Số cp lưu hành    = Vốn điều lệ / Mệnh giá (10.000 đ — Luật Doanh nghiệp 2020)
Tỷ lệ sở hữu NĐT = Tiền góp / (Định giá pre + Tiền góp)
```

Case này: 112 tỷ / 1.600.000 cp = 70.000 đ/cp → 5 tỷ / 70.000 = 71.428 cp.

## Bút toán — tách mệnh giá và thặng dư

```
Nợ 112  (Tiền gửi NH)              Tiền góp thực nhận
   Có 4111 (Vốn đầu tư CSH)        Số cp × mệnh giá
   Có 4112 (Thặng dư vốn cổ phần) Số cp × (giá phát hành − mệnh giá)
```

**Tại sao phải tách:** ghi thẳng tiền góp vào 4111 sẽ cho tỷ lệ sở hữu sai (case này 23.8% thay vì
4.27%) vì mệnh giá 10.000 đ là mệnh giá pháp lý cố định, không phản ánh giá trị thị trường.
Phần chênh chính là giá trị doanh nghiệp đã có sẵn — thuộc về cổ đông cũ.

## Bẻ cong số — phải khai báo

71.428 cp × 70.000 đ = 4.999.960.000 đ ≠ 5 tỷ. Chênh 40.000 đ hấp thụ vào 4112.
Giá thực tế 70.001,12 đ/cp (lệch 0,0016%). Luôn ghi rõ trong tài liệu — bộ phận kế toán sẽ tự
tính lại và thấy lệch nếu giấu.

## Chi phí phát hành

```
Nợ 4112   Có 112
```
Ghi giảm thẳng 4112, **không** qua 642/chi phí — bản chất là giao dịch vốn (Thông tư 200/2014/TT-BTC).
Nếu chi phí phát sinh TRƯỚC khi có thặng dư (gọi vốn lần đầu): tạm ghi TK 242 chi phí trả trước,
kết chuyển vào 4112 khi phát hành xong. Thiếu thặng dư thì phần dư ghi TK 421 (LNST chưa phân phối) —
TK 4112 không bao giờ để dư Nợ cuối kỳ.

## Thủ tục (CTCP)

1. HĐQT nghị quyết phát hành cp riêng lẻ (cần ĐHĐCĐ đã ủy quyền trong Điều lệ). Dưới 100 NĐT +
   không chào bán công chúng → không cần UBCK.
2. Ký hợp đồng subscription (số cp, giá, tổng tiền, thời hạn, quyền nghĩa vụ).
3. NĐT chuyển khoản — nội dung ghi rõ "thanh toán tiền mua cp phát hành thêm". Không nhận tiền mặt.
4. Hạch toán khi **tiền về tài khoản** (chứng từ: sao kê NH + HĐ + nghị quyết). Ký HĐ chưa ghi sổ.
5. Đăng ký thay đổi vốn điều lệ với Sở KHĐT trong **10 ngày**.
6. Cập nhật sổ cổ đông (căn cứ pháp lý quyền sở hữu / biểu quyết / cổ tức).
7. Cấp **giấy chứng nhận cổ phần** (Điều 122 Luật Doanh nghiệp 2020) — khác với "cập nhật sổ cổ đông"
   ở bước 6, hai việc này hay bị gộp nhầm.

**Rủi ro thứ tự:** nhận tiền trước → đăng ký Sở KHĐT sau là phổ biến nhưng nếu Sở KHĐT từ chối
hồ sơ thay đổi vốn thì 5 tỷ đã vào công ty không có căn cứ pháp lý. An toàn hơn: đăng ký trước
(dựa trên nghị quyết HĐQT), nhận tiền sau. Nêu cảnh báo này trong tài liệu.

## Thuế

- **TNDN:** thặng dư vốn KHÔNG phải thu nhập chịu thuế — Khoản 3 Điều 5 Thông tư 78/2014/TT-BTC
  (sửa đổi): "Khoản chênh lệch giữa giá bán và mệnh giá cổ phiếu phát hành thêm không phải thu nhập
  chịu thuế TNDN."
- **TNCN khi phát hành:** không phát sinh.
- **TNCN khi NĐT chuyển nhượng sau này:** mặc định khấu trừ tại nguồn **0,1% trên tổng giá trị
  chuyển nhượng** (Nghị định 126/2020/NĐ-CP). Nếu NĐT đăng ký với cơ quan thuế và đáp ứng điều kiện
  → 20% trên thu nhập thực tế (giá bán − giá mua − chi phí liên quan). Đừng viết "tuỳ điều kiện"
  chung chung — phải nêu mặc định và điều kiện để chuyển đổi.
- **Lệ phí:** đăng ký thay đổi vốn điều lệ ~100.000–200.000 đ. Thuế môn bài điều chỉnh nếu vốn
  điều lệ đổi.

## Bẫy kiểm toán

- 4112 không bao giờ dư Nợ cuối kỳ.
- 4111 phải khớp với vốn điều lệ đã đăng ký tại Sở KHĐT.
- Giá phát hành phải có nghị quyết HĐQT.
- Không ghi nhận trước khi tiền về.
- Chi phí phát hành có chứng từ hợp lệ.

## Tác động chỉ số

Book value/share tăng; EPS pha loãng nhẹ; P/B giảm; nợ/VCSH cải thiện.
Tổng VCSH tăng đúng bằng tiền góp — bảng cân đối vẫn cân.
