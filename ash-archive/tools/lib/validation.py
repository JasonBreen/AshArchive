from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Collection, Mapping
from datetime import date
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlsplit

from .manifest import load_meta_document, load_mods
from .paths import categories_path

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLACEHOLDER_RE = re.compile(
    r"\b(?:tbd|todo|placeholder|unknown|unverified|"
    r"needs? (?:verification|testing|review|confirmation)|"
    r"pending (?:verification|review|testing)|testing (?:is )?pending|"
    r"not (?:yet )?tested|untested|no [^.\n]*test evidence [^.\n]*recorded)\b",
    re.IGNORECASE,
)
CROSS = {
    "shared",
    "openmw-only",
    "mwse-only",
    "equivalent-needed",
    "different-implementation",
    "rejected-in-openmw",
    "rejected-in-mwse",
}
STATUS = {"planned", "testing", "accepted", "rejected", "needs-patch", "deprecated"}
ENGINE_BY_EDITION = {
    "openmw": {"openmw", "vanilla", "both", "unknown"},
    "mwse": {"mwse", "mcp", "mge-xe", "vanilla", "both", "unknown"},
}
REQ_FIELDS = [
    "id",
    "name",
    "category",
    "edition",
    "cross_edition_status",
    "status",
    "engine",
    "source",
    "url",
    "archive_name",
    "version",
    "plugin_files",
    "requires",
    "conflicts",
    "load_after",
    "load_before",
    "patch_notes",
    "testing_notes",
    "decision_reason",
    "priority",
]
STR_FIELDS = [
    "name",
    "category",
    "edition",
    "cross_edition_status",
    "status",
    "source",
    "url",
    "archive_name",
    "version",
    "patch_notes",
    "testing_notes",
    "decision_reason",
]
LIST_FIELDS = ["plugin_files", "requires", "conflicts", "load_after", "load_before"]
REFERENCE_FIELDS = ["requires", "conflicts", "load_after", "load_before"]
VERIFIED_MANIFEST_STATUSES = {"testing", "accepted"}
REVIEWED_MANIFEST_STATUSES = {*VERIFIED_MANIFEST_STATUSES, "rejected"}
RATIONALE_REQUIRED_STATUSES = {"rejected", "needs-patch", "deprecated"}
CROSS_STATUS_FORBIDDEN_BY_EDITION = {
    "openmw": {"mwse-only", "rejected-in-openmw"},
    "mwse": {"openmw-only", "rejected-in-mwse"},
}


def _format_error(path: Path, mod_ref: str, detail: str) -> str:
    return f"[ERROR] {path} :: {mod_ref} :: {detail}"


@lru_cache(maxsize=1)
def _allowed_categories() -> frozenset[str]:
    data = load_meta_document(categories_path())
    cats = data.get("categories", [])
    if not isinstance(cats, list):
        raise ValueError(f"Top-level key 'categories' must be a list: {categories_path()}")
    bad = [category for category in cats if not isinstance(category, str)]
    if bad:
        raise ValueError(f"All categories must be strings in: {categories_path()}")
    return frozenset(cats)


def _mod_ref(mod: dict) -> str:
    mod_id = mod.get("id")
    mod_name = mod.get("name")
    if isinstance(mod_id, str) and mod_id:
        return mod_id
    if isinstance(mod_name, str) and mod_name:
        return mod_name
    return "<missing-id>"


def _is_placeholder(value: object) -> bool:
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    return not stripped or bool(PLACEHOLDER_RE.search(stripped))


def _is_valid_url(value: str) -> bool:
    if not value or any(character.isspace() for character in value):
        return False
    try:
        parsed = urlsplit(value)
        # Accessing port rejects malformed values such as ``:not-a-port``.
        _ = parsed.port
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc) and bool(parsed.hostname)


