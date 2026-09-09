# OpenClaw Adapter

Use this when OpenClaw can read local skills from a workspace or user skills directory. This adapter follows the official OpenClaw skills docs:

- https://docs.openclaw.ai/tools/skills
- https://docs.openclaw.ai/tools/skills-config

## Setup

OpenClaw skills are directories containing a `SKILL.md` file with YAML frontmatter and a markdown body. OpenClaw discovers skills by scanning skill roots; the skill's visible name comes from the `name` field in `SKILL.md`.

Recommended install paths, in OpenClaw's precedence order:

```text
<workspace>/skills/research-toolkit
<workspace>/.agents/skills/research-toolkit
~/.agents/skills/research-toolkit
~/.openclaw/skills/research-toolkit
```

For a workspace-scoped install:

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git \
  ./skills/research-toolkit
```

For a managed/local install:

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git \
  ~/.openclaw/skills/research-toolkit
```

Then tell OpenClaw:

```text
Use the research-toolkit skill for this research task.
Read SKILL.md first. Load references only when the current stage requires them.
Create state/, logs/, and data/ in the research project folder, not inside the skill folder.
```

## Operating Notes

- Keep this repository read-only during ordinary research runs.
- Use the task workspace for `state/`, `logs/`, `data/`, drafts, and final reports.
- This framework does not require `skills.entries.<key>.env` or `skills.entries.<key>.apiKey`; it is an instruction bundle, not a secret-backed tool.
- If your OpenClaw config uses skill allowlists, allow the skill by its frontmatter name: `research-toolkit`.
- Skill or config changes may require a new session before every agent sees the refreshed skill snapshot.
- If OpenClaw has no skill loader in the current environment, paste or attach `SKILL.md` and load `references/` files manually when needed.
- For long research work, ask OpenClaw to update `state/progress.json` after each stage so the task can recover across sessions.

## 中文提示

OpenClaw 官方 skill 机制要求每个 skill 是一个包含 `SKILL.md` 的目录，`SKILL.md` 里有 YAML frontmatter 和 markdown 正文。推荐把本仓库放到官方支持的 skill root 中，例如 `<workspace>/skills/research-toolkit`、`<workspace>/.agents/skills/research-toolkit`、`~/.agents/skills/research-toolkit` 或 `~/.openclaw/skills/research-toolkit`。

如果你的 OpenClaw 配置启用了 skill allowlist，请允许 frontmatter 里的技能名 `research-toolkit`。本框架不需要 `skills.entries.<key>.env` 或 `skills.entries.<key>.apiKey`，因为它是研究指令包，不是需要密钥的工具。

如果当前 OpenClaw 环境没有自动技能加载器，就把 `SKILL.md` 作为主指令交给 agent，并在需要工作流、质量门禁、写作风格或子 agent 审阅时手动加载 `references/` 下的对应文件。
