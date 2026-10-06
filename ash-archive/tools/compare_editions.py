#!/usr/bin/env python3

from lib.manifest import load_mods
from lib.paths import manifest_path
from lib.validation import validate_manifest


def find_cross_status_mismatches(openmw: dict[str, dict], mwse: dict[str, dict]) -> list[str]:
    """Return shared manifest IDs with differing `cross_edition_status` values."""
    shared = set(openmw) & set(mwse)
    return sorted(
        mod_id
        for mod_id in shared
        if openmw[mod_id].get("cross_edition_status") != mwse[mod_id].get("cross_edition_status")
    )


def find_cross_name_mismatches(openmw: dict[str, dict], mwse: dict[str, dict]) -> list[str]:
    """Return shared manifest IDs whose `name` differs across editions."""
    shared = set(openmw) & set(mwse)
    return sorted(
        mod_id for mod_id in shared if openmw[mod_id].get("name") != mwse[mod_id].get("name")
    )


def main() -> int:
    """CLI entry point."""
    errs = []
    openmw_mods: list[dict] | None = None
    try:
        openmw_mods = load_mods(manifest_path("openmw"))
    except ValueError as exc:
        errs.append(f"[ERROR] {exc}")

    mwse_mods: list[dict] | None = None
    try:
        mwse_mods = load_mods(manifest_path("mwse"))
    except ValueError as exc:
        errs.append(f"[ERROR] {exc}")

    if openmw_mods is not None:
        errs.extend(validate_manifest(manifest_path("openmw"), "openmw", mods=openmw_mods))
    if mwse_mods is not None:
        errs.extend(validate_manifest(manifest_path("mwse"), "mwse", mods=mwse_mods))

    if errs:
        print("Cannot compare editions due to manifest errors:")
        for err in errs:
            print(f"- {err}")
        return 1

    openmw = {m["id"]: m for m in openmw_mods if isinstance(m, dict) and "id" in m}
    mwse = {m["id"]: m for m in mwse_mods if isinstance(m, dict) and "id" in m}

    open_ids, mwse_ids = set(openmw), set(mwse)
    shared = sorted(open_ids & mwse_ids)
    open_only = sorted(open_ids - mwse_ids)
    mwse_only = sorted(mwse_ids - open_ids)
    equiv = sorted(
        mod_id
        for mod_id, mod in {**openmw, **mwse}.items()
        if mod.get("cross_edition_status") == "equivalent-needed"
    )
    diff_impl = sorted(
        mod_id
        for mod_id, mod in {**openmw, **mwse}.items()
        if mod.get("cross_edition_status") == "different-implementation"
    )
    mismatched = find_cross_status_mismatches(openmw, mwse)
    name_mismatched = find_cross_name_mismatches(openmw, mwse)

    print("Shared IDs:", ", ".join(shared) or "(none)")
    print("OpenMW-only IDs:", ", ".join(open_only) or "(none)")
    print("MWSE-only IDs:", ", ".join(mwse_only) or "(none)")
    print("IDs marked equivalent-needed:", ", ".join(equiv) or "(none)")
    print("IDs marked different-implementation:", ", ".join(diff_impl) or "(none)")
    print("Mismatched cross_edition_status:", ", ".join(mismatched) or "(none)")
    print("Mismatched shared-ID names:", ", ".join(name_mismatched) or "(none)")
    if mismatched or name_mismatched:
        if mismatched:
            print("[ERROR] Shared manifest IDs must use the same cross_edition_status.")
        if name_mismatched:
            print("[ERROR] Shared manifest IDs must represent the same named identity.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
