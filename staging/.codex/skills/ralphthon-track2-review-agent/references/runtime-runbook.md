# Runtime Runbook

## Build and dry-run

From the repository root:

```bash
python3 .codex/skills/ralphthon-track2-review-agent/scripts/run_batch.py \
  --mode BUILD --papers fixtures/throughput/papers.json --output-dir evidence/build

python3 .codex/skills/ralphthon-track2-review-agent/scripts/run_batch.py \
  --mode DRY-RUN --papers fixtures/throughput/papers.json \
  --output-dir evidence/dry-run --workers 3
```

Expected local outputs are `manifests/`, `outbox/`, `clipboard/`, `ledger.jsonl`, its atomic state snapshot, and `summary.json`. `BUILD` and `DRY-RUN` cannot claim or post to production.

Failure plans are JSON objects keyed by fault type. Each of `malformed_json`, `worker_timeout`, `claim_timeout`, and `post_timeout` maps to a list of paper IDs that receive that one-shot fault. The compatibility key `process_restart_after` reopens the ledger in the same process; it is not evidence of a process restart. Claim and post timeout injections commit remote mock state before raising, so status-first reconciliation can be verified.

```json
{
  "malformed_json": ["paper-001"],
  "worker_timeout": ["paper-002"],
  "claim_timeout": ["paper-003"],
  "post_timeout": ["paper-004"],
  "process_restart_after": 5
}
```

For an actual two-process resume test, set `controlled_process_exit_after` to a positive integer in `DRY-RUN`. The first process durably exits with status 75 after that many `posted_verified` papers. Start a second process with the same output directory and inputs but without the controlled-exit plan. Existing `posted_verified` papers are skipped, the ledger is appended without changing its prefix, and completed manifest/outbox bytes remain unchanged. This hook is fault-injection-only and cannot run in `BUILD` or `LIVE`.

Resume with the same output directory and frozen inputs. Existing `posted_verified` papers are skipped. A manifest identity mismatch is a hard failure, not an overwrite. Paper IDs are used unchanged only when they are path-safe ASCII identifiers; separators, traversal, whitespace, and other unsafe characters are rejected before output paths are created.

## Risk-gated review calibration

After deterministic validation, Root scores review risk using the Skill rubric. The normal fast path goes directly to outbox/post. Only a score of at least 3 may enter the read-only verifier lane, capped at the smaller of three papers or the ceiling of 30% of assignments. Run at most one verifier for 20 seconds, with at most three findings, before T+15 and only while validated backlog is at most two. Never reduce the three active drafting slots while papers remain pending; reuse an idle Worker slot near the end of the queue. Fast/emergency mode, slow posting pace, prior repair, or an exhausted verifier budget bypasses calibration.

Verifier PASS releases the unchanged draft. REPAIR names at most three exact fields and evidence locations. Root grants at most one targeted repair per paper across both schema and calibration paths, reruns the deterministic validator, and never calls the verifier twice. Verifier output is advisory and confers no ledger or platform authority.

## Live discovery and manual fallback

At the authorized live start, spend at most 45 seconds observing assigned count, claim semantics, PDF access, form fields, and the success marker. Do not encode a selector or endpoint until observed. Platform priority is `reconcile/post > download > claim > browse`. Queue high-water is 3; increase only after confirming multiple claims are allowed.

If the adapter cannot be verified, do not force `LIVE`. Continue Worker and validator execution in the local/manual lane. Use each `outbox/<paper_id>.json` and `clipboard/<paper_id>.txt` to claim/download/post through the observed UI, then record the verified status separately.

Start the final status audit at T+23:30 and stop new side effects at T+24:30. Success requires `posted_verified == assigned_count`.
