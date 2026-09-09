# Hermes Agent Adapter

Use this when Hermes Agent is available through the CLI, TUI, desktop app, or messaging gateway. This adapter follows the official Hermes skills docs:

- https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- https://hermes-agent.nousresearch.com/docs/reference/skills-catalog

## Setup

Hermes treats skills as on-demand knowledge documents and stores installed skills in `~/.hermes/skills/` as the primary source of truth. Install this framework as a Hermes skill:

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git \
  ~/.hermes/skills/research-toolkit
```

Then start Hermes and verify the skill is visible:

```bash
hermes
/skills
```

Invoke it by name, or ask Hermes to use the local skill:

```text
Use the research-toolkit skill for this research task.
Read SKILL.md first, then load references only when the stage needs them.
Keep research state in the project workspace.
```

## OpenClaw Migration Path

If you already use OpenClaw and migrate into Hermes, Hermes can import OpenClaw skills. After migration, verify where the imported skill lives and whether it still contains `SKILL.md` plus `references/`.

```bash
hermes claw migrate --dry-run
hermes claw migrate
```

If the migration imports this framework into a nested imports folder, you can use it there or clone a fresh copy into `~/.hermes/skills/research-toolkit` for a cleaner path.

## Operating Notes

- Hermes supports skills as procedural memory; this framework should remain an instruction bundle, not a plugin or core tool.
- Installed skills are available as slash commands. Use `/skills` to inspect the catalog, then invoke the skill by its installed name when useful.
- Use `hermes model` and `hermes tools` normally, but do not make this framework depend on a specific provider.
- Keep `state/`, `logs/`, `data/`, drafts, and final reports in the research project workspace.
- For messaging-gateway use, ask Hermes to summarize and persist `state/progress.json` after each stage so long tasks survive across conversations.

## 中文提示

Hermes 官方技能系统把 skills 视为按需加载的知识文档，主目录是 `~/.hermes/skills/`。推荐把本仓库作为 skill 放到 `~/.hermes/skills/research-toolkit`。启动 Hermes 后用 `/skills` 确认可见，再通过技能名或自然语言让 Hermes 使用 `research-toolkit` 进行研究任务。

如果你从 OpenClaw 迁移到 Hermes，可以先运行 `hermes claw migrate --dry-run` 预览，再执行迁移。迁移后检查该 skill 是否仍包含 `SKILL.md` 和 `references/`。如果路径较深或不清晰，也可以重新克隆一份到 `~/.hermes/skills/research-toolkit`。
