#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from lib.manifest import load_mods
from lib.markdown import render_mod_sections
from lib.paths import EDITIONS, ROOT

START = "<!-- GENERATED-CONTENT:START -->"
END = "<!-- GENERATED-CONTENT:END -->"


def update_modlist(path: Path, content: str) -> None:
    text = path.read_text(encoding="utf-8") if path.exists() else "# Modlist\n\n"
    if START in text and END in text:
        pre = text.split(START)[0]
        post = text.split(END)[1]
        new_text = f"{pre}{START}\n{content}{END}{post}"
    else:
        new_text = f"{text.rstrip()}\n\n{START}\n{content}{END}\n"
    path.write_text(new_text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate MODLIST markdown from manifests.")
    parser.add_argument("--edition", choices=EDITIONS)
    args = parser.parse_args()
    editions = [args.edition] if args.edition else list(EDITIONS)
    for edition in editions:
        mods = load_mods(ROOT / "editions" / edition / "manifests" / "mods.meta")
        body = render_mod_sections(mods)
        modlist_path = ROOT / "editions" / edition / "MODLIST.md"
        update_modlist(modlist_path, body)
        print(f"Updated {modlist_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
