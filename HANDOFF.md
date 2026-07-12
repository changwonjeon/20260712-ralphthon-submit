---
type: Human Handoff
title: Ralphthon Track 2 Build and Submission Handoff
description: Acceptance status, frozen evidence, commands, limitations, live boundary, and human checks.
tags: [ralphthon, track-2, handoff, submission]
timestamp: 2026-07-12T14:46:40+09:00
status: local-build-installed-discovered-live-unverified
---

# Ralphthon Track 2 Handoff

## Outcome

The Track 2-only review runtime, wrapper Skill, native-agent definitions,
deterministic validators, synthetic fixtures, mock recovery evidence, anonymous
Technical Report, Title, Abstract, and operator runbooks are present. The
official `auto-research` subtree is pinned and byte-identical in staging.
An independent native `agent_type=architect` audit passed the staged
architecture, and changed-files-only cleanup plus the full post-clean
regression and submission audit passed.

The verified 28-file package is installed under project `.codex`. A genuinely
fresh Codex session exposed both Skills and successfully spawned all three
custom native roles. No production claim or post occurred; the actual
OpenAgentReview contract and live completion remain unverified until the
authorized 16:35 KST window.

## P0 acceptance status

| P0 gate | Status | Evidence or blocker |
| --- | --- | --- |
| Official `auto-research` pinned at `a9f4f2583648ef4ca54f980f951ae393d153473f` | PASS INSTALLED | Staging and project `.codex` match the 11-file manifest and upstream recursive diff |
| Combined two-Skill and three-agent staged installer | PASS | `scripts/install-track2-codex.py --check-staging` validates 28/28 files |
| Official and wrapper Skills installed in project `.codex` | PASS | Installer read-back reports 28/28 exact matches, zero missing, zero conflicts |
| Wrapper Skill with references, assets, and validators | PASS INSTALLED | Staging and project-local copies match |
| Review Worker, build verifier, submission auditor | PASS INSTALLED AND DISCOVERED | Three typed custom-role spawns returned their expected completion tokens |
| Canonical upstream plus event review schema | PASS | Contribution, Significance, Originality, and Comment remain independent |
| Per-paper input and evidence freeze before Worker execution | PASS IN SYNTHETIC MOCK | Per-paper manifests under the frozen evidence tree |
| Root-only platform, ledger, status, claim, and post authority | PASS BY CONTRACT AND MOCK TEST | Worker surfaces return `ReviewDraft` only |
| Bounded queue, lease, atomic ledger, idempotency, status-first reconciliation | PASS IN SYNTHETIC MOCK | Frozen aggregate plus ledger and failure evidence |
| Gold fixture, matching rule, threshold, and naive baseline frozen before run | PASS | `fixtures/FROZEN_MANIFEST.sha256` and fixture validation evidence |
| Three 10-paper repetitions | PASS IN SYNTHETIC MOCK | 30/30 complete, schema 100%, duplicate posts 0 |
| Malformed JSON, Worker timeout, claim timeout, post timeout, in-process ledger reopen | PASS IN SYNTHETIC MOCK | Each condition recovered once without duplicate posts |
| Actual process interruption and fresh-process resume | PASS IN SYNTHETIC MOCK | `evidence/process-restart-proof/aggregate.json`; exit 75 to 0, final 10/10, prefix and prior artifacts preserved |
| Process rerun idempotency | PASS IN SYNTHETIC MOCK | Ledger and outbox byte-identical after rerun |
| Root manifests, outbox JSON, clipboard text, ledger, and summary | PASS IN SYNTHETIC MOCK | `manifests/`, `outbox/`, and `clipboard/` each contain 10 paper artifacts; root ledger and summary are present |
| Technical Report source, PDF, Title, and Abstract | PASS | Offline Tectonic exit 0; 3 pages; body marker page 3; anonymous metadata/text/source scans, embedded-font checks, exact Title/Abstract match, raw-number check, and three-page visual QA passed |
| `review-agent.md` and root `README.md` | PASS | Final evidence identities, mock/live boundary, and install instructions are present |
| New-session discovery for both Skills | PASS | `evidence/external-final-verification.json` |
| Explicit native architect verification | PASS FOR ARCHITECTURE; ENVIRONMENT BLOCKER RESOLVED LATER | The preserved 14:00 snapshot is `evidence/architect-audit.md`; post-Ralph install/discovery resolution is recorded separately |
| Full post-clean runtime and package regression | PASS | 49/49 tests; compileall; wrapper 17/17, upstream 11/11, fixtures 16/16, installer 28/28; root and JSON audits |
| Changed-files-only cleanup | PASS | `evidence/ai-slop-cleaner-report.md`; root direct diff review and post-clean read-back completed |
| Production claim/post and live completion | NOT RUN | Authorized window begins at 16:35 KST |

