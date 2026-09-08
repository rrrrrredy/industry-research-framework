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

The standalone checker and eval runner share review and open-issue semantics. A clean latest global review covers earlier ordinary unit reviews; later blocking findings still need a clean review of the same scope or a new global review. A local PASS cannot clear another scope or a failed global review. Explicitly required scopes remain independent: a global PASS does not remove their requirements. Malformed history cannot be repaired by appending a PASS; preserve and correct the invalid record explicitly. A `routed_action` alone is a plan, not a resolution.

## Limitation disclosure is not keyword certification

`limitation_disclosure.status` distinguishes `not_applicable`, `absent`, `contradiction`, `text_covered`, and `needs_review`. An absent disclosure signal or a recognized blanket denial of existing limitations fails the mechanical check. The denial detector is bounded and heuristic; it does not recognize every possible wording.

`text_covered` means the recorded limitation text was found after punctuation/whitespace normalization, not that it is factually correct or asserted honestly. `needs_review` reports `unmatched_limitations` and a visible warning when only some limitations match, the wording is paraphrased, or the message is generic. These uncertain cases do not fail solely for using a valid paraphrase, but a mechanical PASS must not be reported as verified disclosure. `semantic_verification` is always false: a content reviewer must check meaning, coverage and material contradictions. There is no compulsory wording, extra declaration file or model/API dependency.

中文说明：两个入口现在共享问题关闭和审查历史的判断。“安排了后续动作”不等于问题解决，后来的局部阻断也不能被旧全稿PASS掩盖。限制披露会区分明显否认、未见披露信号、文字覆盖和待语义复核；只出现“限制”二字不再被表述为披露已核验。文字覆盖及机械PASS仍不证明事实正确；正常同义表达不会仅因无法精确匹配就被当成错误。

## Regression coverage

`python scripts/check_delivery_contract.py` reseals unrelated hashes so a stale receipt cannot mask the target defect. It includes known-good controls, custom message binding, captured-message differences, declared review scopes, bounded review-event permutations and the terminal-state truth table. These checks do not establish universal natural-language completion detection or research quality.

`python scripts/check_evaluator_contract.py` adds cross-entry review recovery, later local blockers, malformed/invalid-UTF-8 history, routed-only issues, limitation-denial and partial-coverage controls, and distinct versus repeated English/Chinese text. All diagnostic fixture changes are isolated and resealed; frozen research inputs and historical reports are not rewritten.
