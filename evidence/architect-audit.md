---
type: Architect Audit
title: Ralphthon Track 2 Independent Architecture Audit
description: Independent native architect verdict over the staged implementation, frozen evidence, and submission package.
tags: [ralphthon, track-2, architect, audit]
timestamp: 2026-07-12T14:00:00+09:00
status: architecture-pass-full-p0-blocked
---

# Independent Architect Audit

## Verdict

`ARCHITECTURE_VERDICT: PASS`

The implemented and staged BUILD/DRY-RUN package has a coherent fail-closed
architecture for frozen-input review, three bounded draft workers, Root-owned
side effects, deterministic validation, append-only/atomic state, status-first
reconciliation, restart recovery, and manual outbox fallback. No P0 code defect
was found in that audited scope. This PASS does **not** approve a production
adapter, live platform behavior, or project-local Skill discovery.

`FULL_P0_VERDICT: BLOCKED`

The full Ralph P0/exit contract is not complete. All 28 staged Codex files are
still absent from project `.codex`, and fresh-session discovery failed before
prompt evaluation under the sandbox. The changed-files-only cleanup and its
post-cleanup full regression are also pending. Live platform discovery,
production claim/post, and live completion remain deliberately unrun. These
states must not be converted into PASS.

## Audit context

- Audit role: native `agent_type=architect`, independent read-only review.
- Audited at: `2026-07-12T14:00:00+09:00`.
- Repository HEAD: `760971f895950b8c2a7376c2551f923777cf8c78`.
- Required baseline: `67a89a0ee7c18d6abdd4c5c734d5b1bdc97f8784`; verified as an ancestor of HEAD.
- Official upstream worktree: clean at
  `a9f4f2583648ef4ca54f980f951ae393d153473f`.
- Worktree: intentionally dirty with Ralph artifacts and the already-applied
  `work/run-ralph-direct.sh` compatibility change. This audit did not modify any
  implementation, fixture, document, raw evidence, or generated artifact.
- Required intake reviewed: `RALPH_GOAL.md`, the frozen context and execution
  plan, participant guide, submission contract, and official upstream
  `auto-research/SKILL.md`.

## P0 findings

### P0-BLOCKED-1 — project-local installation is absent

`python3 scripts/install-track2-codex.py --check` reports `not-installed` with
28 missing files, zero matches, and zero content conflicts. This directly blocks
the required project paths in `RALPH_GOAL.md:39-41`. The staged installer is
valid, but staging is not installation. See
`evidence/discovery/staged-codex-validation.txt:21-31`,
`evidence/discovery/fresh-session-discovery.md:50-54`, and
`CHECKPOINT.json:11-13,39-41`.

### P0-BLOCKED-2 — fresh-session Skill/native-agent discovery is unproved

Both isolated Codex discovery surfaces exited 1 with `Operation not permitted`
before a session context rendered. Static YAML/TOML/hash validation cannot
substitute for the required new-session discovery of `$auto-research` and
`$ralphthon-track2-review-agent`. Native agent definitions are therefore valid
in staging but not runtime-discovered or invocation-proven. See
`RALPH_GOAL.md:66`, `evidence/discovery/fresh-session-discovery.md:15-52`, and
`FAILURE_LEDGER.md:39-46`.

### P0-PENDING-3 — changed-files-only cleanup and final regression

The mandatory cleanup manifest contains only three comments and no file paths
at `.omx/ralph/changed-files.txt:1-3`. Consequently the required changed-files-
only deslop pass and post-deslop full regression have not occurred. This is an
exit-gate precondition from `RALPH_GOAL.md:75`, not an architecture defect.

### P0-DEFERRED-4 — production adapter and live completion

The source rejects every `LIVE` CLI request before writing
(`src/ralphthon_track2_review_agent/runtime.py:343-359`), and the handoff
correctly records the production adapter as absent
(`HANDOFF.md:265-285`). The selector-free manual lane is defined in
`MANUAL_PLATFORM.md:10-68`. No endpoint, selector, assignment count, field
mapping, receipt, production claim/post, or `posted_verified == assigned_count`
live result was observed. This respects `RALPH_GOAL.md:80-85`, but the live
outcome remains deferred rather than passed.

## Major findings

No major defect was found in the staged BUILD/DRY-RUN implementation. The two
environment/runtime-verification gaps above remain P0 blockers: staged native
agent TOML is not evidence of successful native-agent discovery, and synthetic
mock completion is not evidence of live completion.

## Minor findings

