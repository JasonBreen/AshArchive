from __future__ import annotations

from datetime import date
from pathlib import Path

from .manifest import load_meta_document
from .validation import ID_RE, _format_error, _is_placeholder, _is_valid_url

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
EVIDENCED_COMPATIBILITY_STATUS = {
    "openmw-compatible",
    "mwse-compatible",
    "both-compatible",
    "incompatible",
}
RISK_LEVELS = {"low", "medium", "high", "unknown"}
PROMOTION_TARGETS = {"openmw", "mwse", "both", "neither", "undecided"}
STRING_FIELDS = {
    "name",
    "engine_notes",
    "source_url",
    "evidence_notes",
    "thematic_reason",
    "promotion_notes",
    "last_reviewed",
}


def _mod_ref(candidate: dict) -> str:
    mod_id = candidate.get("id")
    mod_name = candidate.get("name")
    if isinstance(mod_id, str) and mod_id:
        return mod_id
    if isinstance(mod_name, str) and mod_name:
        return mod_name
    return "<missing-id>"


def _validate_enum(
    candidate: dict,
    field_name: str,
    allowed: set[str],
    path: Path,
    mod_ref: str,
) -> list[str]:
    value = candidate[field_name]
    if not isinstance(value, str) or value not in allowed:
        return [_format_error(path, mod_ref, f"invalid {field_name} {value!r}")]
    return []


def _has_review(candidate: dict) -> bool:
    reviewers = candidate.get("reviewed_by")
    return (
        isinstance(reviewers, list)
        and any(
            isinstance(reviewer, str) and not _is_placeholder(reviewer) for reviewer in reviewers
        )
        and isinstance(candidate.get("last_reviewed"), str)
        and bool(candidate["last_reviewed"].strip())
    )


def _validate_review_fields(candidate: dict, path: Path, mod_ref: str) -> list[str]:
    errors: list[str] = []
    reviewed_by = candidate["reviewed_by"]
    if not isinstance(reviewed_by, list) or any(
        not isinstance(reviewer, str) or _is_placeholder(reviewer) for reviewer in reviewed_by
    ):
        errors.append(
            _format_error(path, mod_ref, "field 'reviewed_by' must be non-placeholder list[str]")
        )
    elif len(reviewed_by) != len(set(reviewed_by)):
        errors.append(_format_error(path, mod_ref, "field 'reviewed_by' contains duplicates"))

    last_reviewed = candidate["last_reviewed"]
    if isinstance(last_reviewed, str) and last_reviewed:
        try:
            parsed = date.fromisoformat(last_reviewed)
        except ValueError:
            parsed = None
        if parsed is None or parsed.isoformat() != last_reviewed:
            errors.append(_format_error(path, mod_ref, "field 'last_reviewed' must use YYYY-MM-DD"))
    return errors


def _validate_lists(candidate: dict, path: Path, mod_ref: str) -> list[str]:
    errors: list[str] = []
    intended_editions = candidate["intended_editions"]
    if not isinstance(intended_editions, list) or not intended_editions:
        errors.append(
            _format_error(path, mod_ref, "field 'intended_editions' must be a non-empty list")
        )
    elif any(not isinstance(edition, str) for edition in intended_editions):
        errors.append(_format_error(path, mod_ref, "field 'intended_editions' must be list[str]"))
    else:
        invalid_editions = [
            edition for edition in intended_editions if edition not in INTENDED_EDITIONS
        ]
        if invalid_editions:
            errors.append(
                _format_error(
                    path, mod_ref, f"invalid intended_editions values {invalid_editions!r}"
                )
            )
        if len(intended_editions) != len(set(intended_editions)):
            errors.append(
                _format_error(path, mod_ref, "field 'intended_editions' contains duplicates")
            )

    related_manifest_ids = candidate["related_manifest_ids"]
    if not isinstance(related_manifest_ids, list) or any(
        not isinstance(manifest_id, str) for manifest_id in related_manifest_ids
    ):
        errors.append(
            _format_error(path, mod_ref, "field 'related_manifest_ids' must be list[str]")
        )
    else:
        if len(related_manifest_ids) != len(set(related_manifest_ids)):
            errors.append(
                _format_error(path, mod_ref, "field 'related_manifest_ids' contains duplicates")
            )
        for manifest_id in related_manifest_ids:
            if not ID_RE.fullmatch(manifest_id):
                errors.append(
                    _format_error(
                        path,
                        mod_ref,
                        f"field 'related_manifest_ids' has malformed reference {manifest_id!r}",
                    )
                )
    return errors


