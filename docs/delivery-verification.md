# Delivery checker: contract and observation limits

The checker is an optional offline consistency check. It is not a runtime permission hook and cannot prove that an agent invoked it. The research and writing requirements remain in [SKILL.md](../SKILL.md); this page documents the checker interface, not additional writing rules.

```bash
python <skill-directory>/scripts/check_delivery.py <task-directory>
```

The receipt binds the current artifact, brief, progress, source and claim records, review log, and intended delivery message. Applicable requirement and uncertainty files are also bound. Text hashes normalize CRLF and CR to LF. Finish the relevant edits before sealing; a later edit makes the old receipt stale. Do not rerun unrelated research just to create a new receipt.

Use `--delivery-message note.md` for a non-default intended message. The receipt must bind that selected filename. Artifact, receipt and intended-message paths must resolve inside the task directory.

## Comparing a captured reply

```bash
python <skill-directory>/scripts/check_delivery.py <task-directory> --actual-message captured-reply.md
```

The supplied capture is compared with the bound intended message, normalizing only line endings and outer whitespace. A runtime caller can retain its final-message output separately and call the checker after the run. Retain the original runtime output and document any extraction of client metadata; do not silently remove substantive differences.

The `delivery_observation` result is `not_provided`, `matched`, `mismatch`, or `unreadable`. Missing or different supplied captures fail. `not_provided` means only the intended message was checked, not that the actual user received it.

A caller-supplied file is not authenticated delivery attestation. An agent writing another copy of its intended message does not create independent capture evidence. This interface alone does not intercept or enforce the live final reply.

## Task-declared review requirements

A task may already require several review scopes. It can declare these in `progress.json` as `required_review_scopes`, a list of distinct non-empty scope names. The latest record for each declared scope must pass without open issues before terminal delivery; the global review is still required. This optional interface does not require extra reviewers or review cycles for ordinary work. A model's PASS remains a model judgment, not proof of factual or editorial quality.

Recognized progress statuses are `in_progress`, `paused`, `blocked`, and `complete`. Terminal state requires both `stage: final` and `status: complete`; neither alone is sufficient.

## Regression coverage

`python scripts/check_delivery_contract.py` reseals unrelated hashes so a stale receipt cannot mask the target defect. It includes known-good controls, custom message binding, captured-message differences, declared review scopes, bounded review-event permutations and the terminal-state truth table. These checks do not establish universal natural-language completion detection or research quality.
