#!/usr/bin/env python3
"""Assert that known-good fixture artifacts still pass the offline runner."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

from run_evals import evaluate_case, load_cases, load_sources


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evals-dir", default="evals")
    parser.add_argument("--fixtures-dir", default="evals/conformance_fixtures")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    evals_dir = (repo_root / args.evals_dir).resolve()
    fixtures_dir = (repo_root / args.fixtures_dir).resolve()
    manifest = read_json(fixtures_dir / "manifest.json")
    cases_by_id = {case["case_id"]: case for case in load_cases(evals_dir / "cases")}
    sources_by_id = load_sources(evals_dir)

    failures: list[str] = []
    for fixture in manifest["fixtures"]:
        fixture_id = fixture["fixture_id"]
        case_id = fixture["case_id"]
        case = cases_by_id[case_id]
        fixture_dir = fixtures_dir / fixture_id / case_id
        final_path = (repo_root / fixture["final_path"]).resolve()
        final_text = final_path.read_text(encoding="utf-8")

        mutation_results: list[tuple[dict[str, Any], dict[str, Any]]] = []
        with tempfile.TemporaryDirectory(prefix="irf-conformance-") as temp_dir:
            run_dir = Path(temp_dir) / case_id
            shutil.copytree(fixture_dir, run_dir)
            shutil.copy2(final_path, run_dir / "final.md")
            result = evaluate_case(case, run_dir, sources_by_id)

            progress_path = run_dir / "state" / "progress.json"
            original_progress = read_json(progress_path)
            for mutation in fixture.get("mutations", []):
                mutated_progress = dict(original_progress)
                mutated_progress.update(mutation.get("progress_updates", {}))
                progress_path.write_text(
                    json.dumps(mutated_progress, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                mutation_results.append((mutation, evaluate_case(case, run_dir, sources_by_id)))

        expected_status = fixture.get("expected_status", "pass")
        if result["status"] != expected_status:
            failures.append(f"{fixture_id}: expected {expected_status}, got {result['status']}")

        min_score = int(fixture.get("min_score", 80))
        if result["score"] < min_score:
            failures.append(f"{fixture_id}: expected score >= {min_score}, got {result['score']}")

        for flag in fixture.get("forbidden_quality_flags", []):
            if flag in result.get("quality_flags", []):
                failures.append(f"{fixture_id}: unexpected quality flag {flag}")

        for flag in fixture.get("forbidden_coverage_flags", []):
            if flag in result.get("coverage_flags", []):
                failures.append(f"{fixture_id}: unexpected coverage flag {flag}")

        for term in fixture.get("required_final_terms", []):
            if term not in final_text:
                failures.append(f"{fixture_id}: required final term was not preserved: {term!r}")

        for term in fixture.get("forbidden_final_terms", []):
            if term in final_text:
                failures.append(f"{fixture_id}: forbidden final term leaked: {term!r}")

        for mutation, mutation_result in mutation_results:
            mutation_id = mutation["mutation_id"]
            allowed_statuses = set(mutation.get("allowed_statuses", ["review", "fail"]))
            if mutation_result["status"] not in allowed_statuses:
                failures.append(
                    f"{fixture_id}/{mutation_id}: expected status in "
                    f"{sorted(allowed_statuses)}, got {mutation_result['status']}"
                )
            for flag in mutation.get("expected_quality_flags", []):
                if flag not in mutation_result.get("quality_flags", []):
                    failures.append(
                        f"{fixture_id}/{mutation_id}: missing quality flag {flag}"
                    )
            print(
                f"{fixture_id}/{mutation_id}: {mutation_result['status']} "
                f"{mutation_result['score']}/{mutation_result['max_score']} "
                f"quality={mutation_result.get('quality_flags', [])}"
            )

        print(
            f"{fixture_id}: {result['status']} "
            f"{result['score']}/{result['max_score']} "
            f"quality={result.get('quality_flags', [])} "
            f"coverage={result.get('coverage_flags', [])}"
        )

    if failures:
        print("\nConformance fixture failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
