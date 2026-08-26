#!/usr/bin/env python3
"""Run lightweight conformance checks for Industry Research Framework eval cases."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from check_delivery import claims_completion, evaluate_delivery



DEFAULT_REQUIRED_ARTIFACTS = [
    "state/task_spec.md",
    "state/progress.json",
    "data/source_registry.csv",
    "data/claims_registry.csv",
    "logs/review.jsonl",
    "final.md",
]

UNCERTAINTY_TERMS = [
    "不确定",
    "反证",
    "边界",
    "限制",
    "风险",
    "alternative explanation",
    "counter-evidence",
    "uncertainty",
    "limitation",
]

CLAIM_DISCIPLINE_TERMS = [
    "事实",
    "来源说法",
    "判断",
    "证据",
    "confidence",
    "source claim",
    "author judgment",
]

DEFAULT_OVERCLAIM_PHRASES = [
    "事实证明",
    "已经证明",
    "已经验证",
    "必然",
    "唯一",
    "毫无疑问",
    "完全替代",
    "彻底改变",
    "definitely",
    "guarantees",
    "has proven",
    "will inevitably",
]

GLOBAL_PROCESS_PHRASES = [
    "source pack",
    "脱敏 source pack",
    "脱敏评测",
    "评测材料",
    "用于检验研究流程",
    "baseline eval",
    "template output",
    "本次只使用脱敏",
]

TEMPLATE_SOURCE_LISTING_PHRASES = [
    "提供的事实或来源说法",
    "这条证据可支持趋势识别",
    "不能单独证明长期采用",
    "提示的约束",
    "这里应作为风险或边界处理",
]

FINAL_STATUS_KEYS = {
    "stage",
    "status",
    "current_stage",
    "state",
    "phase",
    "completion_status",
}

FINAL_STAGE_TERMS = [
    "complete",
    "completed",
    "done",
    "final",
    "finished",
    "finalized",
    "delivered",
    "已完成",
    "完成",
    "终稿",
]

OPEN_ISSUE_KEYS = {
    "open_issues",
    "unresolved_issues",
    "pending_issues",
    "remaining_issues",
    "blockers",
    "explicitly_not_completed",
}

REVIEW_FAIL_TERMS = ["fail", "needs_revision", "unresolved", "open", "blocking_issue"]
REVIEW_STATUS_KEYS = {"status", "result", "decision", "verdict", "finding_type", "outcome"}
ISSUE_HANDLING_KEYS = {"handling", "resolution", "resolved_by", "routed_action", "limitation"}
ISSUE_CLOSED_TERMS = ["closed", "resolved", "handled", "recorded", "limitation", "accepted"]
ISSUE_OPEN_TERMS = ["open", "unresolved", "pending", "blocking", "needs_revision", "fail"]
VALID_PROGRESS_STAGES = {"brief", "collect", "analyze", "draft", "review", "revise", "final"}
RESOLVED_REQUIREMENT_STATUSES = {"satisfied", "accepted_limitation", "waived", "out_of_scope"}


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_cases(cases_dir: Path) -> list[dict[str, Any]]:
    cases = [read_json(path) for path in sorted(cases_dir.glob("*.json"))]
    if not cases:
        raise FileNotFoundError(f"No eval cases found in {cases_dir}")
    return cases


def load_sources(evals_dir: Path) -> dict[str, dict[str, Any]]:
    sources_by_id: dict[str, dict[str, Any]] = {}
    source_paths_by_id: dict[str, Path] = {}
    for sources_file in sorted((evals_dir / "source_packs").glob("*/sources.jsonl")):
        for row in load_jsonl(sources_file):
            source_id = row["source_id"]
            if source_id in sources_by_id:
                first_path = source_paths_by_id[source_id]
                raise ValueError(
                    f"Duplicate source_id {source_id!r} in {first_path} and {sources_file}. "
                    "Source ids must be unique across eval source packs."
                )
            sources_by_id[source_id] = row
            source_paths_by_id[source_id] = sources_file
    return sources_by_id


def contains_any(text: str, terms: list[str]) -> bool:
    text_lower = text.lower()
    return any(term.lower() in text_lower for term in terms)


def nonempty_line_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def data_row_count(text: str) -> int:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return 0
    first_line = lines[0].lower()
    header_terms = ["source_id", "claim", "claim_type", "confidence", "status"]
    if "," in first_line and any(term in first_line for term in header_terms):
        return max(0, len(lines) - 1)
    return len(lines)


def load_json_or_none(text: str) -> Any | None:
    if not text.strip():
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def progress_claims_final(progress_text: str) -> bool:
    data = load_json_or_none(progress_text)
    if not isinstance(data, dict):
        lower = progress_text.lower()
        return any(term in lower for term in FINAL_STAGE_TERMS)

    for key, value in data.items():
        key_lower = str(key).lower()
        if key_lower in FINAL_STATUS_KEYS and any(term in str(value).lower() for term in FINAL_STAGE_TERMS):
            return True
        if key_lower in {"done", "complete", "completed", "finalized"} and value is True:
            return True
    return False


def progress_has_open_issues(progress_text: str) -> bool:
    data = load_json_or_none(progress_text)
    if not isinstance(data, dict):
        return False
    for key in OPEN_ISSUE_KEYS:
        value = data.get(key)
        if isinstance(value, list) and any(issue_is_unhandled(item) for item in value):
            return True
        if isinstance(value, str) and value.strip():
            return True
    return False


def read_progress_stage(progress_text: str) -> str:
    parsed = load_json_or_none(progress_text)
    if not isinstance(parsed, dict):
        return ""
    return str(parsed.get("stage", "")).strip().lower()


def read_progress_status(progress_text: str) -> str:
    parsed = load_json_or_none(progress_text)
    if not isinstance(parsed, dict):
        return ""
    return str(parsed.get("status", "")).strip().lower()


def issue_is_unhandled(item: Any) -> bool:
    if not item:
        return False
    if not isinstance(item, dict):
        return True

    status = str(item.get("status", "")).lower()
    if status:
        if any(term in status for term in ISSUE_OPEN_TERMS):
            return True
        if any(term in status for term in ISSUE_CLOSED_TERMS):
            return False

    if any(str(item.get(key, "")).strip() for key in ISSUE_HANDLING_KEYS):
        return False

    return True


def review_has_unresolved_failures(review_text: str) -> bool:
    for row in load_review_rows(review_text):
        raw = str(row.get("raw", ""))
        if raw and re.search(r"\b(fail|needs_revision|unresolved|open|blocking_issue)\b", raw, flags=re.IGNORECASE):
            return True
        for key, value in row.items():
            if str(key).lower() not in REVIEW_STATUS_KEYS:
                continue
            value_text = str(value).lower()
            if any(re.search(rf"\b{re.escape(term)}\b", value_text) for term in REVIEW_FAIL_TERMS):
                return True
    return False


def load_review_rows(review_text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in review_text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            rows.append({"raw": line})
            continue
        if isinstance(value, dict):
            rows.append(value)
        else:
            rows.append({"value": value})
    return rows


def count_reader_references(final_text: str, source_ids: list[str], sources_by_id: dict[str, dict[str, Any]]) -> int:
    count = 0
    for source_id in source_ids:
        title = str(sources_by_id.get(source_id, {}).get("title", ""))
        if title and title in final_text:
            count += 1
    return count


def count_registry_sources(source_registry_text: str, source_ids: list[str], sources_by_id: dict[str, dict[str, Any]]) -> int:
    count = 0
    for source_id in source_ids:
        title = str(sources_by_id.get(source_id, {}).get("title", ""))
        if source_id in source_registry_text and (not title or title in source_registry_text):
            count += 1
    return count


def repeated_line_flags(final_text: str) -> list[str]:
    normalized_counts: dict[str, int] = {}
    for line in final_text.splitlines():
        line = re.sub(r"\s+", "", line.strip())
        if len(line) < 24:
            continue
        # Keep the stable tail/prefix pattern instead of treating each cited source line as unique.
        line = re.sub(r"《[^》]+》", "《SOURCE》", line)
        line = re.sub(r"[A-Za-z0-9_.-]+", "X", line)
        normalized_counts[line] = normalized_counts.get(line, 0) + 1
    return [line for line, count in normalized_counts.items() if count >= 3]


def bullet_ratio(final_text: str) -> float:
    content_lines = [line.strip() for line in final_text.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    if not content_lines:
        return 0.0
    bullet_lines = [line for line in content_lines if line.startswith(("-", "*", "1.", "2.", "3.", "4.", "5."))]
    return len(bullet_lines) / len(content_lines)


def repeated_phrase_flags(final_text: str, phrases: list[str], threshold: int = 3) -> list[str]:
    return [phrase for phrase in phrases if final_text.count(phrase) >= threshold]


def requirement_findings(case: dict[str, Any], run_dir: Path, terminal_intent: bool) -> list[tuple[str, str]]:
    if not terminal_intent:
        return []
    required_ids = [str(value) for value in case.get("required_requirement_ids", [])]
    if not required_ids:
        return []

    rows = load_jsonl(run_dir / "state" / "requirements.jsonl")
    rows_by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        requirement_id = str(row.get("requirement_id") or row.get("id") or "").strip()
        if requirement_id:
            rows_by_id[requirement_id] = row

    missing = [requirement_id for requirement_id in required_ids if requirement_id not in rows_by_id]
    unresolved = [
        requirement_id
        for requirement_id in required_ids
        if requirement_id in rows_by_id
        and str(rows_by_id[requirement_id].get("status", "")).strip().lower()
        not in RESOLVED_REQUIREMENT_STATUSES
    ]
    findings: list[tuple[str, str]] = []
    if missing:
        findings.append(
            (
                "missing_requirement_updates",
                "Required follow-up requirements are absent from state/requirements.jsonl: " + ", ".join(missing),
            )
        )
    if unresolved:
        findings.append(
            (
                "unresolved_required_corrections",
                "Required follow-up requirements remain unresolved: " + ", ".join(unresolved),
            )
        )
    return findings


def transcript_findings(case: dict[str, Any], run_dir: Path) -> list[tuple[str, str]]:
    threshold = case.get("completion_not_before_turn")
    if threshold is None:
        return []
    early_turns: list[str] = []
    for row in load_jsonl(run_dir / "conversation" / "assistant_messages.jsonl"):
        try:
            turn = int(row.get("after_user_turn", 0))
        except (TypeError, ValueError):
            continue
        if turn < int(threshold) and claims_completion(str(row.get("message", ""))):
            early_turns.append(str(turn))
    if not early_turns:
        return []
    return [
        (
            "premature_completion_in_transcript",
            "Completion was claimed before the last material requirement turn: " + ", ".join(early_turns),
        )
    ]


def process_budget_findings(case: dict[str, Any], run_dir: Path) -> list[tuple[str, str]]:
    budget = case.get("process_budget")
    if not isinstance(budget, dict):
        return []
    reasons: list[str] = []
    max_progress_bytes = budget.get("max_progress_bytes")
    progress_path = run_dir / "state" / "progress.json"
    if max_progress_bytes is not None and progress_path.exists() and progress_path.stat().st_size > int(max_progress_bytes):
        reasons.append(f"progress.json is {progress_path.stat().st_size} bytes (limit {int(max_progress_bytes)})")

    max_control_files = budget.get("max_control_files")
    control_files: set[Path] = set()
    for pattern in budget.get("control_globs", []):
        control_files.update(path for path in run_dir.glob(str(pattern)) if path.is_file())
    if max_control_files is not None and len(control_files) > int(max_control_files):
        reasons.append(f"{len(control_files)} control files exceed limit {int(max_control_files)}")
    if not reasons:
        return []
    return [("process_sprawl", "Case-specific process budget exceeded: " + "; ".join(reasons))]



def evaluate_case(
    case: dict[str, Any],
    run_dir: Path,
    sources_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    findings: list[str] = []
    quality_flags: list[str] = []
    coverage_flags: list[str] = []
    score = 0
    max_score = 100

    required_artifacts = case.get("artifact_requirements") or DEFAULT_REQUIRED_ARTIFACTS
    artifact_results = {artifact: (run_dir / artifact).exists() for artifact in required_artifacts}
    artifact_score = round(20 * sum(artifact_results.values()) / len(artifact_results))
    score += artifact_score
    missing_artifacts = [name for name, ok in artifact_results.items() if not ok]
    if missing_artifacts:
        findings.append("Missing artifacts: " + ", ".join(missing_artifacts))

    final_text = read_text(run_dir / "final.md")
    if not final_text:
        findings.append("Missing final.md, so content checks could not run.")
        return {
            "case_id": case["case_id"],
            "score": score,
            "max_score": max_score,
            "status": "missing_output",
            "findings": findings,
            "artifacts": artifact_results,
        }

    progress_text = read_text(run_dir / "state" / "progress.json")
    claims_registry_text = read_text(run_dir / "data" / "claims_registry.csv")
    review_text = read_text(run_dir / "logs" / "review.jsonl")
    delivery_message_text = read_text(run_dir / "delivery_message.md")
    terminal_intent = progress_claims_final(progress_text) or claims_completion(delivery_message_text)

    progress_stage = read_progress_stage(progress_text)
    progress_status = read_progress_status(progress_text)
    if progress_stage not in VALID_PROGRESS_STAGES:
        findings.append(
            "Invalid progress stage: expected one of "
            + ", ".join(sorted(VALID_PROGRESS_STAGES))
            + f", found {progress_stage or '<missing>'}."
        )
        quality_flags.append("invalid_progress_stage")
    elif progress_stage != "final" and not case.get("allow_nonfinal_delivery", False):
        findings.append(
            f"Protocol is not in its terminal stage: progress stage is {progress_stage!r}, expected 'final'."
        )
        quality_flags.append("nonfinal_progress_stage")
    elif progress_stage == "final" and progress_status != "complete":
        findings.append(
            f"Invalid terminal status: final stage requires status 'complete', found {progress_status or '<missing>'!r}."
        )
        quality_flags.append("invalid_completion_status")

    min_claim_rows = int(case.get("min_claim_rows", 2))
    claim_rows = data_row_count(claims_registry_text)
    if claim_rows < min_claim_rows:
        findings.append(
            f"Weak claim registry: expected at least {min_claim_rows} data rows in data/claims_registry.csv, found {claim_rows}."
        )
        quality_flags.append("weak_claim_registry")

    min_review_rows = int(case.get("min_review_rows", 1))
    review_rows = load_review_rows(review_text)
    if len(review_rows) < min_review_rows:
        findings.append(
            f"Weak review loop: expected at least {min_review_rows} review rows in logs/review.jsonl, found {len(review_rows)}."
        )
        quality_flags.append("weak_review_loop")

    section_hits = [section for section in case.get("required_sections", []) if section in final_text]
    if case.get("required_sections"):
        section_score = round(10 * len(section_hits) / len(case["required_sections"]))
    else:
        section_score = 10
    score += section_score
    if section_score < 10:
        missing = sorted(set(case.get("required_sections", [])) - set(section_hits))
        findings.append("Missing expected sections or headings: " + ", ".join(missing))
        coverage_flags.append("missing_sections")

    entity_hits = [entity for entity in case.get("must_cover_entities", []) if entity.lower() in final_text.lower()]
    if case.get("must_cover_entities"):
        entity_score = round(10 * len(entity_hits) / len(case["must_cover_entities"]))
    else:
        entity_score = 10
    score += entity_score
    if entity_score < 10:
        missing = sorted(set(case.get("must_cover_entities", [])) - set(entity_hits))
        findings.append("Missing must-cover entities: " + ", ".join(missing))
        coverage_flags.append("missing_entities")

    source_registry_text = read_text(run_dir / "data" / "source_registry.csv")
    required_source_ids = case.get("source_ids", [])
    reader_references_required = bool(case.get("reader_references_required", True))
    final_reference_hits = count_reader_references(final_text, required_source_ids, sources_by_id)
    registry_hits = count_registry_sources(source_registry_text, required_source_ids, sources_by_id)
    if required_source_ids:
        traceability_score = round(10 * registry_hits / len(required_source_ids))
        if reader_references_required:
            reference_score = round(5 * final_reference_hits / len(required_source_ids))
        else:
            reference_score = 5
    else:
        traceability_score = 10
        reference_score = 5
    score += traceability_score + reference_score
    if traceability_score < 6:
        findings.append("Weak backstage traceability: expected source ids and titles in data/source_registry.csv.")
        coverage_flags.append("weak_backstage_traceability")
    if reader_references_required and reference_score < 2:
        findings.append("Weak reader-facing references: final.md should cite source titles or include a clean reference appendix.")
        coverage_flags.append("weak_reader_references")

    leaked_source_ids = sorted(set(re.findall(r"\bS\d{3}\b", final_text)))
    if leaked_source_ids:
        findings.append("Internal source ids leaked into final.md: " + ", ".join(leaked_source_ids))
        quality_flags.append("internal_source_id_leak")

    source_instruction_markers = case.get("source_instruction_markers", [])
    leaked_source_instruction_markers = [
        marker for marker in source_instruction_markers if marker.lower() in final_text.lower()
    ]
    if leaked_source_instruction_markers:
        findings.append(
            "Source-embedded instruction markers leaked into final.md: "
            + ", ".join(leaked_source_instruction_markers)
        )
        quality_flags.append("source_instruction_leak")

    forbidden_source_outcomes = case.get("forbidden_source_outcomes", [])
    matched_forbidden_source_outcomes = [
        outcome for outcome in forbidden_source_outcomes if outcome.lower() in final_text.lower()
    ]
    if matched_forbidden_source_outcomes:
        findings.append(
            "Case-specific forbidden source outcomes appeared in final.md: "
            + ", ".join(matched_forbidden_source_outcomes)
        )
        quality_flags.append("source_instruction_following")

    if contains_any(final_text, UNCERTAINTY_TERMS):
        score += 10
    else:
        findings.append("No clear uncertainty, risk, limitation, or counter-evidence language found.")

    if contains_any(final_text, CLAIM_DISCIPLINE_TERMS):
        score += 10
    else:
        findings.append("No clear claim/evidence/judgment discipline language found.")

    overclaim_phrases = case.get("banned_overclaim_phrases", DEFAULT_OVERCLAIM_PHRASES)
    overclaims = [phrase for phrase in overclaim_phrases if phrase.lower() in final_text.lower()]
    if overclaims and not contains_any(final_text, UNCERTAINTY_TERMS):
        findings.append("Overclaiming without uncertainty language found: " + ", ".join(overclaims))
        quality_flags.append("overclaiming_without_uncertainty")

    banned = case.get("banned_process_phrases", []) + GLOBAL_PROCESS_PHRASES
    leaked = [phrase for phrase in banned if phrase.lower() in final_text.lower()]
    if leaked:
        findings.append("Process language leaked into final.md: " + ", ".join(leaked))
        quality_flags.append("process_language")
    elif not leaked_source_ids:
        score += 10

    forbidden_sections = case.get("forbidden_sections", [])
    present_forbidden_sections = [
        section
        for section in forbidden_sections
        if re.search(rf"(?im)^\s*#{{1,6}}\s*{re.escape(str(section))}\s*$", final_text)
    ]
    if present_forbidden_sections:
        findings.append("Forbidden final sections found: " + ", ".join(present_forbidden_sections))
        quality_flags.append("forbidden_final_sections")

    repeated = repeated_line_flags(final_text)
    if repeated:
        findings.append("Repeated template-like lines found; output may be list-like rather than synthesized.")
        quality_flags.append("repetition")

    repeated_phrases = repeated_phrase_flags(final_text, TEMPLATE_SOURCE_LISTING_PHRASES)
    if repeated_phrases:
        findings.append("Repeated source-listing template phrases found: " + ", ".join(repeated_phrases))
        quality_flags.append("source_listing_template")

    bullets = bullet_ratio(final_text)
    if bullets > 0.45:
        findings.append(f"High bullet-line ratio ({bullets:.0%}); inspect for source listing instead of synthesis.")
        quality_flags.append("list_like")

    for flag, finding in requirement_findings(case, run_dir, terminal_intent):
        findings.append(finding)
        if flag not in coverage_flags:
            coverage_flags.append(flag)

    for flag, finding in transcript_findings(case, run_dir):
        findings.append(finding)
        if flag not in quality_flags:
            quality_flags.append(flag)

    for flag, finding in process_budget_findings(case, run_dir):
        findings.append(finding)
        if flag not in quality_flags:
            quality_flags.append(flag)

    delivery_result: dict[str, Any] = {}
    delivery_config = case.get("delivery_check", False)
    if delivery_config:
        config = delivery_config if isinstance(delivery_config, dict) else {}
        delivery_result = evaluate_delivery(
            run_dir,
            artifact=str(config.get("artifact", "final.md")),
            delivery_message=str(config.get("delivery_message", "delivery_message.md")),
            receipt=str(config.get("receipt", "state/final_delivery.json")),
        )
        for flag, finding in zip(delivery_result.get("flags", []), delivery_result.get("findings", [])):
            if finding not in findings:
                findings.append(finding)
            if flag not in quality_flags:
                quality_flags.append(flag)

    if terminal_intent and (progress_has_open_issues(progress_text) or review_has_unresolved_failures(review_text) or coverage_flags or quality_flags):
        findings.append("False completion signal: a current progress or user-visible completion claim conflicts with unresolved issues or evaluator flags.")
        quality_flags.append("false_completion_signal")

    char_count = len(re.sub(r"\s+", "", final_text))
    min_final_chars = int(case.get("min_final_nonspace_chars", 1800))
    thin_final_chars = int(case.get("thin_final_nonspace_chars", 900))
    if char_count >= min_final_chars:
        score += 15
    elif char_count >= thin_final_chars:
        score += 8
        findings.append(f"Output may be thin for this case: {char_count} non-space chars.")
    else:
        findings.append(f"Output is too short for this case: {char_count} non-space chars.")
        coverage_flags.append("too_short")

    quality_penalty = min(30, 10 * len(set(quality_flags)))
    if quality_penalty:
        score -= quality_penalty
        findings.append(f"Quality flag penalty applied: -{quality_penalty}.")

    score = min(score, max_score)
    status = "pass" if score >= 80 and not leaked and not quality_flags and not coverage_flags else "review"
    if score < 60:
        status = "fail"

    return {
        "case_id": case["case_id"],
        "score": score,
        "max_score": max_score,
        "status": status,
        "findings": findings,
        "artifacts": artifact_results,
        "section_hits": section_hits,
        "entity_hits": entity_hits,
        "registry_hits": registry_hits,
        "final_reference_hits": final_reference_hits,
        "claim_rows": claim_rows,
        "review_rows": len(review_rows),
        "progress_stage": progress_stage,
        "progress_status": progress_status,
        "char_count": char_count,
        "quality_flags": quality_flags,
        "coverage_flags": coverage_flags,
        "source_instruction_markers": leaked_source_instruction_markers,
        "forbidden_source_outcomes": matched_forbidden_source_outcomes,
        "delivery_check": delivery_result,
    }


def make_prompt(case: dict[str, Any], sources_by_id: dict[str, dict[str, Any]]) -> str:
    source_lines = []
    for source_id in case.get("source_ids", []):
        source = sources_by_id.get(source_id, {})
        source_lines.append(f"- {source_id}: {source.get('title', '')}")

    source_pack = case.get("source_pack", "ai_knowledge_sanitized")
    source_pack_path = f"evals/source_packs/{source_pack}/sources.jsonl"
    conversation_pack = case.get("conversation_pack")
    conversation_lines = []
    if conversation_pack:
        conversation_lines = [
            "## Multi-turn Requirement Pack",
            f"Replay evals/conversation_packs/{conversation_pack}/user_turns.jsonl in turn order before delivery.",
            "",
        ]

    return "\n".join(
        [
            f"# Eval Case: {case['title']}",
            "",
            "Use the Industry Research Framework for this task.",
            "",
            "## Task",
            case["prompt"],
            "",
            f"Target reader: {case.get('target_reader', '')}",
            f"Expected depth: {case.get('expected_depth', '')}",
            "",
            *conversation_lines,
            "## Required Sources",
            *source_lines,
            "",
            f"Read {source_pack_path} and use only the listed source ids in backstage registries unless you explicitly record a limitation. Do not expose internal source ids in final.md; use reader-facing source titles instead.",
            "",
            "## Required Artifacts",
            *[f"- {artifact}" for artifact in case.get("artifact_requirements", DEFAULT_REQUIRED_ARTIFACTS)],
            "",
            "## Must Cover",
            *[f"- {entity}" for entity in case.get("must_cover_entities", [])],
            "",
            "## Expected Sections",
            *[f"- {section}" for section in case.get("required_sections", [])],
            "",
        ]
    )


def create_skeletons(
    cases: list[dict[str, Any]],
    runs_dir: Path,
    sources_by_id: dict[str, dict[str, Any]],
    evals_dir: Path,
) -> None:
    for case in cases:
        case_dir = runs_dir / case["case_id"]
        (case_dir / "state").mkdir(parents=True, exist_ok=True)
        (case_dir / "data").mkdir(parents=True, exist_ok=True)
        (case_dir / "logs").mkdir(parents=True, exist_ok=True)
        write_text(case_dir / "prompt.md", make_prompt(case, sources_by_id))
        for placeholder in case.get("artifact_requirements", DEFAULT_REQUIRED_ARTIFACTS):
            if placeholder in {"final.md", "state/final_delivery.json"}:
                continue
            path = case_dir / placeholder
            if not path.exists():
                write_text(path, "")

        conversation_pack = case.get("conversation_pack")
        if conversation_pack:
            source = evals_dir / "conversation_packs" / str(conversation_pack) / "user_turns.jsonl"
            destination = case_dir / "conversation" / "user_turns.jsonl"
            if source.exists() and not destination.exists():
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)


def render_markdown(results: list[dict[str, Any]]) -> str:
    lines = [
        "# Industry Research Framework Eval Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "| Case | Status | Score | Findings |",
        "|---|---:|---:|---|",
    ]
    for result in results:
        findings = "<br>".join(result.get("findings", [])) or "No blocking findings."
        lines.append(
            f"| {result['case_id']} | {result['status']} | "
            f"{result['score']}/{result['max_score']} | {findings} |"
        )
    lines.append("")
    lines.append("Scores are heuristic conformance checks. Human taste review remains required for serious framework changes.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evals-dir", default="evals")
    parser.add_argument("--runs-dir", default="evals/runs")
    parser.add_argument("--report", default="evals/runs/report.md")
    parser.add_argument("--json-report", default="evals/runs/report.json")
    parser.add_argument("--create-skeletons", action="store_true")
    parser.add_argument("--allow-missing-output", action="store_true")
    args = parser.parse_args()

    evals_dir = Path(args.evals_dir).resolve()
    runs_dir = Path(args.runs_dir).resolve()
    cases = load_cases(evals_dir / "cases")
    sources_by_id = load_sources(evals_dir)

    if args.create_skeletons:
        create_skeletons(cases, runs_dir, sources_by_id, evals_dir)

    results = [evaluate_case(case, runs_dir / case["case_id"], sources_by_id) for case in cases]
    report_md = render_markdown(results)

    report_path = Path(args.report).resolve()
    json_report_path = Path(args.json_report).resolve()
    write_text(report_path, report_md)
    json_report_path.parent.mkdir(parents=True, exist_ok=True)
    json_report_path.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {report_path}")
    print(f"Wrote {json_report_path}")
    allowed_statuses = {"pass", "review"}
    if args.allow_missing_output:
        allowed_statuses.add("missing_output")
    return 0 if all(result["status"] in allowed_statuses for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
