# Two reviewers agreed—and still missed a bad control

DeepSeek and Kimi reviewed twenty synthetic pairs without seeing the author's labels or explanations. Their 80 first-pass excerpt judgments all agreed with the proposed good/bad labels. **That is not 80/80 accuracy:** both accepted an original control that incorrectly treated four label-check passes as four usable video results.

This package preserves the exact masked inputs, model-visible final answers, request settings, eight attempt records, original proposals, mappings and separate revision protocol. Hidden reasoning and credentials are excluded. The original catalogs and earlier diagnostic results are unchanged.

## What happened

| Observation | Evidence boundary |
|---|---|
| Two ten-pair batches per model: 80 excerpt judgments | Agreement with fallible author proposals, not ground truth |
| Four selected pairs repeated with A/B swapped: 16 judgments | One DeepSeek judgment changed; batch composition also changed, so this does not isolate position bias |
| One between-model severity disagreement; nine severity differences from author proposals | Severity labels also need calibration; the author is not automatically correct |
| Both models missed the original usability-denominator defect | Polished caution and complete review JSON do not establish sound reasoning |
| Two separately retained case revisions, reviewed by both models: eight more judgments | Both distinguish the revised controls from bad excerpts; no human calibration or broader accuracy claim follows |

The original `semantic_filler_zh` control divided cost across “four usable results,” although only four candidates passed a label check. The revised control says **at most four label-compliant candidates**, does not infer full usability, and refuses to compute full unit cost without the missing inputs. It also removes unsupported camera/person-preservation detail.

The original `process_trace_vs_material_limit_zh` case did not clearly specify the delivery surface. DeepSeek changed its assessment from flawed to acceptable in the smaller fresh-context order check; a legitimate progress message can discuss next steps. The revision states that the assessed excerpt belongs in the reader-facing report body, not a progress message or method appendix. It criticizes substituting backstage activity for analysis without asserting that unobserved activity never occurred.

Both revisions are retained in [revisions.json](../../revisions.json). The current catalog loader applies them while leaving raw history intact:

```bash
python scripts/check_semantic_diagnostics.py
python scripts/check_semantic_diagnostics.py --show-current
python scripts/check_semantic_review_bundle.py --self-test
```

## Inspect and reproduce

`run-index.json` maps every call to its input, request, attempt and final answer. `mapping.json` reveals the original batch randomization only after reviews have finished; `revisions-mapping.json` does the same for the two revised cases. `source-catalogs/` preserves the exact author proposals and correction record used here. The first three jobs use the original catalogs, not the current corrected view. The final job uses the two retained revisions.

`analysis.json` is a descriptive comparison derived from those answers, not an accuracy score. The between-model disagreement concerns the severity of the unsupported “entirely inconclusive” assessment of a randomized trial; the changed repeat judgment concerns the process-trace bad excerpt. Other severity differences from the author proposals include self-PASS evidence, supervised-pilot eligibility, late scope and causal interpretation. No majority vote resolves these labels as truth.

Each provider used a 32,768 output-token cap and 600-second transport timeout; no automatic retries were made. Calls use the project's existing separate CNY50 provider ceilings. Recorded reservations are upper bounds, not invoices. Exact fresh replay may produce different judgments and new charges; obtain authorization, preserve a new output directory and do not overwrite this dated package.

For a fixed-input replay, send the recorded `system` and `user` strings as separate messages using that call's request settings. Do not reveal author labels, mappings or prior reviews until the new judgment is captured. The original and revision freeze files also record hashes of private controllers that are not distributed here; this is not a portable runtime certification or a claim of third-party reproduction.

## 中文结论

本轮最重要的结果不是“两个模型全都判对”，而是：首轮80个片段判断都同意作者标签，仍共同漏掉一个正例错误。更换展示顺序及批次组成后还出现了一次改判，严重性标注也有分歧。

已分别修正“标签通过等于整体可用”的错误和正文/进度消息场景不清的问题，保留旧样本、旧结果与两名非作者的新复审。模型复审提供了进一步诊断意见，不等于人类校准。二十组成对短片段和两项修订也不等于二十二个独立真实研究任务。
