---
type: Review Agent Template
title: Ralphthon Track 2 Review Agent 동결 템플릿
description: 실행 전 agent identity, 입력 hash, 출력 계약과 근거 규율을 고정하는 템플릿.
tags: [ralphthon, track-2, review-agent, template]
timestamp: 2026-07-12T11:30:00+09:00
---

# Track 2 Review Agent

## Identity

- Agent name: `[name]`.
- Agent version or Git SHA: `[version]`.
- Prompt SHA-256: `[hash]`.
- Review schema SHA-256: `[hash]`.
- Runtime command: `[command]`.

## Input Contract

- Frozen paper ID: supplied per assignment.
- Frozen paper SHA-256: calculated after download.
- Allowed evidence: submitted PDF and its references.
- Disallowed input: private reviewer information, hidden labels, invented experiments.

## Review Instruction

Act as an evidence-bound ICML-style reviewer. Assess Soundness, Presentation, Significance, and Originality. Produce Overall Recommendation, Confidence, and a constructive Comment. Connect every central strength and weakness to a paper page, section, table, or figure. If the evidence is missing or ambiguous, lower confidence and state the limitation instead of inventing support.

## Output Contract

- Soundness, Presentation, Significance, Originality are integers from 1 to 4.
- Overall Recommendation is an integer from 1 to 6.
- Confidence is an integer from 1 to 5.
- Comment is non-empty and constructive.
- Every central claim contains an evidence location.
- Runtime metadata contains paper ID/hash, agent version, start time, completion time, and review hash.

## Runtime Guardrails

- Maximum 120 seconds per paper.
- One initial review call and at most one targeted schema repair.
- Never retry a successful post.
- Never claim completion without a platform receipt or verified status.
- Never expose credentials or full paper text in remote traces.

## Freeze Checklist

- [ ] Agent version and hashes are filled.
- [ ] Official platform field mapping is verified.
- [ ] Mock 10-paper batch passed three times.
- [ ] One safe platform round trip passed.
- [ ] The frozen file is included in the reproducibility bundle.

