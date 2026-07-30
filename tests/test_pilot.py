from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
PILOT_PATH = ROOT / "scripts" / "pilot.py"
FAKE_ADAPTER_PATH = ROOT / "evals" / "pilot" / "fake_adapter.py"

spec = importlib.util.spec_from_file_location("industry_research_pilot", PILOT_PATH)
pilot = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = pilot
spec.loader.exec_module(pilot)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def make_fixture(repo_root: Path) -> Path:
    (repo_root / "evals" / "cases").mkdir(parents=True)
    pack_root = repo_root / "evals" / "source_packs" / "test_pack"
    pack_root.mkdir(parents=True)
    pilot_root = repo_root / "evals" / "pilot"
    pilot_root.mkdir(parents=True)

    (repo_root / "SKILL.md").write_text(
        "# Frozen framework\n\nUse evidence carefully.\n",
        encoding="utf-8",
    )
    rubric = {
        "rubric_id": "neutral",
        "input_boundary": "Review final.md only.",
        "reviewers_per_submission": 2,
        "scale": {"min": 1, "max": 5},
        "dimensions": [
            {"name": "evidence"},
            {"name": "synthesis"},
        ],
    }
    write_json(pilot_root / "rubric.json", rubric)
    write_json(
        pack_root / "manifest.json",
        {"source_pack_id": "test_pack", "source_ids": ["S001", "S002"]},
    )
    (pack_root / "sources.jsonl").write_text(
        json.dumps(
            {"source_id": "S001", "title": "Source one", "content": "Evidence one"},
            sort_keys=True,
        )
        + "\n"
        + json.dumps(
            {"source_id": "S002", "title": "Source two", "content": "Evidence two"},
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    case_paths: list[str] = []
    for index in (1, 2):
        case_path = repo_root / "evals" / "cases" / f"case_{index}.json"
        write_json(
            case_path,
            {
                "case_id": f"case_{index}",
                "title": f"Case {index}",
                "task_type": "industry_report",
                "language": "en",
                "prompt": f"Analyze market {index}.",
                "target_reader": "strategy readers",
                "expected_depth": "short pilot report",
                "must_cover_entities": ["Example"],
                "required_sections": ["Judgment", "Evidence", "Risks"],
                "source_pack": "test_pack",
                "source_ids": ["S001", "S002"],
                "artifact_requirements": ["state/progress.json"],
                "quality_focus": ["framework_specific_field"],
            },
        )
        case_paths.append(case_path.relative_to(repo_root).as_posix())

    protocol = {
        "protocol_version": "1.0",
        "study_id": "fixture_pilot",
        "status": "preregistered_no_live_runs",
        "claim_boundary": "Synthetic plumbing only; no efficacy claim.",
        "cases": case_paths,
        "replicates": 2,
        "randomization_seed": 7,
        "conditions": ["baseline", "treatment"],
        "skill_path": "SKILL.md",
        "rubric_path": "evals/pilot/rubric.json",
        "source_pack_root": "evals/source_packs",
        "model": {
            "snapshot": "SET_DATED_MODEL_SNAPSHOT",
            "snapshot_kind": "placeholder",
            "temperature": 0,
            "seed": 7,
        },
        "adapter": {
            "interface_version": "pilot-adapter-v1",
            "transport": "subprocess_json_stdin_stdout",
            "identity_kind": "placeholder",
            "expected_identity_sha256": "SET_ADAPTER_IDENTITY",
        },
        "primary_outcome": {
            "input": "final.md only",
            "reviewers_per_submission": 2,
            "rubric": "evals/pilot/rubric.json",
        },
        "failure_policy": {
            "retain_every_attempt": True,
            "retry_limit": 1,
        },
        "isolation": {
            "fresh_session_per_run": True,
            "fresh_workspace_per_run": True,
            "harness_verification": "not_available_for_subprocess_transport",
        },
    }
    protocol_path = pilot_root / "protocol.json"
    write_json(protocol_path, protocol)
    return protocol_path


def model_input_without_framework(request: dict[str, object]) -> dict[str, object]:
    model_input = dict(request["model_input"])
    model_input.pop("framework_instruction", None)
    return model_input


class PilotPreparationTests(unittest.TestCase):
    def test_prepare_is_deterministic_and_isolates_baseline(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            protocol_path = make_fixture(repo_root)
            first_output = repo_root / "first"
            second_output = repo_root / "second"
            with mock.patch.object(pilot, "git_commit", return_value="a" * 40):
                first = pilot.prepare_pilot(repo_root, protocol_path, first_output)
                second = pilot.prepare_pilot(repo_root, protocol_path, second_output)
                first_errors = pilot.verify_manifest(
                    repo_root,
                    first_output / "manifest.json",
                )
                second_errors = pilot.verify_manifest(
                    repo_root,
                    second_output / "manifest.json",
                )

            self.assertEqual(first, second)
            self.assertEqual(first_errors, [])
            self.assertEqual(second_errors, [])
            self.assertEqual(len(first["runs"]), 8)

            pairs: dict[str, list[dict[str, object]]] = {}
            for entry in first["runs"]:
                pairs.setdefault(entry["pair_id"], []).append(entry)
                workspace = first_output / entry["workspace_path"]
                workspace_names = {
                    path.name for path in workspace.iterdir() if path.is_file()
                }
                self.assertNotIn("rubric.json", workspace_names)
                self.assertFalse(any("anchor" in name for name in workspace_names))
                if entry["condition"] == "baseline":
                    self.assertEqual(
                        workspace_names,
                        {"task.json", "sources.jsonl", "output_contract.md"},
                    )
                else:
                    self.assertEqual(
                        workspace_names,
                        {
                            "task.json",
                            "sources.jsonl",
                            "output_contract.md",
                            "framework.md",
                        },
                    )

            for pair_entries in pairs.values():
                by_condition = {
                    entry["condition"]: json.loads(
                        (
                            first_output / entry["request_path"]
                        ).read_text(encoding="utf-8")
                    )
                    for entry in pair_entries
                }
                self.assertNotIn(
                    "framework_instruction",
                    by_condition["baseline"]["model_input"],
                )
                self.assertIn(
                    "framework_instruction",
                    by_condition["treatment"]["model_input"],
                )
                self.assertEqual(
                    model_input_without_framework(by_condition["baseline"]),
                    model_input_without_framework(by_condition["treatment"]),
                )
                self.assertNotIn("condition", by_condition["baseline"])
                self.assertNotIn("condition", by_condition["treatment"])

    def test_verify_rejects_each_frozen_input_change(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            protocol_path = make_fixture(repo_root)
            output_dir = repo_root / "prepared"
            with mock.patch.object(pilot, "git_commit", return_value="a" * 40):
                manifest = pilot.prepare_pilot(repo_root, protocol_path, output_dir)
                for relative_name in (
                    "SKILL.md",
                    "evals/pilot/rubric.json",
                    "evals/cases/case_1.json",
                    "evals/source_packs/test_pack/sources.jsonl",
                ):
                    with self.subTest(relative_name=relative_name):
                        path = repo_root / relative_name
                        original = path.read_bytes()
                        path.write_bytes(original + b"\n")
                        errors = pilot.verify_manifest(
                            repo_root,
                            output_dir / "manifest.json",
                        )
                        path.write_bytes(original)
                        self.assertIn(
                            f"input hash changed: {relative_name}",
                            errors,
                        )
                self.assertEqual(manifest["repo_commit"], "a" * 40)

    def test_verify_rejects_non_allowlisted_pair_difference(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            protocol_path = make_fixture(repo_root)
            output_dir = repo_root / "prepared"
            with mock.patch.object(pilot, "git_commit", return_value="a" * 40):
                manifest = pilot.prepare_pilot(repo_root, protocol_path, output_dir)
                treatment = next(
                    entry
                    for entry in manifest["runs"]
                    if entry["condition"] == "treatment"
                )
                request_path = output_dir / treatment["request_path"]
                request = json.loads(request_path.read_text(encoding="utf-8"))
                request["model_input"]["task"]["prompt"] = "Changed prompt"
                write_json(request_path, request)
                errors = pilot.verify_manifest(
                    repo_root,
                    output_dir / "manifest.json",
                )

            self.assertIn(
                f"request differs from frozen inputs: {treatment['run_id']}",
                errors,
            )
            self.assertEqual(
                errors,
                [f"request differs from frozen inputs: {treatment['run_id']}"],
            )

    def test_verify_rejects_manifest_model_upgrade(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            protocol_path = make_fixture(repo_root)
            output_dir = repo_root / "prepared"
            with mock.patch.object(pilot, "git_commit", return_value="a" * 40):
                pilot.prepare_pilot(repo_root, protocol_path, output_dir)
                manifest_path = output_dir / "manifest.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest["model"] = {
                    "snapshot": "dated-model-2026-07-30",
                    "snapshot_kind": "dated",
                    "temperature": 0,
                    "seed": 7,
                }
                write_json(manifest_path, manifest)
                errors = pilot.verify_manifest(repo_root, manifest_path)

            self.assertIn(
                "manifest model differs from frozen protocol",
                errors,
            )


class PilotAttemptTests(unittest.TestCase):
    def test_adapter_isolation_attestation_cannot_make_subprocess_confirmatory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            protocol_path = make_fixture(repo_root)
            output_dir = repo_root / "prepared"
            attempts_dir = repo_root / "attempts"
            adapter_path = repo_root / "repo_reading_adapter.py"
            adapter_path.write_text(
                "import json, sys\n"
                "from pathlib import Path\n"
                "request = json.load(sys.stdin)\n"
                f"leaked = Path({str(repo_root / 'SKILL.md')!r}).read_text()\n"
                "model = request['model']\n"
                "sampling = {k: v for k, v in model.items() "
                "if k not in {'snapshot', 'snapshot_kind'}}\n"
                "json.dump({\n"
                "  'interface_version': 'pilot-adapter-v1',\n"
                "  'status': 'completed',\n"
                "  'final_text': 'REPO_READ=' + leaked.splitlines()[0],\n"
                "  'metadata': {\n"
                "    'provider': 'claimed-provider',\n"
                "    'request_id': 'claimed-request',\n"
                "    'actual_model': model['snapshot'],\n"
                "    'system_fingerprint': 'claimed-fingerprint',\n"
                "    'seed_supported': True,\n"
                "    'isolation_attestation': True,\n"
                "    'synthetic': False,\n"
                "    'adapter_version': 'claimed-v1',\n"
                "    'actual_sampling': sampling,\n"
                "    'usage': {},\n"
                "    'stop_reason': 'stop',\n"
                "    'tool_transcript': [{'headers': [\n"
                "      ['x-api-key', 'TOOL-SECRET']]}]},\n"
                "  'provider_request': {'headers': [\n"
                "    ['x-api-key', 'ANTHROPIC-SECRET'],\n"
                "    ['authorization', 'Basic dXNlcjpwYXNz']],\n"
                "    'requestHeaders': [{'name': 'x-api-key',\n"
                "      'value': 'CAMEL-SECRET'}],\n"
                "    'header_pairs': [['x-api-key', 'PAIR-SECRET']],\n"
                "    'headers_list': [{'name': 'x-api-key',\n"
                "      'value': 'LIST-SECRET'}],\n"
                "    'url': 'https://example.test/run?api_key=QUERY-SECRET'},\n"
                "  'provider_response': {'headers': [\n"
                "    ['set-cookie', 'SESSION-SECRET']],\n"
                "    'diagnostic': 'Authorization: Basic dXNlcjpwYXNzdw'}}, "
                "sys.stdout)\n",
                encoding="utf-8",
            )
            with mock.patch.object(pilot, "git_commit", return_value="a" * 40):
                manifest = pilot.prepare_pilot(repo_root, protocol_path, output_dir)
                baseline = next(
                    entry
                    for entry in manifest["runs"]
                    if entry["condition"] == "baseline"
                )
                record = pilot.dispatch_run(
                    repo_root,
                    output_dir / "manifest.json",
                    attempts_dir,
                    baseline["run_id"],
                    [sys.executable, str(adapter_path)],
                )

            self.assertEqual(record["status"], "completed")
            self.assertEqual(record["evidence_grade"], "exploratory")
            self.assertIn(
                "subprocess isolation is not verified by the harness",
                record["evidence_grade_reasons"],
            )
            self.assertTrue(
                record["response"]["final_text"].startswith("REPO_READ=")
            )
            persisted = json.dumps(record, ensure_ascii=False)
            for secret in (
                "ANTHROPIC-SECRET",
                "CAMEL-SECRET",
                "PAIR-SECRET",
                "LIST-SECRET",
                "TOOL-SECRET",
                "dXNlcjpwYXNz",
                "dXNlcjpwYXNzdw",
                "QUERY-SECRET",
                "SESSION-SECRET",
            ):
                self.assertNotIn(secret, persisted)
            self.assertEqual(
                record["response"]["provider_request"]["headers"],
                "[REDACTED]",
            )
            for key in ("requestHeaders", "header_pairs", "headers_list"):
                self.assertEqual(
                    record["response"]["provider_request"][key],
                    "[REDACTED]",
                )
            self.assertEqual(
                record["response"]["metadata"]["tool_transcript"][0]["headers"],
                "[REDACTED]",
            )

    def test_failed_adapter_stderr_header_is_redacted(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            protocol_path = make_fixture(repo_root)
            output_dir = repo_root / "prepared"
            attempts_dir = repo_root / "attempts"
            adapter_path = repo_root / "failing_adapter.py"
            adapter_path.write_text(
                "import sys\n"
                "print('x-api-key: STDERR-SECRET', file=sys.stderr)\n"
                "raise SystemExit(1)\n",
                encoding="utf-8",
            )
            with mock.patch.object(pilot, "git_commit", return_value="a" * 40):
                manifest = pilot.prepare_pilot(repo_root, protocol_path, output_dir)
                record = pilot.dispatch_run(
                    repo_root,
                    output_dir / "manifest.json",
                    attempts_dir,
                    manifest["runs"][0]["run_id"],
                    [sys.executable, str(adapter_path)],
                )

            self.assertEqual(record["status"], "failed")
            self.assertNotIn(
                "STDERR-SECRET",
                json.dumps(record, ensure_ascii=False),
            )
            self.assertIn("x-api-key: [REDACTED]", record["stderr"])

    def test_failed_attempt_and_retry_are_both_retained(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            protocol_path = make_fixture(repo_root)
            output_dir = repo_root / "prepared"
            attempts_dir = repo_root / "attempts"
            with mock.patch.object(pilot, "git_commit", return_value="a" * 40):
                manifest = pilot.prepare_pilot(repo_root, protocol_path, output_dir)
                run_id = manifest["runs"][0]["run_id"]
                failed = pilot.dispatch_run(
                    repo_root,
                    output_dir / "manifest.json",
                    attempts_dir,
                    run_id,
                    [str(repo_root / "missing-adapter")],
                )
                completed = pilot.dispatch_run(
                    repo_root,
                    output_dir / "manifest.json",
                    attempts_dir,
                    run_id,
                    [sys.executable, str(FAKE_ADAPTER_PATH)],
                )
                with self.assertRaises(pilot.PilotError):
                    pilot.dispatch_run(
                        repo_root,
                        output_dir / "manifest.json",
                        attempts_dir,
                        run_id,
                        [sys.executable, str(FAKE_ADAPTER_PATH)],
                    )

            self.assertEqual(failed["status"], "failed")
            self.assertTrue(
                any(
                    "adapter could not start" in error
                    for error in failed["validation_errors"]
                )
            )
            self.assertEqual(completed["status"], "completed")
            self.assertEqual(completed["evidence_grade"], "exploratory")
            self.assertIn(
                "adapter response is synthetic",
                completed["evidence_grade_reasons"],
            )
            self.assertIn(
                "model snapshot is not declared as dated",
                completed["evidence_grade_reasons"],
            )
            self.assertIn(
                "pilot inputs were prepared from a dirty worktree",
                completed["evidence_grade_reasons"],
            )
            self.assertIn(
                "subprocess isolation is not verified by the harness",
                completed["evidence_grade_reasons"],
            )
            self.assertIn(
                "adapter identity is not frozen",
                completed["evidence_grade_reasons"],
            )
            attempt_paths = sorted((attempts_dir / run_id).glob("attempt-*.json"))
            self.assertEqual(
                [path.name for path in attempt_paths],
                ["attempt-001.json", "attempt-002.json"],
            )
            self.assertEqual(
                completed["previous_attempt_sha256"],
                pilot.sha256_file(attempt_paths[0]),
            )

    def test_blind_export_rejects_flipped_conditions_before_writing_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            protocol_path = make_fixture(repo_root)
            output_dir = repo_root / "prepared"
            blind_dir = repo_root / "blind"
            with mock.patch.object(pilot, "git_commit", return_value="a" * 40):
                pilot.prepare_pilot(repo_root, protocol_path, output_dir)

            manifest_path = output_dir / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            for entry in manifest["runs"]:
                entry["condition"] = (
                    "treatment"
                    if entry["condition"] == "baseline"
                    else "baseline"
                )
            write_json(manifest_path, manifest)

            with self.assertRaisesRegex(
                pilot.PilotError,
                "manifest does not match its preparation commitment",
            ):
                pilot.create_blind_export(
                    repo_root,
                    manifest_path,
                    repo_root / "attempts",
                    blind_dir,
                )
            self.assertFalse(blind_dir.exists())

    def test_blind_export_rejects_attempts_from_another_study(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            protocol_path = make_fixture(repo_root)
            output_dir = repo_root / "prepared"
            attempts_dir = repo_root / "foreign-attempts"
            blind_dir = repo_root / "blind"
            with mock.patch.object(pilot, "git_commit", return_value="a" * 40):
                manifest = pilot.prepare_pilot(repo_root, protocol_path, output_dir)

            run_id = manifest["runs"][0]["run_id"]
            write_json(
                attempts_dir / run_id / "attempt-001.json",
                {
                    "attempt_record_version": "pilot-attempt-v1",
                    "run_id": run_id,
                    "attempt": 1,
                    "previous_attempt_sha256": None,
                    "status": "completed",
                    "request_sha256": "0" * 64,
                    "request": {"foreign": "request"},
                    "response": {
                        "interface_version": "pilot-adapter-v1",
                        "status": "completed",
                        "final_text": "FOREIGN STUDY OUTPUT",
                        "metadata": {},
                    },
                },
            )

            with mock.patch.object(pilot, "git_commit", return_value="a" * 40):
                with self.assertRaises(pilot.PilotError) as raised:
                    pilot.create_blind_export(
                        repo_root,
                        output_dir / "manifest.json",
                        attempts_dir,
                        blind_dir,
                    )
            message = str(raised.exception)
            self.assertIn("request hash does not match manifest", message)
            self.assertIn("persisted request does not match manifest", message)
            self.assertFalse(blind_dir.exists())

    def test_blind_export_hides_labels_and_score_lock_needs_two_reviewers(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            protocol_path = make_fixture(repo_root)
            output_dir = repo_root / "prepared"
            attempts_dir = repo_root / "attempts"
            blind_dir = repo_root / "blind"
            with mock.patch.object(pilot, "git_commit", return_value="a" * 40):
                manifest = pilot.prepare_pilot(repo_root, protocol_path, output_dir)
                for entry in manifest["runs"]:
                    pilot.dispatch_run(
                        repo_root,
                        output_dir / "manifest.json",
                        attempts_dir,
                        entry["run_id"],
                        [sys.executable, str(FAKE_ADAPTER_PATH)],
                    )

            with mock.patch.object(pilot, "git_commit", return_value="a" * 40):
                submissions_path, keys_path, accounting_path, commitment_path = (
                    pilot.create_blind_export(
                        repo_root,
                        output_dir / "manifest.json",
                        attempts_dir,
                        blind_dir,
                    )
                )
            submissions_text = submissions_path.read_text(encoding="utf-8")
            self.assertNotIn('"condition"', submissions_text)
            self.assertNotIn('"run_id"', submissions_text)
            self.assertNotIn("framework_instruction", submissions_text)
            self.assertNotIn('"status"', submissions_text)
            self.assertNotIn('"attempt_count"', submissions_text)
            self.assertNotIn('"had_failed_attempt"', submissions_text)
            accounting_text = accounting_path.read_text(encoding="utf-8")
            self.assertIn('"attempt_count":1', accounting_text)
            self.assertIn('"had_failed_attempt":false', accounting_text)
            keys = json.loads(keys_path.read_text(encoding="utf-8"))
            self.assertEqual(
                {row["condition"] for row in keys["rows"]},
                {"baseline", "treatment"},
            )
            commitment = json.loads(commitment_path.read_text(encoding="utf-8"))
            self.assertEqual(
                commitment["keys_sha256"],
                pilot.sha256_file(keys_path),
            )

            submissions = pilot.load_jsonl(submissions_path)
            scores_path = repo_root / "scores.jsonl"
            scores: list[dict[str, object]] = []
            one_reviewer_scores: list[dict[str, object]] = []
            for submission in submissions:
                for reviewer_id in ("reviewer-1", "reviewer-2"):
                    row = {
                        "submission_id": submission["submission_id"],
                        "reviewer_id": reviewer_id,
                        "scores": {"evidence": 3, "synthesis": 4},
                    }
                    scores.append(row)
                    if reviewer_id == "reviewer-1":
                        one_reviewer_scores.append(row)
            pilot.write_jsonl(scores_path, one_reviewer_scores)
            with self.assertRaises(pilot.PilotError):
                pilot.lock_scores(
                    repo_root / "evals" / "pilot" / "rubric.json",
                    submissions_path,
                    commitment_path,
                    scores_path,
                    repo_root / "incomplete-score-lock.json",
                )
            extra_reviewer_scores = scores + [
                {
                    "submission_id": submission["submission_id"],
                    "reviewer_id": "reviewer-3",
                    "scores": {"evidence": 3, "synthesis": 4},
                }
                for submission in submissions
            ]
            pilot.write_jsonl(scores_path, extra_reviewer_scores)
            with self.assertRaises(pilot.PilotError):
                pilot.lock_scores(
                    repo_root / "evals" / "pilot" / "rubric.json",
                    submissions_path,
                    commitment_path,
                    scores_path,
                    repo_root / "extra-reviewer-score-lock.json",
                )
            pilot.write_jsonl(scores_path, scores)
            lock_path = repo_root / "score-lock.json"
            lock = pilot.lock_scores(
                repo_root / "evals" / "pilot" / "rubric.json",
                submissions_path,
                commitment_path,
                scores_path,
                lock_path,
            )

            self.assertEqual(lock["completed_submissions"], 8)
            self.assertEqual(lock["score_rows"], 16)
            self.assertFalse(lock["condition_labels_included"])
            original_keys = keys_path.read_bytes()
            keys_path.write_bytes(original_keys + b"\n")
            self.assertNotEqual(
                commitment["keys_sha256"],
                pilot.sha256_file(keys_path),
            )
            with self.assertRaises(pilot.PilotError):
                pilot.lock_scores(
                    repo_root / "evals" / "pilot" / "rubric.json",
                    submissions_path,
                    commitment_path,
                    scores_path,
                    lock_path,
                )

    def test_redaction_removes_credentials_without_erasing_usage_tokens(self):
        redacted = pilot.redact_adapter_response(
            {
                "api_key": "sk-secretvalue",
                "authorization": "Bearer secretvalue",
                "usage": {"input_tokens": 12, "output_tokens": 4},
                "message": "Bearer anothersecret",
                "basic_message": "Basic dXNlcjpwYXNz",
                "unpadded_basic_message": "Basic dXNlcjpwYXNzdw",
                "ordinary_text": "Basic research methods",
                "ordinary_list": ["token", "ordinary-label"],
                "final_text": (
                    "Authorization: policy design matters for enterprise agents."
                ),
                "provider_request": {
                    "headers": {
                        "x-api-key": "ANTHROPIC-SECRET",
                        "api-key": "AZURE-SECRET",
                        "x-goog-api-key": "GOOGLE-SECRET",
                        "proxy-authorization": "PROXY-SECRET",
                        "client-secret": "CLIENT-SECRET",
                        "id-token": "ID-SECRET",
                        "cookie": "SESSION-SECRET",
                        "set-cookie": "RESPONSE-SECRET",
                    },
                    "url": (
                        "https://example.test/run?"
                        "api_key=QUERY-SECRET&x=1"
                    ),
                    "request_headers": [
                        ["x-api-key", "PAIR-SECRET"],
                        ["authorization", "Basic dXNlcjpwYXNz"],
                        {
                            "name": "x-goog-api-key",
                            "value": "OBJECT-SECRET",
                        },
                        "client-secret: LINE-SECRET",
                        "accept: Basic research methods",
                    ],
                    "requestHeaders": [
                        {
                            "name": "x-api-key",
                            "value": "CAMEL-SECRET",
                        }
                    ],
                    "header_pairs": [["x-api-key", "PAIR-SECRET"]],
                    "headers_list": [
                        {
                            "name": "x-api-key",
                            "value": "LIST-SECRET",
                        }
                    ],
                },
            }
        )

        self.assertEqual(redacted["api_key"], "[REDACTED]")
        self.assertEqual(redacted["authorization"], "[REDACTED]")
        self.assertEqual(
            redacted["usage"],
            {"input_tokens": 12, "output_tokens": 4},
        )
        self.assertEqual(redacted["message"], "Bearer [REDACTED]")
        self.assertEqual(redacted["basic_message"], "Basic [REDACTED]")
        self.assertEqual(
            redacted["unpadded_basic_message"],
            "Basic [REDACTED]",
        )
        self.assertEqual(redacted["ordinary_text"], "Basic research methods")
        self.assertEqual(
            redacted["ordinary_list"],
            ["token", "ordinary-label"],
        )
        self.assertEqual(
            redacted["final_text"],
            "Authorization: policy design matters for enterprise agents.",
        )
        self.assertEqual(
            redacted["provider_request"]["headers"],
            "[REDACTED]",
        )
        self.assertEqual(
            redacted["provider_request"]["url"],
            "https://example.test/run?api_key=[REDACTED]&x=1",
        )
        self.assertEqual(
            redacted["provider_request"]["request_headers"],
            "[REDACTED]",
        )
        for key in ("requestHeaders", "header_pairs", "headers_list"):
            self.assertEqual(
                redacted["provider_request"][key],
                "[REDACTED]",
            )
        request = {
            "model_input": {
                "sources": [{"header": "Market overview"}],
            }
        }
        self.assertEqual(pilot.redact_value(request), request)
        for argument in (
            "--api-key=plainsecret",
            "--token=plainsecret",
            "--authorization=Bearer plainsecret",
            "--x-api-key=plainsecret",
            "--x-goog-api-key=plainsecret",
            "https://example.test/run?client_secret=plainsecret",
        ):
            with self.subTest(argument=argument):
                with self.assertRaises(pilot.PilotError):
                    pilot.validate_adapter_command(["adapter", argument])


if __name__ == "__main__":
    unittest.main()
