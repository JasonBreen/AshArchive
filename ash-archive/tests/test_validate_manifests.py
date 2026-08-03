from pathlib import Path

import pytest
import yaml

from tools import validate_manifests as manifest_validator

FIXTURE_DIR = Path(__file__).parent / "fixtures"


def test_validate_repository_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Setup mock manifests
    manifest_paths = {
        "openmw": tmp_path / "openmw.control.meta",
        "mwse": tmp_path / "mwse.control.meta",
    }

    # We'll use simple valid mods with empty lists, no refs needed for basic passes if we craft them carefully
    openmw_mod = {
        "id": "test-mod",
        "name": "Test Mod",
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

    mwse_mod = dict(openmw_mod)
    mwse_mod["id"] = "test-mod-mwse"
    mwse_mod["edition"] = "mwse"
    mwse_mod["engine"] = ["mwse"]

    manifest_paths["openmw"].write_text(yaml.dump({"mods": [openmw_mod]}), encoding="utf-8")
    manifest_paths["mwse"].write_text(yaml.dump({"mods": [mwse_mod]}), encoding="utf-8")

    # Mock sourced mods path
    source_path = tmp_path / "sourced-mods.control.meta"
    source_path.write_text(yaml.dump({"sourced_candidates": []}), encoding="utf-8")

    monkeypatch.setattr(
        manifest_validator, "manifest_path", lambda edition: manifest_paths[edition]
    )

    # Test valid repository
    errors = manifest_validator.validate_repository(["openmw", "mwse"], source_path)
    assert not errors


def test_validate_repository_load_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    manifest_paths = {
        "openmw": tmp_path / "openmw.control.meta",
        "mwse": tmp_path / "mwse.control.meta",
    }

    # Malformed YAML
    manifest_paths["openmw"].write_text("mods: [invalid_yaml: }", encoding="utf-8")

    # Valid YAML but empty for mwse
    manifest_paths["mwse"].write_text(yaml.dump({"mods": []}), encoding="utf-8")

    source_path = tmp_path / "sourced-mods.control.meta"
    source_path.write_text(yaml.dump({"sourced_candidates": []}), encoding="utf-8")

    monkeypatch.setattr(
        manifest_validator, "manifest_path", lambda edition: manifest_paths[edition]
    )

    # If the edition is in the requested list, the error should be captured
    errors = manifest_validator.validate_repository(["openmw"], source_path)
    assert len(errors) == 1
    assert "Invalid YAML content" in errors[0]


def test_validate_repository_manifest_validation_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest_paths = {
        "openmw": tmp_path / "openmw.control.meta",
        "mwse": tmp_path / "mwse.control.meta",
    }

    # Missing required fields will fail manifest validation
    bad_mod = {"id": "bad-mod"}
    manifest_paths["openmw"].write_text(yaml.dump({"mods": [bad_mod]}), encoding="utf-8")
    manifest_paths["mwse"].write_text(yaml.dump({"mods": []}), encoding="utf-8")

    source_path = tmp_path / "sourced-mods.control.meta"
    source_path.write_text(yaml.dump({"sourced_candidates": []}), encoding="utf-8")

    monkeypatch.setattr(
        manifest_validator, "manifest_path", lambda edition: manifest_paths[edition]
    )

    errors = manifest_validator.validate_repository(["openmw"], source_path)
    assert len(errors) > 0
    assert any("missing field" in err for err in errors)


def test_validate_repository_edition_filtering(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest_paths = {
        "openmw": tmp_path / "openmw.control.meta",
        "mwse": tmp_path / "mwse.control.meta",
    }

    # openmw is valid
    openmw_mod = {
        "id": "test-mod",
        "name": "Test Mod",
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
    manifest_paths["openmw"].write_text(yaml.dump({"mods": [openmw_mod]}), encoding="utf-8")

    # mwse is malformed yaml
    manifest_paths["mwse"].write_text("mods: [invalid_yaml: }", encoding="utf-8")

    source_path = tmp_path / "sourced-mods.control.meta"
    source_path.write_text(yaml.dump({"sourced_candidates": []}), encoding="utf-8")

    monkeypatch.setattr(
        manifest_validator, "manifest_path", lambda edition: manifest_paths[edition]
    )

    # Should skip validation of mwse (load error suppressed because mwse not in editions list)
    errors = manifest_validator.validate_repository(["openmw"], source_path)
    assert not errors
