# Frozen Upstream Auto Research Skill

- Repository commit: `a9f4f2583648ef4ca54f980f951ae393d153473f`
- Git tree: `13768e05524bd5a9705c413b36660d618aa166c5`
- Source subtree: `skills/auto-research/`
- Staged destination: `staging/.codex/skills/auto-research/`
- File count: 11

The staged destination is a byte-identical copy of the pinned source subtree.
Install it as `.codex/skills/auto-research/` in an execution context that has
write authority for the project-local `.codex` directory.

Verification:

```sh
diff -qr \
  tmp/ralphthon-icml-official/skills/auto-research \
  staging/.codex/skills/auto-research

(cd staging/.codex/skills/auto-research && \
  shasum -a 256 -c ../../../auto-research.sha256)
```
