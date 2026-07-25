#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lib.manifest import load_mods
from lib.paths import EDITIONS, ROOT, manifest_path
from lib.sourced_mods import validate_sourced_mods
from lib.validation import validate_manifest, validate_source_references

SOURCED_MODS_PATH = ROOT / "shared" / "sourced-mods.control.meta"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Ash Archive edition manifests and canonical source links."
    )
    parser.add_argument("--edition", choices=EDITIONS, help="Validate one edition only.")
    return parser.parse_args()


def validate_repository(editions: list[str], source_path: Path = SOURCED_MODS_PATH) -> list[str]:
    errors: list[str] = []
    manifest_paths = {edition: manifest_path(edition) for edition in EDITIONS}
    mods_by_edition: dict[str, list[dict]] = {}
    loaded_editions: set[str] = set()

    for edition, path in manifest_paths.items():
        try:
            mods_by_edition[edition] = load_mods(path)
            loaded_editions.add(edition)
        except ValueError as exc:
            mods_by_edition[edition] = []
            if edition in editions:
                errors.append(f"[ERROR] {exc}")

    for edition in editions:
        # Avoid repeating a load error already captured above.
        if edition in loaded_editions:
            errors.extend(
                validate_manifest(manifest_paths[edition], edition, mods=mods_by_edition[edition])
            )

    candidates, source_errors = validate_sourced_mods(source_path)
    errors.extend(source_errors)
    errors.extend(
        validate_source_references(
            mods_by_edition,
            manifest_paths,
            candidates,
            source_path,
            editions,
        )
    )
    return errors


def main() -> int:
    args = parse_args()
    editions = [args.edition] if args.edition else list(EDITIONS)
    errors = validate_repository(editions)

    if errors:
        for err in errors:
            print(err)
        return 1

    print(f"[OK] Manifest validation passed for: {', '.join(editions)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
