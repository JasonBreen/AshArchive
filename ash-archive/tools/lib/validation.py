from __future__ import annotations

import re
from pathlib import Path

from .manifest import load_mods

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
ENGINE = {"openmw", "mwse", "mcp", "mge-xe", "vanilla", "both", "unknown"}
REQ_FIELDS = [
    "id", "name", "category", "edition", "cross_edition_status", "status", "engine",
    "source", "url", "archive_name", "version", "plugin_files", "requires", "conflicts",
    "load_after", "load_before", "patch_notes", "testing_notes", "decision_reason", "priority",
]
STR_FIELDS = [
    "name", "category", "source", "url", "archive_name", "version",
    "patch_notes", "testing_notes", "decision_reason",
]
LIST_FIELDS = ["plugin_files", "requires", "conflicts", "load_after", "load_before"]


def _validate_enum_fields(mod: dict, path: Path, mod_id: str, expected_edition: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(mod["id"], str) or not ID_RE.match(mod["id"]):
        errors.append(f"{path}: mod={mod_id} invalid id; expected lowercase kebab-case")
    if mod["edition"] != expected_edition:
        errors.append(
            f"{path}: mod={mod_id} edition '{mod['edition']}' must be '{expected_edition}'"
        )
    if mod["cross_edition_status"] not in CROSS:
        errors.append(
            f"{path}: mod={mod_id} invalid cross_edition_status '{mod['cross_edition_status']}'"
        )
    if mod["status"] not in STATUS:
        errors.append(f"{path}: mod={mod_id} invalid status '{mod['status']}'")
    return errors


def _validate_field_types(mod: dict, path: Path, mod_id: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(mod["engine"], list) or not mod["engine"]:
        errors.append(f"{path}: mod={mod_id} engine must be a non-empty list")
    elif any(e not in ENGINE for e in mod["engine"]):
        errors.append(f"{path}: mod={mod_id} invalid engine values {mod['engine']}")
    for f in LIST_FIELDS:
        if not isinstance(mod[f], list) or any(not isinstance(x, str) for x in mod[f]):
            errors.append(f"{path}: mod={mod_id} field '{f}' must be list[str]")
    for f in STR_FIELDS:
        if not isinstance(mod[f], str):
            errors.append(f"{path}: mod={mod_id} field '{f}' must be a string")
    if not isinstance(mod["priority"], int):
        errors.append(f"{path}: mod={mod_id} field 'priority' must be integer")
    return errors


def validate_mod(mod: dict, path: Path, expected_edition: str) -> list[str]:
    errors = []
    mod_id = mod.get("id", "<missing-id>")
    for f in REQ_FIELDS:
        if f not in mod:
            errors.append(f"{path}: mod={mod_id} missing field '{f}'")
    if errors:
        return errors
    errors.extend(_validate_enum_fields(mod, path, mod_id, expected_edition))
    errors.extend(_validate_field_types(mod, path, mod_id))
    return errors


def validate_manifest(path: Path, edition: str) -> list[str]:
    mods = load_mods(path)
    if not mods:
        return [f"{path}: no mods defined"]
    errors: list[str] = []
    for mod in mods:
        if not isinstance(mod, dict):
            errors.append(f"{path}: non-object entry in mods list")
            continue
        errors.extend(validate_mod(mod, path, edition))
    return errors
