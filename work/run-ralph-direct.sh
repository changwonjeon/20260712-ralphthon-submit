#!/bin/zsh
set -euo pipefail

ROOT="/Users/redux80/Documents/_20260712_Ralphthon"
cd "$ROOT"

task_text="$(<RALPH_GOAL.md)"
exec omx ralph --direct --xhigh -a never -s workspace-write -C "$ROOT" "$task_text"

