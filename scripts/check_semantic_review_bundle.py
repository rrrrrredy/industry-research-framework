#!/usr/bin/env python3
"""Check the dated semantic-review evidence, not the correctness of its labels."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile

from check_semantic_diagnostics import apply_revisions

DEFAULT=Path(__file__).resolve().parents[1]/'evals/semantic_diagnostics/reviews/2026-09-08'
JOBS=('batch-01','batch-02','order-control','revised-controls-02')
PROVIDERS=('deepseek','kimi')
PURPOSE='semantic_review_diagnostics_not_accuracy'

def require(value, message):
    if not value: raise ValueError(message)


def text(path): return path.read_text(encoding='utf-8').replace('\r\n','\n').replace('\r','\n')
def digest(path): return hashlib.sha256(text(path).encode()).hexdigest()
def read(path): return json.loads(text(path))


def safe(root, name):
    require(isinstance(name,str) and bool(name), 'Missing referenced path')
    rel = PurePosixPath(name)
    require(not rel.is_absolute() and '..' not in rel.parts and '\\' not in name and ':' not in name,
            'Unsafe referenced path')
    path = (root/name).resolve()
    require(path.is_relative_to(root), 'Referenced file escapes bundle')
    return path


def observations(root):
    mapping=read(root/'mapping.json')['jobs']
    rows=[]
    for provider in PROVIDERS:
        for job in JOBS[:3]:
            answer=read(root/f'finals/{provider}/{job}.json')['parsed']
            lookup={x['id']:x for x in answer['cases']}
            for item in mapping[job]:
                for label in ('A','B'):
                    value=lookup[item['id']][label]
                    rows.append({'provider':provider,'job':job,'case_id':item['original_id'],
                        'variant':item[label],'display':label,'judgment':value['judgment'],
                        'critical_fact_error':value['critical_fact_error']})
    return rows

def check_bundle(root):
    try:
        root=root.resolve()
        manifest=read(root/'bundle-manifest.json')
        require(manifest['schema_version']==1 and manifest['purpose']==PURPOSE,'Wrong semantic bundle type')
        files=manifest['files']
        require(isinstance(files,dict) and bool(files),'Empty inventory')
        require({p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}==set(files)|{'bundle-manifest.json'},
                'Missing or unlisted public file')
        for name,h in files.items():
            path=safe(root,name)
            require(digest(path)==h,'Stale file: '+name)
            if path.suffix=='.json': read(path)
            for pattern in (r'(?<![A-Za-z0-9])[A-Za-z]:[/\\]',r'(?i)\bsk-[A-Za-z0-9_-]{12,}',
                            r'(?i)\bgh[pousr]_[A-Za-z0-9_]{20,}',r'"(?:authorization|api_key|reasoning_content)"\s*:',
                            r'<oai-mem-citation>',r'-----BEGIN .*PRIVATE KEY-----'):
                require(re.search(pattern,text(path)) is None,'Public-safety pattern: '+name)
        index=read(root/'run-index.json')
        require(index['purpose']==PURPOSE and index['schema_version']==1,'Wrong index scope')
        for key in ('held_out','human_calibrated','author_labels_are_truth'):
            require(index[key] is False,'Unproven claim: '+key)
        require(index['unique_original_pairs']==20 and index['revised_pairs']==2
                and index['additional_independent_tasks_from_revisions']==0,'Task count inflated')
        rows=index['records']
        require(index['attempts']==index['complete_responses']==len(rows)==8,'Eight actual calls required')
        require({(r['provider'],r['job']) for r in rows}=={(p,j) for p in PROVIDERS for j in JOBS},'Attempt coverage mismatch')
        original=read(root/'freeze.json'); revision=read(root/'revised-controls-freeze.json')
        for freeze in (original,revision):
            for name,h in freeze['files'].items():
                if name in ('run.py','run_revised_controls.py'): continue
                mapped={'mapping.private.json':'mapping.json','revised-controls-map.private.json':'revisions-mapping.json'}.get(name,name)
                require(digest(safe(root,mapped))==h,'Frozen input changed: '+mapped)
        for name,h in original['origins'].items(): require(digest(root/'source-catalogs'/name)==h,'Original catalog changed')
        require(digest(root/'source-catalogs/revisions.json')==revision['revisions_sha256'],'Revisions changed')
        history=[(n,read(root/'source-catalogs'/n)) for n in ('cases.json','additional-cases.json')]
        old={c['id']:c for _,d in history for c in d['cases']}
        current={c['id']:c for _,d in apply_revisions(history,read(root/'source-catalogs/revisions.json')) for c in d['cases']}
        mapping=read(root/'mapping.json')['jobs']
        correction=read(root/'revisions-mapping.json')
        require(correction['labels_are_truth'] is False,'Correction map claims truth')
        require(set(mapping)==set(JOBS[:3]),'Original mapping jobs changed')
        first=[r['original_id'] for j in JOBS[:2] for r in mapping[j]]
        require(len(first)==len(set(first))==20 and set(first)==set(old),'Original pair coverage changed')
        require(len(mapping['order-control'])==4 and len({r['original_id'] for r in mapping['order-control']})==4,'Invalid order subset')
        first_map={r['original_id']:r for j in JOBS[:2] for r in mapping[j]}
        for item in mapping['order-control']:
            require(item['A']==first_map[item['original_id']]['B'] and item['B']==first_map[item['original_id']]['A'],
                    'Repeat did not swap A/B')
        for row in rows:
            p,j=row['provider'],row['job']; prefix=f'{p}/{j}.json'
            require(row['input']==f'inputs/{j}.json' and row['attempt']==f'attempts/{prefix}'
                    and row['final']==f'finals/{prefix}' and row['request']==f'requests/{prefix}','Wrong call paths')
            inp=read(safe(root,row['input'])); attempt=read(safe(root,row['attempt']))
            request=read(safe(root,row['request'])); final=read(safe(root,row['final']))
            require(attempt['task']==j and attempt['status']=='response_complete','Completed call replaced or lost')
            require(attempt['input_sha256']==final['input_sha256']==digest(safe(root,row['input'])),'Input binding mismatch')
            require(request['messages']==[{'role':'system','content':inp['system']},{'role':'user','content':inp['user']}],'Request mismatch')
            model='deepseek-v4-pro' if p=='deepseek' else 'kimi-k3'
            require(request['model']==attempt['model_requested']==attempt['model_returned']==final['model_returned']==model,'Model mismatch')
            require(attempt['valid_json_object'] is True and attempt['task_schema_complete'] is True
                    and attempt['model_identity_expected'] is True,'Incomplete or unexpected response relabeled')
            cap='max_tokens' if p=='deepseek' else 'max_completion_tokens'
            require(request[cap]==attempt['max_output_tokens']==32768,'Output cap mismatch')
            require(attempt['usage']==final['usage'] and final['finish_reason']=='stop','Terminal usage mismatch')
            require(final['external_fact_check'] is False,'Text review claims external verification')
            require(attempt['cumulative_liability_after_reservation_cny']<=50,'Budget ceiling exceeded')
            require(json.loads(final['content'])==final['parsed'],'Visible/parsed reply mismatch')
            shown=json.loads(inp['user'].split('\nReturn JSON ',1)[0])
            maps=correction['items'] if j==JOBS[-1] else mapping[j]
            cases=current if j==JOBS[-1] else old
            expected=2 if j==JOBS[-1] else 4 if j=='order-control' else 10
            ids={f'item-{i:02}' for i in range(1,expected+1)}
            require(len(shown)==len(maps)==len(final['parsed']['cases'])==expected,'Wrong excerpt count')
            require({s['id'] for s in shown}=={m['id'] for m in maps}=={c['id'] for c in final['parsed']['cases']}==ids,'Duplicate or missing item')
            by_id={s['id']:s for s in shown}
            for m in maps:
                c=cases[m['case_id'] if j==JOBS[-1] else m['original_id']]
                if j==JOBS[-1]: require(m['revision_id']==c['revision_id'],'Revision identity mismatch')
                require({m['A'],m['B']}=={'bad','control'},'Invalid masked variants')
                require(by_id[m['id']]=={'id':m['id'],'evidence':c['evidence'],'A':c[m['A']],'B':c[m['B']]},'Excerpt differs from frozen variant')
            for item in final['parsed']['cases']:
                for label in ('A','B'):
                    v=item[label]
                    require(v['judgment'] in {'acceptable','flawed','insufficient_context'} and type(v['critical_fact_error']) is bool,
                            'Invalid judgment schema')
                    require(isinstance(v['reason'],str) and bool(v['reason'].strip()) and isinstance(v['evidence_boundary'],str)
                            and bool(v['evidence_boundary'].strip()),'Missing reason or boundary')
        analysis=read(root/'analysis.json'); obs=observations(root)
        require(analysis['observations']==obs and analysis['human_calibrated'] is False and analysis['held_out'] is False,'Analysis changed observations/claims')
        first={(r['provider'],r['case_id'],r['variant']):r for r in obs if r['job']!='order-control'}
        require(analysis['first_pass_excerpt_judgments']==len(first)==80 and analysis['repeat_excerpt_judgments']==16,'Observation counts changed')
        agreement=sum(r['judgment']==('flawed' if r['variant']=='bad' else 'acceptable') for r in first.values())
        require(analysis['first_pass_agreement_with_author_variant_labels']==agreement,'Agreement count changed')
        changes=[]
        for r in obs:
            if r['job']!='order-control': continue
            prior=first[r['provider'],r['case_id'],r['variant']]
            if (prior['judgment'],prior['critical_fact_error'])!=(r['judgment'],r['critical_fact_error']):
                changes.append({'provider':r['provider'],'case_id':r['case_id'],'variant':r['variant'],
                    'first_judgment':prior['judgment'],'repeat_judgment':r['judgment'],
                    'first_critical':prior['critical_fact_error'],'repeat_critical':r['critical_fact_error']})
        require(analysis['repeat_changes']==changes,'Repeat disagreement omitted')
        disagreements=[]; severity=[]
        for (p,c,v),r in first.items():
            if p=='deepseek':
                other=first['kimi',c,v]
                if (r['judgment'],r['critical_fact_error'])!=(other['judgment'],other['critical_fact_error']):
                    disagreements.append({'case_id':c,'variant':v,'deepseek':r,'kimi':other})
            if v=='bad' and r['critical_fact_error']!=old[c]['critical_fact_failure']:
                severity.append({'provider':p,'case_id':c,'model_critical':r['critical_fact_error'],
                                 'author_proposed_critical':old[c]['critical_fact_failure']})
        require(analysis['between_reviewer_disagreements']==disagreements,'Between-reviewer disagreement omitted')
        require(analysis['critical_flag_disagreements_with_author']==severity,'Severity disagreement omitted')
        require(analysis['purpose']=='descriptive_diagnostics_not_accuracy' and analysis['unique_original_pairs']==20
                and analysis['original_attempts']==6,'Original diagnostic scope changed')
        return []
    except (OSError,UnicodeError,ValueError,KeyError,TypeError,AttributeError,IndexError) as exc: return [str(exc)]

def self_test(root):
    require(not check_bundle(root),'Known-good evidence must pass')
    cases=('unlisted','lost_attempt','fake_truth','task_inflation','map','input','request','parsed','analysis',
           'between_disagreement','severity_disagreement','privacy','invalid_json')
    with tempfile.TemporaryDirectory(prefix='irf-semantic-review-') as folder:
        for case in cases:
            trial=Path(folder)/case; shutil.copytree(root,trial)
            name='run-index.json'; value=read(trial/name); raw=None
            if case=='unlisted': (trial/'unexpected.txt').write_text('not listed',encoding='utf-8')
            elif case=='lost_attempt': value['records'].pop()
            elif case=='fake_truth': value['author_labels_are_truth']=True
            elif case=='task_inflation': value['additional_independent_tasks_from_revisions']=2
            elif case=='map': name='mapping.json'; value=read(trial/name); value['jobs']['batch-01'][0]['A']='bad'; value['jobs']['batch-01'][0]['B']='bad'
            elif case=='input': name='inputs/batch-01.json'; value=read(trial/name); value['user']+='changed'
            elif case=='request': name='requests/kimi/batch-01.json'; value=read(trial/name); value['messages'][1]['content']='changed'
            elif case=='parsed': name='finals/deepseek/batch-01.json'; value=read(trial/name); value['parsed']['cases'][0]['A']['judgment']='invented'
            elif case=='analysis': name='analysis.json'; value=read(trial/name); value['repeat_changes']=[]
            elif case=='between_disagreement': name='analysis.json'; value=read(trial/name); value['between_reviewer_disagreements']=[]
            elif case=='severity_disagreement': name='analysis.json'; value=read(trial/name); value['critical_flag_disagreements_with_author']=[]
            elif case=='privacy': name='README.md'; raw=text(trial/name)+'\nD:/private/example.txt\n'
            elif case=='invalid_json': raw='{broken'
            if case!='unlisted':
                (trial/name).write_text(raw if raw is not None else json.dumps(value,ensure_ascii=False),encoding='utf-8')
                m=read(trial/'bundle-manifest.json'); m['files'][name]=digest(trial/name)
                (trial/'bundle-manifest.json').write_text(json.dumps(m),encoding='utf-8')
            require(bool(check_bundle(trial)),'Negative control accepted: '+case)
    print(f'PASS: real semantic-review bundle and {len(cases)} isolated negative controls; labels remain uncalibrated')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('bundle',type=Path,nargs='?',default=DEFAULT); p.add_argument('--self-test',action='store_true')
    args=p.parse_args(); errors=check_bundle(args.bundle)
    if errors: print('FAIL: '+'; '.join(errors)); raise SystemExit(1)
    if args.self_test: self_test(args.bundle)
    else: print('PASS: 8 model calls and frozen case bindings intact; no accuracy claim')
