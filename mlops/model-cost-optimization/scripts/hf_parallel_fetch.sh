#!/usr/bin/env bash
# Resumable parallel-chunk download for one large HuggingFace file.
#
# WHY: a single `curl -L` on huggingface.co/<repo>/resolve/main/<file> throttles per
# connection (~0.5-1.1 MB/s measured 2026-09-25). N range requests roughly double it
# (~1.7 MB/s with N=8) and each chunk resumes independently.
#
# Usage:
#   bash hf_parallel_fetch.sh <repo> <filename> [out_dir] [n_chunks]
#   bash hf_parallel_fetch.sh knowledgator/gliformer-large-v1 pytorch_model.bin
#
# Re-run the SAME command to resume (curl -C - continues each part.*). Delete part.* to start over.
# Finish with: verify size == Content-Length (the script prints both).
set -u

REPO="${1:?repo, e.g. knowledgator/gliformer-large-v1}"
FILE="${2:?filename, e.g. pytorch_model.bin}"
OUT_DIR="${3:-.}"
N="${4:-8}"

URL="https://huggingface.co/${REPO}/resolve/main/${FILE}"
mkdir -p "$OUT_DIR"
cd "$OUT_DIR" || exit 1

LEN=$(curl -sIL "$URL" | grep -i '^content-length' | tail -1 | tr -d '\r' | awk '{print $2}')
echo "url=$URL"
echo "LEN=$LEN bytes  ($(awk -v l="$LEN" 'BEGIN{printf "%.0f", l/1e6}') MB)  chunks=$N"

CH=$(( (LEN + N - 1) / N ))
: > ranges.txt
for i in $(seq 0 $((N-1))); do
  S=$(( i * CH )); E=$(( S + CH - 1 ))
  [ "$E" -ge "$LEN" ] && E=$(( LEN - 1 ))
  echo "$S $E" >> ranges.txt
done

seq 0 $((N-1)) | xargs -P "$N" -I{} bash -c '
  S=$(awk -v n={} "NR==n+1 {print \$1}" ranges.txt)
  E=$(awk -v n={} "NR==n+1 {print \$2}" ranges.txt)
  curl -sL -C - -o part.{} -r "$S-$E" "'"$URL"'"
  echo "part {} -> $(stat -c %s part.{} 2>/dev/null)"
'

# Assemble only if every chunk is the expected size; otherwise keep part.* and re-run.
ok=1
for i in $(seq 0 $((N-1))); do
  S=$(awk -v n=$((i+1)) 'NR==n {print $1}' ranges.txt)
  E=$(awk -v n=$((i+1)) 'NR==n {print $2}' ranges.txt)
  want=$(( E - S + 1 ))
  got=$(stat -c %s "part.$i" 2>/dev/null || echo 0)
  [ "$got" = "$want" ] || { echo "part.$i incomplete: $got/$want — re-run to resume"; ok=0; }
done

if [ "$ok" = 1 ]; then
  : > "$FILE.tmp"
  for i in $(seq 0 $((N-1))); do cat "part.$i" >> "$FILE.tmp"; done
  mv "$FILE.tmp" "$FILE"
  echo "assembled $FILE size=$(stat -c %s "$FILE") expected=$LEN"
  rm -f part.* ranges.txt
else
  echo "NOT assembled — re-run this same command to resume the missing chunks"
  exit 2
fi
