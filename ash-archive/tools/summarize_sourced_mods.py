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
    parser = argparse.ArgumentParser(
        description="Summarize sourced-mod candidates by thematic bucket."
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=ROOT / "shared" / "sourced-mods.control.meta",
        help="Path to sourced-mods control file (default: shared/sourced-mods.control.meta)",
    )
    return parser.parse_args()


def generate_summary(candidates: list[dict]) -> str:
    """Build a bucketed Markdown table summary for sourced candidates."""
    lines = []
    grouped: dict[str, list[dict]] = defaultdict(list)
    for candidate in candidates:
        grouped[candidate["thematic_bucket"]].append(candidate)

    lines.append("Sourced mod candidates (intake desk)")
    lines.append(f"Total: {len(candidates)}")
    lines.append("")

    for bucket in sorted(grouped):
        lines.append(f"[{bucket}]")
        lines.append(
            "id | name | candidate_status | intended_editions | compatibility_status | risk_level | source_confidence"
        )
        lines.append(
            "-- | ---- | ---------------- | ----------------- | -------------------- | ---------- | -----------------"
        )
        for candidate in sorted(grouped[bucket], key=lambda item: item["id"]):
            row = [candidate["id"], candidate["name"]]
            for field in SUMMARY_FIELDS:
                value = candidate[field]
                if isinstance(value, list):
                    row.append(",".join(value))
                else:
                    row.append(value)
            lines.append(" | ".join(row))
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    """CLI entry point."""
    args = _parse_args()
    candidates, errors = validate_sourced_mods(args.file)

    if errors:
        for error in errors:
            print(error)
        return 1

    print(generate_summary(candidates))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
