# Evaluation Roadmap And Claim Boundaries

Research Toolkit needs several kinds of evidence. Combining them into one score would make the project look stronger while making its claims less trustworthy.

## Claim Ladder

| Track | Question | Current evidence | What it may claim | What it may not claim |
|---|---|---|---|---|
| A. Deterministic conformance | Did an artifact follow configured protocol and delivery rules? | Implemented: positive controls, 22 negative fixtures, source integrity, DSH adapter checks | Known structural and traceability failures are detected for tested fixtures | The report is factually correct, insightful, or useful |
| B. Cross-agent portability | Can different runtimes execute the same frozen protocol, and how do their failures differ? | Protocol frozen; no completed runtime pairs published | Runtime-specific adherence and integration observations after the publication gate passes | A general framework effect from one synthetic task |
| C. Real-task efficacy | Does using the framework improve decision-useful research versus normal agent behavior? | Study design required; no valid result in this repository | A bounded treatment estimate after preregistered held-out runs and independent review | Universal superiority across models, tasks, or organizations |
| D. External adoption | Can other maintainers reproduce, extend, and keep using it? | Early maintainer-led repository; verify live GitHub and reproduction evidence at each release | Nothing beyond early project maturity | Community validation or ecosystem traction |

## Track A: Deterministic Conformance

Keep this layer fast, offline, and fail-closed. Every new mechanical rule needs both:

- a known-bad fixture that was previously accepted or is a plausible regression;
- a known-good control that proves the rule does not improve by rejecting everything.

The machine-readable result uses `result_schema_version: 2`, `conformance_status`, `conformance_score`, and `conformance_flags`. `research_quality_status` remains `not_evaluated`. A score of 100 means only that the configured mechanical checks found no issue.

High-risk flags such as false completion, malformed final review records, and configured source-instruction violations are blocking failures. `review` also exits non-zero by default.

## Development Reports And Review Diagnostics

The [2026-09-07 evidence package](../evals/diagnostics/2026-09-07/) includes actual calibration reports, retained failures, editorial repairs and three-model text diagnostics. It is not part of the held-out study or the cross-runtime publication gate. Model/provider, context exposure, retrieval access, requested and returned identity where available, incomplete responses and adjudication are disclosed separately. Different vendors diversify viewpoints; their agreement is neither factual ground truth nor human calibration.

The protocol's numbers (usually 3–7 clarification questions, ledger maintenance intervals, stagnation triggers and review-loop budgets) are operational heuristics, not empirically optimized thresholds. No current ablation establishes their superiority. The clarification rule still asks only for missing essential information. Preserve these defaults until observed premature stops, missed stalls, redundant searches or maintenance costs justify a scoped comparison; do not infer validity from numerical precision.

The two stagnation signals observe different units:

| Signal | Observation | Intended response |
| --- | --- | --- |
| Two stale complete unit cycles | Evidence-to-argument cycles add no useful analytical progress, even if sources were found | Change the structural angle |
| Three unproductive searches/source passes | A collection direction yields no useful evidence | Stop that collection direction |

This is an explanation of existing rules, not a new schema or extra required stage files. Self-authored non-empty gate files would not prove that a stage happened before the next one. Current receipts bind final artifacts and reviews; full intermediate-stage chronology remains only partly observable.

## Current Report And Review Plan

Complete and verify all accepted method, execution, checker, data and documentation corrections before starting new report-writing or model-review runs. Offline regressions are preparation, not an efficacy study; green CI alone does not authorize a study start.

The current development lane uses Astra inside Codex as the sole author, actually loading the pinned framework and using its research workflow. Every report, in both initial review and re-review, receives four separate reviews: GPT-5.6 Sol (`gpt-5.6-sol`, `high`) in a fresh Codex context, DeepSeek, Kimi, and GLM-5.3 (requested `high`). DeepSeek, Kimi and GLM are reviewers, not substitute authors. This is a study configuration, not a Codex dependency or a four-model requirement of the framework itself.

Give all four reviewers the same complete report version, task and supplied evidence, with version hashes. Do not expose another reviewer's current-round opinion before their response is locked. Record actual context, tools, evidence access, model identity when exposed, truncation and failures. Three responses constitute an incomplete panel, not a completed four-reviewer round. Author self-checks do not count as independent reviews; different models do not guarantee statistical independence.

