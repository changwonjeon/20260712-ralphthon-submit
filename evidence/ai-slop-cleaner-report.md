# Changed-Files-Only Cleanup Report

## Outcome

The reviewer-approved `$ai-slop-cleaner` pass completed without changing runtime
behavior, APIs, tests, dependencies, frozen fixtures, official upstream content,
raw runtime evidence, per-paper artifacts, or generated submission files. The
full regression remains green at 49/49 tests. The bundled CLI and all documents
now state its actual fail-closed boundary: it supports BUILD and mock-only
DRY-RUN and rejects LIVE unconditionally.

The wrapper and native-agent checksum manifest is valid. Its new SHA-256 is:

```text
daa71e174640dbc135f9a735bb4d42db99dba4e7abd7802b7aeb7866ac75c7f3  staging/ralphthon-track2-review-agent.sha256
```

## Writer and reviewer separation

The writer pass inspected the changed human-authored surface and produced a
plan without editing files. The reviewer then approved a closed edit list and
explicitly rejected behavior changes. This execution pass applied only that
list. No opportunistic refactor, new abstraction, dependency, or test rewrite
was added.

The allowlist is `.omx/ralph/changed-files.txt`. It excludes the byte-identical
staged official `auto-research` subtree, frozen fixtures, authoritative/raw
evidence and ledgers, manifests, outbox, clipboard artifacts, generated
PDF/PNG/TeX auxiliary files, and the user-owned
`work/run-ralph-direct.sh` compatibility fix. This report is the explicitly
requested human-authored validation record and is not a raw run artifact.

## Exact cleanup

- Deleted the unused `WORKER_PROMPT` import from `runtime.py` and unused
  `read_json` import from `ledger.py`.
- Replaced the unreachable `else b""` branch in `manifest.py` with an explicit
  type-narrowing assertion followed by the already-proven `paper_bytes` value.
- Removed stale `F401` suppressions from the three wrapper scripts while
  preserving the required `E402` suppressions.
- Corrected the README repository map so quality evaluation is located under
  `tests/quality_eval.py`, not the source package.
- Corrected the report to describe append-only ledger writes with atomic
  snapshot replacement and to state that validator-reject state and validation
  errors are recorded for malformed output; it no longer claims preservation
  of the raw malformed value.
- Corrected LIVE wording in the wrapper Skill, README, agent definition, and
  handoff. The Skill-guided read-only discovery/manual lane remains the safe
  16:35 entry; no working programmatic production adapter is implied.
- Regenerated the wrapper checksum manifest and updated every non-raw citation
  of its manifest SHA-256.

## Fallback inventory and reviewer decisions

| Surface | Classification | Decision |
| --- | --- | --- |
| `io_utils.atomic_write_bytes` directory-open `OSError` fallback | Compatibility fallback with a documented residual durability risk | Retained unchanged because the reviewer rejected behavior changes. It runs only after file fsync and `os.replace`, allowing filesystems that cannot open directories to keep the replaced file. Because it catches every `OSError`, directory durability is not proven on that branch; no stronger claim is made. |
| `_failure_ids` unsupported-value-to-empty-set behavior | Permissive input fallback | Retained unchanged; strict validation would alter the API. Required evidence independently asserts every injected recovery counter. |
| Worker-slot `BaseException` handler | Grounded cleanup guard | Retained; it restores the slot and immediately re-raises, so it masks no failure. |
| Claim, post, and worker `TimeoutError` handlers | Grounded recovery contract | Retained; they implement bounded retry or status-first reconciliation. |
| Mock locator and repair-worker defaults | Grounded synthetic-fixture behavior | Retained; mock-only limitations remain explicit. |
| Staged install, manual platform, and offline Tectonic reductions | Evidence-backed operational fallback | Retained; each blocker and claim boundary remains explicit. |

## Validation evidence

Targeted regressions passed:

```text
test_manifest_ledger.py: 7/7
test_identity_contract.py: 3/3
test_cli_interfaces.py: 5/5
```

Full regression:

```text
python3 -m unittest discover -s tests -p 'test_*.py' -v
Ran 49 tests in 1.284s
OK
```

