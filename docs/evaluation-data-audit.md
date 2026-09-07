# Evaluation data audit — 2026-09-07

The current data is suitable for the declared workflow exercises, not a public factual benchmark. Source integrity, semantic accuracy, provenance and reuse rights are different claims.

## What changed

- S006, S010 and S012 remain quarantined. Their summaries deny usable underlying content while their key points assert facts. Original records and reasons remain available; active cases do not reference them.
- S007 contained two undated weekly token totals, 4.12 and 5.16 trillion, without distinguishing observation weeks or the measured population. The numeric key point and summary sentence were excluded. This does not establish that both numbers are false; it establishes that the supplied record cannot resolve their scope.
- S011 attributed XGBoost to Tencent. The [original paper](https://arxiv.org/pdf/1603.02754) identifies Tianqi Chen and Carlos Guestrin at the University of Washington. The combined key point was excluded, not silently rewritten into a new source.
- The historical AI Agent taste anchor included AgentSDK-specific statements not supported by its four listed notes. Those assertions were removed. The inference from GUI benchmark difficulty to coding-agent maturity and the final all-or-nothing market criterion were narrowed.

The exact excluded text, reason and evidence are retained in [source_policy.json](../evals/source_policy.json); the original full rows also remain in the b541a667b89a4ea9da8fffd8d58851e5f03b795e Git snapshot. Source IDs and case mappings remain stable. The generator applies the same exact exclusions, and a regression reintroduces the original text to ensure it is rejected.

## Current inventory and use limits

| Pack | Active / quarantined | Available provenance | Permitted use |
| --- | --- | --- | --- |
| ai_knowledge_sanitized | 9 / 3 | Undated historical summaries; original public links unavailable | Workflow exercise only; not a current market or fact answer key |
| model_company_pipeline_synthetic | 8 / 0 | Repository-authored fictional companies and events | Synthetic workflow/reasoning exercise only |
| prompt_injection_synthetic | 1 / 0 | Repository-authored vendor facts and attack instructions | Configured source-boundary exercise only |

Seventeen active rows have no document date. A pack generation date is not a source publication date. Unknown dates and original-document rights have not been invented or certified. Sanitization is not proof of factual accuracy or permission to republish private originals. Any future factual benchmark needs independently traceable sources, dates, observation scope and an appropriate rights review.

## Residual-content review

The three quarantined records were compared with active cases and the reference prose, not just their IDs. Their distinctive price-war figures, ByteDance technology-stack list and OpenAI compensation/headcount/DERP assertions are not used by the active taste anchors. Generic ideas such as research–engineering coordination are not, by themselves, evidence of contamination. The two new exclusions are likewise absent from active anchors and case prompts.

This is a bounded content audit, not proof that every paraphrase or inherited claim has been found. All nine legacy active rows were read; many remaining dated-market and adoption claims still lack independently recoverable provenance. They remain explicitly non-authoritative. The eight-company synthetic case is not rehabilitated into evidence about actual companies.

## Verification

```bash
python scripts/check_eval_source_integrity.py
python scripts/check_source_policy_contract.py
python scripts/check_eval_source_integrity.py --purpose factual
```

The first command checks structure, references, permitted purpose and recurrence of the exact reviewed exclusions. The second includes positive controls, negative factual-use checks, an exact non-mutating/idempotent curation check and regeneration from reconstructed pre-curation inputs. The third must exit non-zero for the current packs; that is the expected result, not a failed factual study.

The source-use policy is an evaluation-data boundary, not a new research protocol schema. Frozen cross-agent files, the synthetic frozen source pack, SKILL.md and all references remain unchanged. Old runs keep their old input hashes; new runs must identify the new candidate rather than retroactively claiming these corrections.

中文结论：本轮清理的是已证实的错误归属、未解开的数字口径冲突和参考稿无来源支持的外推。其余未知项明确保留，不把“检查通过”包装成“数据完全正确、版权全部清楚”。
