from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from .manifest import load_mods, load_yaml
from .paths import categories_path

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
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
    "source",
    "url",
    "archive_name",
    "version",
    "patch_notes",
    "testing_notes",
    "decision_reason",
]
LIST_FIELDS = ["plugin_files", "requires", "conflicts", "load_after", "load_before"]


def _format_error(path: Path, mod_ref: str, detail: str) -> str:
    return f"[ERROR] {path} :: {mod_ref} :: {detail}"


@lru_cache(maxsize=1)
def _allowed_categories() -> frozenset[str]:
    data = load_yaml(categories_path())
    cats = data.get("categories", [])
    if not isinstance(cats, list):
        raise ValueError(f"Top-level key 'categories' must be a list: {categories_path()}")
    bad = [c for c in cats if not isinstance(c, str)]
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
    if mod["edition"] != expected_edition:
        errors.append(
            _format_error(
                path,
                mod_ref,
                f"edition mismatch: found {mod['edition']!r}, expected {expected_edition!r}",
            )
        )
    if mod["cross_edition_status"] not in CROSS:
        errors.append(
            _format_error(
                path,
                mod_ref,
                f"invalid cross_edition_status {mod['cross_edition_status']!r}",
            )
        )
    if mod["status"] not in STATUS:
        errors.append(_format_error(path, mod_ref, f"invalid status {mod['status']!r}"))
    allowed = _allowed_categories()
    if mod["category"] not in allowed:
        errors.append(
            _format_error(
                path,
                mod_ref,
                f"invalid category {mod['category']!r}; expected one of shared/categories.meta",
            )
        )
    return errors


def _validate_engine_field(mod: dict, path: Path, mod_ref: str, expected_edition: str) -> list[str]:
    errors: list[str] = []
    engine = mod["engine"]
    if not isinstance(engine, list):
        return [_format_error(path, mod_ref, "field 'engine' must be list[str]")]
    if not engine:
        return [_format_error(path, mod_ref, "engine must be a non-empty list")]
    if any(not isinstance(e, str) for e in engine):
        return [_format_error(path, mod_ref, "field 'engine' must be list[str]")]

    allowed = ENGINE_BY_EDITION[expected_edition]
    invalid = [e for e in engine if e not in allowed]
    if invalid:
        errors.append(
            _format_error(
                path,
                mod_ref,
                f"invalid engine values {invalid!r} for edition {expected_edition!r}",
            )
        )

    unique_values = set(engine)
    if "unknown" in unique_values and len(unique_values) > 1:
        errors.append(
            _format_error(
                path,
                mod_ref,
                "engine cannot combine 'unknown' with other values",
            )
        )
    if "both" in unique_values and len(unique_values) > 1:
        errors.append(
            _format_error(
                path,
                mod_ref,
                "engine cannot combine 'both' with other values",
            )
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
    if not isinstance(mod["priority"], int):
        errors.append(_format_error(path, mod_ref, "field 'priority' must be integer"))
    return errors


def validate_mod(mod: dict, path: Path, expected_edition: str) -> list[str]:
    errors = []
    mod_ref = _mod_ref(mod)
    for field_name in REQ_FIELDS:
        if field_name not in mod:
            errors.append(_format_error(path, mod_ref, f"missing field '{field_name}'"))
    if errors:
        return errors
    errors.extend(_validate_enum_fields(mod, path, mod_ref, expected_edition))
    errors.extend(_validate_field_types(mod, path, mod_ref, expected_edition))
    return errors


def validate_manifest(path: Path, edition: str) -> list[str]:
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
    return errors
