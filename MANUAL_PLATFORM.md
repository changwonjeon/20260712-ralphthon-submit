---
type: Live Runbook
title: Ralphthon Track 2 Manual Platform Fallback
description: OpenAgentReview 계약이 확인되지 않았거나 자동 브라우저가 불안정할 때 Root와 사람 운영자가 사용하는 selector-free fallback.
tags: [ralphthon, track-2, live, manual-fallback, okf]
timestamp: 2026-07-12T12:49:00+09:00
status: build-verified-live-unverified
---

# Safety boundary

This runbook is for the 16:35-17:00 KST live window. Ralph build and dry-run
work must not claim or post production papers. No endpoint, DOM selector,
receipt shape, or claim rule is assumed here. The visible OpenAgentReview state
is authoritative until an official contract is observed.

# First 45 seconds: `LIVE_DISCOVERY`

The Root operator records the visible assigned count, review field labels and
ranges, claim reversibility or TTL, PDF retrieval path, posted-success marker,
and whether multiple claims are permitted. Keep the queue high-water at three;
raise it to six only after the live interface confirms multiple claims are
allowed. If discovery cannot establish a safe automated contract within 45
seconds, stay on this manual lane.

Platform work is serialized in this order:

1. reconcile an ambiguous post or complete a ready post;
2. download an already claimed paper;
3. claim the next paper;
4. browse for additional assignments.

# Manual paper loop

1. In the signed-in browser, claim one visible assignment and save its paper
   and any supplied evidence locally. Preserve the platform paper identifier.
2. Before any Review Worker runs, Root creates the per-paper manifest and
   verifies the paper, evidence, prompt, schema, and agent hashes by read-back.
3. Give only that frozen manifest and its allowed files to one Review Worker.
   Workers return `ReviewDraft`; they never claim, post, inspect remote status,
   or mutate the ledger.
4. Run the deterministic validator. One targeted schema repair is allowed. An
   identity mismatch is blocking and must not be repaired by changing hashes.
5. Root writes the validated draft to `outbox/` as JSON and to `clipboard/` as
   plain field-ready text. The local artifact retains Contribution,
   Significance, Originality, and Comment as independent fields; only fields
   visibly accepted by the platform are copied to the form.
6. Enter the review through the visible form, submit once, then verify the
   visible posted state or receipt before marking `posted_verified`.
7. If claim or post times out, inspect visible status first. Never repeat an
   ambiguous side effect merely because the client timed out.

# Deadline degradation

- T+15:00: if verified completion is below 70 percent, reduce draft timeout to
  60 seconds and use concise evidence-bound comments.
- T+20:00: if more than one assignment remains, stop nonessential analysis and
  use the minimum complete schema with explicit limitations.
- T+22:00: prioritize validation, post, and reconciliation over new analysis.
- T+23:30: start a full visible status audit.
- T+24:30: stop new side effects and export ledger plus outbox.

# Completion and unresolved state

Success is exactly `posted_verified == assigned_count`. A local outbox file,
submit click, client response, mock result, or planned action is not verified
live completion. Keep ambiguous operations as `claim_unknown` or
`post_unknown`, preserve their evidence, and report them honestly at hard stop.
