# Contributing

Contributions are welcome when they make the protocol easier to follow, harder to game, or more credible in real research work without turning the repository into a heavy orchestration product.

## Authority And Scope

- `SKILL.md` is the sole normative protocol source.
- The public page may embed `SKILL.md`, but `python scripts/check_docs_sync.py` must prove exact synchronization.
- README files, agent adapters, plugins, and examples are distribution or explanation layers. They must not introduce competing protocol rules.
- Mechanical conformance, semantic research quality, runtime wiring, and general framework efficacy are separate claims and must be reported separately.

## Before Opening A Change

1. State the concrete failure, adoption problem, or evidence gap.
2. Prefer the smallest change that affects an observable result.
3. Add a known-bad regression fixture for a deterministic failure.
4. Add or preserve a known-good control so the checker cannot improve by rejecting everything.
5. Use synthetic or rights-cleared data. Sanitized internal summaries are workflow seeds, not public factual authority.
6. Do not update frozen cross-agent inputs after runs begin; create a new protocol version and lock instead.

## Required Checks

```bash
python scripts/check_docs_sync.py
python scripts/run_dsh_evals.py validate
python scripts/check_eval_source_integrity.py
python scripts/check_cross_agent_protocol.py
python scripts/check_regression_fixtures.py
python scripts/check_conformance_fixtures.py
```

If `SKILL.md` changed, refresh the public copy first:

```bash
python scripts/check_docs_sync.py --write
```

Changes to `scripts/run_evals.py` must preserve result schema semantics: `conformance_status`, `conformance_score`, and `conformance_flags` are mechanical; `research_quality_status` cannot become a quality verdict without a separately designed and calibrated evaluation.

## Pull Request Evidence

Include:

- the failure or use case addressed;
- files and contract fields changed;
- exact checks run and their outcomes;
- one negative example that is newly caught;
- one positive control that still passes;
- limitations and any intentionally deferred work.

Do not claim improved report quality from a green deterministic test alone. Real efficacy claims require held-out tasks, matched baseline/framework runs, calibrated independent review, and disclosure of failures, retries, cost, and latency.