def _validate_enum_fields(mod: dict, path: Path, mod_ref: str, expected_edition: str) -> list[str]:
    errors: list[str] = []
    mod_id = mod.get("id")
    if not isinstance(mod_id, str) or not ID_RE.fullmatch(mod_id):
        errors.append(
            _format_error(
                path,
                mod_ref,
                f"invalid id {mod_id!r}; expected lowercase kebab-case like 'patch-for-purists'",
            )
        )

    edition = mod["edition"]
    if not isinstance(edition, str) or edition != expected_edition:
        errors.append(
            _format_error(
                path,
                mod_ref,
                f"edition mismatch: found {edition!r}, expected {expected_edition!r}",
            )
        )

    cross_edition_status = mod["cross_edition_status"]
    if not isinstance(cross_edition_status, str) or cross_edition_status not in CROSS:
        errors.append(
            _format_error(
                path,
                mod_ref,
                f"invalid cross_edition_status {cross_edition_status!r}",
            )
        )
    elif cross_edition_status in CROSS_STATUS_FORBIDDEN_BY_EDITION[expected_edition]:
        errors.append(
            _format_error(
                path,
                mod_ref,
                f"cross_edition_status {cross_edition_status!r} is incompatible with "
                f"edition {expected_edition!r}",
            )
        )

    status = mod["status"]
    if not isinstance(status, str) or status not in STATUS:
        errors.append(_format_error(path, mod_ref, f"invalid status {status!r}"))

    category = mod["category"]
    allowed = _allowed_categories()
    if not isinstance(category, str) or category not in allowed:
        errors.append(
            _format_error(
                path,
                mod_ref,
                f"invalid category {category!r}; expected one of shared/categories.control.meta",
            )
        )
    return errors


def _validate_engine_field(mod: dict, path: Path, mod_ref: str, expected_edition: str) -> list[str]:
    engine = mod["engine"]
    if not isinstance(engine, list) or any(not isinstance(value, str) for value in engine):
        return [_format_error(path, mod_ref, "field 'engine' must be list[str]")]
    if not engine:
        return [_format_error(path, mod_ref, "engine must be a non-empty list")]

    errors: list[str] = []
    allowed = ENGINE_BY_EDITION[expected_edition]
    invalid = [value for value in engine if value not in allowed]
    if invalid:
        errors.append(
            _format_error(
                path,
                mod_ref,
                f"invalid engine values {invalid!r} for edition {expected_edition!r}",
            )
        )

    if len(engine) != len(set(engine)):
        errors.append(_format_error(path, mod_ref, "engine contains duplicate values"))
    unique_values = set(engine)
    if "unknown" in unique_values and len(unique_values) > 1:
        errors.append(
            _format_error(path, mod_ref, "engine cannot combine 'unknown' with other values")
        )
    if "both" in unique_values and len(unique_values) > 1:
        errors.append(
            _format_error(path, mod_ref, "engine cannot combine 'both' with other values")
        )
    return errors


def _validate_field_types(mod: dict, path: Path, mod_ref: str, expected_edition: str) -> list[str]:
    errors: list[str] = []
    errors.extend(_validate_engine_field(mod, path, mod_ref, expected_edition))
    for field_name in LIST_FIELDS:
        value = mod[field_name]
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            errors.append(_format_error(path, mod_ref, f"field '{field_name}' must be list[str]"))
    for field_name in STR_FIELDS:
        if not isinstance(mod[field_name], str):
            errors.append(_format_error(path, mod_ref, f"field '{field_name}' must be a string"))
    if isinstance(mod["name"], str) and not mod["name"].strip():
        errors.append(_format_error(path, mod_ref, "field 'name' must not be blank"))
    priority = mod["priority"]
    if isinstance(priority, bool) or not isinstance(priority, int):
        errors.append(_format_error(path, mod_ref, "field 'priority' must be integer"))
    elif priority < 1:
        errors.append(_format_error(path, mod_ref, "field 'priority' must be a positive integer"))

    source_reference = mod.get("source_reference")
    if source_reference is not None and (
        not isinstance(source_reference, str) or not ID_RE.fullmatch(source_reference)
    ):
        errors.append(
            _format_error(
                path,
                mod_ref,
                "field 'source_reference' must be a lowercase kebab-case source id",
            )
        )
    return errors


def _validate_url_and_evidence(mod: dict, path: Path, mod_ref: str) -> list[str]:
    errors: list[str] = []
    url = mod["url"]
    if isinstance(url, str) and url.strip() and not _is_placeholder(url) and not _is_valid_url(url):
        errors.append(_format_error(path, mod_ref, f"malformed url {url!r}; expected http(s) URL"))

    status = mod["status"]
    if status in RATIONALE_REQUIRED_STATUSES and _is_placeholder(mod["decision_reason"]):
        errors.append(
            _format_error(
                path,
                mod_ref,
                f"status {status!r} requires non-placeholder 'decision_reason' rationale",
            )
        )
    if not isinstance(status, str) or status not in VERIFIED_MANIFEST_STATUSES:
        return errors

    source_reference = mod.get("source_reference")
    if status == "accepted" and not (
        isinstance(source_reference, str) and ID_RE.fullmatch(source_reference)
    ):
        errors.append(_format_error(path, mod_ref, "status 'accepted' requires source_reference"))
    if source_reference is None:
        for field_name in ("source", "url"):
            if _is_placeholder(mod[field_name]):
                errors.append(
                    _format_error(
                        path,
                        mod_ref,
                        f"status {status!r} requires a verified '{field_name}' or source_reference",
                    )
                )
    for field_name in ("archive_name", "version", "testing_notes", "decision_reason"):
        if _is_placeholder(mod[field_name]):
            errors.append(
                _format_error(
                    path,
                    mod_ref,
                    f"status {status!r} requires non-placeholder '{field_name}' evidence",
                )
            )
    return errors


