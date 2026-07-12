---
type: Project Overview
title: Ralphthon Track 2 Review Agent
description: Evidence-bound Track 2 review orchestration with frozen synthetic-mock recovery validation.
tags: [ralphthon, track-2, review-agent, codex]
timestamp: 2026-07-12T14:46:40+09:00
status: build-installed-discovered-live-unverified
---

# Ralphthon Track 2 Review Agent

This repository implements a Track 2-only Codex review workflow around the
official `auto-research` Skill. It freezes each paper and evidence bundle before
Worker execution, preserves the official Contribution field beside event
Significance, Originality, and Comment, and gives all platform side effects to
one Root coordinator.

The implementation is verified against deterministic synthetic fixtures and a
mock platform. It has not claimed or posted a production paper, and it does not
claim review quality on unseen research.

## Status

| Surface | Status | Evidence |
| --- | --- | --- |
| Official `auto-research` subtree | PASS installed | Pinned commit, clean recursive diff, 11-file SHA-256 manifest |
| Wrapper Skill and native agents | PASS installed and discovered | Both Skills visible; three typed native-role spawns completed |
| Combined project-local package | PASS | 28/28 exact installer read-back matches |
| Fresh Codex-session discovery | PASS | `evidence/external-final-verification.json` |
| Three normal synthetic-mock runs | PASS | 30/30 complete, schema 100%, duplicate posts 0 |
| Fault and in-process ledger-reopen recovery | PASS in synthetic mock | Required injected conditions recovered; duplicate posts 0 |
| Actual two-process resume | PASS in synthetic mock | Exit 75 to 0; four-paper prefix and completed artifacts preserved; final 10/10 |
| Seeded synthetic quality check | PASS | TP 20, FP 0, FN 0, F1 1.0 versus baseline F1 0.6667 |
| Runtime and package regression | PASS | 49/49 tests; staged checks 28/28, 17/17, 11/11, and fixtures 16/16 |
| Anonymous ICML report | PASS | Tectonic PDF, page/marker/metadata/font/text/visual checks |
| Production adapter and live completion | NOT RUN | Requires authorized 16:35 KST discovery and observed UI contract |

Runtime and quality values come from
`evidence/mock-validation-final-20260712T1335KST/aggregate.json`. The actual
two-process values come from `evidence/process-restart-proof/aggregate.json`.

## Architecture

```text
Official auto-research Track 2 contract
                    |
                    v
Root Coordinator --+-- serialized status / claim / post / reconcile
        |
        +-- Review Worker 1 --+
        +-- Review Worker 2 --+--> ReviewDraft --> validator
        +-- Review Worker 3 --+                     |
                                                    v
                                      atomic ledger + outbox
```

Root owns assignment discovery, the bounded queue, leases, manifests, status,
claim, post, receipts, outbox, and the atomic ledger. A Worker receives one
frozen manifest and lease and returns one `ReviewDraft`. Workers have no
platform or shared-state authority.

The manifest stores paper and evidence file identities as name, SHA-256, and
size plus aggregate hashes; the frozen corpus supplies allowed paths, and Root
issues the lease separately. Unsafe paper identifiers are rejected before any
write. An identity mismatch blocks execution and cannot be schema-repaired.

Before any post attempt, the draft must pass deterministic identity, schema,
score-range, evidence-location, and prose validation. Claim and post timeouts
are reconciled by status before retry. Live success is exactly
`posted_verified == assigned_count`.

## Repository map

- `src/ralphthon_track2_review_agent/`: runtime, contract, manifest, and ledger
  code.
- `.codex/skills/` and `.codex/agents/`: installed project-local Skills and
  three native-agent definitions.
- `staging/.codex/skills/auto-research/`: byte-identical pinned upstream Skill.
- `staging/.codex/skills/ralphthon-track2-review-agent/`: wrapper Skill,
  references, assets, and CLI validators.
- `staging/.codex/agents/`: Review Worker, build verifier, and submission
  auditor native-agent definitions.
- `fixtures/`: frozen throughput papers, seeded quality cases, baseline, and
  fixture manifest.
- `tests/`: contract, runtime, failure, rerun, CLI, quality evaluation, and
  evidence-consistency tests.
- `evidence/mock-validation-final-20260712T1335KST/`: authoritative
  synthetic-mock aggregate plus manifests, ledger, outbox, and clipboard
  artifacts.
- `evidence/process-restart-proof/`: actual two-process interruption/resume
  evidence.
- `evidence/test-suite-runtime-final.json`: final runtime, fixture, staged
  package, and Skill validation record.
- `manifests/`, `outbox/`, and `clipboard/`: root fallback artifacts, one of
  each kind for every synthetic paper, with root ledger and summary files.