def _validate_source_url_consistency(candidate: dict, path: Path, mod_ref: str) -> list[str]:
    errors: list[str] = []
    source_url = candidate["source_url"]
    if isinstance(source_url, str) and source_url.strip() and not _is_valid_url(source_url):
        errors.append(
            _format_error(
                path, mod_ref, f"malformed source_url {source_url!r}; expected http(s) URL"
            )
        )
    return errors


def _validate_source_confidence_consistency(candidate: dict, path: Path, mod_ref: str) -> list[str]:
    errors: list[str] = []
    source_confidence = candidate["source_confidence"]
    source_url = candidate["source_url"]
    if source_confidence == "verified":
        if (
            not isinstance(source_url, str)
            or not source_url.strip()
            or not _is_valid_url(source_url)
        ):
            errors.append(
                _format_error(
                    path, mod_ref, "source_confidence 'verified' requires a valid source_url"
                )
            )
        if candidate["source_type"] == "unknown":
            errors.append(
                _format_error(
                    path, mod_ref, "source_confidence 'verified' cannot use source_type 'unknown'"
                )
            )
        if _is_placeholder(candidate["evidence_notes"]):
            errors.append(
                _format_error(path, mod_ref, "source_confidence 'verified' requires evidence_notes")
            )
    return errors


def _validate_compatibility_status_consistency(
    candidate: dict, path: Path, mod_ref: str
) -> list[str]:
    errors: list[str] = []
    compatibility_status = candidate["compatibility_status"]
    if compatibility_status in EVIDENCED_COMPATIBILITY_STATUS:
        if _is_placeholder(candidate["evidence_notes"]) or _is_placeholder(
            candidate["engine_notes"]
        ):
            errors.append(
                _format_error(
                    path,
                    mod_ref,
                    f"compatibility_status {compatibility_status!r} requires evidence and engine notes",
                )
            )
        if not _has_review(candidate):
            errors.append(
                _format_error(
                    path,
                    mod_ref,
                    f"compatibility_status {compatibility_status!r} requires review information",
                )
            )

    intended_editions = candidate["intended_editions"]
    if isinstance(intended_editions, list):
        required_compatibility_editions = {
            "openmw-compatible": {"openmw"},
            "mwse-compatible": {"mwse"},
            "both-compatible": {"openmw", "mwse"},
        }.get(compatibility_status, set())
        missing = required_compatibility_editions - set(intended_editions)
        if missing:
            errors.append(
                _format_error(
                    path,
                    mod_ref,
                    f"compatibility_status {compatibility_status!r} contradicts intended_editions",
                )
            )
    return errors


def _validate_promotion_target_consistency(candidate: dict, path: Path, mod_ref: str) -> list[str]:
    errors: list[str] = []
    intended_editions = candidate["intended_editions"]
    if isinstance(intended_editions, list):
        promotion_target = candidate["promotion_target"]
        required_target_editions = {
            "openmw": {"openmw"},
            "mwse": {"mwse"},
            "both": {"openmw", "mwse"},
        }.get(promotion_target, set())
        if required_target_editions - set(intended_editions):
            errors.append(
                _format_error(
                    path,
                    mod_ref,
                    f"promotion_target {promotion_target!r} contradicts intended_editions",
                )
            )
    return errors