Package and immutable-surface checks:

```text
wrapper checksum manifest: 17/17 OK
official upstream checksum manifest: 11/11 OK
official upstream recursive diff: empty
frozen fixture checksum manifest: 16/16 OK
staged installer check: 28/28 files, status=staging-valid
quick_validate.py: Skill is valid!
Python static compilation: PASS
git diff --check: PASS
repository __pycache__ / .pyc scan: 0 files
```

The system Python lacked `yaml`, and a first `uv run` attempt could not write
its default home cache. Validation was recovered without repository mutation by
loading the already cached PyYAML package read-only; `quick_validate.py` then
returned `Skill is valid!`.

Before and after tests, excluded content digests were byte-identical:

```text
raw evidence tree: f1fa80beff1a2af99571928cda81cffcae46d0873d02f14631f34206fb610b4a
frozen fixtures: 4e45e58096cc194d0a405fb081eafd0ec1469601f5849ee5e6132ba1647d6c23
root manifests: 7ae713c8629c585b16108e5665f91e9f0e9e7dd4fbc1477a21826f5324bb79c7
root outbox: 3be62753c177b0fdcdab50df04d05ed6764fc6e180917f038d20a7217eec7225
root clipboard: 8d699345b4f24675cd63d52e6e3453b7a394d8505bb5da5d345ab596887a796a
official staged upstream: b46fb7e1798948f620cb59018145b17d30a929eb04d93e97d7dcab9d14ac511b
```

The root ledger, state snapshot, summary, PDF, TeX auxiliary file, and TeX log
also retained their exact pre-pass hashes.

## Required Root refresh

The Technical Report source changed but generated files were intentionally not
rebuilt in this pass:

```text
41b8e9318e4eb1fc08819bd0636d1333ec362786b0f71f80f1e0f45d7f2eec80  submission/technical-report.tex
07e3adef234cc6b1806c15dd855025776533a707de609df46de2c25148c770ad  submission/technical-report.pdf (pre-cleanup build)
```

Root must rebuild the PDF with the preserved offline Tectonic command, rerun
page/body-marker/anonymity/metadata/font/text/visual checks, refresh the TeX and
PDF hashes in `HANDOFF.md` and report validation evidence, and only then update
`CHECKPOINT.json`.

## Root post-clean read-back

Root directly reviewed the cleanup allowlist and the resulting implementation,
Skill, runbook, and report changes. The review confirmed that the pass removed
only the two unused imports and the unreachable manifest branch, retained both
reviewer-rejected compatibility fallbacks, preserved the BUILD/DRY-RUN behavior
and fail-closed LIVE boundary, and did not touch the official upstream subtree,
frozen fixtures, raw evidence, per-paper artifacts, or the user-owned launcher
compatibility change.

Fresh root verification completed at `2026-07-12T14:23:34+09:00`:

```text
tests: 49/49 PASS (1.654s)
compileall / git diff check / repository pycache scan: PASS
wrapper / upstream / fixtures / staged installer: 17/17, 11/11, 16/16, 28/28 PASS
Skill quick_validate / native TOML / Skill agent YAML: 2/2, 3/3, 2/2 PASS
root audit / outbox schema: 10/10, duplicate attempts and keys 0
PDF: 3 pages, BODY-END-MARKER page 3, four embedded/subset/Unicode fonts, no Type 3
anonymity / placeholder / exact Title and Abstract / raw metrics: PASS
```

The final post-clean report source and rebuilt PDF are:

```text
d8b17f65cb9f965214127869badf8ce64d4f4749d46607dedda69b46d503c2a0  submission/technical-report.tex
b1a8c476f9bf0718d4a64c7192467fad588fe7a35f25380a9d363696548db18f  submission/technical-report.pdf
```

The pre-clean hashes in the preceding “Required Root refresh” section are
retained as historical cleanup handoff evidence and are superseded by this
root read-back. The independent architect audit is likewise preserved as its
14:00 KST pre-clean snapshot; the final completion audit records the newer
post-clean verification separately.
