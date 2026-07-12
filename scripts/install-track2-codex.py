#!/usr/bin/env python3
"""Check or safely install the staged official/wrapper skills and native agents."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SKILL_NAMES = ("auto-research", "ralphthon-track2-review-agent")
AGENT_NAMES = (
    "track2-review-worker.toml",
    "track2-review-verifier.toml",
    "track2-submission-auditor.toml",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repository_root() -> Path:
    root = Path(__file__).resolve().parent.parent
    if not (root / "staging" / ".codex").is_dir():
        raise RuntimeError(f"staged .codex tree not found under {root}")
    return root


def source_files(root: Path) -> list[tuple[Path, Path]]:
    staged = root / "staging" / ".codex"
    pairs: list[tuple[Path, Path]] = []
    for skill_name in SKILL_NAMES:
        skill_source = staged / "skills" / skill_name
        if not (skill_source / "SKILL.md").is_file():
            raise RuntimeError(f"staged Skill is incomplete: {skill_source}")
        pairs.extend(
            (source, root / ".codex" / "skills" / skill_name / source.relative_to(skill_source))
            for source in sorted(skill_source.rglob("*"))
            if source.is_file()
        )
    for name in AGENT_NAMES:
        source = staged / "agents" / name
        if not source.is_file():
            raise RuntimeError(f"staged native agent is missing: {source}")
        pairs.append((source, root / ".codex" / "agents" / name))
    return pairs


def manifest(root: Path, pairs: Iterable[tuple[Path, Path]]) -> dict[str, Any]:
    entries = []
    for source, destination in pairs:
        entries.append(
            {
                "source": str(source.relative_to(root)),
                "destination": str(destination.relative_to(root)),
                "sha256": sha256_file(source),
                "size_bytes": source.stat().st_size,
            }
        )
    return {
        "manifest_version": "1.0",
        "skills": list(SKILL_NAMES),
        "files": entries,
    }


def destination_status(source: Path, destination: Path) -> str:
    if not destination.exists():
        return "missing"
    if not destination.is_file():
        return "conflict-nonfile"
    return "match" if sha256_file(source) == sha256_file(destination) else "conflict-content"


def atomic_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        shutil.copyfile(source, temporary)
        shutil.copymode(source, temporary)
        with temporary.open("rb") as handle:
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def install(
    pairs: list[tuple[Path, Path]], *, replace: bool
) -> tuple[list[dict[str, str]], Path | None]:
    statuses = [
        {"path": str(destination), "status": destination_status(source, destination)}
        for source, destination in pairs
    ]
    conflicts = [entry for entry in statuses if entry["status"].startswith("conflict")]
    if conflicts and not replace:
        raise RuntimeError(
            "destination conflicts found; inspect with --check or explicitly use --replace"
        )

    backup_root: Path | None = None
    if conflicts:
        first_destination = pairs[0][1]
        repository = first_destination.parents[3]
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup_root = repository / "staging" / "install-backups" / stamp
        for source, destination in pairs:
            if destination.is_file() and sha256_file(source) != sha256_file(destination):
                backup = backup_root / destination.relative_to(repository)
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(destination, backup)

    installed: list[dict[str, str]] = []
    for source, destination in pairs:
        status = destination_status(source, destination)
        if status == "match":
            installed.append({"path": str(destination), "action": "unchanged"})
            continue
        if status == "conflict-nonfile":
            raise RuntimeError(f"refusing to replace non-file destination: {destination}")
        atomic_copy(source, destination)
        if sha256_file(source) != sha256_file(destination):
            raise OSError(f"install read-back mismatch: {destination}")
        installed.append({"path": str(destination), "action": "installed"})
    return installed, backup_root


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check-staging", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--install", action="store_true")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Back up and replace conflicting files; valid only with --install.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.replace and not args.install:
        raise SystemExit("--replace requires --install")

    root = repository_root()
    pairs = source_files(root)
    result: dict[str, Any] = {"manifest": manifest(root, pairs)}
    if args.check_staging:
        result["status"] = "staging-valid"
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0

    if args.check:
        files = [
            {
                "destination": str(destination.relative_to(root)),
                "status": destination_status(source, destination),
            }
            for source, destination in pairs
        ]
        result.update({"status": "installed" if all(f["status"] == "match" for f in files) else "not-installed", "files": files})
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["status"] == "installed" else 1

    installed, backup_root = install(pairs, replace=args.replace)
    result.update(
        {
            "status": "installed",
            "files": installed,
            "backup": str(backup_root.relative_to(root)) if backup_root else None,
        }
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
