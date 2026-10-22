# -*- coding: utf-8 -*-
"""
Khung engine chấm điểm + tối ưu tỉ lệ công thức phụ gia chăn nuôi.
Copy file này, thay khối DU_LIEU, chạy: python formula-engine.py

Đã encode sẵn các bài học:
  - tách gói chỉ gỡ một phần hình phạt (không bao giờ 100%)
  - có hình phạt nhiệt ép viên
  - có thưởng cơ chế dự phòng (không chỉ lấy max)
  - trần điểm 0,95 (không công thức nào hoàn hảo)
  - gắn nhãn bệnh cho từng nguyên liệu
  - chặn seed vượt ngân sách
  - phạt khi trộn quá nhiều nguyên liệu
  - chế độ ÉP BUỘC nhóm cố định + báo Δ so với bản không ép
"""
import json, io, os

W_E, W_S = 0.5, 0.5              # hiệu quả / ổn định, ngang nhau
BUDGETS = [0.5, 1.0, 2.0]        # % khẩu phần = 5 / 10 / 20 kg mỗi tấn cám
MAX_NL = 8                       # số nguyên liệu tối đa cho khả thi sản xuất
TRAN_DIEM = 0.95                 # trần giá trị một cửa
HE_SO_DU_PHONG = 0.25            # trọng số cơ chế dự phòng
DIR = os.path.dirname(os.path.abspath(__file__))

# ============================ DU_LIEU (THAY Ở ĐÂY) ============================
# ev: 0 lý thuyết | 1 in vitro | 2 in vivo đúng loài | 3 đúng loài + nhiều trại/nhiễm tự nhiên
# dmin/dmax: % khẩu phần, dải liều ĐÃ CÓ NGƯỜI THỬ trên loài đích (không phải liều hãng khuyên)
# mic: nồng độ/MIC ở liều tham chiếu, None nếu không phải kháng khuẩn
# legal: 1.0 tên riêng trong danh mục | 0.7 dòng thảo dược mở | 0.5 mục thực phẩm | 0.3 mục công nhận
# boc: True đã bọc | None không rõ | False không bọc
# cc: cơ chế — dùng để thưởng dự phòng, hai chất cùng cc KHÔNG được thưởng
NL = {
 "acid-benzoic":  dict(ten="Acid benzoic",        benh=("TC","HH"), cua=["D"], ev=2, dmin=0.3, dmax=0.6,
                       mic=None, legal=1.0, cc="acid_hoa", tag={"acid_tu_do"}, boc=None, gia=1),
 "kali-diformat": dict(ten="Kali diformat",       benh=("TC","HH"), cua=["D"], ev=2, dmin=0.6, dmax=1.8,
                       mic=None, legal=1.0, cc="muoi_acid", tag={"acid_muoi"}, boc=None, gia=1),
 "mos":           dict(ten="MOS",                 benh=("TC",), cua=["A"], ev=2, dmin=0.15, dmax=0.25,
                       mic=None, legal=1.0, cc="oligosaccharide", tag={"prebiotic"}, boc=None, gia=2),
 "butyrate-boc":  dict(ten="Na-butyrate bọc lipid", benh=("TC",), cua=["A"], ev=2, dmin=0.075, dmax=0.15,
                       mic=None, legal=1.0, cc="butyrate", tag={"butyrate_boc"}, boc=True, gia=4),
 "ken-lactate":   dict(ten="Kẽm lactate",         benh=("TC",), cua=["A","B"], ev=2, dmin=0.05, dmax=0.08,
                       mic=None, legal=1.0, cc="ion_kem", tag={"ion_kim_loai"}, boc=None, gia=2),
 "ors":           dict(ten="Bù nước điện giải",   benh=("TC",), cua=["B"], ev=2, dmin=0.15, dmax=0.3,
                       mic=None, legal=1.0, cc="dien_giai", tag={"dien_giai"}, boc=None, gia=1),
 "thymol":        dict(ten="Thymol bọc",          benh=("TC","HH"), cua=["D"], ev=2, dmin=0.03, dmax=0.05,
                       mic=None, legal=1.0, cc="tinh_dau", tag={"tinh_dau"}, boc=True, gia=5),
 # nhóm bị ÉP khi khách yêu cầu biến thể +kiềm/khoáng/đất hiếm
 "khoang-sat":    dict(ten="Khoáng sét",          benh=("TC","HH"), cua=[], ev=2, dmin=0.2, dmax=0.5,
                       mic=None, legal=1.0, cc="khoang_hut", tag={"clay_manh"}, boc=None, gia=1),
 "dat-hiem":      dict(ten="Lanthanide citrate",  benh=("TC","HH"), cua=["B"], ev=0, dmin=0.01, dmax=0.03,
                       mic=None, legal=1.0, cc="dat_hiem", tag={"dat_hiem"}, boc=None, gia=4),
 "kiem-thao-duoc":dict(ten="Bộ kiềm thảo dược",   benh=("TC","HH"), cua=[], ev=0, dmin=0.2, dmax=0.5,
                       mic=None, legal=0.7, cc="kiem", tag={"kiem","thao_duoc"}, boc=None, gia=2),
}
# trọng số cửa theo bệnh — phải cộng = 1.0
CUA_THEO_BENH = {
 "TC": {"D": 0.20, "A": 0.35, "B": 0.30, "C": 0.15},
 "HH": {"E_re": 0.35, "E_col": 0.30, "B": 0.20, "D": 0.15},
}
# tách gói gỡ được bao nhiêu phần của từng xung đột (1.0 = gỡ hết — ĐỪNG dùng 1.0 cho hấp phụ)
TACH_GOI_GO = {
 "clay_huu_co": 0.6, "clay_tinh_dau": 0.6, "clay_oligo": 0.6, "dat_hiem_clay": 0.6,
 "acid_kiem": 0.3,
}
# ============================================================================

