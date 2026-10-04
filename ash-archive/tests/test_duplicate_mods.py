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


def test_main_no_issues(capsys) -> None:
    from unittest.mock import patch

    from tools.check_duplicate_mods import main

    with patch("tools.check_duplicate_mods._load_mods_for_path") as mock_load:
        mock_load.return_value = ([], False)
        result = main()
    assert result == 0
    captured = capsys.readouterr()
    assert "[OK] No duplicate IDs or likely accidental duplicate names found." in captured.out


def test_main_load_failed(capsys) -> None:
    from unittest.mock import patch

    from tools.check_duplicate_mods import main

    with patch("tools.check_duplicate_mods._load_mods_for_path") as mock_load:
        mock_load.return_value = ([], True)
        result = main()
    assert result == 1


def test_main_duplicate_ids(capsys) -> None:
    from unittest.mock import patch

    from tools.check_duplicate_mods import main

    with patch("tools.check_duplicate_mods._load_mods_for_path") as mock_load:
        mock_load.return_value = ([{"id": "a", "name": "A"}, {"id": "a", "name": "A"}], False)
        result = main()
    assert result == 1
    captured = capsys.readouterr()
    assert "[ERROR]" in captured.out
    assert "duplicate id in manifest" in captured.out


def test_main_duplicate_names_same_edition(capsys) -> None:
    from unittest.mock import patch

    from tools.check_duplicate_mods import main

    with patch("tools.check_duplicate_mods._load_mods_for_path") as mock_load:
        mock_load.return_value = ([{"id": "a", "name": "A"}, {"id": "b", "name": "A"}], False)
        result = main()
    assert result == 0
    captured = capsys.readouterr()
    assert "[WARN]" in captured.out
    assert "duplicate name used by different ids in this manifest" in captured.out
    assert "[OK] Duplicate scan completed with warnings only." in captured.out


def test_main_cross_edition_warnings(capsys) -> None:
    from unittest.mock import patch

    from tools.check_duplicate_mods import main

    def mock_load_side_effect(path):
        if "openmw" in str(path):
            return [{"id": "a", "name": "A"}], False
        elif "mwse" in str(path):
            return [{"id": "b", "name": "A"}], False
        return [], False

    with patch("tools.check_duplicate_mods._load_mods_for_path") as mock_load:
        mock_load.side_effect = mock_load_side_effect
        result = main()

    assert result == 0
    captured = capsys.readouterr()
    assert (
        "[WARN] all editions :: A :: duplicate name across editions with different ids"
        in captured.out
    )
    assert "[OK] Duplicate scan completed with warnings only." in captured.out
