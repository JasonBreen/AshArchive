from __future__ import annotations

from pathlib import Path

import pytest

from tools.lib.wabbajack import (
    check_duplicate_archive_names,
    check_edition_wabbajack_readiness,
    check_mod_wabbajack_readiness,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_PLANNED_MOD: dict = {
    "id": "sample-mod",
    "name": "Sample Mod",
    "status": "planned",
    "source": "tbd",
    "url": "",
    "archive_name": "",
    "version": "",
}

_ACCEPTED_MOD: dict = {
    "id": "accepted-mod",
    "name": "Accepted Mod",
    "status": "accepted",
    "source": "nexus",
    "url": "https://www.nexusmods.com/morrowind/mods/12345",
    "archive_name": "AcceptedMod_1.0.7z",
    "version": "1.0",
}

_PATH = Path("test.yaml")


# ---------------------------------------------------------------------------
# Planned mods (scaffold state) — must not raise errors
# ---------------------------------------------------------------------------


def test_planned_mod_no_errors() -> None:
    messages = check_mod_wabbajack_readiness(_PLANNED_MOD, _PATH)
    errors = [m for m in messages if m.startswith("[ERROR]")]
    assert errors == []


# ---------------------------------------------------------------------------
# Accepted mod — missing download metadata
# ---------------------------------------------------------------------------


def test_accepted_mod_missing_url() -> None:
    mod = {**_ACCEPTED_MOD, "url": ""}
    messages = check_mod_wabbajack_readiness(mod, _PATH)
    assert any("has no url" in m for m in messages)


def test_accepted_mod_missing_archive_name() -> None:
    mod = {**_ACCEPTED_MOD, "archive_name": ""}
    messages = check_mod_wabbajack_readiness(mod, _PATH)
    assert any("has no archive_name" in m for m in messages)


def test_accepted_mod_missing_version() -> None:
    mod = {**_ACCEPTED_MOD, "version": ""}
    messages = check_mod_wabbajack_readiness(mod, _PATH)
    assert any("has no version" in m for m in messages)


def test_accepted_mod_tbd_source_errors() -> None:
    mod = {**_ACCEPTED_MOD, "source": "tbd"}
    messages = check_mod_wabbajack_readiness(mod, _PATH)
    assert any("unresolved source" in m for m in messages)


def test_accepted_mod_unknown_source_errors() -> None:
    mod = {**_ACCEPTED_MOD, "source": "unknown"}
    messages = check_mod_wabbajack_readiness(mod, _PATH)
    assert any("unresolved source" in m for m in messages)


# ---------------------------------------------------------------------------
# Accepted mod — fully valid
# ---------------------------------------------------------------------------


def test_accepted_mod_valid_passes() -> None:
    messages = check_mod_wabbajack_readiness(_ACCEPTED_MOD, _PATH)
    errors = [m for m in messages if m.startswith("[ERROR]")]
    assert errors == []


# ---------------------------------------------------------------------------
# Nexus URL format
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_url",
    [
        "https://example.com/mod",
        "https://www.nexusmods.com/skyrimspecialedition/mods/12345",
        "https://nexusmods.com/morrowind/mods/12345",
        "http://www.nexusmods.com/morrowind/mods/12345",
        "https://www.nexusmods.com/morrowind/mods/",
        "https://www.nexusmods.com/morrowind/mods/abc",
    ],
)
def test_nexus_invalid_url_errors(bad_url: str) -> None:
    mod = {**_PLANNED_MOD, "source": "nexus", "url": bad_url}
    messages = check_mod_wabbajack_readiness(mod, _PATH)
    assert any("malformed url" in m for m in messages)


def test_nexus_valid_url_passes() -> None:
    mod = {**_PLANNED_MOD, "source": "nexus", "url": "https://www.nexusmods.com/morrowind/mods/47423"}
    messages = check_mod_wabbajack_readiness(mod, _PATH)
    errors = [m for m in messages if m.startswith("[ERROR]")]
    assert errors == []


def test_nexus_empty_url_not_checked() -> None:
    """An empty nexus URL should not trigger the format check."""
    mod = {**_PLANNED_MOD, "source": "nexus", "url": ""}
    messages = check_mod_wabbajack_readiness(mod, _PATH)
    assert not any("malformed url" in m for m in messages)


# ---------------------------------------------------------------------------
# URL / archive_name mismatch warning
# ---------------------------------------------------------------------------


def test_url_set_without_archive_name_warns() -> None:
    mod = {**_PLANNED_MOD, "url": "https://www.nexusmods.com/morrowind/mods/1", "archive_name": ""}
    messages = check_mod_wabbajack_readiness(mod, _PATH)
    assert any("archive_name is empty" in m for m in messages)


def test_archive_name_set_without_url_no_warning() -> None:
    """archive_name without a URL is allowed (manual/offline install)."""
    mod = {**_PLANNED_MOD, "url": "", "archive_name": "SomeMod.7z"}
    messages = check_mod_wabbajack_readiness(mod, _PATH)
    assert not any("archive_name is empty" in m for m in messages)


# ---------------------------------------------------------------------------
# Archive extension warnings
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("ext", [".7z", ".zip", ".rar"])
def test_recognised_archive_extensions_pass(ext: str) -> None:
    mod = {**_ACCEPTED_MOD, "archive_name": f"SomeMod{ext}"}
    messages = check_mod_wabbajack_readiness(mod, _PATH)
    assert not any("recognised extension" in m for m in messages)


def test_unrecognised_extension_warns() -> None:
    mod = {**_ACCEPTED_MOD, "archive_name": "SomeMod_1.0"}
    messages = check_mod_wabbajack_readiness(mod, _PATH)
    assert any("recognised extension" in m for m in messages)


# ---------------------------------------------------------------------------
# Duplicate archive_name detection
# ---------------------------------------------------------------------------


def test_duplicate_archive_names_errors() -> None:
    mods = [
        {**_ACCEPTED_MOD, "id": "mod-a", "archive_name": "SharedArchive.7z"},
        {**_ACCEPTED_MOD, "id": "mod-b", "archive_name": "SharedArchive.7z"},
    ]
    messages = check_duplicate_archive_names(mods, _PATH)
    assert any("duplicate archive_name" in m for m in messages)


def test_unique_archive_names_pass() -> None:
    mods = [
        {**_ACCEPTED_MOD, "id": "mod-a", "archive_name": "ModA.7z"},
        {**_ACCEPTED_MOD, "id": "mod-b", "archive_name": "ModB.7z"},
    ]
    messages = check_duplicate_archive_names(mods, _PATH)
    assert messages == []


def test_empty_archive_names_not_flagged_as_duplicates() -> None:
    """Empty archive_name on multiple mods must not be reported as a duplicate."""
    mods = [
        {**_PLANNED_MOD, "id": "mod-a"},
        {**_PLANNED_MOD, "id": "mod-b"},
    ]
    messages = check_duplicate_archive_names(mods, _PATH)
    assert messages == []


# ---------------------------------------------------------------------------
# Integration: real manifests (scaffold state) must be error-free
# ---------------------------------------------------------------------------


def test_real_manifests_have_no_wabbajack_errors() -> None:
    from tools.lib.manifest import load_mods
    from tools.lib.paths import manifest_path

    for edition in ("openmw", "mwse"):
        path = manifest_path(edition)
        mods = load_mods(path)
        messages = check_edition_wabbajack_readiness(mods, path)
        errors = [m for m in messages if m.startswith("[ERROR]")]
        assert errors == [], f"Unexpected Wabbajack errors in {edition} manifest:\n" + "\n".join(
            errors
        )
