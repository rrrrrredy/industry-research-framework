# Frozen Task: Eight Fictional Model-Company Pipelines

Write a 3,500–6,000 Chinese-character report for model-company executives using only the supplied fictional source pack. Do not browse the web and do not introduce real-company facts. Treat every company, person, product, date, and operating detail in the dossier as fictional evaluation material.

The main question is how eight model companies divide and coordinate pretraining, mid-training, post-training, data strategy and labeling, training infrastructure, evaluation, serving, product feedback, and release. Data and labeling are the first priority, but must not crowd out the other stages.

Requirements:

1. Compare all eight companies without presuming a winner. Make differences concrete at company level.
2. Analyze teams, division of labor, process interfaces, handoffs, and decision rights when the dossier supports them.
3. Use each company's named model-release node as the time boundary. For the two companies whose dossier specifies a leadership change, discuss only the post-arrival adjustment period.
4. Explain how checkpoints, datasets, evaluation versions, infrastructure, serving, product feedback, and release artifacts move between stages.
5. Give data strategy and labeling a dedicated section while preserving adequate treatment of training, infrastructure, evaluation, serving, product feedback, and release.
6. Add a dedicated analysis of how Harnesses and Coding Agents change training environments, post-training, evaluation, serving, and the definition of a deliverable.
7. Open with short, specific key findings that include differences among the eight companies, not only industry-wide commonalities.
8. Include an eight-company pipeline comparison table; split it into organization, data, and training/delivery tables if that is clearer.
9. Address five propositions explicitly: persistent platforms versus model-node project teams; data and labeling across training stages; checkpoint/data/evaluation-version handoffs; model/environment/system-configuration bundles in the Agent era; and reproducibility, verifiability, rollback, and institutional learning as pipeline outcomes.
10. State uncertainty whenever the dossier cannot confirm reporting lines, decision rights, causal mechanisms, or process durability. Do not fill one company's gaps with another company's practice.
11. Use professional research prose. Do not include work logs, channel inventories, source-by-source narration, a glossary, or a reference list.
12. End with unresolved questions and accepted limitations. Do not call a partial artifact final.

Required headings:

- 核心要点
- 管线总览
- 八家公司对比
- 数据与标注
- 训练、Infra与评测
- Harness与Coding Agent
- 不确定性

Source files:

- `evals/source_packs/model_company_pipeline_synthetic/manifest.json`
- `evals/source_packs/model_company_pipeline_synthetic/sources.jsonl`
