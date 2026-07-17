from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
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
    path.write_text(
        yaml.safe_dump({"sourced_candidates": entries}, sort_keys=False), encoding="utf-8"
    )


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


def test_blank_candidate_name_fails(tmp_path: Path) -> None:
    candidate = dict(FIXTURE_REQUIRED_FIELDS)
    candidate["name"] = "  "
    fixture = tmp_path / "sourced-mods.control.meta"
    _write_sourced(fixture, [candidate])

    _, errors = validate_sourced_mods(fixture)

    assert any("field 'name' must not be blank" in error for error in errors)


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


def test_duplicate_candidate_ids_fail(tmp_path: Path) -> None:
    first = dict(FIXTURE_REQUIRED_FIELDS)
    second = dict(FIXTURE_REQUIRED_FIELDS)
    fixture = tmp_path / "sourced-mods.control.meta"
    _write_sourced(fixture, [first, second])

    _, errors = validate_sourced_mods(fixture)

    assert any("duplicate id in sourced candidates" in error for error in errors)


@pytest.mark.parametrize(
    "url",
    ["nexusmods.com/morrowind/mods/1", "ftp://example.com/mod", "https://exa mple.com"],
)
def test_malformed_source_url_fails(tmp_path: Path, url: str) -> None:
    candidate = dict(FIXTURE_REQUIRED_FIELDS)
    candidate["source_url"] = url
    fixture = tmp_path / "sourced-mods.control.meta"
    _write_sourced(fixture, [candidate])

    _, errors = validate_sourced_mods(fixture)

    assert any("malformed source_url" in error for error in errors)


def test_verified_source_requires_canonical_evidence_but_not_human_review(tmp_path: Path) -> None:
    candidate = dict(FIXTURE_REQUIRED_FIELDS)
    candidate.update(
        {
            "source_type": "nexus",
            "source_url": "https://www.nexusmods.com/morrowind/mods/1",
            "source_confidence": "verified",
            "evidence_notes": "The source page identifies the candidate.",
        }
    )
    fixture = tmp_path / "sourced-mods.control.meta"
    _write_sourced(fixture, [candidate])

    _, errors = validate_sourced_mods(fixture)

    assert errors == []


@pytest.mark.parametrize(
    ("overrides", "expected"),
    [
        ({"source_url": ""}, "requires a valid source_url"),
        ({"source_type": "unknown"}, "cannot use source_type 'unknown'"),
        ({"evidence_notes": "needs verification"}, "requires evidence_notes"),
    ],
)
def test_verified_source_rejects_placeholder_states(
    tmp_path: Path, overrides: dict, expected: str
) -> None:
    candidate = dict(FIXTURE_REQUIRED_FIELDS)
    candidate.update(
        {
            "source_type": "nexus",
            "source_url": "https://www.nexusmods.com/morrowind/mods/1",
            "source_confidence": "verified",
            "evidence_notes": "The source page identifies the candidate.",
        }
    )
    candidate.update(overrides)
    fixture = tmp_path / "sourced-mods.control.meta"
    _write_sourced(fixture, [candidate])

    _, errors = validate_sourced_mods(fixture)

    assert any(expected in error for error in errors)


def test_compatibility_claim_requires_evidence_and_review(tmp_path: Path) -> None:
    candidate = dict(FIXTURE_REQUIRED_FIELDS)
    candidate.update(
        {
            "compatibility_status": "openmw-compatible",
            "engine_notes": "needs verification",
            "evidence_notes": "needs verification",
        }
    )
    fixture = tmp_path / "sourced-mods.control.meta"
    _write_sourced(fixture, [candidate])

    _, errors = validate_sourced_mods(fixture)

    joined = "\n".join(errors)
    assert "requires evidence and engine notes" in joined
    assert "requires review information" in joined


def test_compatibility_claim_rejects_placeholder_reviewer(tmp_path: Path) -> None:
    candidate = dict(FIXTURE_REQUIRED_FIELDS)
    candidate.update(
        {
            "compatibility_status": "openmw-compatible",
            "engine_notes": "OpenMW test route passed.",
            "evidence_notes": "Recorded test evidence supports OpenMW.",
            "reviewed_by": ["TBD"],
            "last_reviewed": "2026-07-17",
        }
    )
    fixture = tmp_path / "sourced-mods.control.meta"
    _write_sourced(fixture, [candidate])

    _, errors = validate_sourced_mods(fixture)

    joined = "\n".join(errors)
    assert "reviewed_by' must be non-placeholder" in joined
    assert "requires review information" in joined


def test_promoted_candidate_requires_review_notes_and_manifest_link(tmp_path: Path) -> None:
    candidate = dict(FIXTURE_REQUIRED_FIELDS)
    candidate.update({"candidate_status": "promoted", "promotion_target": "openmw"})
    fixture = tmp_path / "sourced-mods.control.meta"
    _write_sourced(fixture, [candidate])

    _, errors = validate_sourced_mods(fixture)

    joined = "\n".join(errors)
    assert "requires related_manifest_ids" in joined
    assert "requires promotion_notes" in joined
    assert "requires review information" in joined


@pytest.mark.parametrize("candidate_status", ["rejected", "superseded"])
def test_terminal_candidate_decision_requires_notes_and_review(
    tmp_path: Path, candidate_status: str
) -> None:
    candidate = dict(FIXTURE_REQUIRED_FIELDS)
    candidate["candidate_status"] = candidate_status
    fixture = tmp_path / "sourced-mods.control.meta"
    _write_sourced(fixture, [candidate])

    _, errors = validate_sourced_mods(fixture)

    joined = "\n".join(errors)
    assert "requires promotion_notes" in joined
    assert "requires review information" in joined


def test_malformed_related_manifest_reference_fails(tmp_path: Path) -> None:
    candidate = dict(FIXTURE_REQUIRED_FIELDS)
    candidate["related_manifest_ids"] = ["Bad Manifest ID"]
    fixture = tmp_path / "sourced-mods.control.meta"
    _write_sourced(fixture, [candidate])

    _, errors = validate_sourced_mods(fixture)

    assert any("malformed reference" in error for error in errors)


def test_promotion_target_must_fit_intended_editions(tmp_path: Path) -> None:
    candidate = dict(FIXTURE_REQUIRED_FIELDS)
    candidate["promotion_target"] = "mwse"
    fixture = tmp_path / "sourced-mods.control.meta"
    _write_sourced(fixture, [candidate])

    _, errors = validate_sourced_mods(fixture)

    assert any("promotion_target 'mwse' contradicts intended_editions" in error for error in errors)
