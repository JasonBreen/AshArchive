#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from lib.manifest import load_mods
from lib.paths import EDITIONS, manifest_path


@dataclass
class DuplicateReport:
    duplicate_ids: list[str]
    duplicate_names_with_different_ids: list[str]


def find_duplicates(mods: list[dict]) -> DuplicateReport:
    id_counts = defaultdict(int)
    name_to_ids = defaultdict(set)
    for mod in mods:
        mod_id = mod.get("id")
        mod_name = mod.get("name")
        if isinstance(mod_id, str) and mod_id:
            id_counts[mod_id] += 1
        if isinstance(mod_name, str) and mod_name and isinstance(mod_id, str) and mod_id:
            name_to_ids[mod_name].add(mod_id)

    dup_ids = sorted(mod_id for mod_id, count in id_counts.items() if count > 1)
    dup_names = sorted(name for name, ids in name_to_ids.items() if len(ids) > 1)
    return DuplicateReport(duplicate_ids=dup_ids, duplicate_names_with_different_ids=dup_names)


def find_cross_edition_name_mismatches(mods_by_edition: dict[str, list[dict]]) -> list[tuple[str, str, str]]:
    name_to_edition_ids: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for edition, mods in mods_by_edition.items():
        for mod in mods:
            mod_id = mod.get("id")
            mod_name = mod.get("name")
            if isinstance(mod_name, str) and mod_name and isinstance(mod_id, str) and mod_id:
                name_to_edition_ids[mod_name][edition].add(mod_id)

    warnings: list[tuple[str, str, str]] = []
    for name, edition_ids in sorted(name_to_edition_ids.items()):
        if len(edition_ids) < 2:
            continue
        merged_ids = set().union(*edition_ids.values())
        if len(merged_ids) <= 1:
            continue
        detail = "; ".join(
            f"{edition}: {', '.join(sorted(ids))}" for edition, ids in sorted(edition_ids.items())
        )
        warnings.append(("all editions", name, detail))
    return warnings


def _load_mods_for_path(path: Path) -> list[dict]:
    try:
        return load_mods(path)
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return []


def main() -> int:
    has_errors = False
    mods_by_edition: dict[str, list[dict]] = {}

    for edition in EDITIONS:
        path = manifest_path(edition)
        mods = _load_mods_for_path(path)
        mods_by_edition[edition] = mods
        report = find_duplicates(mods)

        for mod_id in report.duplicate_ids:
            has_errors = True
            print(f"[ERROR] {path} :: {mod_id} :: duplicate id in manifest")
        for name in report.duplicate_names_with_different_ids:
            print(
                f"[WARN] {path} :: {name} :: duplicate name used by different ids in this manifest"
            )

    cross_warnings = find_cross_edition_name_mismatches(mods_by_edition)
    for scope, name, detail in cross_warnings:
        print(f"[WARN] {scope} :: {name} :: duplicate name across editions with different ids ({detail})")

    if has_errors:
        return 1

    if not cross_warnings and all(not find_duplicates(mods).duplicate_names_with_different_ids for mods in mods_by_edition.values()):
        print("[OK] No duplicate IDs or likely accidental duplicate names found.")
    else:
        print("[OK] Duplicate scan completed with warnings only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
