# Repo provenance: PaperBanana vs PaperVizAgent

Verified 2026-10-21. This is how to re-derive every claim below.

## The two repos

| | `dwzhu-pku/PaperBanana` | `google-research/papervizagent` |
|---|---|---|
| Created | 2026-01-30 | 2026-02-11 |
| Last push | 2026-10-19 | 2026-02-27 |
| Stars | 7,345 | 560 |
| Files (git) | 95 | 37 |
| License | Apache-2.0 | Apache-2.0 |
| Model routes | Gemini, OpenRouter, OrcaRouter, Atlas, OpenAI, local, ollama | Gemini |
| Dataset prep script | `scripts/prepare_bench.py` | absent |
| Tests | 7+ modules, 135 tests | absent |
| Dockerfile | present | present |

Note the ordering: the fork was created **12 days before** Google's official release. The fork's README says it "forked the content of" the Google repo — that describes the current file content, not the GitHub fork lineage. First author Dawei Zhu developed the method during a Google internship; the repo header is still `Copyright 2026 Google LLC`.

## Re-derive the diff

```bash
cd /tmp && mkdir -p pb_cmp && cd pb_cmp
for f in agents/retriever_agent.py agents/planner_agent.py agents/critic_agent.py \
         utils/generation_utils.py prompts/diagram_eval_prompts.py; do
  out=$(echo "$f" | tr '/' '_')
  curl -s "https://raw.githubusercontent.com/google-research/papervizagent/main/$f" -o "g_$out"
  loc=~/research-lab/repos/PaperBanana/$f
  if [ -s "g_$out" ] && [ -s "$loc" ]; then
    printf "%-38s google=%5s dong | local=%5s dong | %s\n" "$f" \
      "$(wc -l < g_$out)" "$(wc -l < $loc)" \
      "$([ "$(md5sum < g_$out)" = "$(md5sum < $loc)" ] && echo GIONG || echo KHAC)"
    diff <(tr -d '\r' < "g_$out") <(tr -d '\r' < "$loc") | grep -cE '^[<>]' \
      | xargs -I{} echo "     {} dong khac"
  fi
done
```

Result at time of check:

```
agents/retriever_agent.py              google=  339 dong | local=  339 dong | KHAC   4 dong khac
agents/planner_agent.py                google=  141 dong | local=  163 dong | KHAC  22 dong khac
agents/critic_agent.py                 google=  235 dong | local=  235 dong | KHAC   4 dong khac
utils/generation_utils.py              google=  464 dong | local= 1189 dong | KHAC 725 dong khac
prompts/diagram_eval_prompts.py        google=  208 dong | local=  208 dong | KHAC   0 dong khac
```

## What the 4-line diffs actually are

`agents/retriever_agent.py` and `agents/critic_agent.py`, both:

```
-        self.model_name = self.exp_config.model_name
+        self.model_name = self.exp_config.main_model_name

-        response_list = await generation_utils.call_gemini_with_retry_async(
+        response_list = await generation_utils.call_model_with_retry_async(
```

Pure rename generalisation: "gemini" → "model". The agent logic is untouched.

## Where the fork's value actually is

- `utils/generation_utils.py` 464 → 1189 lines: the provider abstraction (`openrouter/`, `orcarouter/`, `atlas/`, `local/`, `ollama/`), client construction, image-size tiers, retry logic.
- `demo.py` (49 KB Streamlit) and `app.py` (40 KB Gradio): UI surfaces.
- `tests/`: 135 tests, all about the provider/route layer, not the agents.
- `skill/`: a clawhub-packaged wrapper (`MIT-0`) exposing `run.py`.
- `notebooks/`, `style_guides/generate_category_style_guide.py`.

Residual forks in naming that confirm the lineage: `main.py` docstring says "Main script to launch PaperVizAgent", and `configs/model_config.template.yaml` says "Model and API Configuration for PaperVizAgent".

## Getting upstream, if you actually want it

```bash
git clone --depth 1 https://github.com/google-research/papervizagent.git
cd papervizagent
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
# Gemini key required; no provider layer, no dataset script.
# You must build data/PaperBananaBench yourself before main.py is useful.
```

Prefer upstream only when you need the untouched reference implementation. For any real use, the fork wins — it is the one with the provider layer, the dataset fetcher, and tests.

## Commercial / legal note

The fork's README states: patents have been filed by Google on the specific workflows, this restricts third-party commercial applications using similar logic, and the project is not an officially supported Google product (so not eligible for Google's OSS vulnerability rewards program). Apache-2.0 on the code does not clear the patent question.
