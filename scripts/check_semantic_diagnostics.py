#!/usr/bin/env python3
"""Validate diagnostic data structure, never infer semantic correctness from labels."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
FILES = ('cases.json', 'additional-cases.json')
TEXT_FIELDS = ('id', 'focus', 'evidence', 'bad', 'control', 'expected_failure', 'control_boundary')

def validate_catalog(documents):
    identifiers = set()
    for name, document in documents:
        if not isinstance(document, dict):
            raise ValueError(f'{name}: expected object')
        if (type(document.get('schema_version')) is not int or document.get('schema_version') != 1
                or document.get('purpose') != 'diagnostic_only'
                or document.get('labels') != 'author_proposed_uncalibrated'
                or document.get('held_out') is not False
                or document.get('automatic_quality_scoring') is not False):
            raise ValueError(f'{name}: diagnostic-only claim boundary changed')
        cases = document.get('cases')
        if not isinstance(cases, list) or not cases:
            raise ValueError(f'{name}: nonempty cases required')
        for index, case in enumerate(cases):
            if not isinstance(case, dict):
                raise ValueError(f'{name}:{index}: expected case object')
            for key in TEXT_FIELDS:
                if not isinstance(case.get(key), str) or not case[key].strip():
                    raise ValueError(f'{name}:{index}: missing {key}')
            if not re.fullmatch(r'[a-z][a-z0-9_]*', case['id']):
                raise ValueError(f'{name}:{index}: id must be a canonical lowercase identifier')
            if case['id'] in identifiers:
                raise ValueError(f'duplicate diagnostic id: {case["id"]}')
            identifiers.add(case['id'])
            if type(case.get('critical_fact_failure')) is not bool:
                raise ValueError(f'{name}:{index}: critical_fact_failure must be boolean')
            if case['bad'].strip() == case['control'].strip():
                raise ValueError(f'{name}:{index}: identical bad and control excerpts')
    return identifiers

def load_catalog():
    return [(name, json.loads((ROOT / 'evals/semantic_diagnostics' / name).read_text(encoding='utf-8')))
            for name in FILES]

class DiagnosticDataTests(unittest.TestCase):
    def setUp(self):
        self.documents = copy.deepcopy(load_catalog())

    def test_current_catalog(self):
        self.assertEqual(len(validate_catalog(self.documents)), 20)

    def test_original_six_preserved(self):
        self.assertEqual(len(self.documents[0][1]['cases']), 6)

    def test_duplicate_across_files(self):
        self.documents[1][1]['cases'][0]['id'] = self.documents[0][1]['cases'][0]['id']
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_missing_control(self):
        del self.documents[1][1]['cases'][0]['control']
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_missing_evidence(self):
        self.documents[1][1]['cases'][0]['evidence'] = ' '
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_identical_excerpts(self):
        case = self.documents[1][1]['cases'][0]
        case['control'] = case['bad']
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_no_automatic_quality_promotion(self):
        self.documents[0][1]['automatic_quality_scoring'] = True
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_no_heldout_promotion(self):
        self.documents[0][1]['held_out'] = True
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_string_boolean_rejected(self):
        self.documents[0][1]['cases'][0]['critical_fact_failure'] = 'false'
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_count_does_not_establish_quality(self):
        self.documents[0][1]['cases'][0]['control'] = 'An author-proposed label can still be wrong.'
        self.assertEqual(len(validate_catalog(self.documents)), 20)

    def test_boolean_schema_rejected(self):
        self.documents[0][1]['schema_version'] = True
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_nonlist_cases_rejected(self):
        self.documents[0][1]['cases'] = {'id': 'not_a_case_list'}
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_noncanonical_identifier_rejected(self):
        self.documents[0][1]['cases'][0]['id'] += ' '
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_missing_boundary_rejected(self):
        del self.documents[0][1]['cases'][0]['control_boundary']
        with self.assertRaises(ValueError): validate_catalog(self.documents)

if __name__ == '__main__':
    ids = validate_catalog(load_catalog())
    print(f'{len(ids)} development pairs parsed; semantic correctness and research quality NOT evaluated.')
    unittest.main()
