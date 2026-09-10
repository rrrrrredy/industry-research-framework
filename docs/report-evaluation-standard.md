# Report evaluation: current standard

This is the project's evaluation design, not an extra requirement for every Research Toolkit user. It does not replace the research method in `SKILL.md`. Use this standard for new report studies; retain earlier frozen experiments with their original scales and reviewer counts.

## One rubric, separate questions

All current report studies use five dimensions, each scored **0–4** or `not_assessed`: task fidelity; facts and evidence; explanation and synthesis; counterevidence and boundaries; reader usefulness. Depth is assessed within the substantive analysis and the requested deliverable, not dropped when using five dimensions. Readability includes a useful opening, coherent structure, concrete language and freedom from work-log prose.

The shared anchors are: 0, the essential requirement is absent or fails; 1, major defects make this aspect unusable; 2, partly met but substantive revision is needed; 3, meets the task with bounded issues; 4, fully developed with concrete support. Missing assessment context is `not_assessed`, not zero or approval. Each rating needs a reason and a locatable excerpt. Do not compute a weighted overall passing score or convert historical 1–5 results into this scale.

Keep four results separate:

| Result | What it establishes |
| --- | --- |
| Execution record | Which method, sources, tools, stages and interventions were actually used. Files alone do not establish chronology or reading. |
| First-submission quality | The first complete candidate after the assigned workflow's own checks, before the shared external review feedback. Failure remains part of the result. |
| Repair and delivery | What valid feedback changed, the new version's quality, regressions, and the effort required to reach a usable report. |
| Product effect | Baseline versus toolkit on independent, matched tasks; not the quality of a repeatedly edited showcase alone. |

## Common workflow

1. Admit the task: preserve its origin, reader, cutoff, scope, source access, rights and task-family exposure. Freeze task-specific coverage and evidence requirements before writing; do not provide the desired research conclusion.
2. Freeze the study version, author/runtime settings, normal tool access, review conditions and endpoints. The baseline disables the tested toolkit, not normal search or all ordinary self-checking. Preserve context separation and randomize paired condition order. Any resource/stopping or retry rule must be declared before a batch; no hidden 15-minute/60-minute deadline is introduced here.
3. Run the assigned workflow. For the toolkit condition this includes outline, research, analysis, section writing and review, followed by an actual whole-report reading. Check whether the outline addresses the actual questions and whether its section hierarchy supports the argument before drafting; revise it when evidence changes the argument. Follow any task-specific independent structure-review requirement, without adding another default four-model panel. Capture genuine events; do not manufacture missing historical steps.
4. Save the first complete candidate without overwriting it. Four non-author reviewers receive the same full task, report and evidence version, independently. Current roles are Astra in Codex as sole author/reviser; GPT-5.6 Sol high in a fresh Codex context, DeepSeek, Kimi and GLM-5.3 high as reviewers. These roles are this study's configuration, not a dependency of the toolkit.
5. Lock original reviews before exposing feedback. Record every finding, including disagreements and failed calls. The author/operator checks the actual passage and source before accepting a correction. Do not substitute votes for evidence.
6. Batch the justified repairs into a new version, check affected analysis and the whole report, then obtain four same-version reviews. Do not reuse an older review as approval of edited text. A transport or formatting failure is not a zero-quality report and is not retried silently.
7. Deliver when the common readiness conditions below are met. Preserve initial and later results, interventions, time, tokens or known costs, unknown charges and unresolved evidence limits separately.
8. Aggregate product feedback across all completed evaluations, decide what to adopt and why, modify the toolkit where justified, and verify regressions. Known serious defects may be fixed earlier with separate version groups. Final project acceptance includes this product work, not only reports and scores.

## Findings, repairs and stopping

