from tools.lint_repo import SKILL_PRESETS, validate_repo_configuration


def test_repo_skill_workflows_are_complete() -> None:
    assert len(SKILL_PRESETS) == 8
    assert validate_repo_configuration() == []
