# Semantic diagnostic pairs

The six original bad/control pairs in `cases.json` cover paraphrased filler, irrelevant evidence bindings, denominator swaps, process traces versus useful limitations, retrospective PASS claims, and contract-tier omissions. Fourteen additional pairs in `additional-cases.json` bring the development catalog to 20, adding time and unit mismatches, causal overclaims, copied evidence, missing costs, late corrections, justified positive judgments and severity aggregation. English cases include meaningful specificity controls; the original six and their historical model diagnostics are unchanged.

All business facts are fictional. These are development/calibration excerpts, not held-out tasks, complete reports or a gold quality benchmark. Related examples share failure families: twenty excerpts do not constitute twenty independent real-world task observations.

The paired labels are author-proposed and have not been calibrated by two independent human reviewers. No API call or judge score is stored here. The deterministic evaluator must continue to report research quality as `not_evaluated`; it does not acquire semantic competence by reading these examples.

How to use:

Run `python scripts/check_semantic_diagnostics.py` for structural validation and positive/negative data-contract tests. Passing this script does not validate the proposed semantic labels. Actual model reviews, disagreements and any revised labels must be recorded separately.

1. Give a reviewer the evidence and both excerpts in randomized order, without the labels or explanations. Save the mapping privately.
2. Ask for the specific claim, missing condition or reasoning defect, and what the evidence actually permits. Preserve disagreements and review limitations.
3. Reveal the proposed explanation only after the initial review. A model review is a diagnostic opinion, not human blind review or a measured product-effect conclusion.
4. Critical fact failures must be reported separately; polished structure and procedural points cannot cancel them.
5. Keep the controls: valid uncertainty, a reasoned negative decision, substantial prose, or an honestly labeled stage draft must not fail merely for being cautious or unfinished.

These cases reflect failure types also observed in the internal Codex calibration: broad self-PASS, weak reader navigation, process phrases and a missing decision-reversing comparison. They do not include private raw logs or identify real companies. Structural parsing of the JSON is not evidence that a reviewer detects these failures.

中文：原六组加新增十四组，共二十组成对语义诊断材料，不是新增二十条写作硬规则。正常对照既包括适当保留不确定性，也包括证据允许时作出明确正向判断；不能训练成“越谨慎越正确”。严重事实错误单列，不靠排版或流程分抵消。正式保留任务、人类校准、完整报告及模型实测均另行记录；样本数不证明评测有效性。
