from pathlib import Path
import tomllib

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
PRESET_DIR = REPO_ROOT / ".agents" / "presets"
AGENT_DIR = REPO_ROOT / ".codex" / "agents"


def _yaml_presets() -> dict[str, dict]:
    return {
        path.stem: yaml.safe_load(path.read_text(encoding="utf-8"))
        for path in PRESET_DIR.glob("*.yaml")
    }


def _toml_agents() -> dict[str, dict]:
    return {
        path.stem: tomllib.loads(path.read_text(encoding="utf-8"))
        for path in AGENT_DIR.glob("*.toml")
    }


def test_repo_agent_set_matches_canonical_presets() -> None:
    assert _toml_agents().keys() == _yaml_presets().keys()


def test_repo_agents_include_required_codex_fields_and_preset_guardrails() -> None:
    presets = _yaml_presets()

    for stem, agent in _toml_agents().items():
        assert agent["name"] == stem
        assert agent["description"].strip()
        instructions = agent["developer_instructions"]
        assert instructions.strip()

        preset = presets[stem]
        for required_path in preset.get("read_before_editing", []):
            assert required_path in instructions, f"{stem} does not require reading {required_path}"
        for forbidden_action in preset.get("forbidden_actions", []):
            assert forbidden_action in instructions, (
                f"{stem} does not preserve forbidden action {forbidden_action}"
            )
        for check in preset.get("required_checks", []):
            assert check["command"] in instructions, (
                f"{stem} does not preserve required check {check['command']}"
            )


def test_root_agents_file_loads_repository_policy() -> None:
    guidance = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "AGENT-RULES.md" in guidance
    assert "ash-archive/PROJECT-BIBLE.md" in guidance
    assert ".codex/agents/" in guidance
