# Claude Adapter

Use this when working with Claude, Claude Code, or a Claude project.

## Setup

Attach this repository, paste the repository URL, or add `SKILL.md` to Claude's project instructions. Start with:

```text
Use https://github.com/rrrrrredy/research-toolkit as the research protocol.
Read SKILL.md as the controlling instruction.
Ask the research brief gate before collecting sources if critical information is missing.
Create and maintain state/, logs/, and data/ for substantial work.
```

## Operating Notes

- Use Claude projects or file attachments to keep `SKILL.md` available across turns.
- Ask Claude to write state files explicitly when the task is long.
- If Claude cannot write files, ask it to maintain the same state sections in the conversation and export them when possible.
- That conversation-only fallback does not establish durable file recovery or artifact-bound delivery verification; check the [integration guide](./README.md#conversation-only-use) before relying on it for a long task.
- Load `references/writing-style.md` only when entering drafting or reader cleanup.
- Load `references/quality-gates.md` before declaring completion.

## 中文提示

把 `SKILL.md` 放进 Claude 的项目指令或作为附件。先明确范围、读者、深度和证据标准，列提纲，再搜集资料、分析并分节写作。

只能在聊天中记录进度时，请保存并在继续任务时重新提供。自动恢复需要重新打开已保存文件；交付检查需要访问实际报告并运行脚本，见[使用说明](./README.md#中文说明)。
