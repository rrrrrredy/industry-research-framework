from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
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


class ArtifactParsingTests(unittest.TestCase):
    def test_multiline_csv_field_counts_as_one_claim_row(self):
        text = (
            'claim_id,claim,status\n'
            'C1,"The claim spans\n'
            'two physical lines",accepted\n'
        )

        rows, errors = run_evals.parse_csv_rows(text, {"claim_id", "claim"})

        self.assertEqual(errors, [])
        self.assertEqual(len(rows), 1)
        self.assertIn("two physical lines", rows[0]["claim"])

    def test_source_registry_requires_exact_source_id_and_title(self):
        text = (
            "source_id,title,used_for\n"
            'S0010,"AI Agent Research Report extra",background\n'
        )

        hits, errors = run_evals.count_registry_sources(
            text,
            ["S001"],
            {"S001": {"title": "AI Agent Research Report"}},
        )

        self.assertEqual(errors, [])
        self.assertEqual(hits, 0)

    def test_quoted_source_title_with_comma_matches_exactly(self):
        text = (
            "source_id,title,used_for\n"
            'S001,"AI Agents, Platforms, and Adoption",background\n'
        )

        hits, errors = run_evals.count_registry_sources(
            text,
            ["S001"],
            {"S001": {"title": "AI Agents, Platforms, and Adoption"}},
        )

        self.assertEqual(errors, [])
        self.assertEqual(hits, 1)

    def test_missing_required_csv_header_is_reported(self):
        rows, errors = run_evals.parse_csv_rows(
            "claim_id,status\nC1,accepted\n",
            {"claim_id", "claim"},
        )

        self.assertEqual(rows, [])
        self.assertEqual(errors, ["missing required headers: claim"])

    def test_empty_required_csv_value_is_not_counted(self):
        rows, errors = run_evals.parse_csv_rows(
            "claim_id,claim,status\nC1,,accepted\n",
            {"claim_id", "claim"},
        )

        self.assertEqual(rows, [])
        self.assertEqual(errors, ["row 2 has empty required values: claim"])

    def test_duplicate_csv_headers_are_rejected_after_normalization(self):
        rows, errors = run_evals.parse_csv_rows(
            "claim_id,CLAIM_ID,claim\nC1,C2,Example\n",
            {"claim_id", "claim"},
        )

        self.assertEqual(rows, [])
        self.assertEqual(errors, ["header contains duplicate field names"])

    def test_csv_rows_with_extra_or_missing_fields_are_rejected(self):
        for text, expected_error in (
            (
                "claim_id,claim\nC1,Example,extra\n",
                "row 2 has more fields than the header",
            ),
            (
                "claim_id,claim,status\nC1,Example\n",
                "row 2 has fewer fields than the header",
            ),
        ):
            with self.subTest(expected_error=expected_error):
                rows, errors = run_evals.parse_csv_rows(
                    text,
                    {"claim_id", "claim"},
                )

                self.assertEqual(rows, [])
                self.assertEqual(errors, [expected_error])

    def test_blank_csv_rows_are_ignored(self):
        rows, errors = run_evals.parse_csv_rows(
            "claim_id,claim\n\nC1,Example\n,\n\nC2,Another\n",
            {"claim_id", "claim"},
        )

        self.assertEqual(errors, [])
        self.assertEqual([row["claim_id"] for row in rows], ["C1", "C2"])

    def test_csv_headers_support_bom_and_unicode_equivalence(self):
        rows, errors = run_evals.parse_csv_rows(
            "\ufeffｃｌａｉｍ＿ｉｄ,claim\nC1,Example\n",
            {"claim_id", "claim"},
        )

        self.assertEqual(errors, [])
        self.assertEqual(rows[0]["claim_id"], "C1")

    def test_duplicate_source_ids_are_rejected(self):
        text = (
            "source_id,title,used_for\n"
            "S001,First title,background\n"
            "S001,Second title,analysis\n"
        )

        hits, errors = run_evals.count_registry_sources(
            text,
            ["S001"],
            {"S001": {"title": "First title"}},
        )

        self.assertEqual(hits, 0)
        self.assertEqual(errors, ["duplicate source_id values: S001"])

    def test_nfkc_equivalent_source_ids_are_rejected_as_duplicates(self):
        text = (
            "source_id,title,used_for\n"
            "S001,First title,background\n"
            "Ｓ００１,Second title,analysis\n"
        )

        hits, errors = run_evals.count_registry_sources(
            text,
            ["S001"],
            {"S001": {"title": "First title"}},
        )

        self.assertEqual(hits, 0)
        self.assertEqual(
            errors,
            ["duplicate source_id values: S001 / Ｓ００１"],
        )

    def test_source_titles_match_under_nfc_equivalence(self):
        hits, errors = run_evals.count_registry_sources(
            "source_id,title\nS001,Cafe\u0301\n",
            ["S001"],
            {"S001": {"title": "Café"}},
        )

        self.assertEqual(errors, [])
        self.assertEqual(hits, 1)

    def test_plain_text_review_line_is_malformed_not_a_review_row(self):
        rows, errors = run_evals.parse_review_rows("looks good")

        self.assertEqual(rows, [])
        self.assertEqual(len(errors), 1)
        self.assertTrue(errors[0].startswith("line 1 is not valid JSON:"))

    def test_json_scalar_review_line_is_malformed(self):
        rows, errors = run_evals.parse_review_rows('"PASS"')

        self.assertEqual(rows, [])
        self.assertEqual(errors, ["line 1 must be a JSON object"])

    def test_review_row_requires_status_issues_and_routed_actions(self):
        rows, errors = run_evals.parse_review_rows(
            json.dumps({})
        )

        self.assertEqual(rows, [])
        self.assertEqual(
            errors,
            [
                "line 1 is missing or invalid: review_type, scope, review status, "
                "issues list, routed_actions list"
            ],
        )

    def test_review_outcome_must_be_canonical(self):
        rows, errors = run_evals.parse_review_rows(
            json.dumps(
                {
                    "review_type": "reader",
                    "scope": "full draft",
                    "result": "looks good",
                    "issues": [],
                    "routed_actions": [],
                }
            )
        )

        self.assertEqual(rows, [])
        self.assertEqual(
            errors,
            ["line 1 is missing or invalid: result outcome"],
        )

    def test_unsupported_review_outcome_alias_is_not_accepted(self):
        rows, errors = run_evals.parse_review_rows(
            json.dumps(
                {
                    "review_type": "reader",
                    "scope": "full draft",
                    "verdict": "PASS",
                    "issues": [],
                    "routed_actions": [],
                }
            )
        )

        self.assertEqual(rows, [])
        self.assertEqual(
            errors,
            ["line 1 is missing or invalid: review status"],
        )

    def test_conflicting_review_outcomes_are_rejected(self):
        rows, errors = run_evals.parse_review_rows(
            json.dumps(
                {
                    "review_type": "reader",
                    "scope": "full draft",
                    "result": "PASS",
                    "status": "FAIL",
                    "issues": ["weak conclusion"],
                    "routed_actions": [],
                }
            )
        )

        self.assertEqual(rows, [])
        self.assertEqual(
            errors,
            ["line 1 is missing or invalid: conflicting review outcomes"],
        )

    def test_review_json_rejects_duplicate_keys(self):
        rows, errors = run_evals.parse_review_rows(
            '{"review_type":"reader","review_type":"evidence","scope":"full draft",'
            '"result":"PASS","issues":[],"routed_actions":[]}'
        )

        self.assertEqual(rows, [])
        self.assertEqual(
            errors,
            ["line 1 is not valid JSON: duplicate JSON key: review_type"],
        )

    def test_review_json_accepts_utf8_bom(self):
        rows, errors = run_evals.parse_review_rows(
            "\ufeff"
            + json.dumps(
                {
                    "review_type": "reader",
                    "scope": "full draft",
                    "result": "PASS",
                    "issues": [],
                    "routed_actions": [],
                }
            )
        )

        self.assertEqual(errors, [])
        self.assertEqual(len(rows), 1)

    def test_review_outcome_accepts_nfkc_equivalent_enum(self):
        rows, errors = run_evals.parse_review_rows(
            json.dumps(
                {
                    "review_type": "reader",
                    "scope": "full draft",
                    "result": "ＰＡＳＳ",
                    "issues": [],
                    "routed_actions": [],
                },
                ensure_ascii=False,
            )
        )

        self.assertEqual(errors, [])
        self.assertEqual(len(rows), 1)

    def test_review_scope_uses_unicode_equivalence_for_closure(self):
        text = review_log(
            {
                "review_type": "reader",
                "scope": "Café",
                "result": "FAIL",
                "issues": [{"resolution": "revise"}],
                "routed_actions": ["revise"],
            },
            {
                "review_type": "reader",
                "scope": "Cafe\u0301",
                "result": "PASS",
                "issues": [],
                "routed_actions": [],
            },
        )

        self.assertFalse(run_evals.review_has_unresolved_failures(text))

    def test_review_entries_must_have_substantive_content(self):
        for field, value, expected_field in (
            ("issues", [None], "issues entries"),
            ("issues", [{}], "issues entries"),
            ("routed_actions", [None], "routed_actions entries"),
            ("routed_actions", [""], "routed_actions entries"),
        ):
            with self.subTest(field=field, value=value):
                row = {
                    "review_type": "reader",
                    "scope": "full draft",
                    "result": "PASS",
                    "issues": [],
                    "routed_actions": [],
                }
                row[field] = value

                rows, errors = run_evals.parse_review_rows(json.dumps(row))

                self.assertEqual(rows, [])
                self.assertEqual(
                    errors,
                    [f"line 1 is missing or invalid: {expected_field}"],
                )

    def test_failed_review_requires_an_issue(self):
        rows, errors = run_evals.parse_review_rows(
            json.dumps(
                {
                    "review_type": "evidence",
                    "scope": "section-1",
                    "result": "FAIL",
                    "issues": [],
                    "routed_actions": [],
                }
            )
        )

        self.assertEqual(rows, [])
        self.assertEqual(
            errors,
            ["line 1 is missing or invalid: FAIL issues"],
        )

    def test_evaluate_case_surfaces_all_malformed_artifact_flags(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            (run_dir / "data").mkdir()
            (run_dir / "logs").mkdir()
            (run_dir / "final.md").write_text(
                "# Result\nEvidence remains uncertain because of a limitation.",
                encoding="utf-8",
            )
            (run_dir / "data" / "claims_registry.csv").write_text(
                "claim_id,status\nC1,accepted\n",
                encoding="utf-8",
            )
            (run_dir / "data" / "source_registry.csv").write_text(
                "source,title\nS001,Example\n",
                encoding="utf-8",
            )
            (run_dir / "logs" / "review.jsonl").write_text(
                "looks good\n",
                encoding="utf-8",
            )

            result = run_evals.evaluate_case(
                {
                    "case_id": "malformed_artifacts",
                    "artifact_requirements": ["final.md"],
                    "min_claim_rows": 0,
                    "min_review_rows": 0,
                    "min_final_nonspace_chars": 0,
                    "source_ids": [],
                },
                run_dir,
                {},
            )

        self.assertIn("malformed_claim_registry", result["quality_flags"])
        self.assertIn("malformed_source_registry", result["quality_flags"])
        self.assertIn("malformed_review_log", result["quality_flags"])

    def test_duplicate_claim_ids_are_rejected_under_nfkc_equivalence(self):
        for second_id in ("C1", "Ｃ１"):
            with self.subTest(second_id=second_id):
                with tempfile.TemporaryDirectory() as temp_dir:
                    run_dir = Path(temp_dir)
                    (run_dir / "data").mkdir()
                    (run_dir / "logs").mkdir()
                    (run_dir / "final.md").write_text(
                        "# Result\nEvidence remains uncertain because of a limitation.",
                        encoding="utf-8",
                    )
                    (run_dir / "data" / "claims_registry.csv").write_text(
                        "claim_id,claim\n"
                        "C1,First claim\n"
                        f"{second_id},Second claim\n",
                        encoding="utf-8",
                    )
                    (run_dir / "data" / "source_registry.csv").write_text(
                        "source_id,title\n",
                        encoding="utf-8",
                    )
                    (run_dir / "logs" / "review.jsonl").write_text(
                        review_log(
                            {
                                "review_type": "reader",
                                "scope": "full draft",
                                "result": "PASS",
                                "issues": [],
                                "routed_actions": [],
                            }
                        ),
                        encoding="utf-8",
                    )

                    result = run_evals.evaluate_case(
                        {
                            "case_id": "duplicate_claim_ids",
                            "artifact_requirements": ["final.md"],
                            "min_claim_rows": 0,
                            "min_review_rows": 0,
                            "min_final_nonspace_chars": 0,
                            "source_ids": [],
                        },
                        run_dir,
                        {},
                    )

                self.assertIn(
                    "malformed_claim_registry",
                    result["quality_flags"],
                )


if __name__ == "__main__":
    unittest.main()
