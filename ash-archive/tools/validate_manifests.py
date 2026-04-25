#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from lib.paths import EDITIONS, manifest_path
from lib.validation import validate_manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Ash Archive edition manifests.")
    parser.add_argument("--edition", choices=EDITIONS, help="Validate one edition only.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    editions = [args.edition] if args.edition else list(EDITIONS)
    errors: list[str] = []
    for edition in editions:
        path = manifest_path(edition)
        errors.extend(validate_manifest(path, edition))
    if errors:
        print("Manifest validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print(f"Manifest validation passed for: {', '.join(editions)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
