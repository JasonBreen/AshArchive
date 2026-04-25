#!/usr/bin/env python3
from __future__ import annotations

from lib.manifest import load_mods
from lib.paths import manifest_path
from lib.validation import validate_manifest


def main() -> int:
    errs = []
    errs.extend(validate_manifest(manifest_path("openmw"), "openmw"))
    errs.extend(validate_manifest(manifest_path("mwse"), "mwse"))
    if errs:
        print("Cannot compare editions due to manifest errors:")
        for err in errs:
            print(f"- {err}")
        return 1

    openmw = {m["id"]: m for m in load_mods(manifest_path("openmw"))}
    mwse = {m["id"]: m for m in load_mods(manifest_path("mwse"))}

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
    mismatched = sorted(
        mod_id
        for mod_id in shared
        if openmw[mod_id].get("cross_edition_status") != mwse[mod_id].get("cross_edition_status")
    )

    print("Shared IDs:", ", ".join(shared) or "(none)")
    print("OpenMW-only IDs:", ", ".join(open_only) or "(none)")
    print("MWSE-only IDs:", ", ".join(mwse_only) or "(none)")
    print("IDs marked equivalent-needed:", ", ".join(equiv) or "(none)")
    print("IDs marked different-implementation:", ", ".join(diff_impl) or "(none)")
    print("Mismatched cross_edition_status:", ", ".join(mismatched) or "(none)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
