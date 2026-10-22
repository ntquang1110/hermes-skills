# -*- coding: utf-8 -*-
"""
Tạo văn bản trình Chủ tịch: phát hành thêm cổ phần để huy động vốn.

Tham số hóa toàn bộ biến số. Chạy:
    python create_capital_raise_doc.py

Đầu ra: Google Doc + URL, đã share quyền writer, đã format tiêu đề, bảng thật.
"""
import re, sys, io, json, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def _retry(req, tries=8, base=15):
    """Exec một request Google API, retry có backoff khi bị 429 rate limit hoặc lỗi mạng."""
    from googleapiclient.errors import HttpError
    for i in range(tries):
        try:
            return req.execute()
        except HttpError as e:
            status = getattr(e.resp, 'status', None)
            if status == 429 and i < tries - 1:
                time.sleep(base * (i + 1))
                continue
            raise
        except Exception as e:
            if i < tries - 1:
                time.sleep(base * (i + 1) / 2)
                continue
            raise
    return None

TOKEN = r"C:\Users\NTQUANG_DELL\AppData\Local\hermes\google_token.json"

# ============================================================
# 1. THAM SỐ THAY ĐỔI Ở ĐÂY
# ============================================================
PARAMS = {
    "company_name": "CÔNG TY CỔ PHẦN MANNA ĐẤT VÀNG",
    "mst": "0109767318",
    "founder_pct": None,          # tỷ lệ % hiện tại của Chủ tịch, ví dụ 55.0. None = chưa biết

    "V0": 16_000_000_000,         # vốn điều lệ hiện tại (VNĐ)
    "P": 10_000,                  # mệnh giá cổ phần (VNĐ)
    "I": 5_000_000_000,           # số tiền huy động (VNĐ)
    "Vpre": 112_000_000_000,      # định giá pre-money (VNĐ)

    "n_investors": 5,             # số nhà đầu tư dự kiến
    "investor_amount": 1_000_000_000,  # số tiền mỗi NĐT (VNĐ)

    "charter_thresholds": "Không rõ (mặc định: >50% và 65%)",
    "doc_date": "08/10/2026",
}


