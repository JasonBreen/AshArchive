from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EDITIONS = ("openmw", "mwse")


def manifest_path(edition: str) -> Path:
    return ROOT / "editions" / edition / "manifests" / "mods.meta"


def categories_path() -> Path:
    return ROOT / "shared" / "categories.meta"
