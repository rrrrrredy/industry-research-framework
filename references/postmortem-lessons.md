# Postmortem Lessons

These lessons were distilled from a demanding longform industry research project and generalized for future research-writing tasks.

## What Worked

- State files prevented context loss.
- Source, claim, and uncertainty registries reduced unsupported claims.
- Section-by-section writing produced better work than one-shot generation.
- Review logs were useful only when every issue was routed to a concrete revision.
- Reader-facing cleanup made the final piece feel like a publishable article rather than a work report.
- Counter-evidence improved the argument when integrated into analysis instead of parked at the end.

## What Failed Or Was Risky

- The task drifted into system design even though the desired output was a research article.
- Too much process scaffolding leaked into prose.
- Repeated phrases such as "user-provided material" and "the source shows" weakened author voice.
- Treating one topic-specific project as the universal method overfit the skill.
- Subagents sometimes echoed the main agent's assumptions instead of independently checking them.
- Large registries were useful backstage but unreadable as public appendices.
- Declaring completion after a partial milestone caused false closure.
- A forward test can pass state-file and registry checks while still producing a report that is too short. Backend completeness is not the same thing as publishable depth.
- Detailed instructions did not prevent a chat response from overstating completion because the visible claim was outside the existing deterministic check.
- Material corrections added across many turns were vulnerable to loss without stable requirement ids and terminal reconciliation.
- A PASS for one section or review dimension was wrongly treated as evidence for the whole delivery.
- Extra lifecycle machinery increased state volume without improving the reader-facing artifact or the truth of the completion claim.

## User Preference Pattern

For long research writing, the preferred output is:

- thesis-led
- evidence-backed
- detailed where complexity requires it
- explicit about expected depth before drafting
- written section by section
- clean of process language
- explicit about uncertainty without becoming defensive
- supported by reader-facing references
- reviewed for both factual discipline and reading experience

## Method Pattern

Use a two-layer system:

1. Research backend: sources, claims, uncertainty, logs, review.
2. Publishing frontend: argument, structure, prose, references.

The backend makes the article reliable. The frontend makes it worth reading.

The delivery boundary connects both layers: current requirements, global review, accepted limitations, artifact hashes, and the user-visible status must agree. A stage artifact may be useful and honestly delivered without passing the terminal gate.
