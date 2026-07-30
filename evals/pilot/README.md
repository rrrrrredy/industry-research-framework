# Preregistered Paired Pilot

This directory contains a provider-neutral harness for a future paired baseline-versus-framework pilot.

No live model runs are included. The synthetic adapter and CI tests validate the experimental plumbing, not framework efficacy.

## Evidence boundary

The committed files establish that the repository can:

- freeze the protocol, repository commit, skill, cases, source packs, rubric, model parameters, and run matrix by SHA-256
- create paired baseline and treatment requests whose model-visible inputs differ only by the frozen framework instruction
- keep the baseline workspace free of the framework, taste anchors, rubric, and repository checkout
- call an external JSON-over-stdin/stdout adapter without reading or serializing provider credentials
- append every failed or successful attempt instead of replacing inconvenient runs
- downgrade synthetic, floating-model, seed-unsupported, or isolation-unverified runs to `exploratory`
- export final-text-only, label-blinded reviewer submissions, retain a separate blind attrition ledger, and commit the private mapping hash before scoring

They do not establish that the framework improves quality, reduces failures, saves tokens, generalizes across providers, or produces statistically significant effects.

The subprocess transport is not a filesystem or network sandbox. Setting the adapter working directory does not prevent it from reading the repository or other machine state, and an adapter's isolation attestation is not independent proof. This version therefore grades every subprocess run as `exploratory`, even when the adapter reports a dated model, seed support, and fresh-session isolation. A future confirmatory run requires a separately verified sandbox boundary.

## Frozen design

[`protocol_v1.json`](./protocol_v1.json) preregisters three cases, three paired replicates, and two conditions, for 18 planned live calls:

- baseline receives a neutral task, the same selected sources, and the same output contract
- treatment receives those identical inputs plus the frozen `SKILL.md`

The primary endpoint is independent, label-blinded review of `final.md` only with [`final_quality_rubric_v1.json`](./final_quality_rubric_v1.json). Framework artifact conformance, token use, latency, and run failure rate are exploratory because they can structurally favor or otherwise reveal the treatment.

Before a live run, replace the model placeholder with a dated provider snapshot, set `snapshot_kind` to `dated`, freeze the external adapter identity SHA-256, and commit those changes. Run `prepare` from that clean commit. Dirty inputs, a changed adapter, a sampling mismatch, missing provider provenance, or unverified isolation keep the evidence exploratory or invalidate the attempt.

## Commands

Prepare a frozen matrix. Publish or timestamp `manifest-commitment.json` before dispatch so later manifest changes are detectable:

```bash
python scripts/pilot.py prepare \
  --repo-root . \
  --protocol evals/pilot/protocol_v1.json \
  --output-dir evals/pilot/live/prepared
```

Verify the commit, input hashes, workspaces, requests, and pairwise allowlist:

```bash
python scripts/pilot.py verify \
  --repo-root . \
  --manifest evals/pilot/live/prepared/manifest.json
```

Run one synthetic plumbing check. The adapter command must be last:

```bash
python scripts/pilot.py dispatch \
  --repo-root . \
  --manifest evals/pilot/live/prepared/manifest.json \
  --attempts-dir evals/pilot/live/attempts \
  --run-id R001 \
  --adapter-command python evals/pilot/fake_adapter.py
```

For a real provider, replace the fake command with an external adapter that implements `pilot-adapter-v1`. The adapter owns authentication; credentials are forbidden in command-line arguments. The harness passes a credential-free request on stdin and expects one JSON response on stdout containing the redacted raw provider request and response, provider/request/model identity, system fingerprint, actual sampling parameters, usage, stop reason, tool transcript, adapter version, and an isolation attestation. The harness records the complete redacted command and adapter identity hash. HTTP headers are not retained as provenance: any structured adapter-response field whose normalized name contains `header` is replaced wholesale with `[REDACTED]`, and sensitive header lines in stderr or unparsed stdout are scrubbed before persistence.

Create the blind export after all planned attempts. Before writing any blind files, this command re-verifies the preparation commitment and frozen inputs, then binds every attempt's request hash and persisted request to its manifest run:

```bash
python scripts/pilot.py blind \
  --repo-root . \
  --manifest evals/pilot/live/prepared/manifest.json \
  --attempts-dir evals/pilot/live/attempts \
  --output-dir evals/pilot/live/blind
```

Give reviewers only `submissions.jsonl`; it contains `submission_id` and `final_text`, nothing about condition, case, paths, status, or retry history. `accounting.jsonl` retains missing/failed attempts and retry history separately. Keep `keys.json` private, and publish or timestamp `commitment.json` before scoring so the submission-to-condition mapping cannot be silently replaced later.

Prepare a JSONL score file with `submission_id`, `reviewer_id`, and one integer score for every rubric dimension, then lock it against that pre-score commitment:

```bash
python scripts/pilot.py lock-scores \
  --rubric evals/pilot/final_quality_rubric_v1.json \
  --submissions evals/pilot/live/blind/submissions.jsonl \
  --commitment evals/pilot/live/blind/commitment.json \
  --scores evals/pilot/live/scores.jsonl \
  --output evals/pilot/live/score-lock.json
```

The harness intentionally does not aggregate or reveal results. A later results PR should include the frozen protocol, all attempts, the score lock, the reveal mapping, paired outcomes, cost/latency data, and explicit limitations.
