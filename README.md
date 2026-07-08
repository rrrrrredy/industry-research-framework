# Industry Research Framework

A framework for longform, source-backed industry research and publishable writing by AI agents.

It ships no scraper, data source, or fixed report template. Instead, it prescribes conventions for how an agent persists state, separates evidence from prose, avoids topic drift, schedules review, and turns a large research backend into a clean reader-facing article or report.

Scope Contract Research Brief Task State Recovery Guardrails Source Registry Claim Discipline Staged Drafting Review Loop Reader Revision

[Open framework page](https://rrrrrredy.github.io/industry-research-framework/framework.html#fullmd)

The framework page is the structured reading guide. `SKILL.md` is the authoritative agent instruction file. Files under `references/` are optional modules loaded only when the task needs that method, review loop, or writing guidance.

## 30-Second Quickstart

1. Start with `SKILL.md`.
2. Ask the agent to run the research scope calibration and confirm output, reader, depth, evidence standard, and coverage.
3. For substantial work, create `state/`, `logs/`, and `data/` before collecting many sources.
4. Load reference files only when needed: workflow for setup or recovery, analysis lenses for method choice, subagent guidance before delegation, gotchas for drift diagnosis, writing style before drafting, and quality gates before completion.
5. Draft section by section, keep evidence backstage, obey hard stops, and run reader review only after coverage and evidence checks are stable.

## Use With Your Agent

This repository is designed to stay lightweight. You do not need a hosted app, crawler, database, or CLI to use it. The default path is: give this repository URL to your agent, ask it to read `SKILL.md`, and let it load files under `references/` only when the task needs them.

```text
Use https://github.com/rrrrrredy/industry-research-framework as your research protocol.
Read SKILL.md first. Before collecting sources, run the research brief gate.
For a substantial task, create state/, logs/, and data/ in the project folder.
Keep sources, claims, uncertainty, and review notes backstage.
Draft section by section and run quality gates before final delivery.
```

Recommended installation modes:

- **Codex / local coding agents**: clone this repository into the agent's skill or instructions directory, then mention `$industry-research-framework` or point the agent at `SKILL.md`.
- **Claude / Gemini CLI / Cursor**: paste the repository URL into the session and ask the agent to read `SKILL.md` as the controlling instruction. Load `references/` files only on demand.
- **ChatGPT or any general agent**: attach or paste `SKILL.md`, then give the task brief. If file access is available, provide the whole repository.
- **OpenClaw**: install as a skill directory containing `SKILL.md`, for example `<workspace>/skills/industry-research-framework` or `~/.openclaw/skills/industry-research-framework`. If skill allowlists are enabled, allow the frontmatter name `industry-research-framework`. No env or API key config is required for this framework.
- **Hermes Agent**: install as a skill under `~/.hermes/skills/industry-research-framework`, then use `/skills` to confirm it is visible and invoke it by name. If migrating from OpenClaw, use Hermes' official migration flow and verify that `SKILL.md` plus `references/` were imported.

Agent-specific notes live in [`agents/`](./agents/):

- [`agents/codex.md`](./agents/codex.md)
- [`agents/claude.md`](./agents/claude.md)
- [`agents/gemini-cli.md`](./agents/gemini-cli.md)
- [`agents/cursor.md`](./agents/cursor.md)
- [`agents/chatgpt.md`](./agents/chatgpt.md)
- [`agents/openclaw.md`](./agents/openclaw.md)
- [`agents/hermes.md`](./agents/hermes.md)

## Example Tasks

Use these as realistic smoke tests for the framework:

1. **Industry report**: "Research the 2026 AI agent market for strategy readers. Cover platform players, workflow products, protocol/ecosystem moves, commercialization, adoption barriers, and failure modes. Deliver a 6,000-10,000 word Chinese report."
2. **Competitive analysis**: "Compare OpenAI, Anthropic, Google, ByteDance, Alibaba, and Tencent in AI agent and coding-agent strategy. Separate product surface, developer ecosystem, model capability, distribution, and monetization."
3. **Investment memo**: "Write an investment memo on the AI video generation market. Focus on category timing, key companies, technical moat, pricing pressure, GTM, adoption risk, and counter-evidence."
4. **Monthly observation**: "Produce an AI industry monthly observation for an executive reader. Synthesize model releases, agent infrastructure, product competition, open-source dynamics, China/US differences, and implications."
5. **Technical route research**: "Research reasoning model competition from DeepSeek R1 to Claude Sonnet-style hybrid reasoning. Explain technical paths, product consequences, and what remains uncertain."

## Good vs Bad Output

Good output:

- Opens with a thesis or executive judgment, not a work log.
- Defines scope, reader, evidence standard, and depth before large-scale collection.
- Separates verified facts, source claims, interpretation, author judgment, and speculation.
- Uses sources to support claims and states what each source can and cannot prove.
- Handles counter-evidence, uncertainty, adoption friction, and alternative explanations.
- Writes section by section and removes internal source IDs, audit labels, and process language before final delivery.
- Stops and repairs state when evidence, claims, depth, or completion signals fail a hard stop.

Bad output:

- Starts writing immediately without confirming scope, audience, depth, or evidence standard.
- Treats company PR, media summaries, and community comments as equal evidence.
- Lists sources or companies without explaining mechanisms, causality, or implications.
- Leaves phrases such as "the user provided", "the material shows", or "this source supplements" in the final article.
- Declares completion after collecting many links or drafting one section.
- Produces a short, compressed report while claiming the source registry proves depth.
- Marks progress as complete while review findings, coverage gaps, or depth problems remain open.

## Conformance Checklist

Use this lightweight checklist to see whether an agent followed the protocol:

- [ ] **Brief gate**: the agent confirmed or recorded objective, reader, output format, scope, evidence standard, and expected depth.
- [ ] **State files**: substantial work created or updated `state/task_spec.md`, `state/progress.json`, and recovery notes.
- [ ] **Claim registry**: important facts, claims, judgments, and uncertainties were tracked separately from source notes.
- [ ] **Quality gate**: evidence, coverage, structure, counter-evidence, and depth were reviewed before final assembly.
- [ ] **Hard stops**: evidence dead ends, empty claim registries, process leakage, thin drafts, and false completion signals were stopped and repaired.
- [ ] **Reader cleanup**: the final prose removed process language, internal IDs, audit labels, and unsupported claims.

## Evaluation Suite

This repository includes a lightweight evaluation loop under [`evals/`](./evals/). It is intentionally simple: cases, sanitized source packs, rubrics, and an offline runner that checks required artifacts and report quality signals.

```bash
python scripts/run_evals.py --runs-dir evals/runs --report evals/runs/report.md
python scripts/check_regression_fixtures.py
```

To rebuild the sanitized AI knowledge source pack from local knowledge repositories:

```bash
python scripts/build_sanitized_eval_set.py ^
  --aiknowledge-cli D:\path\to\aiknowledge-cli ^
  --knowledge-graph D:\path\to\ai-knowledge-graph
```

See [`evals/README.md`](./evals/README.md) for the full loop.

## 01 Motivation: Five Failure Modes

Longform research agents tend to fail in five recurring ways:

1. **Topic overfitting**: a method distilled from one project becomes falsely treated as the universal frame.
2. **Process leakage**: the final article reads like a work log.
3. **Evidence drift**: sources, claims, uncertainty, and author judgment collapse into one argument.
4. **False completion**: a partial milestone is reported as final completion before coverage, review, and reader-quality revision are done.
5. **Depth collapse**: source counts and coverage checklists pass, but the finished report is too short or compressed for the expected research depth.

Every mechanism in this framework targets one of those failures.

## 02 Scope Contract

This repository is scoped as an execution framework for producing substantial research deliverables. It is not a theory system, product architecture, or universal modeling language.

Keep inside this repository:

- **Process**: research scope calibration, staged execution, source processing, drafting, review, revision, and final cleanup.
- **State**: task state, progress, findings, assumptions, decisions, and direction tracking.
- **Audit**: source, claim, uncertainty, coverage, depth, and reader-quality checks.

Keep outside this repository unless it is explicitly spun out as a separate project:

- domain ontologies, universal taxonomies, or generalized modeling languages
- intermediate representations, scoring systems, embeddings, knowledge graphs, or ranking engines
- dashboards, CLIs, databases, automation pipelines, or product architecture
- methodology manifestos that do not directly improve the current research deliverable

If a task starts drifting into those layers, keep the research deliverable moving and record the idea as a future extension.

## 03 Behavioral Constraints

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

## 04 Architecture

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

## 05 State File System

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

Recovery protocol:

1. Read `state/task_spec.md` for objective, scope, reader, output, depth, evidence standard, and assumptions.
2. Read `state/progress.json` for current stage, completed units, open issues, stale_count, and next action.
3. Read the latest entries in `state/findings.jsonl` and `state/iteration_log.jsonl` for recent direction.
4. Read `state/directions_tried.json` to avoid repeated paths.
5. Resume from the matching step in the operating loop. Do not re-run completed stages or re-ask an answered research brief.

## 06 Research Brief Gate

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

## 07 Operating Loop

1. Run the research brief gate, then plan the scope, inputs, output, and done criteria.
2. Collect or process only the sources needed for that stage.
3. Convert sources into claims, uncertainty, and analysis notes.
4. Draft a bounded section or unit.
5. Review the section for evidence, coverage, structure, skepticism, and prose.
6. Revise the section and registries.
7. Update progress and define the next stage.

If one cycle adds no new evidence, case, counterexample, framework, or judgment, increment `stale_count`. If `stale_count >= 2`, pivot the structural angle rather than searching harder inside the same frame.

For longform deliverables, source counts, claim counts, link counts, and file size are backend health signals only. They cannot substitute for a depth review. Before final assembly, compare the draft against the depth budget and expand thin units before reader review.

## 08 Analysis Lens Scheduling

Choose the lens that fits the research question:

- framing/category analysis
- horizontal-vertical analysis
- adoption analysis
- capital analysis
- organization/talent analysis
- policy/legitimacy analysis
- counter-case analysis

Pick one primary lens and at most two secondary lenses unless the user explicitly requests a multi-method report.

## 09 Subagent And Review Scheduling

Use subagents for bounded work only:

- requirement mapping
- source discovery
- evidence-chain verification
- coverage audit
- skeptical review
- structure review
- reader-quality review

Subagents should not rewrite the whole report or own the thesis.

## 10 Engineering Constraints

- Every important hard claim needs a confidence boundary.
- Every 20 important facts, figures, or judgments should update source and claim registries.
- Official materials show stated position; they do not prove adoption.
- Media materials show public framing; they need corroboration for hard facts.
- User/community evidence shows reception; it is not automatically representative.
- Reader review may improve flow and clarity, but must not invent facts.

## 11 Validation And Limits

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

## 12 Execution Guardrails

- If three consecutive searches or source passes add no relevant evidence, stop that direction and draft or pivot.
- If `source_registry.csv` grows while `claims_registry.csv` stays thin, pause collection and extract claims.
- Cap full review-revise cycles at two per section unless the user asks for more.
- Before reader review, compare the draft against the depth budget and expand thin units.
- If new work falls outside `task_spec.md`, record it as a proposed extension and ask before expanding.
- Subagent prompts must ask reviewers to actively look for issues; if no issue is found, they must explain the basis for PASS.

## 13 Full SKILL.md

The authoritative instruction file is [`SKILL.md`](./SKILL.md). The framework page includes the full skill text in a copyable block.

## Repository Structure

```text
industry-research-framework/
├── LICENSE
├── SKILL.md
├── agents/
│   ├── README.md
│   ├── openai.yaml
│   ├── codex.md
│   ├── claude.md
│   ├── gemini-cli.md
│   ├── cursor.md
│   ├── chatgpt.md
│   ├── openclaw.md
│   └── hermes.md
├── docs/
│   ├── index.html
│   └── framework.html
├── evals/
│   ├── README.md
│   ├── cases/
│   ├── regression_fixtures/
│   ├── rubrics/
│   ├── source_packs/
│   └── taste_anchors/
├── scripts/
│   ├── build_sanitized_eval_set.py
│   ├── check_regression_fixtures.py
│   └── run_evals.py
└── references/
    ├── research-workflow.md
    ├── optional-analysis-lenses.md
    ├── horizontal-vertical-analysis.md
    ├── subagents-and-review-loop.md
    ├── writing-style.md
    ├── quality-gates.md
    ├── gotchas.md
    └── postmortem-lessons.md
```

## Reuse

Clone or copy this repository into the directory where your agent system loads reusable skills or instruction bundles:

```bash
git clone https://github.com/rrrrrredy/industry-research-framework.git \
  ./agent-skills/industry-research-framework
```

For systems without a formal skill loader, use `SKILL.md` as the main instruction file and load files under `references/` only when the task requires them.

## License

This project is open source under the [MIT License](./LICENSE).

---

# 中文说明：产业研究框架

这是一个面向 AI agent 的长篇产业研究与写作框架，用于处理资料量大、周期长、需要形成可发布文章或研究报告的任务。

它不是抓取工具、数据源或固定报告模板。它提供的是一套可复用的研究执行框架：帮助 agent 在开工前澄清关键任务信息，保存任务状态，区分来源与判断，分阶段推进写作，完成审阅与读者视角修订，并把复杂的后台研究整理成干净的成稿。

框架页面是给读者看的结构化导览，`SKILL.md` 是 agent 实际使用的权威指令文件，`references/` 下的文件是按需加载的扩展模块。只有任务需要某个方法、审阅循环或写作规则时，才读取对应 reference。

## 30 秒快速开始

1. 先使用 `SKILL.md`。
2. 让 agent 先做研究范围校准，确认交付物、读者、深度、证据标准和覆盖范围。
3. 对资料量大的任务，先创建 `state/`、`logs/` 和 `data/`，再大规模收集资料。
4. reference 文件只在需要时读取：启动或恢复任务读 workflow，选择分析方法读 analysis lenses，派发子 agent 前读 subagent guidance，诊断漂移读 gotchas，进入写作前读 writing style，阶段验收前读 quality gates。
5. 一段一段写，证据留在后台，遵守 hard stops，覆盖和证据检查稳定后再做读者审阅。

## 给 Agent 使用

这个仓库刻意保持轻量。默认用法不是安装一个新产品，也不是启动爬虫或数据库，而是：把仓库链接交给你正在使用的 agent，让它先读 `SKILL.md`，只在任务需要时再读取 `references/` 下的扩展文件。

```text
请使用 https://github.com/rrrrrredy/industry-research-framework 作为本次研究协议。
先读取 SKILL.md。收集资料前，先完成研究范围校准。
如果任务较大，在项目目录里创建 state/、logs/、data/。
来源、判断、不确定性和审阅记录留在后台。
按章节推进写作，并在最终交付前运行质量门禁。
```

推荐使用方式：

- **Codex / 本地 coding agent**：把本仓库克隆到 agent 的 skill 或 instruction 目录，再在任务中提到 `$industry-research-framework` 或直接指向 `SKILL.md`。
- **Claude / Gemini CLI / Cursor**：把仓库链接发给 agent，让它把 `SKILL.md` 当作控制指令；`references/` 文件只在需要对应方法时读取。
- **ChatGPT 或通用 agent**：上传或粘贴 `SKILL.md`，再给研究任务；如果支持文件访问，直接提供整个仓库。
- **OpenClaw**：按官方 skill 机制安装为包含 `SKILL.md` 的目录，例如 `<workspace>/skills/industry-research-framework` 或 `~/.openclaw/skills/industry-research-framework`。如果启用了 skill allowlist，请允许 frontmatter 名称 `industry-research-framework`。本框架不需要 env 或 API key 配置。
- **Hermes Agent**：按官方 skill 机制放到 `~/.hermes/skills/industry-research-framework`，启动后用 `/skills` 确认可见，再通过技能名调用。如果从 OpenClaw 迁移到 Hermes，使用 Hermes 官方迁移流程，并确认 `SKILL.md` 和 `references/` 已导入。

不同 agent 的适配说明见 [`agents/`](./agents/)：

- [`agents/codex.md`](./agents/codex.md)
- [`agents/claude.md`](./agents/claude.md)
- [`agents/gemini-cli.md`](./agents/gemini-cli.md)
- [`agents/cursor.md`](./agents/cursor.md)
- [`agents/chatgpt.md`](./agents/chatgpt.md)
- [`agents/openclaw.md`](./agents/openclaw.md)
- [`agents/hermes.md`](./agents/hermes.md)

## 真实任务示例

这些任务可以作为框架的 smoke test：

1. **行业报告**：研究 2026 年 AI Agent 市场，面向战略读者，覆盖平台型玩家、工作流产品、协议与生态、商业化、采用阻力和失败模式，输出 6000-10000 字中文报告。
2. **竞品分析**：比较 OpenAI、Anthropic、Google、字节、阿里、腾讯的 AI Agent 与 coding agent 策略，区分产品形态、开发者生态、模型能力、分发和商业化。
3. **投资 memo**：写一份 AI 视频生成市场投资 memo，重点分析品类时机、关键公司、技术壁垒、价格压力、GTM、采用风险和反证。
4. **月度观察**：为管理层写 AI 行业月度观察，综合模型发布、Agent 基础设施、产品竞争、开源动态、中美差异和影响判断。
5. **技术路线研究**：研究从 DeepSeek R1 到 Claude Sonnet 风格混合推理的 reasoning model 竞争，解释技术路径、产品后果和仍不确定的问题。

## 好输出 / 坏输出

好的输出：

- 先给核心判断或执行摘要，而不是工作日志。
- 大规模收集资料前，明确范围、读者、证据标准和深度。
- 区分已验证事实、来源说法、解释、作者判断和猜测。
- 用来源支撑判断，并说明每类来源能证明什么、不能证明什么。
- 处理反证、不确定性、采用阻力和替代解释。
- 分章节推进，最终交付前删除内部来源编号、审阅标签和过程语言。
- 在证据、判断、深度或完成状态触发 hard stop 时，先停下修复状态和稿件。

坏的输出：

- 不确认范围、读者、深度和证据标准就直接开写。
- 把公司 PR、媒体摘要和社区反馈当成同等级证据。
- 罗列来源或公司，却不解释机制、因果和影响。
- 终稿里保留“用户提供的资料”“材料显示”“该来源补充了”等过程话术。
- 收集了很多链接或写完一个章节后就宣布完成。
- 报告很短、很压缩，却用来源台账完整来替代深度。
- `progress.json` 标记完成，但审阅问题、覆盖缺口或深度问题仍未关闭。

## 符合性清单

用这个极轻 checklist 判断 agent 是否真的遵守了框架：

- [ ] **研究范围校准**：agent 已确认或记录目标、读者、输出格式、范围、证据标准和预期深度。
- [ ] **状态文件**：较大任务已创建或更新 `state/task_spec.md`、`state/progress.json` 和恢复记录。
- [ ] **判断台账**：重要事实、来源说法、作者判断和不确定性没有混在普通笔记里。
- [ ] **质量门禁**：最终组装前检查了证据、覆盖、结构、反证和深度。
- [ ] **Hard stops**：证据枯竭、判断台账为空、过程泄漏、稿件过薄和虚假完成信号已经被停止并修复。
- [ ] **读者清理**：终稿删除了过程语言、内部编号、审阅标签和无法支撑的判断。

## 评测集

仓库内置一个轻量评测闭环，见 [`evals/`](./evals/)：包含 cases、脱敏 source pack、rubric 和离线 runner，用于检查 agent 是否真的遵守框架。

```bash
python scripts/run_evals.py --runs-dir evals/runs --report evals/runs/report.md
python scripts/check_regression_fixtures.py
```

如果本地有 AI 知识库仓库，可以重新生成脱敏评测数据：

```bash
python scripts/build_sanitized_eval_set.py ^
  --aiknowledge-cli D:\path\to\aiknowledge-cli ^
  --knowledge-graph D:\path\to\ai-knowledge-graph
```

完整使用方法见 [`evals/README.md`](./evals/README.md)。

## 01 动机：五类常见失败

长篇研究任务中，agent 很容易出现五类问题：

1. **方法过拟合**：从一个具体项目中提炼出的经验，被误当成所有研究任务的默认框架。
2. **过程泄漏**：终稿不像作者写的研究文章，而像“我读取了什么材料、做了什么处理”的工作日志。
3. **证据漂移**：事实、来源说法、媒体解释、不确定性和作者判断混在一起，最后很难追溯。
4. **过早完成**：只完成一个局部阶段，就把它当成整体任务完成。
5. **深度塌缩**：来源数量、覆盖清单和审阅记录看似合格，但成稿过短、过于压缩，没有达到任务应有的研究深度。

这个框架里的状态文件、来源台账、判断台账、阶段审阅和读者修订，都是为了解决这些问题。

## 02 范围契约

这个仓库只承载“产业研究执行框架”，不承载理论系统、产品架构或通用建模语言。

允许放进这个仓库的内容：

- **process**：研究范围校准、分阶段执行、资料处理、写作、审阅、修订和终稿清理。
- **state**：任务状态、进度、发现、假设、决策和方向记录。
- **audit**：来源、判断、不确定性、覆盖度、深度和读者体验检查。

不应放进这个仓库的内容，除非明确拆成独立项目：

- 领域本体、通用分类体系或通用建模语言
- 中间表示、评分系统、embedding、知识图谱或排序引擎
- 仪表盘、CLI、数据库、自动化流水线或产品架构
- 不能直接改善当前研究交付物的方法论宣言

如果任务开始滑向这些方向，应保持当前研究交付物继续推进，把相关想法记录为未来扩展，而不是扩展当前框架。

## 03 核心原则

- **交付物优先**：如果用户要的是文章或报告，不要偏移成系统设计、prompt 设计或流程说明。
- **先做研究范围校准**：如果缺少影响方向、范围、交付物或深度判断的关键信息，先集中提问；其中必须确认预期篇幅或研究深度。
- **先建状态，再扩资料**：长任务必须把目标、范围、进度、发现、待核项写入文件，而不是只依赖聊天上下文。
- **证据不是正文**：来源台账、审阅记录、访问失败、内部来源编号留在后台，不能直接污染终稿。
- **先定深度，再写终稿**：在写作前明确预期篇幅、章节展开计划、重点单元的深度要求，以及什么情况属于“太短”。
- **分阶段推进**：规划、收集、分析、写作、审阅、修订、更新状态，按阶段循环。
- **方法按需选择**：框架与类别分析、横纵分析、资本分析、采用分析都是可选镜头，不是默认结构。
- **审阅必须闭环**：每个审阅问题都要变成具体修改动作、降级后的判断，或明确的不确定性说明。
- **读者视角最后介入**：先完成事实、覆盖、结构和深度检查，再做可读性、节奏和理解负担优化。

## 04 研究范围校准

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

## 05 研究后台与成稿

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

## 06 断点恢复与执行护栏

断点恢复时，先读 `state/task_spec.md`，再读 `state/progress.json`，再读 `state/findings.jsonl` 和 `state/iteration_log.jsonl` 的最新记录，最后读 `state/directions_tried.json`。不要重复已完成阶段；如果 `task_spec.md` 已经记录研究范围，不要重新做研究范围校准。

执行中遵守这些护栏：

- 连续三次搜索或资料处理没有新增有效证据时，停止当前方向，记录后转向或进入写作。
- 来源台账持续增长但判断台账很薄时，暂停收集，先做判断提取。
- 每个章节的完整审阅-修订循环默认最多两轮，剩余问题写成限制或后续任务。
- 读者审阅前必须对照深度预算，先补薄弱单元，再优化表达。
- 新工作超出 `task_spec.md` 时，先记录为扩展建议，不直接扩大任务。
- 子 agent 必须主动寻找问题；若判定 PASS，必须说明依据。

## 07 适用场景

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

## 08 与框架页面的关系

完整框架页面在这里：

[Industry Research Framework](https://rrrrrredy.github.io/industry-research-framework/framework.html#fullmd)

仓库源码在这里：

[rrrrrredy/industry-research-framework](https://github.com/rrrrrredy/industry-research-framework)

## 09 许可协议

本项目采用 [MIT License](./LICENSE) 开源。


