from pathlib import Path

import pytest
import yaml

from tools import validate_manifests as manifest_validator
from tools.lib.validation import validate_manifest, validate_source_references

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
    errors = validate_manifest(Path("tests/fixtures/valid_mods.control.meta"), "openmw")
    assert errors == []


def test_invalid_fixture_fails() -> None:
    errors = validate_manifest(Path("tests/fixtures/invalid_mods.control.meta"), "openmw")
    assert errors
    joined = "\n".join(errors)
    assert "invalid id" in joined
    assert "invalid cross_edition_status" in joined
    assert "field 'priority' must be integer" in joined
    assert "invalid category" in joined


def test_missing_required_field_fails(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod.pop("url")
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("missing field 'url'" in error for error in errors)


def test_invalid_enum_fails(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["status"] = "not-valid"
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("invalid status" in error for error in errors)


def test_invalid_category_fails(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["category"] = "Bugfixes"
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("invalid category" in error for error in errors)


def test_blank_manifest_name_fails(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["name"] = "  "
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("field 'name' must not be blank" in error for error in errors)


@pytest.mark.parametrize(
    "invalid_id",
    ["Patch For Purists", "patch_for_purists", "Patch-for-Purists", "patch for purists"],
)
def test_invalid_kebab_case_id_fails(tmp_path: Path, invalid_id: str) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["id"] = invalid_id
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("expected lowercase kebab-case" in error for error in errors)


def test_edition_mismatch_fails(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["edition"] = "mwse"
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("edition mismatch" in error for error in errors)


@pytest.mark.parametrize(
    ("edition", "cross_edition_status"),
    [("openmw", "mwse-only"), ("mwse", "openmw-only")],
)
def test_cross_edition_status_must_match_manifest_edition(
    tmp_path: Path, edition: str, cross_edition_status: str
) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["edition"] = edition
    mod["engine"] = [edition]
    mod["cross_edition_status"] = cross_edition_status
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, edition)

    assert any("incompatible with edition" in error for error in errors)


def test_openmw_manifest_rejects_mwse_engine_value(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["engine"] = ["mwse"]
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("invalid engine values" in error for error in errors)


def test_engine_unknown_cannot_be_combined(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["engine"] = ["unknown", "openmw"]
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("cannot combine 'unknown'" in error for error in errors)


def test_duplicate_ids_fail(tmp_path: Path) -> None:
    first = dict(FIXTURE_REQUIRED_FIELDS)
    second = dict(FIXTURE_REQUIRED_FIELDS)
    second["priority"] = 2
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [first, second])

    errors = validate_manifest(fixture, "openmw")

    assert any("duplicate id in manifest" in error for error in errors)


def test_duplicate_priority_within_category_fails(tmp_path: Path) -> None:
    first = dict(FIXTURE_REQUIRED_FIELDS)
    second = dict(FIXTURE_REQUIRED_FIELDS, id="second-mod", name="Second Mod")
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [first, second])

    errors = validate_manifest(fixture, "openmw")

    assert any("duplicate priority 1 within category" in error for error in errors)


def test_same_priority_in_different_categories_passes(tmp_path: Path) -> None:
    first = dict(FIXTURE_REQUIRED_FIELDS)
    second = dict(
        FIXTURE_REQUIRED_FIELDS,
        id="second-mod",
        name="Second Mod",
        category="Engine and Foundation",
    )
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [first, second])

    errors = validate_manifest(fixture, "openmw")

    assert errors == []


@pytest.mark.parametrize("priority", [0, -1, True])
def test_priority_must_be_positive_integer(tmp_path: Path, priority: object) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["priority"] = priority
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("priority" in error for error in errors)


@pytest.mark.parametrize(
    "url",
    ["nexusmods.com/morrowind/mods/1", "ftp://example.com/mod", "https://exa mple.com"],
)
def test_malformed_manifest_url_fails(tmp_path: Path, url: str) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["url"] = url
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("malformed url" in error for error in errors)


def test_honest_planned_placeholder_passes(tmp_path: Path) -> None:
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [dict(FIXTURE_REQUIRED_FIELDS)])

    assert validate_manifest(fixture, "openmw") == []


def test_testing_status_rejects_placeholder_evidence(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["status"] = "testing"
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    joined = "\n".join(errors)
    assert "requires a verified 'source'" in joined
    assert "requires a verified 'url'" in joined
    assert "requires non-placeholder 'archive_name' evidence" in joined
    assert "requires non-placeholder 'version' evidence" in joined
    assert "requires non-placeholder 'testing_notes' evidence" in joined
    assert "requires reviewed_by" in joined
    assert "requires last_reviewed" in joined


def test_testing_status_with_concrete_evidence_passes(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod.update(
        {
            "status": "testing",
            "source": "nexus",
            "url": "https://www.nexusmods.com/morrowind/mods/1",
            "archive_name": "sample.7z",
            "version": "1.0",
            "testing_notes": "Smoke test completed on the documented route.",
            "decision_reason": "Maintainer approved this entry for the test queue.",
            "reviewed_by": ["Maintainer A"],
            "last_reviewed": "2026-07-17",
        }
    )
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    assert validate_manifest(fixture, "openmw") == []


@pytest.mark.parametrize(
    "testing_notes",
    ["Not tested.", "No repository test evidence is recorded.", "Testing pending."],
)
def test_testing_status_rejects_explicit_non_test_evidence(
    tmp_path: Path, testing_notes: str
) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod.update(
        {
            "status": "testing",
            "source": "nexus",
            "url": "https://www.nexusmods.com/morrowind/mods/1",
            "archive_name": "sample.7z",
            "version": "1.0",
            "testing_notes": testing_notes,
            "decision_reason": "Maintainer approved this entry for the test queue.",
            "reviewed_by": ["Maintainer A"],
            "last_reviewed": "2026-07-17",
        }
    )
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("requires non-placeholder 'testing_notes' evidence" in error for error in errors)


def test_testing_status_rejects_placeholder_reviewer(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod.update(
        {
            "status": "testing",
            "source": "nexus",
            "url": "https://www.nexusmods.com/morrowind/mods/1",
            "archive_name": "sample.7z",
            "version": "1.0",
            "testing_notes": "Documented smoke-test route passed.",
            "decision_reason": "Maintainer approved this entry for the test queue.",
            "reviewed_by": ["TBD"],
            "last_reviewed": "2026-07-17",
        }
    )
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("reviewed_by' must be non-placeholder" in error for error in errors)
    assert any("status 'testing' requires reviewed_by" in error for error in errors)


@pytest.mark.parametrize("status", ["rejected", "needs-patch", "deprecated"])
def test_decision_status_requires_rationale(tmp_path: Path, status: str) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod.update({"status": status, "decision_reason": "TBD"})
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("requires non-placeholder 'decision_reason' rationale" in error for error in errors)
    if status == "rejected":
        assert any("status 'rejected' requires reviewed_by" in error for error in errors)
        assert any("status 'rejected' requires last_reviewed" in error for error in errors)


def test_accepted_status_requires_canonical_source_reference(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod.update(
        {
            "status": "accepted",
            "source": "nexus",
            "url": "https://www.nexusmods.com/morrowind/mods/1",
            "archive_name": "sample.7z",
            "version": "1.0",
            "testing_notes": "Compatibility route completed without observed blockers.",
            "decision_reason": "Maintainer reviewed the recorded evidence.",
            "reviewed_by": ["Maintainer A"],
            "last_reviewed": "2026-07-17",
        }
    )
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("status 'accepted' requires source_reference" in error for error in errors)


@pytest.mark.parametrize("field_name", ["requires", "conflicts", "load_after", "load_before"])
def test_malformed_manifest_reference_fails(tmp_path: Path, field_name: str) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod[field_name] = ["Bad Reference"]
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any(f"field '{field_name}' has malformed reference" in error for error in errors)


@pytest.mark.parametrize("field_name", ["requires", "conflicts", "load_after", "load_before"])
def test_nonexistent_manifest_reference_fails(tmp_path: Path, field_name: str) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod[field_name] = ["missing-mod"]
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("references nonexistent manifest id 'missing-mod'" in error for error in errors)


def test_valid_manifest_reference_passes(tmp_path: Path) -> None:
    required = dict(FIXTURE_REQUIRED_FIELDS)
    dependent = dict(
        FIXTURE_REQUIRED_FIELDS,
        id="dependent-mod",
        name="Dependent Mod",
        priority=2,
        requires=["sample-mod"],
        load_after=["sample-mod"],
    )
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [required, dependent])

    assert validate_manifest(fixture, "openmw") == []


def test_contradictory_manifest_references_fail(tmp_path: Path) -> None:
    required = dict(FIXTURE_REQUIRED_FIELDS)
    dependent = dict(
        FIXTURE_REQUIRED_FIELDS,
        id="dependent-mod",
        name="Dependent Mod",
        priority=2,
        requires=["sample-mod"],
        conflicts=["sample-mod"],
        load_after=["sample-mod"],
        load_before=["sample-mod"],
    )
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [required, dependent])

    errors = validate_manifest(fixture, "openmw")

    joined = "\n".join(errors)
    assert "both requires and conflicts" in joined
    assert "both load_after and load_before" in joined


def test_invalid_source_reference_shape_fails(tmp_path: Path) -> None:
    mod = dict(FIXTURE_REQUIRED_FIELDS)
    mod["source_reference"] = "Bad Source ID"
    fixture = tmp_path / "mods.control.meta"
    _write_manifest(fixture, [mod])

    errors = validate_manifest(fixture, "openmw")

    assert any("source_reference" in error for error in errors)


def _canonical_candidate(**overrides: object) -> dict:
    candidate = {
        "id": "sample-candidate",
        "name": "Sample Candidate",
        "candidate_status": "candidate",
        "thematic_bucket": "foundation",
        "intended_editions": ["openmw"],
        "engine_notes": "OpenMW evaluation remains pending.",
        "source_type": "nexus",
        "source_url": "https://www.nexusmods.com/morrowind/mods/1",
        "source_confidence": "verified",
        "compatibility_status": "needs-testing",
        "evidence_notes": "The source page identifies the candidate.",
        "thematic_reason": "Fixture",
        "risk_level": "unknown",
        "promotion_target": "openmw",
        "promotion_notes": "",
        "reviewed_by": [],
        "last_reviewed": "",
        "related_manifest_ids": ["sample-manifest-id"],
    }
    candidate.update(overrides)
    return candidate


def _linked_manifest(**overrides: object) -> dict:
    mod = dict(
        FIXTURE_REQUIRED_FIELDS,
        id="sample-manifest-id",
        name="Sample Candidate",
        source_reference="sample-candidate",
    )
    mod.update(overrides)
    return mod


def _validate_source_link(mod: dict, candidate: dict) -> list[str]:
    return validate_source_references(
        {"openmw": [mod], "mwse": []},
        {"openmw": Path("openmw.meta"), "mwse": Path("mwse.meta")},
        [candidate],
        Path("sourced.meta"),
        ["openmw"],
    )


def test_valid_source_reference_passes() -> None:
    assert _validate_source_link(_linked_manifest(), _canonical_candidate()) == []


@pytest.mark.parametrize(
    ("mod_overrides", "candidate_overrides", "expected"),
    [
        ({"name": "Wrong Name"}, {}, "name does not match"),
        ({}, {"intended_editions": ["mwse"]}, "does not include edition"),
        ({}, {"related_manifest_ids": []}, "does not link back"),
        ({"source": "github"}, {}, "does not match canonical source_type"),
        ({"url": "https://example.com/wrong"}, {}, "does not match canonical source_url"),
    ],
)
def test_source_reference_mismatches_fail(
    mod_overrides: dict,
    candidate_overrides: dict,
    expected: str,
) -> None:
    errors = _validate_source_link(
        _linked_manifest(**mod_overrides),
        _canonical_candidate(**candidate_overrides),
    )

    assert any(expected in error for error in errors)


def test_nonexistent_source_reference_fails() -> None:
    mod = _linked_manifest(source_reference="missing-source")

    errors = _validate_source_link(mod, _canonical_candidate())

    assert any("does not exist" in error for error in errors)


def test_nonexistent_related_manifest_id_fails() -> None:
    candidate = _canonical_candidate(related_manifest_ids=["missing-manifest"])

    errors = _validate_source_link(_linked_manifest(), candidate)

    assert any("references nonexistent manifest id" in error for error in errors)


def test_planning_source_link_is_independent_of_promotion_target() -> None:
    candidate = _canonical_candidate(promotion_target="mwse")

    assert _validate_source_link(_linked_manifest(), candidate) == []


def test_accepted_source_link_requires_matching_promotion_target() -> None:
    mod = _linked_manifest(status="accepted")
    candidate = _canonical_candidate(
        candidate_status="promoted",
        compatibility_status="openmw-compatible",
        promotion_target="mwse",
    )

    errors = _validate_source_link(mod, candidate)

    assert any("promotion_target to include edition 'openmw'" in error for error in errors)


def test_reverse_source_link_rejects_wrong_edition_only_match() -> None:
    wrong_edition_mod = _linked_manifest(edition="mwse", engine=["mwse"])
    wrong_edition_mod.pop("source_reference")
    candidate = _canonical_candidate(intended_editions=["openmw"])

    errors = validate_source_references(
        {"openmw": [], "mwse": [wrong_edition_mod]},
        {"openmw": Path("openmw.meta"), "mwse": Path("mwse.meta")},
        [candidate],
        Path("sourced.meta"),
        ["mwse"],
    )

    assert any("resolves only to unintended editions" in error for error in errors)


def test_empty_source_registry_does_not_bypass_manifest_links(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest_paths = {
        "openmw": tmp_path / "openmw.control.meta",
        "mwse": tmp_path / "mwse.control.meta",
    }
    _write_manifest(manifest_paths["openmw"], [_linked_manifest()])
    _write_manifest(manifest_paths["mwse"], [])
    source_path = tmp_path / "sourced-mods.control.meta"
    source_path.write_text("sourced_candidates: []\n", encoding="utf-8")
    monkeypatch.setattr(
        manifest_validator, "manifest_path", lambda edition: manifest_paths[edition]
    )

    errors = manifest_validator.validate_repository(["openmw"], source_path)

    assert any("source_reference 'sample-candidate' does not exist" in error for error in errors)
