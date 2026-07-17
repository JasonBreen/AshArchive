from pathlib import Path

import pytest

from tools.generate_modlist_markdown import END, START, expected_modlist, render_modlist_document


def test_render_modlist_document_is_idempotent() -> None:
    initial = f"# Modlist\n\nIntro.\n\n{START}\nold\n{END}\n"
    generated = render_modlist_document(initial, "new\n")

    assert render_modlist_document(generated, "new\n") == generated
    assert generated == f"# Modlist\n\nIntro.\n\n{START}\nnew\n{END}\n"


@pytest.mark.parametrize(
    "document",
    [
        f"# Modlist\n{START}\nmissing end\n",
        f"# Modlist\n{END}\nmissing start\n",
        f"# Modlist\n{START}\none\n{END}\n{START}\ntwo\n{END}\n",
        f"# Modlist\n{END}\n{START}\n",
    ],
)
def test_render_modlist_document_rejects_invalid_markers(document: str) -> None:
    with pytest.raises(ValueError):
        render_modlist_document(document, "generated\n")


def test_expected_modlist_does_not_write(tmp_path: Path) -> None:
    path = tmp_path / "MODLIST.md"
    path.write_text("# Modlist\n", encoding="utf-8")

    current, expected = expected_modlist(path, "generated\n")

    assert current == "# Modlist\n"
    assert expected != current
    assert path.read_text(encoding="utf-8") == current
