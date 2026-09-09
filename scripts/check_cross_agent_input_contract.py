#!/usr/bin/env python3
"""Controls for immutable historical inputs, including working-tree evolution."""
from pathlib import Path
import os
import tempfile
import unittest
import warnings
import zipfile

import check_cross_agent_protocol as checker


class FrozenInputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="irf-frozen-input-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.archive = self.root / "evals/cross_agent/frozen-inputs-v1.zip"
        self.archive.parent.mkdir(parents=True)
        self.content = b"Frozen study instructions\n"
        self.paths = ["SKILL.md"]
        self.lock = {"SKILL.md": checker.sha256_content(Path("SKILL.md"), self.content)}

    def write_archive(self, entries):
        with zipfile.ZipFile(self.archive, "w") as archive:
            for name, content in entries:
                archive.writestr(name, content)

    def errors(self):
        errors = []
        checker.validate_frozen_inputs(self.root, self.paths, self.lock, errors)
        return errors

    def test_unchanged_archive_survives_live_framework_update(self):
        self.write_archive([("SKILL.md", self.content)])
        (self.root / "SKILL.md").write_text("New research framework\n", encoding="utf-8")
        self.assertEqual(self.errors(), [])

    def test_archive_text_newline_normalization_preserves_original_lock(self):
        self.write_archive([("SKILL.md", self.content.replace(b"\n", b"\r\n"))])
        self.assertEqual(self.errors(), [])

    def test_changed_archive_is_rejected_even_when_live_file_matches(self):
        self.write_archive([("SKILL.md", b"Changed study instructions\n")])
        (self.root / "SKILL.md").write_bytes(self.content)
        self.assertIn("frozen input hash mismatch: SKILL.md", self.errors())

    def test_missing_archive_never_falls_back_to_live_input(self):
        (self.root / "SKILL.md").write_bytes(self.content)
        self.assertTrue(self.errors())

    def test_missing_and_extra_members_are_rejected(self):
        for entries in ([], [("SKILL.md", self.content), ("extra.md", b"extra")]):
            with self.subTest(entries=len(entries)):
                self.write_archive(entries)
                self.assertTrue(self.errors())

    def test_duplicate_member_is_rejected(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            self.write_archive([("SKILL.md", self.content), ("SKILL.md", self.content)])
        self.assertTrue(self.errors())

    def test_escaping_logical_path_is_rejected_without_extraction(self):
        self.paths = ["../outside.md"]
        self.lock = {self.paths[0]: checker.sha256_content(Path("outside.md"), self.content)}
        self.write_archive([(self.paths[0], self.content)])
        self.assertTrue(self.errors())
        self.assertFalse((self.root.parent / "outside.md").exists())

    def test_malformed_archive_is_rejected(self):
        self.archive.write_bytes(b"not a zip archive")
        self.assertTrue(self.errors())


if __name__ == "__main__":
    if os.environ.get("IRF_TEST_TMPDIR"):
        tempfile.tempdir = os.environ["IRF_TEST_TMPDIR"]
    unittest.main(verbosity=2)
