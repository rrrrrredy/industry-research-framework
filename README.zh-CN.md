# 研究工具箱

[English](./README.md) | [简体中文](./README.zh-CN.md)

研究工具箱（Research Toolkit）提供面向 AI 的研究方法、工作流程与检查工具，用于产业、公司、市场和技术等多来源、长篇研究。

它帮助 Agent 明确研究问题、搜集资料、形成判断、分章节写作，并在交付前检查证据和内容。研究进度与来源记录保存在任务文件中，方便长任务中断后继续。

[查看框架介绍](https://rrrrrredy.github.io/research-toolkit/framework.html) · [查看实际报告与修订案例](./evals/diagnostics/2026-09-07/)

## 给 Agent 使用

把仓库链接交给你正在使用的 Agent，让它先读 [`SKILL.md`](./SKILL.md)，只在任务需要时再读取 `references/` 下的扩展文件。

把下面这段说明和你的研究题目一起发给 Agent：

```text
请使用 https://github.com/rrrrrredy/research-toolkit 中的研究方法完成本次任务。
先读 SKILL.md，再按任务需要读取 references/ 中的文件。
先确认研究目标、范围、读者和预期篇幅；已经明确的信息不用重复询问。
先列提纲，再搜集资料、分析并分章节写作。
区分事实、来源观点和你的判断，处理重要反例与不确定性。
交付前检查证据、问题覆盖、分析深度和可读性，并处理审阅发现的问题。
报告先给主要结论，正文不放执行日志和内部审阅标签。
长任务请保存研究进度、来源和后续修改要求，完成说明应与实际交付一致。
```

### 打不开链接，或想长期使用？

- **Agent 打不开 GitHub**：下载仓库，把 `SKILL.md` 上传给它；需要哪个扩展文件，再从 `references/` 中上传对应文件。
- **希望在常用工具中安装**：查看[各工具的使用说明](./agents/README.md#中文说明)，按其中与你所用工具对应的步骤操作。首次尝试可以先使用上面的链接方式。
- **只能在聊天中使用**：仍可提供这些研究指令。长任务需要自行保存和补充进度；自动恢复、文件检查等功能，需要所用 AI 能实际保存文件和运行相应脚本。

资料检索、网站登录和文件访问由你使用的 AI 工具提供。这个仓库提供研究方法和检查规则。

## 它如何组织研究

1. **明确问题**：确认要回答什么、交给谁看、需要多深，以及哪些内容不在范围内。
2. **列出提纲，定向搜集资料**：按问题寻找来源，记录资料能支持什么判断，以及还缺什么。
3. **分析并分节写作**：解释机制、差异和影响，处理反例，避免只罗列公司或链接。
4. **审阅与修改**：先检查事实、覆盖、结构和深度，再调整表达。每个重要问题都要有处理结果。
5. **核对交付**：检查整篇报告、未解决的问题和交付文件，准确说明完成情况。

较长任务会把目标、进度、来源、判断与审阅记录分别保存。恢复任务时，Agent 据此继续已有工作。

具体执行要求以 [`SKILL.md`](./SKILL.md) 为准。这份 README 提供使用导览。

## 适合什么任务

例如：

- 研究国内办公 Agent 产品，比较具体能力、使用条件、商业化和采用证据。
- 研究某条技术路线的进展、应用与局限。
- 比较多家公司的产品、人才、技术与生态策略。
- 分析行业的付费模式、成本结构与商业变化。
- 把大量资料写成行业观察、专题分析或公司研究报告。

简单问答、单篇摘要、代码开发和创意写作通常无需使用这套完整流程。

## 研究完成前检查

这份清单帮助你检查结果；逐项勾选不能代替阅读报告。

- [ ] 研究范围、读者、篇幅和必须回答的问题已经明确。
- [ ] 主要判断有来源支撑，事实、来源观点与作者分析区分清楚。
- [ ] 重要反例、替代解释和证据不足之处已经处理。
- [ ] 正文解释了机制和影响，达到了约定的分析深度。
- [ ] 审阅发现的问题和后续修改要求都有处理结果。
- [ ] 成稿先给主要判断，没有内部编号、执行日志和审阅标签。
- [ ] 整篇报告与交付说明一致；仍未完成的内容没有被说成已经完成。
- [ ] 长任务的进度和研究记录已经保存，后续能继续使用。

## 案例与评测

[已公开的报告与修订案例](./evals/diagnostics/2026-09-07/)保留了四份原稿、两份修订稿、失败审查和三模型文本诊断，也保留未返回完整结论的记录。可以直接比较改动及其依据。这些案例用于开发和校准，尚不能证明框架在一般任务上的效果。

[`evals/`](./evals/)包含研究题目、资料包、评分规则、正负例和检查脚本。验证分为几个部分：

- **流程和文件检查**：发现状态矛盾、缺失记录、无效交付等可重复检查的问题。
- **报告内容评审**：检查事实、分析、反例和读者能否使用结果；评审意见还需核实。
- **真实任务对照**：在相同条件下比较使用框架与不使用框架的报告。
- **其他工具与外部复现**：检查别人能否在不同工具中重复完成研究。

当前已有[多 Agent 同题对照方案](./evals/cross_agent/)，尚未公开完整的运行时配对结果。具体进展和结论限制见[评测计划](./docs/evaluation-roadmap.md)。

<details>
<summary>检查命令与结果字段</summary>

在仓库目录中运行：

```bash
python scripts/run_evals.py --runs-dir evals/runs --report evals/runs/report.md
python scripts/check_regression_fixtures.py
python scripts/check_conformance_fixtures.py
python scripts/check_docs_sync.py
```

交付检查针对具体研究任务目录：

```bash
python scripts/check_delivery.py <任务目录>
```

`conformance_status` 和 `conformance_score` 记录脚本能检查的结构、可追溯性与失败信号。离线评分中的 `research_quality_status` 保持为 `not_evaluated`；报告内容的评审另行记录。脚本通过不能证明报告质量提高。

[DSH 使用说明](./agents/deepseek-harness.md)区分本地结构检查、原生 Skill 加载测试和调用真实模型的研究测试。测试脚本存在，不代表当前设备已经通过测试。

全部维护检查见 [`CONTRIBUTING.md`](./CONTRIBUTING.md)，评测数据的生成方法见 [`evals/README.md`](./evals/README.md)。

</details>

## 深入使用

| 需要了解什么 | 阅读位置 |
| --- | --- |
| 完整执行要求 | [`SKILL.md`](./SKILL.md) |
| 如何启动、保存进度和恢复任务 | [研究流程](./references/research-workflow.md) |
| 如何选择分析方法 | [可选分析方法](./references/optional-analysis-lenses.md) |
| 如何分工与审阅 | [分工和审阅](./references/subagents-and-review-loop.md) |
| 如何组织正文和修改表达 | [写作说明](./references/writing-style.md) |
| 交付前需要检查什么 | [质量检查](./references/quality-gates.md)、[交付检查说明](./docs/delivery-verification.md) |
| 如何排查重复出现的问题 | [常见问题](./references/gotchas.md) |
| 如何安装、检查版本和更新 | [各工具使用说明](./agents/README.md#中文说明)、[版本管理](./docs/installation-versioning.md) |

## 维护与许可

项目变更见 [`CHANGELOG.md`](./CHANGELOG.md)，贡献要求见 [`CONTRIBUTING.md`](./CONTRIBUTING.md)。

本项目采用 [MIT License](./LICENSE)。
