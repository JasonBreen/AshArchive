from __future__ import annotations

from pathlib import Path

import yaml


def load_yaml(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except FileNotFoundError as exc:
        raise ValueError(f"Missing YAML file: {path}") from exc
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"Top-level YAML must be a mapping: {path}")
    return data


def load_mods(path: Path) -> list[dict]:
    data = load_yaml(path)
    mods = data.get("mods", [])
    if not isinstance(mods, list):
        raise ValueError(f"'mods' must be a list: {path}")
    return mods
