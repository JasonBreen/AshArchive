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
    """Find duplicate IDs and same-name/different-ID collisions in one manifest."""
    seen_ids: set[str] = set()
    dup_ids_set: set[str] = set()
    name_to_ids: dict[str, set[str]] = defaultdict(set)
    dup_names_set: set[str] = set()

    for mod in mods:
        mod_id = mod.get("id")
        mod_name = mod.get("name")

        has_id = isinstance(mod_id, str) and mod_id
        if has_id:
            if mod_id in seen_ids:
                dup_ids_set.add(mod_id)
            else:
                seen_ids.add(mod_id)

        if isinstance(mod_name, str) and mod_name and has_id:
            ids = name_to_ids[mod_name]
            ids.add(mod_id)
            if len(ids) > 1:
                dup_names_set.add(mod_name)

    dup_ids = sorted(dup_ids_set)
    dup_names = sorted(dup_names_set)
    return DuplicateReport(duplicate_ids=dup_ids, duplicate_names_with_different_ids=dup_names)


def find_cross_edition_name_mismatches(
    mods_by_edition: dict[str, list[dict]],
) -> list[tuple[str, str, str]]:
    """Find same-name mods that map to different IDs across editions."""
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


def _load_mods_for_path(path: Path) -> tuple[list[dict], bool]:
    try:
        return load_mods(path), False
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return [], True


def main() -> int:
    """CLI entry point."""
    has_errors = False
    has_duplicate_names = False
    mods_by_edition: dict[str, list[dict]] = {}

    for edition in EDITIONS:
        path = manifest_path(edition)
        mods, load_failed = _load_mods_for_path(path)
        has_errors = has_errors or load_failed
        mods_by_edition[edition] = mods
        report = find_duplicates(mods)

        for mod_id in report.duplicate_ids:
            has_errors = True
            print(f"[ERROR] {path} :: {mod_id} :: duplicate id in manifest")
        if report.duplicate_names_with_different_ids:
            has_duplicate_names = True
        for name in report.duplicate_names_with_different_ids:
            print(
                f"[WARN] {path} :: {name} :: duplicate name used by different ids in this manifest"
            )

    cross_warnings = find_cross_edition_name_mismatches(mods_by_edition)
    for scope, name, detail in cross_warnings:
        print(
            f"[WARN] {scope} :: {name} :: duplicate name across editions with different ids ({detail})"
        )

    if has_errors:
        return 1

    if not cross_warnings and not has_duplicate_names:
        print("[OK] No duplicate IDs or likely accidental duplicate names found.")
    else:
        print("[OK] Duplicate scan completed with warnings only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
