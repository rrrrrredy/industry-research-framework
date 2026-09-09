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

在 Claude 中，建议把 `SKILL.md` 放进项目指令或作为附件。不要让 Claude 一上来直接写全文；先校准范围、读者、深度和证据标准，再分阶段推进。

如果当前环境只能在对话中保存状态，不能据此确认文件持久化恢复或绑定实际产物的交付校验已经通过；长任务先核对[接入说明中的能力限制](./README.md#中文说明)。
