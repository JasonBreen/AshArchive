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
