# Longform Industry Research Protocol

A protocol framework for longform, source-backed industry research and publishable writing by AI agents.

It ships no scraper, data source, or fixed report template. Instead, it prescribes conventions for how an agent persists state, separates evidence from prose, avoids topic drift, schedules review, and turns a large research backend into a clean reader-facing article or report.

Task State Source Registry Claim Discipline Staged Drafting Review Loop Reader Revision

[Open protocol page](https://rrrrrredy.github.io/longform-industry-narrative-research/framework.html#fullmd)

## 01 Motivation: Four Failure Modes

Longform research agents tend to fail in four recurring ways:

1. **Topic overfitting**: a method distilled from one project becomes falsely treated as the universal frame.
2. **Process leakage**: the final article reads like a work log.
3. **Evidence drift**: sources, claims, uncertainty, and author judgment collapse into one narrative.
4. **False completion**: a partial milestone is reported as final completion before coverage, review, and reader-quality revision are done.

Every mechanism in this protocol targets one of those failures.

## 02 Behavioral Constraints

Hard rules of the protocol:

- Deliverable first: if the output is an article or report, do not drift into system design.
- State before scale: write task state before expanding source collection.
- Evidence is not prose: registries and audit labels stay backstage.
- Staged execution: plan, collect, analyze, draft, review, revise, then continue.
- Optional lenses only: narrative analysis and horizontal-vertical analysis are tools, not default structure.
- Review closes the loop: every audit finding becomes a revision action, downgraded claim, or explicit limitation.
- Reader review comes last: improve readability after factual and coverage checks are stable.

## 03 Architecture

```text
Main Agent
  owns thesis, structure, final judgment

Research Backend
  state files
  source registry
  claim registry
  uncertainty list
  review logs

Publishing Frontend
  thesis
  analytical sections
  synthesis
  counter-evidence
  reader-facing references
  final prose cleanup
```

Subagents may inspect or challenge bounded parts of the backend, but the main agent owns the argument and final prose.

## 04 State File System

```text
{task}/state/
  task_spec.md
  progress.json
  findings.jsonl
  directions_tried.json
  iteration_log.jsonl

{task}/logs/
  work.jsonl
  review.jsonl

{task}/data/
  source_registry.csv
  claims_registry.csv
  uncertainty_registry.csv
```

Use state files to recover after context loss. Do not rely on chat history as the only memory.

## 05 Operating Loop

1. Plan the scope, inputs, output, and done criteria.
2. Collect or process only the sources needed for that stage.
3. Convert sources into claims, uncertainty, and analysis notes.
4. Draft a bounded section or unit.
5. Review the section for evidence, coverage, structure, skepticism, and prose.
6. Revise the section and registries.
7. Update progress and define the next stage.

If one cycle adds no new evidence, case, counterexample, framework, or judgment, increment `stale_count`. If `stale_count >= 2`, pivot the structural angle rather than searching harder inside the same frame.

## 06 Analysis Lens Scheduling

Choose the lens that fits the research question:

- narrative analysis
- horizontal-vertical analysis
- adoption analysis
- capital analysis
- organization/talent analysis
- policy/legitimacy analysis
- counter-case analysis

Pick one primary lens and at most two secondary lenses unless the user explicitly requests a multi-method report.

## 07 Subagent And Review Scheduling

Use subagents for bounded work only:

- requirement mapping
- source discovery
- evidence-chain verification
- coverage audit
- skeptical review
- structure review
- reader-quality review

Subagents should not rewrite the whole report or own the thesis.

## 08 Engineering Constraints

- Every important hard claim needs a confidence boundary.
- Every 20 important facts, figures, or judgments should update source and claim registries.
- Official materials show stated position; they do not prove adoption.
- Media materials show public framing; they need corroboration for hard facts.
- User/community evidence shows reception; it is not automatically representative.
- Reader review may improve flow and clarity, but must not invent facts.

## 09 Validation And Limits

Before declaring completion:

- Required coverage is complete or limitations are explicit.
- Major claims trace back to sources or uncertainty records.
- Facts, source claims, interpretations, and author judgments remain distinct.
- Counter-evidence has been addressed.
- Reader review has been run after factual and coverage review.
- Final prose reads like an author's report, not an agent process report.

Limits:

- The protocol reduces citation and evidence errors; it does not eliminate them.
- Subagent review is a check, not external truth.
- Optional lenses can overfit the report if used mechanically.
- State files only work if updated during the task, not reconstructed after the fact.

## 10 Full SKILL.md

The authoritative instruction file is [`SKILL.md`](./SKILL.md). The protocol page includes the full skill text in a copyable block.

## Repository Structure

```text
longform-industry-narrative-research/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── docs/
│   ├── index.html
│   └── framework.html
└── references/
    ├── research-workflow.md
    ├── optional-analysis-lenses.md
    ├── horizontal-vertical-analysis.md
    ├── subagents-and-review-loop.md
    ├── writing-style.md
    ├── quality-gates.md
    └── postmortem-lessons.md
```

## Reuse

Clone or copy this repository into the directory where your agent system loads reusable skills or instruction bundles:

```bash
git clone https://github.com/rrrrrredy/longform-industry-narrative-research.git \
  ./agent-skills/longform-industry-research
```

For systems without a formal skill loader, use `SKILL.md` as the main instruction file and load files under `references/` only when the task requires them.

---

# 中文说明：长篇产业研究协议

这是一个面向 AI agent 的长篇产业研究与写作协议，用于处理资料量大、周期长、需要形成可发布文章或研究报告的任务。

它不是抓取工具、数据源、固定报告模板，也不是只服务于“叙事研究”的方法。它的作用是规定一套可复用的研究执行约束：agent 如何保存任务状态、如何区分来源与判断、如何分阶段写作、如何进行审计与读者视角修订，以及如何把复杂的后台研究整理成干净的前台文章。

## 01 动机：四类常见失败

长篇研究任务中，agent 很容易出现四类问题：

1. **方法过拟合**：从一个具体项目中提炼出的经验，被误当成所有研究任务的默认框架。
2. **过程泄漏**：终稿不像作者写的研究文章，而像“我读取了什么材料、做了什么处理”的工作日志。
3. **证据漂移**：事实、来源说法、媒体解释、不确定性和作者判断混在一起，最后很难追溯。
4. **过早完成**：只完成一个局部阶段，就把它当成整体任务完成。

这个协议里的状态文件、来源台账、判断台账、阶段审计、读者修订，都是为了解决这些问题。

## 02 核心原则

- **交付物优先**：如果用户要的是文章或报告，不要偏移成系统设计、prompt 设计或流程说明。
- **先建状态，再扩资料**：长任务必须把目标、范围、进度、发现、待核项写入文件，而不是只依赖聊天上下文。
- **证据不是正文**：来源台账、审计记录、失败访问、内部 source id 留在后台，不能直接污染终稿。
- **分阶段推进**：规划、收集、分析、写作、审计、修订、更新状态，按阶段循环。
- **方法按需选择**：叙事分析、横纵分析、资本分析、采用分析都是可选镜头，不是默认结构。
- **审计必须闭环**：每个审计问题都要变成具体修改动作、降级后的判断，或明确的不确定性说明。
- **读者审计最后执行**：先完成事实、覆盖和结构检查，再做可读性、节奏和理解负担优化。

## 03 后台与前台

研究后台包括：

- `state/task_spec.md`
- `state/progress.json`
- `state/findings.jsonl`
- `state/directions_tried.json`
- `logs/work.jsonl`
- `logs/review.jsonl`
- `data/source_registry.csv`
- `data/claims_registry.csv`
- `data/uncertainty_registry.csv`

前台文章包括：

- 核心判断
- 研究范围
- 分析章节
- 跨案例综合
- 反证与边界
- 结论
- 读者可读的参考资料

后台保证可追溯，前台保证可阅读。两者必须分开。

## 04 适用场景

适合用于：

- 公司、产品、市场类别研究
- 技术生态与产业链分析
- 行业竞争格局研究
- 政策、监管与制度分析
- 组织、人才流动与运营模式研究
- 产品采用与用户行为分析
- 商业模式、定价、融资与资本市场分析
- 跨区域、跨市场、跨公司比较研究
- 将大量资料整理成可发布文章或研究报告

不适合用于：

- 简单事实问答
- 单篇文章摘要
- 纯引文格式整理
- 单纯数据清洗
- 没有资料约束的创意写作
- 用户真正想要代码、仪表盘或自动化工具的任务

## 05 与协议页面的关系

完整协议页面在这里：

[Longform Industry Research Protocol](https://rrrrrredy.github.io/longform-industry-narrative-research/framework.html#fullmd)

仓库源码在这里：

[rrrrrredy/longform-industry-narrative-research](https://github.com/rrrrrredy/longform-industry-narrative-research)