| Finding after checking the evidence | Required handling |
| --- | --- |
| Critical | Invented or conclusion-reversing facts, missing primary deliverables, concealed decisive limits, source instructions taking control, or false completion: record and repair; unresolved means no final delivery. |
| Major | A required question, central mechanism, comparison or evidence chain is materially deficient, or the report needs substantive restructuring to be usable: record and repair. |
| Minor, confirmed defect | Correct a factual imprecision, misleading sentence, broken reference or other demonstrated local defect in a batched revision; do not ignore it solely because the label says minor. |
| Optional preference or unsupported allegation | Record a reasoned rejection or no-change decision. An extra column, repeated caveat, preferred title style or speculative correction does not force another round. |
| Unresolved evidence dispute | Seek the relevant source or permitted alternative. A missing mandatory reading/task remains open; disclosure alone cannot waive it. If the task permits a bounded conclusion and evidence remains genuinely unavailable, state what cannot be concluded without silently deleting the required question. |

A readiness decision requires: the promised report and required questions are present; mandatory reading is completed or covered by an actual relevant user decision; important claims are supported or accurately bounded; analysis and depth meet the task; the complete current text has been read; four current reviews are complete and every finding has an evidenced disposition; no unresolved critical/major issue or confirmed defect remains. Applicable delivery records must match the current artifact. Script success, four favorable labels and high mean scores cannot replace this decision.

For material user requirements and explicit corrections, point to the current passage, table or other requested output that satisfies each one. Check what it actually says; a filled mapping, reviewer label or old version's location is not evidence of satisfaction. Keep unresolved corrections open. Check the title, opening and section structure against the task, not just the reviewer's last list of edits. Hash binding catches an outdated review record; it cannot establish that the reviewer read carefully or judged correctly.

Stop editorial iteration when these conditions hold; do not seek four empty finding lists or maximize every score. If a new substantive defect appears, reopen it. Repeated optional suggestions alone are not progress. This study's user has authorized continued repair until the work is complete, so there is no required number of repair rounds here and no claim that nine rounds is a good default. This does not remove the toolkit's ordinary review checkpoints. General research stagnation guidance is not a permission to abandon a mandatory requirement.

## Fair comparisons and feedback use

The primary matched comparison is first submission versus first submission. Extra operator coaching or user corrections before that endpoint are recorded as interventions; they cannot silently become ordinary autonomous performance. If repair is studied, both conditions receive the same prospectively declared reviewer access, feedback, revision opportunities and stopping procedure. Report repair rounds and effort separately; a nine-round report and a one-round baseline are not a matched final-quality comparison.

Keep development tasks, reviewer checks, and independent effect tests separate. A task used to fix the method or judge instructions cannot remain held out. Translations, renamed cases, correlated task families and reruns do not increase the independent task count. Twelve distinct task families are a screening design, not a power guarantee. Freeze their actual sampling and analysis plan before those runs; preserve both-failed, unresolved and excluded cases rather than turning them into wins.

