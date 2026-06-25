# Research Workflow

Use this file when planning or restarting a complex longform research task.

## 1. Research Brief Gate

Before collecting sources, check whether the user has supplied enough decision-critical information. If critical information is missing, ask one compact clarification batch before starting. Do not ask ritual questions when the request is already clear.

Ask only for missing critical information:

- research object and scope boundaries
- target reader and decision context
- final output format, language, and publishing context
- expected depth, rough length band, or depth level
- required coverage, exclusions, and priority units
- required materials, source exclusions, and evidence standard
- time period, geography, deadline, and whether charts/tables are expected

The expected length or depth question is required whenever it is missing. If the user does not answer, make a conservative assumption, record it in `task_spec.md`, and begin with a bounded Stage 1.

## 2. Task Specification

Before collecting more material, write:

- objective
- target reader
- final output format and language
- core question
- required coverage
- excluded claims
- minimum evidence standard
- expected depth, rough length band, and unit-level expansion plan
- planned source categories
- staged structure
- completion criteria

If the user supplied many requirements, turn them into a checklist before writing. Keep this checklist backstage; do not paste it into the final article unless requested.

## 3. State System

For long tasks, create:

```text
state/
  task_spec.md
  progress.json
  findings.jsonl
  directions_tried.json
  iteration_log.jsonl
logs/
  work.jsonl
  review.jsonl
data/
  source_registry.csv
  claims_registry.csv
  uncertainty_registry.csv
```

Use state files to survive context loss. Do not rely on chat history as the only memory.

`progress.json` should track current stage, completed units, open issues, stale_count, and next action.

`directions_tried.json` should prevent repeated digging in the same direction. If one cycle adds no new evidence, case, counterexample, framework, or judgment, increment `stale_count`. If `stale_count >= 2`, pivot the structural angle rather than merely searching harder.

## 4. Source Intake

Classify sources by function:

- official position: company, institution, regulator, author, or project self-description
- primary evidence: filings, datasets, repositories, model cards, technical reports, pricing pages, benchmark tables
- expert explanation: papers, talks, interviews, podcasts, lectures, books
- market evidence: financial reports, app intelligence, customer cases, pricing, procurement, funding data
- media interpretation: news, newsletters, longform media, trade publications
- user/community reception: forums, issues, reviews, social posts, developer discussions
- counter-evidence: failures, criticism, lawsuits, security incidents, adoption barriers, churn, cost problems

For each source, record what it can and cannot prove. Official statements show intent and positioning; they do not prove adoption. Media coverage shows framing; it does not prove market reality. User threads show reception; they are not representative samples unless supported by broader data.

## 5. Claim Registry

Track claims separately from sources.

Minimum fields:

- claim_id
- claim
- type: fact, source_claim, interpretation, author_judgment
- evidence_level: strong, moderate, weak, speculative
- supporting_sources
- counter_evidence
- uncertainty
- intended_section

Every 20 important facts, figures, or judgments, update source and claim registries before continuing.

## 6. Analysis Units

Use the unit that matches the assignment:

- company or organization
- product or service
- market segment
- technology or standard
- policy or regulation
- person or institution
- region or country
- event or period
- case study

For each unit, write an analysis card:

1. Timeline: key phases and turning points.
2. Position: current role in the market, ecosystem, debate, or workflow.
3. Mechanism: how actions produce external effects.
4. Evidence: strongest support and what each source proves.
5. Counter-evidence: limits, failures, alternative explanations.
6. Implication: what changes for readers, operators, investors, policymakers, or researchers.

Do not average length across units. Allocate space according to importance, evidence richness, and complexity.

## 7. Depth Planning

Before drafting a longform deliverable, define:

- expected reader: executive, practitioner, investor, researcher, public reader, or mixed
- expected output depth: briefing, standard report, deep report, or publishable longform article
- rough length band or section-level expansion target
- units that require extended treatment because they are central, complex, controversial, or evidence-rich
- units that may be intentionally short and why
- signals that the draft is too compressed, such as shallow mechanism explanation, list-like company coverage, missing counter-evidence, or no synthesis beyond a comparison table

Do not use source count, claim count, link count, registry completeness, or file size as a substitute for depth. A report can be evidence-complete and still be too short for the assignment.

## 8. Staged Execution

For each stage:

1. Plan the stage: scope, inputs, output, done criteria.
2. Execute: collect, process, analyze, or draft.
3. Review: coverage, evidence, structure, skepticism, and reader experience where appropriate.
4. Revise: route review findings into concrete edits.
5. Update state: progress, findings, sources, claims, uncertainty, next action.

Do not treat a partial-stage pass as whole-project completion.

## 9. Assembly

Assemble around the argument:

1. core insights or executive summary
2. scope and method note
3. main analytical sections
4. cross-case synthesis
5. counter-evidence and uncertainty
6. implications
7. conclusion
8. reader-facing references

If the draft reads like a list of sources, rewrite around mechanisms, causality, comparison, and implications.
