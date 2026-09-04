# Evaluation Roadmap And Claim Boundaries

Industry Research Framework needs several kinds of evidence. Combining them into one score would make the project look stronger while making its claims less trustworthy.

## Claim Ladder

| Track | Question | Current evidence | What it may claim | What it may not claim |
|---|---|---|---|---|
| A. Deterministic conformance | Did an artifact follow configured protocol and delivery rules? | Implemented: positive controls, 22 negative fixtures, source integrity, DSH adapter checks | Known structural and traceability failures are detected for tested fixtures | The report is factually correct, insightful, or useful |
| B. Cross-agent portability | Can different runtimes execute the same frozen protocol, and how do their failures differ? | Protocol frozen; no model runs published | Runtime-specific adherence and integration observations after the publication gate passes | A general framework effect from one synthetic task |
| C. Real-task efficacy | Does using the framework improve decision-useful research versus normal agent behavior? | Study design required; no valid result in this repository | A bounded treatment estimate after preregistered held-out runs and independent review | Universal superiority across models, tasks, or organizations |
| D. External adoption | Can other maintainers reproduce, extend, and keep using it? | Early maintainer-led repository; verify live GitHub and reproduction evidence at each release | Nothing beyond early project maturity | Community validation or ecosystem traction |

## Track A: Deterministic Conformance

Keep this layer fast, offline, and fail-closed. Every new mechanical rule needs both:

- a known-bad fixture that was previously accepted or is a plausible regression;
- a known-good control that proves the rule does not improve by rejecting everything.

The machine-readable result uses `result_schema_version: 2`, `conformance_status`, `conformance_score`, and `conformance_flags`. `research_quality_status` remains `not_evaluated`. A score of 100 means only that the configured mechanical checks found no issue.

High-risk flags such as false completion, malformed final review records, and configured source-instruction violations are blocking failures. `review` also exits non-zero by default.

## Track B: Frozen Cross-Agent Portability

Use [`evals/cross_agent/`](../evals/cross_agent/) for the public showcase. Run three or four agents against one frozen fictional task under two matched conditions: baseline and framework. Preserve failed runs instead of repairing them.

The publication gate requires complete paired records, input hashes, matched within-agent settings, raw process streams, workspaces, blind run mapping, and at least two independent reviews per run. Until then, the only honest label is `prepared_no_runs`.

This track is useful for integration and failure analysis. It is deliberately not the primary efficacy test.

## Track C: Held-Out Real-Task Efficacy

The primary product-effect study should use at least 12 held-out, rights-cleared real research tasks sampled from the intended workload. Freeze the design before model execution.

For each task and production agent environment:

1. Run baseline and framework conditions with the same model, reasoning setting, tools, context budget, timeout, and retry rule.
2. Keep the task, sources, and target reader fixed; randomize condition order where carryover cannot occur.
3. Preserve complete outputs, failures, latency, cost or token usage when exposed, and user corrections.
4. Blind at least two target-reader reviewers plus an evidence auditor to condition.
5. Score task fidelity, factual/evidence discipline, synthesis, counter-evidence, decision usefulness, and reader quality separately.
6. Treat invented facts, missing primary deliverables, hidden critical limitations, and false completion as critical failures that averages cannot offset.
7. Publish every task-level pair, paired differences, uncertainty intervals, disagreements, exclusions, and reruns.

Do not mix different models into the framework-effect estimate. Cross-model robustness is a later question; the causal contrast is framework versus baseline within the same production environment.

## Track D: Reproduction And Adoption

After the first tagged release, invite external users to reproduce one frozen case, submit a failure fixture, or contribute an adapter. Track external issues, pull requests, forks, reproducible run bundles, and repeat users. Stars are discovery signals, not validation.

## Data Rules

- Use synthetic packs for public deterministic and portability checks when factual freshness is not the target.
- Quarantine internally contradictory records; never leave them active merely to preserve case counts.
- Use live, dated, rights-cleared sources for efficacy studies and freeze a source snapshot for each task.
- Keep private or licensed evidence out of public bundles unless redistribution rights are explicit.
- Separate evaluator-development data, reviewer-calibration data, and final held-out tasks.

## Release Sequence

1. Stabilize conformance schema v2 and delivery semantics.
2. Publish an initial tagged release with migration notes and exact checks.
3. Execute the frozen cross-agent showcase without changing its inputs.
4. Run the preregistered real-task efficacy study.
5. Add optional domain packs or distribution plugins only when repeated external use demonstrates the need.
