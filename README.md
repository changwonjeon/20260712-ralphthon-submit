---
type: Project Overview
title: Ralphthon Track 2 Review Agent
description: Evidence-bound Codex Skill and distributed execution structure for producing ICML-style reviews from frozen papers under a fixed deadline.
tags: [ralphthon, track-2, review-agent, codex, okf]
timestamp: 2026-07-12T16:15:52+09:00
status: build-installed-discovered-live-unverified
---

# Ralphthon Track 2 Review Agent

[Korean README](README_kr.md)

This repository provides a Codex Skill and execution evidence for reviewing assigned papers in ICML style under a fixed deadline while preserving the official `auto-research` Skill's Track 2-only frozen-paper path. Every paper and evidence bundle is frozen before Worker execution, and a single Root Coordinator owns all platform side effects.

The implementation has been validated against deterministic synthetic fixtures, an executable risk-gated mock verifier path, and a separate two-paper qualitative review/verifier trial over frozen public arXiv PDFs. It has not claimed an OpenAgentReview paper or posted a production review, and it does not claim general review accuracy, human agreement, or live-platform throughput.

## Current status

| Surface | Status | Evidence |
| --- | --- | --- |
| Official `auto-research` Skill | PASS INSTALLED | Upstream commit `a9f4f2583648ef4ca54f980f951ae393d153473f`; the 11-file manifest and recursive diff match. |
| Wrapper Skill and native agents | PASS INSTALLED AND DISCOVERED | Project-local `.codex` installation and fresh-session discovery completed. |
| Combined package | PASS | Staging and installed copies match 29/29. |
| Regression and performance-policy evaluator | PASS LOCALLY | All 70 regression tests and `tests/performance_evaluator.py` pass. |
| Normal synthetic mock | PASS IN MOCK | Three 10-paper runs completed 30/30 with 100% schema validity and zero duplicate posts. |
| Failure recovery and restart | PASS IN MOCK | Malformed JSON, Worker, claim, and post timeouts; ledger reopen; and actual two-process resume were verified. |
| Evidence-first and risk-gated calibration | PASS IN EXECUTABLE DRY-RUN | Explicit risk sidecars drive the cap, gates, PASS/REPAIR, fail-open verifier faults, one shared repair budget, revalidation, ledger, and summary paths. |
| Real-paper reviewer/verifier trial | PASS QUALITATIVE, NOT GOLD-LABELED | Two frozen public arXiv PDFs produced paper-specific reviews; an independent verifier returned PASS on both. |
| English Technical Report | PASS LOCAL PDF | Four-page ICML report; PDF metadata Author `Anonymous`; fonts, text, and all rendered pages verified. |
| Korean comprehension report | PASS LOCAL PDF | Six-page A4 single-column companion; PDF metadata Author `Anonymous`; fonts, text, and all rendered pages verified. |
| Production adapter and live completion | **NOT RUN** | The actual UI contract must be observed during the authorized live window. |

## Architecture

```text
Official auto-research Track 2 contract
                    |
                    v
Root Coordinator --+-- serialized status / claim / post / reconcile
        |
        +-- Review Worker 1 --+
        +-- Review Worker 2 --+--> ReviewDraft --> validator --> risk gate --+
        +-- Review Worker 3 --+                         |                  |
                                                        | fast path        | high risk only
                                                        v                  v
                                             atomic ledger + outbox   bounded verifier
                                                        ^                  |
                                                        +-- one repair ----+
```

Root owns assignment discovery, the bounded queue, leases, manifests, status, claim, post, receipts, outbox, and the atomic ledger. Each of the three Workers receives one frozen manifest and active lease and returns only a `ReviewDraft`; Workers have no platform or shared-state authority.

## Execution contract

- Freeze the paper, evidence, schema, prompt, and agent version SHA-256 for every paper.
- Reject `paper_id`, `lease_id`, `input_hash`, `evidence_hash`, `prompt_hash`, or `agent_version` mismatches without repair.
- Preserve official `contribution` and event `significance`, `originality`, and `comment` as independent fields; never convert between them.
- Run deterministic identity, schema, score-range, evidence-location, and required-prose validation first.
- Share one targeted-repair budget per paper across schema and calibration repairs.
- Before canonical JSON, each Worker performs a private claim map, falsification pass, score anchoring, and consistency pass.
- Low confidence or an extreme recommendation alone never invokes the verifier. Only a schema-valid draft with compound risk score at least three is eligible.
- Bound calibration to `min(3, ceil(assigned_count * 0.3))` papers, one verifier, 20 seconds and three findings per paper, before T+15 with validated backlog at most two.
- Do not reduce the three drafting slots for verifier work while drafts remain pending. Fast or emergency mode, slow posting pace, and any prior repair bypass calibration.
- After claim or post timeout, check status before retrying. Never repeat a successful or reconciled post.
- Live success is exactly `posted_verified == assigned_count`.

