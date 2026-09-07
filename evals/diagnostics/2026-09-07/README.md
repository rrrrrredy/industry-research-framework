# Actual reports and development diagnostics / 实际产出与开发期诊断

Two calibration tasks were actually run in Codex with and without the framework. The framework outputs had useful evidence but weak navigation, insufficiently prioritized conclusions and overly generous self-reviews. They were repaired under the **unchanged original protocol**. This package preserves all four original reader outputs, the two repairs, intervening review failures and a later three-model text diagnostic. It does not establish a framework win rate.

两道校准题确实分别运行了框架组与无框架组。框架稿不是零内容，但章节导航、判断优先级和自评严格度不足。这里保留四份原始读者稿及两份修订稿，供直接比较；不是用后台 PASS 替代读者判断，也不将修订前后包装成框架效果证明。

| Task / 题目 | Original framework / 原框架稿 | Original baseline / 原基线稿 | Repaired report / 修订稿 |
| --- | --- | --- | --- |
| Customer service / AI 客服商业化 | [Read](reports/customer-service/original-framework.md) | [Read](reports/customer-service/original-baseline.md) | [Read](reports/customer-service/repaired.md) |
| Commercial video / 商业视频制作 | [Read](reports/video-production/original-framework.md) | [Read](reports/video-production/original-baseline.md) | [Read](reports/video-production/repaired.md) |

The reports are in Chinese, with a 2026-09-07 information cutoff. They are historical documentary research, not current procurement, legal or investment advice. Recheck dynamic prices, terms and availability before reuse. Original outputs contain known weaknesses and are retained as evidence, not endorsed answers.

## What changed / 改了什么

- The repairs begin with conditional choices and rejection conditions, then explain the companies, costs, evidence and actions in five substantive sections. No new universal word limit or writing template was introduced.
- The customer-service repair's first source audit **failed**. Corrections address organization-level billing restrictions, Help Agent units and time windows, Zendesk product scope, study heterogeneity and weak historical-source attribution. The failed draft and review remain in its `reviews/` directory.
- The video repair distinguishes ordinary and enterprise contracts, nominal generation prices and usable-output costs, documented entry points and unverified procurement eligibility. fal and Gemini Developer API are not presented as cleared confidential-material routes. A reviewer's unsupported shared-concurrency-pool inference was rejected.
- Final minor edits follow the [finding-by-finding adjudication](ADJUDICATION.md). The model-reviewed versions are `before-model-diagnostics.md`, **not** the later `repaired.md` files. Each has a separate hash.

修订重点是落实原本已有的要求：把具体判断放前面，按板块展开，把价格、条款和证据缺口写成会改变选择的条件。客服首轮事实审查的失败没有删除；视频稿仍明确没有进行付费生成或目标企业账户验证。两份修订稿均未获得独立人类验收。

## Three-model diagnostic, not three agent runtimes

All providers received the same frozen text inputs: six synthetic development pairs and the two repaired reports as they stood before the last minor edits. Semantic A/B author labels were withheld, but report briefs contained the author's provisional thesis. The report reviews were therefore **not blinded** to that thesis. The reviewers had no retrieval tools; earlier retrieval-enabled Astra source audits are a separate condition.

| Route | Requested model | Completed text replies | Preserved failure |
| --- | --- | --- | --- |
| Astra inside Codex, existing ChatGPT login | `gpt-6-astra`, high | 3 / 3 | None; served identity not independently attested |
| DeepSeek official API | `deepseek-v4-pro`, high | 3 / 3 | None |
| Kimi China official API | `kimi-k3`, high | 2 / 3 | Video: output limit, empty final answer |

Eight complete replies from nine attempts. Kimi's video request exhausted 8,192 completion tokens, of which 8,189 were reported as reasoning, and returned no final content. There was no retry. A missing answer is not a report verdict.

All three models rejected the six author-proposed flawed excerpts and accepted the six controls. They disagreed with the author's `critical_fact_error` label for the self-PASS/sequence overclaim. That uncalibrated disagreement is preserved; neither the labels nor the agreement are human ground truth. The five completed report reviews said `usable_with_limits`. These are model opinions, not independently verified facts.

三模型提供的是文本诊断，不是三种 Agent 的完整研究对照。跨厂商可以增加视角，但不能自动消除共同输入诱导、共同事实假设或自评偏差；模型多数票不是事实裁决。

## Evidence and repeatability

- [Frozen inputs and design](model-input-manifest.json), [author-proposed labels](author-labels.json), [all attempt metadata and summary](summary.json), [final model replies](results/) and [API request bodies without authentication](requests/).
- Each report folder includes its original request, repair brief, source/claim/uncertainty records, pre-review versions and structured reviewer summaries. Summaries are not raw transcripts or independently authenticated execution traces.
- [Calibration provenance](calibration-provenance.json) records original and exported hashes. The exports normalize line endings and outer whitespace; one local download footer was removed from each video output. No analytical prose or public citations were removed. Private original captures remain unchanged.
- [A real CLI capture control](runtime-capture-control.json) records a matching captured message and a deliberately mismatched negative control. It used a synthetic fixture. It does not attest this desktop UI or prove report quality; the repaired report checks themselves had `delivery_observation: not_provided`.
- [Bundle manifest](bundle-manifest.json) binds the public text files with LF-normalized SHA-256 hashes. Check it offline from the repository root with `python scripts/check_diagnostic_bundle.py`. It verifies the package, not the truth of a model's judgment.

For a fresh text rerun, use the exact `system` and `user` strings in `inputs/<task>.json`. DeepSeek/Kimi request JSON records the actual parameters; use your own explicitly authorized credentials outside files and logs. Astra used Codex `exec`, requested `gpt-6-astra` with high reasoning, ignored user configuration, used an ephemeral read-only session, and emitted JSON events plus its last message. The public API requests and Codex wrappers differ, so latency and token counts are not a fair model ranking. A rerun can produce a different answer; retain it separately instead of overwriting this dated bundle. No command in the offline checker calls a model.

The usage-based cost guard was approximately CNY 0.80 for DeepSeek and CNY 1.51 for Kimi, separately under CNY 50 ceilings. DeepSeek used a deliberately conservative 10 CNY/USD conversion, not an exchange-rate quote. These are estimates, not invoices; reservations and calculation basis remain in `summary.json`. Astra did not use a separately billed OpenAI API.

## What remains unproved / 尚未证明

The calibration tasks were authored for development, already seen during repairs, and run framework-first. Human reviews were not completed. Longer, interactively corrected repairs cannot be compared with the original baseline as a causal treatment. No matched API report-generation experiment took place. No three-runtime publication gate, 12-task held-out study or external reproduction was completed by this package.

原框架 `SKILL.md` 与八份核心 reference 未修改。这里补的是实际产出、具体失败和证据边界；它们不替代正式同环境对照、双人盲审或第三方复现。第三方网页内容仅链接并作必要分析，版权和服务条款仍属于原权利人。包内不包含密钥、私人聊天、本机配置或模型思维链。