1. `staging/.codex/skills/ralphthon-track2-review-agent/SKILL.md:20` says LIVE is
   rejected “unless” a verified adapter and production authority are supplied
   programmatically, while the current public implementation unconditionally
   rejects LIVE at `src/ralphthon_track2_review_agent/runtime.py:355-359` and has
   no authority parameter. The behavior is safely fail-closed, and
   `HANDOFF.md:270-274,296-299` discloses the absent adapter, but the Skill wording
   should describe the current CLI as BUILD/DRY-RUN-only until a separately
   verified live integration exists.
2. `src/ralphthon_track2_review_agent/runtime.py:19` imports an unused
   `WORKER_PROMPT` alias, and `src/ralphthon_track2_review_agent/ledger.py:13`
   imports unused `read_json`. These are safe cleanup candidates with no
   behavioral significance.

## Contract matrix

| Contract | Verdict | Grounded evidence |
| --- | --- | --- |
| Official upstream byte identity | PASS IN STAGING | Upstream worktree is clean at the required commit; recursive diff is empty; all 11 entries in `staging/auto-research.sha256` verify. |
| Official Skill project install | BLOCKED | Installer read-back reports 28/28 destinations missing; `evidence/discovery/fresh-session-discovery.md:50-54`. |
| Wrapper Skill and native agents | PASS STATIC / DISCOVERY BLOCKED | Wrapper frontmatter passes quick validation; three TOMLs parse; 17/17 wrapper manifest entries verify; definitions at `staging/.codex/agents/track2-review-worker.toml:1-13`, `track2-review-verifier.toml:1-11`, and `track2-submission-auditor.toml:1-11`. |
| Canonical review fields | PASS | Independent `contribution`, `significance`, `originality`, and `comment` definitions and ranges are explicit in `src/ralphthon_track2_review_agent/contract.py:20-28,52-139`; no conversion rule exists in `references/review-contract.md:15-21`. |
| Pre-Worker paper/evidence freeze | PASS IN MOCK | Manifest freezes file identities and aggregate hashes at `manifest.py:30-92`; runtime freezes it at `runtime.py:476-489` before worker submission at `runtime.py:506-514`. |
| Lease separate from immutable manifest | PASS | Manifest immutable keys exclude lease at `manifest.py:11-23`; Root creates the lease at `runtime.py:476-480`, and validation requires the active lease at `contract.py:269-282` and `runtime.py:543-547`. |
| Root-only authority | PASS BY ARCHITECTURE AND TEST | Worker future receives only draft inputs at `runtime.py:506-514`; status/claim/post/ledger/outbox operations remain on the coordinator path at `runtime.py:491-505,588-642`; native Worker prohibition is explicit at `track2-review-worker.toml:6-12`. |
| Three-worker bounded pool | PASS IN MOCK | Worker count is constrained to 1..3 at `runtime.py:360-361`; three logical slots and at most three active futures are enforced at `runtime.py:426-433,506-525`; concurrent-ID test is `tests/test_runtime_integration.py:53-86`. |
| Atomic ledger and idempotency | PASS IN MOCK | O_APPEND event write, fsync, and atomic snapshot are at `ledger.py:20-92`; post key creation and duplicate guard are at `runtime.py:597-639`; ledger audit is at `ledger.py:124-143`. |
| Status-first reconciliation | PASS IN MOCK | Pre-claim and timeout status checks are at `runtime.py:490-504`; pre-post and timeout checks are at `runtime.py:598-639`; persisted observations show two checks and one attempt for each injected ambiguous action in `evidence/mock-validation-final-20260712T1335KST/aggregate.json`. |
| Malformed/timeout/restart coverage | PASS IN SYNTHETIC MOCK | Fault run recovered one malformed JSON, Worker timeout, claim timeout, post timeout, and compatibility ledger reopen with 10/10 and no duplicates; actual two-process proof exited 75 then 0, preserved the four-paper prefix and completed bytes, and finished 10/10. Worker timeout is adapter `TimeoutError` recovery, not thread termination. |
| Frozen quality protocol | PASS FOR SEEDED FIXTURES ONLY | Freeze precedes execution in `fixtures/FREEZE.json:1-14`; exact location rule and thresholds are frozen in `fixtures/quality/EVALUATION_CONTRACT.md:14-54`; hashes verify 16/16. Candidate TP/FP/FN is 20/0/0, F1 1.0 versus baseline 10/0/10, F1 0.6667. This is not unseen-paper quality. |
| Outbox and manual fallback | PASS IN MOCK | Root has 10 manifests, 10 outbox JSON files, and 10 clipboard files; fresh ledger audit reports assigned 10, posted 10, duplicate attempts/keys 0. Manual procedure is selector-free at `MANUAL_PLATFORM.md:17-68`. |
| Report source/PDF/Title/Abstract | PASS | Latest TeX was built offline at 13:45:16 KST. PDF is 3 letter-size pages; body marker is page 3; metadata Author is Anonymous; four fonts are embedded/subset/Unicode-capable with no Type 3; forbidden scans and visual QA pass. See `evidence/report/report-validation.txt:10-69`. |
| Report metrics and claim boundary | PASS | Aggregate hashes match `report-validation.txt:56-64`; report/Abstract values match raw evidence; mock/live limits are explicit in `technical-report.tex:163-179,198-249`, `ABSTRACT.txt:1`, and `HANDOFF.md:87-96`. |
| Production claim boundary | PASS SAFETY / LIVE NOT RUN | BUILD and DRY-RUN use only local mock state; LIVE fails closed; no production claim/post occurred. Success remains exactly `posted_verified == assigned_count` in `runtime-runbook.md:34-40` and `MANUAL_PLATFORM.md:63-68`. |
| Fresh Codex discovery | BLOCKED | Required by `RALPH_GOAL.md:66`; failure evidence is `evidence/discovery/fresh-session-discovery.md:15-54`. |
| Changed-files-only deslop | PENDING | `.omx/ralph/changed-files.txt` has no actionable paths; post-cleanup regression has not run. |

