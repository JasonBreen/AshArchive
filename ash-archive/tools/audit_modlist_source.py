#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

from lib.paths import ROOT

REQUIRED_COLUMNS = [
    "#Mod_Priority",
    "#Mod_Status",
    "#Mod_Name",
    "#Note",
    "#Primary_Category",
    "#Nexus_ID",
    "#Mod_Nexus_URL",
    "#Mod_Version",
    "#Install_Date",
    "#Download_File_Name",
]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit a raw Mod Organizer-style modlist source artifact.")
    parser.add_argument(
        "--file",
        type=Path,
        default=ROOT / "shared" / "source-inputs" / "modlist.txt",
        help="Path to source modlist.txt (default: shared/source-inputs/modlist.txt)",
    )
    return parser.parse_args()


def _normalize(text: str | None) -> str:
    return (text or "").strip()


def _read_rows(path: Path) -> tuple[list[dict[str, str]] | None, list[str]]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                return None, ["[ERROR] malformed CSV: missing header row"]

            missing = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
            if missing:
                return None, [f"[ERROR] missing required columns: {', '.join(missing)}"]

            rows: list[dict[str, str]] = []
            for row in reader:
                rows.append({column: _normalize(row.get(column)) for column in REQUIRED_COLUMNS})
            return rows, []
    except FileNotFoundError:
        return None, [f"[ERROR] file not found: {path}"]
    except csv.Error as exc:
        return None, [f"[ERROR] malformed CSV: {exc}"]
    except OSError as exc:
        return None, [f"[ERROR] unable to read file: {exc}"]


def _to_int(value: str) -> int | None:
    if value == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def audit_rows(rows: list[dict[str, str]]) -> dict[str, object]:
    enabled = 0
    disabled = 0
    nexus_backed = 0
    unmanaged = 0
    dlc = 0
    local = 0
    nexus_negative_one = 0
    missing_category = 0
    duplicates: dict[int, list[str]] = defaultdict(list)
    disabled_rows: list[tuple[str, str]] = []

    for row in rows:
        mod_name = row["#Mod_Name"]
        status = row["#Mod_Status"]
        nexus_id = _to_int(row["#Nexus_ID"])

        if status == "+":
            enabled += 1
        elif status == "-":
            disabled += 1
            disabled_rows.append((row["#Mod_Priority"], mod_name))

        is_unmanaged = mod_name.startswith("Unmanaged:")
        is_dlc = mod_name.startswith("DLC:")

        if is_unmanaged:
            unmanaged += 1
        if is_dlc:
            dlc += 1

        if nexus_id is not None and nexus_id > 0:
            nexus_backed += 1
            duplicates[nexus_id].append(mod_name)
        elif nexus_id == -1:
            nexus_negative_one += 1

        if not is_unmanaged and not is_dlc and (nexus_id is None or nexus_id == 0):
            local += 1

        if row["#Primary_Category"] == "":
            missing_category += 1

    repeated_positive_nexus_ids = {
        nexus_id: names for nexus_id, names in sorted(duplicates.items()) if len(names) > 1
    }

    return {
        "total_rows": len(rows),
        "enabled_rows": enabled,
        "disabled_rows": disabled,
        "nexus_backed_rows": nexus_backed,
        "unmanaged_rows": unmanaged,
        "dlc_rows": dlc,
        "local_rows": local,
        "nexus_id_negative_one_rows": nexus_negative_one,
        "missing_category_rows": missing_category,
        "repeated_positive_nexus_ids": repeated_positive_nexus_ids,
        "disabled_rows_detail": sorted(disabled_rows),
    }


def print_report(path: Path, report: dict[str, object]) -> None:
    print(f"Source file: {path}")
    print(f"Total rows: {report['total_rows']}")
    print(f"Enabled rows: {report['enabled_rows']}")
    print(f"Disabled rows: {report['disabled_rows']}")
    print(f"Nexus-backed rows (Nexus_ID > 0): {report['nexus_backed_rows']}")
    print(f"Unmanaged rows (name starts with 'Unmanaged:'): {report['unmanaged_rows']}")
    print(f"DLC rows (name starts with 'DLC:'): {report['dlc_rows']}")
    print(f"Local rows (Nexus_ID is 0/empty and not unmanaged/DLC): {report['local_rows']}")
    print(f"Rows with Nexus_ID = -1: {report['nexus_id_negative_one_rows']}")
    print(f"Rows with missing #Primary_Category: {report['missing_category_rows']}")
    print()
    print("Repeated positive Nexus IDs:")
    repeated = report["repeated_positive_nexus_ids"]
    if repeated:
        for nexus_id, names in repeated.items():
            print(f"- {nexus_id}: {', '.join(names)}")
    else:
        print("- None")

    print()
    print("Disabled rows (priority, name):")
    details = report["disabled_rows_detail"]
    if details:
        for priority, name in details:
            print(f"- {priority} | {name}")
    else:
        print("- None")


def main() -> int:
    args = _parse_args()
    rows, errors = _read_rows(args.file)
    if errors:
        for error in errors:
            print(error)
        return 1

    assert rows is not None
    report = audit_rows(rows)
    print_report(args.file, report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
