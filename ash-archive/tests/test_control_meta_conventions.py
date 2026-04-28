from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONTROL_META_FILES = [
    "shared/categories.control.meta",
    "shared/sourced-mods.control.meta",
    "shared/source-triage.control.meta",
    "shared/source-package-meta.control.meta",
    "editions/openmw/manifests/mods.control.meta",
    "editions/openmw/manifests/load-order.control.meta",
    "editions/openmw/manifests/external-tools.control.meta",
    "editions/openmw/manifests/patches.control.meta",
    "editions/openmw/manifests/rejected-mods.control.meta",
    "editions/mwse/manifests/mods.control.meta",
    "editions/mwse/manifests/load-order.control.meta",
    "editions/mwse/manifests/external-tools.control.meta",
    "editions/mwse/manifests/patches.control.meta",
    "editions/mwse/manifests/rejected-mods.control.meta",
]


def test_internal_control_files_use_control_meta_extension() -> None:
    for rel_path in CONTROL_META_FILES:
        control_path = ROOT / rel_path
        assert control_path.exists(), f"missing control meta file: {rel_path}"
        legacy_path = control_path.with_name(control_path.name.replace(".control.meta", ".meta"))
        assert not legacy_path.exists(), f"legacy meta file still present: {legacy_path}"


def test_mo2_sidecar_doc_marks_internal_meta_as_non_sidecar() -> None:
    doc_path = ROOT / "shared" / "mo2-download-meta-sidecars.md"
    text = doc_path.read_text(encoding="utf-8")
    assert "not MO2 download sidecars" in text
