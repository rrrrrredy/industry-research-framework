#!/usr/bin/env python3
"""Offline controls for source purpose, exact curation, and regeneration; not semantic fact scoring."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import build_sanitized_eval_set as builder
import check_eval_source_integrity as checker

REPO = Path(__file__).resolve().parents[1]


class SourcePolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="irf-source-policy-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.policies = checker.read_source_policy(REPO / "evals/source_policy.json")
        self.policy = self.policies["ai_knowledge_sanitized"]
        self.sources = checker.read_jsonl(REPO / "evals/source_packs/ai_knowledge_sanitized/sources.jsonl")

    def run_checker(self, *args):
        return subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(REPO / "scripts/check_eval_source_integrity.py"), *args],
            capture_output=True, text=True, encoding="utf-8", check=False,
        )

    def uncurated_sources(self):
        rows = copy.deepcopy(self.sources)
        for item in self.policy["excluded_claims"]:
            row = next(value for value in rows if value["source_id"] == item["source_id"])
            if item["field"] == "key_points":
                row["key_points"].append(item["text"])
            else:
                row["summary"] += item["text"]
        return rows

    def test_current_workflow_inputs_pass(self):
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("workflow only", result.stdout)

    def test_current_inputs_cannot_be_called_factual_benchmark(self):
        result = self.run_checker("--purpose", "factual")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertEqual(result.stdout.count("not eligible for factual"), len(self.policies))
        self.assertNotIn("PASS:", result.stdout)

    def test_curation_is_exact_nonmutating_and_idempotent(self):
        rows = self.uncurated_sources()
        original = copy.deepcopy(rows)
        self.assertEqual(len(checker.excluded_claim_findings(rows, self.policy)), 3)
        curated = checker.apply_source_exclusions(rows, self.policy)
        self.assertEqual(rows, original)
        self.assertEqual(curated, self.sources)
        self.assertEqual(checker.apply_source_exclusions(curated, self.policy), curated)
        self.assertEqual(checker.excluded_claim_findings(curated, self.policy), [])

    def test_generator_cannot_resurrect_reviewed_claims(self):
        rows = self.uncurated_sources() + checker.read_jsonl(
            REPO / "evals/source_packs/ai_knowledge_sanitized/quarantined_sources.jsonl"
        )
        docs = [dict(row, id=row["source_id"]) for row in rows]
        data_dir = self.root / "data"
        data_dir.mkdir()
        (data_dir / "knowledge_base_public.json").write_text(json.dumps(docs, ensure_ascii=False), encoding="utf-8")
        active, quarantined, mapping = builder.build_sources(self.root, None)
        self.assertEqual(len(active), 9)
        self.assertEqual({row["source_id"] for row in quarantined}, {"S006", "S010", "S012"})
        self.assertEqual(checker.excluded_claim_findings(active, self.policy), [])
        for case in builder.build_cases(mapping):
            self.assertFalse(set(case["source_ids"]) & {"S006", "S010", "S012"})

    def test_reintroduced_claim_is_rejected_in_cli(self):
        target = self.root / "evals"
        shutil.copytree(REPO / "evals/source_packs", target / "source_packs")
        shutil.copyfile(REPO / "evals/source_policy.json", target / "source_policy.json")
        path = target / "source_packs/ai_knowledge_sanitized/sources.jsonl"
        path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in self.uncurated_sources()) + "\n", encoding="utf-8")
        result = self.run_checker("--evals-dir", str(target))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("excluded claim was reintroduced", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_missing_policy_is_not_assumed_safe(self):
        result = self.run_checker("--evals-dir", str(self.root))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source policy failure", result.stdout)

    def test_policy_cannot_self_certify_factual_quality(self):
        policy = checker.read_json(REPO / "evals/source_policy.json")
        policy["packs"]["ai_knowledge_sanitized"]["factual_authority"] = True
        path = self.root / "source_policy.json"
        path.write_text(json.dumps(policy), encoding="utf-8")
        with self.assertRaises(ValueError):
            checker.read_source_policy(path)

    def test_invalid_manifest_shape_is_reported_without_traceback(self):
        target = self.root / "evals"
        shutil.copytree(REPO / "evals/source_packs", target / "source_packs")
        shutil.copyfile(REPO / "evals/source_policy.json", target / "source_policy.json")
        (target / "source_packs/ai_knowledge_sanitized/manifest.json").write_text("[]\n", encoding="utf-8")
        result = self.run_checker("--evals-dir", str(target))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("manifest must be an object", result.stdout)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    if os.environ.get("IRF_TEST_TMPDIR"):
        tempfile.tempdir = os.environ["IRF_TEST_TMPDIR"]
    unittest.main(verbosity=2)
