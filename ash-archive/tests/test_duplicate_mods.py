from pathlib import Path

from tools.check_duplicate_mods import (
    DuplicateReport,
    _load_mods_for_path,
    find_cross_edition_name_mismatches,
    find_duplicates,
)


def test_find_duplicate_ids_and_names() -> None:
    mods = [
        {"id": "a", "name": "Same"},
        {"id": "a", "name": "Same"},
        {"id": "b", "name": "Same"},
    ]
    duplicates = find_duplicates(mods)
    assert duplicates == DuplicateReport(
        duplicate_ids=["a"],
        duplicate_names_with_different_ids=["Same"],
    )


def test_cross_edition_duplicate_names_with_different_ids_warn() -> None:
    warnings = find_cross_edition_name_mismatches(
        {
            "openmw": [{"id": "patch-for-purists-openmw", "name": "Patch for Purists"}],
            "mwse": [{"id": "patch-for-purists-mwse", "name": "Patch for Purists"}],
        }
    )

    assert warnings == [
        (
            "all editions",
            "Patch for Purists",
            "mwse: patch-for-purists-mwse; openmw: patch-for-purists-openmw",
        )
    ]


def test_load_failure_is_reported_to_caller(tmp_path: Path) -> None:
    mods, load_failed = _load_mods_for_path(tmp_path / "missing.control.meta")

    assert mods == []
    assert load_failed is True
