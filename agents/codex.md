# Codex Adapter

Use this when Codex can read or clone repositories in a local workspace.

## Setup

Clone this repository into the location where you keep reusable skills or project instructions:

```bash
git clone https://github.com/rrrrrredy/research-toolkit.git agent-skills/research-toolkit
```

Then tell Codex:

```text
Use the Research Toolkit in agent-skills/research-toolkit.
Read SKILL.md first. Load references only when needed.
For this research task, create task state files before broad source collection.
```

## Operating Notes

- Use Codex file access for `state/`, `logs/`, `data/`, drafts, and review notes.
- Keep the final answer separate from backstage registries.
- If the session resumes after compaction or interruption, recover from `state/task_spec.md`, `state/progress.json`, recent findings, and `directions_tried.json`.
- Do not let coding workflow habits replace research workflow gates; the deliverable is the research report.
- For correction-heavy multi-turn research, keep `state/requirements.jsonl` current. Before a terminal response, mirror the intended response into `delivery_message.md` and run:

```bash
python scripts/check_delivery.py <task-directory>
```

  If the check fails, deliver a clearly labeled stage artifact or repair the owning stage; do not claim final completion.

## 中文提示

把仓库放在本地项目或技能目录中，让 Codex 先读 `SKILL.md`。长任务先创建任务记录，再扩大资料搜集；继续任务时，从 `state/` 读取已有进度，不只依赖聊天记忆。

多轮纠错任务需要维护 `state/requirements.jsonl`。准备宣布终稿前，把拟发送的交付说明写入 `delivery_message.md`，运行 `python scripts/check_delivery.py <任务目录>`；未通过时只能明确交付阶段稿，或回到对应阶段修复。
