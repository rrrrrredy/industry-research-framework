---
name: industry-research-framework
description: Framework for longform, source-backed industry research and publishable writing by AI agents. Use when an agent must plan, clarify, collect, verify, analyze, draft, review, revise, and finalize a substantial industry, market, company, product, technology, policy, or ecosystem research article/report across multiple stages and many sources. Prescribes a scope contract, research brief gate, task state, source/claim/uncertainty registries, depth budgeting, staged execution, optional analysis lenses, subagent review, reader-quality revision, and final prose cleanup. Do not use for quick factual answers, simple summaries, citation formatting only, spreadsheet-only work, or purely creative writing.
---

# Industry Research Framework

This skill is a framework for longform industry research and publishable writing. It ships no scraper, data source, or fixed report template; instead it prescribes conventions for how an AI agent persists state, separates evidence from prose, avoids topic drift, schedules review, and turns a large research backend into a clean reader-facing article or report.

## 1. Motivation

Longform research agents tend to fail in five recurring ways:

1. Topic overfitting: a method distilled from one project becomes falsely treated as the universal frame.
2. Process leakage: the final article reads like a work log, with phrases such as "the user provided" or "the material shows".
3. Evidence drift: sources, claims, uncertainty, and author judgment collapse into one undifferentiated argument.
4. False completion: a partial milestone is reported as final completion before coverage, review, and reader-quality revision are done.
5. Depth collapse: a report satisfies source counts and coverage checklists but is too short, compressed, or thin for the user's expected research depth.

Every mechanism in this framework targets one of those failures.

## 2. Scope Contract

This skill is an execution framework for producing substantial research deliverables. It is not a theory system, product architecture, or universal modeling language.

Keep inside this skill:

1. Process: research scope calibration, staged execution, source processing, drafting, review, revision, and final cleanup.
2. State: task state, progress, findings, assumptions, decisions, and direction tracking.
3. Audit: source, claim, uncertainty, coverage, depth, and reader-quality checks.

Keep outside this skill unless the user explicitly asks for a separate system design project:

1. Domain ontologies, universal taxonomies, or generalized modeling languages.
2. Intermediate representations, scoring systems, embeddings, knowledge graphs, or ranking engines.
3. Dashboards, CLIs, databases, automation pipelines, or product architecture.
4. Methodology manifestos that do not directly improve the current research deliverable.

If a task starts drifting into the excluded layers, preserve the current deliverable path, record the idea as a future extension, and do not expand the workflow.

## 3. Behavioral Constraints

1. Deliverable first: if the requested output is an article or report, do not drift into system design, prompt design, or workflow exposition.
2. Research brief gate before collection: ask one compact clarification batch when decision-critical information is missing.
3. State before scale: for long tasks, write task state to files before expanding source collection.
4. Evidence is not prose: registries, logs, audit labels, and access failures stay backstage unless the user requests an audit appendix.
5. Depth budget before drafting: record expected depth, rough length band, unit-level expansion plan, and what "too short" would mean for this task.
6. Staged execution: plan, collect, analyze, draft, review, revise, and update state before moving to the next unit.
7. Section-level progress: write complex work by section, company, case, period, or argument; do not generate the whole report in one pass.
8. Optional lenses only: framing/category analysis, horizontal-vertical analysis, capital analysis, and adoption analysis are tools, not default structure.
9. Review closes the loop: every audit finding must become a revision action, a downgraded claim, or an explicit limitation.
10. Reader review comes last: improve readability only after factual, coverage, structure, and depth checks are stable.

## 4. Architecture

    Main Agent
    owns thesis, structure, final judgment

    Research Backend   Publishing Frontend
    state files        thesis / sections
    source registry    mechanisms / synthesis
    claim registry     counter-evidence
    uncertainty list   reader-facing references
    review logs        final prose cleanup

Subagents may inspect or challenge bounded parts of the backend, but the main agent owns the argument and final prose.

## 5. State Files

For substantial work, create:

    {task}/state/
      task_spec.md            # objective, reader, output, scope, depth, evidence standard, assumptions
      progress.json           # stage, completed units, open issues, stale_count
      findings.jsonl          # append-only findings and judgments
      directions_tried.json   # directions already attempted
      iteration_log.jsonl     # stage summaries

    {task}/logs/
      work.jsonl              # execution decisions
      review.jsonl            # review findings and routed fixes

    {task}/data/
      source_registry.csv
      claims_registry.csv
      uncertainty_registry.csv

Use state files to recover after context loss. Do not rely on chat history as the only memory.

### Context Recovery Protocol

When resuming after context loss, session restart, or handoff:

1. Read `state/task_spec.md` for objective, scope, reader, output, depth, evidence standard, and assumptions.
2. Read `state/progress.json` for current stage, completed units, open issues, stale_count, and next action.
3. Read the latest entries in `state/findings.jsonl` and `state/iteration_log.jsonl` to recover the recent direction.
4. Read `state/directions_tried.json` to avoid repeating failed or exhausted paths.
5. Resume from the matching step in the operating loop.

Do not re-run completed stages. Do not re-ask the research brief if `task_spec.md` already records the answers.

## 6. Research Brief Gate

Before collection, decide whether the request contains enough decision-critical information. If not, ask one compact batch of questions before starting. The batch should usually contain 3-7 questions and must cover expected length or depth when it is missing.

Ask only for missing critical information:

- research object and scope boundaries
- target reader and decision context
- output format, language, and publishing context
- expected depth, rough length band, or depth level
- must-cover units, exclusions, and priority areas
- required sources or materials, source exclusions, and evidence standard
- time period, geography, deadline, and whether charts/tables are expected

