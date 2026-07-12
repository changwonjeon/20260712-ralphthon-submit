---
type: Discovery Evidence
title: Isolated Codex Skill Discovery Attempt
description: Read-only fresh-session discovery attempt for the staged official and wrapper Skills.
tags: [ralphthon, track-2, codex, discovery]
timestamp: 2026-07-12T13:15:34+09:00
---

# Isolated Codex Skill Discovery Attempt

## Isolation

Created `/tmp/ralphthon-track2-discovery.89cvDt`, copied only `staging/.codex/` into it, and initialized an empty Git repository. The isolated `.codex` bundle contained 28 files. The project `.codex` directory was not modified.

## Ephemeral read-only session attempt

Command shape:

```text
codex exec --ephemeral --sandbox read-only --skip-git-repo-check --ignore-user-config --color never --json -C /tmp/ralphthon-track2-discovery.89cvDt <read-only discovery prompt>
```

Exit code: `1`.

Output:

```text
WARNING: proceeding, even though we could not create PATH aliases: Operation not permitted (os error 1)
Reading additional input from stdin...
Error: failed to initialize in-process app-server client: Operation not permitted (os error 1)
```

## Read-only prompt-input fallback

Command shape:

```text
codex debug prompt-input 'Discovery only: $auto-research $ralphthon-track2-review-agent'
```

Exit code: `1`.

Output:

```text
WARNING: proceeding, even though we could not create PATH aliases: Operation not permitted (os error 1)
Error: Operation not permitted (os error 1)
```

## Result

Fresh-session discovery is **blocked**, not passed. The child sandbox denies the Codex app-server and debug discovery surfaces before a session context is rendered. No production or project state was changed. Static staged validation passed for both Skill directories, the wrapper manifest is 17/17, and the frozen official upstream subtree is 11/11, but those checks are not a substitute for fresh-session discovery.

The actual project installation is also not proven: `scripts/install-track2-codex.py --check` reports all 28 staged files missing from project `.codex`, with zero content conflicts. Installation must occur through a write-capable local surface before repeating fresh-session discovery.

## Resolution after the Ralph snapshot

This document preserves the 13:15 KST read-only sandbox attempt. At 14:36 KST,
the verified 28-file package was installed through a write-capable local
surface. Installer read-back reported 28/28 exact matches with no missing or
conflicting files. A genuinely fresh Codex session then exposed both Skills
and successfully spawned all three project-local native roles. The current
verdict is therefore **PASS** for project installation and fresh-session
discovery. The authoritative follow-up record is
`evidence/external-final-verification.json`.
