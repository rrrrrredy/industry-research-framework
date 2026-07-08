# Taste Anchors

Taste anchors are human-readable examples used to calibrate the evaluation loop. They are not gold answers and should not be treated as model training data. Their job is to show the difference between mechanical conformance and publishable research quality.

## Anchors

- [`ai_agent_market_landscape_zh/high_quality.md`](./ai_agent_market_landscape_zh/high_quality.md): a reader-facing, thesis-led Chinese sample for the AI Agent market landscape case.
- [`ai_agent_market_landscape_zh/baseline_vs_anchor.md`](./ai_agent_market_landscape_zh/baseline_vs_anchor.md): comparison between a template-compliant baseline and the taste anchor.

## How To Use

1. Run the deterministic evaluator.
2. Inspect one or two outputs manually.
3. Compare them against the nearest taste anchor.
4. Convert repeated gaps into rubric language, deterministic checks, or a regression fixture under `evals/regression_fixtures/`.

## 中文说明

Taste anchor 用来校准“像不像一篇真正的研究报告”。它不是标准答案，也不是训练集。自动 runner 负责抓流程和结构问题；taste anchor 负责帮助人类 reviewer 判断报告是否有 thesis、机制、综合判断和读者体验。
