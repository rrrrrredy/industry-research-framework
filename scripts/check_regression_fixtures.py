#!/usr/bin/env python3
"""Assert that known bad eval fixtures are caught by the offline runner."""

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
    parser.add_argument("--fixtures-dir", default="evals/regression_fixtures")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    evals_dir = (repo_root / args.evals_dir).resolve()
    fixtures_dir = (repo_root / args.fixtures_dir).resolve()
    manifest_path = fixtures_dir / "manifest.json"
    manifest = read_json(manifest_path)
    cases_by_id = {case["case_id"]: case for case in load_cases(evals_dir / "cases")}
    sources_by_id = load_sources(evals_dir)

    failures: list[str] = []
    for fixture in manifest["fixtures"]:
        fixture_id = fixture["fixture_id"]
        case_id = fixture["case_id"]
        case = dict(cases_by_id[case_id])
        case.update(fixture.get("case_overrides", {}))
        fixture_dir = fixtures_dir / fixture_id / case_id
        with tempfile.TemporaryDirectory(prefix="irf-regression-") as temp_dir:
            run_dir = Path(temp_dir) / case_id
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

            for relative, content in fixture.get("write_files", {}).items():
                target = (run_dir / str(relative)).resolve()
                target.relative_to(run_dir.resolve())
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(str(content), encoding="utf-8")

            for relative, content in fixture.get("append_files", {}).items():
                target = (run_dir / str(relative)).resolve()
                target.relative_to(run_dir.resolve())
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("a", encoding="utf-8", newline="") as f:
                    f.write(str(content))

            final_path = fixture.get("final_path")
            if final_path:
                shutil.copy2((repo_root / final_path).resolve(), run_dir / "final.md")
            generated_final = fixture.get("generated_final")
            if generated_final:
                prefix = str(generated_final.get("prefix", ""))
                sentence = str(generated_final.get("repeat_sentence", ""))
                repeat_count = int(generated_final.get("repeat_count", 0))
                (run_dir / "final.md").write_text(
                    prefix + sentence * repeat_count,
                    encoding="utf-8",
                )
            append_final_text = fixture.get("append_final_text")
            if append_final_text:
                with (run_dir / "final.md").open("a", encoding="utf-8", newline="") as f:
                    f.write(str(append_final_text))

            result = evaluate_case(case, run_dir, sources_by_id)

        allowed_statuses = set(fixture.get("allowed_statuses", ["fail", "review"]))
        if result["conformance_status"] not in allowed_statuses:
            failures.append(
                f"{fixture_id}: expected status in {sorted(allowed_statuses)}, got {result['conformance_status']}"
            )

        for flag in fixture.get("expected_conformance_flags", []):
            if flag not in result.get("conformance_flags", []):
                failures.append(f"{fixture_id}: missing conformance flag {flag}")

        for flag in fixture.get("expected_coverage_flags", []):
            if flag not in result.get("coverage_flags", []):
                failures.append(f"{fixture_id}: missing coverage flag {flag}")

        findings_text = "\n".join(result.get("findings", []))
        for needle in fixture.get("expected_findings_contains", []):
            if needle not in findings_text:
                failures.append(f"{fixture_id}: finding did not contain {needle!r}")

        print(
            f"{fixture_id}: {result['conformance_status']} "
            f"{result['conformance_score']}/{result['max_conformance_score']} "
            f"conformance={result.get('conformance_flags', [])} "
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
