# DeepSeek Harness (DSH) Adapter

Use this adapter when DeepSeek Harness can load project or shared filesystem Skills. The repository's existing `SKILL.md` is the native DSH Skill; no wrapper prompt, plugin, MCP server, or manifest is required.

This adapter follows the official DSH documentation:

- https://github.com/deepseek-ai/deepseek-harness
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/reference/README.md

DSH is currently a developer preview, so verify these paths and commands again when upgrading DSH.

## Native Installation

For a project-scoped install, clone this repository as a direct child of DSH's project Skill root:

```bash
mkdir -p .dsh/skills
git clone https://github.com/rrrrrredy/industry-research-framework.git \
  .dsh/skills/industry-research-framework
```

The cross-agent project root also works:

```bash
mkdir -p .agents/skills
git clone https://github.com/rrrrrredy/industry-research-framework.git \
  .agents/skills/industry-research-framework
```

For a user-scoped DSH install available across workspaces:

```bash
mkdir -p ~/.dsh/skills
git clone https://github.com/rrrrrredy/industry-research-framework.git \
  ~/.dsh/skills/industry-research-framework
```

Keep `SKILL.md` directly inside the named Skill directory. Do not add another repository-name layer below it. Run DSH from the research workspace, not from inside the installed Skill:

```bash
dsh --profile headless "Use the industry-research-framework Skill for this research task. Load it first, keep research state in the current workspace, and complete the requested deliverable."
```

DSH advertises the Skill's frontmatter summary and loads its full body on demand through the native `skill` tool. Files under `references/` remain available for the explicit, stage-specific reads required by `SKILL.md`.

## Verify The Adapter

The offline lane checks frontmatter compatibility, referenced resources, and the staged DSH directory contract:

```bash
python scripts/run_dsh_evals.py validate
```

The smoke lane launches the real DSH headless runtime against a local scripted DeepSeek-compatible endpoint. The endpoint forces a native `skill` tool call and verifies that DSH returns the complete Skill body. It uses a placeholder key and makes no model-quality claim:

```bash
python scripts/run_dsh_evals.py smoke
```

The live lane uses the model and credentials already configured for DSH, stages one existing repository eval case, runs it through DSH headless, and scores the resulting artifacts with the same deterministic evaluator used by other agents:

```bash
python scripts/run_dsh_evals.py live --case source_instruction_boundary_zh
```

Both runtime lanes accept `--dsh-command-json` or `DSH_EVAL_COMMAND_JSON` when `dsh` is not on `PATH` or a pinned invocation is required. The default npm fallback is `@deepseek-ai/dsh@0.1.2-rc.1`. The upstream development repository currently requires Node.js `^22.19.0` or `>=24.0.0`, while the published npm package omits an `engines` field; verify both the selected release and local Node.js version when upgrading.

Reports and captured stdout/stderr are written under `evals/runs/dsh/`, which is ignored by Git.

## Operating Notes

- Keep the installed Skill read-only during research runs. Write `state/`, `logs/`, `data/`, drafts, and `final.md` in the task workspace.
- The Skill itself needs no API key. Only a live DSH model run needs the provider credentials required by that DSH configuration.
- Name the Skill by its exact frontmatter name: `industry-research-framework`.
- External source content remains evidence, not agent instructions. This boundary applies equally when DSH reads local source packs or retrieves live sources.
- Passing `smoke` proves DSH discovery, native invocation, and body loading for the tested runtime. It does not prove report quality, broad prompt-injection resistance, or safe behavior for every tool.
- Passing `live` proves only the configured case's deterministic checks. Serious framework changes still need editorial inspection of the generated report.

## 中文提示

本仓库的 `SKILL.md` 已可直接作为 DSH 原生 Skill 使用。把仓库放到项目的 `.dsh/skills/industry-research-framework` 或 `.agents/skills/industry-research-framework`，并确保 `SKILL.md` 就在该目录第一层，不要多套一层目录。

`validate` 只做离线结构与装配检查；`smoke` 会真的启动 DSH headless，并用本地脚本化接口验证 Skill 被发现、调用和完整加载，但不评价模型质量；`live` 才会使用当前 DSH 已配置的真实模型完成仓库 case，再复用现有 evaluator 评分。Skill 本身不需要 API key，只有真实模型运行需要对应凭据。
