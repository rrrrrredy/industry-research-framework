# Delivery checker: contract and observation limits

The checker is an optional offline consistency check. It is not a runtime permission hook and cannot prove that an agent invoked it. The research and writing requirements remain in [SKILL.md](../SKILL.md); this page documents the checker interface, not additional writing rules.

The default is **delivery contract 2**. The receipt container remains `schema_version: 1`; contract versions identify which checks were performed. Results include `delivery_contract_version`, `current_contract_checked`, and `semantic_verification: false`. None authenticates user consent, proves actual reading, or certifies editorial quality.

```bash
python <skill-directory>/scripts/check_delivery.py <task-directory>
```

The receipt binds the current artifact, brief, progress, source and claim records, review log, and intended delivery message. Applicable requirement and uncertainty files are also bound. Text hashes normalize CRLF and CR to LF. Finish the relevant edits before sealing; a later edit makes the old receipt stale. Do not rerun unrelated research just to create a new receipt.

Use `--delivery-message note.md` for a non-default intended message. The receipt must bind that selected filename. Artifact, receipt and intended-message paths must resolve inside the task directory.

## Requirement closure and reading records

In `state/requirements.jsonl`, `satisfied` needs a non-empty evidence string or list of strings. A requirement closed as `waived`, `out_of_scope`, or `accepted_limitation` needs a `user_decision` object with non-empty `source_turn` and `quote`. The quoted decision must concern that requirement; an original user exclusion can establish scope. A status label, the author's decision, or disclosure of a gap does not replace the user's decision.

For example, these are **synthetic record examples**, not evidence of a real approval:

```json
{"requirement_id":"R-read-1","status":"waived","user_decision":{"source_turn":"user-message-7","quote":"You may skip the inaccessible article."}}
```

For reading that the task actually requires:

```json
{"requirement_id":"R-read-2","status":"satisfied","evidence":"notes/source-2.md","reading_requirement":"full_text","required_source_ids":["S02"]}
```

The linked `data/source_registry.csv` row must occur exactly once and have `read_scope` and a non-empty `read_evidence` reference. Use `full_text`, `relevant_sections`, `abstract`, `partial`, or `not_read` to describe the actual reading. A `full_text` requirement accepts only `full_text`; `relevant_sections` accepts completed relevant-section reading or full text. The evidence reference should identify the read sections and notes or observations that support the record. HTTP 200 and a URL in the registry establish access, not reading. Optional background sources do not become mandatory full reads.

The checker compares these declared fields. It cannot detect an omitted requirement, infer reading duties from free-form prose, verify a fabricated quote, or establish comprehension from a note. The author still reconciles the records with the actual request and sources. Both the standalone checker and eval runner check requirement closure, including when the runner's optional receipt check is disabled.

## Comparing a captured reply

```bash
python <skill-directory>/scripts/check_delivery.py <task-directory> --actual-message captured-reply.md
```

The supplied capture is compared with the bound intended message, normalizing only line endings and outer whitespace. A runtime caller can retain its final-message output separately and call the checker after the run. Retain the original runtime output and document any extraction of client metadata; do not silently remove substantive differences.

The `delivery_observation` result is `not_provided`, `matched`, `mismatch`, or `unreadable`. Missing or different supplied captures fail. `not_provided` means only the intended message was checked, not that the actual user received it.

A caller-supplied file is not authenticated delivery attestation. An agent writing another copy of its intended message does not create independent capture evidence. This interface alone does not intercept or enforce the live final reply.

## Task-declared review requirements

A task may already require several review scopes. It can declare these in `progress.json` as `required_review_scopes`, a list of distinct non-empty scope names. The latest record for each declared scope must pass without open issues before terminal delivery; the global review is still required. This optional interface does not require extra reviewers or review cycles for ordinary work. A model's PASS remains a model judgment, not proof of factual or editorial quality.

The latest global review and each declared required scope also need `artifact_sha256`, the SHA-256 of the primary report they reviewed after LF newline normalization. For example, add that hash to the actual review row alongside its scope and result. A missing or malformed hash fails with `missing_review_artifact_binding`; a different current report fails with `stale_review_artifact`. The receipt separately binds the current review log. Resealing that receipt cannot make an earlier review cover edited prose. A local recheck cannot refresh the global binding, and a global PASS cannot refresh a task-required specialist binding.