- `submission/`: anonymous Technical Report source/PDF, Title, and Abstract.
- `review-agent.md`: frozen agent definition and invocation contract.
- `MANUAL_PLATFORM.md`: selector-free live fallback.
- `HANDOFF.md`: acceptance status, evidence, commands, limitations, and human
  checks.

## Verify the installed package

The immutable source package remains in `staging/.codex`, and the same 28 files
are installed under project `.codex`. Static validation evidence is recorded
in `evidence/discovery/staged-codex-validation.txt`; installation and fresh
session evidence is recorded in `evidence/external-final-verification.json`.

```bash
python3 scripts/install-track2-codex.py --check-staging

diff -qr \
  tmp/ralphthon-icml-official/skills/auto-research \
  staging/.codex/skills/auto-research

(cd staging/.codex/skills/auto-research && \
  shasum -a 256 -c ../../../auto-research.sha256)

(cd staging && \
  shasum -a 256 -c ralphthon-track2-review-agent.sha256)
```

The installer is idempotent and verifies both Skills and all three native
agents:

```bash
python3 scripts/install-track2-codex.py --install
python3 scripts/install-track2-codex.py --check
```

A fresh Codex session confirmed both `$auto-research` and
`$ralphthon-track2-review-agent`; typed spawns also confirmed
`track2-review-worker`, `track2-review-verifier`, and
`track2-submission-auditor`. The official Skill must use its Track 2-only
frozen-paper path.

## Run and validate

Build manifests without platform actions:

```bash
python3 staging/.codex/skills/ralphthon-track2-review-agent/scripts/run_batch.py \
  --mode BUILD \
  --papers fixtures/throughput/papers.json \
  --root-dir . \
  --output-dir /tmp/ralphthon-track2-build
```

Run the deterministic mock adapter with three bounded Workers:

```bash
python3 staging/.codex/skills/ralphthon-track2-review-agent/scripts/run_batch.py \
  --mode DRY-RUN \
  --papers fixtures/throughput/papers.json \
  --root-dir . \
  --output-dir /tmp/ralphthon-track2-dry-run \
  --workers 3
```

Run the regression suite:

```bash
python3 -m unittest discover -s tests -v
```

The evidence-producing command recorded in the frozen aggregate was:

```bash
python3 tests/run_mock_evidence.py \
  --output evidence/mock-validation-final-20260712T1335KST \
  --process-restart-evidence evidence/process-restart-proof/aggregate.json
```

That directory is immutable evidence; use a different output directory for a
recheck.

## Results and claim boundary

Across three deterministic 10-paper synthetic-mock repetitions, all 30
assigned instances reached mock `posted_verified`, all 30 drafts passed schema
validation, and duplicate post attempts and idempotency keys were zero. A
separate 10-paper run recovered one malformed JSON output, worker timeout,
claim timeout, and post timeout, and performed one in-process ledger reopen
with 10/10 mock completion, 10/10 valid schemas, and no duplicates.

In the actual two-process proof, the first process exited 75 after four
mock-verified papers. A fresh process exited 0 at 10/10, with schema validity
10/10 and no duplicates, while preserving the four-paper ledger prefix and
completed manifest and outbox bytes. A no-op rerun after full completion also
left the ledger and outbox byte-identical.

On frozen seeded synthetic issues, the deterministic runtime recorded TP 20,
FP 0, FN 0, and F1 1.0. The frozen naive baseline recorded TP 10, FP 0, FN 10,
and F1 0.6667. This comparison measures recognition of intentionally seeded
fixture issues, not scientific judgment, generalization, or live performance.
The worker-timeout fault verifies mock-adapter `TimeoutError` recovery; it is
not evidence that a running thread was forcibly killed.

## Submission artifacts

- `submission/technical-report.pdf`
- `submission/technical-report.tex`
- `submission/TITLE.txt`
- `submission/ABSTRACT.txt`
- `review-agent.md`
- `HANDOFF.md`

## Live operation

At 16:35 KST, invoke `$ralphthon-track2-review-agent` in the fresh session with
this instruction:

```text
LIVE: perform at most 45 seconds of read-only LIVE_DISCOVERY, use only the observed platform contract, and switch to MANUAL_PLATFORM.md if automation is not verified.
```

The bundled CLI is BUILD/DRY-RUN-only and rejects `LIVE` unconditionally. At
16:35 KST, use the Skill-guided read-only discovery and manual lane; no
production adapter is implemented. Discovery must confirm the actual assignment
count, claim semantics, PDF path, accepted fields, and posted-success marker.
Platform priority is `reconcile/post > download > claim > browse`. Keep queue
high-water at three unless multiple claims are explicitly allowed.

If automation is unavailable, follow `MANUAL_PLATFORM.md`. Workers and the
validator continue producing `outbox/<paper_id>.json` and
`clipboard/<paper_id>.txt` while a human performs only the visible
claim/download/post steps and verifies posted status.
