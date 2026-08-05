import pytest

from tools.compare_editions import find_cross_name_mismatches, find_cross_status_mismatches, main
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


def test_main_success(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_load_mods(path: str) -> list[dict]:
        if "openmw" in str(path):
            return [{"id": "mod-a", "name": "Mod A", "cross_edition_status": "equivalent-needed"}]
        return [{"id": "mod-a", "name": "Mod A", "cross_edition_status": "equivalent-needed"}]

    monkeypatch.setattr("tools.compare_editions.load_mods", mock_load_mods)
    monkeypatch.setattr("tools.compare_editions.validate_manifest", lambda *args, **kwargs: [])

    assert main() == 0
    out, _err = capsys.readouterr()
    assert "Shared IDs: mod-a" in out
    assert "Mismatched cross_edition_status: (none)" in out


def test_main_load_error(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_load_mods(path: str) -> list[dict]:
        raise ValueError("Invalid manifest")

    monkeypatch.setattr("tools.compare_editions.load_mods", mock_load_mods)

    assert main() == 1
    out, _err = capsys.readouterr()
    assert "Cannot compare editions due to manifest errors:" in out
    assert "- [ERROR] Invalid manifest" in out


def test_main_mismatch_error(
    capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    def mock_load_mods(path: str) -> list[dict]:
        if "openmw" in str(path):
            return [{"id": "mod-a", "name": "Mod A", "cross_edition_status": "equivalent-needed"}]
        return [
            {"id": "mod-a", "name": "Mod B", "cross_edition_status": "different-implementation"}
        ]

    monkeypatch.setattr("tools.compare_editions.load_mods", mock_load_mods)
    monkeypatch.setattr("tools.compare_editions.validate_manifest", lambda *args, **kwargs: [])

    assert main() == 1
    out, _err = capsys.readouterr()
    assert "[ERROR] Shared manifest IDs must use the same cross_edition_status." in out
    assert "[ERROR] Shared manifest IDs must represent the same named identity." in out
