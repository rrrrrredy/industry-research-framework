#!/usr/bin/env python3
"""Assert that known-good fixture artifacts still pass the offline runner."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import subprocess
import sys
from pathlib import Path
from typing import Any

from check_delivery import sha256_file
from run_evals import evaluate_case, load_cases, load_sources


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def assemble_fixture(repo_root: Path, fixture: dict[str, Any], fixture_dir: Path, run_dir: Path) -> None:
    base_fixture = fixture.get("base_fixture")
    if base_fixture:
        shutil.copytree((repo_root / base_fixture).resolve(), run_dir)
        if fixture_dir.exists():
            shutil.copytree(fixture_dir, run_dir, dirs_exist_ok=True)
    elif fixture_dir.exists():
        shutil.copytree(fixture_dir, run_dir)
    else:
        run_dir.mkdir(parents=True)

    for relative in fixture.get("remove_paths", []):
        target = (run_dir / str(relative)).resolve()
        target.relative_to(run_dir.resolve())
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()



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
    with tempfile.TemporaryDirectory(prefix="irf-hash-conformance-") as temp_dir:
        temp_root = Path(temp_dir)
        lf_path = temp_root / "lf.txt"
        crlf_path = temp_root / "crlf.txt"
        lf_path.write_bytes(b"alpha\nbeta\n")
        crlf_path.write_bytes(b"alpha\r\nbeta\r\n")
        if sha256_file(lf_path) != sha256_file(crlf_path):
            failures.append(
                "delivery hash portability: LF and CRLF text produced different canonical hashes"
            )

    for fixture in manifest["fixtures"]:
        fixture_id = fixture["fixture_id"]
        case_id = fixture["case_id"]
        case = dict(cases_by_id[case_id])
        case.update(fixture.get("case_overrides", {}))
        fixture_dir = fixtures_dir / fixture_id / case_id
        final_path = (repo_root / fixture["final_path"]).resolve()
        final_text = final_path.read_text(encoding="utf-8")

        mutation_results: list[tuple[dict[str, Any], dict[str, Any]]] = []
        delivery_cli_result: subprocess.CompletedProcess[str] | None = None
        with tempfile.TemporaryDirectory(prefix="irf-conformance-") as temp_dir:
            run_dir = Path(temp_dir) / case_id
            assemble_fixture(repo_root, fixture, fixture_dir, run_dir)
            shutil.copy2(final_path, run_dir / "final.md")
            result = evaluate_case(case, run_dir, sources_by_id)
            if fixture.get("check_delivery_cli"):
                delivery_cli_result = subprocess.run(
                    [sys.executable, str(repo_root / "scripts" / "check_delivery.py"), str(run_dir)],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    check=False,
                )

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
        if result["conformance_status"] != expected_status:
            failures.append(
                f"{fixture_id}: expected {expected_status}, got {result['conformance_status']}"
            )

        min_score = int(fixture.get("min_score", 80))
        if result["conformance_score"] < min_score:
            failures.append(
                f"{fixture_id}: expected score >= {min_score}, got {result['conformance_score']}"
            )

        if fixture.get("check_delivery_cli") and (
            delivery_cli_result is None
            or delivery_cli_result.returncode != 0
            or "PASS:" not in delivery_cli_result.stdout
        ):
            output = "" if delivery_cli_result is None else (delivery_cli_result.stdout + delivery_cli_result.stderr)
            failures.append(f"{fixture_id}: standalone delivery CLI did not emit PASS: {output.strip()}")

        for flag in fixture.get("forbidden_conformance_flags", []):
            if flag in result.get("conformance_flags", []):
                failures.append(f"{fixture_id}: unexpected conformance flag {flag}")

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
            if mutation_result["conformance_status"] not in allowed_statuses:
                failures.append(
                    f"{fixture_id}/{mutation_id}: expected status in "
                    f"{sorted(allowed_statuses)}, got {mutation_result['conformance_status']}"
                )
            for flag in mutation.get("expected_conformance_flags", []):
                if flag not in mutation_result.get("conformance_flags", []):
                    failures.append(
                        f"{fixture_id}/{mutation_id}: missing conformance flag {flag}"
                    )
            print(
                f"{fixture_id}/{mutation_id}: {mutation_result['conformance_status']} "
                f"{mutation_result['conformance_score']}/{mutation_result['max_conformance_score']} "
                f"conformance={mutation_result.get('conformance_flags', [])}"
            )

        print(
            f"{fixture_id}: {result['conformance_status']} "
            f"{result['conformance_score']}/{result['max_conformance_score']} "
            f"conformance={result.get('conformance_flags', [])} "
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
