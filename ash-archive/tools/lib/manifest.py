from __future__ import annotations

import copy
from functools import lru_cache
from pathlib import Path

import yaml


@lru_cache(maxsize=None)
def _load_meta_document_cached(path: Path) -> dict:
    """Load and cache a YAML metadata document, enforcing a mapping root."""
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except FileNotFoundError as exc:
        raise ValueError(f"Missing metadata file: {path}") from exc
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML content in metadata file {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"Top-level metadata document must be a mapping: {path}")
    return data


def load_meta_document(path: Path) -> dict:
    """Load a YAML metadata document and enforce a mapping root."""
    return copy.deepcopy(_load_meta_document_cached(path))


def load_mods(path: Path) -> list[dict]:
    """Return the `mods` list from a metadata document."""
    data = load_meta_document(path)
    mods = data.get("mods", [])
    if not isinstance(mods, list):
        raise ValueError(f"'mods' must be a list: {path}")
    return mods