def _validate_candidate_status_consistency(candidate: dict, path: Path, mod_ref: str) -> list[str]:
    errors: list[str] = []
    candidate_status = candidate["candidate_status"]
    if candidate_status == "promoted":
        if candidate["promotion_target"] in {"neither", "undecided"}:
            errors.append(
                _format_error(
                    path,
                    mod_ref,
                    "candidate_status 'promoted' requires a concrete promotion_target",
                )
            )
        related_ids = candidate["related_manifest_ids"]
        if not isinstance(related_ids, list) or not related_ids:
            errors.append(
                _format_error(
                    path, mod_ref, "candidate_status 'promoted' requires related_manifest_ids"
                )
            )
        if _is_placeholder(candidate["promotion_notes"]):
            errors.append(
                _format_error(path, mod_ref, "candidate_status 'promoted' requires promotion_notes")
            )
        if not _has_review(candidate):
            errors.append(
                _format_error(
                    path, mod_ref, "candidate_status 'promoted' requires review information"
                )
            )
    elif candidate_status in {"rejected", "superseded"}:
        if _is_placeholder(candidate["promotion_notes"]):
            errors.append(
                _format_error(
                    path,
                    mod_ref,
                    f"candidate_status {candidate_status!r} requires promotion_notes",
                )
            )
        if not _has_review(candidate):
            errors.append(
                _format_error(
                    path,
                    mod_ref,
                    f"candidate_status {candidate_status!r} requires review information",
                )
            )
    return errors


def _validate_candidate_consistency(candidate: dict, path: Path, mod_ref: str) -> list[str]:
    errors: list[str] = []
    errors.extend(_validate_source_url_consistency(candidate, path, mod_ref))
    errors.extend(_validate_source_confidence_consistency(candidate, path, mod_ref))
    errors.extend(_validate_compatibility_status_consistency(candidate, path, mod_ref))
    errors.extend(_validate_promotion_target_consistency(candidate, path, mod_ref))
    errors.extend(_validate_candidate_status_consistency(candidate, path, mod_ref))
    return errors


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

    for field_name in STRING_FIELDS:
        if not isinstance(candidate[field_name], str):
            errors.append(_format_error(path, mod_ref, f"field '{field_name}' must be a string"))
    if isinstance(candidate["name"], str) and not candidate["name"].strip():
        errors.append(_format_error(path, mod_ref, "field 'name' must not be blank"))

    errors.extend(_validate_enum(candidate, "candidate_status", CANDIDATE_STATUS, path, mod_ref))
    errors.extend(_validate_enum(candidate, "thematic_bucket", THEMATIC_BUCKETS, path, mod_ref))
    errors.extend(_validate_enum(candidate, "source_type", SOURCE_TYPES, path, mod_ref))
    errors.extend(_validate_enum(candidate, "source_confidence", SOURCE_CONFIDENCE, path, mod_ref))
    errors.extend(
        _validate_enum(candidate, "compatibility_status", COMPATIBILITY_STATUS, path, mod_ref)
    )
    errors.extend(_validate_enum(candidate, "risk_level", RISK_LEVELS, path, mod_ref))
    errors.extend(_validate_enum(candidate, "promotion_target", PROMOTION_TARGETS, path, mod_ref))
    errors.extend(_validate_lists(candidate, path, mod_ref))
    errors.extend(_validate_review_fields(candidate, path, mod_ref))

    # Consistency checks assume the relevant scalar enum and string fields are well-typed.
    if not any("must be a string" in error or "invalid " in error for error in errors):
        errors.extend(_validate_candidate_consistency(candidate, path, mod_ref))
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
    seen_ids: set[str] = set()
    duplicate_ids: set[str] = set()
    for candidate in candidates:
        if not isinstance(candidate, dict):
            errors.append(f"[ERROR] {path} :: <entry> :: non-object entry in sourced_candidates")
            continue
        candidate_id = candidate.get("id")
        if isinstance(candidate_id, str):
            if candidate_id in seen_ids:
                duplicate_ids.add(candidate_id)
            seen_ids.add(candidate_id)
        errors.extend(validate_candidate(candidate, path))
    for candidate_id in sorted(duplicate_ids):
        errors.append(_format_error(path, candidate_id, "duplicate id in sourced candidates"))
    return candidates, errors
