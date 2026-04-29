from __future__ import annotations

import re
from pathlib import Path

from .manifest import load_meta_document

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

REQUIRED_FIELDS = [
    "id",
    "name",
    "candidate_status",
    "thematic_bucket",
    "intended_editions",
    "engine_notes",
    "source_type",
    "source_url",
    "source_confidence",
    "compatibility_status",
    "evidence_notes",
    "thematic_reason",
    "risk_level",
    "promotion_target",
    "promotion_notes",
    "reviewed_by",
    "last_reviewed",
    "related_manifest_ids",
]

CANDIDATE_STATUS = {"candidate", "under-review", "promoted", "rejected", "superseded"}
THEMATIC_BUCKETS = {
    "foundation",
    "engine-tools",
    "dream-sixth-house",
    "blight-ash-weather",
    "soundscape-silence",
    "visual-atmosphere",
    "travel-pilgrimage",
    "factions-politics",
    "quests-archives",
    "survival-body-horror",
    "ui-perception",
    "landmass-expansion",
    "patches-compatibility",
}
INTENDED_EDITIONS = {"openmw", "mwse"}
SOURCE_TYPES = {"nexus", "modding-openmw", "github", "author-site", "documentation", "unknown"}
SOURCE_CONFIDENCE = {"verified", "likely", "unverified"}
COMPATIBILITY_STATUS = {
    "unverified",
    "openmw-compatible",
    "mwse-compatible",
    "both-compatible",
    "incompatible",
    "needs-testing",
    "conflicting-reports",
}
RISK_LEVELS = {"low", "medium", "high", "unknown"}
PROMOTION_TARGETS = {"openmw", "mwse", "both", "neither", "undecided"}


def _format_error(path: Path, mod_ref: str, detail: str) -> str:
    return f"[ERROR] {path} :: {mod_ref} :: {detail}"


def _mod_ref(candidate: dict) -> str:
    mod_id = candidate.get("id")
    mod_name = candidate.get("name")
    if isinstance(mod_id, str) and mod_id:
        return mod_id
    if isinstance(mod_name, str) and mod_name:
        return mod_name
    return "<missing-id>"


def _validate_string_field(candidate: dict, field_name: str, path: Path, mod_ref: str) -> list[str]:
    if not isinstance(candidate[field_name], str):
        return [_format_error(path, mod_ref, f"field '{field_name}' must be a string")]
    return []


def validate_candidate(candidate: dict, path: Path) -> list[str]:
    errors: list[str] = []
    mod_ref = _mod_ref(candidate)

    for field_name in REQUIRED_FIELDS:
        if field_name not in candidate:
            errors.append(_format_error(path, mod_ref, f"missing field '{field_name}'"))
    if errors:
        return errors

    mod_id = candidate["id"]
    if not isinstance(mod_id, str) or not ID_RE.fullmatch(mod_id):
        errors.append(
            _format_error(path, mod_ref, f"invalid id {mod_id!r}; expected lowercase kebab-case")
        )

    errors.extend(_validate_string_field(candidate, "name", path, mod_ref))
    errors.extend(_validate_string_field(candidate, "engine_notes", path, mod_ref))
    errors.extend(_validate_string_field(candidate, "source_url", path, mod_ref))
    errors.extend(_validate_string_field(candidate, "evidence_notes", path, mod_ref))
    errors.extend(_validate_string_field(candidate, "thematic_reason", path, mod_ref))
    errors.extend(_validate_string_field(candidate, "promotion_notes", path, mod_ref))
    errors.extend(_validate_string_field(candidate, "last_reviewed", path, mod_ref))

    if candidate["candidate_status"] not in CANDIDATE_STATUS:
        errors.append(
            _format_error(path, mod_ref, f"invalid candidate_status {candidate['candidate_status']!r}")
        )
    if candidate["thematic_bucket"] not in THEMATIC_BUCKETS:
        errors.append(
            _format_error(path, mod_ref, f"invalid thematic_bucket {candidate['thematic_bucket']!r}")
        )
    if candidate["source_type"] not in SOURCE_TYPES:
        errors.append(_format_error(path, mod_ref, f"invalid source_type {candidate['source_type']!r}"))
    if candidate["source_confidence"] not in SOURCE_CONFIDENCE:
        errors.append(
            _format_error(path, mod_ref, f"invalid source_confidence {candidate['source_confidence']!r}")
        )
    if candidate["compatibility_status"] not in COMPATIBILITY_STATUS:
        errors.append(
            _format_error(
                path,
                mod_ref,
                f"invalid compatibility_status {candidate['compatibility_status']!r}",
            )
        )
    if candidate["risk_level"] not in RISK_LEVELS:
        errors.append(_format_error(path, mod_ref, f"invalid risk_level {candidate['risk_level']!r}"))
    if candidate["promotion_target"] not in PROMOTION_TARGETS:
        errors.append(
            _format_error(path, mod_ref, f"invalid promotion_target {candidate['promotion_target']!r}")
        )

    intended_editions = candidate["intended_editions"]
    if not isinstance(intended_editions, list) or not intended_editions:
        errors.append(_format_error(path, mod_ref, "field 'intended_editions' must be a non-empty list"))
    elif any(not isinstance(edition, str) for edition in intended_editions):
        errors.append(_format_error(path, mod_ref, "field 'intended_editions' must be list[str]"))
    else:
        invalid_editions = [edition for edition in intended_editions if edition not in INTENDED_EDITIONS]
        if invalid_editions:
            errors.append(
                _format_error(path, mod_ref, f"invalid intended_editions values {invalid_editions!r}")
            )

    for field_name in ("reviewed_by", "related_manifest_ids"):
        value = candidate[field_name]
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            errors.append(_format_error(path, mod_ref, f"field '{field_name}' must be list[str]"))

    return errors


def load_sourced_candidates(path: Path) -> list[dict]:
    data = load_meta_document(path)
    candidates = data.get("sourced_candidates")
    if not isinstance(candidates, list):
        raise ValueError(f"Top-level key 'sourced_candidates' must be a list: {path}")
    return candidates


def validate_sourced_mods(path: Path) -> tuple[list[dict], list[str]]:
    try:
        candidates = load_sourced_candidates(path)
    except ValueError as exc:
        return [], [f"[ERROR] {exc}"]

    errors: list[str] = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            errors.append(f"[ERROR] {path} :: <entry> :: non-object entry in sourced_candidates")
            continue
        errors.extend(validate_candidate(candidate, path))
    return candidates, errors
