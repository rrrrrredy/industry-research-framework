#!/usr/bin/env python3
"""Validate that a user-visible delivery claim matches current research state."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


CANONICAL_STAGES = {"brief", "collect", "analyze", "draft", "review", "revise", "final"}
OPEN_ISSUE_KEYS = {
    "open_issues",
    "unresolved_issues",
    "pending_issues",
    "remaining_issues",
    "blockers",
    "explicitly_not_completed",
}
CLOSED_ISSUE_TERMS = {"closed", "resolved", "handled", "accepted_limitation", "waived"}
OPEN_ISSUE_TERMS = {"open", "unresolved", "pending", "blocking", "incomplete", "not_completed"}
RESOLVED_REQUIREMENT_STATUSES = {"satisfied", "accepted_limitation", "waived", "out_of_scope"}

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
    return path.read_text(encoding="utf-8", errors="replace")


def read_json_or_none(path: Path) -> Any | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def inspect_jsonl(path: Path, label: str) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    findings: list[str] = []
    for line_number, line in enumerate(read_text(path).splitlines(), start=1):
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


def inspect_requirements(path: Path) -> tuple[list[str], list[str]]:
    """Return terminal-blocking requirement findings and accepted limitations."""

    findings: list[str] = []
    accepted_limitations: list[str] = []
    if not path.exists():
        return findings, accepted_limitations

    for line_number, line in enumerate(read_text(path).splitlines(), start=1):
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
        elif status == "accepted_limitation":
            limitation = str(
                row.get("summary") or row.get("description") or row.get("evidence") or label
            ).strip()
            accepted_limitations.append(limitation)
    return findings, accepted_limitations


def claims_completion(message: str) -> bool:
    """Return True only for an affirmative user-visible completion claim."""

    scrubbed = message.lower()
    for pattern in NEGATED_COMPLETION_PATTERNS:
        scrubbed = re.sub(pattern, " ", scrubbed, flags=re.IGNORECASE)
    return any(re.search(pattern, scrubbed, flags=re.IGNORECASE) for pattern in COMPLETION_PATTERNS)


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
    if any(issue.get(key) for key in ("resolution", "handling", "accepted_as_limitation", "routed_action")):
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
    latest: dict[str, Any] | None = None
    for row in rows:
        scope = str(row.get("scope", "")).strip().lower()
        if scope in GLOBAL_REVIEW_SCOPES:
            latest = row
    if latest is None:
        return False
    result = str(
        latest.get("result")
        or latest.get("status")
        or latest.get("decision")
        or latest.get("verdict")
        or ""
    ).strip().lower()
    return result in PASS_REVIEW_TERMS and not review_row_has_open_issues(latest)


def review_has_global_pass(review_path: Path) -> bool:
    rows, findings = inspect_jsonl(review_path, "Review")
    return not findings and latest_global_review_passes(rows)


def evaluate_delivery(
    project_root: Path,
    artifact: str = "final.md",
    delivery_message: str = "delivery_message.md",
    receipt: str = "state/final_delivery.json",
) -> dict[str, Any]:
    root = project_root.resolve()
    flags: list[str] = []
    findings: list[str] = []

    def add(flag: str, finding: str) -> None:
        if flag not in flags:
            flags.append(flag)
            findings.append(finding)

    progress_path = root / "state" / "progress.json"
    progress = read_json_or_none(progress_path)
    if not isinstance(progress, dict):
        progress = {}

    stage = str(progress.get("stage", "")).strip().lower()
    status = str(progress.get("status", "")).strip().lower()
    if stage not in CANONICAL_STAGES:
        add("invalid_progress_stage", f"Progress stage is not canonical: {stage or '<missing>'}.")
    if stage == "final" and status != "complete":
        add("invalid_completion_status", "A final stage requires status 'complete'.")
    elif status == "complete" and stage != "final":
        add("invalid_completion_status", "Status 'complete' requires stage 'final'.")

    message_path = root / delivery_message
    message_exists = message_path.exists()
    message = read_text(message_path)
    completion_claim = claims_completion(message)
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
        root / "state" / "requirements.jsonl"
    )
    if terminal_intent:
        for finding in requirement_findings:
            add("unresolved_required_corrections", finding)

    receipt_path = root / receipt
    receipt_exists = receipt_path.exists()
    receipt_data = read_json_or_none(receipt_path)
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

        expected_inputs = [artifact, *REQUIRED_HASH_INPUTS]
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
    if terminal_intent:
        for finding in review_findings:
            add("invalid_review_log", finding)
        if not latest_global_review_passes(review_rows):
            add(
                "insufficient_final_review_scope",
                "The latest full-report or global-final review is missing, non-PASS, or records open issues.",
            )

    accepted_limitations = list(dict.fromkeys(accepted_limitations))
    if terminal_intent and accepted_limitations and not any(
        term.lower() in message.lower() for term in LIMITATION_DISCLOSURE_TERMS
    ):
        add(
            "undisclosed_accepted_limitations",
            "Accepted limitations exist backstage but are absent from the user-visible delivery message.",
        )

    return {
        "ok": not flags,
        "flags": flags,
        "findings": findings,
        "completion_claim": completion_claim,
        "terminal_state": terminal_state,
        "stage": stage,
        "status": status,
        "accepted_limitations": accepted_limitations,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--artifact", default="final.md")
    parser.add_argument("--delivery-message", default="delivery_message.md")
    parser.add_argument("--receipt", default="state/final_delivery.json")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = evaluate_delivery(
        Path(args.project_root),
        artifact=args.artifact,
        delivery_message=args.delivery_message,
        receipt=args.receipt,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["ok"]:
        print("PASS: delivery claim matches current state and receipt.")
    else:
        print("FAIL: delivery claim is not safe.")
        for finding in result["findings"]:
            print(f"- {finding}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
