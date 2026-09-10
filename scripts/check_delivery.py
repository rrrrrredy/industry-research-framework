#!/usr/bin/env python3
"""Validate that a user-visible delivery claim matches current research state."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any


CANONICAL_STAGES = {"brief", "collect", "analyze", "draft", "review", "revise", "final"}
PROGRESS_STATUSES = {"in_progress", "paused", "blocked", "complete"}
OPEN_ISSUE_KEYS = {
    "open_issues",
    "unresolved_issues",
    "pending_issues",
    "remaining_issues",
    "blockers",
    "explicitly_not_completed",
}
CLOSED_ISSUE_TERMS = {"closed", "resolved", "handled", "accepted_limitation", "waived"}
OPEN_ISSUE_TERMS = {
    "open", "unresolved", "pending", "blocking", "incomplete", "not_completed",
    "in_progress", "needs_revision", "fail", "failed", "blocked", "blocking_issue",
}
RESOLVED_REQUIREMENT_STATUSES = {"satisfied", "accepted_limitation", "waived", "out_of_scope"}
DELIVERY_CONTRACT_VERSION = 2
REQUIREMENT_DECISION_STATUSES = {"accepted_limitation", "waived", "out_of_scope"}
READING_REQUIREMENTS = {"full_text", "relevant_sections"}

COMPLETION_PATTERNS = [
    r"(?:终稿|最终稿|完整稿)(?:已经|已|现已)?(?:完成|形成|交付|可交付)",
    r"(?:任务|研究|报告|成稿)(?:已经|已|现已)?(?:完成|交付)",
    r"(?:都|全都|全部(?:内容)?)(?:已经|已|现已)?(?:搞定|完成|就绪)",
    r"(?:任务|研究|报告|成稿|终稿|最终稿|完整稿)(?:已经|已|现已)?(?:写好|做好|搞定|就绪)",
    r"(?:已经|已|现已|全部|正式)(?:完成|交付).{0,6}(?:任务|研究|报告|终稿|最终稿|完整稿)",
    r"\b(?:final report|final delivery|final answer) (?:is )?(?:complete|completed|ready|delivered)\b",
    r"\b(?:task|research|report|work) (?:is |has been )?(?:complete|completed|done|delivered)\b",
    r"\b(?:everything|all work|all content) (?:is |has been )?(?:done|complete|completed|ready|all set)\b",
    r"\b(?:ready to (?:publish|ship|deliver|submit)|good to go)\b",
]
NEGATED_COMPLETION_PATTERNS = [
    r"(?:尚|还|仍|并)?未.{0,5}(?:完成|交付|形成)",
    r"(?:没有|并没有).{0,5}(?:完成|交付|形成)",
    r"(?:不是|并非|非|不构成|不能视为).{0,5}(?:终稿|最终稿|完整稿|完成|交付)",
    r"(?:还不能|不能|无法|不可以|不可).{0,5}(?:发布|提交|交付)",
    r"(?:阶段稿|草稿|中间稿)",
    r"\b(?:not final|not complete|not completed|not ready|not ready to publish|unfinished|incomplete|draft|work in progress)\b",
]
LIMITATION_DISCLOSURE_TERMS = [
    "已知限制",
    "限制",
    "不确定",
    "未能",
    "无法确认",
    "公开信息不足",
    "accepted limitation",
    "known limitation",
    "limitation",
]
REQUIRED_HASH_INPUTS = [
    "state/task_spec.md",
    "state/progress.json",
    "data/source_registry.csv",
    "data/claims_registry.csv",
    "logs/review.jsonl",
    "delivery_message.md",
]
OPTIONAL_HASH_INPUTS = [
    "state/requirements.jsonl",
    "data/uncertainty_registry.csv",
]
CANONICAL_TEXT_HASH_SUFFIXES = {".csv", ".html", ".json", ".jsonl", ".md", ".py", ".txt", ".yaml", ".yml"}
GLOBAL_REVIEW_SCOPES = {
    "global_final_delivery",
    "full_report",
    "full report",
    "full_draft",
    "full draft",
    "global",
    "全文",
    "全稿",
}
PASS_REVIEW_TERMS = {"pass", "passed", "complete", "approved"}
REVIEW_STATUS_KEYS = {"result", "status", "decision", "verdict", "finding_type", "outcome"}
FAIL_REVIEW_TERMS = {"fail", "failed", "needs_revision", "unresolved", "open", "blocking_issue", "blocked"}
REVIEW_ISSUE_KEYS = {
    "issues",
    "findings",
    "open_issues",
    "unresolved_issues",
    "blockers",
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def read_json_or_none(path: Path) -> Any | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeError):
        return None


def inspect_jsonl(path: Path, label: str) -> tuple[list[dict[str, Any]], list[str]]:
    try:
        content = read_text(path)
    except (OSError, UnicodeError):
        return [], [f"{label} log is unreadable or is not valid UTF-8."]
    return inspect_jsonl_text(content, label)


def inspect_jsonl_text(content: str, label: str) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    findings: list[str] = []
    for line_number, line in enumerate(content.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            findings.append(f"{label} row {line_number} is not valid JSON.")
            continue
        if isinstance(value, dict):
            rows.append(value)
        else:
            findings.append(f"{label} row {line_number} is not an object.")
    return rows, findings


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows, _ = inspect_jsonl(path, "JSONL")
    return rows


def nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def has_evidence(value: Any) -> bool:
    return nonempty_text(value) or (
        isinstance(value, list) and bool(value) and all(nonempty_text(item) for item in value)
    )


def inspect_required_reading(row: dict[str, Any], registry_path: Path) -> list[str]:
    """Check declared reading records, not actual comprehension or source truth."""
    if "reading_requirement" not in row and "required_source_ids" not in row:
        return []
    required = row.get("reading_requirement")
    source_ids = row.get("required_source_ids")
    if not isinstance(required, str) or required not in READING_REQUIREMENTS:
        return ["reading_requirement must be full_text or relevant_sections."]
    if not (isinstance(source_ids, list) and source_ids
            and all(nonempty_text(value) for value in source_ids)
            and len(set(source_ids)) == len(source_ids)):
        return ["required_source_ids must be a non-empty list of distinct source ids."]
    try:
        with registry_path.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream, strict=True))
    except (OSError, UnicodeError, csv.Error):
        return ["Required reading has no readable UTF-8 source registry."]
    findings = []
    for source_id in source_ids:
        matches = [source for source in rows if source.get("source_id") == source_id]
        if len(matches) != 1:
            findings.append(f"Required source {source_id} must have exactly one registry row.")
            continue
        source = matches[0]
        allowed = {"full_text"} if required == "full_text" else {"full_text", "relevant_sections"}
        if source.get("read_scope") not in allowed:
            findings.append(f"Required source {source_id} has not met its {required} reading requirement.")
        if not nonempty_text(source.get("read_evidence")):
            findings.append(f"Required source {source_id} has no reading evidence reference.")
    return findings


def inspect_requirements(path: Path, contract_version: int = DELIVERY_CONTRACT_VERSION) -> tuple[list[str], list[str]]:
    """Return terminal-blocking requirement findings and accepted limitations."""

    findings: list[str] = []
    accepted_limitations: list[str] = []
    if not path.exists():
        return findings, accepted_limitations

    try:
        content = read_text(path)
    except (OSError, UnicodeError):
        return ["Requirements are unreadable or are not valid UTF-8."], []
    for line_number, line in enumerate(content.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            findings.append(f"Requirement row {line_number} is not valid JSON.")
            continue
        if not isinstance(row, dict):
            findings.append(f"Requirement row {line_number} is not an object.")
            continue

        requirement_id = str(row.get("requirement_id") or row.get("id") or "").strip()
        status = str(row.get("status", "")).strip().lower()
        label = requirement_id or f"row {line_number}"
        if not requirement_id:
            findings.append(f"Requirement row {line_number} has no stable id.")
        if status not in RESOLVED_REQUIREMENT_STATUSES:
            findings.append(
                f"Requirement {label} is not terminally resolved (status: {status or '<missing>'})."
            )
        if contract_version == 2 and status in RESOLVED_REQUIREMENT_STATUSES:
            if status in REQUIREMENT_DECISION_STATUSES:
                decision = row.get("user_decision")
                if not (isinstance(decision, dict)
                        and nonempty_text(decision.get("source_turn"))
                        and nonempty_text(decision.get("quote"))):
                    findings.append(
                        f"Requirement {label} needs a specific user_decision source_turn and quote "
                        f"before it can be {status}; disclosure alone is not permission."
                    )
            else:
                if not has_evidence(row.get("evidence")):
                    findings.append(f"Requirement {label} is satisfied without evidence.")
                findings.extend(
                    f"Requirement {label}: {finding}" for finding in inspect_required_reading(
                        row, path.parent.parent / "data" / "source_registry.csv"
                    )
                )
        if status == "accepted_limitation":
            limitation = str(
                row.get("summary") or row.get("description") or row.get("evidence") or label
            ).strip()
            accepted_limitations.append(limitation)
    return findings, accepted_limitations


def claims_completion(message: str, artifact: str = "final.md") -> bool:
    """Return True only for an affirmative user-visible completion claim."""

    scrubbed = message.lower()
    for pattern in NEGATED_COMPLETION_PATTERNS:
        scrubbed = re.sub(pattern, " ", scrubbed, flags=re.IGNORECASE)
    if any(re.search(pattern, scrubbed, flags=re.IGNORECASE) for pattern in COMPLETION_PATTERNS):
        return True

    # Runtime replies often name the primary file instead of saying "the report".
    # Only its visible filename counts; unrelated links and link targets do not.
    name = re.escape(Path(artifact.replace("\\", "/")).name)
    if not name:
        return False
    reference = rf"(?<!!)\[\s*`?{name}`?\s*\]\([^\n)]+\)|`{name}`"
    linked = re.sub(reference, " irf_primary_artifact ", message.lower(), flags=re.IGNORECASE)
    linked = re.sub(
        r"(?:\b(?:draft|outline|chapter|section)\b|阶段稿|草稿|中间稿|提纲)\s*irf_primary_artifact",
        " partial_artifact ", linked, flags=re.IGNORECASE,
    )
    # Keep partial-work nouns in place here, so "completed a draft of file"
    # cannot become "completed file" by deleting its qualification.
    for pattern in NEGATED_COMPLETION_PATTERNS[:4]:
        linked = re.sub(pattern, " ", linked, flags=re.IGNORECASE)
    linked = re.sub(
        r"\b(?:not(?: yet)?|never)\s+(?:complete|completed|done|finished|delivered)\b",
        " ", linked, flags=re.IGNORECASE,
    )
    patterns = (
        r"(?:已经|现已|已)\s*(?:完成|交付|写好|做好)\s*(?:了\s*)?irf_primary_artifact\b(?!\s*(?:的|中|['’]s\b))",
        r"\birf_primary_artifact\s*(?:已经|现已|已)\s*(?:完成|交付|写好|做好)",
        r"\b(?:completed|finished|delivered)\s+(?:the\s+)?irf_primary_artifact\b(?!\s*(?:的|中|['’]s\b))",
        r"\birf_primary_artifact\s+(?:(?:is|has been)\s+)?(?:complete|completed|done|delivered)\b",
    )
    return any(re.search(pattern, linked, flags=re.IGNORECASE) for pattern in patterns)


def issue_is_open(issue: Any) -> bool:
    if issue in (None, "", [], {}):
        return False
    if isinstance(issue, str):
        return True
    if not isinstance(issue, dict):
        return bool(issue)

    status = str(issue.get("status", "")).strip().lower()
    if status in CLOSED_ISSUE_TERMS:
        return False
    if status in OPEN_ISSUE_TERMS:
        return True
    if any(issue.get(key) for key in ("resolution", "handling", "accepted_as_limitation")):
        return False
    return True


def collect_open_issues(data: Any) -> list[Any]:
    if not isinstance(data, dict):
        return []
    issues: list[Any] = []
    for key in OPEN_ISSUE_KEYS:
        value = data.get(key)
        if isinstance(value, list):
            issues.extend(item for item in value if issue_is_open(item))
        elif issue_is_open(value):
            issues.append(value)
    return issues


def collect_accepted_limitations(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return []
    value = data.get("accepted_limitations", [])
    if isinstance(value, str):
        return [value] if value.strip() else []
    if not isinstance(value, list):
        return []
    limitations: list[str] = []
    for item in value:
        if isinstance(item, str) and item.strip():
            limitations.append(item.strip())
        elif isinstance(item, dict):
            text = str(item.get("description") or item.get("limitation") or item.get("issue") or "").strip()
            if text:
                limitations.append(text)
    return limitations


def sha256_file(path: Path) -> str:
    """Hash binary files byte-for-byte and text files with canonical LF newlines."""

    digest = hashlib.sha256()
    canonical_text = path.suffix.lower() in CANONICAL_TEXT_HASH_SUFFIXES
    pending_cr = b""
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            if not canonical_text:
                digest.update(chunk)
                continue
            chunk = pending_cr + chunk
            pending_cr = b""
            if chunk.endswith(b"\r"):
                pending_cr = b"\r"
                chunk = chunk[:-1]
            digest.update(chunk.replace(b"\r\n", b"\n").replace(b"\r", b"\n"))
    if pending_cr:
        digest.update(b"\n")
    return digest.hexdigest()


def resolve_inside(root: Path, relative_path: str) -> Path | None:
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def review_row_has_open_issues(row: dict[str, Any]) -> bool:
    for key in REVIEW_ISSUE_KEYS:
        value = row.get(key)
        if isinstance(value, list) and any(issue_is_open(issue) for issue in value):
            return True
        if not isinstance(value, list) and issue_is_open(value):
            return True
    return False


def latest_global_review_passes(rows: list[dict[str, Any]]) -> bool:
    return any(scope_key(str(row.get("scope", ""))) == "__global__" for row in rows) and not review_has_unresolved_findings(rows)


def review_row_is_blocking(row: dict[str, Any]) -> bool:
    return review_row_has_open_issues(row) or any(
        re.search(rf"\b{re.escape(term)}\b", str(row.get(key, "")), flags=re.IGNORECASE)
        for key in REVIEW_STATUS_KEYS for term in FAIL_REVIEW_TERMS
    )


def review_has_unresolved_findings(rows: list[dict[str, Any]]) -> bool:
    """A clean global review covers prior ordinary reviews, not later blockers.

    Later local findings need a clean review of the same scope or a new global
    review. Task-declared required scopes remain independently checked by the
    delivery contract; this helper does not erase them or require new artifacts.
    """
    global_indices = [i for i, row in enumerate(rows)
                      if scope_key(str(row.get("scope", ""))) == "__global__"]
    start = 0
    if global_indices:
        latest = global_indices[-1]
        if not review_passes(rows[latest]):
            return True
        start = latest + 1
    pending: set[str] = set()
    for row in rows[start:]:
        scope = scope_key(str(row.get("scope") or row.get("review_type") or "__unspecified__"))
        if review_row_is_blocking(row):
            pending.add(scope)
        elif review_passes(row):
            pending.discard(scope)
    return bool(pending)


def review_passes(row: dict[str, Any]) -> bool:
    result = str(
        row.get("result")
        or row.get("status")
        or row.get("decision")
        or row.get("verdict")
        or ""
    ).strip().lower()
    return result in PASS_REVIEW_TERMS and not review_row_is_blocking(row)


def scope_key(value: str) -> str:
    normalized = value.strip().lower()
    return "__global__" if normalized in GLOBAL_REVIEW_SCOPES else normalized


def review_has_global_pass(review_path: Path) -> bool:
    rows, findings = inspect_jsonl(review_path, "Review")
    return not findings and latest_global_review_passes(rows)


def assess_limitation_disclosure(message: str, limitations: list[str]) -> dict[str, Any]:
    """Observe literal coverage and known contradictions, never certify meaning.

    Unmatched paraphrases require review; they are not automatically false. This
    does not add a compulsory wording, declaration file or model/API dependency.
    """
    normalize = lambda value: re.sub(r"[\W_]+", "", value.casefold())
    normalized_message = normalize(message)
    unmatched = [value for value in limitations
                 if not normalize(value) or normalize(value) not in normalized_message]
    scrubbed = re.sub(
        r"(?:并非|并不是|不是|不能说|不应说|不得宣称)\s*(?:没有|不存在|无)(?:任何|已知)?(?:限制|局限|不确定性)",
        "", message, flags=re.IGNORECASE,
    )
    scrubbed = re.sub(
        r"\bnot\s+(?:without|free\s+of)\s+(?:any\s+|known\s+)?(?:limitations?|uncertainties)\b",
        "", scrubbed, flags=re.IGNORECASE,
    )
    denial = any(re.search(pattern, scrubbed, flags=re.IGNORECASE) for pattern in (
        r"(?:没有|不存在|无)(?:任何|已知|什么)?(?:限制|局限|不确定性)",
        r"\b(?:no|without)\s+(?:any\s+|known\s+)?(?:limitations?|uncertainties)\b",
        r"\bfree\s+of\s+(?:any\s+|known\s+)?(?:limitations?|uncertainties)\b",
    ))
    if not limitations:
        status = "not_applicable"
    elif denial:
        status = "contradiction"
    elif not unmatched:
        status = "text_covered"
    elif len(unmatched) == len(limitations) and not any(
        term.casefold() in message.casefold() for term in LIMITATION_DISCLOSURE_TERMS
    ):
        status = "absent"
    else:
        status = "needs_review"
    return {"status": status, "unmatched_limitations": unmatched,
            "semantic_verification": False}


def evaluate_delivery(
    project_root: Path,
    artifact: str = "final.md",
    delivery_message: str = "delivery_message.md",
    receipt: str = "state/final_delivery.json",
    actual_message: Path | None = None,
    contract_version: int = DELIVERY_CONTRACT_VERSION,
) -> dict[str, Any]:
    root = project_root.resolve()
    flags: list[str] = []
    findings: list[str] = []

    def add(flag: str, finding: str) -> None:
        if flag not in flags:
            flags.append(flag)
            findings.append(finding)
        else:
            index = flags.index(flag)
            if finding not in findings[index].split("\n"):
                findings[index] += "\n" + finding

    if type(contract_version) is not int or contract_version not in {1, 2}:
        add("invalid_delivery_contract_version", "Delivery contract version must be 1 or 2.")

    progress_path = root / "state" / "progress.json"
    progress = read_json_or_none(progress_path)
    if not isinstance(progress, dict):
        progress = {}

    stage = str(progress.get("stage", "")).strip().lower()
    status = str(progress.get("status", "")).strip().lower()
    if stage not in CANONICAL_STAGES:
        add("invalid_progress_stage", f"Progress stage is not canonical: {stage or '<missing>'}.")
    if status not in PROGRESS_STATUSES:
        add("invalid_progress_status", f"Progress status is not canonical: {status or '<missing>'}.")
    if stage == "final" and status != "complete":
        add("invalid_completion_status", "A final stage requires status 'complete'.")
    elif status == "complete" and stage != "final":
        add("invalid_completion_status", "Status 'complete' requires stage 'final'.")

    message_path = resolve_inside(root, delivery_message)
    receipt_path = resolve_inside(root, receipt)
    artifact_path = resolve_inside(root, artifact)
    for label, path in (("delivery message", message_path), ("receipt", receipt_path), ("artifact", artifact_path)):
        if path is None:
            add("invalid_delivery_path", f"The {label} path must stay inside the task directory.")
    message_exists = message_path is not None and message_path.is_file()
    try:
        message = read_text(message_path) if message_exists else ""
    except (OSError, UnicodeError):
        message = ""
        add("invalid_delivery_message", "The intended delivery message is unreadable or is not valid UTF-8.")
    completion_claim = claims_completion(message, artifact=artifact)
    terminal_state = stage == "final" and status == "complete"
    terminal_intent = completion_claim or terminal_state

    if terminal_intent and not message_exists:
        add("missing_delivery_message", "Terminal delivery has no user-visible delivery message to validate.")
    if completion_claim and not terminal_state:
        add(
            "completion_claim_without_terminal_state",
            "The user-visible message claims completion while progress is not final/complete.",
        )

    open_progress_issues = collect_open_issues(progress)
    if completion_claim and open_progress_issues:
        add(
            "completion_claim_with_open_blockers",
            "The user-visible message claims completion while progress still records open blockers.",
        )
    elif terminal_state and open_progress_issues:
        add(
            "terminal_state_with_open_blockers",
            "Progress is final/complete while open blockers or explicitly incomplete units remain.",
        )

    requirement_findings, requirement_limitations = inspect_requirements(
        root / "state" / "requirements.jsonl", contract_version=contract_version
    )
    if terminal_intent:
        for finding in requirement_findings:
            add("unresolved_required_corrections", finding)

    receipt_exists = receipt_path is not None and receipt_path.is_file()
    receipt_data = read_json_or_none(receipt_path) if receipt_exists else None
    if terminal_intent and not receipt_exists:
        add("missing_delivery_receipt", "Terminal delivery is missing state/final_delivery.json.")
    elif receipt_exists and not isinstance(receipt_data, dict):
        add("invalid_delivery_receipt", "The delivery receipt is not valid JSON object data.")

    accepted_limitations = collect_accepted_limitations(progress)
    accepted_limitations.extend(requirement_limitations)
    if isinstance(receipt_data, dict):
        accepted_limitations.extend(collect_accepted_limitations(receipt_data))
        if receipt_data.get("schema_version") != 1 or receipt_data.get("status") != "pass":
            add("invalid_delivery_receipt", "The delivery receipt must use schema_version 1 and status 'pass'.")
        if receipt_data.get("scope") != "global_final_delivery":
            add(
                "insufficient_final_review_scope",
                "The delivery receipt does not cover the global final delivery.",
            )
        if receipt_data.get("artifact") != artifact:
            add("delivery_receipt_artifact_mismatch", "The receipt names a different primary artifact.")
        if collect_open_issues(receipt_data):
            add("invalid_delivery_receipt", "The delivery receipt records unresolved issues despite PASS status.")

        expected_inputs = [
            artifact, *[path for path in REQUIRED_HASH_INPUTS if path != "delivery_message.md"],
            delivery_message,
        ]
        expected_inputs.extend(path for path in OPTIONAL_HASH_INPUTS if (root / path).exists())
        hashes = receipt_data.get("artifacts")
        if not isinstance(hashes, dict):
            add("incomplete_delivery_receipt", "The delivery receipt has no artifact hash map.")
        else:
            for relative in expected_inputs:
                path = resolve_inside(root, relative)
                if path is None or not path.is_file():
                    add("missing_delivery_inputs", f"Required delivery input is missing or outside the project: {relative}.")
                    continue
                recorded_hash = str(hashes.get(relative, "")).strip().lower()
                if not recorded_hash:
                    add("incomplete_delivery_receipt", f"The delivery receipt omits a hash for {relative}.")
                elif recorded_hash != sha256_file(path).lower():
                    add("stale_delivery_receipt", f"The delivery receipt is stale for {relative}.")

    review_rows, review_findings = inspect_jsonl(root / "logs" / "review.jsonl", "Review")
    required_scopes = progress.get("required_review_scopes", [])
    valid_scopes = (
        isinstance(required_scopes, list)
        and all(isinstance(value, str) and value.strip() for value in required_scopes)
    )
    if valid_scopes:
        keys = [scope_key(value) for value in required_scopes]
        valid_scopes = len(keys) == len(set(keys))
    if not valid_scopes:
        add("invalid_required_review_scopes", "required_review_scopes must be a list of distinct, non-empty scope names.")
    if terminal_intent:
        for finding in review_findings:
            add("invalid_review_log", finding)
        if not latest_global_review_passes(review_rows):
            add(
                "insufficient_final_review_scope",
                "The latest full-report or global-final review is missing, non-PASS, or records open issues.",
            )
        if valid_scopes:
            latest_by_scope = {
                scope_key(str(row.get("scope", ""))): row for row in review_rows
            }
            for scope in required_scopes:
                latest = latest_by_scope.get(scope_key(scope))
                if latest is None:
                    add("missing_required_review", f"No review exists for required scope {scope!r}.")
                elif not review_passes(latest):
                    add("failed_required_review", f"The latest review for required scope {scope!r} is not a clean PASS.")

        if contract_version == 2 and artifact_path is not None and artifact_path.is_file():
            latest_by_scope = {scope_key(str(row.get("scope", ""))): row for row in review_rows}
            scopes_to_bind = {"__global__"}
            if valid_scopes:
                scopes_to_bind.update(scope_key(value) for value in required_scopes)
            current_hash = sha256_file(artifact_path)
            for scope in sorted(scopes_to_bind):
                row = latest_by_scope.get(scope)
                if row is None or not review_passes(row):
                    continue  # Missing/failed reviews already have their own findings.
                bound_hash = row.get("artifact_sha256")
                if not isinstance(bound_hash, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", bound_hash):
                    add("missing_review_artifact_binding", f"Latest {scope!r} review has no valid artifact_sha256.")
                elif bound_hash.lower() != current_hash:
                    add("stale_review_artifact", f"Latest {scope!r} review does not cover the current artifact.")

    accepted_limitations = list(dict.fromkeys(accepted_limitations))
    disclosure = assess_limitation_disclosure(message, accepted_limitations)
    warnings: list[str] = []
    if type(contract_version) is int and contract_version == 1:
        warnings.append(
            "Legacy v1 record check only: user-decision evidence, declared reading depth and "
            "review-to-artifact binding were not checked. This is not current-contract acceptance."
        )
    if terminal_intent and disclosure["status"] in {"absent", "contradiction"}:
        add(
            "undisclosed_accepted_limitations",
            "Accepted limitations exist backstage but are absent from the user-visible delivery message."
            if disclosure["status"] == "absent" else
            "Accepted limitations exist backstage but the delivery message explicitly denies them.",
        )
    elif terminal_intent and disclosure["status"] == "needs_review":
        warnings.append(
            "Specific limitation coverage requires semantic review; a generic keyword or unmatched "
            "paraphrase is not verification. Inspect limitation_disclosure.unmatched_limitations."
        )

    delivery_observation = "not_provided"
    if actual_message is not None:
        captured_path = Path(actual_message)
        try:
            captured = captured_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            delivery_observation = "unreadable"
            add("missing_actual_delivery", "The caller-provided actual delivery capture is missing or unreadable.")
        else:
            normalize = lambda text: text.replace("\r\n", "\n").replace("\r", "\n").strip()
            if not message_exists or normalize(captured) != normalize(message):
                delivery_observation = "mismatch"
                add("actual_delivery_mismatch", "The captured actual reply differs from the receipt-bound intended message.")
            else:
                delivery_observation = "matched"

    return {
        "ok": not flags,
        "delivery_contract_version": contract_version,
        "current_contract_checked": type(contract_version) is int and contract_version == DELIVERY_CONTRACT_VERSION,
        "semantic_verification": False,
        "flags": flags,
        "findings": findings,
        "completion_claim": completion_claim,
        "terminal_state": terminal_state,
        "stage": stage,
        "status": status,
        "accepted_limitations": accepted_limitations,
        "limitation_disclosure": disclosure,
        "warnings": warnings,
        "delivery_observation": delivery_observation,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--artifact", default="final.md")
    parser.add_argument("--delivery-message", default="delivery_message.md")
    parser.add_argument("--receipt", default="state/final_delivery.json")
    parser.add_argument(
        "--actual-message", type=Path,
        help="Compare a caller-provided runtime capture with the receipt-bound message; no capture is inferred.",
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--contract-version", type=int, choices=(1, 2), default=DELIVERY_CONTRACT_VERSION,
        help="Default 2 checks current records. Use 1 only for explicitly labelled historical diagnostics.",
    )
    args = parser.parse_args()

    result = evaluate_delivery(
        Path(args.project_root),
        artifact=args.artifact,
        delivery_message=args.delivery_message,
        receipt=args.receipt,
        actual_message=args.actual_message,
        contract_version=args.contract_version,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["ok"]:
        label = "legacy v1 record checks, not current-contract acceptance" if args.contract_version == 1 else "mechanical delivery checks"
        print(f"PASS: {label}; not a semantic quality verdict.")
    else:
        print("FAIL: delivery claim is not safe.")
        for finding in result["findings"]:
            print(f"- {finding}")
    if not args.json:
        for warning in result["warnings"]:
            print(f"REVIEW: {warning}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
