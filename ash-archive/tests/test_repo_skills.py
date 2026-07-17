from tools.lint_repo import SKILL_PRESETS, validate_repo_configuration

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


def test_repo_skill_workflows_are_complete() -> None:
    assert SKILL_PRESETS == EXPECTED_SKILL_PRESETS
    assert validate_repo_configuration() == []
