---
type: Failure Ledger
title: Ralphthon Track 2 Failure Ledger
description: Ralph Loop에서 반복 실패와 축소 결정을 append-only로 기록한다.
tags: [ralphthon, track-2, ralph, failures, okf]
timestamp: 2026-07-12T12:15:45+09:00
---

# Failure Ledger

Ralph Loop는 같은 failure signature가 두 번 발생하면 시각, gate, signature, 시도한 repair, 축소 결정, 남은 위험을 이 문서에 추가한다. 기존 기록은 수정하거나 삭제하지 않는다.

현재 기록된 Ralph Loop 실패는 없다.

## 2026-07-12T12:41:56+09:00 — project-local `.codex` write denial

- Gate: official Skill installation and wrapper/native-agent creation.
- Signature: writes below project `.codex/` fail with `Operation not permitted` or are classified as outside the writable project, while ordinary workspace paths remain writable.
- Reproduction count: two independent lanes reproduced the same failure after POSIX owner-write permission was restored.
- Repairs attempted: verified the directory, added owner write permission, retried upstream copy, skill initialization, and direct patch creation.
- Reduction decision: build the byte-identical upstream subtree and wrapper/native-agent package under `staging/.codex/`, run all validators and runtime tests there, and leave only the final project-local installation/new-session discovery gate blocked by the sandbox path policy.
- Remaining risk: Codex cannot discover the staged skills from a fresh project session until a human or less restrictive session copies the verified staging tree into `.codex/`.

## 2026-07-12T12:44:46+09:00 — Tectonic sandbox panic

- Gate: anonymous ICML 2026 PDF build.
- Signature: Tectonic exits before TeX execution with a macOS `system-configuration`/`reqwest` panic containing `Attempted to create a NULL object`.
- Reproduction count: the normal invocation and an explicit working-directory invocation failed with the same signature.
- Repairs attempted: changed the invocation working-directory form and confirmed the failure occurs before document compilation.
- Reduction decision: preserve both raw Tectonic logs, attempt a local-cache/offline bundle path, then use an already installed TeX engine if available; keep PDF rendering, page-count, metadata, text, anonymity, and body-page checks unchanged.
- Remaining risk: if the fallback engine succeeds, the PDF can be format-verified but the required Tectonic-success gate remains failed and must be reported honestly.

### Resolution of the Tectonic failure

The reduced local-cache path succeeded with exit 0:
`TECTONIC_CACHE_DIR=../tmp/pdfs/tectonic-work-cache tectonic -C -b ../tmp/pdfs/tectonic-cache.zip technical-report.tex --keep-logs --keep-intermediates`.
The raw success log is `evidence/report/tectonic-offline-success.log`; subsequent PDF checks therefore use a genuine Tectonic build, while the two network-path panics remain preserved as environment evidence.

## 2026-07-12T13:33:00+09:00 — fresh-session discovery sandbox denial

- Gate: fresh Codex-session discovery of the staged official and wrapper Skills.
- Signature: both an isolated `codex exec` discovery attempt and its `codex debug prompt-input` fallback terminated before Skill discovery with the operating-system signature `Operation not permitted`.
- Reproduction count: two separate Codex discovery surfaces reproduced the same sandbox-denial class; the failing subcommands differed, but neither reached prompt evaluation.
- Repairs attempted: moved the discovery workspace to a writable isolated directory, then reduced from the app-server-backed execution path to the prompt-input debug path.
- Reduction decision: preserve the failed discovery evidence and use static staged Skill validation, upstream/wrapper SHA-256 manifests, and installer staging checks as the bounded verification path. Do not claim successful fresh-session discovery.
- Remaining risk: actual Codex discovery remains unverified until the staged package can be installed under project `.codex/` and a less restrictive Codex process can start.

## 2026-07-12T13:46:00+09:00 — append-only reader clarification

- The sentence near the top stating that no Ralph Loop failures were recorded
  captures the ledger's creation-time state. It is intentionally retained
because this ledger is append-only. The dated entries above are the current
failure record and supersede that creation-time statement.

## 2026-07-12T14:22:00+09:00 — post-clean font-parser false negative

- Gate: final post-clean PDF font and submission audit.
- Signature: a temporary Python wrapper around `pdffonts` twice reported
  `fonts_embedded_subset_unicode=false` even though the raw four font rows each
  contained the authoritative `yes yes yes` embedded/subset/Unicode flags.
- Reproduction count: two runs failed with the same wrapper-parser signature;
  the PDF bytes and raw `pdffonts` output were unchanged.
- Repairs attempted: first parsed whitespace-separated tokens, then attempted
  multi-space column splitting. Both approaches mis-modeled the three adjacent
  flag fields as one display column.
- Reduction decision: stop changing the general parser and verify the four
  raw font rows directly, requiring the exact `yes yes yes` flag group and no
  `Type 3` row. Retain `pdfinfo` as the independent page, metadata, and
  JavaScript authority.
- Remaining risk: none for this PDF snapshot; the reduced check is tied to the
  raw `pdffonts` output and is recorded with the final artifact hash.

## 2026-07-12T14:36:00+09:00 — project installation and discovery resolution

- Resolution: a write-capable local surface installed the staged 28-file
  package under project `.codex`; installer read-back reported 28/28 exact
  matches with no missing files or conflicts.
- Fresh-session evidence: both Skills appeared in a genuinely fresh Codex
  session, and typed spawns of `track2-review-worker`,
  `track2-review-verifier`, and `track2-submission-auditor` returned their
  expected completion tokens.
- Current risk: the earlier environment blocker is closed. Production claim,
  post, and the live OpenAgentReview contract remain deliberately untested
  until the authorized 16:35 KST window.
- Evidence: `evidence/external-final-verification.json`.
