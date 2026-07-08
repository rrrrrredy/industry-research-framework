# Evaluation Loop

This directory contains a lightweight evaluation loop for Industry Research Framework. It is not a model benchmark. It checks whether an agent using the framework actually preserves the habits the framework is supposed to enforce: brief gate, state files, source/claim discipline, review gates, and clean final prose.

## Directory Layout

```text
evals/
  cases/                         # one JSON task per eval case
  regression_fixtures/            # known-bad outputs that the runner must flag
  rubrics/                       # human and automated scoring guidance
  source_packs/
    ai_knowledge_sanitized/      # sanitized seed sources generated from local knowledge repos
  runs/                          # local eval outputs, ignored by git if desired
```

## Rebuild The Sanitized Source Pack

If you have local copies of `aiknowledge-cli` and `ai-knowledge-graph`, rebuild the source pack and cases:

```bash
python scripts/build_sanitized_eval_set.py \
  --aiknowledge-cli /path/to/aiknowledge-cli \
  --knowledge-graph /path/to/ai-knowledge-graph
```

On Windows PowerShell:

```powershell
python scripts/build_sanitized_eval_set.py `
  --aiknowledge-cli D:\path\to\aiknowledge-cli `
  --knowledge-graph D:\path\to\ai-knowledge-graph
```

The builder removes internal KM URLs, original internal document IDs, emails, phone numbers, and internal knowledge-system labels. The generated pack is still a workflow eval seed, not a public factual authority.

## Run An Eval

Create run folders and prompts:

```bash
python scripts/run_evals.py --create-skeletons --allow-missing-output --runs-dir evals/runs
```

For each case, give `evals/runs/<case_id>/prompt.md` to the agent under test. The agent should fill:

```text
state/task_spec.md
state/progress.json
data/source_registry.csv
data/claims_registry.csv
logs/review.jsonl
final.md
```

Then score the run:

```bash
python scripts/run_evals.py --runs-dir evals/runs --report evals/runs/report.md
```

The runner writes:

```text
evals/runs/report.md
evals/runs/report.json
```

## Run Regression Fixtures

Regression fixtures are intentionally bad outputs. They are not new research tasks; they verify that the deterministic runner catches recurring failures such as process leakage, depth collapse, evidence drift, overclaiming, and false completion.

```bash
python scripts/check_regression_fixtures.py
```

The fixture check passes only when each bad sample is scored as `review` or `fail` and the expected quality or coverage flags are present.

## How To Iterate

1. Change `SKILL.md`, `README.md`, or a reference file.
2. Run the same eval cases.
3. Compare scores and read `report.md`.
4. Manually inspect at least one passing and one failing output.
5. Convert repeated human feedback into a rubric item or a new case.
6. Add a regression fixture when a deterministic bad pattern should never pass again.
7. Keep a small set of taste anchors: outputs that feel right, outputs that feel shallow, and outputs that leak process language.

## What The Automated Runner Checks

- required artifacts exist
- expected sections appear
- must-cover entities appear
- backstage sources are traceable in `data/source_registry.csv`
- final references use reader-facing source titles rather than internal source ids
- uncertainty, risk, limitation, or counter-evidence is present
- claim/evidence/judgment language is present
- banned process phrases do not leak into `final.md`
- internal source ids do not leak into `final.md`
- obvious eval/process language does not leak into `final.md`
- repeated template-like lines and high bullet-line ratios are flagged for review
- repeated source-listing templates are flagged because they show traceability without synthesis
- output is not obviously too short
- claim registries and review logs are not empty shells
- overconfident absolute claims are flagged when they lack uncertainty language
- progress completion signals are flagged when unresolved issues or evaluator flags remain

These checks are intentionally mechanical. They catch regressions; they do not replace editorial judgment.

## LLM Judge Status

This repo does not enable an LLM judge by default. The first line of defense is deterministic:

- artifact presence
- source registry coverage
- reader-facing references
- process-language leakage
- internal source-id leakage
- bullet density
- repeated source-listing templates
- output length

Add an LLM judge only after the deterministic runner and taste anchors are stable. A future judge should be optional, provider-neutral, and grounded in `evals/rubrics/research_quality.json`; it should explain failures rather than silently overwrite deterministic results.

## 中文说明

这个目录是轻量评测闭环，不是模型排行榜。它评估的是 agent 是否真的遵守了本框架：是否做研究范围校准、是否保留状态文件、是否维护来源和判断台账、是否运行质量门禁、最终成稿是否干净。

使用方法：

1. 用 `scripts/build_sanitized_eval_set.py` 从本地知识库生成脱敏 source pack 和 cases。
2. 用 `scripts/run_evals.py --create-skeletons` 生成每个 case 的运行目录和 prompt。
3. 把 `prompt.md` 交给待测 agent，让它按框架完成状态文件、台账、审阅记录和 `final.md`。
4. 再运行 `scripts/run_evals.py` 生成 `report.md` 和 `report.json`。
5. 运行 `scripts/check_regression_fixtures.py`，确认已知坏样本会被抓住。
6. 你只需要看少量 A/B 输出，判断“像不像你的研究口味”；我可以把这些反馈沉淀为新 case、rubric、regression fixture 或 taste anchor。

目前默认不启用 LLM judge。先用确定性 runner 抓状态文件、来源台账、过程语言、内部编号泄漏、列表密度和重复模板句式；等 taste anchor 和规则稳定后，再考虑增加可选的、供应商无关的 LLM judge。
