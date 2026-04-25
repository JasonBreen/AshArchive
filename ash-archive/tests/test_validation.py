from pathlib import Path

from tools.lib.validation import validate_manifest


def test_valid_fixture_passes() -> None:
    errors = validate_manifest(Path("tests/fixtures/valid_mods.yaml"), "openmw")
    assert errors == []


def test_invalid_fixture_fails() -> None:
    errors = validate_manifest(Path("tests/fixtures/invalid_mods.yaml"), "openmw")
    assert errors
    joined = "\n".join(errors)
    assert "invalid id" in joined
    assert "invalid cross_edition_status" in joined
    assert "priority" in joined