## Authoritative quantitative evidence

Runtime and quality measurements used in the report, Abstract, README, agent
definition, and this handoff come from:

`evidence/mock-validation-final-20260712T1335KST/aggregate.json`

SHA-256:
`239f2de62fcc5a1671b6cf86efc4f3a63077c3e3d2c81ccd2ad04e25a2077910`.
Actual two-process measurements come from
`evidence/process-restart-proof/aggregate.json`, SHA-256
`18d536ca72f87e03117af28d5534d10de1b316a3a0dc26b52fd5a2849e0de5d2`.

| Measurement | Observed synthetic-mock result |
| --- | ---: |
| Normal repetitions | 3 |
| Assigned instances across normal runs | 30 |
| Mock verified-complete across normal runs | 30/30 |
| Schema-valid across normal runs | 30/30 (100%) |
| Duplicate post attempts across normal runs | 0 |
| Duplicate idempotency keys across normal runs | 0 |
| Fault-run mock verified-complete | 10/10 |
| Fault-run schema-valid | 10/10 |
| Fault-run duplicate post attempts | 0 |
| Malformed JSON repairs | 1 |
| Worker timeout recoveries | 1 |
| Claim timeout reconciliations | 1 |
| Post timeout reconciliations | 1 |
| In-process ledger reopen recoveries | 1 |
| Interrupted process exit and mock-verified prefix | 75 after 4 papers |
| Resumed process exit and final completion | 0, 10/10 |
| Resumed process schema and duplicates | 10/10, 0 |
| Resume preservation | Four-paper ledger prefix and completed manifest/outbox bytes preserved |
| Deterministic seeded quality | TP 20, FP 0, FN 0, F1 1.0 |
| Naive seeded baseline | TP 10, FP 0, FN 10, F1 0.6667 |

The no-op process-rerun record also reports byte-identical ledger and outbox
content after full completion.
The evidence kind is `synthetic_mock_runtime_validation`, external side effects
are false, and production claim/post is false.

These results do not measure OpenAgentReview, network or browser latency,
scientific review quality, human agreement, or generalization to unseen
papers. The deterministic seeded-quality result must not be described as a
blind or live agent score. The Worker-timeout result is mock-adapter
`TimeoutError` recovery, not proof that a running thread was forcibly killed.

The canonical frozen prompt SHA-256 is
`29e116b4b25663b65ff9920057a87d2b850080b97be836b364149cb95d9d914a`.
The canonical frozen schema SHA-256 is
`cd19220f5435dc1da4146bd7c1e467cf4bea0ac0ecb69b2ac518b53922363d24`.
The wrapper manifest SHA-256 is
`daa71e174640dbc135f9a735bb4d42db99dba4e7abd7802b7aeb7866ac75c7f3`.

## Skill and agent installation

Verify staged content:

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

Install or re-verify the project-local package idempotently:

```bash
python3 scripts/install-track2-codex.py --install
python3 scripts/install-track2-codex.py --check
```

Fresh-session discovery of both invocations and all three custom native roles
has passed. The invocations are:

```text
$auto-research
$ralphthon-track2-review-agent
```

Use the official Skill only through its Track 2-only frozen-paper path.

## Build, run, and validation commands

Freeze manifests without platform actions:

