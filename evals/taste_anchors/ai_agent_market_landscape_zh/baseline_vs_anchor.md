# Baseline vs Taste Anchor: AI Agent Market Landscape

> Provenance note: this is a retrospective taste-calibration note. The original requests, full responses, model snapshot, and complete run artifacts were not retained, so it is not an A/B pilot result and must not be used as evidence of framework efficacy.

## Baseline Pattern

The first baseline run was mechanically compliant: it created state files, registries, review logs, expected headings, reader-facing source titles, and uncertainty language. The deterministic runner initially gave this style a passing score.

But the output was not good enough. It had three recurring problems:

- **Process leakage**: phrases such as "source pack", "脱敏评测", and "用于检验研究流程" appeared in the final report.
- **Source listing instead of synthesis**: many paragraphs followed the pattern "source X says Y; this can support trend recognition". That proves traceability but does not produce a thesis.
- **Over-listing**: the report was dominated by bullets, so the reader had to do the synthesis work.

## Taste Anchor Pattern

The high-quality anchor still respects the framework, but it behaves differently:

- **Thesis first**: the report opens with a market judgment, not a method note.
- **Evidence is integrated**: source titles are used where useful, but the body explains mechanisms across sources.
- **Claims are bounded cleanly**: adoption, ROI, permissions, reliability, and cost are separated from product-release facts.
- **Counter-evidence is part of the argument**: the report explains how Agent could remain enhanced automation instead of becoming a new software entry point.
- **Reader-facing prose**: the final piece reads like a research memo, not a test run.

## Rubric Implications

The rubric and deterministic runner should not reward artifact completeness alone. A passing output should also:

- avoid eval/process language in `final.md`
- avoid internal source ids in `final.md`
- keep bullet density moderate
- avoid repeated source-listing templates
- explain mechanisms and tradeoffs across sources
- make counter-evidence analytical rather than ceremonial
- include reader-facing source titles only where they help the reader

## 中文总结

模板基线的问题不是“不合规”，而是“只合规”。它完成了状态文件、台账、标题和引用，但读起来像一份测试输出。Taste anchor 的差异在于：先给判断，再把来源融合进机制分析，最后把反证和不确定性变成论证的一部分。
