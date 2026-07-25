import tomllib
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
PRESET_DIR = REPO_ROOT / ".agents" / "presets"
AGENT_DIR = REPO_ROOT / ".codex" / "agents"

EXPECTED_PRESETS = {
    "changelog-agent",
    "documentation-sync-agent",
    "edition-drift-auditor",
    "manifest-lint-agent",
    "modlist-regenerator",
    "release-readiness-agent",
    "source-triage-agent",
    "wabbajack-list-planner",
    "wabbajack-list-writer",
}
REQUIRED_PRESET_FIELDS = {
    "name",
    "purpose",
    "mode",
    "scope",
    "read_before_editing",
    "allowed_actions",
    "forbidden_actions",
    "required_checks",
    "stop_conditions",
    "handoff",
    "human_review_required_for",
}
OPTIONAL_PRESET_FIELDS = {"preference_source", "taste_lenses", "voice_rules"}
LIST_FIELDS = {
    "scope",
    "read_before_editing",
    "allowed_actions",
    "forbidden_actions",
    "stop_conditions",
    "human_review_required_for",
}
BASELINE_READS = {
    "AGENT-RULES.md",
    "ash-archive/LOCAL-AGENT-PRESETS.md",
    "ash-archive/PROJECT-BIBLE.md",
}
BASELINE_FORBIDDEN_ACTIONS = {
    "invent_mod_metadata",
    "accept_or_reject_mods_without_human_review",
    "claim_compatibility_without_evidence",
}
BASELINE_HUMAN_GATES = {
    "accepting_or_rejecting_mods",
    "promoting_candidates_into_edition_manifests",
    "compatibility_claims_based_on_playtesting",
}
CANONICAL_BINDINGS = {
    "scope",
    "allowed_actions",
    "forbidden_actions",
    "required_checks",
    "stop_conditions",
    "human_review_required_for",
}


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


def test_canonical_preset_contracts_are_complete_and_conservative() -> None:
    presets = _yaml_presets()
    assert presets.keys() == EXPECTED_PRESETS

    for stem, preset in presets.items():
        assert isinstance(preset, dict)
        assert REQUIRED_PRESET_FIELDS <= set(preset)
        assert set(preset) <= REQUIRED_PRESET_FIELDS | OPTIONAL_PRESET_FIELDS
        assert preset["name"] == stem
        assert isinstance(preset["purpose"], str) and preset["purpose"].strip()
        assert isinstance(preset["mode"], str) and preset["mode"].strip()

        for field in LIST_FIELDS:
            values = preset[field]
            assert isinstance(values, list) and values, f"{stem} has no {field}"
            assert all(isinstance(value, str) and value.strip() for value in values)
            assert len(values) == len(set(values)), f"{stem} has duplicate {field} entries"

        assert BASELINE_READS <= set(preset["read_before_editing"])
        assert BASELINE_FORBIDDEN_ACTIONS <= set(preset["forbidden_actions"])
        assert BASELINE_HUMAN_GATES <= set(preset["human_review_required_for"])

        checks = preset["required_checks"]
        assert isinstance(checks, list) and checks
        for check in checks:
            assert isinstance(check, dict)
            assert {"working_directory", "command"} <= check.keys()
            assert check.keys() <= {"working_directory", "command", "when"}
            assert check["working_directory"] == "ash-archive"
            assert isinstance(check["command"], str) and check["command"].strip()

        handoff = preset["handoff"]
        assert isinstance(handoff, dict) and handoff
        assert all(isinstance(key, str) and value is True for key, value in handoff.items())


def test_repo_agent_set_matches_canonical_presets() -> None:
    assert _toml_agents().keys() == _yaml_presets().keys() == EXPECTED_PRESETS


def test_repo_agents_preserve_the_complete_canonical_safety_contract() -> None:
    presets = _yaml_presets()

    for stem, agent in _toml_agents().items():
        assert set(agent) == {"name", "description", "developer_instructions"}
        assert agent["name"] == stem
        assert agent["description"].strip()
        instructions = agent["developer_instructions"]
        assert instructions.strip()

        preset = presets[stem]
        canonical_reference = f".agents/presets/{stem}.yaml"
        assert canonical_reference in instructions
        assert "completely before acting" in instructions
        for binding in CANONICAL_BINDINGS:
            assert f"`{binding}`" in instructions, f"{stem} does not bind {binding}"
        for required_path in preset["read_before_editing"]:
            assert required_path in instructions, f"{stem} does not require reading {required_path}"
        for check in preset["required_checks"]:
            assert check["command"] in instructions, (
                f"{stem} does not preserve required check {check['command']}"
            )
        for field in ("forbidden_actions", "stop_conditions", "human_review_required_for"):
            for identifier in preset[field]:
                assert identifier in instructions, f"{stem} does not preserve {field}: {identifier}"


def test_root_agents_file_loads_repository_policy() -> None:
    guidance = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "AGENT-RULES.md" in guidance
    assert "ash-archive/PROJECT-BIBLE.md" in guidance
    assert ".agents/presets/" in guidance
    assert ".codex/agents/" in guidance
    assert ".agents/skills/" in guidance
