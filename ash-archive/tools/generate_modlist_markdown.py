#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
from pathlib import Path

from lib.manifest import load_mods
from lib.markdown import render_mod_sections
from lib.paths import EDITIONS, ROOT

START = "<!-- GENERATED-CONTENT:START -->"
END = "<!-- GENERATED-CONTENT:END -->"


def render_modlist_document(text: str, content: str) -> str:
    """Insert or replace the generated MODLIST section bounded by marker comments."""
    start_count = text.count(START)
    end_count = text.count(END)
    if start_count != end_count or start_count > 1:
        raise ValueError("MODLIST.md must contain exactly one balanced generated marker pair")

    if start_count == 1:
        start_index = text.index(START)
        end_index = text.index(END)
        if end_index < start_index:
            raise ValueError("MODLIST.md generated markers are out of order")
        pre = text[:start_index]
        post = text[end_index + len(END) :]
        return f"{pre}{START}\n{content}{END}{post}"

    return f"{text.rstrip()}\n\n{START}\n{content}{END}\n"


def expected_modlist(path: Path, content: str) -> tuple[str, str]:
    """Return `(current_text, expected_text)` for a MODLIST file."""
    current = path.read_text(encoding="utf-8") if path.exists() else "# Modlist\n\n"
    return current, render_modlist_document(current, content)


def report_diff(path: Path, current: str, expected: str) -> None:
    """Print a unified diff between committed and generated MODLIST content."""
    diff = difflib.unified_diff(
        current.splitlines(keepends=True),
        expected.splitlines(keepends=True),
        fromfile=str(path),
        tofile=f"{path} (generated)",
    )
    print("".join(diff), end="")


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate MODLIST markdown from manifests.")
    parser.add_argument("--edition", choices=EDITIONS)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail and print a diff when committed MODLIST files are stale; do not write files.",
    )
    args = parser.parse_args()
    editions = [args.edition] if args.edition else list(EDITIONS)
    stale = False
    for edition in editions:
        mods = load_mods(ROOT / "editions" / edition / "manifests" / "mods.control.meta")
        body = render_mod_sections(mods)
        modlist_path = ROOT / "editions" / edition / "MODLIST.md"
        current, expected = expected_modlist(modlist_path, body)
        if current == expected:
            print(f"[OK] Current: {modlist_path}")
            continue
        if args.check:
            stale = True
            print(f"[ERROR] Stale generated file: {modlist_path}")
            report_diff(modlist_path, current, expected)
        else:
            modlist_path.write_text(expected, encoding="utf-8")
            print(f"Updated {modlist_path}")
    return int(stale)


if __name__ == "__main__":
    raise SystemExit(main())
