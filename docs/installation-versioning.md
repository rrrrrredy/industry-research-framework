# Installation identity and safe updates

The current repository and Skill name are `research-toolkit`. GitHub redirects the former repository URL to the same project; the current page is [Research Toolkit](https://rrrrrredy.github.io/research-toolkit/).

An installation pinned to an older commit keeps that commit's content and Skill name. To use the renamed version, update to the chosen new commit, place it in a `research-toolkit` Skill directory, and check the files with the command below. Keep only the intended version enabled for a task. Recorded experiments retain their original names and hashes.

Use one repository and one normative SKILL. A release, an installed copy, a locally edited variant and the version used by an experiment can legitimately differ; identify each separately.

## Verify content, not just a label

From a trusted clone containing the intended release commit:

```bash
python scripts/check_installation.py /path/to/installed/research-toolkit --reference <full-commit-sha>
```

The command is read-only. It compares SKILL.md, all reference Markdown and the standalone delivery checker against actual Git object contents, normalizing only text newlines. It does not trust an installed Git HEAD, README version or INSTALLATION.json as proof of content identity. It does not fetch, install, write a manifest or overwrite files.

Exit 0 means the selected payload matches; 1 means a modified/missing/unreadable file; 2 means the reference could not be read. A difference is not itself a diagnosis that the variant is broken. Read the differing files before choosing what to retain. The command intentionally does not inspect other local files or prove which copy the runtime actually loaded.

Record the resolved full commit in experiments. If a local variant is intentional, record its own content hashes and label; do not call it the untouched release. A compact local Skill cannot establish that the full public Skill caused a failure, or vice versa. Fresh model runs must record the actual loaded files.

## Update without losing local work

1. Choose the release and resolve its full commit; verify its published status separately.
2. Compare the installed payload with that commit and back up the exact current installation before changing it.
3. Keep local modifications unless explicitly choosing to replace them. For a modified Git checkout, do not force-reset or overwrite the whole directory. Compare with a separate clean export and apply only the agreed files.
4. Re-run the comparison and the relevant checks. Restart/reload the agent as required by its own documented Skill discovery behavior, then verify the selected Skill was actually loaded.
5. Keep the old variant and its experiment results distinct. Updating an installation does not retroactively change which version a prior report used.

Installing only this checker does not make an old or compact Skill equal to the full release. Conversely, an unchanged protocol with an updated checker is a mixed installation until it is deliberately versioned and verified. Local manifests may document this, but their claims should be checked against content.

## Distribution scope

Keep bilingual entry documents in this repository, `SKILL.md` as the sole normative source, and environment-specific setup notes under `agents/`. Integrations may package the same Skill as a plugin, extension, or other supported bundle when that environment needs one. Packaging is optional and must not create a competing research protocol. This policy is platform-neutral; no one agent product determines the framework's distribution format.

Do not create a second maintained Skill repository merely for another language or installer. Reuse the versioned source and record the packaged commit. Keep installation and capability claims separate from demonstrated runtime conformance and research quality.

## Maintain the online copy and reader entry points

The Full SKILL block in `docs/framework.html` is a copy of `SKILL.md`. CI checks exact text agreement after newline normalization. Run `python scripts/check_docs_sync.py --write` to refresh that block after an approved normative change, then run `python scripts/check_docs_sync.py` to verify it.

README entry points should explain what readers can do: read online, load the Skill, or follow the setup notes for their environment. Keep repository-splitting decisions, copy synchronization, CI commands, and packaging policy in maintenance documentation. Update the corresponding English and Chinese passages together; their section numbers do not have to match.

中文维护要点：中英文入口共用一套研究规范，各环境按需提供接入和打包方式，不单独围绕某个 Agent 定义产品。网页完整指令由 `SKILL.md` 同步生成；修改规范后刷新并校验。README 解释读者如何阅读和使用，仓库拆分、同步检查与打包决策留在维护文档。评测资料的用途限制见[数据审计](./evaluation-data-audit.md)，语义审查的开发材料见[诊断正负例](../evals/semantic_diagnostics/)。

中文：本机版本、公开发布版和实验所用版本必须分开记账。先比较真实内容，再决定更新；不要根据旧Git提交号或自写版本标签误判，也不要为了“同步”覆盖本机修改。这个工具只核对选定运行文件，不证明报告质量或运行时真实加载。
