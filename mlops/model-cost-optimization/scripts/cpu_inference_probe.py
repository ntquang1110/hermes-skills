"""CPU inference probe: load a checkpoint, time bs=1 / bs=N / long-context, report system RAM.

Purpose: answer "can this model actually run on this CPU-only host?" with measured numbers
instead of guesses, before promising anything to the user.

Usage (ALWAYS unset PYTHONPATH first — Hermes' PYTHONPATH poisons non-3.11 venvs):
    unset PYTHONPATH
    export PATH="<venv>/Scripts:$PATH"          # or /bin on Linux/mac
    python cpu_inference_probe.py <model_dir> [config] [threads]

    config: torch (default, fp32 eager) | onnx-fp32 | onnx-int8
    threads: torch/OMP thread count (default: none set = torch default)

Adapters it talks to (jeff-shaped repos): jeff.backends.torch_backend.TorchBackend and
jeff.backends.onnx_backend.OnnxBackend. Fork the make_backend() + group spec for other repos.

Reads a REAL model, so expect: 1 GB checkpoint ≈ +2.6 GB RAM, 30 s load on a laptop.
Report the deltas it prints; scale to bigger checkpoints only with a stated factor.
"""

import ctypes
import json
import statistics
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]  # set to the target repo root when copied out
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "bench"))

MODEL = sys.argv[1]
CONFIG = sys.argv[2] if len(sys.argv) > 2 else "torch"
THREADS = int(sys.argv[3]) if len(sys.argv) > 3 else 0


class _MS(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]


def rss_mb():
    """(system_used_mb, system_avail_mb). psapi GetProcessMemoryInfo returned all zeros on
    this host, so use the system-wide counter and report the load delta instead."""
    if sys.platform != "win32":
        import resource  # noqa: PLC0415

        return round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 1), -1.0
    m = _MS()
    m.dwLength = ctypes.sizeof(_MS)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return round((m.ullTotalPhys - m.ullAvailPhys) / 1e6, 1), round(m.ullAvailPhys / 1e6, 1)


def make_backend(cfg, model, threads):
    if cfg.startswith("onnx"):
        from jeff.backends.onnx_backend import OnnxBackend

        return OnnxBackend(model, quant=cfg.split("-", 1)[1], threads=threads or None, batch_size=16)
    from jeff.backends.torch_backend import TorchBackend

    return TorchBackend(
        model, device="cpu", dtype="float32", attn_kernel="eager", batch_size=16, warmup=False
    )


def main():
    import torch

    if THREADS:
        torch.set_num_threads(THREADS)

    print(json.dumps({"stage": "before_load", "rss_mb": rss_mb()}), flush=True)
    t0 = time.time()
    b = make_backend(CONFIG, MODEL, THREADS)
    print(
        json.dumps(
            {"stage": "loaded", "load_s": round(time.time() - t0, 1), "info": b.info(), "rss_mb": rss_mb()}
        ),
        flush=True,
    )

    from jeff.core import Engine, Group
    from jeff.core.schemas import SystemOneRequest

    groups = [
        Group(key="team", labels=("billing", "technical", "sales"), name="Which team should handle this?"),
        Group(key="frustration", labels=("calm", "annoyed", "angry"), name="How frustrated is the customer?"),
        Group(key="refund", labels=("yes", "no"), name="Does the customer request a refund?"),
    ]
    short = (
        "I was charged twice for my subscription this month and support hasn't replied in 3 days. "
        "I need this fixed today or I'm cancelling."
    )
    long = " ".join([short] * 25)  # ~3.5k chars, hard-tier-like state

    for label, text, bs, iters in (
        ("short bs=1", short, 1, 5),
        ("short bs=8", short, 8, 3),
        ("long bs=1", long, 1, 3),
    ):
        texts, gss = [text] * bs, [groups] * bs
        b.score(texts, gss)  # warm this shape
        ts = []
        for _ in range(iters):
            t1 = time.perf_counter()
            out = b.score(texts, gss)
            ts.append(time.perf_counter() - t1)
        ms = 1000 * statistics.median(ts)
        print(
            json.dumps(
                {
                    "stage": "bench",
                    "case": label,
                    "ms_per_batch": round(ms, 1),
                    "ms_per_text": round(ms / bs, 2),
                    "input_tokens": out[0].input_tokens,
                    "texts_per_s": round(1000 * bs / ms, 2),
                    "tokens_per_s": round(1000 * bs * out[0].input_tokens / ms),
                }
            ),
            flush=True,
        )

    # End-to-end through Engine + decode = what the HTTP API actually returns.
    req = SystemOneRequest.model_validate(
        {
            "state": short,
            "model": "jev-latest",
            "questions": {
                "team": {
                    "type": "choice",
                    "instructions": "Which team should handle this?",
                    "criteria": {
                        "billing": "Payment or subscription issues",
                        "technical": "Bugs or integration problems",
                        "sales": "Pricing or account questions",
                    },
                },
                "frustration": {
                    "type": "score",
                    "instructions": "How frustrated is the customer?",
                    "criteria": ["calm", "annoyed", "angry"],
                },
                "refund": {"type": "noul", "instructions": "Does the customer request a refund?"},
            },
        }
    )
    eng = Engine(b, Path(MODEL).name)
    t1 = time.perf_counter()
    resp = eng.run(req)
    print(
        json.dumps(
            {
                "stage": "engine_e2e",
                "ms": round(1000 * (time.perf_counter() - t1), 1),
                "answers": json.loads(resp.model_dump_json()),
            },
            ensure_ascii=False,
            indent=1,
        ),
        flush=True,
    )
    print(json.dumps({"stage": "final_rss_mb", "rss": rss_mb()}), flush=True)


if __name__ == "__main__":
    main()
