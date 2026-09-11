# Semantic diagnostic pairs

The six original bad/control pairs in `cases.json` cover paraphrased filler, irrelevant evidence bindings, denominator swaps, process traces versus useful limitations, retrospective PASS claims, and contract-tier omissions. Fourteen additional pairs in `additional-cases.json` form the historical 20-pair catalog, adding time and unit mismatches, causal overclaims, copied evidence, missing costs, late corrections, justified positive judgments and severity aggregation. English cases include meaningful specificity controls; the original six and their historical model diagnostics are unchanged.

Three new pairs in [`reader-cases-2026-09-10.json`](./reader-cases-2026-09-10.json) bring the current development view to 23. They cover opening priorities, editorial narration in report prose, and timelines that list facts without explaining them. Each states the reader's actual requirement, keeps a close control and preserves useful uncertainty. No phrase blacklist, standard introduction or fixed insight count is implied. A subsequent internal diagnosis used four model reviewers in fresh contexts. It led to the explicit single-seat pricing scope in [the retained reader revision](./reader-revisions-2026-09-11.json). The private reviews remain outside this repository; the earlier eight public calls did not assess these pairs.

All business facts are fictional. These are development/calibration excerpts, not held-out tasks, complete reports or a gold quality benchmark. Related examples share failure families: 23 pairs do not constitute 23 independent real-world task observations.

The paired labels are author-proposed and have not been calibrated by two independent human reviewers. [Eight actual model-review calls](./reviews/2026-09-08/) retain the original twenty-pair review, order/context sensitivity and separate reviews of two corrected cases. Both models originally missed a defect in an author-proposed control: label-check success is not full usability. The deterministic evaluator must continue to report research quality as `not_evaluated`.

Use the current catalog through `python scripts/check_semantic_diagnostics.py --show-current`. It applies the two retained changes in [`revisions.json`](./revisions.json), plus the single-seat, single-month correction in [`reader-revisions-2026-09-11.json`](./reader-revisions-2026-09-11.json). The three dated source catalogs remain unchanged. All revisions bind to their original case hashes, and none adds an independent task. Do not reuse the known-bad old control as a current quality anchor.

中文：新增三组读者审阅样本分别检查开篇是否埋住主要发现、正文是否夹带持续的修稿口吻、时间线是否只有收录而没有解释。当前视图共23组；新增三组已经过内部四模型新上下文诊断，收费对照补清了一个席位、一个月的共同口径，当前视图通过保留修订应用该更正。私人评审原文不在公共仓库，旧八次公开评审没有评过这三组；这次诊断也不构成人类校准或工具箱效果验证。材料和商业事实均为虚构，不公开私人报告原文。有效限制说明、问句标题或“不是……而是……”等句式本身不判错；判断要回到具体任务和整段表达。

How to use:

Run `python scripts/check_semantic_diagnostics.py` for structural validation and positive/negative data-contract tests. Passing this script does not validate the proposed semantic labels. Actual model reviews, disagreements and any revised labels must be recorded separately.

1. Give a reviewer the evidence and both excerpts in randomized order, without the labels or explanations. Save the mapping privately.
2. Ask for the specific claim, missing condition or reasoning defect, and what the evidence actually permits. Preserve disagreements and review limitations.
3. Reveal the proposed explanation only after the initial review. A model review is a diagnostic opinion, not human blind review or a measured product-effect conclusion.
4. Critical fact failures must be reported separately; polished structure and procedural points cannot cancel them.
5. Keep the controls: valid uncertainty, a reasoned negative decision, substantial prose, or an honestly labeled stage draft must not fail merely for being cautious or unfinished.

These cases reflect failure types also observed in the internal Codex calibration: broad self-PASS, weak reader navigation, process phrases and a missing decision-reversing comparison. They do not include private raw logs or identify real companies. Structural parsing of the JSON is not evidence that a reviewer detects these failures.

中文：原六组加新增十四组，共二十组成对语义诊断材料，不是新增二十条写作硬规则。正常对照既包括适当保留不确定性，也包括证据允许时作出明确正向判断；不能训练成“越谨慎越正确”。本轮已公开两名非作者模型的八次评审调用：首轮共同漏掉旧正例的可用性分母错误，另有顺序/上下文敏感和严重性分歧。两项保留修订由当前视图应用，旧样本和旧结果不覆盖，不把版本数当题目数。模型同意标签不是准确率，也不替代人类校准。
