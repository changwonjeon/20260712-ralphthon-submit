"""Command-line entry point for the bounded Track 2 mock runtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .runtime import (
    ControlledProcessInterruption,
    LiveAdapterUnavailable,
    Mode,
    load_papers,
    run_batch,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=[mode.value for mode in Mode], default=Mode.DRY_RUN.value)
    parser.add_argument("--papers", required=True, help="JSON corpus or papers array")
    parser.add_argument("--output-dir", required=True, help="run evidence directory")
    parser.add_argument("--workers", type=int, default=3, help="bounded worker count (1..3)")
    parser.add_argument("--failure-plan", help="optional deterministic fault-injection JSON")
    parser.add_argument("--root-dir", default=".", help="base for relative paper/evidence paths")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failure_plan = {}
    if args.failure_plan:
        payload = json.loads(Path(args.failure_plan).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("failure plan must be a JSON object")
        failure_plan = payload
    try:
        summary = run_batch(
            load_papers(args.papers),
            args.output_dir,
            mode=args.mode,
            workers=args.workers,
            failure_plan=failure_plan,
            root_dir=args.root_dir,
        )
    except ControlledProcessInterruption as exc:
        print(
            json.dumps(
                {
                    "success": False,
                    "interrupted": True,
                    "mode": Mode.DRY_RUN.value,
                    "posted_verified": exc.posted_verified,
                    "error": str(exc),
                },
                sort_keys=True,
            )
        )
        return exc.exit_code
    except LiveAdapterUnavailable as exc:
        print(json.dumps({"success": False, "error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(summary.to_dict(), sort_keys=True))
    return 0 if summary.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
