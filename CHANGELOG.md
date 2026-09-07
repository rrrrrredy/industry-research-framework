# Changelog

Released changes are grouped by tag. `Unreleased` describes work not yet included in a published version.

## Unreleased

## [v0.1.1](https://github.com/rrrrrredy/industry-research-framework/releases/tag/v0.1.1) — 2026-09-07

Engineering and evidence prerelease. The original SKILL.md and all eight core references are unchanged. Ten offline suites pass; retained development diagnostics are not a held-out efficacy result or three-runtime comparison.

### Changed

- Remove redundant online-reading sections from both READMEs, retain links near the introduction, and make integration guidance platform-neutral; move synchronization and packaging policy to maintenance documentation.
- Reject unknown progress statuses and delivery paths outside the task directory.
- Bind the selected delivery-message filename instead of always requiring the default filename.
- Reject invalid UTF-8 delivery inputs instead of silently replacing bytes or crashing during JSON reads.
- Keep an issue open when it only assigns a routed action; planning a follow-up is not resolution.
- Exclude unresolved numeric-scope claims and a wrong XGBoost attribution from active legacy sources; retain exact originals and audit reasons, and prevent regeneration from restoring them.
- Narrow unsupported assertions in the historical AI Agent editorial example; explicitly distinguish example labels from verified factual or quality results.

### Added

- Optional comparison with a caller-supplied actual reply capture; an absent capture is explicitly `not_provided`.
- Optional verification of task-declared review scopes in addition to the global review.
- Isolated delivery-contract regressions and bounded review-order/state-transition checks.
- Evaluator schema v2 migration guidance and explicit delivery-checker observation limits.
- Workflow-only source-use policy, provenance/rights limitations, and positive/negative regeneration controls.
- Six synthetic semantic bad/control pairs for diagnostic review, not automatic quality scores or held-out evidence.
- Actual calibration report exports, two editorial repairs, retained failed reviews and a frozen three-model text diagnostic with its incomplete response; no efficacy or three-runtime claim.
- Offline public-bundle integrity checks and disclosure of heuristic thresholds, reviewer context exposure and partial stage observability.
- Read-only installed-payload comparison against a selected Git commit and safe-update guidance; local variants are never overwritten.

## [v0.1.0](https://github.com/rrrrrredy/industry-research-framework/releases/tag/v0.1.0) — 2026-09-04

First public prerelease. Mechanical checks do not establish research quality or general framework efficacy.

### Changed

- Split English and Simplified Chinese README files while keeping one repository and one authoritative `SKILL.md`.
- Renamed evaluator output to schema v2 fields that distinguish mechanical conformance from semantic research quality.
- Made `review` non-zero by default in the evaluator; exploratory runs must opt in with `--allow-review`.
- Made false completion, malformed review logs, and configured source-instruction violations blocking failures rather than near-passing review results.
- Made terminal state bidirectional: `stage: final` if and only if `status: complete`.
- Made the latest global review authoritative and fail-closed on malformed rows, later failures, or open issues.
- Expanded terminal receipt hashes to bind progress, review log, and intended delivery message as well as the report and backstage evidence.
- Reframed the public page and gallery around an agent-agnostic ResearchOps protocol and explicit conformance limits.
- Marked the original July 2026 launch MP4 and slides as historical assets instead of silently presenting them as current.

### Added

- Six regression fixtures for sentence-level keyword stuffing, late review failure, asymmetric terminal state, completion paraphrases, malformed review logs, and PASS records with open issues.
- Source-pack quarantine output and an integrity checker for active/quarantined records and case references.
- A frozen, no-result-yet cross-agent baseline/framework protocol with input hashes, blind-review rules, and a publication gate requiring at least three complete agent pairs.
- A four-track evaluation roadmap separating deterministic conformance, cross-agent portability, held-out real-task efficacy, and external adoption.
- A regenerated agent gallery image that includes DeepSeek Harness.

### Verification

- `python scripts/check_docs_sync.py`
- `python scripts/run_dsh_evals.py validate`
- `python scripts/check_eval_source_integrity.py`
- `python scripts/check_cross_agent_protocol.py`
- `python scripts/check_regression_fixtures.py`
- `python scripts/check_conformance_fixtures.py`

The cross-agent publication gate is expected to fail until real paired runs and blind reviews exist.