LLM review is fallible. Use known-error, valid, instruction-injection and ambiguous-evidence controls; retain false alarms and missed defects. Order/length effects and supplier overlap remain possible. Material factual disputes require source checks, not another majority vote. This project does not require human reviewers for its current lane and must not claim human calibration. The design follows the separation of objectives, data, criteria and iterative feedback in [OpenAI's evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices); that guidance also recommends human calibration, which is not supplied here.

For each product issue retain: failing example, impact, root cause, accepted/rejected/deferred decision, change or commit, regression evidence and remaining limits. Distinguish a missing method, an existing rule not executed, a checker gap, a source-access mistake and a reviewer error. Do not automatically add all suggestions to `SKILL.md`. Same-task improvements demonstrate a repair; unused tasks are needed for a broader effect claim.

## Earlier records

`evals/rubrics/research_quality.json` is an earlier seven-dimension, human-review-oriented guide. `evals/cross_agent/review_rubric.md` and its two-reviewer, 1–5 scale belong to a frozen portability protocol. Historical two/three-reviewer semantic diagnostics and withdrawn studies retain their original provenance. They are not the current report-study standard and their scores cannot be pooled with it. Retain their bytes and original failure status; a new standard is not retrospective evidence that it was followed.

---

# 报告评测：现行标准

本页统一本项目后续评测，不给所有工具箱用户增加四模型审稿义务，不替代 `SKILL.md` 的研究方法。历史冻结实验保留原量表、人数和失败，不按新标准倒填“已遵循”。

## 评分与记录

统一五维：**任务遵循、事实与证据、解释与综合、反证与边界、读者可用性**。每维0–4分：0核心要求缺失或不成立；1重大缺陷；2仍需实质修订；3满足任务且问题有界；4充分展开且有具体依据。证据不足用 `not_assessed`，不当0分或通过。各分须有理由和正文定位，不算抵消严重问题的总及格分。分析深度仍在综合与交付要求中检查，没有从五维中删除。

执行是否真实、第一份完整交稿质量、返工后可用性、工具箱相对基线的效果，是四项不同结果。先保存原稿和原评审，再修问题；修后结果不覆盖第一次表现。四位评审仍为Sol high、DeepSeek、Kimi、GLM-5.3 high，写作和返工仅由Codex内Astra承担。四位读同版完整材料、意见互相隔离；作者自查不计独立评审。

## 统一流程与返工

出题和来源准入 → 冻结任务及评测配置 → 提纲、研究、分节写作与实际审读 → 锁定第一份完整稿 → 四人独立初评 → 逐条证据裁定 → 集中返工 → 同版四人复评 → 可用报告 → 汇总反馈并调整产品、验证回归。

- 写作前检查提纲是否回答实际问题、章节层级是否支撑论证；资料改变判断时相应调整。任务明确要求独立结构审阅时照办，不给所有任务再加一轮四模型提纲评审。
- 严重事实/结论错误、主要交付缺失、隐瞒决定性限制、被来源指令操纵或虚假完成，必须修；关键问题、论证或证据链不足也必须修。
- 已证实的小错误同样集中修复，不因标为minor就忽略。可选文风、重复补充和无证纠错，记录不采纳理由，不强制开新一轮。
- 未读完的必读材料或未完成的必做要求，不能靠“披露限制”关闭。需要相应用户决定才能放弃；允许有界研究的题则如实解释证据未知及其影响，不编造答案或偷删问题。
- 交付须满足原任务、重要主张有依据、分析与深度足够、当前全文实际读完、四份当前评审齐全且逐项裁定、没有未解决的严重/实质问题或已证缺陷，适用的交付记录与正文一致。不是四票通过、总分高或脚本PASS就交付。
- 对重要用户要求和明确纠错，定位到当前稿实际满足要求的段落、表格或其他交付内容，并核读内容是否成立。映射表填满、审查者给PASS、旧稿曾满足，都不能销账。标题、开篇与章节结构仍须对照任务检查，不能只复核上轮列出的几处修改。哈希检查能拦旧版审阅，不能证明审阅认真或判断正确。
- 达到这些条件就停止润色，不要求模型“再也提不出意见”。发现新的实质缺陷要处理，重复的可选建议不算新进展。本轮用户已授权持续返工至完成，因此不设固定返工轮数，也不暗设15或60分钟上限；这不取消工具箱日常使用的审阅检查点。

## 对照与产品改进

第一次完整交稿对第一次完整交稿；如果还比较返工，两组事先取得相同评审反馈、返工机会和停止规则，分别报告初始/修后结果及成本。不能把九轮改好的文章与一次生成的基线直接比较。额外操作者辅导、用户更正和环境变化要单列。

用户报告、补充开发题、评审控制和正式独立题分别计数。用于改规则的题不得继续算未参与开发；换标题、翻译、同题重跑不增加独立样本。12题族是初步筛查设计，不是统计保证，具体抽样与分析须在运行前锁定。没有真人校准时明确是LLM评审及来源核对，不宣称客观金标准。

所有评测结束后，逐项交付产品反馈处置：失败依据、影响与归因、采纳/拒绝/暂缓理由、实际修改、回归结果和剩余边界。区分方法欠缺、已有规则未执行、检查器缺陷、资料读取失误和模型误报，不把它们全变成新提示词。同题修好证明案例修复，未用过的任务才用于更广泛效果验证。

旧七维人工量表、冻结跨运行时协议的1–5分/双评审，以及旧双/三模型开发样例均为历史记录，不是现行报告标准；不能换算合并。新旧方案的兼容说明不改变原始数据。