```bash
python3 staging/.codex/skills/ralphthon-track2-review-agent/scripts/run_batch.py \
  --mode BUILD \
  --papers fixtures/throughput/papers.json \
  --root-dir . \
  --output-dir /tmp/ralphthon-track2-build
```

Run a local deterministic mock batch:

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
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The frozen evidence-producing command was:

```bash
python3 tests/run_mock_evidence.py \
  --output evidence/mock-validation-final-20260712T1335KST \
  --process-restart-evidence evidence/process-restart-proof/aggregate.json
```

It exited successfully and intentionally emitted no standard output. Do not
overwrite that directory; use a new output directory for a recheck.

The final fresh post-clean regression record is
`evidence/post-clean-verification.json`:

```text
exit_code=0
tests_run=49
failures=0
errors=0
elapsed_seconds=1.654
compileall=PASS
wrapper_hashes_verified=17
upstream_hashes_verified=11
frozen_fixture_hashes_verified=16
installer_files_verified=28
root_audit=10/10; schema=10/10; duplicate_attempts_and_keys=0
quick_validate=2/2 Skills valid; TOML=3/3; YAML=2/2
```

Offline Tectonic build:

```bash
cd submission
TECTONIC_CACHE_DIR=../tmp/pdfs/tectonic-work-cache \
  tectonic -C -b ../tmp/pdfs/tectonic-cache.zip \
  technical-report.tex --keep-logs --keep-intermediates
```

The normal Tectonic bundle path panicked twice before TeX in the host
`system-configuration`/`reqwest` path. Raw failures remain in
`evidence/report/tectonic-network-attempt.log` and
`evidence/report/tectonic-only-cached-attempt.log`. The local-bundle Tectonic
path succeeds and its exact output is retained in
`evidence/report/tectonic-offline-success.log`.

The final PDF audit is `evidence/report/report-validation.txt`. The PDF was
built at 14:16:01 KST, and root repeated three-page visual QA at 14:20:57 KST.
Final artifact SHA-256 values are:

```text
d8b17f65cb9f965214127869badf8ce64d4f4749d46607dedda69b46d503c2a0  submission/technical-report.tex
b1a8c476f9bf0718d4a64c7192467fad588fe7a35f25380a9d363696548db18f  submission/technical-report.pdf
23451a0afe573a7ca17e8de1e81c32a20fe7ff09ec6cfee017253fb888c9147e  submission/TITLE.txt
17cee83d5261050d9b4c5f3e9271f6b318109b252a83649dff8bb42eba7f30dd  submission/ABSTRACT.txt
```

## Deliverables

- Technical Report source: `submission/technical-report.tex`
- Technical Report PDF: `submission/technical-report.pdf`
- Title: `submission/TITLE.txt`
- Abstract: `submission/ABSTRACT.txt`
- Review Agent definition: `review-agent.md`
- Project overview and reproduction commands: `README.md`
- Manual live fallback: `MANUAL_PLATFORM.md`
- Frozen runtime and quality aggregate:
  `evidence/mock-validation-final-20260712T1335KST/aggregate.json`
- Actual process resume proof: `evidence/process-restart-proof/aggregate.json`
- Fresh post-clean regression: `evidence/post-clean-verification.json`
- Independent native architect audit: `evidence/architect-audit.md`
- Changed-files-only cleanup report: `evidence/ai-slop-cleaner-report.md`
- Prompt-to-artifact completion audit: `evidence/completion-audit.json`,
  SHA-256 `d94facf2c1d4b3d46e083ae099f9fab585eab7069bee7a2f42f02402b56aad87`
- Report build and audit evidence: `evidence/report/`
- Upstream Skill manifest: `staging/auto-research.sha256`
- Wrapper and agent manifest: `staging/ralphthon-track2-review-agent.sha256`,
  SHA-256 `daa71e174640dbc135f9a735bb4d42db99dba4e7abd7802b7aeb7866ac75c7f3`
- Staged package validation: `evidence/discovery/staged-codex-validation.txt`
- Post-Ralph install and fresh-session discovery:
  `evidence/external-final-verification.json`, SHA-256
  `5d6cdeb175c190413a78a58f1e5400a3d9bbc707561ff832b819102b246b0813`
