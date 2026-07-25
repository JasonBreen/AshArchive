from pathlib import Path

from tools.lib.paths import categories_path, manifest_path

_ROOT = Path(__file__).resolve().parents[1]


def test_manifest_path() -> None:
    openmw_path = manifest_path("openmw")
    assert openmw_path == _ROOT / "editions" / "openmw" / "manifests" / "mods.control.meta"
    assert openmw_path.parts[-4:] == ("editions", "openmw", "manifests", "mods.control.meta")

    mwse_path = manifest_path("mwse")
    assert mwse_path == _ROOT / "editions" / "mwse" / "manifests" / "mods.control.meta"
    assert mwse_path.parts[-4:] == ("editions", "mwse", "manifests", "mods.control.meta")


def test_categories_path() -> None:
    cat_path = categories_path()
    assert cat_path == _ROOT / "shared" / "categories.control.meta"
    assert cat_path.parts[-2:] == ("shared", "categories.control.meta")
