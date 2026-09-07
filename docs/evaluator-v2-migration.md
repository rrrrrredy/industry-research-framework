# Evaluator schema v2 migration

Schema v2 makes the existing evidence boundary explicit: passing mechanical conformance is not a research-quality verdict.

| Earlier field | Schema v2 field |
| --- | --- |
| `status` | `conformance_status` |
| `score` | `conformance_score` |
| `max_score` | `max_conformance_score` |
| `quality_flags` | `conformance_flags` |
| No explicit quality boundary | `research_quality_status: not_evaluated` |
| No schema identifier | `result_schema_version: 2` |

`coverage_flags` remains available. A result can contain:

```json
{
  "result_schema_version": 2,
  "conformance_status": "pass",
  "conformance_score": 100,
  "max_conformance_score": 100,
  "conformance_flags": [],
  "coverage_flags": [],
  "research_quality_status": "not_evaluated"
}
```

Consumers should explicitly check the schema and use the conformance fields:

```python
assert result["result_schema_version"] == 2
mechanically_passed = result["conformance_status"] == "pass"
# Do not convert mechanically_passed into a factual or editorial quality claim.
```

The evaluator exits non-zero for `review`, `fail`, and missing required outputs by default. `--allow-review` permits an exploratory run to exit successfully with `review`; it does not change that result to `pass`.

Keep historical output unchanged and identify its schema when importing it. Renaming a field does not retrospectively establish research quality. The standalone delivery checker uses a different `ok`/`flags` contract; do not parse it as an evaluator result.
