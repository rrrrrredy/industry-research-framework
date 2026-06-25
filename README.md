# Longform Industry Research Protocol

A protocol framework for longform, source-backed industry research and publishable writing by AI agents.

It ships no scraper, data source, or fixed report template. Instead, it prescribes conventions for how an agent persists state, separates evidence from prose, avoids topic drift, schedules review, and turns a large research backend into a clean reader-facing article or report.

Task State Source Registry Claim Discipline Staged Drafting Review Loop Reader Revision

[Open protocol page](https://rrrrrredy.github.io/longform-industry-narrative-research/framework.html#fullmd)

## 01 Motivation: Four Failure Modes

Longform research agents tend to fail in four recurring ways:

1. **Topic overfitting**: a method distilled from one project becomes falsely treated as the universal frame.
2. **Process leakage**: the final article reads like a work log.
3. **Evidence drift**: sources, claims, uncertainty, and author judgment collapse into one narrative.
4. **False completion**: a partial milestone is reported as final completion before coverage, review, and reader-quality revision are done.

Every mechanism in this protocol targets one of those failures.

## 02 Behavioral Constraints

Hard rules of the protocol:

- Deliverable first: if the output is an article or report, do not drift into system design.
- State before scale: write task state before expanding source collection.
- Evidence is not prose: registries and audit labels stay backstage.
- Staged execution: plan, collect, analyze, draft, review, revise, then continue.
- Optional lenses only: narrative analysis and horizontal-vertical analysis are tools, not default structure.
- Review closes the loop: every audit finding becomes a revision action, downgraded claim, or explicit limitation.
- Reader review comes last: improve readability after factual and coverage checks are stable.

## 03 Architecture

```text
Main Agent
  owns thesis, structure, final judgment

Research Backend
  state files
  source registry
  claim registry
  uncertainty list
  review logs

Publishing Frontend
  thesis
  analytical sections
  synthesis
  counter-evidence
  reader-facing references
  final prose cleanup
```

Subagents may inspect or challenge bounded parts of the backend, but the main agent owns the argument and final prose.

## 04 State File System

```text
{task}/state/
  task_spec.md
  progress.json
  findings.jsonl
  directions_tried.json
  iteration_log.jsonl

{task}/logs/
  work.jsonl
  review.jsonl

{task}/data/
  source_registry.csv
  claims_registry.csv
  uncertainty_registry.csv
```

Use state files to recover after context loss. Do not rely on chat history as the only memory.

## 05 Operating Loop

1. Plan the scope, inputs, output, and done criteria.
2. Collect or process only the sources needed for that stage.
3. Convert sources into claims, uncertainty, and analysis notes.
4. Draft a bounded section or unit.
5. Review the section for evidence, coverage, structure, skepticism, and prose.
6. Revise the section and registries.
7. Update progress and define the next stage.

If one cycle adds no new evidence, case, counterexample, framework, or judgment, increment `stale_count`. If `stale_count >= 2`, pivot the structural angle rather than searching harder inside the same frame.

## 06 Analysis Lens Scheduling

Choose the lens that fits the research question:

- narrative analysis
- horizontal-vertical analysis
- adoption analysis
- capital analysis
- organization/talent analysis
- policy/legitimacy analysis
- counter-case analysis

Pick one primary lens and at most two secondary lenses unless the user explicitly requests a multi-method report.

## 07 Subagent And Review Scheduling

Use subagents for bounded work only:

- requirement mapping
- source discovery
- evidence-chain verification
- coverage audit
- skeptical review
- structure review
- reader-quality review

Subagents should not rewrite the whole report or own the thesis.

## 08 Engineering Constraints

- Every important hard claim needs a confidence boundary.
- Every 20 important facts, figures, or judgments should update source and claim registries.
- Official materials show stated position; they do not prove adoption.
- Media materials show public framing; they need corroboration for hard facts.
- User/community evidence shows reception; it is not automatically representative.
- Reader review may improve flow and clarity, but must not invent facts.

## 09 Validation And Limits

Before declaring completion:

- Required coverage is complete or limitations are explicit.
- Major claims trace back to sources or uncertainty records.
- Facts, source claims, interpretations, and author judgments remain distinct.
- Counter-evidence has been addressed.
- Reader review has been run after factual and coverage review.
- Final prose reads like an author's report, not an agent process report.

Limits:

- The protocol reduces citation and evidence errors; it does not eliminate them.
- Subagent review is a check, not external truth.
- Optional lenses can overfit the report if used mechanically.
- State files only work if updated during the task, not reconstructed after the fact.

## 10 Full SKILL.md

The authoritative instruction file is [`SKILL.md`](./SKILL.md). The protocol page includes the full skill text in a copyable block.

## Repository Structure

```text
longform-industry-narrative-research/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── docs/
│   ├── index.html
│   └── framework.html
└── references/
    ├── research-workflow.md
    ├── optional-analysis-lenses.md
    ├── horizontal-vertical-analysis.md
    ├── subagents-and-review-loop.md
    ├── writing-style.md
    ├── quality-gates.md
    └── postmortem-lessons.md
```

## Reuse

Clone or copy this repository into the directory where your agent system loads reusable skills or instruction bundles:

```bash
git clone https://github.com/rrrrrredy/longform-industry-narrative-research.git \
  ./agent-skills/longform-industry-research
```

For systems without a formal skill loader, use `SKILL.md` as the main instruction file and load files under `references/` only when the task requires them.