def gia_tri_mot_chat(k, lieu):
    nl = NL[k]
    if nl["ev"] == 0:
        return None
    evn = min(1.0, nl["ev"] / 3.0)
    dn = min(1.0, lieu / nl["dmax"])
    if lieu > nl["dmax"] * 1.01:
        dn = max(0.4, 1.0 - (lieu / nl["dmax"] - 1))
    mn = 1.0 if nl["mic"] is None else min(1.0, nl["mic"])
    return 0.45 * evn + 0.30 * dn + 0.25 * mn

def cham_on_dinh(ct, tach_goi=False):
    tag = set()
    for k in ct:
        tag |= NL[k]["tag"]
    p, loi = 0.0, []
    def hit(dk, diem, ten, khoa=None):
        nonlocal p
        if not dk:
            return
        d = diem
        if tach_goi and khoa and khoa in TACH_GOI_GO:
            d *= (1 - TACH_GOI_GO[khoa])
        p += d
        loi.append(f"{ten} (-{d:.1f})")
    huu_co = tag & {"alkaloid", "thao_duoc", "tinh_dau", "prebiotic", "probiotic",
                    "enzyme", "protein_igy", "flavonoid", "tanin"}
    hit("clay_manh" in tag and bool(huu_co), 20, "khoáng sét hấp phụ hoạt chất hữu cơ", "clay_huu_co")
    hit("clay_manh" in tag and "tinh_dau" in tag, 10, "khoáng sét hấp phụ tinh dầu", "clay_tinh_dau")
    hit("clay_manh" in tag and "prebiotic" in tag, 6, "khoáng sét hấp phụ oligosaccharide", "clay_oligo")
    hit("acid_tu_do" in tag and "kiem" in tag, 25, "acid tự do + kiềm trung hoà lẫn nhau", "acid_kiem")
    hit("acid_tu_do" in tag and "ion_kim_loai" in tag, 8, "acid tự do + ion kẽm tạo phức")
    hit("acid_tu_do" in tag and "probiotic" in tag, 14, "acid tự do giảm sống probiotic")
    hit("acid_tu_do" in tag and "protein_igy" in tag, 12, "IgY biến tính ở pH thấp")
    hit("acid_tu_do" in tag, 5, "acid tự do hút ẩm, ăn mòn thiết bị")
    hit("tanin" in tag and "protein_sdp" in tag, 14, "tanin kết tủa protein huyết tương")
    hit("tanin" in tag and "enzyme" in tag, 8, "tanin bất hoạt enzyme")
    hit("tanin" in tag and "ion_kim_loai" in tag, 6, "tanin chelate ion kim loại")
    hit("dat_hiem" in tag, 10, "đất hiếm tạo phức với phytate khẩu phần")   # không gỡ được
    hit("dat_hiem" in tag and "clay_manh" in tag, 10, "đất hiếm bị khoáng sét hấp phụ", "dat_hiem_clay")
    hit("dat_hiem" in tag and "acid_tu_do" in tag, 6, "đất hiếm tạo phức acid hữu cơ")
    hit("mcfa" in tag and "ion_kim_loai" in tag, 6, "MCFA tạo xà phòng canxi")
    hit("kiem" in tag and "butyrate_boc" in tag, 8, "kiềm làm vỏ bọc butyrate nhả sớm")
    hit("kiem" in tag and "tinh_dau" in tag, 8, "kiềm phá tinh dầu phenol")
    hit("kiem" in tag and "flavonoid" in tag, 4, "kiềm làm mất bền flavonoid")
    hit("kiem" in tag and "protein_igy" in tag, 10, "kiềm làm mất hoạt tính kháng thể")
    nhiet = 0.0
    for k in ct:
        v = NL[k]
        if v["tag"] & {"tinh_dau", "probiotic", "enzyme", "butyrate_boc"}:
            nhiet += 0 if v["boc"] is True else (7 if v["boc"] is None else 15)
    if nhiet:
        p += min(30, nhiet); loi.append(f"nhiệt ép viên làm mất hoạt tính (-{min(30, nhiet):.0f})")
    if len(ct) > 5:
        d = min(9.0, 1.5 * (len(ct) - 5))
        p += d; loi.append(f"trộn {len(ct)} nguyên liệu: phân tầng (-{d:.1f})")
    return max(0.0, 100 - p), loi

