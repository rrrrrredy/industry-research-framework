#!/usr/bin/env python3
"""Validate the frozen cross-agent protocol and, optionally, its publication bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


REVIEW_DIMENSIONS = {
    "task_fidelity",
    "company_specificity",
    "evidence_discipline",
    "mechanism_and_synthesis",
    "counter_evidence_and_limitations",
    "decision_usefulness",
    "reader_quality",
}


def sha256(path: Path) -> str:
    data = path.read_bytes()
    if path.suffix.lower() in {".json", ".jsonl", ".md", ".txt", ".csv", ".yaml", ".yml"}:
        text = data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        data = text.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number} must contain a JSON object")
        rows.append(value)
    return rows


def validate_publication(
    repo_root: Path,
    manifest: dict[str, Any],
    lock: dict[str, Any],
    errors: list[str],
) -> None:
    completed_agents: list[str] = []
    run_ids: set[str] = set()
    conditions = [str(value) for value in manifest.get("conditions", [])]
    required = [str(value) for value in manifest.get("required_run_files", [])]
    lock_hash = sha256(repo_root / "evals" / "cross_agent" / "freeze.lock.json")
    matched_fields = ("runtime_version", "model", "reasoning_effort", "tool_policy", "timeout_seconds")

    for agent in manifest.get("agents", []):
        agent_id = str(agent.get("agent_id", ""))
        condition_dirs = [repo_root / "evals" / "cross_agent" / "runs" / agent_id / condition for condition in conditions]
        present = [path.exists() for path in condition_dirs]
        if not any(present):
            continue
        if not all(present):
            errors.append(f"{agent_id}: baseline/framework pair is incomplete")
            continue

        pair_valid = True
        pair_configs: list[tuple[str, ...]] = []
        for condition, run_dir in zip(conditions, condition_dirs):
            for relative in required:
                if not (run_dir / relative).exists():
                    errors.append(f"{agent_id}/{condition}: missing {relative}")
                    pair_valid = False
            run_path = run_dir / "run.json"
            if not run_path.exists():
                continue
            try:
                run = read_json(run_path)
            except (ValueError, json.JSONDecodeError) as error:
                errors.append(str(error))
                pair_valid = False
                continue
            if run.get("agent_id") != agent_id or run.get("condition") != condition:
                errors.append(f"{agent_id}/{condition}: run identity does not match its directory")
                pair_valid = False
            run_id = str(run.get("run_id", "")).strip()
            if not run_id or run_id in run_ids:
                errors.append(f"{agent_id}/{condition}: missing or duplicate run_id")
                pair_valid = False
            elif run_id:
                run_ids.add(run_id)
            for field in (
                "runtime_version",
                "model",
                "reasoning_effort",
                "tool_policy",
                "timeout_seconds",
                "started_at",
                "finished_at",
                "exit_code",
                "attempt_status",
                "prompt_sha256",
                "freeze_lock_sha256",
                "redactions",
            ):
                if field not in run:
                    errors.append(f"{agent_id}/{condition}: run.json lacks {field}")
                    pair_valid = False
            prompt_path = run_dir / "prompt.md"
            if prompt_path.is_file() and run.get("prompt_sha256") != sha256(prompt_path):
                errors.append(f"{agent_id}/{condition}: prompt hash does not match prompt.md")
                pair_valid = False
            if run.get("freeze_lock_sha256") != lock_hash:
                errors.append(f"{agent_id}/{condition}: run did not bind the current freeze lock")
                pair_valid = False
            if not isinstance(run.get("redactions"), list):
                errors.append(f"{agent_id}/{condition}: redactions must be a list")
                pair_valid = False
            pair_configs.append(
                tuple(json.dumps(run.get(field), ensure_ascii=False, sort_keys=True) for field in matched_fields)
            )
        if len(pair_configs) == len(conditions) and len(set(pair_configs)) != 1:
            errors.append(
                f"{agent_id}: baseline/framework settings differ for " + ", ".join(matched_fields)
            )
            pair_valid = False
        if pair_valid:
            completed_agents.append(agent_id)

    minimum = int(manifest.get("minimum_agents_for_publication", 3))
    if len(completed_agents) < minimum:
        errors.append(f"publication requires {minimum} complete agent pairs; found {len(completed_agents)}")

    for relative in manifest.get("required_review_files", []):
        if not (repo_root / str(relative)).exists():
            errors.append(f"publication bundle is missing {relative}")

    expected_blind_ids: set[str] = set()
    map_path = repo_root / "evals" / "cross_agent" / "reviews" / "blinding-map.json"
    if map_path.exists():
        try:
            map_data = read_json(map_path)
            mappings = map_data.get("runs", [])
            if not isinstance(mappings, list) or not all(isinstance(row, dict) for row in mappings):
                raise ValueError(f"{map_path} must contain a runs array of objects")
            mapped_run_ids = [str(row.get("run_id", "")).strip() for row in mappings]
            blind_ids = [str(row.get("blind_run_id", "")).strip() for row in mappings]
            if any(not value for value in mapped_run_ids + blind_ids):
                errors.append("blinding map contains an empty run_id or blind_run_id")
            if len(mapped_run_ids) != len(set(mapped_run_ids)) or len(blind_ids) != len(set(blind_ids)):
                errors.append("blinding map ids must be unique")
            if set(mapped_run_ids) != run_ids:
                errors.append("blinding map run ids do not exactly match published run ids")
            expected_blind_ids = set(blind_ids)
        except (ValueError, json.JSONDecodeError) as error:
            errors.append(str(error))

    reviews_path = repo_root / "evals" / "cross_agent" / "reviews" / "blind_reviews.jsonl"
    if reviews_path.exists():
        try:
            reviews = read_jsonl(reviews_path)
        except (ValueError, json.JSONDecodeError) as error:
            errors.append(str(error))
            reviews = []
        reviewers: dict[str, set[str]] = defaultdict(set)
        for row in reviews:
            blind_run_id = str(row.get("blind_run_id", "")).strip()
            reviewer_id = str(row.get("reviewer_id", "")).strip()
            if blind_run_id not in expected_blind_ids:
                errors.append(f"review references unknown blind run id: {blind_run_id or '<missing>'}")
            if not reviewer_id:
                errors.append(f"review for {blind_run_id or '<missing>'} lacks reviewer_id")
            elif reviewer_id in reviewers[blind_run_id]:
                errors.append(f"duplicate review by {reviewer_id} for {blind_run_id}")
            else:
                reviewers[blind_run_id].add(reviewer_id)
            scores = row.get("scores")
            if not isinstance(scores, dict) or not REVIEW_DIMENSIONS.issubset(scores):
                errors.append(f"review for {blind_run_id or '<missing>'} lacks required score dimensions")
            elif any(
                not isinstance(scores[name], (int, float)) or isinstance(scores[name], bool) or not 1 <= scores[name] <= 5
                for name in REVIEW_DIMENSIONS
            ):
                errors.append(f"review for {blind_run_id or '<missing>'} has a score outside 1-5")
            if not isinstance(row.get("critical_failure"), bool):
                errors.append(f"review for {blind_run_id or '<missing>'} lacks boolean critical_failure")
            for field in ("critical_failure_reason", "strengths", "problems", "verdict"):
                if field not in row:
                    errors.append(f"review for {blind_run_id or '<missing>'} lacks {field}")
        required_reviewers = int(manifest.get("reviewers_per_run", 2))
        for blind_run_id in expected_blind_ids:
            count = len(reviewers.get(blind_run_id, set()))
            if count < required_reviewers:
                errors.append(
                    f"publication requires {required_reviewers} blinded reviewers for {blind_run_id}; found {count}"
                )

    if manifest.get("status") != "complete":
        errors.append("manifest status must be 'complete' before publication")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-publication", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    manifest_path = repo_root / "evals" / "cross_agent" / "manifest.json"
    lock_path = repo_root / "evals" / "cross_agent" / "freeze.lock.json"
    errors: list[str] = []

    try:
        manifest = read_json(manifest_path)
        lock = read_json(lock_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}")
        return 1

    agents = [str(item.get("agent_id", "")) for item in manifest.get("agents", [])]
    if not 3 <= len(agents) <= 4 or len(agents) != len(set(agents)) or any(not value for value in agents):
        errors.append("manifest must name three or four unique non-empty agent ids")
    if manifest.get("conditions") != ["baseline", "framework"]:
        errors.append("conditions must be exactly baseline and framework")
    if manifest.get("status") not in {"prepared_no_runs", "in_progress", "complete"}:
        errors.append("manifest has an invalid status")

    locked_protocol = lock.get("protocol")
    expected_protocol = {
        "protocol_version": manifest.get("protocol_version"),
        "task_id": manifest.get("task_id"),
        "conditions": manifest.get("conditions"),
        "minimum_agents_for_publication": manifest.get("minimum_agents_for_publication"),
        "agent_ids": agents,
        "reviewers_per_run": manifest.get("reviewers_per_run"),
    }
    if locked_protocol != expected_protocol:
        errors.append("freeze.lock.json protocol fields do not match manifest")

    frozen_inputs = [str(value) for value in manifest.get("frozen_inputs", [])]
    locked_files = lock.get("files", {})
    if not isinstance(locked_files, dict) or set(locked_files) != set(frozen_inputs):
        errors.append("freeze.lock.json paths do not exactly match manifest frozen_inputs")
    else:
        for relative in frozen_inputs:
            path = (repo_root / relative).resolve()
            try:
                path.relative_to(repo_root)
            except ValueError:
                errors.append(f"frozen input escapes repository: {relative}")
                continue
            if not path.is_file():
                errors.append(f"missing frozen input: {relative}")
            elif sha256(path) != str(locked_files.get(relative, "")):
                errors.append(f"frozen input hash mismatch: {relative}")

    if args.require_publication or manifest.get("status") == "complete":
        validate_publication(repo_root, manifest, lock, errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(
        f"PASS: cross-agent protocol v{manifest.get('protocol_version')} is frozen for "
        f"{len(agents)} planned agents; status={manifest.get('status')}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
