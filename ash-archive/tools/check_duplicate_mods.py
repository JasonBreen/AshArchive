#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict

from lib.manifest import load_mods
from lib.paths import EDITIONS, manifest_path


def find_duplicates(mods: list[dict]) -> tuple[list[str], list[str]]:
    id_counts = defaultdict(int)
    name_to_ids = defaultdict(set)
    for mod in mods:
        id_counts[mod.get("id", "")] += 1
        name_to_ids[mod.get("name", "")].add(mod.get("id", ""))
    dup_ids = [mod_id for mod_id, c in id_counts.items() if mod_id and c > 1]
    dup_names = [name for name, ids in name_to_ids.items() if name and len(ids) > 1]
    return dup_ids, dup_names


def main() -> int:
    warnings = False
    for edition in EDITIONS:
        path = manifest_path(edition)
        mods = load_mods(path)
        dup_ids, dup_names = find_duplicates(mods)
        if dup_ids or dup_names:
            warnings = True
        if dup_ids:
            print(f"[{edition}] duplicate ids: {', '.join(sorted(dup_ids))}")
        if dup_names:
            print(f"[{edition}] duplicate names across ids: {', '.join(sorted(dup_names))}")
    if not warnings:
        print("No likely accidental duplicates found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
