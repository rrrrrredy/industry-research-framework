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
- Before final delivery, ask it to check the report against the delivery requirements and remove execution notes from the prose.
- Conversation-only state is a reduced-capability fallback, not proof of durable file recovery or artifact-bound delivery checks. Use the [integration guide](./README.md#conversation-only-use) to assess this boundary before starting a long task.

## 中文提示

给 ChatGPT 或其他聊天工具提供 `SKILL.md`，需要时再补充扩展文件。如果它不能保存文件，让它在聊天中分别记录研究目标、进度、来源、判断、未解决问题和审阅意见。

长任务请自行保存这些记录，在继续时重新提供。自动恢复和交付检查需要工具能保存、重新打开文件并运行检查脚本，详见[使用说明](./README.md#中文说明)。
