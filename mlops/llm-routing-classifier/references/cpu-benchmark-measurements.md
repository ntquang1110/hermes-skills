# CPU benchmark measurements — GLiFormer / GLiClass on Haswell laptop

Direct measurements, not vendor claims. Hardware: Intel i7-4910MQ (4C/8T, 2013 Haswell), 15.9 GB RAM, Windows 10, no GPU usable by modern torch (Quadro K2100M is Kepler; current PyTorch dropped it). Python 3.12.13 via uv, torch 2.14.0, transformers 5.17.0.

## GLiFormer (the model jeff serves)

| Case | 150M base | 400M large |
|---|---|---|
| Load | 7.5 s | 20.8 s |
| Short query, 77 tok, bs=1 | 411 ms | **823 ms** |
| Short query, 77 tok, bs=8 | 250 ms/text | 477 ms/text |
| Long query, 797 tok, bs=1 | 4.19 s | **9.52 s** |
| Full engine request (state + 3 questions, 128 in-tok) | 621 ms | 1.46 s |
| Throughput bs=1 | ~2.4 texts/s | 1.22 texts/s |
| Throughput bs=8 | ~4 texts/s | 2.10 texts/s |
| Peak RSS | ~+2.6 GB over baseline | **11.2 GB** |

The 400M figures began as extrapolation (base × 2.6, the factor the repo itself measured on 8-core x86) and were later confirmed by direct measurement. Run-to-run drift on the 400M: 823-822.9 ms and 9518/9304 ms across two independent runs, so treat these as ±5%.

Batch 8 helps only ~1.7x per text at short length (411→250 for base) and barely at all on the 400M. CPU batching is not a free multiplier here.

## GLiClass multilingual (`knowledgator/gliclass-multilang-ultra`)

| Case | Measured |
|---|---|
| Checkpoint size | 2.5 GB |
| Cold load (includes download + re-init of missing weights) | **994 s** (16.5 min) |
| Per-classification latency | 3.7 - 9.0 s |

During load the library warns that `model.encoder_model.encoder.embed_tokens.weight` is missing and initialises it fresh. That is a packaging defect in the checkpoint and degrades quality independently of language support.

## Vietnamese routing test (5 prompts, 4 agent labels)

Labels: `research`, `sales`, `dev`, `kho vận`.

| Prompt | Expected | Returned |
|---|---|---|
| "Nghiên cứu đối thủ cạnh tranh sản phẩm EZ80" | research | research 0.973 |
| "Gửi email outreach cho khách hàng trang trại Đồng Nai" | sales | sales 0.918 |
| "Sửa lỗi deploy server bị crash khi restart, xem log" | dev | dev 0.898 |
| "Hôm nay anh thấy cái bài viết này hay, em phân tích cho anh" | research (ambiguous) | research 0.914 |
| "Kiểm tra kho hàng còn bao nhiêu bao EZ67" | kho vận | **research 0.863** |

Choice-style gate, the case that actually decides whether an LLM is needed:

| Prompt | Expected | Returned |
|---|---|---|
| "Tính toán lợi nhuận tối ưu cho trang trại 500 heo trong 3 năm" | needs a large model | "câu hỏi đơn giản, trả lời ngắn" **0.134** |
| "Giá EZ80 bao nhiêu?" | simple | "câu hỏi đơn giản" 0.746 |

Reading: 3/5 correct on multi-label routing, and the single decision that matters for cost control (complex vs simple) is wrong with very low confidence. The model is matching on familiar keywords, not understanding the sentence. Do not ship a Vietnamese router on either checkpoint without fine-tuning on your own labelled text.

## ONNX int8 branch (verified)

| Step | Result |
|---|---|
| `encoder.onnx` export, 150M base | 736 MB in 14.4 s |
| Parity vs torch, unseen shape | max abs diff **2.48e-05** (repo threshold < 1e-3) |
| `encoder.int8.onnx` quantize | 645 MB in 29.2 s |
| fp32 nodes retained | 24 MatMuls (FFN output projections) |

## Reproduction

```bash
# separate venv; PYTHONPATH must be cleared first or numpy breaks
unset PYTHONPATH
uv venv --python 3.12 .venv
uv pip install --python .venv gliformer==0.1.2 gliner==0.2.29 transformers onnx onnxruntime

# probe: prints JSON lines per stage (load, bench, engine_e2e, final_rss_mb)
PYTHONPATH=src python probe_cpu.py "D:/models/gliformer-large-v1" torch 8
```

Two invocation traps cost real time and are both pure syntax problems, not code problems:

1. `PYTHONPATH=src` is required to `import jeff` from a `src/`-layout checkout that is not pip-installed. Without it you get `ModuleNotFoundError: No module named 'jeff'` from scripts that otherwise work.
2. `from_pretrained` needs `D:/models/...`, not `/d/models/...`. An MSYS path is parsed as a HuggingFace repo id and raises `HFValidationError`.

Also: `torch.jit.script is deprecated` warnings come from gliformer's import path on both 3.12 and 3.14. They are noise on 3.12 and a genuine unsupported-path risk on 3.14 (the repo pins `>=3.12,<3.13`; upstream tests still pass 15 + 7 on both, so don't rewrite the pin just to satisfy 3.14).
