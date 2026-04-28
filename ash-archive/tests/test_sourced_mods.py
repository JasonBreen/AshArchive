from __future__ import annotations

from pathlib import Path
import subprocess

import yaml

from tools.lib.sourced_mods import validate_sourced_mods


FIXTURE_REQUIRED_FIELDS = {
    "id": "sample-candidate",
    "name": "Sample Candidate",
    "candidate_status": "candidate",
    "thematic_bucket": "foundation",
    "intended_editions": ["openmw"],
    "engine_notes": "Candidate note",
    "source_type": "unknown",
    "source_url": "",
    "source_confidence": "unverified",
    "compatibility_status": "unverified",
    "evidence_notes": "Needs evidence",
    "thematic_reason": "Fixture",
    "risk_level": "unknown",
    "promotion_target": "undecided",
    "promotion_notes": "",
    "reviewed_by": [],
    "last_reviewed": "",
    "related_manifest_ids": [],
}


def _write_sourced(path: Path, entries: list[dict]) -> None:
    path.write_text(yaml.safe_dump({"sourced_candidates": entries}, sort_keys=False), encoding="utf-8")


def test_valid_sourced_fixture_passes() -> None:
    _, errors = validate_sourced_mods(Path("tests/fixtures/valid_sourced_mods.control.meta"))
    assert errors == []


def test_missing_required_field_fails(tmp_path: Path) -> None:
    candidate = dict(FIXTURE_REQUIRED_FIELDS)
    candidate.pop("source_type")
    fixture = tmp_path / "sourced-mods.control.meta"
    _write_sourced(fixture, [candidate])

    _, errors = validate_sourced_mods(fixture)

    assert any("missing field 'source_type'" in error for error in errors)


def test_invalid_candidate_status_fails(tmp_path: Path) -> None:
    candidate = dict(FIXTURE_REQUIRED_FIELDS)
    candidate["candidate_status"] = "accepted"
    fixture = tmp_path / "sourced-mods.control.meta"
    _write_sourced(fixture, [candidate])

    _, errors = validate_sourced_mods(fixture)

    assert any("invalid candidate_status" in error for error in errors)


def test_invalid_thematic_bucket_fails(tmp_path: Path) -> None:
    candidate = dict(FIXTURE_REQUIRED_FIELDS)
    candidate["thematic_bucket"] = "weather"
    fixture = tmp_path / "sourced-mods.control.meta"
    _write_sourced(fixture, [candidate])

    _, errors = validate_sourced_mods(fixture)

    assert any("invalid thematic_bucket" in error for error in errors)


def test_invalid_intended_editions_fails(tmp_path: Path) -> None:
    candidate = dict(FIXTURE_REQUIRED_FIELDS)
    candidate["intended_editions"] = ["both"]
    fixture = tmp_path / "sourced-mods.control.meta"
    _write_sourced(fixture, [candidate])

    _, errors = validate_sourced_mods(fixture)

    assert any("invalid intended_editions" in error for error in errors)


def test_invalid_fixture_fails_for_multiple_reasons() -> None:
    _, errors = validate_sourced_mods(Path("tests/fixtures/invalid_sourced_mods.control.meta"))
    assert errors
    joined = "\n".join(errors)
    assert "invalid id" in joined
    assert "invalid candidate_status" in joined
    assert "invalid thematic_bucket" in joined
    assert "invalid intended_editions" in joined


def test_invalid_kebab_case_id_fails(tmp_path: Path) -> None:
    candidate = dict(FIXTURE_REQUIRED_FIELDS)
    candidate["id"] = "Sample Candidate"
    fixture = tmp_path / "sourced-mods.control.meta"
    _write_sourced(fixture, [candidate])

    _, errors = validate_sourced_mods(fixture)

    assert any("expected lowercase kebab-case" in error for error in errors)


def test_summary_tool_returns_nonzero_for_invalid_fixture() -> None:
    result = subprocess.run(
        [
            "python",
            "tools/summarize_sourced_mods.py",
            "--file",
            "tests/fixtures/invalid_sourced_mods.control.meta",
        ],
        cwd=Path(__file__).resolve().parents[1],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "[ERROR]" in result.stdout
