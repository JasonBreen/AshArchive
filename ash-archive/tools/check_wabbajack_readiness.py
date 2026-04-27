#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from lib.manifest import load_mods
from lib.paths import EDITIONS, manifest_path
from lib.wabbajack import check_edition_wabbajack_readiness


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check Wabbajack readiness of Ash Archive edition manifests."
    )
    parser.add_argument("--edition", choices=EDITIONS, help="Check one edition only.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    editions = [args.edition] if args.edition else list(EDITIONS)
    all_messages: list[str] = []

    for edition in editions:
        path = manifest_path(edition)
        try:
            mods = load_mods(path)
        except ValueError as exc:
            print(f"[ERROR] {exc}")
            return 1
        all_messages.extend(check_edition_wabbajack_readiness(mods, path))

    for msg in all_messages:
        print(msg)

    errors = [m for m in all_messages if m.startswith("[ERROR]")]
    warnings = [m for m in all_messages if m.startswith("[WARN]")]

    if errors:
        return 1

    if not warnings:
        print(f"[OK] Wabbajack readiness check passed for: {', '.join(editions)}")
    else:
        print(f"[OK] Wabbajack readiness check passed with warnings for: {', '.join(editions)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