- Historical read-only discovery attempt: `evidence/discovery/fresh-session-discovery.md`

## Changed implementation and artifact surfaces

- `src/ralphthon_track2_review_agent/`
- `tests/`
- `fixtures/`
- `staging/.codex/skills/auto-research/`
- `staging/.codex/skills/ralphthon-track2-review-agent/`
- `staging/.codex/agents/`
- `scripts/install-track2-codex.py`
- `evidence/`
- `manifests/`
- `outbox/`
- `clipboard/`
- `ledger.jsonl`
- `ledger.state.json`
- `summary.json`
- `submission/`
- `README.md`
- `review-agent.md`
- `MANUAL_PLATFORM.md`
- `HANDOFF.md`
- `CHECKPOINT.json`
- `FAILURE_LEDGER.md`
- `work/run-ralph-direct.sh`

## Known failures and limitations

1. The production adapter is intentionally absent. No endpoint, selector,
   assignment rule, accepted field mapping, or posted-success marker has been
   guessed.
2. The bundled CLI is BUILD/DRY-RUN-only and rejects `LIVE` unconditionally;
   no programmatic production adapter path is implemented.
3. All runtime and quality measurements are deterministic synthetic-mock
   evidence. The seeded quality comparison is not a blind LLM-worker
   evaluation.
4. In-process synthetic elapsed times are not representative of the 25-minute
   browser and paper-review window and are not used as a live speed claim.
5. Default-bundle Tectonic attempts fail in the host network/configuration
   path; the preserved local-bundle command is the verified build route.
6. Mock `posted_verified` is a local adapter state, not an OpenAgentReview
   receipt.
7. The Worker-timeout injection raises mock-adapter `TimeoutError` and verifies
   bounded recovery. It does not forcibly terminate an already running thread.
8. The independent architect audit is intentionally preserved as a 14:00 KST
   pre-clean snapshot. Its older TeX/PDF/wrapper hashes and then-pending cleanup
   status are historical audit evidence; `evidence/post-clean-verification.json`
   and `evidence/completion-audit.json` contain the authoritative later
   read-back.

## 16:35 KST live command and boundary

With the project-local package installed and fresh-session discovery already
verified, invoke at the authorized live window:

```text
$ralphthon-track2-review-agent LIVE: perform at most 45 seconds of read-only LIVE_DISCOVERY, use only the observed platform contract, and switch to MANUAL_PLATFORM.md if automation is not verified.
```

This Skill-guided path is the safe live entry surface. The bundled shell CLI is
BUILD/DRY-RUN-only and rejects `LIVE` unconditionally; do not use it for
discovery. During read-only discovery, record the actual assigned count, claim
semantics, PDF access path, accepted review fields and ranges, multiple-claim
permission, and the posted-success marker.

Platform priority is:

```text
reconcile/post > download > claim > browse
```

Keep queue high-water at three. Raise it to six only after the live interface
confirms multiple claims are allowed. Success remains
`posted_verified == assigned_count`.

## Manual fallback

If the adapter or browser automation is not verified within 45 seconds, follow
`MANUAL_PLATFORM.md`:

1. Human claims and downloads through the visible signed-in UI.
2. Root freezes and reads back each paper/evidence manifest before Worker use.
3. Workers return `ReviewDraft` only.
4. Root validates and writes outbox JSON plus clipboard-ready text.
5. Human copies only fields visibly accepted by the form, submits once, and
   verifies posted state before Root records `posted_verified`.
6. Ambiguous claim or post states are checked in the UI before any retry.

## Human checks still required

- Upload PDF, Title, and Abstract before 16:30 KST and retain the submission
  receipt or visible confirmation.
- At 16:35 KST, perform `LIVE_DISCOVERY` and record the actual platform
  contract before any automated side effect.
- If automation remains unverified, operate the manual lane and retain each
  visible posted-state confirmation.
- At hard stop, export ledger, outbox, receipts, failures, and unresolved
  unknown states without converting them into success.
