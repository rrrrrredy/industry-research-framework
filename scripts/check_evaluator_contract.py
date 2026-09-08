#!/usr/bin/env python3
"""Cross-entry regressions for current review state, disclosure and language controls."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest

import check_delivery as delivery
from check_delivery_contract import BASE, FINAL, REPO, seal, write_json
import run_evals as evaluator


class EvaluatorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = next(c for c in evaluator.load_cases(REPO / "evals/cases")
                        if c["case_id"] == "model_company_pipeline_long_horizon_zh")
        cls.sources = evaluator.load_sources(REPO / "evals")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="irf-evaluator-contract-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "task"
        shutil.copytree(BASE, self.root)
        shutil.copyfile(FINAL, self.root / "final.md")

    def progress(self, **changes):
        path = self.root / "state/progress.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        value.update(changes)
        write_json(path, value)

    def review(self, scope, result, **fields):
        with (self.root / "logs/review.jsonl").open("a", encoding="utf-8") as out:
            out.write(json.dumps({"scope": scope, "result": result, **fields}) + "\n")

    def check(self, *, delivery_enabled=True):
        seal(self.root)
        case = copy.deepcopy(self.case)
        case["delivery_check"] = delivery_enabled
        d = delivery.evaluate_delivery(self.root)
        e = evaluator.evaluate_case(case, self.root, self.sources)
        self.assertNotIn("stale_delivery_receipt", d["flags"], d)
        self.assertEqual(e["research_quality_status"], "not_evaluated")
        return d, e

    def assert_both_pass(self):
        d, e = self.check()
        self.assertTrue(d["ok"], d)
        self.assertEqual(e["conformance_status"], "pass", e)

    def assert_both_fail(self):
        d, e = self.check()
        self.assertFalse(d["ok"], d)
        self.assertEqual(e["conformance_status"], "fail", e)

    def test_known_good(self):
        self.assert_both_pass()

    def test_failure_then_global_recovery(self):
        self.review("full_report", "FAIL", issues=["Fix the claim"])
        self.review("global_final_delivery", "PASS", issues=[])
        self.assert_both_pass()

    def test_pass_then_failure(self):
        self.review("full_report", "PASS")
        self.review("full_report", "FAIL")
        self.assert_both_fail()

    def test_late_local_blocker_invalidates_global_pass(self):
        self.review("unit_a", "FAIL", issues=["New blocking finding"])
        self.assert_both_fail()

    def test_local_pass_cannot_clear_another_scope(self):
        self.review("unit_a", "FAIL")
        self.review("unit_b", "PASS")
        self.assert_both_fail()

    def test_local_recovery_does_not_clear_global_failure(self):
        self.review("full_report", "FAIL")
        self.review("unit_a", "PASS")
        self.assert_both_fail()

    def test_late_local_recovery_has_positive_control(self):
        self.review("unit_a", "FAIL")
        self.review("unit_a", "PASS", issues=[])
        self.assert_both_pass()

    def test_global_review_covers_earlier_ordinary_unit_review(self):
        self.review("unit_a", "FAIL")
        self.review("full_report", "PASS", issues=[])
        self.assert_both_pass()

    def test_declared_scope_cannot_be_erased_by_global_pass(self):
        self.progress(required_review_scopes=["evidence"])
        self.review("evidence", "FAIL")
        self.review("full_report", "PASS")
        self.assert_both_fail()

    def test_malformed_history_is_not_erased_by_pass(self):
        with (self.root / "logs/review.jsonl").open("a", encoding="utf-8") as out:
            out.write("not valid JSON\n")
        self.review("full_report", "PASS")
        self.assert_both_fail()

    def test_routed_action_is_not_resolution_even_without_receipt_check(self):
        self.progress(blockers=[{"id": "R1", "routed_action": "Verify this next"}])
        d, e = self.check(delivery_enabled=False)
        self.assertFalse(d["ok"], d)
        self.assertIn("false_completion_signal", e["conformance_flags"], e)

    def test_invalid_utf8_is_rejected_without_optional_receipt_check(self):
        with (self.root / "logs/review.jsonl").open("ab") as out:
            out.write(b'{"scope":"full_report","result":"PASS","note":"\xff"}\n')
        d, e = self.check(delivery_enabled=False)
        self.assertIn("invalid_review_log", d["flags"], d)
        self.assertIn("invalid_review_log", e["conformance_flags"], e)

    def test_conflicting_failure_status_is_not_hidden_by_result_pass(self):
        self.review("full_report", "PASS", status="FAIL")
        self.assert_both_fail()

    def test_explicitly_resolved_routed_action_is_valid(self):
        self.progress(blockers=[{"id": "R1", "status": "resolved",
                                 "routed_action": "Verify", "resolution": "Corrected claim"}])
        self.assert_both_pass()

    def test_explicit_open_status_wins_over_handling_text(self):
        item = {"status": "open", "handling": "Investigate tomorrow"}
        self.assertTrue(delivery.issue_is_open(item))
        self.assertTrue(evaluator.issue_is_unhandled(item))

    def test_blanket_denial_cannot_disclose_existing_limitations(self):
        for message in ("报告已完成，没有任何限制。", "The report is complete. No limitations."):
            with self.subTest(message=message):
                (self.root / "delivery_message.md").write_text(message, encoding="utf-8")
                d, e = self.check()
                self.assertIn("undisclosed_accepted_limitations", d["flags"], d)
                self.assertEqual(e["conformance_status"], "fail", e)

    def test_specific_coverage_is_observed_not_semantically_certified(self):
        limits = ["无法核验关键财务数据。", "缺少采购合同。"]
        result = delivery.assess_limitation_disclosure("已知限制：无法核验关键财务数据；缺少采购合同。", limits)
        self.assertEqual(result["status"], "text_covered")
        self.assertEqual(result["unmatched_limitations"], [])
        self.assertFalse(result["semantic_verification"])

    def test_partial_disclosure_requires_review(self):
        limits = ["无法核验关键财务数据。", "缺少采购合同。"]
        result = delivery.assess_limitation_disclosure("已知限制：无法核验关键财务数据。", limits)
        self.assertEqual(result["status"], "needs_review")
        self.assertIn("缺少采购合同。", result["unmatched_limitations"])

    def test_valid_paraphrase_is_not_declared_contradictory(self):
        result = delivery.assess_limitation_disclosure(
            "限制是无法从公开资料确认收入。", ["关键财务数据无法核验。"])
        self.assertEqual(result["status"], "needs_review")

    def test_qualified_denials_and_double_negatives_remain_valid(self):
        for message in ("报告并非没有任何限制：收入无法核验。",
                        "The report is not without limitations: revenue is unverified.",
                        "已知限制是收入无法核验，没有其他限制。",
                        "Revenue is unverified; no additional limitations were found."):
            with self.subTest(message=message):
                result = delivery.assess_limitation_disclosure(message, ["收入无法核验。"])
                self.assertNotEqual(result["status"], "contradiction")

    def test_distinct_english_paragraphs_are_not_repetition(self):
        lines = ["Revenue increased as customers renewed their annual contracts.",
                 "The engineering team reduced latency through better scheduling.",
                 "Policy uncertainty may delay procurement decisions next year."]
        self.assertEqual(evaluator.repeated_line_flags("\n".join(lines)), [])
        with (self.root / "final.md").open("a", encoding="utf-8") as out:
            out.write("\n\n" + "\n\n".join(lines))
        self.assert_both_pass()

    def test_real_english_repetition_still_fails(self):
        line = "Revenue increased as customers renewed their annual contracts."
        self.assertTrue(evaluator.repeated_line_flags("\n".join([line] * 3)))

    def test_distinct_chinese_control(self):
        lines = ["收入增长主要来自存量客户续约，但新增客户的获客成本尚未披露。",
                 "工程团队通过重新分配计算任务降低了延迟，具体改善幅度仍需测量。",
                 "政策变化可能影响下一年度采购节奏，企业应区分预算批准和实际签约。"]
        self.assertEqual(evaluator.repeated_line_flags("\n".join(lines)), [])

    def test_citation_variation_does_not_hide_chinese_repetition(self):
        text = "\n".join(f"《资料{i}》显示当前市场规模变化，但其口径不够明确，需要进一步核对。" for i in range(3))
        self.assertTrue(evaluator.repeated_line_flags(text))


if __name__ == "__main__":
    if os.environ.get("IRF_TEST_TMPDIR"):
        tempfile.tempdir = os.environ["IRF_TEST_TMPDIR"]
    unittest.main(verbosity=2)
