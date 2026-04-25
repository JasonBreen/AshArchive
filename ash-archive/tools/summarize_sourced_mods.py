#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from lib.paths import ROOT
from lib.sourced_mods import validate_sourced_mods


SUMMARY_FIELDS = [
    "candidate_status",
    "intended_editions",
    "compatibility_status",
    "risk_level",
    "source_confidence",
]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize sourced-mod candidates by thematic bucket.")
    parser.add_argument(
        "--file",
        type=Path,
        default=ROOT / "shared" / "sourced-mods.yaml",
        help="Path to sourced-mods yaml file (default: shared/sourced-mods.yaml)",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    candidates, errors = validate_sourced_mods(args.file)

    if errors:
        for error in errors:
            print(error)
        return 1

    grouped: dict[str, list[dict]] = defaultdict(list)
    for candidate in candidates:
        grouped[candidate["thematic_bucket"]].append(candidate)

    print("Sourced mod candidates (intake desk)")
    print(f"Total: {len(candidates)}")
    print()

    for bucket in sorted(grouped):
        print(f"[{bucket}]")
        print("id | name | candidate_status | intended_editions | compatibility_status | risk_level | source_confidence")
        print("-- | ---- | ---------------- | ----------------- | -------------------- | ---------- | -----------------")
        for candidate in sorted(grouped[bucket], key=lambda item: item["id"]):
            row = [candidate["id"], candidate["name"]]
            for field in SUMMARY_FIELDS:
                value = candidate[field]
                if isinstance(value, list):
                    row.append(",".join(value))
                else:
                    row.append(value)
            print(" | ".join(row))
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