def _validate_review_metadata(mod: dict, path: Path, mod_ref: str) -> list[str]:
    errors: list[str] = []
    reviewed_by = mod.get("reviewed_by", [])
    if not isinstance(reviewed_by, list) or any(
        not isinstance(reviewer, str) or _is_placeholder(reviewer) for reviewer in reviewed_by
    ):
        errors.append(
            _format_error(path, mod_ref, "field 'reviewed_by' must be non-placeholder list[str]")
        )
        reviewed_by = []
    elif len(reviewed_by) != len(set(reviewed_by)):
        errors.append(_format_error(path, mod_ref, "field 'reviewed_by' contains duplicates"))

    last_reviewed = mod.get("last_reviewed", "")
    valid_review_date = False
    if not isinstance(last_reviewed, str):
        errors.append(_format_error(path, mod_ref, "field 'last_reviewed' must be a string"))
    elif last_reviewed:
        try:
            valid_review_date = date.fromisoformat(last_reviewed).isoformat() == last_reviewed
        except ValueError:
            valid_review_date = False
        if not valid_review_date:
            errors.append(_format_error(path, mod_ref, "field 'last_reviewed' must use YYYY-MM-DD"))

    status = mod.get("status")
    if status in REVIEWED_MANIFEST_STATUSES:
        if not reviewed_by:
            errors.append(_format_error(path, mod_ref, f"status {status!r} requires reviewed_by"))
        if not valid_review_date:
            errors.append(_format_error(path, mod_ref, f"status {status!r} requires last_reviewed"))
    return errors


def validate_mod(mod: dict, path: Path, expected_edition: str) -> list[str]:
    errors: list[str] = []
    mod_ref = _mod_ref(mod)
    for field_name in REQ_FIELDS:
        if field_name not in mod:
            errors.append(_format_error(path, mod_ref, f"missing field '{field_name}'"))
    if errors:
        return errors
    errors.extend(_validate_enum_fields(mod, path, mod_ref, expected_edition))
    errors.extend(_validate_field_types(mod, path, mod_ref, expected_edition))
    errors.extend(_validate_url_and_evidence(mod, path, mod_ref))
    errors.extend(_validate_review_metadata(mod, path, mod_ref))
    return errors


def _validate_uniqueness(mods: list[dict], path: Path) -> list[str]:
    errors: list[str] = []
    ids: dict[str, list[str]] = defaultdict(list)
    priorities: dict[tuple[str, int], list[str]] = defaultdict(list)
    for mod in mods:
        if not isinstance(mod, dict):
            continue
        mod_id = mod.get("id")
        if isinstance(mod_id, str):
            ids[mod_id].append(_mod_ref(mod))
        category = mod.get("category")
        priority = mod.get("priority")
        if (
            isinstance(category, str)
            and isinstance(priority, int)
            and not isinstance(priority, bool)
        ):
            priorities[(category, priority)].append(_mod_ref(mod))

    for mod_id, references in sorted(ids.items()):
        if len(references) > 1:
            errors.append(_format_error(path, mod_id, "duplicate id in manifest"))
    for (category, priority), references in sorted(priorities.items()):
        if len(references) > 1:
            errors.append(
                _format_error(
                    path,
                    ", ".join(references),
                    f"duplicate priority {priority} within category {category!r}",
                )
            )
    return errors


