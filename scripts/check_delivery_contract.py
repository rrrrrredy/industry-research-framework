#!/usr/bin/env python3
"""Isolated delivery regressions: reseal unrelated inputs so stale hashes cannot mask defects."""
from __future__ import annotations

import itertools
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import check_delivery as checker

REPO = Path(__file__).resolve().parents[1]
BASE = REPO / "evals/conformance_fixtures/known_good_model_company_pipeline_zh/model_company_pipeline_long_horizon_zh"
FINAL = REPO / "evals/taste_anchors/model_company_pipeline_long_horizon_zh/high_quality.md"


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def seal(root: Path, message: str = "delivery_message.md") -> None:
    receipt_path = root / "state/final_delivery.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    paths = ["final.md", *[p for p in checker.REQUIRED_HASH_INPUTS if p != "delivery_message.md"], message]
    paths += [p for p in checker.OPTIONAL_HASH_INPUTS if (root / p).is_file()]
    receipt["artifacts"] = {p: checker.sha256_file(root / p) for p in paths}
    write_json(receipt_path, receipt)


class DeliveryContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="irf-delivery-contract-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "task"
        shutil.copytree(BASE, self.root)
        shutil.copyfile(FINAL, self.root / "final.md")
        seal(self.root)

    def evaluate(self, **kwargs):
        return checker.evaluate_delivery(self.root, **kwargs)

    def progress(self, **updates):
        path = self.root / "state/progress.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        value.update(updates)
        write_json(path, value)

    def append_review(self, row):
        with (self.root / "logs/review.jsonl").open("a", encoding="utf-8") as output:
            output.write(json.dumps(row, ensure_ascii=False) + "\n")

    def assert_flag(self, expected, **kwargs):
        result = self.evaluate(**kwargs)
        self.assertFalse(result["ok"], result)
        self.assertIn(expected, result["flags"], result)
        self.assertNotIn("stale_delivery_receipt", result["flags"], result)
        return result

    def test_known_good(self):
        self.assertTrue(self.evaluate()["ok"])

    def test_honest_nonfinal(self):
        self.progress(stage="review", status="in_progress")
        (self.root / "delivery_message.md").write_text("这是阶段稿，尚未完成。\n", encoding="utf-8")
        seal(self.root)
        self.assertTrue(self.evaluate()["ok"])

    def test_late_global_failure(self):
        self.append_review({"scope": "full_report", "result": "needs_revision", "issues": ["late blocker"]})
        seal(self.root)
        self.assert_flag("insufficient_final_review_scope")

    def test_pass_with_open_issues(self):
        self.append_review({"scope": "global_final_delivery", "result": "PASS", "issues": ["still open"]})
        seal(self.root)
        self.assert_flag("insufficient_final_review_scope")

    def test_routed_action_alone_does_not_close_review_issue(self):
        self.append_review({"scope": "full_report", "result": "PASS", "issues": [
            {"id": "R1", "routed_action": "Recheck the missing source next"}
        ]})
        seal(self.root)
        self.assert_flag("insufficient_final_review_scope")

    def test_routed_action_alone_does_not_close_progress_blocker(self):
        self.progress(blockers=[{"id": "R1", "routed_action": "Finish the required chapter next"}])
        seal(self.root)
        self.assert_flag("completion_claim_with_open_blockers")

    def test_explicitly_resolved_routed_issue_has_positive_control(self):
        self.append_review({"scope": "full_report", "result": "PASS", "issues": [
            {"id": "R1", "status": "resolved", "routed_action": "Rechecked source", "resolution": "Claim corrected"}
        ]})
        seal(self.root)
        self.assertTrue(self.evaluate()["ok"])

    def test_malformed_review(self):
        with (self.root / "logs/review.jsonl").open("a", encoding="utf-8") as output:
            output.write("not JSON\n")
        seal(self.root)
        self.assert_flag("invalid_review_log")

    def test_nonobject_review(self):
        with (self.root / "logs/review.jsonl").open("a", encoding="utf-8") as output:
            output.write("[]\n")
        seal(self.root)
        self.assert_flag("invalid_review_log")

    def test_invalid_utf8_review_is_rejected(self):
        with (self.root / "logs/review.jsonl").open("ab") as output:
            output.write(b'{"scope":"detail","note":"\xff"}\n')
        seal(self.root)
        self.assert_flag("invalid_review_log")

    def test_invalid_utf8_requirements_are_rejected(self):
        (self.root / "state/requirements.jsonl").write_bytes(
            b'{"id":"R1","status":"satisfied","summary":"\xff"}\n'
        )
        seal(self.root)
        self.assert_flag("unresolved_required_corrections")

    def test_invalid_utf8_progress_fails_without_crashing(self):
        (self.root / "state/progress.json").write_bytes(
            b'{"stage":"final","status":"complete","note":"\xff"}\n'
        )
        seal(self.root)
        self.assert_flag("invalid_progress_stage")

    def test_invalid_utf8_receipt_fails_without_crashing(self):
        (self.root / "state/final_delivery.json").write_bytes(b'{"note":"\xff"}\n')
        self.assert_flag("invalid_delivery_receipt")

    def test_invalid_utf8_message_is_rejected(self):
        with (self.root / "delivery_message.md").open("ab") as output:
            output.write(b'\xff\n')
        seal(self.root)
        self.assert_flag("invalid_delivery_message")

    def test_complete_requires_final_without_completion_words(self):
        self.progress(stage="review", status="complete")
        (self.root / "delivery_message.md").write_text("仍是阶段稿。\n", encoding="utf-8")
        seal(self.root)
        self.assert_flag("invalid_completion_status")

    def test_completion_paraphrase(self):
        self.progress(stage="review", status="in_progress")
        (self.root / "delivery_message.md").write_text("都搞定了，可以发布。限制仍如上。\n", encoding="utf-8")
        seal(self.root)
        self.assert_flag("completion_claim_without_terminal_state")

    def test_each_required_receipt_binding(self):
        path = self.root / "state/final_delivery.json"
        original = json.loads(path.read_text(encoding="utf-8"))
        for target in ("state/progress.json", "logs/review.jsonl", "delivery_message.md"):
            with self.subTest(target=target):
                receipt = json.loads(json.dumps(original))
                del receipt["artifacts"][target]
                write_json(path, receipt)
                self.assert_flag("incomplete_delivery_receipt")
        write_json(path, original)

    def test_latest_global_event_sequences(self):
        variants = [
            {"scope": "full_report", "result": "PASS", "issues": []},
            {"scope": "full_report", "result": "fail", "issues": []},
            {"scope": "full_report", "result": "PASS", "issues": ["open"]},
            {"scope": "full_report", "result": "needs_revision", "issues": []},
        ]
        for length in (1, 2, 3):
            for indices in itertools.product(range(len(variants)), repeat=length):
                rows = [variants[i] for i in indices]
                with self.subTest(sequence=indices):
                    self.assertEqual(checker.latest_global_review_passes(rows), indices[-1] == 0)

    def test_final_complete_truth_table(self):
        for stage, status in itertools.product(sorted(checker.CANONICAL_STAGES), ("in_progress", "complete")):
            with self.subTest(stage=stage, status=status):
                self.progress(stage=stage, status=status)
                (self.root / "delivery_message.md").write_text("阶段说明。已知限制保持披露。\n", encoding="utf-8")
                seal(self.root)
                result = self.evaluate()
                invalid = (stage == "final") != (status == "complete")
                self.assertEqual("invalid_completion_status" in result["flags"], invalid, result)

    def test_custom_message_is_bound(self):
        original = self.root / "delivery_message.md"
        custom = self.root / "note.md"
        custom.write_bytes(original.read_bytes())
        original.unlink()
        seal(self.root, "note.md")
        self.assertTrue(self.evaluate(delivery_message="note.md")["ok"])

    def test_changed_custom_message_is_rejected(self):
        custom = self.root / "note.md"
        custom.write_bytes((self.root / "delivery_message.md").read_bytes())
        seal(self.root, "note.md")
        custom.write_text(custom.read_text(encoding="utf-8") + "额外说明。\n", encoding="utf-8")
        result = self.evaluate(delivery_message="note.md")
        self.assertIn("stale_delivery_receipt", result["flags"], result)

    def test_message_path_cannot_escape_project(self):
        result = self.evaluate(delivery_message="../outside.md")
        self.assertIn("invalid_delivery_path", result["flags"], result)

    def test_actual_delivery_matches_capture(self):
        capture = Path(self.temp.name) / "captured.md"
        capture.write_bytes((self.root / "delivery_message.md").read_bytes().replace(b"\n", b"\r\n"))
        result = self.evaluate(actual_message=capture)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["delivery_observation"], "matched")

    def test_actual_delivery_mismatch_is_rejected(self):
        capture = Path(self.temp.name) / "captured.md"
        capture.write_text("A different final reply.\n", encoding="utf-8")
        self.assert_flag("actual_delivery_mismatch", actual_message=capture)

    def test_missing_capture_is_not_silently_ignored(self):
        self.assert_flag("missing_actual_delivery", actual_message=Path(self.temp.name) / "missing.md")

    def test_unobserved_delivery_is_not_called_verified(self):
        self.assertEqual(self.evaluate()["delivery_observation"], "not_provided")

    def test_unknown_progress_status(self):
        self.progress(stage="review", status="banana")
        (self.root / "delivery_message.md").write_text("阶段稿。\n", encoding="utf-8")
        seal(self.root)
        self.assert_flag("invalid_progress_status")

    def test_declared_review_dimension_cannot_be_skipped(self):
        self.progress(required_review_scopes=["evidence"])
        seal(self.root)
        self.assert_flag("missing_required_review")

    def test_late_dimension_failure_invalidates_old_pass(self):
        self.progress(required_review_scopes=["evidence"])
        self.append_review({"scope": "evidence", "result": "PASS"})
        self.append_review({"scope": "evidence", "result": "needs_revision"})
        seal(self.root)
        self.assert_flag("failed_required_review")

    def test_dimension_recovery_has_positive_control(self):
        self.progress(required_review_scopes=["evidence"])
        self.append_review({"scope": "evidence", "result": "needs_revision"})
        self.append_review({"scope": "evidence", "result": "PASS", "issues": []})
        seal(self.root)
        self.assertTrue(self.evaluate()["ok"])

    def test_invalid_review_scope_declaration(self):
        self.progress(required_review_scopes="evidence")
        seal(self.root)
        self.assert_flag("invalid_required_review_scopes")

    def test_cli_actual_capture(self):
        capture = Path(self.temp.name) / "captured.md"
        capture.write_bytes((self.root / "delivery_message.md").read_bytes())
        result = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(REPO / "scripts/check_delivery.py"), str(self.root),
             "--actual-message", str(capture), "--json"],
            text=True, encoding="utf-8", capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["delivery_observation"], "matched")


if __name__ == "__main__":
    if os.environ.get("IRF_TEST_TMPDIR"):
        tempfile.tempdir = os.environ["IRF_TEST_TMPDIR"]
    unittest.main(verbosity=2)
