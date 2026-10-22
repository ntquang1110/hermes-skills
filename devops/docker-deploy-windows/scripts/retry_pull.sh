#!/bin/bash
# Retry Docker pulls until all images are present (flaky network pattern).
# Usage: edit IMAGES array, run in background, notify_on_complete=true.
# Loop forever until success — each image may succeed on a different attempt.

IMAGES=(
  "ghcr.io/kanbn/kan:latest"
  "postgres:15"
)

check_present() {
  docker image inspect "$1" >/dev/null 2>&1
}

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
