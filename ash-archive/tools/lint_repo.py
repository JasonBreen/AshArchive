from __future__ import annotations

import re
import subprocess
import sys
import tomllib
from pathlib import Path

import yaml
from yamllint import linter as yaml_linter
from yamllint.config import YamlLintConfig

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT.parent
PRESET_ROOT = REPO_ROOT / ".agents" / "presets"
SKILL_ROOT = REPO_ROOT / ".agents" / "skills"
AGENT_ROOT = REPO_ROOT / ".codex" / "agents"
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

SKILL_PRESETS = {
    "ash-archive-triage-sources": "source-triage-agent.yaml",
    "ash-archive-lint-manifests": "manifest-lint-agent.yaml",
    "ash-archive-regenerate-modlists": "modlist-regenerator.yaml",
    "ash-archive-audit-edition-drift": "edition-drift-auditor.yaml",
    "ash-archive-sync-docs": "documentation-sync-agent.yaml",
    "ash-archive-assess-release": "release-readiness-agent.yaml",
    "ash-archive-plan-wabbajack-list": "wabbajack-list-planner.yaml",
    "ash-archive-write-wabbajack-copy": "wabbajack-list-writer.yaml",
}


def _relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def _load_skill(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("SKILL.md must begin with YAML frontmatter")

    try:
        closing_index = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("SKILL.md frontmatter is not closed") from error

    metadata = yaml.safe_load("\n".join(lines[1:closing_index]))
    if not isinstance(metadata, dict):
        raise ValueError("SKILL.md frontmatter must be a mapping")
    return metadata, "\n".join(lines[closing_index + 1 :])


def _find_conflict_markers() -> list[str]:
    patterns = ("*.md", "*.py", "*.toml", "*.yaml", "*.yml", "*.control.meta")
    paths = {path for pattern in patterns for path in REPO_ROOT.rglob(pattern)}
    issues: list[str] = []

    for path in sorted(paths):
        if any(part in {".git", ".pytest_cache", "__pycache__"} for part in path.parts):
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("<<<<<<< ") or line == "=======" or line.startswith(">>>>>>> "):
                issues.append(f"{_relative(path)}:{line_number}: unresolved merge marker")

    return issues


def validate_repo_configuration() -> list[str]:
    issues = _find_conflict_markers()

    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    try:
        tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as error:
        issues.append(f"{_relative(pyproject_path)}: invalid TOML: {error}")

    preset_names = {path.stem for path in PRESET_ROOT.glob("*.yaml")}
    agent_names = {path.stem for path in AGENT_ROOT.glob("*.toml")}
    if preset_names != agent_names:
        issues.append(
            "agent TOML files must match preset YAML files: "
            f"presets={sorted(preset_names)}, agents={sorted(agent_names)}"
        )

    for agent_path in sorted(AGENT_ROOT.glob("*.toml")):
        try:
            agent = tomllib.loads(agent_path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as error:
            issues.append(f"{_relative(agent_path)}: invalid TOML: {error}")
            continue

        missing = {"name", "description", "developer_instructions"} - agent.keys()
        if missing:
            issues.append(f"{_relative(agent_path)}: missing fields {sorted(missing)}")
        if agent.get("name") != agent_path.stem:
            issues.append(f"{_relative(agent_path)}: name must match the filename stem")

    skill_names = {path.parent.name for path in SKILL_ROOT.glob("*/SKILL.md")}
    if skill_names != SKILL_PRESETS.keys():
        issues.append(
            "repo skill set does not match the expected workflows: "
            f"expected={sorted(SKILL_PRESETS)}, actual={sorted(skill_names)}"
        )

    for skill_name, preset_name in SKILL_PRESETS.items():
        skill_path = SKILL_ROOT / skill_name / "SKILL.md"
        try:
            metadata, body = _load_skill(skill_path)
        except (OSError, yaml.YAMLError, ValueError) as error:
            issues.append(f"{_relative(skill_path)}: {error}")
            continue

        if set(metadata) != {"name", "description"}:
            issues.append(
                f"{_relative(skill_path)}: frontmatter may only contain name and description"
            )
        if metadata.get("name") != skill_name:
            issues.append(f"{_relative(skill_path)}: name must match its directory")
        if not SKILL_NAME_PATTERN.fullmatch(str(metadata.get("name", ""))):
            issues.append(f"{_relative(skill_path)}: name must use lowercase hyphen-case")
        if not str(metadata.get("description", "")).strip():
            issues.append(f"{_relative(skill_path)}: description must not be empty")
        if "TODO" in body:
            issues.append(f"{_relative(skill_path)}: unresolved TODO remains")
        if f".agents/presets/{preset_name}" not in body:
            issues.append(
                f"{_relative(skill_path)}: canonical preset {preset_name} is not referenced"
            )

        interface_path = skill_path.parent / "agents" / "openai.yaml"
        try:
            interface_data = yaml.safe_load(interface_path.read_text(encoding="utf-8"))
            interface = interface_data["interface"]
        except (OSError, KeyError, TypeError, yaml.YAMLError) as error:
            issues.append(f"{_relative(interface_path)}: invalid interface metadata: {error}")
            continue

        required_fields = {"display_name", "short_description", "default_prompt"}
        missing_fields = required_fields - interface.keys()
        if missing_fields:
            issues.append(f"{_relative(interface_path)}: missing fields {sorted(missing_fields)}")
            continue

        short_description = interface["short_description"]
        if not 25 <= len(short_description) <= 64:
            issues.append(
                f"{_relative(interface_path)}: short_description must be 25-64 characters"
            )
        if f"${skill_name}" not in interface["default_prompt"]:
            issues.append(f"{_relative(interface_path)}: default_prompt must mention ${skill_name}")

    return issues


def lint_yaml() -> list[str]:
    config = YamlLintConfig((REPO_ROOT / ".yamllint.yml").read_text(encoding="utf-8"))
    yaml_paths = {
        *REPO_ROOT.rglob("*.yaml"),
        *REPO_ROOT.rglob("*.yml"),
        *PROJECT_ROOT.rglob("*.control.meta"),
    }
    issues: list[str] = []

    for path in sorted(yaml_paths):
        if any(part in {".git", ".pytest_cache", "__pycache__"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for problem in yaml_linter.run(text, config, filepath=_relative(path)):
            issues.append(str(problem))

    return issues


def _run_ruff(arguments: list[str]) -> int:
    command = [sys.executable, "-m", "ruff", *arguments]
    print(f"[RUN] {' '.join(command)}", flush=True)
    return subprocess.run(command, cwd=PROJECT_ROOT, check=False).returncode


def main() -> int:
    issues = [*validate_repo_configuration(), *lint_yaml()]
    for issue in issues:
        print(f"[ERROR] {issue}")

    ruff_check = _run_ruff(["check", "tools", "tests"])
    ruff_format = _run_ruff(["format", "--check", "tools", "tests"])
    if issues or ruff_check or ruff_format:
        return 1

    print("[OK] Repository configuration, YAML, and Python lint checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
