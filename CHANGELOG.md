# Changelog

Released changes are grouped by tag. `Unreleased` describes work not yet included in a published version.

## Unreleased

Development-only semantic diagnostics and clearer integration guidance. These changes do not modify the core research method or establish general efficacy. The v0.1.4 prerelease was withdrawn; v0.1.3 remains the latest available prerelease.

### Changed

- Consolidate duplicated installation lists into three capability-based choices in both READMEs. Add a bilingual adapter index that separates instructions, runtime abilities, and research evidence; disclose the recovery and delivery-check limits of conversation-only use without changing the core method or claiming cross-runtime validation.

### Fixed

- Fail source-integrity checks when the case or source-pack collection is missing or empty, rather than reporting coverage without checking any cases. Reject missing, empty, malformed or duplicate case references, duplicate quarantine IDs and policy entries for missing packs. Report the actual case count; preserve valid workflow controls and the factual-use prohibition. No frozen sources, reports or research-method rules change.

### Added

- Publish eight label-masked semantic-review calls, including a shared missed control defect, severity disagreements and one fresh-context/order-sensitive judgment. Retain and re-review two case corrections without overwriting original inputs; the current catalog applies the corrections while keeping twenty underlying cases. Model agreement is not accuracy or human calibration.
- Add parent-bound case revisions and offline review-bundle checks that recompute observation counts and disagreements from actual model replies, not just document hashes.
- Expand the synthetic semantic diagnostic catalog from six to twenty bad/control pairs. Include justified positive judgments so caution is not mistaken for quality; retain the original six and all historical results. The new labels are author-proposed, uncalibrated development material, not held-out efficacy evidence.
- Validate diagnostic data structure and claim boundaries in CI, with negative cases for missing evidence or controls, duplicate identifiers and invalid types. Passing these checks does not establish that the semantic labels are correct.

## [v0.1.3](https://github.com/rrrrrredy/industry-research-framework/releases/tag/v0.1.3) — 2026-09-08

Checker-consistency prerelease. These fixes do not change the core research method or establish research-quality efficacy.

### Fixed

- Share current review and open-issue semantics between delivery checks and evals. A later clean global review can recover from an earlier failure; later local blockers still invalidate delivery, and a local PASS cannot erase another scope. Required scopes and malformed history remain blocking. A routed action alone never closes an issue.
- Preserve English words in repeated-line detection instead of collapsing distinct paragraphs into one placeholder. Keep genuine repetition and citation-variation controls in both languages.
- Reject recognized blanket denials of accepted limitations. Report unmatched or partial disclosure as requiring semantic review, not as verified by a generic keyword; literal coverage is explicitly not semantic certification.
- Add 24 cross-entry regressions to CI, including invalid UTF-8 even when the optional receipt check is disabled. Preserve existing tests, core protocol text, frozen inputs and historical outputs.
- Label the public comparison as illustrative design goals in English and Chinese, and link separately to actual reports and limitations instead of implying measured before/after improvement.
- Explain the framework's purpose in plain language across both READMEs and the public introduction. Replace the ambiguous runtime-agnostic ResearchOps label without changing the core research method or execution rules.

## [v0.1.2](https://github.com/rrrrrredy/industry-research-framework/releases/tag/v0.1.2) — 2026-09-07

Delivery-checker prerelease. The core protocol and frozen research inputs are unchanged.

### Fixed

- Recognize explicit completion claims that name the selected primary report through a Markdown link or inline filename. Previously, a reply such as `已完成 [report.md](report.md)` could pass the checker while progress remained nonterminal. Keep bare links, unrelated artifacts, negations and explicitly partial work as non-completion controls.
- Add six delivery-contract tests derived from a real Codex reply and bounded wording variants. This closes a known lexical gap; natural-language claim detection is still heuristic, not a semantic guarantee. The core Skill, references and frozen experimental inputs are unchanged.

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