Recognized progress statuses are `in_progress`, `paused`, `blocked`, and `complete`. Terminal state requires both `stage: final` and `status: complete`; neither alone is sufficient.

The standalone checker and eval runner share review and open-issue semantics. A clean latest global review covers earlier ordinary unit reviews; later blocking findings still need a clean review of the same scope or a new global review. A local PASS cannot clear another scope or a failed global review. Explicitly required scopes remain independent: a global PASS does not remove their requirements. Malformed history cannot be repaired by appending a PASS; preserve and correct the invalid record explicitly. A `routed_action` alone is a plan, not a resolution.

## Limitation disclosure is not keyword certification

`limitation_disclosure.status` distinguishes `not_applicable`, `absent`, `contradiction`, `text_covered`, and `needs_review`. An absent disclosure signal or a recognized blanket denial of existing limitations fails the mechanical check. The denial detector is bounded and heuristic; it does not recognize every possible wording.

`text_covered` means the recorded limitation text was found after punctuation/whitespace normalization, not that it is factually correct or asserted honestly. `needs_review` reports `unmatched_limitations` and a visible warning when only some limitations match, the wording is paraphrased, or the message is generic. These uncertain cases do not fail solely for using a valid paraphrase, but a mechanical PASS must not be reported as verified disclosure. `semantic_verification` is always false: a content reviewer must check meaning, coverage and material contradictions. There is no compulsory wording, extra declaration file or model/API dependency.

中文说明：两个入口现在共享问题关闭和审查历史的判断。“安排了后续动作”不等于问题解决，后来的局部阻断也不能被旧全稿PASS掩盖。限制披露会区分明显否认、未见披露信号、文字覆盖和待语义复核；只出现“限制”二字不再被表述为披露已核验。文字覆盖及机械PASS仍不证明事实正确；正常同义表达不会仅因无法精确匹配就被当成错误。

当前默认检查版本为2，交付凭证的JSON外层仍是schema 1。必做要求若改为放弃、排除或接受未完成，需要记录用户对应决定；披露“没有做完”不能自动关闭要求。必读材料需分清要求读到哪里、实际读到哪里；没有要求全文阅读的辅助资料不因此被强制全文阅读。最新全稿审阅及任务明确要求的专项审阅都要绑定实际审阅稿件的哈希，重新生成交付凭证不能替旧审阅补看新稿。这些检查验证记录的一致性，不认证批准真实性、实际阅读或文章质量。

## Historical records

Use `--contract-version 1` only to inspect unchanged historical records that predate these fields. The result and CLI output explicitly label legacy checks and set `current_contract_checked: false`. The eval runner has the matching `--delivery-contract-version 1` option. Legacy success is not acceptance under the current contract. Do not add invented approval quotes or review hashes to old runs to make them pass; perform and record the missing work for a new delivery instead.

旧记录可以用版本1做标明边界的历史诊断，不代表满足当前交付条件。不要给冻结实验补写当时并不存在的批准或审阅。新交付使用默认版本2。

## Regression coverage

`python scripts/check_delivery_contract.py` reseals unrelated hashes so a stale receipt cannot mask the target defect. It includes known-good controls, custom message binding, captured-message differences, declared review scopes, bounded review-event permutations and the terminal-state truth table. These checks do not establish universal natural-language completion detection or research quality.

`python scripts/check_evaluator_contract.py` adds cross-entry review recovery, later local blockers, malformed/invalid-UTF-8 history, routed-only issues, limitation-denial and partial-coverage controls, and distinct versus repeated English/Chinese text. All diagnostic fixture changes are isolated and resealed; frozen research inputs and historical reports are not rewritten.

Current-contract tests add unauthorized/authorized requirement closure, declared full/partial reading, unchanged/currently reviewed report controls, and stale global/specialist reviews. The old conformance and regression fixture runners explicitly use version 1 to preserve historical comparisons; their original inputs and hashes stay unchanged. New positive controls are constructed only in isolated test copies and are not backfilled research records.