GLM was added after some three-reviewer development runs had started. Keep those original freezes and opinions; label its same-input supplementary review as a later addition, not an originally preregistered four-person panel. The GLM lane uses a genuine supported Coding Plan client, not arbitrary HTTP use of subscription quota; see the [official integration guide](https://docs.bigmodel.cn/cn/coding-plan/tool/others). Record that client context can differ from raw API context. Returned token usage and a client's estimated price are not independently verified subscription charges or remaining quota.

Run the complete chain: task admission, frozen setup, outline, research, section drafting, locked first draft, four reviews, evidence-based adjudication, author revision, four re-reviews, and usable final report. Preserve the first draft and failures. A review of an old version cannot approve a new one. A concrete critical finding must be checked and resolved or explicitly bounded; favorable votes and a high average cannot erase it. Unsupported model corrections must not be copied into the report.

This route does not require human reviewers. Use known-error and valid controls to check the rubric before freezing a new study, and report results explicitly as LLM-judged with an evidence-audit boundary, not human-calibrated truth. It does not enable an automatic research-quality PASS in the deterministic runner. Existing frozen experiments and their original reviewer counts remain historical records; do not rewrite them to claim this new plan was executed.

## Track B: Frozen Cross-Agent Portability

Use [`evals/cross_agent/`](../evals/cross_agent/) for the public showcase. Run three or four agents against one frozen fictional task under two matched conditions: baseline and framework. Preserve failed runs instead of repairing them.

The publication gate requires complete paired records, input hashes, matched within-agent settings, raw process streams, workspaces, blind run mapping, and at least two independent reviews per run. Until then, the only honest label is `prepared_no_runs`.

This track is useful for integration and failure analysis. It is deliberately not the primary efficacy test.

## Track C: Held-Out Real-Task Efficacy

The proposed first product-effect study uses 12 distinct, held-out, rights-cleared real research tasks sampled from the intended workload. This is a screening cohort, not a universal sample-size or statistical-power guarantee. Use two separate, excluded tasks to calibrate execution and review; freeze the main study after calibration and before its model runs.

For each task and production agent environment:

1. Run baseline and framework conditions with the same model, reasoning setting, normal tools, starting memory, context budget, timeout, and retry rule. Prevent cross-condition access to outputs or experiment-generated memory. Disable only the tested framework in the baseline; verify the treatment loads the pinned version rather than a drifting installed copy.
2. Keep the request, initial materials, target reader, and information cutoff fixed; randomize condition order within the same time block. Preserve normal web access when the real task needs it, letting each condition choose its own searches and sources. Use identical fixed sources only when the original task requires that restriction.
3. Preserve complete outputs, failures, latency, cost or token usage when exposed, and user corrections.
4. Use the fixed four-reviewer panel above, independently and blinded to condition as far as the report permits. Freeze each review before sharing opinions. Record identity/context leakage and complete a separate evidence audit of material claims and disputes. No human-review prerequisite applies to this new LLM-judged design, and no human calibration may be claimed. Missing, truncated or cross-version reviews leave the panel incomplete.
5. Score task fidelity, factual/evidence discipline, synthesis, counter-evidence, and reader usefulness separately; reader usefulness includes decision value and readable delivery. Use `not_assessed` when evidence or input is insufficient rather than treating it as zero or a clean bill of health.
6. Treat invented facts, missing primary deliverables, hidden critical limitations, and false completion as critical failures that averages cannot offset.
7. Publish every task-level pair, paired differences, descriptive uncertainty, disagreements, exclusions, and reruns. Report win, loss, tie, both-failed, and unresolved outcomes explicitly; neither both-failed nor unresolved outcomes count as framework wins. Any stopping or extension thresholds are preregistered product decision rules, not significance claims. Sequential stopping needs a corresponding statistical design before confirmatory inference.

Do not mix different models into the framework-effect estimate. Cross-model robustness is a later question; the causal contrast is framework versus baseline within the same production environment.

Compare first drafts with first drafts. If revision effects are also measured, give both conditions the same preregistered review and revision opportunities and report initial and revised results separately. Model-review scores alone support only a bounded LLM-judged comparison, not proof that the framework improves real-world decisions.

Twelve tasks in one production environment require 24 primary runs, not 12 tasks multiplied by every showcase agent. If four tasks are selected in advance for one repeat of each condition, those eight additional runs measure sensitivity and are not new independent tasks. Baseline outputs do not lose semantic-quality points for lacking framework-specific registries or receipts; apply conformance checks only where the protocol is applicable, while auditing evidence and truthful delivery in both conditions.

## Track D: Reproduction And Adoption

After the first tagged release, invite external users to reproduce one frozen case, submit a failure fixture, or contribute an adapter. Track external issues, pull requests, forks, reproducible run bundles, and repeat users. Stars are discovery signals, not validation.

## Data Rules

- Use synthetic packs for public deterministic and portability checks when factual freshness is not the target.
- Quarantine internally contradictory records; never leave them active merely to preserve case counts.
- For live-web efficacy studies, freeze task inputs and time boundaries, then preserve each condition's observed sources, access times, and failures for audit. Do not turn a normally online task into a fixed-source test for evaluator convenience.
- Keep private or licensed evidence out of public bundles unless redistribution rights are explicit.
- Separate evaluator-development data, reviewer-calibration data, and final held-out tasks.

## Release Sequence

1. Stabilize conformance schema v2 and delivery semantics.
2. Publish an initial tagged release with migration notes and exact checks.
3. After accepted corrections pass, complete the current single-author report/review lane and freeze the real-task study design before its held-out runs.
4. Run the preregistered real-task study; execute the separate frozen cross-agent showcase when its runtime environments are available, without changing its inputs. Missing external runtimes do not block the Codex-only lane or justify calling model APIs different runtimes.
5. Add optional domain packs or distribution plugins only when repeated external use demonstrates the need.
