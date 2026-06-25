# Industry Research Framework

A framework for longform, source-backed industry research and publishable writing by AI agents.

It ships no scraper, data source, or fixed report template. Instead, it prescribes conventions for how an agent persists state, separates evidence from prose, avoids topic drift, schedules review, and turns a large research backend into a clean reader-facing article or report.

Research Brief Task State Source Registry Claim Discipline Staged Drafting Review Loop Reader Revision

[Open framework page](https://rrrrrredy.github.io/industry-research-framework/framework.html#fullmd)

The framework page is the structured reading guide. `SKILL.md` is the authoritative agent instruction file. Files under `references/` are optional modules loaded only when the task needs that method, review loop, or writing guidance.

## 01 Motivation: Five Failure Modes

Longform research agents tend to fail in five recurring ways:

1. **Topic overfitting**: a method distilled from one project becomes falsely treated as the universal frame.
2. **Process leakage**: the final article reads like a work log.
3. **Evidence drift**: sources, claims, uncertainty, and author judgment collapse into one argument.
4. **False completion**: a partial milestone is reported as final completion before coverage, review, and reader-quality revision are done.
5. **Depth collapse**: source counts and coverage checklists pass, but the finished report is too short or compressed for the expected research depth.

Every mechanism in this framework targets one of those failures.

## 02 Behavioral Constraints

Hard rules of the framework:

- Deliverable first: if the output is an article or report, do not drift into system design.
- Research brief gate before collection: ask one compact clarification batch when decision-critical information is missing.
- State before scale: write task state before expanding source collection.
- Evidence is not prose: registries and audit labels stay backstage.
- Depth budget before drafting: define expected depth, rough length band, unit-level expansion plan, and what would count as too short.
- Staged execution: plan, collect, analyze, draft, review, revise, then continue.
- Optional lenses only: framing/category analysis and horizontal-vertical analysis are tools, not default structure.
- Review closes the loop: every audit finding becomes a revision action, downgraded claim, or explicit limitation.
- Reader review comes last: improve readability after factual, coverage, structure, and depth checks are stable.

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

## 05 Research Brief Gate

Before collecting sources, decide whether the request contains enough decision-critical information. If not, ask one compact batch of questions before starting. The batch should usually contain 3-7 questions and must include expected length or depth when it is missing.

Ask only for missing critical information:

- research object and scope boundaries
- target reader and decision context
- output format, language, and publishing context
- expected depth, rough length band, or depth level
- must-cover units, exclusions, and priority areas
- required sources or materials, source exclusions, and evidence standard
- time period, geography, deadline, and whether charts/tables are expected

If the user has already supplied enough context, proceed and record assumptions in `task_spec.md`. Do not keep asking non-blocking questions.

## 06 Operating Loop

1. Run the research brief gate, then plan the scope, inputs, output, and done criteria.
2. Collect or process only the sources needed for that stage.
3. Convert sources into claims, uncertainty, and analysis notes.
4. Draft a bounded section or unit.
5. Review the section for evidence, coverage, structure, skepticism, and prose.
6. Revise the section and registries.
7. Update progress and define the next stage.

If one cycle adds no new evidence, case, counterexample, framework, or judgment, increment `stale_count`. If `stale_count >= 2`, pivot the structural angle rather than searching harder inside the same frame.

For longform deliverables, source counts, claim counts, link counts, and file size are backend health signals only. They cannot substitute for a depth review. Before final assembly, compare the draft against the depth budget and expand thin units before reader review.

## 07 Analysis Lens Scheduling

Choose the lens that fits the research question:

- framing/category analysis
- horizontal-vertical analysis
- adoption analysis
- capital analysis
- organization/talent analysis
- policy/legitimacy analysis
- counter-case analysis

Pick one primary lens and at most two secondary lenses unless the user explicitly requests a multi-method report.

## 08 Subagent And Review Scheduling

Use subagents for bounded work only:

- requirement mapping
- source discovery
- evidence-chain verification
- coverage audit
- skeptical review
- structure review
- reader-quality review

Subagents should not rewrite the whole report or own the thesis.

## 09 Engineering Constraints

- Every important hard claim needs a confidence boundary.
- Every 20 important facts, figures, or judgments should update source and claim registries.
- Official materials show stated position; they do not prove adoption.
- Media materials show public framing; they need corroboration for hard facts.
- User/community evidence shows reception; it is not automatically representative.
- Reader review may improve flow and clarity, but must not invent facts.

## 10 Validation And Limits

Before declaring completion:

- The research brief gate was completed or assumptions were recorded.
- Required coverage is complete or limitations are explicit.
- Major claims trace back to sources or uncertainty records.
- Facts, source claims, interpretations, and author judgments remain distinct.
- Counter-evidence has been addressed.
- The draft meets the depth budget or explains why the original expected depth is no longer appropriate.
- Reader review has been run after factual, coverage, structure, and depth review.
- Final prose reads like an author's report, not an agent process report.

Limits:

- The framework reduces citation and evidence errors; it does not eliminate them.
- Subagent review is a check, not external truth.
- Optional lenses can overfit the report if used mechanically.
- State files only work if updated during the task, not reconstructed after the fact.

## 11 Full SKILL.md

The authoritative instruction file is [`SKILL.md`](./SKILL.md). The framework page includes the full skill text in a copyable block.

## Repository Structure

```text
industry-research-framework/
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
git clone https://github.com/rrrrrredy/industry-research-framework.git \
  ./agent-skills/industry-research-framework
```

For systems without a formal skill loader, use `SKILL.md` as the main instruction file and load files under `references/` only when the task requires them.

---

# 中文说明：产业研究框架

这是一个面向 AI agent 的长篇产业研究与写作框架，用于处理资料量大、周期长、需要形成可发布文章或研究报告的任务。

它不是抓取工具、数据源或固定报告模板。它提供的是一套可复用的研究执行框架：帮助 agent 在开工前澄清关键任务信息，保存任务状态，区分来源与判断，分阶段推进写作，完成审阅与读者视角修订，并把复杂的后台研究整理成干净的成稿。

框架页面是给读者看的结构化导览，`SKILL.md` 是 agent 实际使用的权威指令文件，`references/` 下的文件是按需加载的扩展模块。只有任务需要某个方法、审阅循环或写作规则时，才读取对应 reference。

## 01 动机：五类常见失败

长篇研究任务中，agent 很容易出现五类问题：

1. **方法过拟合**：从一个具体项目中提炼出的经验，被误当成所有研究任务的默认框架。
2. **过程泄漏**：终稿不像作者写的研究文章，而像“我读取了什么材料、做了什么处理”的工作日志。
3. **证据漂移**：事实、来源说法、媒体解释、不确定性和作者判断混在一起，最后很难追溯。
4. **过早完成**：只完成一个局部阶段，就把它当成整体任务完成。
5. **深度塌缩**：来源数量、覆盖清单和审阅记录看似合格，但成稿过短、过于压缩，没有达到任务应有的研究深度。

这个框架里的状态文件、来源台账、判断台账、阶段审阅和读者修订，都是为了解决这些问题。

## 02 核心原则

- **交付物优先**：如果用户要的是文章或报告，不要偏移成系统设计、prompt 设计或流程说明。
- **先过研究简报门槛**：如果缺少影响方向、范围、交付物或深度判断的关键信息，先集中提问；其中必须确认预期篇幅或研究深度。
- **先建状态，再扩资料**：长任务必须把目标、范围、进度、发现、待核项写入文件，而不是只依赖聊天上下文。
- **证据不是正文**：来源台账、审阅记录、访问失败、内部来源编号留在后台，不能直接污染终稿。
- **先定深度，再写终稿**：在写作前明确预期篇幅、章节展开计划、重点单元的深度要求，以及什么情况属于“太短”。
- **分阶段推进**：规划、收集、分析、写作、审阅、修订、更新状态，按阶段循环。
- **方法按需选择**：框架与类别分析、横纵分析、资本分析、采用分析都是可选镜头，不是默认结构。
- **审阅必须闭环**：每个审阅问题都要变成具体修改动作、降级后的判断，或明确的不确定性说明。
- **读者视角最后介入**：先完成事实、覆盖、结构和深度检查，再做可读性、节奏和理解负担优化。

## 03 研究简报门槛

在开始收集资料前，agent 必须判断用户请求是否已经足够明确。若缺少关键信息，应先集中提出一组简短问题，通常 3-7 个；如果缺少篇幅或深度要求，必须询问。

优先确认：

- 研究对象和范围边界
- 目标读者与使用场景
- 输出格式、语言和发布场景
- 预期篇幅、粗略字数区间或研究深度等级
- 必须覆盖的对象、排除项和优先级
- 必须使用或排除的来源、证据标准
- 时间范围、地域范围、截止时间，以及是否需要图表

如果用户已经提供足够上下文，不要为了流程感反复追问；应直接进入任务，并把默认假设写入 `task_spec.md`。

## 04 研究后台与成稿

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

面向读者的成稿包括：

- 核心判断
- 研究范围
- 分析章节
- 跨案例综合
- 反证与边界
- 结论
- 读者可读的参考资料

后台保证可追溯，成稿保证可阅读。两者必须分开。

## 05 适用场景

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

## 06 与框架页面的关系

完整框架页面在这里：

[Industry Research Framework](https://rrrrrredy.github.io/industry-research-framework/framework.html#fullmd)

仓库源码在这里：

[rrrrrredy/industry-research-framework](https://github.com/rrrrrredy/industry-research-framework)


