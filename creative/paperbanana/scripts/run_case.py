#!/usr/bin/env python
"""Run PaperBanana on a real PaperBananaBench case, loading API keys from the Hermes .env.

Why this exists: the repo reads keys from env vars (``GOOGLE_API_KEY`` etc.) or from
``configs/model_config.yaml``. Rather than copy secrets into the repo, this driver pulls
them from the Hermes .env at call time and injects them into the child process env.

Usage::

    python run_case.py --case-index 0 --task plot    --ark --out chart.png
    python run_case.py --case-index 0 --task diagram --out fig.png
    python run_case.py --case-index 0 --task plot --ark --dry-run

``--ark`` routes every text agent (Retriever, Planner, Stylist, Visualizer, Critic) to
ByteDance Ark through the repo's ``local/`` OpenAI-compatible route. No OpenRouter, no
Google quota. The Ark key is read from the Hermes ``config.yaml`` at call time, never copied.

Add ``--dry-run`` to print the resolved paths and command without executing.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(os.environ.get("PAPERBANANA_REPO", Path.home() / "research-lab" / "repos" / "PaperBanana"))
HERMES_ENV = Path(os.environ.get(
    "HERMES_ENV", Path.home() / "AppData" / "Local" / "hermes" / ".env"
))
HERMES_CONFIG = Path(os.environ.get(
    "HERMES_CONFIG", Path.home() / "AppData" / "Local" / "hermes" / "config.yaml"
))

# Routing trap: generation_utils.call_model_with_retry_async auto-detects the provider by
# which client got initialized, with priority OpenRouter > OrcaRouter > Gemini > Anthropic
# > OpenAI. So exporting OPENROUTER_API_KEY silently hijacks every unprefixed model name -
# including "gemini-3.1-pro-preview" - over to OpenRouter. Forward only the Google key by
# default, and let the caller opt into the others explicitly.
DEFAULT_KEYS = ("GOOGLE_API_KEY",)
OPT_IN_KEYS = (
    "OPENROUTER_API_KEY",
    "OPENAI_API_KEY",
    "ORCAROUTER_API_KEY",
    "ATLASCLOUD_API_KEY",
    "LOCAL_OPENAI_BASE_URL",
    "LOCAL_OPENAI_API_KEY",
)

# Ark text model used when --ark is passed. Strong at code generation, which is what the
# plot route needs (the model writes matplotlib, the code runs locally).
ARK_DEFAULT_MODEL = "deepseek-v4-pro-ga-260813"
# Which custom_providers entry in config.yaml to read the key from.
ARK_PROVIDER_NAMES = ("ark-v3", "Ark.ap-southeast.bytepluses.com")

DEFAULTS = {
    "diagram": {
        "main": "gemini-3.1-pro-preview",
        "image": "gemini-3.1-flash-image-preview",
    },
    "plot": {
        "main": "gemini-3.1-flash-lite",  # code generation; any solid text model works
        "image": None,  # plot never calls an image model
    },
}


def load_env(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def load_ark(config_path: Path) -> tuple[str, str]:
    """Return (base_url, api_key) for the Ark custom provider in the Hermes config.

    Read from disk at call time so the secret never has to live in the repo or in an
    env var that a shell history would capture.
    """
    if not config_path.exists():
        raise SystemExit(f"ERROR: Hermes config not found at {config_path}")
    text = config_path.read_text(encoding="utf-8", errors="replace")
    for name in ARK_PROVIDER_NAMES:
        m = re.search(
            r"- name:\s*" + re.escape(name) + r"\s*\n\s*base_url:\s*(\S+)\s*\n\s*api_key:\s*(\S+)",
            text,
        )
        if m:
            return m.group(1).rstrip("/"), m.group(2)
    raise SystemExit(
        "ERROR: no Ark provider block in config.yaml. Expected one of "
        f"{ARK_PROVIDER_NAMES} under custom_providers."
    )


def pick_case(task: str, index: int) -> dict:
    """Return one case dict from the bench, mapping plot/diagram to their own files."""
    candidates = [
        REPO / "data" / "PaperBananaBench" / task / "test.json",
        REPO / "data" / "PaperBananaBench" / task / "ref.json",
    ]
    for f in candidates:
        if f.exists():
            data = json.loads(f.read_text(encoding="utf-8"))
            if index >= len(data):
                sys.exit(f"ERROR: index {index} out of range; {f.name} has {len(data)} cases")
            return data[index]
    sys.exit(f"ERROR: no bench file for task={task!r} under {REPO/'data'/'PaperBananaBench'}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", choices=["diagram", "plot"], default="diagram")
    ap.add_argument("--case-index", type=int, default=0)
    ap.add_argument("--out", default="out.png")
    ap.add_argument("--main-model", default=None)
    ap.add_argument("--image-model", default=None)
    ap.add_argument("--rounds", type=int, default=1)
    ap.add_argument("--candidates", type=int, default=1)
    ap.add_argument("--retrieval", default="auto")
    ap.add_argument("--ark", action="store_true",
                    help="route all text agents to ByteDance Ark via the local/ route "
                         "(no OpenRouter, no Google quota)")
    ap.add_argument("--ark-model", default=ARK_DEFAULT_MODEL,
                    help=f"Ark model id for --ark (default {ARK_DEFAULT_MODEL})")
    ap.add_argument("--ark-config", default=None,
                    help="path to the Hermes config.yaml holding the Ark key")
    ap.add_argument("--extra-keys", nargs="*", default=[],
                    help="extra env keys from the Hermes .env to forward "
                         "(e.g. --extra-keys OPENROUTER_API_KEY)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    case = pick_case(args.task, args.case_index)
    d = DEFAULTS[args.task]
    main_model = args.main_model or d["main"]
    image_model = args.image_model or d["image"]

    ark_base = ark_key = None
    if args.ark:
        ark_base, ark_key = load_ark(Path(args.ark_config) if args.ark_config else HERMES_CONFIG)
        main_model = f"local/{args.ark_model}"
        if args.task == "diagram":
            sys.exit(
                "ERROR: --ark is text-only. The diagram route needs an image provider "
                "(gpt-image / OpenRouter / OrcaRouter / Gemini). Use --task plot."
            )

    # Stage the case into a temp content file (avoids shell-quoting a long paper excerpt).
    tmp_dir = Path(os.environ.get("TEMP", Path.home() / "AppData" / "Local" / "Temp"))
    tmp_dir.mkdir(parents=True, exist_ok=True)
    content_file = tmp_dir / f"paperbanana_case_{args.task}_{args.case_index}.md"
    content_file.write_text(str(case.get("content", "")), encoding="utf-8")

    cmd = [
        sys.executable,
        "skill/run.py",
        "--task", args.task,
        "--main-model-name", main_model,
        "--content-file", str(content_file),
        "--caption", str(case.get("visual_intent") or case.get("caption") or "figure"),
        "--output", str(Path(args.out).resolve()),
        "--num-candidates", str(args.candidates),
        "--max-critic-rounds", str(args.rounds),
        "--retrieval-setting", args.retrieval,
    ]
    if image_model:
        cmd += ["--image-gen-model-name", image_model]

    env = dict(os.environ)
    hermes_env = load_env(HERMES_ENV)
    forward = list(DEFAULT_KEYS) + list(args.extra_keys or [])
    for k in forward:
        if hermes_env.get(k):
            env[k] = hermes_env[k]
    for k in OPT_IN_KEYS:
        if k not in forward:
            env.pop(k, None)  # never inherit a hijacking key from the parent shell
    env.pop("PYTHONPATH", None)  # a leaked Hermes PYTHONPATH breaks the repo's imports

    # Ark goes in after the pop loop, otherwise it would be stripped as an opt-in key.
    if args.ark:
        env["LOCAL_OPENAI_BASE_URL"] = ark_base
        env["LOCAL_OPENAI_API_KEY"] = ark_key

    skipped = [k for k in OPT_IN_KEYS if hermes_env.get(k) and k not in forward]
    if skipped:
        print(f"withheld  : {skipped}  (would hijack provider auto-detection; use --extra-keys to opt in)")

    print(f"case      : {case.get('id')}  category={case.get('category')}")
    print(f"gt image  : {case.get('path_to_gt_image')}")
    print(f"gt file   : {REPO / 'data' / 'PaperBananaBench' / args.task / str(case.get('path_to_gt_image'))}")
    print(f"main      : {main_model}")
    print(f"image     : {image_model or '(none - plot renders locally)'}")
    if args.ark:
        print(f"ark base  : {ark_base}")
        print(f"ark key   : <{len(ark_key or '')} chars from {args.ark_config or HERMES_CONFIG}>")
    print(f"keys      : {[k for k in forward if env.get(k)]}")
    print(f"cmd       : {' '.join(cmd)}")

    if args.dry_run:
        return 0

    out = Path(args.out)
    # Multi-candidate runs write <stem>_0.png, <stem>_1.png, ... so the plain --out path may
    # never exist. Clear stale matches first, then verify the whole family, not just one name.
    for stale in out.parent.glob(f"{out.stem}*.png"):
        stale.unlink()

    proc = subprocess.run(cmd, cwd=str(REPO), env=env)
    produced = sorted(out.parent.glob(f"{out.stem}*.png"))
    if produced:
        for q in produced:
            print(f"OK   -> {q}  ({q.stat().st_size:,} bytes)")
        # run.py exits 0 even when the critic bailed and no image was written - trust the files.
        if proc.returncode != 0:
            print(f"note : run.py exit={proc.returncode} but images exist", file=sys.stderr)
        return 0
    print(f"\nFAIL: exit={proc.returncode}, no file matching {out.stem}*.png", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
