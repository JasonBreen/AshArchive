from __future__ import annotations

from pathlib import Path

import pytest

from tools.lib.manifest import load_meta_document, load_mods


def test_load_meta_document_valid(tmp_path: Path):
    yaml_file = tmp_path / "valid.yaml"
    yaml_file.write_text("key: value\n", encoding="utf-8")
    assert load_meta_document(yaml_file) == {"key": "value"}


def test_load_meta_document_empty(tmp_path: Path):
    yaml_file = tmp_path / "empty.yaml"
    yaml_file.write_text("", encoding="utf-8")
    assert load_meta_document(yaml_file) == {}


def test_load_meta_document_missing():
    with pytest.raises(ValueError, match="Missing metadata file"):
        load_meta_document(Path("non_existent_file.yaml"))


def test_load_meta_document_invalid_yaml(tmp_path: Path):
    yaml_file = tmp_path / "invalid.yaml"
    yaml_file.write_text("key: value\n- item", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid YAML content"):
        load_meta_document(yaml_file)


def test_load_meta_document_not_dict(tmp_path: Path):
    yaml_file = tmp_path / "list.yaml"
    yaml_file.write_text("- item1\n- item2", encoding="utf-8")
    with pytest.raises(ValueError, match="Top-level metadata document must be a mapping"):
        load_meta_document(yaml_file)


def test_load_mods_valid(tmp_path: Path):
    yaml_file = tmp_path / "mods.yaml"
    yaml_file.write_text("mods:\n  - id: mod1\n  - id: mod2", encoding="utf-8")
    assert load_mods(yaml_file) == [{"id": "mod1"}, {"id": "mod2"}]


def test_load_mods_missing_key(tmp_path: Path):
    yaml_file = tmp_path / "no_mods.yaml"
    yaml_file.write_text("other_key: value", encoding="utf-8")
    assert load_mods(yaml_file) == []


def test_load_mods_not_list(tmp_path: Path):
    yaml_file = tmp_path / "invalid_mods.yaml"
    yaml_file.write_text("mods: not_a_list", encoding="utf-8")
    with pytest.raises(ValueError, match="'mods' must be a list"):
        load_mods(yaml_file)
