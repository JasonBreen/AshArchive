from __future__ import annotations

from pathlib import Path
import subprocess

from tools.audit_modlist_source import _read_rows, audit_rows


def test_valid_source_parses() -> None:
    rows, errors = _read_rows(Path("tests/fixtures/valid_modlist_source.txt"))
    assert errors == []
    assert rows is not None
    assert len(rows) == 6


def test_missing_required_column_fails() -> None:
    rows, errors = _read_rows(Path("tests/fixtures/invalid_modlist_missing_columns.txt"))
    assert rows is None
    assert errors
    assert "missing required columns" in errors[0]


def test_enabled_disabled_counts_and_disabled_preservation() -> None:
    rows, _ = _read_rows(Path("tests/fixtures/valid_modlist_source.txt"))
    assert rows is not None

    report = audit_rows(rows)

    assert report["enabled_rows"] == 4
    assert report["disabled_rows"] == 2
    assert report["disabled_rows_detail"] == [("0003", "A Mod"), ("0005", "Offline Local")]


def test_repeated_nexus_id_and_classifications() -> None:
    rows, _ = _read_rows(Path("tests/fixtures/valid_modlist_source.txt"))
    assert rows is not None

    report = audit_rows(rows)

    assert report["repeated_positive_nexus_ids"] == {12345: ["A Mod", "A Mod - Patch"]}
    assert report["unmanaged_rows"] == 1
    assert report["dlc_rows"] == 1
    assert report["local_rows"] == 2


def test_cli_missing_columns_returns_nonzero() -> None:
    result = subprocess.run(
        [
            "python",
            "tools/audit_modlist_source.py",
            "--file",
            "tests/fixtures/invalid_modlist_missing_columns.txt",
        ],
        cwd=Path(__file__).resolve().parents[1],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "[ERROR]" in result.stdout