## Repository map

- `src/ralphthon_track2_review_agent/` contains the runtime, contract, manifest, and ledger implementation.
- `.codex/skills/` and `.codex/agents/` contain the two installed Skills and three native-agent definitions.
- `staging/.codex/` is the frozen installation source package.
- `fixtures/` contains throughput papers, seeded quality cases, the naive baseline, and a frozen manifest.
- `fixtures/calibration/` contains explicit risk-sidecar plans for executable verifier DRY-RUNs.
- `tests/` covers contracts, runtime, failures, restarts, CLI behavior, quality, and evidence consistency.
- `evidence/mock-validation-final-20260712T1335KST/` contains the authoritative synthetic-mock results.
- `evidence/process-restart-proof/` contains actual two-process interruption and resume evidence.
- `evidence/performance-optimization.json` records the current calibration policy and evaluator result.
- `review_trials/20260712-real-paper-trial/` contains the two frozen real-paper reviews, manifests, and independent verifier records.
- `manifests/`, `outbox/`, `clipboard/`, and `ledger.jsonl` contain mock-run and manual-fallback artifacts.
- `submission/` contains the official English Technical Report and the Korean comprehension companion, each with Title and Abstract files.
- `review-agent.md`, `MANUAL_PLATFORM.md`, and `HANDOFF.md` define the agent, live fallback, and operator handoff.

## Installation and verification

Verify the staged package and official upstream Skill.

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

Install idempotently into project-local `.codex` and verify the read-back.

```bash
python3 scripts/install-track2-codex.py --install
python3 scripts/install-track2-codex.py --check
```

Run the regression suite and quality-per-minute policy evaluator.

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 tests/performance_evaluator.py
```

## BUILD and DRY-RUN

Freeze manifests without platform side effects.

```bash
python3 staging/.codex/skills/ralphthon-track2-review-agent/scripts/run_batch.py \
  --mode BUILD \
  --papers fixtures/throughput/papers.json \
  --root-dir . \
  --output-dir /tmp/ralphthon-track2-build
```

Run the mock adapter with three bounded Workers.

```bash
python3 staging/.codex/skills/ralphthon-track2-review-agent/scripts/run_batch.py \
  --mode DRY-RUN \
  --papers fixtures/throughput/papers.json \
  --root-dir . \
  --output-dir /tmp/ralphthon-track2-dry-run \
  --workers 3
```

Exercise the executable risk-gated verifier branch with an explicit synthetic sidecar. Calibration is off by default; the Python adapter is a deterministic test double and does not impersonate a native Codex verifier.

```bash
python3 staging/.codex/skills/ralphthon-track2-review-agent/scripts/run_batch.py \
  --mode DRY-RUN \
  --papers fixtures/throughput/papers.json \
  --root-dir . \
  --output-dir /tmp/ralphthon-track2-calibration \
  --workers 3 \
  --calibration mock \
  --calibration-plan fixtures/calibration/high-risk-pass.json
```

The authoritative evidence was produced by the command below. Do not overwrite the frozen evidence directory; use a different output path for revalidation.

```bash
python3 tests/run_mock_evidence.py \
  --output evidence/mock-validation-final-20260712T1335KST \
  --process-restart-evidence evidence/process-restart-proof/aggregate.json
