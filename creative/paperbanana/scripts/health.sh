#!/usr/bin/env bash
# Health check for the PaperBanana checkout.
# Usage: bash health.sh [path-to-repo]
# Exits non-zero on the first failed check so it is safe to gate on.
set -u

REPO="${1:-$HOME/research-lab/repos/PaperBanana}"

if [ ! -d "$REPO" ]; then
  echo "FAIL: repo not found at $REPO"
  echo "      git clone https://github.com/dwzhu-pku/PaperBanana.git \"$REPO\""
  exit 1
fi

cd "$REPO" || exit 1
unset PYTHONPATH

# Windows uses Scripts/, POSIX uses bin/. Resolve once.
if [ -x ".venv/Scripts/python.exe" ]; then
  P=".venv/Scripts/python.exe"
elif [ -x ".venv/bin/python" ]; then
  P=".venv/bin/python"
else
  echo "FAIL: no venv python found. Run:"
  echo "      uv venv --python 3.12 .venv && uv pip install --python .venv -r requirements.txt pytest"
  exit 1
fi

fail=0

echo "== python =="
"$P" --version || fail=1

echo "== imports =="
"$P" -c "import agents, utils, prompts; print('  imports OK')" || fail=1

echo "== CLI =="
"$P" skill/run.py --help >/dev/null 2>&1 && echo "  skill/run.py --help OK" || { echo "  FAIL skill/run.py"; fail=1; }

echo "== tests =="
"$P" -m pytest tests/ -q 2>&1 | tail -3 || fail=1

echo "== dataset =="
if [ -f data/PaperBananaBench/diagram/test.json ]; then
  echo "  diagram/test.json present"
else
  echo "  WARN: no dataset. Retriever has no reference set."
  echo "        fix: $P scripts/prepare_bench.py --tasks diagram plot --data-dir data"
fi

echo "== image provider key (--task diagram only) =="
found=""
for k in OPENROUTER_API_KEY GOOGLE_API_KEY ORCAROUTER_API_KEY ATLASCLOUD_API_KEY OPENAI_API_KEY; do
  [ -n "${!k:-}" ] && found="$found $k"
done
if [ -z "$found" ]; then
  if grep -qE '^\s*(openrouter|google|orcarouter|atlascloud|openai)_api_key:\s*"[^"]+"' configs/model_config.yaml 2>/dev/null; then
    echo "  key found in configs/model_config.yaml"
  elif [ -n "${OPENAI_BASE_URL:-}" ]; then
    echo "  OPENAI_BASE_URL=$OPENAI_BASE_URL (local image server route)"
  else
    echo "  WARN: no image-capable key found."
    echo "        --task plot still works fully local (no image API needed)."
    echo "        --task diagram will fail at the Visualizer unless you add one of:"
    echo "        OPENROUTER_API_KEY | GOOGLE_API_KEY | ORCAROUTER_API_KEY | ATLASCLOUD_API_KEY"
    echo "        or set OPENAI_BASE_URL to a local /v1/images/generations server."
  fi
else
  echo "  env:$found"
fi

echo
if [ "$fail" -eq 0 ]; then echo "HEALTH: OK"; else echo "HEALTH: FAILED"; fi
exit "$fail"