def cham_hieu_qua(ct, cua_w, budget):
    chi, loi, tong = {}, [], 0.0
    for cua, w in cua_w.items():
        ung = []
        for k, lieu in ct.items():
            if cua not in NL[k]["cua"]:
                continue
            g = gia_tri_mot_chat(k, lieu)
            if g is None:
                msg = f"{NL[k]['ten']} chưa có bằng chứng trên loài đích, không tính hiệu quả"
                if msg not in loi:
                    loi.append(msg)
                continue
            ung.append((g, k))
        if not ung:
            chi[cua] = 0.0
            continue
        ung.sort(reverse=True)
        best_g, best_k = ung[0]
        du_phong = 0.0
        for g, k in ung[1:]:
            if NL[k]["cc"] != NL[best_k]["cc"]:
                du_phong = max(du_phong, g)
        f = min(TRAN_DIEM, best_g + HE_SO_DU_PHONG * du_phong)
        chi[cua] = round(100 * w * f, 1)
        tong += 100 * w * f
    if sum(ct.values()) > budget + 1e-9:
        loi.append(f"tổng liều {sum(ct.values()):.3f}% vượt ngân sách {budget:g}%")
    return round(tong, 1), chi, loi

def cham(ct, cua_w, budget, tach_goi=False):
    if not ct:
        return -1, 0, 0, []
    S, loiS = cham_on_dinh(ct, tach_goi)
    E, _, loiE = cham_hieu_qua(ct, cua_w, budget)
    return W_E * E + W_S * S, E, S, loiS + loiE

def nhip(k):
    v = NL[k]
    return sorted({round(v["dmin"] + i * (v["dmax"] - v["dmin"]) / 3, 4) for i in range(4)})

def sua_seed(seed, budget, benh):
    ct = {k: min(d, NL[k]["dmax"]) for k, d in seed.items()
          if k in NL and benh in NL[k]["benh"]}
    while sum(ct.values()) > budget and ct:
        k = max(ct, key=lambda x: ct[x] / NL[x]["dmax"])
        ct[k] = round(ct[k] * 0.8, 4)
        if ct[k] < NL[k]["dmin"] * 0.5:
            del ct[k]
    return ct