```

## Skill usage

In a fresh Codex session, invoke the official Skill first and select its Track 2-only frozen-paper path.

```text
$auto-research
```

Then invoke the wrapper Skill.

```text
$ralphthon-track2-review-agent
```

The bundled shell CLI supports `BUILD` and `DRY-RUN` only and always rejects `LIVE`. In DRY-RUN, `--calibration mock` executes the policy and state transitions from an explicit sidecar. In a native Codex run, Root separately invokes `track2-review-verifier`; Python never shells out to simulate independence. Live work uses the Skill execution contract and only platform behavior actually observed during read-only discovery.

## Results and claim boundary

| Measurement | Synthetic-mock result |
| --- | ---: |
| Normal repetitions | 3 |
| Complete and schema-valid | 30/30, 100% |
| Duplicate post attempts and idempotency keys | 0, 0 |
| Fault run | 10/10 complete, schema 10/10, duplicates 0 |
| Actual process resume | First process exit 75 after four papers; fresh process exit 0 at 10/10 |
| Seeded quality | TP 20, FP 0, FN 0, F1 1.0 |
| Naive seeded baseline | TP 10, FP 0, FN 10, F1 0.6667 |
| Executable calibration evaluator | 10 risks scored, bounded subset selected, max verifier concurrency 1, 10/10 posted |
| Real-paper qualitative trial | 2/2 schema/manifest valid, independent verifier PASS 2/2, repairs 0 |

The authoritative runtime and quality evidence is `evidence/mock-validation-final-20260712T1335KST/aggregate.json`, SHA-256 `239f2de62fcc5a1671b6cf86efc4f3a63077c3e3d2c81ccd2ad04e25a2077910`. Process-resume evidence is `evidence/process-restart-proof/aggregate.json`, SHA-256 `18d536ca72f87e03117af28d5534d10de1b316a3a0dc26b52fd5a2849e0de5d2`. The wrapper manifest SHA-256 is `b9fc57b4755c00d273a999be3c7900d2fc7d85c1c897f8fd91a6e8149bc3eaba`.

The synthetic results measure fixtures containing intentionally seeded issues. The two-paper trial shows that separated reviewer/verifier contexts can produce and audit paper-specific findings, but it has no gold review, author rebuttal, raw experiment execution, or human correctness label. None of these results establish general review quality, agreement with judges, browser or network latency, or OpenAgentReview completion. The Worker-timeout fault validates mock-adapter `TimeoutError` recovery; it is not evidence that a running thread was forcibly terminated.

## English submission and Korean companion

| Artifact | Official English | Korean comprehension companion |
| --- | --- | --- |
| Technical Report PDF | `submission/technical-report.pdf` | `submission/technical-report_kr.pdf` |
| Technical Report source | `submission/technical-report.tex` | `submission/technical-report_kr.tex` |
| Title | `submission/TITLE.txt` | `submission/TITLE_kr.txt` |
| Abstract | `submission/ABSTRACT.txt` | `submission/ABSTRACT_kr.txt` |

The English ICML report is the official submission artifact. Files ending in `_kr` are Korean comprehension companions and do not follow the ICML page or column constraints. Shared submission and operation artifacts are `review-agent.md`, `HANDOFF.md`, and `MANUAL_PLATFORM.md`. Immediately before upload, confirm that the English PDF, Title, and Abstract agree and record fresh hashes.

```bash
shasum -a 256 \
  submission/technical-report.pdf \
  submission/technical-report.tex \
  submission/TITLE.txt \
  submission/ABSTRACT.txt \
  submission/technical-report_kr.pdf \
  submission/technical-report_kr.tex \
  submission/TITLE_kr.txt \
  submission/ABSTRACT_kr.txt
```

The verified offline Tectonic command for the English report is:

```bash
cd submission
TECTONIC_CACHE_DIR=../tmp/pdfs/tectonic-work-cache \
  tectonic -C -b ../tmp/pdfs/tectonic-cache.zip \
  technical-report.tex --keep-logs --keep-intermediates
```

## LIVE operation and manual fallback

At the authorized live start, invoke the wrapper Skill in a fresh Codex session with:

```text
$ralphthon-track2-review-agent LIVE: perform at most 45 seconds of read-only LIVE_DISCOVERY, use only the observed platform contract, and switch to MANUAL_PLATFORM.md if automation is not verified.
```

Read-only `LIVE_DISCOVERY` may spend at most 45 seconds confirming the assigned count, claim semantics, PDF access path, accepted fields and score ranges, whether multiple claims are allowed, and the posted-success marker. Never invent an endpoint or selector.

If automation is not verified, switch immediately to `MANUAL_PLATFORM.md`.

1. A human uses the signed-in UI to claim and download.
2. Root freezes and reads back each paper and evidence manifest.
3. A Worker returns only a `ReviewDraft`.
4. Root runs deterministic validation and writes outbox JSON and clipboard text.
5. The human submits only fields accepted by the observed UI and confirms posted state.
6. When claim or post state is ambiguous, inspect UI status before retrying.

Platform priority is `reconcile/post > download > claim > browse`. Start with queue high-water three and raise it only after observing that multiple claims are permitted. The current production adapter and live-completion state remain **NOT RUN**.
