from __future__ import annotations

from pathlib import Path

import yaml


def load_meta_document(path: Path) -> dict:
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


def load_mods(path: Path) -> list[dict]:
    data = load_meta_document(path)
    mods = data.get("mods", [])
    if not isinstance(mods, list):
        raise ValueError(f"'mods' must be a list: {path}")
    return mods
