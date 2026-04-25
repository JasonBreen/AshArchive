from pathlib import Path

import pytest
import yaml

from tools.lib.validation import validate_manifest


FIXTURE_REQUIRED_FIELDS = {
    "id": "sample-mod",
    "name": "Sample Mod",
    "category": "Bug Fixes and Stability",
    "edition": "openmw",
    "cross_edition_status": "equivalent-needed",
    "status": "planned",
    "engine": ["openmw"],
    "source": "tbd",
    "url": "",
    "archive_name": "",
    "version": "",
    "plugin_files": [],
    "requires": [],
    "conflicts": [],
    "load_after": [],
    "load_before": [],
    "patch_notes": "needs verification",
    "testing_notes": "needs verification",
    "decision_reason": "fixture",
    "priority": 1,
}


def _write_manifest(path: Path, mods: list[dict]) -> None:
    path.write_text(yaml.safe_dump({"mods": mods}, sort_keys=False), encoding="utf-8")


def test_valid_fixture_passes() -> None:
    errors = validate_manifest(Path("tests/fixtures/valid_mods.yaml"), "openmw")
    assert errors == []


def test_invalid_fixture_fails() -> None:
    errors = validate_manifest(Path("tests/fixtures/invalid_mods.yaml"), "openmw")
    assert errors
    joined = "\n".join(errors)
    assert "invalid id" in joined
    assert "invalid cross_edition_status" in joined
    assert "field 'priority' must be integer" in joined
    assert "invalid category" in joined


def test_missing_required_field_fails(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod.pop("url")
    fixture = tmp_path / "mods.yaml"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("missing field 'url'" in error for error in errors)


def test_invalid_enum_fails(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["status"] = "not-valid"
    fixture = tmp_path / "mods.yaml"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("invalid status" in error for error in errors)


def test_invalid_category_fails(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["category"] = "Bugfixes"
    fixture = tmp_path / "mods.yaml"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("invalid category" in error for error in errors)


@pytest.mark.parametrize(
    "invalid_id",
    ["Patch For Purists", "patch_for_purists", "Patch-for-Purists", "patch for purists"],
)
def test_invalid_kebab_case_id_fails(tmp_path: Path, invalid_id: str) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["id"] = invalid_id
    fixture = tmp_path / "mods.yaml"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("expected lowercase kebab-case" in error for error in errors)


def test_edition_mismatch_fails(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["edition"] = "mwse"
    fixture = tmp_path / "mods.yaml"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("edition mismatch" in error for error in errors)


def test_openmw_manifest_rejects_mwse_engine_value(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["engine"] = ["mwse"]
    fixture = tmp_path / "mods.yaml"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("invalid engine values" in error for error in errors)


def test_engine_unknown_cannot_be_combined(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["engine"] = ["unknown", "openmw"]
    fixture = tmp_path / "mods.yaml"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("cannot combine 'unknown'" in error for error in errors)
