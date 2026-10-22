# Image routes, and the two `skill/run.py --task plot` bugs

Everything here was verified by running the code, not by reading it.

## 1. Which tasks need an image API

`agents/visualizer_agent.py:38` branches on `"plot" in task_name`:

| `--task` | `use_image_generation` | Renderer | Image API |
|---|---|---|---|
| `plot` | `False` | text model -> matplotlib -> `execute_plot_code_worker` | none |
| `diagram` | `True` | `dispatch_image_generation` | required |

The plot path runs the generated code in a `ProcessPoolExecutor` (`visualizer_agent.py:41`).

## 2. The text-only block for image routes

```python
# utils/generation_utils.py:84
def assert_not_local_openai_image_model(model_name, route_name="image generation"):
    if is_local_openai_model_name(model_name):   # local/ or ollama/
        raise ValueError(f"{model_name!r} uses a local OpenAI-compatible text route. "
                         f"local/ and ollama/ prefixes are text-only and cannot be used for {route_name}.")
```

`dispatch_image_generation` (`generation_utils.py:998`) has exactly four routes, in priority order:

1. model name containing `gpt-image` -> `openai_client.images.generate`
2. `openrouter_client` initialized -> OpenRouter
3. `orcarouter_client` initialized -> OrcaRouter
4. fallback -> Gemini

There is no local image route. `include_gpt_image` is a per-caller flag, and the Polish agent excludes route 1.

## 3. Bug: `--task plot` is silently ignored

Running `skill/run.py --task plot` dies with:

```
RuntimeError: Gemini client was not initialized: missing Google API key.
  generation_utils.py:1067 in dispatch_image_generation
  visualizer_agent.py:137 in process
```

So it took the image branch despite `--task plot`.

**Cause.** `skill/run.py:287` builds the config without `task_name`, so it defaults to `Literal["diagram"]` (`utils/config.py:33`).

```python
    exp_config = config.ExpConfig(
        dataset_name="Demo",
        task_name=args.task,   # <-- ADD THIS LINE
        split_name="demo",
```

**Second bug, same file.** `extract_final_image_b64` hardcoded `task_name = "diagram"` at `run.py:246`, so even a successful plot run would look for `target_diagram_*` while the agents wrote `target_plot_*`.

```python
def extract_final_image_b64(result: dict, exp_mode: str, task_name: str = "diagram") -> str | None:
    prefix = f"target_{task_name}"
    ...
        b64 = extract_final_image_b64(result, exp_mode, args.task)   # call site ~line 342
```

The default keeps it backward compatible. Both patches are applied in the clone at `~/research-lab/repos/PaperBanana`, and `pytest tests/ -q` still reports **135 passed** afterwards.

`main.py` is unaffected — it passes `task_name=args.task_name` correctly at `main.py:100`.

## 4. What the local plot path actually produced

After both patches, `--main-model-name ollama/qwen2.5:3b --retrieval-setting none`:

```
[Retriever] Done. Retrieved 0 references.
Error executing plot code: keyword grid_axis is not recognized; valid keywords are [...]
[Critic] No valid image found for round 0. Using text-only critique mode.
[Critic Round 0] No changes needed. Stopping iteration.
WARNING: No image produced for candidate 0.
```

**30 min 31 s, exit code 0, no image.** What it proves:

1. **The route is sound.** It never called `dispatch_image_generation`. It asked the text model for matplotlib code and ran it locally. No image API was involved at all.
2. **`qwen2.5:3b` is too weak.** It emitted an invalid matplotlib keyword, the exec failed, nothing rendered. The blocker is text-model quality, not the missing image API.
3. **The failure is silent.** Exit code 0 with no artifact.

Ollama also defaults to `context_length: 4096` and ran with `size_vram: 0` (CPU only). PaperBanana's prompts exceed 4096 and get silently truncated. Raise `OLLAMA_CONTEXT_LENGTH` if you use ollama at all.

## 5. `local/` is not sandboxed to localhost

`local/<model>` means an OpenAI-compatible text endpoint you name yourself, via `base_urls.local_openai_base_url` / `LOCAL_OPENAI_BASE_URL`. Point it at any cheap endpoint:

```bash
export LOCAL_OPENAI_BASE_URL="https://<any-openai-compatible>/v1"
export LOCAL_OPENAI_API_KEY="<key>"
--main-model-name "local/<strong-coder-model>"
```

## 6. Escape hatch for diagrams: `OPENAI_BASE_URL`

`openai_client = AsyncOpenAI(api_key=key)` passes no `base_url`, and the OpenAI SDK falls back to the `OPENAI_BASE_URL` environment variable. Verified against the installed SDK:

```
SDK base_url with OPENAI_BASE_URL set : http://127.0.0.1:9999/v1/
SDK base_url with it unset            : https://api.openai.com/v1/
```

```yaml
# configs/model_config.yaml
api_keys:
  openai_api_key: "anything"      # the SDK requires a non-empty key
```
```bash
export OPENAI_BASE_URL="http://127.0.0.1:8081/v1"
# the image model name must CONTAIN "gpt-image" - that substring is the trigger
$P skill/run.py --task diagram --image-gen-model-name "gpt-image-local" ...
```

The server must implement `POST /v1/images/generations` returning `data[0].b64_json`. LocalAI and SwarmUI have OpenAI-compatible image endpoints; A1111/Forge need a shim (native API is `/sdapi/v1/txt2img`).

**Honest caveat:** open-weight diffusion models render in-image text badly, and a methodology diagram is mostly text labels and arrows. Expect noticeably worse output than Gemini / Nano-Banana. Use this to avoid paid APIs, not for publication quality.
