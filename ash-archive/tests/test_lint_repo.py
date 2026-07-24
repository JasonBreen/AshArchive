from pathlib import Path

from tools.lint_repo import _conflict_marker_issues, _is_ignored_repo_path, _markdown_link_issues


def test_repo_scan_ignores_generated_and_test_artifact_directories() -> None:
    assert _is_ignored_repo_path(Path(".codex-pytest-run") / "fixture.md")
    assert _is_ignored_repo_path(Path("package.egg-info") / "README.md")
    assert _is_ignored_repo_path(Path("build") / "README.md")
    assert _is_ignored_repo_path(Path(".venv") / "README.md")
    assert not _is_ignored_repo_path(Path(".agents") / "skills" / "SKILL.md")


def test_conflict_marker_check_covers_plain_text_inventory(tmp_path: Path) -> None:
    inventory = tmp_path / "modlist.txt"
    inventory.write_text("<<<<<<< local\nentry\n=======\nother\n>>>>>>> remote\n", encoding="utf-8")

    issues = _conflict_marker_issues(inventory, tmp_path)

    assert issues == [
        "modlist.txt:1: unresolved merge marker",
        "modlist.txt:3: unresolved merge marker",
        "modlist.txt:5: unresolved merge marker",
    ]


def test_markdown_link_check_accepts_existing_relative_target(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    target = tmp_path / "target.md"
    target.write_text("# Target\n", encoding="utf-8")
    source = docs / "source.md"
    source.write_text("[Target](../target.md#section)\n", encoding="utf-8")

    assert _markdown_link_issues(source, tmp_path) == []


def test_markdown_link_check_reports_missing_target(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text("[Missing](missing.md)\n", encoding="utf-8")

    assert _markdown_link_issues(source, tmp_path) == [
        "source.md:1: broken internal link 'missing.md'"
    ]


def test_markdown_link_check_ignores_external_and_page_anchor_links(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text(
        "[External](https://example.invalid/path) [Section](#section)\n", encoding="utf-8"
    )

    assert _markdown_link_issues(source, tmp_path) == []


def test_markdown_link_check_reports_out_of_bounds_link(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text("[Out of Bounds](../../../../../../../etc/passwd)\n", encoding="utf-8")

    assert _markdown_link_issues(source, tmp_path) == [
        "source.md:1: link escapes repository bounds '../../../../../../../etc/passwd'"
    ]
