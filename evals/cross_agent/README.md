# Cross-Agent Frozen Comparison

This directory defines a public, reproducible comparison across three or four agent runtimes. It is a portability and failure-analysis track, not evidence that the framework improves research in general.

Current status: **prepared, no model runs published**. See [`STATUS.md`](./STATUS.md). Do not cite this directory as a result until the publication gate passes.

## Design

Each participating agent runs the same fictional, no-network research task twice:

1. `baseline`: the agent receives the frozen task and source pack, but not this framework.
2. `framework`: the agent receives the same task and sources plus the frozen `SKILL.md` and reference files.

Keep the runtime, model, reasoning setting, context budget, tool permissions, timeout, and hardware constant within an agent's pair. Differences between different agents are descriptive; the within-agent baseline/framework pair is the relevant intervention contrast.

The source pack is entirely synthetic. This avoids privacy, licensing, freshness, and unverifiable-company-fact problems. It does not make the task representative of all industry research.

## Freeze Boundary

[`manifest.json`](./manifest.json) lists every frozen task, source, prompt, protocol, and review file. [`freeze.lock.json`](./freeze.lock.json) binds them by SHA-256. Validate the freeze with:

```bash
python scripts/check_cross_agent_protocol.py
```

Changing a frozen input creates a new protocol version and requires a new lock. Never silently update an input after runs begin.

## Execution Record

Store each run at `evals/cross_agent/runs/<agent_id>/<condition>/`. A complete attempt preserves:

- `run.json`: unique run id; runtime/model/version; reasoning, tool, and timeout settings; timestamps; exit code and attempt status; prompt and freeze-lock hashes; budgets when exposed; and an explicit redaction list;
- `prompt.md`: the exact user-visible prompt sent to the runtime;
- `stdout.txt` and `stderr.txt`: raw process streams, with secrets redacted but no substantive omissions;
- `workspace/`: every artifact produced, including failures and partial work.

Do not repair a failed run in place. Record the failure, then start a new attempt with a distinct run id and disclose the rerun rule.

## Review And Publication Gate

Randomize run ids before review. `reviews/blinding-map.json` uses a `runs` array whose rows contain exactly one `run_id` and one unique `blind_run_id`; reveal this map only after reviews are locked. At least two reviewers score each output independently with [`review_rubric.md`](./review_rubric.md) without seeing agent or condition. Critical failures cannot be offset by a high average score.

A public comparative claim requires all of the following:

- at least three agents, each with one baseline and one framework attempt under matched settings;
- exact frozen-input hashes and complete raw run records;
- at least two blinded reviews per run plus an adjudication note for material disagreement;
- deterministic conformance reported separately from semantic research quality;
- failures, missing artifacts, retries, cost, latency, and unavailable metrics disclosed;
- a summary that says this is a one-task portability showcase, not a general efficacy estimate.

Use `python scripts/check_cross_agent_protocol.py --require-publication` before publishing a comparative summary.

## Relation To A Real Efficacy Evaluation

One frozen synthetic task can reveal integration failures, protocol adherence differences, and obvious quality regressions. It cannot estimate average treatment effect. A defensible efficacy claim needs multiple held-out real tasks, matched baseline/framework runs within the same production runtime, preregistered stopping rules, calibrated reviewers, and critical-failure reporting. Keep that study separate from this public showcase.
