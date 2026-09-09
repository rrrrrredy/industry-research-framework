# Research Toolkit

[English](./README.md) | [简体中文](./README.zh-CN.md)

Research Toolkit provides methods, workflows, and checks for AI-assisted research reports. It supports substantial, multi-source research on industries, companies, markets, technologies, and related topics.

It guides agents through defining a question, gathering sources, developing an argument, drafting sections, and reviewing the result. Task files preserve progress and evidence so longer projects can resume after an interruption.

[Explore the framework](https://rrrrrredy.github.io/research-toolkit/framework.html) · [Read reports and revision examples](./evals/diagnostics/2026-09-07/)

## Use With Your Agent

Give your agent the repository link. Ask it to read [`SKILL.md`](./SKILL.md) first and load files under `references/` as the task requires.

Send this instruction along with your research question:

```text
Use the research methods in https://github.com/rrrrrredy/research-toolkit for this task.
Read SKILL.md first, then load references/ files as needed.
Confirm the objective, scope, audience, and expected depth. Do not ask again for information already supplied.
Start with an outline, gather and analyze sources, then draft section by section.
Distinguish facts, source claims, and your analysis. Address important counterevidence and uncertainty.
Before delivery, check evidence, question coverage, depth, and readability, and resolve review findings.
Open the report with its main conclusions. Keep execution logs and internal review labels out of the prose.
For long tasks, save progress, evidence, and follow-up requirements. Describe completion accurately.
```

### If the link does not open, or you want to install it

- **Your agent cannot open GitHub**: download the repository and upload `SKILL.md`. When it needs a reference, upload that file from `references/`.
- **You want to install it in a tool you use regularly**: follow the relevant [setup guide](./agents/README.md). You can try the link-based instructions above before installing.
- **You only have a chat interface**: provide the same research instructions, and save and restore progress yourself when needed. Automatic recovery and file checks require an AI tool that can save files and run the relevant scripts.

Source retrieval, website access, and file permissions come from your AI tool. This repository supplies research methods and checks.

## How the Research Works

1. **Define the question**: establish what to answer, who will read it, the required depth, and what is out of scope.
2. **Outline and gather sources**: search against the questions, identify what the evidence supports, and record gaps.
3. **Analyze and draft sections**: explain mechanisms, differences, and implications; address counterexamples.
4. **Review and revise**: check facts, coverage, structure, and depth before polishing prose. Give each material finding a resolution.
5. **Check delivery**: review the whole report, outstanding issues, and actual files, then describe their status accurately.

Longer tasks keep separate records of objectives, progress, sources, claims, and reviews. The agent uses these records when resuming work.

[`SKILL.md`](./SKILL.md) defines the execution requirements. This README is a guide to using them.

## Suitable Tasks

Examples include:

- Researching office agents: capabilities, access conditions, business models, and adoption evidence.
- Examining a technology's progress, applications, and limitations.
- Comparing companies' products, people, technologies, and ecosystems.
- Analyzing pricing models, cost structures, and changes in a market.
- Turning a large collection of sources into an industry briefing, thematic analysis, or company report.

Simple questions, single-article summaries, software development, and creative writing generally do not need this full workflow.

## Before Delivering a Report

Use this checklist alongside a close reading of the report.

- [ ] Scope, audience, expected depth, and required questions are clear.
- [ ] Major claims have supporting sources; facts, source claims, and analysis remain distinct.
- [ ] Important counterevidence, alternative explanations, and evidence gaps have been addressed.
- [ ] The report explains mechanisms and implications at the agreed depth.
- [ ] Review findings and follow-up requirements have recorded resolutions.
- [ ] The report opens with its main judgments and contains no internal IDs, execution logs, or review labels.
- [ ] The report and delivery note agree; unfinished work is not described as complete.
- [ ] Long-running tasks have saved progress and research records that can be reused.

## Reports and Evaluation

The [published reports and revision examples](./evals/diagnostics/2026-09-07/) retain four original reports, two revisions, failed reviews, and a three-model text diagnostic, including an incomplete response. Readers can inspect the changes and their reasons. These are development and calibration examples; they do not establish general framework efficacy.

[`evals/`](./evals/) contains research tasks, source packs, rubrics, positive and negative examples, and checking scripts. Validation covers several separate questions:

- **Workflow and file checks**: detect inconsistent states, missing records, invalid delivery claims, and other reproducible failures.
- **Content review**: assess facts, analysis, counterevidence, and whether a reader can use the result. Review findings still need verification.
- **Real-task comparisons**: compare reports produced with and without the framework under matched conditions.
- **Other tools and external reproduction**: test whether other people can repeat the work in different tools.

A [matched cross-agent comparison protocol](./evals/cross_agent/) is available, but complete runtime pairs have not been published. See the [evaluation plan](./docs/evaluation-roadmap.md) for progress and limits on the conclusions.

<details>
<summary>Checking commands and result fields</summary>

Run these from the repository directory:

```bash
python scripts/run_evals.py --runs-dir evals/runs --report evals/runs/report.md
python scripts/check_regression_fixtures.py
python scripts/check_conformance_fixtures.py
python scripts/check_docs_sync.py
```

Check a specific research task before delivery:

```bash
python scripts/check_delivery.py <task-directory>
```

`conformance_status` and `conformance_score` describe deterministic structure, traceability, and configured failure signals. The offline runner keeps `research_quality_status` as `not_evaluated`; content reviews are recorded separately. Passing scripts does not establish better research quality.

The [DSH guide](./agents/deepseek-harness.md) separates local structure checks, native Skill-loading tests, and research tests using a live model. A test script's presence does not mean your environment has passed it.

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for all maintenance checks and [`evals/README.md`](./evals/README.md) for evaluation data generation.

</details>

## Further Reading

| What you need | Where to read |
| --- | --- |
| Full execution requirements | [`SKILL.md`](./SKILL.md) |
| Starting, saving progress, and resuming | [Research workflow](./references/research-workflow.md) |
| Choosing analysis methods | [Optional analysis methods](./references/optional-analysis-lenses.md) |
| Delegation and review | [Delegation and review](./references/subagents-and-review-loop.md) |
| Drafting and revising prose | [Writing guidance](./references/writing-style.md) |
| Checks before delivery | [Quality checks](./references/quality-gates.md), [delivery verification](./docs/delivery-verification.md) |
| Investigating recurring failures | [Common problems](./references/gotchas.md) |
| Installing, checking versions, and updating | [Setup guides](./agents/README.md), [version management](./docs/installation-versioning.md) |

## Maintenance and License

See [`CHANGELOG.md`](./CHANGELOG.md) for changes and [`CONTRIBUTING.md`](./CONTRIBUTING.md) for contribution requirements.

Released under the [MIT License](./LICENSE).
