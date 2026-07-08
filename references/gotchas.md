# Gotchas

Use this reference when the agent repeatedly drifts, when eval output passes mechanically but reads poorly, or when adapting the framework to a new agent runtime.

## Registry Theater

Symptom: `source_registry.csv`, `claims_registry.csv`, and review logs exist, but the final report is still a list of sources or facts.

Repair:

1. Pick the central reader question again.
2. Convert source rows into mechanisms, tradeoffs, counter-cases, and implications.
3. Rewrite the section around the argument, not around source order.

Eval signal: high artifact score, high bullet density, repeated source-listing phrases, weak synthesis in manual review.

## Source-Listing Prose

Symptom: paragraphs repeatedly say "source X says Y" or "this source supports trend recognition".

Repair:

1. Move source-by-source evidence back into notes or registries.
2. Keep source titles only where they help the reader evaluate evidence.
3. Merge related source claims into one reader-facing judgment with a confidence boundary.

Eval signal: repeated template-like lines or repeated source-listing phrases.

## Evidence Drift

Symptom: verified facts, company claims, media framing, user anecdotes, and author judgment collapse into one confident conclusion.

Repair:

1. Label each important claim as fact, source claim, interpretation, author judgment, or speculation.
2. Downgrade any conclusion supported only by PR, media amplification, or community evidence.
3. Add uncertainty or counter-evidence where the source class cannot prove the claim.

Eval signal: thin or empty `claims_registry.csv`, absolute language without uncertainty, weak claim discipline terms.

## False Completion

Symptom: `progress.json` or the final response claims completion while coverage gaps, review findings, or depth problems remain.

Repair:

1. Reopen the current stage and record the blocking issue.
2. Route each review finding to a revision, downgraded claim, or explicit limitation.
3. Mark final only after quality gates and reader cleanup pass.

Eval signal: progress status claims final completion while the runner still reports coverage or quality flags.

## Depth Collapse

Symptom: the report is concise and clean, but central units are compressed or generic relative to the promised depth.

Repair:

1. Re-read the depth budget in `task_spec.md`.
2. Identify thin units by section, company, period, mechanism, or case.
3. Expand the units with mechanisms, examples, counter-evidence, and implications before reader cleanup.

Eval signal: low non-space character count, missing expected sections, high list ratio, or human review saying "too shallow".

## Lens Overreach

Symptom: framing, horizontal-vertical analysis, capital analysis, or another lens becomes a rigid template even though the user asked for a practical report.

Repair:

1. Restate the reader's decision context.
2. Keep the lens as an analytical tool, not as the section structure unless it truly fits.
3. Delete methodology exposition from the final prose.

Eval signal: final prose explains the method more than the industry question.

## Subagent Sprawl

Symptom: subagents expand scope, rewrite the whole report, or produce conflicting theses.

Repair:

1. Give subagents bounded files, sections, or source classes.
2. Require PASS/FAIL criteria and issue lists.
3. Keep thesis ownership with the main agent.

Eval signal: review logs contain broad rewrites instead of actionable findings, or final prose loses a stable argument.
