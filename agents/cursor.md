# Cursor Adapter

Use this when the research task lives in a Cursor workspace.

## Setup

Add this repository as a folder, submodule, or copied instruction bundle. Then ask Cursor Agent:

```text
Use research-toolkit/SKILL.md as the instruction source for this research task.
Before drafting, create state/task_spec.md and state/progress.json in the task folder.
Keep source, claim, and uncertainty registries under data/.
Use references/quality-gates.md before completion.
```

## Operating Notes

- Cursor is useful for editing state files, drafts, and registries side by side.
- Keep the framework files read-only unless you are intentionally improving the framework.
- Put the research deliverable in a separate project folder such as `research/<task-name>/`.
- Use diffs to review whether final prose still contains process language or internal IDs.

## 中文提示

在 Cursor 中，本仓库更适合作为只读方法包。研究项目文件单独放在 `research/<task-name>/`，框架本身不要被每次研究任务污染。
