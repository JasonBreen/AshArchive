from tools.lib.paths import ROOT, categories_path, manifest_path


def test_manifest_path():
    openmw_path = manifest_path("openmw")
    assert openmw_path == ROOT / "editions" / "openmw" / "manifests" / "mods.control.meta"
    assert openmw_path.parts[-4:] == ("editions", "openmw", "manifests", "mods.control.meta")

    mwse_path = manifest_path("mwse")
    assert mwse_path == ROOT / "editions" / "mwse" / "manifests" / "mods.control.meta"
    assert mwse_path.parts[-4:] == ("editions", "mwse", "manifests", "mods.control.meta")


def test_categories_path():
    cat_path = categories_path()
    assert cat_path == ROOT / "shared" / "categories.control.meta"
    assert cat_path.parts[-2:] == ("shared", "categories.control.meta")
