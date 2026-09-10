#!/usr/bin/env python3
"""Validate diagnostic data structure, never infer semantic correctness from labels."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
FILES = ('cases.json', 'additional-cases.json')
READER_CASES = 'reader-cases-2026-09-10.json'
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

def load_history():
    return [(name, json.loads((ROOT / 'evals/semantic_diagnostics' / name).read_text(encoding='utf-8')))
            for name in FILES]

def case_digest(case):
    return hashlib.sha256(json.dumps(case,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def apply_revisions(documents, revision_document):
    validate_catalog(documents)
    if (type(revision_document.get('schema_version')) is not int or revision_document['schema_version']!=1
        or revision_document.get('purpose')!='diagnostic_only'
        or revision_document.get('labels')!='author_proposed_uncalibrated'
        or revision_document.get('held_out') is not False
        or revision_document.get('automatic_quality_scoring') is not False):
        raise ValueError('Revision claim boundary changed')
    revisions=revision_document.get('revisions')
    if not isinstance(revisions,list) or not revisions: raise ValueError('Missing revisions')
    result=copy.deepcopy(documents)
    lookup={c['id']:c for _,d in result for c in d['cases']}
    seen=set()
    for revision in revisions:
        if not isinstance(revision,dict): raise ValueError('Invalid revision')
        target=revision.get('case_id')
        if target not in lookup or target in seen: raise ValueError('Unknown or duplicate revision target')
        seen.add(target)
        case=lookup[target]
        if case_digest(case)!=revision.get('base_case_sha256'): raise ValueError('Revision base changed')
        identifier=revision.get('revision_id')
        if not isinstance(identifier,str) or not re.fullmatch(re.escape(target)+r'_r[2-9][0-9]*',identifier):
            raise ValueError('Invalid revision identity')
        changes=revision.get('changes')
        if not isinstance(changes,dict) or not changes or set(changes)-{'evidence','bad','control','expected_failure','control_boundary'}:
            raise ValueError('Invalid revision fields')
        if not isinstance(revision.get('reason'),str) or not revision['reason'].strip(): raise ValueError('Missing revision reason')
        case.update(changes)
        case['revision_id']=identifier
    validate_catalog(result)
    return result

def load_revisions():
    return json.loads((ROOT/'evals/semantic_diagnostics/revisions.json').read_text(encoding='utf-8'))

def load_catalog():
    """Current development view; raw historical files are never overwritten."""
    current = apply_revisions(load_history(), load_revisions())
    current.append((READER_CASES, json.loads(
        (ROOT / 'evals/semantic_diagnostics' / READER_CASES).read_text(encoding='utf-8'))))
    validate_catalog(current)
    return current

class DiagnosticDataTests(unittest.TestCase):
    def setUp(self):
        self.documents = copy.deepcopy(load_catalog())

    def test_current_catalog(self):
        self.assertEqual(len(validate_catalog(self.documents)), 23)

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
        self.assertEqual(len(validate_catalog(self.documents)), 23)

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

    def test_history_unchanged_by_materialization(self):
        history=load_history(); before=copy.deepcopy(history)
        current=apply_revisions(history,load_revisions())
        self.assertEqual(history,before)
        self.assertIn('4次可用结果',history[0][1]['cases'][0]['control'])
        self.assertIn('不等于4个整体可用结果',current[0][1]['cases'][0]['control'])

    def test_revision_parent_tamper_rejected(self):
        history=load_history(); history[0][1]['cases'][0]['control']+='changed'
        with self.assertRaises(ValueError): apply_revisions(history,load_revisions())

    def test_unknown_revision_target_rejected(self):
        revisions=load_revisions(); revisions['revisions'][0]['case_id']='not_an_existing_case'
        with self.assertRaises(ValueError): apply_revisions(load_history(),revisions)

    def test_duplicate_revision_rejected(self):
        revisions=load_revisions(); revisions['revisions'].append(copy.deepcopy(revisions['revisions'][0]))
        with self.assertRaises(ValueError): apply_revisions(load_history(),revisions)

    def test_revision_cannot_change_case_identity(self):
        revisions=load_revisions(); revisions['revisions'][0]['changes']['id']='new_case'
        with self.assertRaises(ValueError): apply_revisions(load_history(),revisions)

    def test_revision_cannot_claim_calibration(self):
        revisions=load_revisions(); revisions['labels']='human_calibrated'
        with self.assertRaises(ValueError): apply_revisions(load_history(),revisions)

    def test_unchanged_cases_preserved(self):
        history={c['id']:c for _,d in load_history() for c in d['cases']}
        current={c['id']:c for _,d in load_catalog() for c in d['cases']}
        revised={r['case_id'] for r in load_revisions()['revisions']}
        self.assertTrue(set(history) <= set(current))
        self.assertEqual(len(set(current) - set(history)), 3)
        for identifier in history.keys()-revised: self.assertEqual(history[identifier],current[identifier])

    def test_reader_pairs_are_separate_from_twenty_historical_inputs(self):
        self.assertEqual(len(validate_catalog(load_history())), 20)
        self.assertEqual(self.documents[-1][0], READER_CASES)
        self.assertEqual(len(self.documents[-1][1]['cases']), 3)
        self.assertTrue(all(c['critical_fact_failure'] is False for c in self.documents[-1][1]['cases']))

    def test_reader_pair_cannot_reuse_historical_identity(self):
        self.documents[-1][1]['cases'][0]['id'] = self.documents[0][1]['cases'][0]['id']
        with self.assertRaises(ValueError): validate_catalog(self.documents)

    def test_reader_pairs_cannot_be_promoted_to_heldout_or_measured_quality(self):
        for key in ('held_out', 'automatic_quality_scoring'):
            documents = copy.deepcopy(self.documents)
            documents[-1][1][key] = True
            with self.assertRaises(ValueError): validate_catalog(documents)

if __name__ == '__main__':
    if sys.argv[1:]==['--show-current']:
        print(json.dumps({'notice':'Current author-proposed development cases, not calibrated labels',
                          'cases':[c for _,d in load_catalog() for c in d['cases']]},ensure_ascii=False,indent=2))
        raise SystemExit(0)
    ids = validate_catalog(load_catalog())
    print(f'{len(ids)} development pairs parsed; semantic correctness and research quality NOT evaluated.')
    unittest.main()