# ============================================================
# 2. TÍNH TOÁN
# ============================================================
def compute(p):
    V0, P, I, Vpre = p["V0"], p["P"], p["I"], p["Vpre"]
    N0 = V0 // P
    g = Vpre / N0                       # giá mỗi cổ phần
    n = int(I // g)                     # số cổ phần mới (làm tròn xuống)
    Vm = n * P                          # mệnh giá phần mới
    Ts = I - Vm                         # thặng dư vốn cổ phần
    V1 = V0 + Vm                        # vốn điều lệ mới
    N1 = N0 + n                         # tổng số cp sau
    rN = n / N1                         # tỷ lệ NĐT mới
    rO = N0 / N1                        # tỷ lệ cổ đông cũ
    k = N0 / N1                         # hệ số pha loãng
    book_ps_new = (V1 + Ts) / N1        # giá trị sổ sách mỗi cp sau phát hành

    out = dict(V0=V0, P=P, I=I, Vpre=Vpre, N0=N0, g=g, n=n, Vm=Vm, Ts=Ts,
               V1=V1, N1=N1, rN=rN, rO=rO, k=k, Vpost=Vpre + I, book_ps_new=book_ps_new)

    # ngưỡng sáng lập
    out["threshold_50"] = 50.0 / k
    out["threshold_65"] = 65.0 / k
    out["founder_after"] = (p["founder_pct"] / 100.0 * k * 100) if p.get("founder_pct") else None
    return out


def fmt(n):
    """Định dạng số theo kiểu Việt Nam: dấu chấm phân cách hàng nghìn, dấu phẩy thập phân."""
    if isinstance(n, float):
        if abs(n) < 1:
            return f"{n:.4%}".replace('.', ',')
        return f"{n:,.0f}".replace(',', '.')
    return f"{n:,}".replace(',', '.')


def pct(x):
    return f"{x*100:.4f}%".replace('.', ',')


def vn(x, dec=2):
    """Định dạng số thập phân kiểu Việt Nam: dấu phẩy cho phần thập phân."""
    return f"{x:.{dec}f}".replace('.', ',')


# ============================================================
# 3. GOOGLE DOCS
# ============================================================
def build_doc(title, body_builder, style_builder):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    creds = Credentials.from_authorized_user_file(TOKEN)
    docs = build('docs', 'v1', credentials=creds)
    drive = build('drive', 'v3', credentials=creds)

    doc = docs.documents().create(body={'title': title}).execute()
    doc_id = doc['documentId']

    class _Doc:
        def __init__(self):
            self.buf = []
            self.pos = None

        def _derive_pos(self):
            cur = _retry(docs.documents().get(documentId=doc_id))
            self.pos = cur['body']['content'][-1]['endIndex'] - 1

        def add_text(self, text):
            if self.pos is None:
                self._derive_pos()
            self.buf.append((self.pos, text))
            self.pos += len(text)

        def flush(self):
            if not self.buf:
                return
            reqs = [{'insertText': {'location': {'index': i}, 'text': t}} for i, t in self.buf]
            self.buf = []
            for k in range(0, len(reqs), 40):
                _retry(docs.documents().batchUpdate(documentId=doc_id, body={'requests': reqs[k:k + 40]}))
            self.pos = None

        def add_table(self, data, widths=None):
            self.flush()
            cur = _retry(docs.documents().get(documentId=doc_id))
            end = cur['body']['content'][-1]['endIndex'] - 1
            _retry(docs.documents().batchUpdate(documentId=doc_id, body={'requests': [
                {'insertTable': {'rows': len(data), 'columns': len(data[0]), 'location': {'index': end}}}
            ]}))

            cur = _retry(docs.documents().get(documentId=doc_id))
            tabs = [el for el in cur['body']['content'] if 'table' in el]
            t = tabs[-1]['table']

            fill = []
            for ri, row in enumerate(t['tableRows']):
                for ci, cell in enumerate(row['tableCells']):
                    txt = data[ri][ci]
                    if not txt:
                        continue
                    pidx = next((ce['startIndex'] for ce in cell.get('content', []) if 'paragraph' in ce), None)
                    if pidx is None:
                        continue
                    fill.append({'insertText': {'location': {'index': pidx}, 'text': txt}})
                    if ri == 0:
                        fill.append({'updateTextStyle': {
                            'range': {'startIndex': pidx, 'endIndex': pidx + len(txt)},
                            'textStyle': {'bold': True}, 'fields': 'bold'}})
            for k in range(0, len(fill), 40):
                _retry(docs.documents().batchUpdate(documentId=doc_id, body={'requests': fill[k:k + 40]}))
            self.pos = None

    d = _Doc()
    add_text, add_table = d.add_text, d.add_table

    body_builder(add_text, add_table)
    d.flush()

    # định dạng tiêu đề
    cur = _retry(docs.documents().get(documentId=doc_id))
    reqs = []
    for el in cur['body']['content']:
        p = el.get('paragraph')
        if not p:
            continue
        text = ''.join(r.get('textRun', {}).get('content', '') for r in p.get('elements', []))
        t = text.strip()
        if not t:
            continue
        rng = {'startIndex': el['startIndex'], 'endIndex': el['endIndex'] - 1}
        reqs.extend(style_builder(t, rng))

    if reqs:
        _retry(docs.documents().batchUpdate(documentId=doc_id, body={'requests': reqs}))

    _retry(drive.permissions().create(fileId=doc_id, body={'type': 'anyone', 'role': 'writer'}))
    return f"https://docs.google.com/document/d/{doc_id}/edit"


# ============================================================
# 4. NỘI DUNG
# ============================================================
def body_builder(add_text, add_table):
    p = PARAMS
    c = compute(p)
    fn = fmt

    add_text("TRÌNH CHỦ TỊCH\nPHƯƠNG ÁN TĂNG VỐN ĐIỀU LỆ BẰNG VIỆC PHÁT HÀNH THÊM CỔ PHẦN\n\n")
    add_text(f"Công ty: {p['company_name']}\nMã số doanh nghiệp: {p['mst']}\n"
             f"Người trình: Ban điều hành\nNgày: {p['doc_date']}\n\n")

    # I
    add_text("I. TÓM TẮT ĐIỀU HƯỚNG\n\n")
    add_text(f"1. Đề xuất phát hành thêm cổ phần phổ thông để huy động {fn(c['I'])} VNĐ từ nhà đầu tư, theo hình thức chào bán riêng lẻ.\n\n")
    add_text(f"2. Giá phát hành ước tính: {fn(c['g'])} VNĐ mỗi cổ phần, tương đương {c['g']/c['P']:.1f} lần mệnh giá {fn(c['P'])} VNĐ mỗi cổ phần, xác định trên cơ sở định giá trước phát hành {fn(c['Vpre'])} VNĐ.\n\n")
    add_text(f"3. Vốn điều lệ tăng từ {fn(c['V0'])} VNĐ lên khoảng {fn(c['V1'])} VNĐ, tức chỉ tăng thêm khoảng {fn(c['Vm'])} VNĐ. Phần chênh lệch {fn(c['Ts'])} VNĐ được hạch toán vào Thặng dư vốn cổ phần, không đưa vào vốn điều lệ.\n\n")
    add_text(f"4. Nhà đầu tư mới sở hữu tổng cộng {pct(c['rN'])} vốn. Nếu phân bổ cho {p['n_investors']} nhà đầu tư, mỗi nhà đầu tư sở hữu khoảng {pct(c['rN']/p['n_investors'])}.\n\n")
    add_text("5. Quyền biểu quyết của nhà đầu tư mới: mỗi cổ phần phổ thông luôn có một phiếu biểu quyết. Nhà đầu tư nhỏ không đủ cổ phần để quyết định bất kỳ nội dung nào. Để nhà đầu tư thực sự không có quyền biểu quyết thì phải phát hành cổ phần ưu đãi cổ tức, không phải cổ phần phổ thông.\n\n")
    add_text(f"6. {fn(c['I'])} VNĐ huy động được ghi vào vốn chủ sở hữu {fn(c['V1']+c['Ts'])} VNĐ, gồm vốn điều lệ {c['V1']/1e9:.2f} tỷ và thặng dư vốn cổ phần {c['Ts']/1e9:.2f} tỷ. Định giá {c['Vpost']/1e9:.0f} tỷ là mức định giá các bên thỏa thuận, không phải là vốn điều lệ.\n\n")

    # II
    add_text("II. SỐ LIỆU CỐT LÕI\n\n")
    add_text("A. Thông số đầu vào\n\n")
    add_table([
        ["Thông số", "Giá trị"],
        ["Vốn điều lệ hiện tại", f"{fn(c['V0'])} VNĐ"],
        ["Mệnh giá cổ phần theo Điều lệ", f"{fn(c['P'])} VNĐ mỗi cổ phần (cần xác nhận)"],
        ["Tổng số cổ phần hiện tại", f"{fn(c['N0'])} cổ phần"],
        ["Định giá trước phát hành (pre-money)", f"{fn(c['Vpre'])} VNĐ"],
        ["Số tiền huy động", f"{fn(c['I'])} VNĐ"],
        ["Định giá sau phát hành (post-money)", f"{fn(c['Vpost'])} VNĐ"],
    ], widths=[3200, 4000])

    add_text("\nB. Giá phát hành\n\n")
    add_text(f"Giá mỗi cổ phần = {fn(c['Vpre'])} chia {fn(c['N0'])} = {fn(c['g'])} VNĐ mỗi cổ phần.\n")
    add_text(f"Tỷ lệ so với mệnh giá = {fn(c['g'])} chia {fn(c['P'])} = {c['g']/c['P']:.1f} lần.\n\n")

    add_text("C. Số cổ phần phát hành\n\n")
    add_text(f"Số cổ phần mới = {fn(c['I'])} chia {fn(c['g'])} = {fn(c['n'])} cổ phần.\n")
    add_text(f"Giá trị mệnh giá phần phát hành mới = {fn(c['n'])} nhân {fn(c['P'])} = {fn(c['Vm'])} VNĐ.\n")
    add_text(f"Thặng dư vốn cổ phần = {fn(c['I'])} trừ {fn(c['Vm'])} = {fn(c['Ts'])} VNĐ.\n\n")

    add_text("D. Bảng cân đối sau phát hành\n\n")
    add_table([
        ["Hạng mục", "Trước phát hành", "Sau phát hành", "Chênh lệch"],
        ["Vốn điều lệ", fn(c['V0']), fn(c['V1']), f"+{fn(c['Vm'])}"],
        ["Thặng dư vốn cổ phần", "0", fn(c['Ts']), f"+{fn(c['Ts'])}"],
        ["Vốn chủ sở hữu", fn(c['V0']), fn(c['V1']+c['Ts']), f"+{fn(c['I'])}"],
        ["Tổng số cổ phần", fn(c['N0']), fn(c['N1']), f"+{fn(c['n'])}"],
        ["Giá trị sổ sách mỗi cổ phần", fn(c['P']), fn(int(c['book_ps_new'])), f"+{fn(int(c['book_ps_new'])-c['P'])}"],
        ["Định giá", fn(c['Vpre']), fn(c['Vpost']), f"+{fn(c['I'])}"],
    ], widths=[2400, 1800, 1800, 1800])

    add_text("\nE. Cơ cấu sở hữu sau phát hành\n\n")
    add_table([
        ["Nhóm sở hữu", "Số cổ phần", "Tỷ lệ sở hữu"],
        ["Cổ đông hiện hữu", fn(c['N0']), pct(c['rO'])],
        ["Nhà đầu tư mới", fn(c['n']), pct(c['rN'])],
        ["Tổng cộng", fn(c['N1']), "100%"],
    ], widths=[3200, 2200, 2000])

    add_text(f"\nMô hình phân bổ cho {p['n_investors']} nhà đầu tư, mỗi nhà đầu tư {fn(p['investor_amount'])} VNĐ\n\n")
    per = int((p['investor_amount'] // c['g']))
    rows = [["Nhà đầu tư", "Số tiền (VNĐ)", "Số cổ phần", "Tỷ lệ sở hữu"]]
    for i in range(1, p['n_investors'] + 1):
        share = per if i < p['n_investors'] else c['n'] - per * (p['n_investors'] - 1)
        rows.append([f"Nhà đầu tư {i}", fn(p['investor_amount']), fn(share), pct(share / c['N1'])])
    rows.append(["Tổng cộng", fn(c['I']), fn(c['n']), pct(c['rN'])])
    add_table(rows, widths=[2000, 2200, 1600, 1600])

    add_text(f"\nGhi chú làm tròn: mỗi nhà đầu tư nhận {fn(per)} cổ phần, nhà đầu tư cuối cùng nhận {fn(c['n'] - per*(p['n_investors']-1))} cổ phần để tổng bằng {fn(c['n'])}.\n\n")

    # III
    add_text("III. TRẢ LỜI CÂU HỎI CỦA CHỦ TỊCH\n\n")
    add_text("Câu 1. Sau khi phát hành, vốn điều lệ tăng lên bao nhiêu?\n\n")
    add_text(f"Câu trả lời: tăng lên khoảng {fn(c['V1'])} VNĐ, tức chỉ tăng thêm khoảng {fn(c['Vm'])} VNĐ.\n\n")
    add_text("Căn cứ: Điều 112 khoản 1 Luật Doanh nghiệp 2020 số 59/2020/QH14 quy định: \"Vốn điều lệ của công ty cổ phần là tổng mệnh giá cổ phần các loại đã bán.\"\n\n")
    add_text(f"Do đó chỉ có mệnh giá của cổ phần mới bán đi mới đưa vào vốn điều lệ. Với mệnh giá {fn(c['P'])} VNĐ và {fn(c['n'])} cổ phần mới bán, phần tăng vốn điều lệ là {fn(c['Vm'])} VNĐ. Phần còn lại {fn(c['Ts'])} VNĐ là chênh lệch giữa giá phát hành {fn(c['g'])} VNĐ và mệnh giá {fn(c['P'])} VNĐ, được hạch toán vào Thặng dư vốn cổ phần theo Thông tư 133/2016/TT-BTC, không nằm trong vốn điều lệ.\n\n")
    add_text(f"Hệ quả: vốn điều lệ trên Giấy chứng nhận đăng ký doanh nghiệp sau khi hoàn tất thủ tục sẽ là {fn(c['V1'])} VNĐ.\n\n")

    add_text("Câu 2. Tại sao không tăng vốn điều lệ lên mức định giá?\n\n")
    add_text("Vốn điều lệ và định giá là hai khái niệm khác nhau.\n\n")
    add_text("Vốn điều lệ là tổng mệnh giá của các cổ phần đã bán, được ghi trên Giấy chứng nhận đăng ký doanh nghiệp, là cơ sở pháp lý về sở hữu và tỷ lệ biểu quyết.\n\n")
    add_text(f"Định giá {fn(c['Vpre'])} VNĐ là mức giá trị do các bên thỏa thuận cho toàn bộ doanh nghiệp, dùng để xác định giá phát hành mỗi cổ phần. Định giá không được ghi vào vốn điều lệ và không được đăng ký thay đổi trên Giấy chứng nhận đăng ký doanh nghiệp.\n\n")
    add_text("Ba phương án minh họa khi huy động số tiền đề xuất:\n\n")
    at_par_n = c['I'] // c['P']
    total_par = c['N0'] + at_par_n
    add_table([
        ["Phương án", "Giá mỗi cổ phần", "Số cổ phần", "Vốn điều lệ sau", "Tỷ lệ nhà đầu tư", "Đánh giá"],
        ["1. Bán ở mệnh giá", fn(c['P']), fn(at_par_n), fn(c['V0'] + at_par_n*c['P']),
         pct(at_par_n/total_par), "Bán rẻ hơn nhiều so với định giá đã thỏa thuận"],
        ["2. Bán theo định giá", fn(c['g']), fn(c['n']), fn(c['V1']), pct(c['rN']), "Khuyến nghị"],
        ["3. Ép vốn điều lệ lên định giá", "Không khả thi", "Không khả thi", "Không khả thi", "Không khả thi",
         "Sai lệch toàn bộ bảng số liệu, không phản ánh đúng cam kết"],
    ], widths=[1500, 1100, 1100, 1500, 1100, 2200])
    add_text("\nĐề xuất: chọn phương án 2.\n\n")

    add_text("Câu 3. Cổ đông mới sở hữu khoảng 0,85% thì có quyền biểu quyết gì?\n\n")
    add_text("Về pháp lý, mỗi cổ phần phổ thông luôn có một phiếu biểu quyết theo Điều 115 khoản 1 điểm a Luật Doanh nghiệp 2020. Không có quy định nào của pháp luật cho phép tước quyền biểu quyết của cổ đông sở hữu cổ phần phổ thông.\n\n")
    add_text("Về thực tiễn, tỷ lệ nhỏ không đủ để quyết định bất kỳ nội dung nào:\n\n")
    add_table([
        ["Nội dung cần quyết", "Tỷ lệ phiếu cần có", "Căn cứ", "Nhà đầu tư nhỏ"],
        ["Nghị quyết thông thường", "Trên 50% tổng số phiếu biểu quyết của cổ đông dự họp", "Điều 148 khoản 2", "Không đủ"],
        ["Loại cổ phần và tổng số cổ phần", "Từ 65% tổng số phiếu biểu quyết của cổ đông dự họp", "Điều 148 khoản 1 điểm a", "Không đủ"],
        ["Xem tra cứu báo cáo tài chính", "Từ 5% tổng số cổ phần phổ thông", "Điều 115 khoản 2", "Không có quyền"],
        ["Yêu cầu triệu tập Đại hội đồng cổ đông", "Từ 5% tổng số cổ phần phổ thông", "Điều 115 khoản 2 và khoản 3", "Không có quyền"],
        ["Yêu cầu Ban kiểm soát kiểm tra", "Từ 5% tổng số cổ phần phổ thông", "Điều 115 khoản 2 điểm c", "Không có quyền"],
    ], widths=[2200, 2400, 1800, 1400])
    add_text("\nKết luận: với cổ phần phổ thông, nhà đầu tư nhỏ không có giá trị quyết định, nhưng vẫn có đầy đủ quyền biểu quyết như các cổ đông phổ thông khác, chỉ là tỷ lệ không đủ lớn.\n\n")
    add_text("Nếu muốn nhà đầu tư thực sự không có quyền biểu quyết: phải phát hành cổ phần ưu đãi cổ tức thay vì cổ phần phổ thông. Theo Điều 117 khoản 3 Luật Doanh nghiệp 2020, cổ đông sở hữu cổ phần ưu đãi cổ tức không có quyền biểu quyết, không có quyền dự họp Đại hội đồng cổ đông, không có quyền đề cử người vào Hội đồng quản trị và Ban kiểm soát.\n\n")
    add_text("Lưu ý quan trọng: không được dùng cổ phần ưu đãi biểu quyết để giữ quyền kiểm soát. Theo Điều 116 khoản 1, chỉ tổ chức được Chính phủ ủy quyền và cổ đông sáng lập được quyền nắm giữ cổ phần ưu đãi biểu quyết, và quyền ưu đãi biểu quyết của cổ đông sáng lập chỉ có hiệu lực trong 3 năm kể từ ngày công ty được cấp Giấy chứng nhận đăng ký doanh nghiệp.\n\n")
    add_text("Hơn nữa, Điều 114 khoản 5 quy định cổ phần phổ thông không thể chuyển đổi thành cổ phần ưu đãi.\n\n")

    # IV
    add_text("IV. THẨM QUYỀN QUYẾT ĐỊNH VÀ NGƯỠNG THÔNG QUA\n\n")
    add_text("A. Phân cấp thẩm quyền\n\n")
    add_table([
        ["Nội dung", "Thẩm quyền quyết định", "Căn cứ"],
        ["Loại cổ phần và tổng số cổ phần được quyền chào bán", "Đại hội đồng cổ đông", "Điều 138 khoản 2 điểm b; Điều 112 khoản 3"],
        ["Giá bán cổ phần, thời điểm, phương thức", "Hội đồng quản trị", "Điều 126; Điều 153 khoản 2 điểm d"],
        ["Kiến nghị loại cổ phần và tổng số cổ phần", "Hội đồng quản trị kiến nghị", "Điều 153 khoản 2 điểm b"],
        ["Đăng ký thay đổi vốn điều lệ", "Công ty", "Điều 123 khoản 4"],
    ], widths=[2600, 2400, 2800])
    add_text("\nTóm lại: Đại hội đồng cổ đông quyết định bán bao nhiêu và bán loại nào. Hội đồng quản trị quyết định bán cho ai, bán ở giá nào và vào thời điểm nào.\n\n")

    add_text("B. Ngưỡng thông qua nghị quyết\n\n")
    add_text("Điều 147 khoản 2 điểm c: nghị quyết về loại cổ phần và tổng số cổ phần của từng loại phải được thông qua bằng hình thức biểu quyết tại cuộc họp Đại hội đồng cổ đông, không được lấy ý kiến bằng văn bản, trừ khi Điều lệ công ty có quy định khác.\n\n")
    add_text("Điều 148 khoản 1 điểm a: nghị quyết về loại cổ phần và tổng số cổ phần của từng loại được thông qua nếu được số cổ đông đại diện từ 65% tổng số phiếu biểu quyết trở lên của tất cả cổ đông dự họp tán thành; tỷ lệ cụ thể do Điều lệ công ty quy định.\n\n")
    add_text("Điều 148 khoản 2: các nghị quyết khác được thông qua khi được số cổ đông sở hữu trên 50% tổng số phiếu biểu quyết của tất cả cổ đông dự họp tán thành.\n\n")
    add_text("Lưu ý kỹ thuật: tỷ lệ trên được tính trên tổng số phiếu biểu quyết của các cổ đông DỰ HỌP, không phải trên tổng số cổ phần đang lưu hành.\n\n")

    add_text("C. Ảnh hưởng pha loãng đến Chủ tịch\n\n")
    add_text(f"Hệ số pha loãng = {fn(c['N0'])} chia {fn(c['N1'])} = {c['k']:.6f}\n\n")
    thr_rows = [["Tỷ lệ trước phát hành", "Tỷ lệ sau phát hành", "Đánh giá"]]
    for before in [50.0, c['threshold_50'], 60.0, c['threshold_65'], 70.0, 75.0]:
        after = before / 100 * c['k'] * 100
        if abs(before - c['threshold_50']) < 0.01:
            note = "Ngưỡng giữ trên 50%"
        elif abs(before - c['threshold_65']) < 0.01:
            note = "Đủ để tự thông qua nghị quyết 65%"
        elif before == 50.0:
            note = "Mất đa số tuyệt đối"
        elif before == 60.0:
            note = "Giữ được đa số, nhưng chưa đủ 65%"
        else:
            note = "Thoải mái"
        thr_rows.append([f"{before:.2f}%".replace('.', ','), f"{after:.2f}%".replace('.', ','), note])
    add_table(thr_rows, widths=[2400, 2400, 3000])

    if p.get("founder_pct"):
        add_text(f"\nTheo dữ liệu hiện có: Chủ tịch đang sở hữu {vn(p['founder_pct'])}%"
                 f", sau khi pha loãng còn {vn(c['founder_after'])}%.\n\n")
    else:
        add_text(f"\nChưa có tỷ lệ hiện tại của Chủ tịch. Ngưỡng giữ trên 50% sau phát hành: {vn(c['threshold_50'])}%"
                 f". Ngưỡng tự thông qua nghị quyết 65%: {vn(c['threshold_65'])}%.\n\n")

    # V
    add_text("V. TRÌNH TỰ PHÁP LÝ VÀ VIỆC CẦN LÀM\n\n")
    steps = [
        ("Bước 1. Chuẩn bị hồ sơ và số liệu", [
            "1.1. Xác định mệnh giá cổ phần theo Điều lệ hiện hành.",
            "1.2. Lấy Báo cáo tài chính gần nhất để xác định giá trị sổ sách mỗi cổ phần, bảo đảm giá phát hành không thấp hơn giá trị được ghi trong sổ sách tại thời điểm gần nhất theo Điều 126 Luật Doanh nghiệp 2020.",
            "1.3. Danh sách và số lượng nhà đầu tư. Nếu số nhà đầu tư từ 100 trở lên thì không còn thuộc hình thức chào bán riêng lẻ.",
            "1.4. Xác định tỷ lệ sở hữu hiện tại của Chủ tịch và từng cổ đông.",
            "1.5. Lập bảng phân tích sở hữu trước và sau phát hành.",
        ]),
        ("Bước 2. Quyết định của Đại hội đồng cổ đông", [
            "2.1. Nghiên cứu Điều lệ để xác định tỷ lệ thông qua nghị quyết theo từng nội dung.",
            "2.2. Biểu quyết tại cuộc họp Đại hội đồng cổ đông, không lấy ý kiến bằng văn bản.",
            "2.3. Nghị quyết nêu rõ: loại cổ phần, tổng số cổ phần được quyền chào bán, số cổ phần của từng loại, giá phát hành, tỷ lệ sở hữu sau phát hành.",
            f"2.4. Chủ tịch hiện sở hữu từ {vn(c['threshold_65'])}% trở lên có thể tự thông qua. Nếu dưới mức này, cần vận động để đạt từ 65% tổng số phiếu biểu quyết của cổ đông dự họp trở lên.",
            "2.5. Thu thập phiếu thuận bằng văn bản có chữ ký của tất cả các cổ đông để loại trừ rủi ro tranh chấp về sau.",
        ]),
        ("Bước 3. Quyết định của Hội đồng quản trị", [
            "3.1. Hội đồng quản trị quyết định thời điểm, phương thức và giá bán cổ phần.",
            "3.2. Kiến nghị loại cổ phần và tổng số cổ phần được quyền chào bán để trình Đại hội đồng cổ đông.",
            f"3.3. Xác nhận giá phát hành {fn(c['g'])} VNĐ mỗi cổ phần không thấp hơn giá trị sổ sách mỗi cổ phần tại thời điểm gần nhất.",
        ]),
        ("Bước 4. Chào bán cho cổ đông hiện hữu", [
            "4.1. Đây là thủ tục bắt buộc, không được bỏ qua.",
            "4.2. Thông báo bằng văn bản đến từng cổ đông theo địa chỉ liên lạc trong sổ đăng ký cổ đông, chậm nhất 15 ngày trước ngày kết thúc thời hạn đăng ký mua cổ phần.",
            "4.3. Nội dung thông báo gồm: họ tên, địa chỉ liên lạc, giấy tờ pháp lý; số cổ phần và tỷ lệ sở hữu hiện có; tổng số cổ phần dự kiến chào bán; số cổ phần được quyền mua; giá chào bán; thời hạn đăng ký mua; họ tên và chữ ký người đại diện theo pháp luật; kèm mẫu phiếu đăng ký mua cổ phần.",
            "4.4. Cổ đông có quyền chuyển quyền ưu tiên mua cổ phần của mình cho người khác.",
        ]),
        ("Bước 5. Chào bán riêng lẻ cho nhà đầu tư bên ngoài", [
            "5.1. Điều kiện: không chào bán thông qua phương tiện thông tin đại chúng; chào bán cho dưới 100 nhà đầu tư, không kể nhà đầu tư chứng khoán chuyên nghiệp, hoặc chỉ chào bán cho nhà đầu tư chứng khoán chuyên nghiệp.",
            "5.2. Chỉ bán phần còn lại sau khi cổ đông hiện hữu và người nhận chuyển quyền ưu tiên mua không mua hết, với điều kiện không bất lợi hơn.",
            "5.3. Ký hợp đồng đăng ký mua cổ phần giữa công ty và từng nhà đầu tư.",
            "5.4. Nhà đầu tư nước ngoài mua cổ phần phải làm thủ tục theo quy định của Luật Đầu tư.",
        ]),
        ("Bước 6. Thanh toán và hạch toán", [
            f"6.1. Nhà đầu tư chuyển đủ {fn(c['I'])} VNĐ vào tài khoản của công ty.",
            f"6.2. Hạch toán: Nợ Tài sản tiền tệ hoặc tài khoản tiền gửi {fn(c['I'])}; Có Vốn điều lệ {fn(c['Vm'])}; Có Thặng dư vốn cổ phần {fn(c['Ts'])}.",
            "6.3. Cổ phần được coi là đã bán khi đã được thanh toán đủ và thông tin về người mua được ghi đầy đủ vào sổ đăng ký cổ đông.",
        ]),
        ("Bước 7. Đăng ký và cập nhật", [
            "7.1. Cập nhật sổ đăng ký cổ đông.",
            "7.2. Đăng ký thay đổi nội dung đăng ký doanh nghiệp, gồm vốn điều lệ mới và danh sách cổ đông mới, trong thời hạn 10 ngày kể từ ngày hoàn thành đợt bán cổ phần.",
            "7.3. Cấp hoặc giao cổ phiếu cho người mua; trường hợp không giao cổ phiếu thì ghi thông tin cổ đông vào sổ đăng ký cổ đông.",
            "7.4. Sửa đổi, bổ sung Điều lệ công ty nếu Điều lệ có ghi rõ mức vốn điều lệ.",
        ]),
    ]
    for title, items in steps:
        add_text(title + "\n\n")
        for it in items:
            add_text(it + "\n")
        add_text("\n")

    add_text("Bước 8. Rào chắn pháp lý, không được bỏ qua\n\n")
    add_table([
        ["Rào chắn", "Nếu bỏ qua", "Hậu quả"],
        ["Quyền ưu tiên mua của cổ đông hiện hữu", "Không chào bán cho cổ đông hiện hữu trước", "Cổ đông cũ có cơ sở khiếu nại yêu cầu hủy giao dịch"],
        ["Ngưỡng thông qua nghị quyết", "Không đủ 65% phiếu của cổ đông dự họp", "Nghị quyết có thể bị khiếu nại và bị Tòa án hủy bỏ theo Điều 151"],
        ["Giá phát hành so với giá trị sổ sách", "Giá phát hành thấp hơn giá trị sổ sách", "Vi phạm Điều 126 Luật Doanh nghiệp 2020"],
        ["Giới hạn số nhà đầu tư", "Số nhà đầu tư từ 100 trở lên", "Không còn thuộc hình thức chào bán riêng lẻ, bị xử lý hành chính"],
        ["Thời hạn đăng ký thay đổi vốn điều lệ", "Trễ quá 10 ngày", "Bị xử phạt hành chính theo quy định về đăng ký doanh nghiệp"],
    ], widths=[2400, 2600, 2800])

    # VI
    add_text("\nVI. CÁC RỦI RO CẦN CHỐT TRƯỚC KHI ĐƯA RA ĐẠI HỘI\n\n")
    add_text(f"Rủi ro 1. Tỷ lệ hiện tại của Chủ tịch. Cần biết chính xác Chủ tịch đang sở hữu bao nhiêu phần trăm. Nếu từ {vn(c['threshold_50'])}% đến dưới {vn(c['threshold_65'])}% thì sau khi phát hành Chủ tịch sẽ nằm trong vùng nguy hiểm: vẫn còn trên 50%, nhưng không đủ để thông qua riêng các nghị quyết 65% nếu các cổ đông khác tham dự họp.\n\n")
    add_text(f"Rủi ro 2. Ngưỡng thông qua nghị quyết trong Điều lệ hiện hành. Hiện ghi nhận: {p['charter_thresholds']}. Cần xem Điều lệ trước khi ấn định ngày họp.\n\n")
    add_text("Rủi ro 3. Khả năng tham dự của các cổ đông khác. Nghị quyết được tính trên phiếu của cổ đông dự họp. Nên thu thập phiếu thuận bằng văn bản và tổ chức họp có đủ điều kiện để tránh bị khiếu nại về hình thức.\n\n")
    add_text("Rủi ro 4. Giá trị sổ sách mỗi cổ phần. Nếu công ty có lợi nhuận giữ lại hoặc quỹ khác, giá trị sổ sách mỗi cổ phần có thể cao hơn mệnh giá. Cần kiểm tra Báo cáo tài chính gần nhất.\n\n")
    add_text("Rủi ro 5. Số lượng nhà đầu tư. Nếu danh sách nhà đầu tư vượt 100 người thì hình thức chào bán riêng lẻ không còn phù hợp.\n\n")
    add_text("Rủi ro 6. Thuế. Luật Thuế thu nhập cá nhân hiện hành là Luật số 109/2025/QH15 có hiệu lực từ ngày 01/7/2026 và Nghị định số 253/2026/NĐ-CP. Thu nhập từ đầu tư vốn, gồm cổ tức và lợi nhuận được chia, chịu thuế suất 5%. Việc phát hành thêm cổ phần cho nhà đầu tư là hình thức góp vốn, phần chênh lệch giữa giá phát hành và mệnh giá được hạch toán vào thặng dư vốn cổ phần, không phải là thu nhập chịu thuế thu nhập cá nhân tại thời điểm đăng ký mua. Cần làm việc với kế toán thuế để xác định phương án hạch toán và kê khai phù hợp.\n\n")

    # VII
    add_text("VII. BẢNG TỔNG HỢP TRÌNH CHỦ TỊCH\n\n")
    add_table([
        ["Thông tin", "Giá trị"],
        ["Phương án", "Phát hành thêm cổ phần phổ thông, chào bán riêng lẻ"],
        ["Số tiền huy động", f"{fn(c['I'])} VNĐ"],
        ["Định giá trước phát hành", f"{fn(c['Vpre'])} VNĐ"],
        ["Định giá sau phát hành", f"{fn(c['Vpost'])} VNĐ"],
        ["Giá phát hành mỗi cổ phần", f"{fn(c['g'])} VNĐ, tương đương {c['g']/c['P']:.1f} lần mệnh giá"],
        ["Số cổ phần phát hành mới", f"{fn(c['n'])} cổ phần"],
        ["Vốn điều lệ trước", f"{fn(c['V0'])} VNĐ"],
        ["Vốn điều lệ sau", f"{fn(c['V1'])} VNĐ"],
        ["Thặng dư vốn cổ phần", f"{fn(c['Ts'])} VNĐ"],
        ["Tổng vốn chủ sở hữu sau phát hành", f"{fn(c['V1']+c['Ts'])} VNĐ"],
        ["Tỷ lệ cổ đông hiện hữu", pct(c['rO'])],
        ["Tỷ lệ nhà đầu tư mới", pct(c['rN'])],
        ["Tỷ lệ mỗi nhà đầu tư", f"{pct(c['rN']/p['n_investors'])}, với {p['n_investors']} nhà đầu tư"],
        ["Ngưỡng giữ trên 50% của Chủ tịch", f"{vn(c['threshold_50'])}% trước phát hành"],
        ["Ngưỡng tự thông qua nghị quyết 65%", f"{vn(c['threshold_65'])}% trước phát hành"],
        ["Ngưỡng thông qua nghị quyết quan trọng", "65% phiếu của cổ đông dự họp"],
        ["Thủ tục bắt buộc", "Chào bán cho cổ đông hiện hữu trước, thông báo trước 15 ngày"],
        ["Thời hạn đăng ký thay đổi vốn điều lệ", "10 ngày kể từ ngày hoàn thành đợt bán"],
        ["Hạn mức chào bán riêng lẻ", "Dưới 100 nhà đầu tư"],
    ], widths=[3200, 4000])

    # VIII
    add_text("\nVIII. ĐỀ XUẤT CHỦ TỊCH CHỐT\n\n")
    add_text(f"Đề xuất 1. Chốt phương án phát hành thêm {fn(c['n'])} cổ phần phổ thông, giá {fn(c['g'])} VNĐ mỗi cổ phần, huy động {fn(c['I'])} VNĐ.\n\n")
    add_text(f"Đề xuất 2. Chốt rằng vốn điều lệ sau phát hành là {fn(c['V1'])} VNĐ, phần chênh lệch {fn(c['Ts'])} VNĐ vào Thặng dư vốn cổ phần.\n\n")
    add_text(f"Đề xuất 3. Chốt tỷ lệ sở hữu sau phát hành: cổ đông hiện hữu {pct(c['rO'])}, nhà đầu tư mới {pct(c['rN'])}.\n\n")
    add_text(f"Đề xuất 4. Xác nhận tỷ lệ sở hữu hiện tại của Chủ tịch và cho phép Ban điều hành xây dựng nghị quyết Đại hội đồng cổ đông trên cơ sở ngưỡng 65%.\n\n")
    add_text("Đề xuất 5. Cho phép Ban điều hành triển khai toàn bộ thủ tục từ bước 1 đến bước 8, đồng thời báo cáo Chủ tịch về kết quả mỗi giai đoạn.\n\n")

    # IX
    add_text("IX. CÁC THÔNG TIN CẦN BỔ SUNG TRƯỚC KHI TRIỂN KHAI\n\n")
    add_table([
        ["Thông tin cần bổ sung", "Tính chất"],
        ["Tỷ lệ sở hữu hiện tại của Chủ tịch", "Bắt buộc"],
        ["Mệnh giá cổ phần theo Điều lệ", "Bắt buộc"],
        ["Báo cáo tài chính gần nhất", "Bắt buộc"],
        ["Số lượng và danh sách nhà đầu tư", "Bắt buộc"],
        ["Ngưỡng thông qua nghị quyết theo Điều lệ hiện hành", "Bắt buộc"],
        ["Số lượng thành viên Hội đồng quản trị hiện tại", "Nên có"],
        ["Cơ cấu cổ đông hiện hành chi tiết", "Nên có"],
    ], widths=[5200, 2000])

    add_text("\nChủ tịch xem xét, cho ý kiến chỉ đạo.\n\n")


def style_builder(t, rng):
    reqs = []
    if t in ('TRÌNH CHỦ TỊCH', 'PHƯƠNG ÁN TĂNG VỐN ĐIỀU LỆ BẰNG VIỆC PHÁT HÀNH THÊM CỔ PHẦN'):
        reqs.append({'updateTextStyle': {'range': rng, 'textStyle': {'bold': True, 'fontSize': {'magnitude': 16, 'unit': 'PT'}}, 'fields': 'bold,fontSize'}})
        reqs.append({'updateParagraphStyle': {'range': rng, 'paragraphStyle': {'alignment': 'CENTER'}, 'fields': 'alignment'}})
    elif re.match(r'^(I{1,3}|IV|V|VI{1,3}|IX|X)\.\s', t):
        reqs.append({'updateTextStyle': {'range': rng, 'textStyle': {'bold': True, 'fontSize': {'magnitude': 13, 'unit': 'PT'}}, 'fields': 'bold,fontSize'}})
    elif re.match(r'^[A-E]\.\s', t) or re.match(r'^Bước \d+\.', t) or t.startswith('Rủi ro ') or t.startswith('Đề xuất ') or t.startswith('Câu '):
        reqs.append({'updateTextStyle': {'range': rng, 'textStyle': {'bold': True}, 'fields': 'bold'}})
    return reqs


if __name__ == '__main__':
    url = build_doc(
        f"Trình Chủ tịch - Tăng vốn điều lệ và phát hành thêm cổ phần - {PARAMS['company_name']}",
        body_builder, style_builder
    )
    print("URL:", url)
