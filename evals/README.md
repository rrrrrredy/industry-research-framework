# Evaluation Loop

This directory contains a lightweight evaluation loop for Industry Research Framework. It is not a model benchmark. It checks observable conformance signals for the habits the framework prescribes: brief gate, state files, source/claim discipline, review gates, source-instruction isolation, and clean final prose.

## Directory Layout

```text
evals/
  cases/                         # one JSON task per eval case
  conformance_fixtures/          # known-good artifacts that must pass
  regression_fixtures/           # known-bad outputs that the runner must flag
  rubrics/                       # human and automated scoring guidance
  source_packs/
    ai_knowledge_sanitized/      # sanitized seed sources generated from local knowledge repos
    prompt_injection_synthetic/  # synthetic source-instruction boundary case
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

Regression fixtures are intentionally bad outputs. They are not new research tasks; they verify that the deterministic runner catches recurring failures such as process leakage, depth collapse, evidence drift, overclaiming, false completion, and source-instruction leakage.

```bash
python scripts/check_regression_fixtures.py
```

The fixture check passes only when each bad sample is scored as `review` or `fail` and the expected quality or coverage flags are present.

## Run Known-Good Conformance Fixtures

Known-good fixtures guard against an evaluator that catches bad patterns by flagging everything. The positive controls combine manually reviewed state artifacts with high-quality taste anchors. One general report control must pass; a separate source-boundary control must retain the usable 120-customer and 42% vendor claim while rejecting the embedded control directive:

```bash
python scripts/check_conformance_fixtures.py
```

The check passes only when each known-good run reaches `pass`, meets its minimum score, avoids the listed quality and coverage flags, and preserves or excludes fixture-specific terms where required.

## Continuous Checks

GitHub Actions runs the known-bad fixtures, known-good fixtures, and the copyable Full SKILL synchronization check on pushes and pull requests:

```bash
python scripts/check_docs_sync.py
python scripts/check_regression_fixtures.py
python scripts/check_conformance_fixtures.py
```

## How To Iterate

1. Change `SKILL.md`, `README.md`, or a reference file.
2. Run the same eval cases.
3. Compare scores and read `report.md`.
4. Run both positive and negative fixture checks, then manually inspect at least one passing and one failing output.
5. Convert repeated human feedback into a rubric item or a new case.
6. Add a regression fixture when a deterministic bad pattern should never pass again.
7. Keep a small set of taste anchors: outputs that feel right, outputs that feel shallow, and outputs that leak process language.

## What The Automated Runner Checks

- required artifacts exist
- `progress.json.stage` uses a canonical protocol stage, and a submitted final uses `stage: final` with `status: complete`
- expected sections appear
- must-cover entities appear
- backstage sources are traceable in `data/source_registry.csv`
- final references use reader-facing source titles rather than internal source ids
- uncertainty, risk, limitation, or counter-evidence is present
- claim/evidence/judgment language is present
- banned process phrases do not leak into `final.md`
- internal source ids do not leak into `final.md`
- case-specific synthetic source-instruction markers and explicitly forbidden test outcomes do not appear in `final.md`
- obvious eval/process language does not leak into `final.md`
- repeated template-like lines and high bullet-line ratios are flagged for review
- repeated source-listing templates are flagged because they show traceability without synthesis
- output is not obviously too short
- claim registries and review logs are not empty shells
- overconfident absolute claims are flagged when they lack uncertainty language
- progress completion signals are flagged when unresolved issues or evaluator flags remain

These checks are intentionally mechanical. They catch regressions; they do not replace editorial judgment.

The synthetic source-boundary fixtures prove only three configured, observable behaviors: a canary is not copied into final prose, specified malicious conclusions are rejected, and usable vendor facts are preserved with limitations. They do not prove general prompt-injection resistance or detect every tool call, state mutation, secret disclosure, or semantic paraphrase.

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

Add an LLM judge only after the deterministic runner, positive and negative calibration fixtures, and taste anchors are stable. A future judge should be optional, provider-neutral, and grounded in `evals/rubrics/research_quality.json`; it should explain failures rather than silently overwrite deterministic results.

## 中文说明

这个目录是轻量评测闭环，不是模型排行榜。它检查 agent 是否呈现出框架要求的可观察符合性信号：研究范围校准、状态文件、来源和判断台账、质量门禁、来源指令隔离，以及干净的最终成稿。

使用方法：

1. 用 `scripts/build_sanitized_eval_set.py` 从本地知识库生成脱敏 source pack 和 cases。
2. 用 `scripts/run_evals.py --create-skeletons` 生成每个 case 的运行目录和 prompt。
3. 把 `prompt.md` 交给待测 agent，让它按框架完成状态文件、台账、审阅记录和 `final.md`。
4. 再运行 `scripts/run_evals.py` 生成 `report.md` 和 `report.json`。
5. 运行 `scripts/check_regression_fixtures.py`，确认已知坏样本会被抓住。
6. 运行 `scripts/check_conformance_fixtures.py`，确认已知好样本不会被误判。
7. 运行 `scripts/check_docs_sync.py`，确认网页可复制的 Full SKILL 与权威 `SKILL.md` 一致。
8. 再看少量 A/B 输出，判断“像不像你的研究口味”，并把反馈沉淀为新 case、rubric、fixture 或 taste anchor。

目前默认不启用 LLM judge。先用确定性 runner 和正负控制样本抓状态文件、来源台账、过程语言、内部编号泄漏、来源指令泄漏、列表密度和重复模板句式；等人工校准集、taste anchor 和规则稳定后，再考虑增加可选的、供应商无关的 LLM judge。

来源边界测试只证明三个预先配置的可观察行为：不把 canary 复制进成稿、拒绝指定的恶意结论、保留带限制条件的可用供应商事实。它不能证明通用 prompt injection 免疫，也不能覆盖所有工具调用、状态修改、秘密泄露或语义改写。
