#!/bin/bash
# =============================================================================
# compress-audio.sh — Nén file audio/video xuống dưới 20MB
# =============================================================================
# Usage:
#   compress-audio.sh <input_file> [output_file]
#
# If output_file omitted, writes to <input_basename>.compressed.ogg
# in the same directory as the input file.
#
# Dependencies: ffmpeg, ffprobe
# Platform: Windows (git-bash / MSYS2)
# =============================================================================

set -euo pipefail

INPUT="$1"
OUTPUT="${2:-"${INPUT%.*}.compressed.ogg"}"
TARGET_MB=20
SAFE_MB=18  # Dư 2MB cho overhead

# --- Hàm lấy dung lượng file (Windows-compatible) ---
get_filesize_bytes() {
    # `stat -c%s` không hoạt động trên MSYS2, dùng ls + awk / wc -c
    wc -c < "$1" 2>/dev/null | tr -d ' '
}

# --- Kiểm tra ffmpeg ---
if ! command -v ffmpeg &>/dev/null; then
    echo "ERROR: ffmpeg not found. Install ffmpeg first."
    exit 1
fi

# --- Kiểm tra file đầu vào ---
if [ ! -f "$INPUT" ]; then
    # Thử với MSYS path translation
    if [ -f "/$(echo "$INPUT" | sed 's/\\/\//g; s/://')" ]; then
        INPUT="/$(echo "$INPUT" | sed 's/\\/\//g; s/://')"
    else
        echo "ERROR: Input file not found: $INPUT"
        exit 1
    fi
fi

# --- Lấy thông tin file ---
FILESIZE_BYTES=$(get_filesize_bytes "$INPUT")
FILESIZE_MB=$(( FILESIZE_BYTES / 1048576 ))
echo "📁 Input: $(basename "$INPUT")"
echo "📏 Size: ${FILESIZE_MB}MB (${FILESIZE_BYTES} bytes)"

# --- Xác định loại file ---
EXT="${INPUT##*.}"
EXT_LOWER=$(echo "$EXT" | tr '[:upper:]' '[:lower:]')
AUDIO_EXTS="mp3 wav ogg opus m4a wma aac flac"

# --- Nếu đã < 20MB và là audio thuần thì bỏ qua ---
if [ "$FILESIZE_MB" -lt "$TARGET_MB" ]; then
    if echo "$AUDIO_EXTS" | grep -qw "$EXT_LOWER"; then
        echo "✅ File < ${TARGET_MB}MB và là audio thuần → không cần nén"
        if [ "$OUTPUT" != "$INPUT" ]; then
            cp "$INPUT" "$OUTPUT"
            echo "✅ Copied to: $OUTPUT"
        else
            echo "✅ Không cần xử lý"
        fi
        exit 0
    fi
fi

# --- Lấy duration (giây) bằng ffprobe ---
DURATION=$(ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 "$INPUT" 2>/dev/null || echo "0")
DURATION_INT=${DURATION%.*}  # Bỏ phần thập phân

if [ -z "$DURATION_INT" ] || [ "$DURATION_INT" -le 0 ]; then
    echo "⚠️  Không đọc được duration, dùng bitrate mặc định 24k"
    BITRATE="24k"
else
    echo "⏱️  Duration: ${DURATION_INT}s ($(( DURATION_INT / 60 ))ph $(( DURATION_INT % 60 ))s)"

    # Tính bitrate để đảm bảo < SAFE_MB (18MB)
    MAX_BYTES=$(( SAFE_MB * 1024 * 1024 ))
    MAX_BITS=$(( MAX_BYTES * 8 ))
    CALC_BITRATE=$(( MAX_BITS / DURATION_INT / 1000 ))  # kbps

    # Giới hạn bitrate: min 16k (nghe được speech), max 64k (dư quality)
    if [ "$CALC_BITRATE" -lt 16 ]; then
        BITRATE="16k"
        echo "⚠️  File rất dài → nén xuống 16kbps (vẫn nghe rõ speech)"
    elif [ "$CALC_BITRATE" -gt 64 ]; then
        BITRATE="64k"
        echo "🔊 File ngắn → giữ chất lượng 64kbps"
    else
        BITRATE="${CALC_BITRATE}k"
        echo "🎯 Bitrate mục tiêu: ${BITRATE}"
    fi
fi

# --- Nén ---
echo "🔄 Đang nén... (có thể mất vài phút với file dài)"
# Xuất ra file tạm rồi rename để tránh lỗi đường dẫn
TMP_OUTPUT="${OUTPUT}.tmp.ogg"
ffmpeg -y -v error -stats \
    -i "$INPUT" \
    -vn              `# Bỏ video track nếu có` \
    -ac 1            `# Mono (đủ cho speech)` \
    -ar 16000        `# 16kHz (chuẩn Whisper)` \
    -c:a libopus     \
    -b:a "$BITRATE"  \
    -application voip `# Tối ưu hóa cho speech` \
    "$TMP_OUTPUT"

# --- Kiểm tra kết quả ---
if [ ! -f "$TMP_OUTPUT" ]; then
    echo "❌ Nén thất bại!"
    exit 1
fi

mv "$TMP_OUTPUT" "$OUTPUT"

OUT_BYTES=$(get_filesize_bytes "$OUTPUT")
OUT_MB=$(( OUT_BYTES / 1048576 ))
SAVED=0
if [ "$FILESIZE_BYTES" -gt 0 ]; then
    SAVED=$(( 100 - (OUT_BYTES * 100 / FILESIZE_BYTES) ))
fi

echo "✅ Nén hoàn tất!"
echo "📁 Output: $OUTPUT"
echo "📏   ${FILESIZE_MB}MB → ${OUT_MB}MB (giảm ${SAVED}%)"

if [ "$OUT_MB" -ge "$TARGET_MB" ]; then
    echo "⚠️  File vẫn >= ${TARGET_MB}MB! Cần chunk nhỏ hơn hoặc giảm thêm bitrate."
fi
