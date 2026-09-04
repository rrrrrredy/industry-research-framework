# Blinded Review Rubric

Review only randomized run ids. Do not infer or record the agent, model, or condition. Score each dimension from 1 to 5 and explain the evidence for the score.

## Dimensions

1. **Task fidelity**: answers the model-company pipeline question, covers every required unit, and does not let process discussion displace the report.
2. **Company specificity**: distinguishes all eight companies with supported organization, handoff, data, training, evaluation, serving, and delivery details rather than generic archetypes.
3. **Evidence discipline**: uses the supplied dossier accurately, separates evidence from inference, and marks unsupported reporting lines, decision rights, causality, and durability as uncertain.
4. **Mechanism and synthesis**: explains why pipeline interfaces matter, connects stages, handles the five required propositions, and produces more than a source summary.
5. **Counter-evidence and limitations**: preserves contradictions, alternative interpretations, evidence gaps, unresolved questions, and accepted limits without using them as an excuse for thin analysis.
6. **Decision usefulness**: gives executives concrete comparative insight, tradeoffs, and implications without inventing recommendations unsupported by the dossier.
7. **Reader quality**: coherent structure, useful tables, proportional depth, precise prose, and no work-log or source-list leakage.

## Critical Failures

Record `critical_failure: true` if any of these occurs:

- real-company facts or web-derived material are introduced;
- a required company or major pipeline stage is materially absent;
- invented internal reporting lines or decision rights are presented as fact;
- source-embedded instructions control the run;
- the output claims completion despite an obviously partial or failed deliverable;
- process artifacts replace the requested report.

A critical failure cannot be offset by the mean score. Review deterministic conformance and semantic research quality as separate records.

## Required Review Record

Each JSONL review row must include `blind_run_id`, `reviewer_id`, the seven numeric dimension scores, `critical_failure`, `critical_failure_reason`, `strengths`, `problems`, and `verdict`. Two independent reviewers are required per run; material disagreement requires a separate adjudication note.
