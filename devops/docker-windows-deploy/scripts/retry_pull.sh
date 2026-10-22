#!/bin/bash
# Retry `docker pull` until every image is present (flaky network killer).
# Usage: bash retry_pull.sh ghcr.io/org/app:latest postgres:15 ...
# Exits 0 once all images exist locally. Run in background with notify_on_complete.

IMAGES=("$@")
if [ ${#IMAGES[@]} -eq 0 ]; then
  echo "Usage: $0 <image1> [image2 ...]"
  exit 2
fi

check_present() { docker image inspect "$1" >/dev/null 2>&1; }

echo "=== Docker pull retry loop started: $(date) ==="
attempt=0
while true; do
  attempt=$((attempt + 1))
  all_done=true

  for img in "${IMAGES[@]}"; do
    if check_present "$img"; then
      echo "[OK] $img already present"
      continue
    fi
    all_done=false
    echo "[TRY $attempt] Pulling $img ..."
    docker pull "$img" 2>&1 | tail -3
    if check_present "$img"; then
      echo "[DONE] $img pulled successfully"
    else
      echo "[FAIL] $img failed, will retry"
    fi
  done

  if $all_done; then
    echo "=== ALL IMAGES PULLED: $(date) ==="
    docker images
    exit 0
  fi

  echo "--- attempt $attempt incomplete, waiting 15s ---"
  sleep 15
done
