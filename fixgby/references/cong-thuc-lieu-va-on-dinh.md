# Bàn giao tầng SẢN PHẨM — chốt liều, ổn định, sheet định mức (21/10/2026)

Nối tiếp lớp CHẤT × CHẤT của `docs/14-cong-thuc-co-ban`. Đây là trạng thái đã chốt, trích lại được.

## 1. Bản chốt liều — và bản cũ đã SAI

| File | Nội dung | Dùng được? |
|---|---|---|
| `docs/14-cong-thuc-co-ban/09-lieu-san.md` | **BẢN CHỐT**: TC-1 **2,5 kg/tấn** → 90,40 điểm (đỉnh/platô) · HH-1 **4,5 kg/tấn** → 95,75 | ✅ trích file này |
| `docs/14-cong-thuc-co-ban/08-chot-ngan-sach.md` | bản cũ: TC-1 5,0 · HH-1 7,5 kg/tấn | ❌ **đã đánh dấu SAI** — nửa số kg là tiền đổ đi |
| `docs/14-cong-thuc-co-ban/10-thu-on-dinh-gia-toc.md` | đề cương thử ổn định 3/6 tháng (xem skill `product-stability-testing`) | ✅ |

Đường cong đã đo: TC-1 0,70→79,70 (sàn kỹ thuật) · 2,5→**90,40** · 8,0→90,40 (dẹt từ 2,5).
HH-1 1,80→86,00 (sàn) · 4,5→**95,75** · 7,5→96,75.

## 2. Hai luật rút ra — đừng tái phạm

**(a) Chốt liều phải quét CẢ HAI CHIỀU.** Quét một chiều tới điểm bão hoà từng làm chốt sai **gấp đôi** (5,0 thay
vì 2,5 kg/tấn). Ở HH-1, 4,5 kg mất đúng **1,00 điểm** so 7,5 kg mà tiết kiệm 3 kg/tấn cám. Biên giá trị:
TC-1 2,5→2,0 mất 0,25 điểm/kg còn HH-1 4,5→4,0 mất 2,00 — **TC-1 rẻ điểm hơn HH-1 tám lần**.

**(b) Điểm ổn định S = 100 KHÔNG phải tin tốt.** Nó chỉ nghĩa là engine không tìm ra cặp tương kỵ nào trong tổ
hợp đó. Bằng chứng: ép thêm nền kiềm + nền khoáng thì S rơi **88 → 70 → 82**, và hiệu quả không bao giờ bằng
bản tự do. Muốn nói "ổn định" với khách thì phải có thử gia tốc + dài hạn thật.

## 3. Cửa C — nút thắt lớn nhất

**Cửa C = 0 ở MỌI công thức**, kể cả nghiệm tự do: không chất nào trong 57 có bằng chứng ≥ L2 cho **miễn dịch
niêm mạc (IgA tiết)** → trần của tiêu chảy hiện là **85 điểm**. Ứng viên rẻ lấp cửa C: ***Bacillus subtilis*
0,20 kg/tấn (bậc L4**, tổng quan 29 nghiên cứu) — vào được mọi tổ hợp sàn. Nợ đang tra: bài tổng quan đó **có đo
IgA tiết trong phân hay không**.

## 4. Sheet định mức — tab `CT heo (fixgby)`

6 công thức đã đổ ra sheet `VK – RnD + Lab` (id `<SHEET_ID>`, gid
`1534069869`), **thêm tab** — KHÔNG chèn dòng vào block `Định mức & Lượng mua` của Quang (sẽ làm gãy tổng ở
PHẦN 2 của anh). Pattern + bộ 3 cột cân được + phép kiểm `TỔNG` cộng đúng 100 %/1000 g:
`google-sheets-ops/references/premix-dinh-muc-tab-pattern.md`.

## 5. Vùng khí hậu — chốt cho mọi thử ổn định ở VN

Việt Nam là **vùng IVB**: dài hạn **30 °C ± 2 / 75% RH ± 5**, gia tốc **40 ± 2 / 75 ± 5** tối thiểu 6 tháng
(ICH Q1A(R2) + ASEAN/WHO TRS 953). **Đo ở 25 °C/60% RH là điều kiện vùng I–II — sai vùng, phải nói thẳng khi ai
đó trích kết quả 25/60.**

## 6. Còn nợ (đã bàn giao cho Quang)

Bacillus có đo IgA tiết trong phân không · hàm lượng tannin hạt dẻ thật của lô hàng (giả định 65–75%) · bảng giá
nhà cung cấp → giá vốn VND (cột giá trong engine **chỉ là thứ bậc**, không dùng định giá) · thử gia tốc 3/6
tháng · chốt nhà sản xuất tách 2 gói · **Balantidium coli** và **Strongyloides ransomi** chưa dựng đường đi.
