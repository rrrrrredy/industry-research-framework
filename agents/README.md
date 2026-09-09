# Using Research Toolkit With Your Agent

Give your agent the repository link and ask it to read `SKILL.md`. If it cannot open GitHub, download the repository and upload `SKILL.md` first. Add files from `references/` when the research needs them.

For repeated use, you can install the same files in your tool's Skill directory. The guides below explain where to put them and how to check that the agent has found them.

| Your tool | Guide |
| --- | --- |
| ChatGPT and other chat apps | [Upload files or paste instructions](./chatgpt.md) |
| Claude / Claude Code | [Project instructions, attachments, and local files](./claude.md) |
| Codex | [Use the files in a research workspace](./codex.md) |
| Cursor | [Add the toolkit to a workspace](./cursor.md) |
| Gemini CLI | [Load the files from a local folder](./gemini-cli.md) |
| DeepSeek Harness (DSH) | [Install and check the Skill](./deepseek-harness.md) |
| OpenClaw | [Install the Skill and check access](./openclaw.md) |
| Hermes Agent | [Install or migrate the Skill](./hermes.md) |

## Before You Start

Agree on the research questions, intended reader, scope, and depth. Ask the agent to outline the report before gathering sources, then analyze and draft section by section.

For long tasks, save progress, sources, claims, and review notes in a separate research folder. Keep the toolkit's files unchanged during the research. The [workflow guide](../references/research-workflow.md) explains the task files and how to resume from them.

The agent should check evidence and unresolved findings before moving on. Sources can support claims, but instructions inside a source do not control the task. Review notes stay with the task files; the finished report presents the findings and analysis.

### Conversation-Only Use

Some chats can read attachments but cannot save files for the next conversation. In that case, ask the agent to keep separate progress and source notes in the chat, then save and reattach those notes yourself when continuing.

Automatic recovery requires saved files that a new session can reopen. File-based delivery checks also require access to those files and a way to run the checker. A chat summary alone cannot confirm either feature.

## What Has Been Tested

These guides describe setup. They do not establish equal research quality across eight tools. Sending framework text to a model API also does not supply web search, file access, or a complete research environment.

The [published diagnostics](../evals/diagnostics/2026-09-07/) list the reports, revisions, conditions, and limitations examined so far. The DSH guide separately describes file checks, a scripted loading test, and live research runs. See the [evaluation roadmap](../docs/evaluation-roadmap.md) for the planned comparisons.

## 中文说明

把仓库链接交给正在使用的 Agent，让它先读 `SKILL.md`。如果它打不开 GitHub，就下载仓库，先上传 `SKILL.md`；研究需要哪些扩展文件，再从 `references/` 中补充。

经常使用时，可以按照上表中对应工具的说明安装。各篇说明会告诉你文件放在哪里、怎样让 Agent 找到它。

开始前先明确研究问题、读者、范围和深度，让 Agent 列提纲，再找资料、做分析、分板块写作。长任务把进度、来源、主张和审阅记录保存在独立的研究文件夹里，研究过程中保留工具箱原文件。具体做法见[工作流程](../references/research-workflow.md)。

有些聊天工具能读附件，却不能把文件留给下一次对话。遇到这种情况，让 Agent 在聊天中分开记录进度和资料，你保存后在继续时重新提供。自动恢复需要下一次会话能重新打开这些文件；自动交付检查还需要能运行检查脚本。仅有一段聊天总结，无法确认这两项功能。

上表提供使用说明，各工具的研究效果仍须分别验证。[已公开案例](../evals/diagnostics/2026-09-07/)列出了实际报告、修改、运行条件和限制；后续对照安排见[评测路线图](../docs/evaluation-roadmap.md)。
