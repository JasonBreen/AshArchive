from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

# Morrowind Nexus mod-page URL pattern (Wabbajack resolves the file from here)
NEXUS_URL_RE = re.compile(r"^https://www\.nexusmods\.com/morrowind/mods/\d+")

# Source values that map to a supported Wabbajack downloader
WABBAJACK_SOURCES = {"nexus", "github", "modding-openmw", "direct"}

# Archive file-extensions Wabbajack is known to handle
ARCHIVE_EXTENSIONS = {".7z", ".zip", ".rar"}


def _format_error(path: Path, mod_ref: str, detail: str) -> str:
    return f"[ERROR] {path} :: {mod_ref} :: {detail}"


def _format_warning(path: Path, mod_ref: str, detail: str) -> str:
    return f"[WARN] {path} :: {mod_ref} :: {detail}"


def _mod_ref(mod: dict) -> str:
    mod_id = mod.get("id")
    mod_name = mod.get("name")
    if isinstance(mod_id, str) and mod_id:
        return mod_id
    if isinstance(mod_name, str) and mod_name:
        return mod_name
    return "<missing-id>"


def check_mod_wabbajack_readiness(mod: dict, path: Path) -> list[str]:
    """Return error/warning messages for a single mod entry."""
    messages: list[str] = []
    mod_ref = _mod_ref(mod)
    status = mod.get("status", "")
    url = mod.get("url", "")
    archive_name = mod.get("archive_name", "")
    version = mod.get("version", "")
    source = mod.get("source", "")

    # Accepted mods must carry complete download metadata for Wabbajack compilation.
    if status == "accepted":
        if not url:
            messages.append(_format_error(path, mod_ref, "accepted mod has no url"))
        if not archive_name:
            messages.append(_format_error(path, mod_ref, "accepted mod has no archive_name"))
        if not version:
            messages.append(_format_error(path, mod_ref, "accepted mod has no version"))
        if source in ("tbd", "", "unknown"):
            messages.append(
                _format_error(
                    path, mod_ref, f"accepted mod has unresolved source {source!r}"
                )
            )
        elif source not in WABBAJACK_SOURCES:
            messages.append(
                _format_warning(
                    path,
                    mod_ref,
                    f"source {source!r} may not be a supported Wabbajack downloader",
                )
            )

    # Nexus URL format — checked regardless of status so bad URLs are caught early.
    if source == "nexus" and url:
        if not NEXUS_URL_RE.match(url):
            messages.append(
                _format_error(
                    path,
                    mod_ref,
                    f"nexus source has malformed url {url!r}; "
                    "expected https://www.nexusmods.com/morrowind/mods/<id>",
                )
            )

    # Warn when a URL is recorded but the archive name is still missing.
    if url and not archive_name:
        messages.append(
            _format_warning(path, mod_ref, "url is set but archive_name is empty")
        )

    # Warn when an archive_name has an unrecognised extension.
    if archive_name and not any(archive_name.lower().endswith(ext) for ext in ARCHIVE_EXTENSIONS):
        messages.append(
            _format_warning(
                path,
                mod_ref,
                f"archive_name {archive_name!r} does not have a recognised extension "
                "(.7z, .zip, .rar)",
            )
        )

    return messages


def check_duplicate_archive_names(mods: list[dict], path: Path) -> list[str]:
    """Return errors for non-empty archive_name values that appear more than once."""
    messages: list[str] = []
    name_to_refs: dict[str, list[str]] = defaultdict(list)

    for mod in mods:
        archive_name = mod.get("archive_name", "")
        if archive_name:
            name_to_refs[archive_name].append(_mod_ref(mod))

    for archive_name, mod_refs in sorted(name_to_refs.items()):
        if len(mod_refs) > 1:
            messages.append(
                _format_error(
                    path,
                    ", ".join(mod_refs),
                    f"duplicate archive_name {archive_name!r}",
                )
            )

    return messages


def check_edition_wabbajack_readiness(mods: list[dict], path: Path) -> list[str]:
    """Run all Wabbajack readiness checks for a single edition manifest."""
    messages: list[str] = []
    for mod in mods:
        if not isinstance(mod, dict):
            continue
        messages.extend(check_mod_wabbajack_readiness(mod, path))
    messages.extend(check_duplicate_archive_names(mods, path))
    return messages
