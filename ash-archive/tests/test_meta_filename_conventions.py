from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_META_FILES = [
    # Shared metadata
    "shared/categories.control.meta",
    "shared/sourced-mods.control.meta",
    "shared/source-triage.control.meta",
    "shared/source-package-meta.control.meta",
    # OpenMW edition manifests
    "editions/openmw/manifests/mods.control.meta",
    "editions/openmw/manifests/load-order.control.meta",
    "editions/openmw/manifests/external-tools.control.meta",
    "editions/openmw/manifests/patches.control.meta",
    "editions/openmw/manifests/rejected-mods.control.meta",
    # MWSE edition manifests
    "editions/mwse/manifests/mods.control.meta",
    "editions/mwse/manifests/load-order.control.meta",
    "editions/mwse/manifests/external-tools.control.meta",
    "editions/mwse/manifests/patches.control.meta",
    "editions/mwse/manifests/rejected-mods.control.meta",
    # Test fixtures
    "tests/fixtures/valid_mods.control.meta",
    "tests/fixtures/invalid_mods.control.meta",
    "tests/fixtures/valid_sourced_mods.control.meta",
    "tests/fixtures/invalid_sourced_mods.control.meta",
]


def test_required_meta_files_exist() -> None:
    for rel_path in REQUIRED_META_FILES:
        meta_path = ROOT / rel_path
        assert meta_path.exists(), f"missing metadata file: {rel_path}"


def test_legacy_yaml_counterparts_do_not_exist() -> None:
    for rel_path in REQUIRED_META_FILES:
        meta_path = ROOT / rel_path
        yaml_path = meta_path.with_suffix(".yaml")
        assert not yaml_path.exists(), f"legacy YAML file still present: {yaml_path}"
