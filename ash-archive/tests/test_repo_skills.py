from pathlib import Path

import yaml

from tools.lint_repo import SKILL_PRESETS, _load_skill, validate_repo_configuration

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / ".agents" / "skills"
PRESET_ROOT = REPO_ROOT / ".agents" / "presets"
EXPECTED_SKILL_PRESETS = {
    "ash-archive-triage-sources": "source-triage-agent.yaml",
    "ash-archive-lint-manifests": "manifest-lint-agent.yaml",
    "ash-archive-regenerate-modlists": "modlist-regenerator.yaml",
    "ash-archive-audit-edition-drift": "edition-drift-auditor.yaml",
    "ash-archive-sync-docs": "documentation-sync-agent.yaml",
    "ash-archive-assess-release": "release-readiness-agent.yaml",
    "ash-archive-plan-wabbajack-list": "wabbajack-list-planner.yaml",
    "ash-archive-write-wabbajack-copy": "wabbajack-list-writer.yaml",
}
CANONICAL_BINDINGS = {
    "scope",
    "allowed_actions",
    "forbidden_actions",
    "required_checks",
    "stop_conditions",
    "human_review_required_for",
}


def test_repo_skill_set_has_one_exact_canonical_preset_mapping() -> None:
    skill_names = {path.parent.name for path in SKILL_ROOT.glob("*/SKILL.md")}
    assert SKILL_PRESETS == EXPECTED_SKILL_PRESETS
    assert skill_names == EXPECTED_SKILL_PRESETS.keys()


def test_repo_skills_preserve_reading_checks_and_canonical_guardrails() -> None:
    for skill_name, preset_filename in EXPECTED_SKILL_PRESETS.items():
        skill_path = SKILL_ROOT / skill_name / "SKILL.md"
        metadata, body = _load_skill(skill_path)
        preset = yaml.safe_load((PRESET_ROOT / preset_filename).read_text(encoding="utf-8"))

        assert metadata["name"] == skill_name
        assert metadata["description"].strip()
        canonical_reference = f".agents/presets/{preset_filename}"
        assert canonical_reference in body
        assert "completely before acting" in body
        for binding in CANONICAL_BINDINGS:
            assert f"`{binding}`" in body, f"{skill_name} does not bind {binding}"
        for required_path in preset["read_before_editing"]:
            assert required_path in body, f"{skill_name} does not require reading {required_path}"
        for check in preset["required_checks"]:
            assert check["command"] in body, (
                f"{skill_name} does not preserve required check {check['command']}"
            )

        normalized_body = " ".join(body.split())
        assert "Never invent mod metadata" in normalized_body
        assert "accept or reject a mod" in normalized_body
        assert "promote a candidate" in normalized_body
        assert "claim compatibility without documented evidence and human review" in normalized_body

        interface_path = skill_path.parent / "agents" / "openai.yaml"
        interface_data = yaml.safe_load(interface_path.read_text(encoding="utf-8"))
        assert set(interface_data) == {"interface"}
        assert set(interface_data["interface"]) == {
            "display_name",
            "short_description",
            "default_prompt",
        }
        assert f"${skill_name}" in interface_data["interface"]["default_prompt"]


def test_repo_configuration_lint_covers_skill_workflows() -> None:
    assert validate_repo_configuration() == []
