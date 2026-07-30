from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_EVALS_PATH = ROOT / "scripts" / "run_evals.py"

spec = importlib.util.spec_from_file_location("industry_research_run_evals", RUN_EVALS_PATH)
run_evals = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = run_evals
spec.loader.exec_module(run_evals)


def review_log(*rows: dict[str, object]) -> str:
    return "\n".join(json.dumps(row) for row in rows)


class ReviewClosureTests(unittest.TestCase):
    def test_routed_failure_followed_by_matching_pass_is_closed(self):
        text = review_log(
            {
                "review_type": "evidence",
                "scope": "section-1",
                "result": "FAIL",
                "issues": [
                    {
                        "status": "resolved",
                        "routed_action": "downgrade the claim",
                    }
                ],
                "routed_actions": ["downgrade the claim"],
            },
            {
                "review_type": "evidence",
                "scope": "section-1",
                "result": "PASS",
                "issues": [],
                "routed_actions": [],
            },
        )

        self.assertFalse(run_evals.review_has_unresolved_failures(text))

    def test_routed_failure_without_rerun_remains_open(self):
        text = review_log(
            {
                "review_type": "evidence",
                "scope": "section-1",
                "result": "FAIL",
                "issues": [
                    {
                        "status": "resolved",
                        "routed_action": "downgrade the claim",
                    }
                ],
                "routed_actions": ["downgrade the claim"],
            }
        )

        self.assertTrue(run_evals.review_has_unresolved_failures(text))

    def test_unrouted_failure_cannot_be_closed_by_empty_pass(self):
        text = review_log(
            {
                "review_type": "evidence",
                "scope": "section-1",
                "result": "FAIL",
                "issues": ["unsupported adoption claim"],
                "routed_actions": [],
            },
            {
                "review_type": "evidence",
                "scope": "section-1",
                "result": "PASS",
                "issues": [],
                "routed_actions": [],
            },
        )

        self.assertTrue(run_evals.review_has_unresolved_failures(text))

    def test_pass_for_another_scope_does_not_close_failure(self):
        text = review_log(
            {
                "review_type": "evidence",
                "scope": "section-1",
                "result": "FAIL",
                "issues": [{"status": "resolved", "resolution": "add source"}],
                "routed_actions": ["add source"],
            },
            {
                "review_type": "evidence",
                "scope": "section-2",
                "result": "PASS",
                "issues": [],
                "routed_actions": [],
            },
        )

        self.assertTrue(run_evals.review_has_unresolved_failures(text))

    def test_later_failure_reopens_a_previously_passing_scope(self):
        text = review_log(
            {
                "review_type": "reader",
                "scope": "full draft",
                "result": "PASS",
                "issues": [],
                "routed_actions": [],
            },
            {
                "review_type": "reader",
                "scope": "full draft",
                "result": "FAIL",
                "issues": [{"status": "open", "finding": "weak synthesis"}],
                "routed_actions": [],
            },
        )

        self.assertTrue(run_evals.review_has_unresolved_failures(text))

    def test_pass_with_open_issue_does_not_close_failure(self):
        text = review_log(
            {
                "review_type": "reader",
                "scope": "full draft",
                "result": "FAIL",
                "issues": [{"status": "resolved", "resolution": "revise synthesis"}],
                "routed_actions": ["revise synthesis"],
            },
            {
                "review_type": "reader",
                "scope": "full draft",
                "result": "PASS",
                "issues": [{"status": "open", "finding": "weak conclusion"}],
                "routed_actions": [],
            },
        )

        self.assertTrue(run_evals.review_has_unresolved_failures(text))

    def test_pass_with_negated_closed_status_does_not_close_failure(self):
        for issue_status in ("not resolved", "unhandled", "not closed"):
            with self.subTest(issue_status=issue_status):
                text = review_log(
                    {
                        "review_type": "reader",
                        "scope": "full draft",
                        "result": "FAIL",
                        "issues": [
                            {"status": "resolved", "resolution": "revise synthesis"}
                        ],
                        "routed_actions": ["revise synthesis"],
                    },
                    {
                        "review_type": "reader",
                        "scope": "full draft",
                        "result": "PASS",
                        "issues": [{"status": issue_status}],
                        "routed_actions": [],
                    },
                )

                self.assertTrue(run_evals.review_has_unresolved_failures(text))

    def test_not_pass_does_not_close_failure(self):
        text = review_log(
            {
                "review_type": "evidence",
                "scope": "section-1",
                "result": "FAIL",
                "issues": [{"status": "resolved", "resolution": "add source"}],
                "routed_actions": ["add source"],
            },
            {
                "review_type": "evidence",
                "scope": "section-1",
                "result": "NOT PASS",
                "issues": [],
                "routed_actions": [],
            },
        )

        self.assertTrue(run_evals.review_has_unresolved_failures(text))

    def test_routed_failure_does_not_overwrite_earlier_unrouted_failure(self):
        text = review_log(
            {
                "review_type": "evidence",
                "scope": "section-1",
                "result": "FAIL",
                "issues": [{"status": "open", "finding": "unsupported claim"}],
                "routed_actions": [],
            },
            {
                "review_type": "evidence",
                "scope": "section-1",
                "result": "FAIL",
                "issues": [{"status": "resolved", "resolution": "downgrade claim"}],
                "routed_actions": ["downgrade claim"],
            },
            {
                "review_type": "evidence",
                "scope": "section-1",
                "result": "PASS",
                "issues": [],
                "routed_actions": [],
            },
        )

        self.assertTrue(run_evals.review_has_unresolved_failures(text))

    def test_empty_route_values_do_not_close_failure(self):
        for empty_value in (None, {}):
            with self.subTest(empty_value=empty_value):
                text = review_log(
                    {
                        "review_type": "evidence",
                        "scope": "section-1",
                        "result": "FAIL",
                        "issues": [empty_value],
                        "routed_actions": [empty_value],
                    },
                    {
                        "review_type": "evidence",
                        "scope": "section-1",
                        "result": "PASS",
                        "issues": [],
                        "routed_actions": [],
                    },
                )

                self.assertTrue(run_evals.review_has_unresolved_failures(text))

    def test_null_issue_with_valid_action_stays_open(self):
        text = review_log(
            {
                "review_type": "evidence",
                "scope": "section-1",
                "result": "FAIL",
                "issues": [None],
                "routed_actions": ["add source"],
            },
            {
                "review_type": "evidence",
                "scope": "section-1",
                "result": "PASS",
                "issues": [],
                "routed_actions": [],
            },
        )

        self.assertTrue(run_evals.review_has_unresolved_failures(text))

    def test_null_handling_value_stays_open(self):
        for empty_value in (None, {}):
            with self.subTest(empty_value=empty_value):
                text = review_log(
                    {
                        "review_type": "evidence",
                        "scope": "section-1",
                        "result": "FAIL",
                        "issues": [{"resolution": empty_value}],
                        "routed_actions": [],
                    },
                    {
                        "review_type": "evidence",
                        "scope": "section-1",
                        "result": "PASS",
                        "issues": [],
                        "routed_actions": [],
                    },
                )

                self.assertTrue(run_evals.review_has_unresolved_failures(text))

    def test_routed_action_without_issue_stays_open(self):
        text = review_log(
            {
                "review_type": "evidence",
                "scope": "section-1",
                "result": "FAIL",
                "issues": [],
                "routed_actions": ["add source"],
            },
            {
                "review_type": "evidence",
                "scope": "section-1",
                "result": "PASS",
                "issues": [],
                "routed_actions": [],
            },
        )

        self.assertTrue(run_evals.review_has_unresolved_failures(text))

    def test_resolved_without_explicit_pass_remains_open(self):
        text = review_log(
            {
                "review_type": "evidence",
                "scope": "section-1",
                "result": "FAIL",
                "issues": [{"status": "resolved", "resolution": "add source"}],
                "routed_actions": ["add source"],
            },
            {
                "review_type": "evidence",
                "scope": "section-1",
                "status": "resolved",
                "issues": [],
                "routed_actions": [],
            },
        )

        self.assertTrue(run_evals.review_has_unresolved_failures(text))


if __name__ == "__main__":
    unittest.main()