## Fresh verification reviewed and rerun

- Unit/integration/evidence suite: `49` tests, `0` failures, `0` errors,
  completed in `0.862s` with
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -v`.
- Wrapper manifest: `17/17` SHA-256 entries PASS; manifest file SHA-256
  `0dc6e3137e5b9c503532c63512297f77699b283015a539de8a95fe2fa727aa2e`.
- Official upstream: `11/11` SHA-256 entries PASS; recursive diff empty;
  official commit exact.
- Frozen fixture manifest: `16/16` SHA-256 entries PASS.
- Combined staged installer: `28/28` files enumerated and valid.
- Skill validation: both staged Skills report `Skill is valid!`; YAML and all
  three native-agent TOMLs parse.
- Static compilation: Python `compileall` PASS with cache redirected outside the
  repository; repository-local `__pycache__`/`.pyc` count is zero.
- JSON read-back: 532 current fixture/evidence/outbox/manifest/state JSON files
  parsed successfully.
- Root fallback audit: assigned 10, `posted_verified` 10, schema-valid outbox
  10/10, duplicate post attempts 0, duplicate idempotency keys 0.
- Authoritative mock aggregate SHA-256:
  `239f2de62fcc5a1671b6cf86efc4f3a63077c3e3d2c81ccd2ad04e25a2077910`.
- Two-process proof SHA-256:
  `18d536ca72f87e03117af28d5534d10de1b316a3a0dc26b52fd5a2849e0de5d2`.
- Final PDF SHA-256:
  `07e3adef234cc6b1806c15dd855025776533a707de609df46de2c25148c770ad`;
  TeX SHA-256:
  `debe3798df5f52e2d419f8427ac98693e46d2547dbb55f46d9d6b477a3160b32`.
- All three persisted PDF page renders were independently inspected; text,
  tables, figure, notice, marker, references, and page numbers are legible with
  no clipping, overlap, or broken glyphs.

## Changed-files-only deslop safety

`DESLOP_VERDICT: CONDITIONALLY SAFE`

Do not start the pass while `.omx/ralph/changed-files.txt` is empty. First
populate it with explicit repo-relative human-authored implementation, test,
wrapper/native-agent, and documentation paths. Exclude the byte-identical
official upstream subtree, frozen fixtures, authoritative raw run evidence,
outbox/manifests/clipboard, PDF, renders, and logs. Those are immutable evidence
or generated artifacts, not cleanup candidates.

The safe cleanup scope is behavior-preserving only: remove the two unused
imports above and correct the fail-closed LIVE wording. Add no dependency or new
feature. If a staged wrapper/native file changes, regenerate and verify its
17-file manifest. Then rerun all 49 tests, wrapper/upstream/fixture/installer
hash checks, Skill/TOML/static validation, root audit, anonymity/metric scans,
and PDF checks if any submission source changed.

## Exit recommendation

Proceed to the bounded changed-files-only cleanup and fresh full regression.
After those pass, the staged architecture may remain PASS, but `FULL_P0_VERDICT`
must stay BLOCKED until a write-capable session installs all 28 files into
project `.codex` and a genuinely fresh Codex session discovers both Skills and
the native roles. Keep production/live state NOT RUN until authorized discovery;
use the manual lane if no verified adapter exists.
