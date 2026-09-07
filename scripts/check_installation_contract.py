#!/usr/bin/env python3
"""Positive and negative installation-comparison controls; temporary data only."""
from __future__ import annotations
import os
from pathlib import Path
import tempfile
import unittest
import check_installation as checker


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="irf-install-check-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.payload = {"SKILL.md": "研究规范\n".encode("utf-8")}
        (self.root / "SKILL.md").write_bytes(self.payload["SKILL.md"])

    def test_matching_payload(self):
        self.assertTrue(checker.compare_payload(self.root, self.payload)["payload_matches"])

    def test_newlines_do_not_create_a_false_variant(self):
        (self.root / "SKILL.md").write_bytes(self.payload["SKILL.md"].replace(b"\n", b"\r\n"))
        self.assertTrue(checker.compare_payload(self.root, self.payload)["payload_matches"])

    def test_modified_file_is_not_hidden_by_version_metadata(self):
        (self.root / "SKILL.md").write_text("local variant\n", encoding="utf-8")
        (self.root / "INSTALLATION.json").write_text('{"version":"v0.1.0"}', encoding="utf-8")
        result = checker.compare_payload(self.root, self.payload)
        self.assertFalse(result["payload_matches"])
        self.assertEqual(result["files"][0]["status"], "modified")

    def test_missing_required_file_is_visible(self):
        payload = {**self.payload, "references/writing-style.md": b"reference\n"}
        result = checker.compare_payload(self.root, payload)
        self.assertFalse(result["payload_matches"])
        self.assertEqual(result["files"][1]["status"], "missing_or_unreadable")

    def test_extra_local_files_are_ignored_and_not_modified(self):
        extra = self.root / "private-local-note.txt"
        extra.write_text("keep unchanged", encoding="utf-8")
        before = {path.name: path.read_bytes() for path in self.root.iterdir()}
        self.assertTrue(checker.compare_payload(self.root, self.payload)["payload_matches"])
        self.assertEqual(before, {path.name: path.read_bytes() for path in self.root.iterdir()})


if __name__ == "__main__":
    if os.environ.get("IRF_TEST_TMPDIR"):
        tempfile.tempdir = os.environ["IRF_TEST_TMPDIR"]
    unittest.main(verbosity=2)
