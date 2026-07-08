#!/usr/bin/env python3
"""Assert that known bad eval fixtures are caught by the offline runner."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from run_evals import evaluate_case, load_cases, load_sources


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evals-dir", default="evals")
    parser.add_argument("--fixtures-dir", default="evals/regression_fixtures")
    args = parser.parse_args()

    evals_dir = Path(args.evals_dir).resolve()
    fixtures_dir = Path(args.fixtures_dir).resolve()
    manifest_path = fixtures_dir / "manifest.json"
    manifest = read_json(manifest_path)
    cases_by_id = {case["case_id"]: case for case in load_cases(evals_dir / "cases")}
    sources_by_id = load_sources(evals_dir)

    failures: list[str] = []
    for fixture in manifest["fixtures"]:
        fixture_id = fixture["fixture_id"]
        case_id = fixture["case_id"]
        case = cases_by_id[case_id]
        run_dir = fixtures_dir / fixture_id / case_id
        result = evaluate_case(case, run_dir, sources_by_id)

        allowed_statuses = set(fixture.get("allowed_statuses", ["fail", "review"]))
        if result["status"] not in allowed_statuses:
            failures.append(
                f"{fixture_id}: expected status in {sorted(allowed_statuses)}, got {result['status']}"
            )

        for flag in fixture.get("expected_quality_flags", []):
            if flag not in result.get("quality_flags", []):
                failures.append(f"{fixture_id}: missing quality flag {flag}")

        for flag in fixture.get("expected_coverage_flags", []):
            if flag not in result.get("coverage_flags", []):
                failures.append(f"{fixture_id}: missing coverage flag {flag}")

        findings_text = "\n".join(result.get("findings", []))
        for needle in fixture.get("expected_findings_contains", []):
            if needle not in findings_text:
                failures.append(f"{fixture_id}: finding did not contain {needle!r}")

        print(
            f"{fixture_id}: {result['status']} "
            f"{result['score']}/{result['max_score']} "
            f"quality={result.get('quality_flags', [])} "
            f"coverage={result.get('coverage_flags', [])}"
        )

    if failures:
        print("\nRegression fixture failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
