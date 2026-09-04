# Changelog

All notable repository changes are recorded here. Until the first tagged release, entries remain under `Unreleased` and must not be described as a published version.

## Unreleased

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