def toi_uu(benh, budget, seed, tach_goi=False, ep_buoc=(), max_vong=80, ten=""):
    cua_w = CUA_THEO_BENH[benh]
    ct = sua_seed(seed, budget, benh)
    for k in ep_buoc:
        ct.setdefault(k, NL[k]["dmin"])
    if sum(ct.values()) > budget + 1e-9:
        raise AssertionError(f"seed không khả thi: {sum(ct.values()):.3f}% > {budget:g}%")
    best = cham(ct, cua_w, budget, tach_goi)[0]
    log = []
    for v in range(max_vong):
        ung = None
        for k in list(ct):                                  # đổi liều
            for d in nhip(k):
                thu = dict(ct); thu[k] = d
                if sum(thu.values()) > budget:
                    continue
                s = cham(thu, cua_w, budget, tach_goi)[0]
                if s > best + 1e-6:
                    best, ung = s, ("đổi liều", k, d, thu)
        for k in [x for x in NL if set(NL[x]["cua"]) & set(cua_w) and benh in NL[x]["benh"]]:
            if k in ct or len(ct) >= MAX_NL:            # thêm
                continue
            for d in nhip(k):
                thu = dict(ct); thu[k] = d
                if sum(thu.values()) > budget:
                    continue
                s = cham(thu, cua_w, budget, tach_goi)[0]
                if s > best + 1e-6:
                    best, ung = s, ("thêm", k, d, thu)
        for k in list(ct):                                  # bỏ (trừ nhóm ép)
            if k in ep_buoc:
                continue
            thu = {a: b for a, b in ct.items() if a != k}
            if not thu:
                continue
            s = cham(thu, cua_w, budget, tach_goi)[0]
            if s > best + 1e-6:
                best, ung = s, ("bỏ", k, 0, thu)
        if not ung:
            log.append((v, "DỪNG — không còn bước cải thiện", round(best, 2)))
            break
        hanh, k, d, ct = ung
        best = cham(ct, cua_w, budget, tach_goi)[0]
        log.append((v, f"{hanh} {k} → {d:g}%", round(best, 2)))
    S, loiS = cham_on_dinh(ct, tach_goi)
    E, chi, loiE = cham_hieu_qua(ct, cua_w, budget)
    for k, d in ct.items():
        if d > NL[k]["dmax"] * 1.01:
            loiE.append(f"{NL[k]['ten']} vượt liều đã thử ({d:g}% > {NL[k]['dmax']:g}%)")
    return dict(ten=ten, benh=benh, budget=budget, tach_goi=tach_goi, ct=ct, E=E, S=S,
                total=round(W_E * E + W_S * S, 2), chi=chi, canh_bao=loiS + loiE, log=log,
                tong_lieu=round(sum(ct.values()), 4))

if __name__ == "__main__":
    SEED = {"acid-benzoic": 0.6, "mos": 0.2, "butyrate-boc": 0.1, "ken-lactate": 0.08}
    EP = {"khoang-sat": 0.3, "dat-hiem": 0.02, "kiem-thao-duoc": 0.3}
    ra = []
    for ten, benh, seed in [("TC-1", "TC", SEED)]:
        for b in BUDGETS:
            for tach in (False, True):
                ra.append(toi_uu(benh, b, seed, tach, ten=ten))
                s3 = dict(seed); s3.update(EP)
                ra.append(toi_uu(benh, b, s3, tach, ep_buoc=tuple(EP), ten=ten + "+3"))
    ra = [r for r in ra if r["total"] > 0]
    ra.sort(key=lambda r: -r["total"])
    for r in ra:
        print(f"{r['ten']:8s} {r['budget']:>4.1f}% {'2 gói' if r['tach_goi'] else '1 bao'}"
              f" → tổng {r['total']:5.1f} (E {r['E']:5.1f} · S {r['S']:5.1f}) liều {r['tong_lieu']:.3f}%")
        for k, d in sorted(r["ct"].items(), key=lambda x: -x[1]):
            print(f"      · {d*10:6.2f} kg/tấn  {NL[k]['ten']}")
        print("      cửa:", r["chi"], "| vòng:", len(r["log"]))
        for c in r["canh_bao"][:4]:
            print("      ⚠", c)
    # Δ của biến thể bị ép
    idx = {(r["ten"], r["budget"], r["tach_goi"]): r for r in ra}
    print("\nGIÁ CỦA VIỆC ÉP NHÓM CỐ ĐỊNH")
    for (ten, b, tach), r in sorted(idx.items()):
        if not ten.endswith("+3"):
            continue
        base = idx.get((ten[:-2], b, tach))
        if base:
            print(f"  {ten:10s} {b:>4.1f}% {'2 gói' if tach else '1 bao'}"
                  f"  Δ {r['total'] - base['total']:+6.1f}  ({base['total']:.1f} → {r['total']:.1f})")
    json.dump(ra, io.open(os.path.join(DIR, "ket-qua-toi-uu.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\n{len(ra)} phương án → ket-qua-toi-uu.json")
