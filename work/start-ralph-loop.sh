#!/bin/zsh
set -euo pipefail

ROOT="/Users/redux80/Documents/_20260712_Ralphthon"
CONFIRMATION="${1:-}"

if [[ "$CONFIRMATION" != "START-RALPH" ]]; then
  print -u2 "User start signal required. Run only after the event operator says to start."
  exit 2
fi

cd "$ROOT"

if [[ ! -s RALPH_GOAL.md ]]; then
  print -u2 "RALPH_GOAL.md is missing."
  exit 3
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
  print -u2 "Working tree is not clean. Freeze and commit preflight artifacts first."
  exit 4
fi

if ! tmux has-session -t ralphthon-awake 2>/dev/null; then
  tmux new-session -d -s ralphthon-awake "/usr/bin/caffeinate -dimsu -t 11400"
fi

if ! tmux has-session -t ralphthon-deadline 2>/dev/null; then
  tmux new-session -d -s ralphthon-deadline "$ROOT/work/ralph-deadline-watchdog.sh"
fi

task_text="$(<RALPH_GOAL.md)"
exec omx ralph --tmux --xhigh -a never -s workspace-write -C "$ROOT" "$task_text"