def _validate_references(mods: list[dict], path: Path) -> list[str]:
    errors: list[str] = []
    known_ids = {
        mod["id"] for mod in mods if isinstance(mod, dict) and isinstance(mod.get("id"), str)
    }
    for mod in mods:
        if not isinstance(mod, dict):
            continue
        mod_ref = _mod_ref(mod)
        mod_id = mod.get("id")
        valid_lists: dict[str, list[str]] = {}
        for field_name in REFERENCE_FIELDS:
            value = mod.get(field_name)
            if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                continue
            valid_lists[field_name] = value
            if len(value) != len(set(value)):
                errors.append(
                    _format_error(
                        path, mod_ref, f"field '{field_name}' contains duplicate references"
                    )
                )
            for reference in value:
                if not ID_RE.fullmatch(reference):
                    errors.append(
                        _format_error(
                            path,
                            mod_ref,
                            f"field '{field_name}' has malformed reference {reference!r}",
                        )
                    )
                elif reference == mod_id:
                    errors.append(
                        _format_error(
                            path, mod_ref, f"field '{field_name}' cannot reference itself"
                        )
                    )
                elif reference not in known_ids:
                    errors.append(
                        _format_error(
                            path,
                            mod_ref,
                            f"field '{field_name}' references nonexistent manifest id {reference!r}",
                        )
                    )

        requires = set(valid_lists.get("requires", []))
        conflicts = set(valid_lists.get("conflicts", []))
        contradictory = sorted(requires & conflicts)
        if contradictory:
            errors.append(
                _format_error(
                    path,
                    mod_ref,
                    f"same ids cannot appear in both requires and conflicts: {contradictory!r}",
                )
            )
        load_after = set(valid_lists.get("load_after", []))
        load_before = set(valid_lists.get("load_before", []))
        contradictory = sorted(load_after & load_before)
        if contradictory:
            errors.append(
                _format_error(
                    path,
                    mod_ref,
                    f"same ids cannot appear in both load_after and load_before: {contradictory!r}",
                )
            )
    return errors


def validate_manifest(path: Path, edition: str) -> list[str]:
    if edition not in ENGINE_BY_EDITION:
        return [f"[ERROR] {path} :: <manifest> :: unsupported edition {edition!r}"]
    try:
        mods = load_mods(path)
    except ValueError as exc:
        return [f"[ERROR] {exc}"]
    if not mods:
        return [f"[ERROR] {path} :: <manifest> :: no mods defined"]
    errors: list[str] = []
    for mod in mods:
        if not isinstance(mod, dict):
            errors.append(f"[ERROR] {path} :: <manifest> :: non-object entry in mods list")
            continue
        errors.extend(validate_mod(mod, path, edition))
    errors.extend(_validate_uniqueness(mods, path))
    errors.extend(_validate_references(mods, path))
    return errors


def _check_manifest_to_source(
    mods_by_edition: Mapping[str, list[dict]],
    manifest_paths: Mapping[str, Path],
    candidate_by_id: dict[str, dict],
    source_path: Path,
    selected_editions: set[str],
) -> list[str]:
    errors: list[str] = []
    for edition in selected_editions:
        path = manifest_paths[edition]
        for mod in mods_by_edition.get(edition, []):
            if not isinstance(mod, dict):
                continue
            source_reference = mod.get("source_reference")
            if not isinstance(source_reference, str) or not ID_RE.fullmatch(source_reference):
                continue
            mod_ref = _mod_ref(mod)
            candidate = candidate_by_id.get(source_reference)
            if candidate is None:
                errors.append(
                    _format_error(
                        path,
                        mod_ref,
                        f"source_reference {source_reference!r} does not exist in {source_path}",
                    )
                )
                continue

            if mod.get("name") != candidate.get("name"):
                errors.append(
                    _format_error(
                        path,
                        mod_ref,
                        "manifest name does not match canonical source record name "
                        f"{candidate.get('name')!r}",
                    )
                )
            intended_editions = candidate.get("intended_editions")
            if isinstance(intended_editions, list) and edition not in intended_editions:
                errors.append(
                    _format_error(
                        path,
                        mod_ref,
                        f"source record does not include edition {edition!r} in intended_editions",
                    )
                )
            if candidate.get("candidate_status") in {"rejected", "superseded"}:
                errors.append(
                    _format_error(
                        path,
                        mod_ref,
                        f"source_reference points to {candidate.get('candidate_status')!r} candidate",
                    )
                )
            related_manifest_ids = candidate.get("related_manifest_ids")
            if isinstance(related_manifest_ids, list) and mod.get("id") not in related_manifest_ids:
                errors.append(
                    _format_error(
                        path,
                        mod_ref,
                        "source record related_manifest_ids does not link back to this manifest id",
                    )
                )

            manifest_source = mod.get("source")
            if isinstance(manifest_source, str) and not _is_placeholder(manifest_source):
                if manifest_source != candidate.get("source_type"):
                    errors.append(
                        _format_error(
                            path,
                            mod_ref,
                            f"manifest source {manifest_source!r} does not match canonical "
                            f"source_type {candidate.get('source_type')!r}",
                        )
                    )
            manifest_url = mod.get("url")
            if isinstance(manifest_url, str) and not _is_placeholder(manifest_url):
                if manifest_url != candidate.get("source_url"):
                    errors.append(
                        _format_error(
                            path,
                            mod_ref,
                            "manifest url does not match canonical source_url",
                        )
                    )

            status = mod.get("status")
            if status in VERIFIED_MANIFEST_STATUSES:
                if candidate.get("source_confidence") != "verified":
                    errors.append(
                        _format_error(
                            path,
                            mod_ref,
                            f"status {status!r} requires source_confidence 'verified'",
                        )
                    )
                if status == "accepted":
                    if candidate.get("candidate_status") != "promoted":
                        errors.append(
                            _format_error(
                                path,
                                mod_ref,
                                "status 'accepted' requires source candidate_status 'promoted'",
                            )
                        )
                    if candidate.get("promotion_target") not in {edition, "both"}:
                        errors.append(
                            _format_error(
                                path,
                                mod_ref,
                                "status 'accepted' requires source promotion_target to include "
                                f"edition {edition!r}",
                            )
                        )
                    compatible_statuses = {
                        "openmw": {"openmw-compatible", "both-compatible"},
                        "mwse": {"mwse-compatible", "both-compatible"},
                    }
                    if candidate.get("compatibility_status") not in compatible_statuses[edition]:
                        errors.append(
                            _format_error(
                                path,
                                mod_ref,
                                f"status 'accepted' lacks compatible evidence for edition {edition!r}",
                            )
                        )
    return errors


