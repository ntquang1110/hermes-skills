#!/usr/bin/env python3
"""Push 6 bài tâm lý 13/08 vào KFlow, prepend OVERVIEW JSON để tab Visualize render đúng chuẩn."""
import json, ssl, urllib.request, os

BASE = "http://localhost:3003"
AUTH = "Bearer hermes-knowledge-secret"
PASSCODE = "<PASSCODE>"
COOKIE = f"tfo_auth={__import__('hashlib').sha256(PASSCODE.encode()).hexdigest()}"
SLUG = "tam-ly"

OVERVIEWS = {
    1: {
        "what": "Leader soi từng chi tiết sau khi giao việc khiến nhân viên ngừng chủ động. Họ không lười, họ phản ứng đúng với hệ thống phản hồi.",
        "why": "Vòng lặp soi → thụ động → soi nhiều hơn tạo ra chính cái tính mà leader chê. Mất tự chủ là mất động lực nội tại.",
        "mechanism": [
            "Skinner (1953): hành vi bị phạt (bị sửa từng chi tiết) thì giảm, hành vi an toàn (làm theo lệnh) thì lặp lại",
            "Deci & Ryan (1985) SDT: kiểm soát từng bước phá nhu cầu tự chủ, mất tự chủ là mất động lực nội tại",
            "Bandura (1977): mọi quyết định đều bị sửa → self-efficacy sụp → không dám làm",
            "Brehm (1966) reactance: bị kiểm soát quá mức → chống lại hoặc rút lui; rút lui khiến leader càng soi",
            "Vòng lặp tự củng cố: soi → thụ động → 'đúng là không yên tâm' → soi nhiều hơn"
        ],
        "players": ["Leader (Quang)", "Nhân viên (Tùng)", "Phạt vi mô", "Tự chủ (SDT)", "Self-efficacy"],
        "applications": [
            "Giao việc kèm tiêu chí rõ, chờ sản phẩm cuối thay vì sửa trong lúc làm",
            "Hỏi 'em cần gì để hoàn thành' thay vì kiểm soát từng bước",
            "Khen nỗ lực chủ động, không chỉ chê kết quả"
        ],
        "limits": "Không phải mọi sửa đổi đều là phạt. Sửa có nguyên tắc, có giải thích vẫn giữ được niềm tin.",
        "analogy": "Giống huấn luyện chó: phạt sai lúc làm thì con vật ngừng thử, chỉ ngồi yên chờ lệnh."
    },
    2: {
        "what": "Chỉ tiêu đo sai tạo hành vi sai. Khi con số thành mục tiêu, nó không còn là thước đo tốt (Goodhart 1975).",
        "why": "Hệ thống thưởng theo số đơn khiến nhân viên tối ưu số đơn, bỏ khách lớn khó chốt. Siết chỉ tiêu càng làm méo thước đo.",
        "mechanism": [
            "Skinner (1953): hành vi được thưởng thì lặp lại → thưởng theo số đơn thì tối ưu số đơn",
            "Goodhart (1975) + Strathern (1997): con số nào bị gắn thưởng phạt thì con số đó bị bóp méo",
            "Deci, Koestner & Ryan (1999) meta 128 thí nghiệm: thưởng vật chất có điều kiện giảm động lực nội tại",
            "Vòng lặp: chỉ tiêu sai → hành vi sai → kết quả sai → đổ lỗi nhân viên → siết chỉ tiêu thêm"
        ],
        "players": ["Chỉ tiêu (KPI)", "Nhân viên (Hùng)", "Thưởng vật chất", "Động lực nội tại", "Goodhart's law"],
        "applications": [
            "Đổi KPI từ số đơn sang doanh thu + lợi nhuận + giá trị khách",
            "Đo thước nào muốn hành vi đó: thiết kế KPI theo hành vi mong muốn",
            "Kết hợp chỉ tiêu định lượng và định tính để không méo"
        ],
        "limits": "Không phải KPI nào cũng xấu. Vấn đề là gắn thưởng phạt cứng vào một con số duy nhất.",
        "analogy": "Giống đo cân nặng bằng thước đo chiều cao: con số thì có, nhưng không đo thứ bạn muốn."
    },
    3: {
        "what": "Nhân viên đổ lỗi hoàn cảnh không phải do gian dối. Thiên kiến tự phục vụ (Miller & Ross 1975) tự bảo vệ hình ảnh bản thân.",
        "why": "Hỏi 'tại sao' càng gắt càng kích amygdala, PFC ngừng lý luận khách quan, phòng thủ càng cao. Câu hỏi buộc tội không bao giờ sinh ra lời nhận lỗi.",
        "mechanism": [
            "Miller & Ross (1975) self-serving bias: gán thành công cho mình, đổ thất bại ra ngoài",
            "Jones & Nisbett (1971) actor-observer asymmetry: hành vi của mình = hoàn cảnh, của người khác = tính cách",
            "Festinger (1957) cognitive dissonance: 'tôi làm tốt' đụng 'tôi gây lỗi' → bộ não bẻ lý do ra ngoài",
            "Hỏi 'tại sao' gắt → amygdala báo động → PFC ngừng khách quan → phòng thủ sâu hơn",
            "Vòng lặp: buộc tội → chối → buộc tội mạnh hơn → chối sâu hơn"
        ],
        "players": ["Nhân viên (Tuấn)", "Leader (Quang)", "Self-serving bias", "Actor-observer asymmetry", "Amygdala / PFC"],
        "applications": [
            "Hỏi 'chuyện gì đã xảy ra, lần sau làm khác thế nào' thay vì 'tại sao'",
            "Tách người khỏi lỗi: 'quy trình nào cho phép lỗi này xảy ra'",
            "Xây văn hóa báo lỗi không phạt để lỗi lộ ra sớm"
        ],
        "limits": "Cần phân biệt phòng thủ vô thức với né trách nhiệm có chủ đích. Hai cái xử lý khác nhau.",
        "analogy": "Giống phản xạ giơ tay đỡ khi ngã: bộ não chặn lỗi trước khi ý thức kịp nghĩ."
    },
    4: {
        "what": "Khách im lặng không có nghĩa là hài lòng. Quyết định quay lại được đưa ra từ ký ức (remembering self), không phải trải nghiệm thực.",
        "why": "Mất khách im lặng là kiểu mất đắt nhất vì không có tín hiệu để sửa. Điểm kết dở quyết định ký ức.",
        "mechanism": [
            "Kahneman, Fredrickson, Schreiber & Redelmeier (1993) peak-end rule: ký ức = đỉnh cảm xúc + đoạn kết",
            "Kahneman (2011): experiencing self trải nghiệm tốt, nhưng remembering self quyết định quay lại hay không",
            "Giao trễ một ngày + không ai hỏi thăm = điểm kết dở ghi vào ký ức",
            "Vòng lặp: không hỏi → không biết điểm kết dở → không sửa → khách đi âm thầm → đổ cho 'thị trường khó'"
        ],
        "players": ["Khách hàng", "Điểm kết trải nghiệm", "Ký ức (remembering self)", "Đỉnh cảm xúc (peak)", "Công ty"],
        "applications": [
            "Gọi hỏi thăm 3-7 ngày sau giao hàng để bắt điểm kết dở",
            "Chăm sóc sau bán: xác nhận đã nhận, dùng thử thế nào, cần gì thêm",
            "Biến mọi kết thúc thành tích cực: hướng dẫn, khuyến mãi quay lại, lời cảm ơn"
        ],
        "limits": "Peak-end rule mạnh nhưng không phủ toàn bộ quyết định. Giá trị sản phẩm dài hạn vẫn quyết định.",
        "analogy": "Giống phim: dở suốt hai tiếng nhưng kết hay, người ta nhớ là phim hay. Và ngược lại."
    },
    5: {
        "what": "Giữ người cũ không theo kịp vì ba cái neo: chi phí chìm, cam kết nhất quán, sợ mất. Không phải vì giá trị thực.",
        "why": "Né quyết định → lỗi tiếp tục → team bực → càng áy náy càng né. Người cũ mòn trong vai trò cũ, cả hai phía đều thiệt.",
        "mechanism": [
            "Arkes & Blumer (1985) sunk cost: tiếc 12 năm đã bỏ → giữ quyết định sai để không phí phạm quá khứ",
            "Cialdini (1984) commitment & consistency: đã nói 'anh em trong nhà' → bộ não muốn nhất quán → né quyết định khó",
            "Kahneman & Tversky (1979) loss aversion: nỗi đau khi mất nặng gấp đôi niềm vui khi được",
            "Vòng lặp: né → lỗi tiếp → team bực → áy náy → né sâu hơn"
        ],
        "players": ["Leader (Quang)", "Người cũ (Chú Tư)", "Sunk cost", "Cam kết & nhất quán", "Loss aversion"],
        "applications": [
            "Tách lòng trung thành khỏi năng lực: ghi nhận cống hiến, chuyển vai trò phù hợp",
            "Nói thẳng bằng kịch bản: 'cảm ơn 12 năm, đây là vai trò mới phù hợp năng lực hiện tại'",
            "Đặt chuẩn năng lực cho vai trò, không đặt theo tuổi thâm niên"
        ],
        "limits": "Trung thành có giá trị thật. Vấn đề là giữ người ở sai vai trò, không phải giữ người.",
        "analogy": "Giống giữ chiếc xe cũ vì đã đi 12 năm: tiếc là thật, nhưng mỗi km mới đều đắt hơn xe mới."
    },
    6: {
        "what": "Một người trễ giờ không ai nói là tín hiệu 'trễ là bình thường'. Cả team học theo chuẩn mực mô tả, không tự nhiên lỏng lẻo.",
        "why": "Im lặng của leader chính là phần thưởng duy trì hành vi. Xử lý muộn và xử lý tập thể làm bất mãn lan ra.",
        "mechanism": [
            "Cialdini, Reno & Kallgren (1990) descriptive norms: con người quyết định theo 'người khác đang làm gì'",
            "Skinner (1953): hành vi không bị phản ứng thì được duy trì → im lặng = thưởng",
            "Vòng xoáy: 1 người trễ → 3 người trễ → xử lý tập thể → người vô tội bị phạt oan → bất mãn → càng lơ"
        ],
        "players": ["Nhân viên trễ (Tùng)", "Người học theo (Hùng, Mai)", "Chuẩn mực mô tả", "Sự im lặng của leader", "Xử lý tập thể"],
        "applications": [
            "Xử lý ngay vi phạm đầu tiên, riêng tư, đúng người: 'tuần này em trễ 3 lần, có chuyện gì không?'",
            "Không xử lý tập thể: chỉ đúng người, tránh phạt oan",
            "Leader nói rõ chuẩn mực mong muốn bằng lời và hành vi nhất quán"
        ],
        "limits": "Không phải vi phạm nhỏ nào cũng cần xử lý ngay. Phân biệt lỗi hệ thống và lỗi cá nhân lặp lại.",
        "analogy": "Giống vết rạn nhỏ trên tường: không vá thì cả mảng tường theo nhau nứt."
    }
}

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def push(idx):
    path = f"C:/Users/NTQUANG_DELL/hermes-temp/psy_2026-08-13/psy_{idx}.txt"
    with open(path, encoding="utf-8-sig") as f:
        content = f.read().strip()
    title = content.splitlines()[0].strip()
    ov = OVERVIEWS[idx]
    block = "<!--OVERVIEW-->" + json.dumps(ov, ensure_ascii=False) + "<!--/OVERVIEW-->\n\n"
    new_content = block + content
    body = json.dumps({"title": title, "content": new_content, "topic_slug": SLUG, "source_url": ""}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(f"{BASE}/api/knowledge", data=body, headers={
        "Authorization": AUTH, "Content-Type": "application/json", "Cookie": COOKIE})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=25)
    return json.loads(resp.read().decode())

for i in range(1, 7):
    try:
        r = push(i)
        print(f"OK psy_{i} -> {r.get('id', r)}")
    except Exception as e:
        err = str(e)
        try:
            if hasattr(e, "read"):
                err += " | " + e.read().decode()[:300]
        except Exception:
            pass
        print(f"ERR psy_{i}: {err}")
