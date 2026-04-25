from __future__ import annotations

from pathlib import Path
import yaml


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Top-level YAML must be a mapping: {path}")
    return data


def load_mods(path: Path) -> list[dict]:
    data = load_yaml(path)
    mods = data.get("mods", [])
    if not isinstance(mods, list):
        raise ValueError(f"'mods' must be a list: {path}")
    return mods
