#!/usr/bin/env python3
"""Check a dated public diagnostic bundle offline; never score research quality."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile

DEFAULT = Path(__file__).resolve().parents[1] / 'evals/diagnostics/2026-09-07'
PROVIDERS = ('astra', 'deepseek', 'kimi')
TASKS = ('semantic', 'customer-service', 'video-production')


def digest(path: Path) -> str:
    text = path.read_text(encoding='utf-8').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def check_bundle(root: Path) -> list[str]:
    """Fail closed on missing files, malformed data or contradictory run metadata."""
    try:
        root = root.resolve()
        manifest = read_json(root / 'bundle-manifest.json')
        require(manifest['schema_version'] == 1, 'Unknown bundle schema')
        require(manifest['purpose'] == 'development_diagnostics_not_efficacy', 'Wrong evidence scope')
        files = manifest['files']
        require(isinstance(files, dict) and bool(files), 'Missing file hashes')
        actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
        require(actual == set(files) | {'bundle-manifest.json'}, 'Missing or unlisted bundle file')
        for name, expected in files.items():
            rel = PurePosixPath(name)
            require(not rel.is_absolute() and '..' not in rel.parts and '\\' not in name, 'Unsafe bundle path')
            path = (root / name).resolve()
            require(path.is_relative_to(root), 'Bundle path resolves outside root')
            require(isinstance(expected, str) and re.fullmatch('[0-9a-f]{64}', expected) is not None, 'Invalid hash')
            require(digest(path) == expected, f'Stale bundle file: {name}')
            if path.suffix == '.json':
                read_json(path)

        inputs = read_json(root / 'model-input-manifest.json')
        require(inputs['held_out'] is False, 'Development inputs must not become held-out evidence')
        summary = read_json(root / 'summary.json')
        records = summary['records']
        pairs = [(row['provider'], row['task']) for row in records]
        require(len(pairs) == 9 and set(pairs) == {(p, t) for p in PROVIDERS for t in TASKS},
                'Keep exactly all nine original attempts, including incomplete responses')
        require(summary['attempt_count'] == len(records), 'Attempt count disagrees with records')
        complete = 0
        failures = set()
        for row in records:
            provider, task = row['provider'], row['task']
            frozen = inputs['input_sha256'][task]
            require(digest(root / f'inputs/{task}.json') == frozen, 'Frozen input changed')
            require(row['input_sha256'] == frozen, 'Attempt bound to a different input')
            final = read_json(root / f'results/{provider}/{task}.json')
            require(final['input_sha256'] == frozen, 'Final reply bound to a different input')
            require(final['external_fact_check'] is False, 'Text review cannot claim external fact checks')
            if row['status'] == 'response_complete':
                require(isinstance(final['parsed'], dict), 'Complete response needs parsed final JSON')
                require(json.loads(final['content']) == final['parsed'], 'Stored final content and parsed result differ')
                complete += 1
            else:
                require(row['status'] == 'response_needs_inspection', 'Unknown attempt status')
                require(final['finish_reason'] == 'length' and final['parsed'] is None and final['content'] == '',
                        'Do not replace the preserved incomplete response with a verdict')
                failures.add((provider, task))
            if provider != 'astra':
                request = read_json(root / f'requests/{provider}/{task}.json')
                source = read_json(root / f'inputs/{task}.json')
                require(request['messages'] == [{'role': 'system', 'content': source['system']},
                                                {'role': 'user', 'content': source['user']}], 'Request differs from frozen input')
                require(request['model'] == row['model_requested'] == final['model_returned'], 'Model identity fields disagree')
        require(summary['complete_responses'] == complete == 8, 'Complete-response count disagrees')
        require({(r['provider'], r['task']) for r in summary['failures']} == failures == {('kimi', 'video-production')},
                'Incomplete-response summary missing or changed')
        require(summary['human_reviews'] == 0, 'No human reviews were completed in this diagnostic')
        return []
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, AttributeError) as exc:
        return [str(exc)]


def self_test(root: Path) -> int:
    """Reseal mutated files so unrelated hashes do not mask metadata defects."""
    require(not check_bundle(root), 'Known-good public bundle must pass before mutation tests')
    with tempfile.TemporaryDirectory(prefix='irf-diagnostic-contract-') as scratch:
        for case in ('tampered_text', 'missing_failure', 'parsed_disagreement', 'unlisted_file', 'invalid_json'):
            trial = Path(scratch) / case
            shutil.copytree(root, trial)
            changed = None
            if case == 'tampered_text':
                path = trial / 'reports/customer-service/repaired.md'
                path.write_text(path.read_text(encoding='utf-8') + '\nChanged\n', encoding='utf-8')
            elif case == 'missing_failure':
                changed = 'summary.json'
                value = read_json(trial / changed)
                value['failures'] = []
                (trial / changed).write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
            elif case == 'parsed_disagreement':
                changed = 'results/astra/customer-service.json'
                value = read_json(trial / changed)
                value['parsed']['verdict'] = 'invented_replacement'
                (trial / changed).write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
            elif case == 'unlisted_file':
                (trial / 'unexpected.txt').write_text('must not be silently omitted', encoding='utf-8')
            else:
                changed = 'summary.json'
                (trial / changed).write_text('{malformed', encoding='utf-8')
            if changed:
                manifest = read_json(trial / 'bundle-manifest.json')
                manifest['files'][changed] = digest(trial / changed)
                (trial / 'bundle-manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
            require(bool(check_bundle(trial)), f'Negative control unexpectedly passed: {case}')
    print('PASS: 1 positive and 5 isolated negative bundle controls; no quality verdict')
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', type=Path, nargs='?', default=DEFAULT)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    findings = check_bundle(args.bundle)
    if findings:
        for finding in findings:
            print('FAIL: ' + finding)
        return 1
    if args.self_test:
        return self_test(args.bundle)
    print('PASS: dated bundle intact; 9 attempts, 8 complete replies, 1 preserved incomplete response; no quality verdict')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