def _check_source_to_manifest(
    candidates: list[dict],
    manifests_by_id: dict[str, list[tuple[str, dict]]],
    source_path: Path,
    selected_editions: set[str],
) -> list[str]:
    errors: list[str] = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        candidate_id = candidate.get("id")
        related_ids = candidate.get("related_manifest_ids")
        if not isinstance(candidate_id, str) or not isinstance(related_ids, list):
            continue
        for manifest_id in related_ids:
            if not isinstance(manifest_id, str) or not ID_RE.fullmatch(manifest_id):
                continue
            matches = manifests_by_id.get(manifest_id, [])
            if not matches:
                errors.append(
                    _format_error(
                        source_path,
                        candidate_id,
                        f"related_manifest_ids references nonexistent manifest id {manifest_id!r}",
                    )
                )
                continue
            selected_matches = [
                (edition, mod) for edition, mod in matches if edition in selected_editions
            ]
            if not selected_matches:
                continue
            intended_editions = candidate.get("intended_editions")
            eligible_matches = [
                (edition, mod)
                for edition, mod in selected_matches
                if not isinstance(intended_editions, list) or edition in intended_editions
            ]
            if not eligible_matches:
                found_editions = sorted({edition for edition, _ in selected_matches})
                errors.append(
                    _format_error(
                        source_path,
                        candidate_id,
                        f"related manifest id {manifest_id!r} resolves only to unintended "
                        f"editions {found_editions!r}",
                    )
                )
                continue
            for edition, mod in eligible_matches:
                if mod.get("source_reference") != candidate_id:
                    errors.append(
                        _format_error(
                            source_path,
                            candidate_id,
                            f"manifest {edition!r} id {manifest_id!r} does not link back with "
                            f"source_reference {candidate_id!r}",
                        )
                    )
    return errors


def validate_source_references(
    mods_by_edition: Mapping[str, list[dict]],
    manifest_paths: Mapping[str, Path],
    candidates: list[dict],
    source_path: Path,
    editions: Collection[str] | None = None,
) -> list[str]:
    """Validate optional links between edition manifests and canonical source records."""
    selected_editions = set(editions or mods_by_edition)
    candidate_by_id = {
        candidate["id"]: candidate
        for candidate in candidates
        if isinstance(candidate, dict) and isinstance(candidate.get("id"), str)
    }
    manifests_by_id: dict[str, list[tuple[str, dict]]] = defaultdict(list)
    for edition, mods in mods_by_edition.items():
        for mod in mods:
            if isinstance(mod, dict) and isinstance(mod.get("id"), str):
                manifests_by_id[mod["id"]].append((edition, mod))

    errors: list[str] = []
    errors.extend(
        _check_manifest_to_source(
            mods_by_edition, manifest_paths, candidate_by_id, source_path, selected_editions
        )
    )
    errors.extend(
        _check_source_to_manifest(candidates, manifests_by_id, source_path, selected_editions)
    )
    return errors
