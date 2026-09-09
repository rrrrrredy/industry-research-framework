# ChatGPT / General Agent Adapter

Use this when the agent cannot install a skill but can read pasted instructions or attached files.

## Setup

Provide the repository URL or attach `SKILL.md`. If file attachments are limited, provide only `SKILL.md` first and add reference files on demand.

Starter prompt:

```text
Use the attached Research Toolkit SKILL.md as the protocol.
Do not start broad source collection until the research brief gate is complete.
If you cannot write files, maintain task_spec, progress, source registry, claim registry, uncertainty registry, and review log as clearly separated sections.
Do not expose backstage registries in the final report unless I ask for an audit appendix.
```

## Operating Notes

- Ask the agent to restate the scope contract before research starts.
- For long tasks, request section-by-section work instead of one-shot drafting.
- When the context gets long, ask the agent to summarize state in the same field names used by the framework.
- Before final delivery, ask it to use the research completion checklist and remove execution notes from the report.
- Conversation-only state is a reduced-capability fallback, not proof of durable file recovery or artifact-bound delivery checks. Use the [integration guide](./README.md#conversation-only-use) to assess this boundary before starting a long task.

## 中文提示

向 ChatGPT 或其他聊天工具提供 `SKILL.md`，需要时再补充扩展文件。不能保存文件时，让 Agent 在聊天中分别记录任务目标、进度、来源、判断、不确定性和审阅意见。

长任务请保存这些记录，继续时重新提供。自动恢复需要新会话能重新打开文件；交付检查还需要访问实际报告并运行脚本，见[使用说明](./README.md#中文说明)。
