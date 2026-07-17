from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CONTROL_META_FILES = [
    "shared/categories.control.meta",
    "shared/sourced-mods.control.meta",
    "shared/source-triage.control.meta",
    "shared/source-package-meta.control.meta",
]


def _to_legacy_yaml_path(meta_path: Path) -> Path:
    return meta_path.with_name(meta_path.name.replace(".control.meta", ".yaml"))


def test_expected_meta_files_exist() -> None:
    edition_manifest_meta = sorted(
        ROOT.glob("editions/*/manifests/*.control.meta"),
    )
    fixture_meta = sorted(
        ROOT.glob("tests/fixtures/*.control.meta"),
    )

    assert edition_manifest_meta, "expected .control.meta files under editions/*/manifests/"
    assert fixture_meta, "expected .control.meta fixtures under tests/fixtures/"

    for rel_path in CONTROL_META_FILES:
        meta_path = ROOT / rel_path
        assert meta_path.exists(), f"missing shared control metadata file: {rel_path}"


def test_legacy_yaml_equivalents_absent() -> None:
    canonical_meta_paths = [ROOT / rel_path for rel_path in CONTROL_META_FILES]
    canonical_meta_paths.extend(ROOT.glob("editions/*/manifests/*.control.meta"))
    canonical_meta_paths.extend(ROOT.glob("tests/fixtures/*.control.meta"))

    assert canonical_meta_paths, "no canonical .control.meta files discovered"

    for meta_path in canonical_meta_paths:
        yaml_path = _to_legacy_yaml_path(meta_path)
        assert not yaml_path.exists(), f"legacy YAML file still present: {yaml_path}"
