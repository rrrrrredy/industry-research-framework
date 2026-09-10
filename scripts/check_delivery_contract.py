#!/usr/bin/env python3
"""Isolated delivery regressions: reseal unrelated inputs so stale hashes cannot mask defects."""
from __future__ import annotations

import itertools
import csv
import json
import os
from pathlib import Path
import re
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


def bind_synthetic_reviews(root: Path) -> None:
    """Build a current-contract control in a temp copy, never reseal real reviews."""
    path = root / "logs/review.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    for row in rows:
        row["artifact_sha256"] = checker.sha256_file(root / "final.md")
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def seal(root: Path, message: str = "delivery_message.md", artifact: str = "final.md") -> None:
    receipt_path = root / "state/final_delivery.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["artifact"] = artifact
    paths = [artifact, *[p for p in checker.REQUIRED_HASH_INPUTS if p != "delivery_message.md"], message]
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
        bind_synthetic_reviews(self.root)
        seal(self.root)

    def evaluate(self, **kwargs):
        return checker.evaluate_delivery(self.root, **kwargs)

    def progress(self, **updates):
        path = self.root / "state/progress.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        value.update(updates)
        write_json(path, value)

    def append_review(self, row):
        row = dict(row)
        row.setdefault("artifact_sha256", checker.sha256_file(self.root / "final.md"))
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

    def test_progress_status_contract_is_documented(self):
        # Check the caller-facing enum against the real checker, not a second
        # hand-maintained list. A native checkpoint exposed this documentation gap.
        lines = (REPO / "SKILL.md").read_text(encoding="utf-8").splitlines()
        declaration = [line for line in lines if line.startswith("`progress.json.status` accepts ")]
        self.assertEqual(len(declaration), 1, "The status enum must be discoverable in the normative source")
        values = re.findall(r"`([^`]+)`", declaration[0])[1:]
        self.assertEqual(set(values), checker.PROGRESS_STATUSES)
        self.assertEqual(len(values), len(set(values)))

    def test_native_descriptive_checkpoint_status_is_not_canonical(self):
        # Exact status from a real partial native run; no private report/log needed.
        self.progress(stage="review", status="paused_at_user_requested_checkpoint")
        (self.root / "delivery_message.md").write_text("这是阶段稿，后续板块尚未完成。\n", encoding="utf-8")
        seal(self.root)
        self.assert_flag("invalid_progress_status")

    def test_canonical_checkpoint_statuses_keep_honest_partial_work_valid(self):
        for status in ("in_progress", "paused", "blocked"):
            with self.subTest(status=status):
                self.progress(stage="review", status=status, next_action="Continue the remaining sections later")
                (self.root / "delivery_message.md").write_text("这是阶段稿，后续板块尚未完成。\n", encoding="utf-8")
                seal(self.root)
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

    def test_linked_primary_artifact_completion_is_not_a_stage_delivery(self):
        # Derived from an actual Codex reply; no private path or report is needed.
        self.progress(stage="review", status="in_progress")
        for message in ("已完成 [final.md](final.md)。", "Completed [final.md](final.md)."):
            with self.subTest(message=message):
                (self.root / "delivery_message.md").write_text(message + " 已知限制保持披露。\n", encoding="utf-8")
                seal(self.root)
                self.assert_flag("completion_claim_without_terminal_state")

    def test_linked_primary_artifact_keeps_valid_terminal_control(self):
        (self.root / "delivery_message.md").write_text(
            "已完成 [final.md](final.md)。已知限制保持披露。\n", encoding="utf-8"
        )
        seal(self.root)
        result = self.evaluate()
        self.assertTrue(result["ok"], result)
        self.assertTrue(result["completion_claim"], result)

    def test_link_or_partial_unit_alone_is_not_whole_report_completion(self):
        self.progress(stage="review", status="in_progress")
        for message in (
            "查看 [final.md](final.md)。",
            "[final.md](final.md)",
            "已完成 [outline.md](outline.md)，正文仍在整理。",
            "已完成 [final.md](final.md) 的提纲，全文仍在整理。",
            "Completed [final.md](final.md)'s outline. The report is still being written.",
            "已完成草稿 [final.md](final.md)，全文仍在整理。",
            "Draft [final.md](final.md) is complete.",
            "Completed the draft of [final.md](final.md).",
        ):
            with self.subTest(message=message):
                (self.root / "delivery_message.md").write_text(message + "\n", encoding="utf-8")
                seal(self.root)
                result = self.evaluate()
                self.assertTrue(result["ok"], result)
                self.assertFalse(result["completion_claim"], result)

    def test_negated_linked_completion_is_honest(self):
        self.progress(stage="review", status="in_progress")
        for message in ("尚未完成 [final.md](final.md)。", "没有完成 [final.md](final.md)。",
                        "Not completed [final.md](final.md)."):
            with self.subTest(message=message):
                (self.root / "delivery_message.md").write_text(message + "\n", encoding="utf-8")
                seal(self.root)
                self.assertTrue(self.evaluate()["ok"])

    def test_linked_completion_uses_selected_primary_artifact(self):
        self.progress(stage="review", status="in_progress")
        shutil.copyfile(self.root / "final.md", self.root / "report.md")
        (self.root / "delivery_message.md").write_text(
            "已完成 [report.md](report.md)。已知限制保持披露。\n", encoding="utf-8"
        )
        seal(self.root, artifact="report.md")
        self.assert_flag("completion_claim_without_terminal_state", artifact="report.md")

    def test_inline_primary_filename_completion(self):
        self.progress(stage="review", status="in_progress")
        for message in ("已完成 `final.md`。", "`final.md` 已完成。", "Completed `final.md`.",
                        "`final.md` is complete."):
            with self.subTest(message=message):
                (self.root / "delivery_message.md").write_text(message + " 已知限制保持披露。\n", encoding="utf-8")
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

    def requirement(self, **changes):
        row = {"requirement_id": "NEW-READ", "summary": "Read the specified source in full.",
               "status": "satisfied", "evidence": "Reading notes for the required source."}
        row.update(changes)
        original = (BASE / "state/requirements.jsonl").read_text(encoding="utf-8")
        (self.root / "state/requirements.jsonl").write_text(
            original + json.dumps(row) + "\n", encoding="utf-8")
        seal(self.root)

    def reading_source(self, scope="full_text", evidence="notes/source-1.md: main text and appendices"):
        path = self.root / "data/source_registry.csv"
        with path.open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            fields = list(reader.fieldnames)
            rows = list(reader)
        for field in ("read_scope", "read_evidence"):
            if field not in fields:
                fields.append(field)
        rows[0].update(read_scope=scope, read_evidence=evidence)
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        return rows[0]["source_id"]

    def test_self_accepted_or_waived_requirements_are_rejected(self):
        for status in ("accepted_limitation", "waived", "out_of_scope"):
            with self.subTest(status=status):
                self.requirement(status=status)
                self.assert_flag("unresolved_required_corrections")

    def test_all_unresolved_requirement_findings_are_reported(self):
        self.requirement(requirement_id="R-first", status="waived")
        with (self.root / "state/requirements.jsonl").open("a", encoding="utf-8") as out:
            out.write(json.dumps({"requirement_id": "R-second", "status": "out_of_scope"}) + "\n")
        seal(self.root)
        result = self.assert_flag("unresolved_required_corrections")
        index = result["flags"].index("unresolved_required_corrections")
        self.assertIn("R-first", result["findings"][index])
        self.assertIn("R-second", result["findings"][index])
        self.assertEqual(len(result["flags"]), len(result["findings"]))

    def test_disclosing_unread_work_does_not_authorize_waiver(self):
        self.requirement(status="accepted_limitation")
        with (self.root / "delivery_message.md").open("a", encoding="utf-8") as out:
            out.write("\nKnown limitation: Read the specified source in full. It remains unread.\n")
        seal(self.root)
        result = self.assert_flag("unresolved_required_corrections")
        self.assertNotIn("undisclosed_accepted_limitations", result["flags"])

    def test_specific_user_decision_has_positive_controls(self):
        for status in ("waived", "out_of_scope", "accepted_limitation"):
            with self.subTest(status=status):
                self.requirement(status=status, user_decision={
                    "source_turn": "user-turn-7", "quote": "You may leave that article unread."})
                with (self.root / "delivery_message.md").open("a", encoding="utf-8") as out:
                    out.write("\nKnown limitation: Read the specified source in full. It remains unread.\n")
                seal(self.root)
                result = self.evaluate()
                self.assertTrue(result["ok"], result)
                self.assertFalse(result["semantic_verification"])

    def test_user_decision_must_have_nonempty_typed_reference_and_quote(self):
        for decision in (None, True, [], "approved", {}, {"source_turn": "T1"},
                         {"source_turn": " ", "quote": "Skip"},
                         {"source_turn": "T1", "quote": []},
                         {"source_turn": 2, "quote": "Skip"}):
            with self.subTest(decision=decision):
                self.requirement(status="waived", user_decision=decision)
                self.assert_flag("unresolved_required_corrections")

    def test_satisfied_requirement_needs_evidence_but_no_extra_user_approval(self):
        for evidence in (None, " ", [], {}, True, ["done", ""]):
            with self.subTest(evidence=evidence):
                self.requirement(evidence=evidence)
                self.assert_flag("unresolved_required_corrections")
        for evidence in ("notes/read.md", ["notes/read.md", "final.md section 2"]):
            self.requirement(evidence=evidence)
            self.assertTrue(self.evaluate()["ok"])

    def test_full_reading_is_not_access_or_abstract_reading(self):
        for scope in ("not_read", "abstract", "partial", "relevant_sections", "accessible", ""):
            with self.subTest(scope=scope):
                source_id = self.reading_source(scope)
                self.requirement(reading_requirement="full_text", required_source_ids=[source_id])
                self.assert_flag("unresolved_required_corrections")

    def test_full_reading_and_relevant_section_positive_controls(self):
        for required, actual in (("full_text", "full_text"), ("relevant_sections", "full_text"),
                                 ("relevant_sections", "relevant_sections")):
            with self.subTest(required=required, actual=actual):
                source_id = self.reading_source(actual)
                self.requirement(reading_requirement=required, required_source_ids=[source_id])
                self.assertTrue(self.evaluate()["ok"])

    def test_unread_optional_background_does_not_become_a_mandatory_full_read(self):
        self.reading_source("not_read", "")
        self.requirement()  # This requirement does not demand reading that background source.
        self.assertTrue(self.evaluate()["ok"])

    def test_reading_without_evidence_or_missing_source_fails(self):
        source_id = self.reading_source("full_text", "")
        self.requirement(reading_requirement="full_text", required_source_ids=[source_id])
        self.assert_flag("unresolved_required_corrections")
        self.requirement(reading_requirement="full_text", required_source_ids=["not-in-registry"])
        self.assert_flag("unresolved_required_corrections")

    def test_duplicate_required_source_rows_are_ambiguous(self):
        source_id = self.reading_source()
        path = self.root / "data/source_registry.csv"
        with path.open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            fields, rows = reader.fieldnames, list(reader)
        with path.open("a", encoding="utf-8", newline="") as stream:
            csv.DictWriter(stream, fieldnames=fields).writerow(rows[0])
        self.requirement(reading_requirement="full_text", required_source_ids=[source_id])
        self.assert_flag("unresolved_required_corrections")

    def test_reading_declaration_types_fail_closed(self):
        for required, sources in (("unknown", ["S1"]), ([], ["S1"]), ("full_text", []),
                                  ("full_text", "S1"), ("full_text", ["S1", "S1"]),
                                  ("full_text", [" "]), ("full_text", [1])):
            with self.subTest(required=required, sources=sources):
                self.requirement(reading_requirement=required, required_source_ids=sources)
                self.assert_flag("unresolved_required_corrections")

    def test_explicit_waiver_can_close_an_unread_source(self):
        source_id = self.reading_source("not_read", "")
        self.requirement(status="waived", reading_requirement="full_text", required_source_ids=[source_id],
                         user_decision={"source_turn": "user-turn-7", "quote": "Skip this article."})
        self.assertTrue(self.evaluate()["ok"])

    def test_unfinished_required_reading_is_valid_only_as_honest_partial_delivery(self):
        source_id = self.reading_source("not_read", "")
        self.requirement(status="open", reading_requirement="full_text", required_source_ids=[source_id])
        self.progress(stage="collect", status="blocked", next_action="Ask for the inaccessible required text")
        (self.root / "delivery_message.md").write_text("阶段稿；指定材料尚未读完，研究未完成。\n", encoding="utf-8")
        seal(self.root)
        self.assertTrue(self.evaluate()["ok"])

    def test_free_text_is_not_semantically_certified(self):
        self.requirement(evidence="Only an access attempt; the source remains unread.")
        result = self.evaluate()
        self.assertTrue(result["ok"])
        self.assertFalse(result["semantic_verification"])

    def test_resealing_new_prose_does_not_reseal_old_review(self):
        with (self.root / "final.md").open("a", encoding="utf-8") as out:
            out.write("\nA new substantive conclusion that was not in the reviewed report.\n")
        seal(self.root)
        self.assert_flag("stale_review_artifact")

    def test_actual_current_global_review_recovers_after_revision(self):
        with (self.root / "final.md").open("a", encoding="utf-8") as out:
            out.write("\nA separately reviewed new conclusion.\n")
        self.append_review({"scope": "full_report", "result": "PASS", "issues": []})
        seal(self.root)
        self.assertTrue(self.evaluate()["ok"])

    def test_new_local_review_does_not_cover_unreviewed_whole_revision(self):
        with (self.root / "final.md").open("a", encoding="utf-8") as out:
            out.write("\nAn additional report conclusion.\n")
        self.append_review({"scope": "unit_a", "result": "PASS"})
        seal(self.root)
        self.assert_flag("stale_review_artifact")

    def test_new_global_review_does_not_refresh_required_specialist_review(self):
        self.progress(required_review_scopes=["reader_quality"])
        self.append_review({"scope": "reader_quality", "result": "PASS"})
        with (self.root / "final.md").open("a", encoding="utf-8") as out:
            out.write("\nAn additional report conclusion.\n")
        self.append_review({"scope": "full_report", "result": "PASS"})
        seal(self.root)
        self.assert_flag("stale_review_artifact")
        self.append_review({"scope": "reader_quality", "result": "PASS"})
        seal(self.root)
        self.assertTrue(self.evaluate()["ok"])

    def test_bad_review_hashes_are_rejected(self):
        for bound in (None, [], {}, True, " ", "a" * 63, "g" * 64):
            with self.subTest(bound=bound):
                self.append_review({"scope": "full_report", "result": "PASS", "artifact_sha256": bound})
                seal(self.root)
                self.assert_flag("missing_review_artifact_binding")

    def test_review_hash_uses_portable_lf_bytes(self):
        path = self.root / "final.md"
        path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        seal(self.root)
        self.assertTrue(self.evaluate()["ok"])

    def test_legacy_is_explicit_and_never_current_acceptance(self):
        shutil.copyfile(BASE / "logs/review.jsonl", self.root / "logs/review.jsonl")
        seal(self.root)
        self.assert_flag("missing_review_artifact_binding")
        result = self.evaluate(contract_version=1)
        self.assertTrue(result["ok"])
        self.assertFalse(result["current_contract_checked"])
        self.assertFalse(result["semantic_verification"])
        self.assertTrue(any("Legacy v1" in value for value in result["warnings"]))

    def test_invalid_contract_version_is_not_a_legacy_bypass(self):
        for version in (0, 3, True, "1", None, 1.0, 2.0):
            with self.subTest(version=version):
                result = self.assert_flag("invalid_delivery_contract_version", contract_version=version)
                self.assertFalse(result["current_contract_checked"])
                self.assertFalse(any("Legacy v1" in value for value in result["warnings"]))


if __name__ == "__main__":
    if os.environ.get("IRF_TEST_TMPDIR"):
        tempfile.tempdir = os.environ["IRF_TEST_TMPDIR"]
    unittest.main(verbosity=2)
