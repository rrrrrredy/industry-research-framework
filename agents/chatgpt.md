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
- Before final delivery, ask it to run the research completion checklist and remove process language.
- Conversation-only state is a reduced-capability fallback, not proof of durable file recovery or artifact-bound delivery checks. Use the [integration guide](./README.md#conversation-only-use) to assess this boundary before starting a long task.

## 中文提示

如果使用 ChatGPT 或其他通用 agent，最少只需要提供 `SKILL.md`。不能写文件时，也要让 agent 用清晰分区维护 task spec、progress、source registry、claim registry、uncertainty 和 review log。

纯对话状态不能证明文件持久化恢复或绑定实际产物的交付校验已通过。长任务开始前，先核对[接入说明中的能力限制](./README.md#中文说明)。
