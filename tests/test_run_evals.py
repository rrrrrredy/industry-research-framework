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


if __name__ == "__main__":
    unittest.main()