If the user has already supplied enough context, do not ask ritual questions. Proceed, record assumptions in `task_spec.md`, and mark unresolved non-critical details as assumptions or uncertainties.

If critical details remain unanswered after one clarification batch, make conservative assumptions, record them, and begin with a bounded Stage 1 instead of stalling.

## 7. Operating Loop

For each stage:

1. Run the research brief gate, then plan the scope, inputs, output, and done criteria.
2. Collect or process only the sources needed for that stage.
3. Convert sources into claims, uncertainty, and analysis notes.
4. Draft a bounded section or unit.
5. Review the section for evidence, coverage, structure, skepticism, and prose.
6. Revise the section and registries.
7. Update progress and define the next stage.

If one cycle adds no new evidence, case, counterexample, framework, or judgment, increment `stale_count`. If `stale_count >= 2`, pivot the structural angle rather than merely searching harder.

For longform deliverables, do not use source count, claim count, link count, or file size as completion substitutes. They are backend health signals, not proof that the finished report has enough depth. Before final assembly, compare the draft against the depth budget and expand thin units before reader review.

## 8. Source And Claim Discipline

Classify sources by what they can prove:

- official materials show stated position, intent, product surface, or formal policy
- primary data supports measurable claims when definitions and collection methods are clear
- expert materials explain reasoning, context, and interpretation
- media materials show public framing but need corroboration for hard facts
- user/community evidence shows reception but is not automatically representative
- counter-evidence limits, weakens, or falsifies the main claim

Classify claims separately:

- verified fact
- source claim
- interpretation
- author judgment
- speculation

Every important hard claim should have a confidence boundary. Do not turn company PR, investor hopes, or media amplification into fact.

## 9. Analysis Lens Scheduling

Choose the lens that fits the research question:

- framing/category analysis: positioning, legitimacy, category creation, public meaning, and media translation
- horizontal-vertical analysis: timeline depth plus current competitor/substitute comparison
- adoption analysis: user behavior, workflow change, replacement, friction
- capital analysis: pricing, revenue, valuation, funding, cost structure, margins
- organization/talent analysis: operating model, hiring, leadership, talent flow
- policy/legitimacy analysis: regulation, compliance, trust, geopolitical or institutional pressure
- counter-case analysis: strongest alternative explanation and failure modes

Pick one primary lens and at most two secondary lenses unless the user explicitly requests a multi-method report.

Read `references/optional-analysis-lenses.md` when choosing lenses. Read `references/horizontal-vertical-analysis.md` only after that lens has been selected.

## 10. Subagent Scheduling

Use subagents only for bounded work:

- requirement mapping
- source discovery for separate regions, actors, or source classes
- evidence-chain verification
- coverage audit
- skeptical review
- structure review
- reader-quality review after the draft is stable

A subagent prompt must include objective, files or sections to inspect, output format, PASS/FAIL criteria, and boundaries. Subagents should not rewrite the whole report or own the thesis.

Read `references/subagents-and-review-loop.md` before delegation.

## 11. Finalization

The final article or report should contain reader-facing material only:

- conclusion-first insights when useful
- scope note
- analytical sections organized by argument, case, period, or mechanism
- synthesis across units
- counter-evidence and uncertainty expressed cleanly
- implications
- reader-facing reference appendix

Remove:

- visible source IDs
- audit labels
- file paths
- "the user provided"
- "the material shows"
- "this source supplements"
- "this section passed audit"
- excessive caveats that weaken rather than clarify judgment

## 12. Validation And Limits

Before declaring completion:

1. The research brief gate was completed or assumptions were recorded.
2. Required coverage is complete or limitations are explicit.
3. Major claims trace back to sources or uncertainty records.
4. Facts, source claims, interpretations, and author judgments remain distinct.
5. Counter-evidence has been addressed.
6. The draft meets the depth budget or explicitly explains why the original expected depth is no longer appropriate.
7. Reader review has been run after factual, coverage, structure, and depth review.
8. The final prose reads like an author's report, not an agent process report.

Limits:

1. The framework reduces citation and evidence errors; it does not eliminate them.
2. Subagent review is a check, not external truth.
3. Optional lenses can overfit the report if used mechanically.
4. State files help recovery, but they only work if updated during the task, not reconstructed after the fact.

## 13. Execution Guardrails

Use these guardrails to prevent loops, overcollection, and scope drift:

1. Source collection: if three consecutive searches or source passes add no relevant evidence, stop collecting in that direction, update `directions_tried.json`, and draft or pivot.
2. Claim extraction: if `source_registry.csv` grows while `claims_registry.csv` stays thin, pause collection and extract claims before gathering more sources.
3. Review loop: cap full review-revise cycles at two per section unless the user asks for more; record unresolved issues as limitations or follow-up tasks.
4. Depth check: before reader review, compare the draft against the depth budget and expand thin units before optimizing prose.
5. Scope expansion: if new work falls outside `task_spec.md`, record it as a proposed extension and ask before expanding the project.
6. Subagent review: prompts must ask the reviewer to actively look for issues; if no issue is found, the reviewer must state what evidence supports PASS.

## References

- Read `references/research-workflow.md` only when starting a substantial project, creating state files, or resuming after context loss.
- Read `references/optional-analysis-lenses.md` only when the research question needs an explicit analysis lens decision.
- Read `references/horizontal-vertical-analysis.md` only when horizontal-vertical analysis has been selected.
- Read `references/subagents-and-review-loop.md` only before delegating work or running a review loop.
- Read `references/writing-style.md` only when entering drafting, final cleanup, or reader-driven revision.
- Read `references/quality-gates.md` only before declaring a stage or final deliverable complete.
- Read `references/postmortem-lessons.md` only when adapting this framework or diagnosing repeated task drift.


