---
type: Review Agent Definition
title: Ralphthon Track 2 Evidence-Bound Review Agent
description: Frozen Track 2 review contract, authority boundary, runtime identity, and mock validation evidence.
tags: [ralphthon, track-2, review-agent, codex]
timestamp: 2026-07-12T13:40:00+09:00
status: synthetic-mock-verified-live-unverified
---

# Ralphthon Track 2 Review Agent

## Frozen identity

- Agent name: `ralphthon-track2-review-agent`.
- Runtime version: `ralphthon-track2-review-agent-v1`.
- Official upstream dependency: `auto-research` at commit `a9f4f2583648ef4ca54f980f951ae393d153473f`.
- Canonical frozen task-prompt asset SHA-256: `29e116b4b25663b65ff9920057a87d2b850080b97be836b364149cb95d9d914a`.
- Canonical frozen schema SHA-256: `cd19220f5435dc1da4146bd7c1e467cf4bea0ac0ecb69b2ac518b53922363d24`.
- Frozen fixture manifest: `fixtures/FROZEN_MANIFEST.sha256`.
- Staged package manifest: `staging/ralphthon-track2-review-agent.sha256`
  with SHA-256 `38f2c01d2d27d3f8451f97167a3fbec9b11bfa4723d1f8ca72e0484723a9d0f7`.

The task-prompt asset and schema hashes above are written into every per-paper
manifest in the frozen synthetic-mock evidence. The native developer policy is
a separate surface frozen by the staged-package manifest above; Root verifies
and records that wrapper-manifest SHA in batch metadata. Before live use, Root
must also freeze and read back the actual paper, evidence, task-prompt asset,
schema, and agent hashes for each assignment.

## Input contract

Each Worker receives exactly one immutable manifest and one bounded lease. The
manifest records the platform paper identifier; paper and evidence file names,
SHA-256 values, and sizes; aggregate input and evidence hashes; prompt and
schema hashes; agent version; and freeze time. The frozen corpus supplies the
allowed file paths separately; the Root-issued lease is also separate from the
manifest. Unsafe paper identifiers are rejected before any artifact or ledger
write. An existing manifest with a different identity is a hard failure, is
never overwritten, and cannot enter the targeted schema-repair path.

Allowed review evidence is the frozen paper and explicitly supplied evidence.
The agent does not request private reviewer information, hidden labels, new
training, GPU work, VESSL, W&B, or additional experiments.

## Review instruction

Act as an evidence-bound ICML-style reviewer. Connect every central strength,
weakness, evidence-trace item, and score rationale to a page, section, table,
figure, appendix, or saved result. If support is absent or ambiguous, state the
limitation and lower confidence instead of inventing evidence, citations,
experiments, intent, or consensus.

Before emitting JSON, privately build a claim map, run a falsification pass,
anchor each score independently, and check consistency across claims,
rationales, scores, confidence, and comment. Prefer a few high-impact findings,
and distinguish missing evidence from evidence that a claim is false.

## Output contract

Workers return one canonical `ReviewDraft` JSON object containing:

- Summary, Strengths, Weaknesses, Questions, Ethics and Limitations, Evidence
  Trace, and score rationales.
- Soundness, Presentation, Contribution, Significance, and Originality as
  independent integers from 1 to 4.
- Overall Recommendation from 1 to 6 and Confidence from 1 to 5.
- A non-empty constructive Comment.
- Paper, lease, Worker, prompt, input, evidence, agent, and timing provenance.

Contribution is the official upstream field. Significance, Originality, and
Comment are event fields. No conversion, alias, average, or inferred mapping is
permitted among them.

## Authority and recovery

Root alone may discover assignments, claim, query status, post, write receipts,
own lease state, or mutate the atomic ledger. Three persistent Workers only
read frozen inputs and return `ReviewDraft`. The queue high-water mark is three
until the live interface confirms that multiple claims are permitted.

Root writes `outbox/<paper_id>.json` and `clipboard/<paper_id>.txt` before any
post attempt. Deterministic validation remains mandatory. Root routes only a
high-risk, schema-valid subset to read-only draft calibration: risk score at
least 3, ceil(30%) and at most three papers, one verifier for 20 seconds, before T+15
with backlog at most two. The fast path bypasses calibration. Schema and
calibration share one targeted-repair budget per paper. Claim and post timeouts
enter an unknown state and are reconciled by status before a retry. A verified
post is never repeated. Live success is exactly
`posted_verified == assigned_count`.

## Invocation

After the staged package is installed into a writable project `.codex` tree,
start a fresh Codex session and invoke:

```text
$auto-research
```

Select its Track 2-only frozen-paper path, then invoke:

```text
$ralphthon-track2-review-agent
```

For a local deterministic batch without production side effects:

```bash
python3 staging/.codex/skills/ralphthon-track2-review-agent/scripts/run_batch.py \
  --mode DRY-RUN \
  --papers fixtures/throughput/papers.json \
  --root-dir . \
  --output-dir /tmp/ralphthon-track2-dry-run \
  --workers 3
```

## Frozen mock evidence

Runtime and quality evidence is
`evidence/mock-validation-final-20260712T1335KST/aggregate.json`, SHA-256
`239f2de62fcc5a1671b6cf86efc4f3a63077c3e3d2c81ccd2ad04e25a2077910`.
Actual process-resume evidence is
`evidence/process-restart-proof/aggregate.json`, SHA-256
`18d536ca72f87e03117af28d5534d10de1b316a3a0dc26b52fd5a2849e0de5d2`.

- Three synthetic 10-paper runs completed 30/30 assigned instances, with
  schema validity 30/30 (100%) and zero duplicate post attempts or idempotency
  keys.
- One synthetic fault run recovered one malformed JSON output, worker timeout,
  claim timeout, and post timeout, and performed one in-process ledger reopen;
  it completed 10/10 with schema validity 10/10 and no duplicates.
- In a separate two-process proof, the first process exited 75 after four
  mock-verified papers. A fresh process exited 0 at 10/10 with schema validity
  10/10 and no duplicates while preserving the four-paper ledger prefix and
  completed manifest and outbox bytes.
- A no-op rerun after full completion also left the ledger and outbox
  byte-identical.
- On frozen seeded synthetic issues, the deterministic runtime recorded TP 20,
  FP 0, FN 0, and F1 1.0. The naive baseline recorded TP 10, FP 0, FN 10, and
  F1 0.6667.

These are deterministic synthetic-mock measurements. They do not establish
live-platform completion, latency, or review quality on unseen papers. The
worker-timeout injection verifies mock-adapter `TimeoutError` recovery; it does
not prove forced termination of a running thread.

## Live boundary

The production endpoint, selector set, assignment count, claim semantics,
accepted field mapping, and posted-success marker remain unverified until the
authorized live window. The bundled CLI is BUILD/DRY-RUN-only and rejects
`LIVE` unconditionally; no production adapter is implemented. At 16:35 KST,
Root uses the Skill-guided path for at most 45 seconds of read-only
`LIVE_DISCOVERY`; if automation cannot be verified, follow `MANUAL_PLATFORM.md`
while Workers continue producing validated outbox and clipboard artifacts.
