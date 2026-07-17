from tools.compare_editions import find_cross_name_mismatches, find_cross_status_mismatches
from tools.lib.manifest import load_mods
from tools.lib.paths import manifest_path


def test_editions_have_shared_ids() -> None:
    openmw = {m["id"] for m in load_mods(manifest_path("openmw"))}
    mwse = {m["id"] for m in load_mods(manifest_path("mwse"))}
    assert openmw & mwse


def test_each_edition_has_unique_ids() -> None:
    openmw = {m["id"] for m in load_mods(manifest_path("openmw"))}
    mwse = {m["id"] for m in load_mods(manifest_path("mwse"))}
    assert openmw - mwse
    assert mwse - openmw


def test_cross_edition_status_mismatch_is_detected() -> None:
    openmw = {"shared-id": {"cross_edition_status": "equivalent-needed"}}
    mwse = {"shared-id": {"cross_edition_status": "different-implementation"}}

    assert find_cross_status_mismatches(openmw, mwse) == ["shared-id"]


def test_cross_edition_name_mismatch_is_detected() -> None:
    openmw = {"shared-id": {"name": "Shared Identity"}}
    mwse = {"shared-id": {"name": "Different Identity"}}

    assert find_cross_name_mismatches(openmw, mwse) == ["shared-id"]
