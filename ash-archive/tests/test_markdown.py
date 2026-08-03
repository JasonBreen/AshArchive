from __future__ import annotations

from tools.lib.markdown import _sanitize_inline, render_mod_sections


def test_sanitize_inline() -> None:
    assert _sanitize_inline("normal text") == "normal text"
    assert _sanitize_inline("text with `backticks`") == "text with 'backticks'"
    assert _sanitize_inline("text\nwith\rnewlines") == "text with newlines"
    assert _sanitize_inline("  leading and trailing  ") == "leading and trailing"


def test_render_mod_sections_empty() -> None:
    assert render_mod_sections([]) == "\n"


def test_render_mod_sections_basic() -> None:
    mods = [
        {
            "category": "Visuals",
            "name": "Better Textures",
            "id": "better-textures",
            "status": "accepted",
            "engine": ["openmw", "mwse"],
            "cross_edition_status": "identical",
            "decision_reason": "Great mod.",
        }
    ]
    expected = (
        "## Visuals\n"
        "- **Better Textures** (`better-textures`) — status: `accepted`, engine: `openmw, mwse`, "
        "cross-edition: `identical`. Reason: Great mod.\n"
    )
    assert render_mod_sections(mods) == expected


def test_render_mod_sections_sorting() -> None:
    mods = [
        {
            "category": "Visuals",
            "name": "B Mod",
            "id": "b-mod",
            "status": "accepted",
            "cross_edition_status": "identical",
            "decision_reason": "test",
            "priority": 2,
        },
        {
            "category": "Audio",
            "name": "A Mod",
            "id": "a-mod",
            "status": "accepted",
            "cross_edition_status": "identical",
            "decision_reason": "test",
            "priority": 1,
        },
        {
            "category": "Visuals",
            "name": "C Mod",
            "id": "c-mod",
            "status": "accepted",
            "cross_edition_status": "identical",
            "decision_reason": "test",
            "priority": 1,
        },
    ]

    # Audio should be before Visuals (alphabetical).
    # Within Visuals, C Mod (priority 1) should be before B Mod (priority 2).
    expected = (
        "## Audio\n"
        "- **A Mod** (`a-mod`) — status: `accepted`, engine: ``, cross-edition: `identical`. Reason: test\n"
        "\n"
        "## Visuals\n"
        "- **C Mod** (`c-mod`) — status: `accepted`, engine: ``, cross-edition: `identical`. Reason: test\n"
        "- **B Mod** (`b-mod`) — status: `accepted`, engine: ``, cross-edition: `identical`. Reason: test\n"
    )
    assert render_mod_sections(mods) == expected


def test_render_mod_sections_missing_optional_keys() -> None:
    mods = [
        {
            "category": "Core",
            "name": "Core Mod",
            "id": "core-mod",
            "status": "testing",
            "cross_edition_status": "unknown",
            "decision_reason": "pending",
            # missing "engine" and "priority"
        },
        {
            "category": "Core",
            "name": "Another Core Mod",
            "id": "another-core",
            "status": "testing",
            "cross_edition_status": "unknown",
            "decision_reason": "pending",
            "priority": 1,
            # missing "engine"
        },
    ]
    # Another Core Mod (priority 1) should be before Core Mod (missing priority = 9999).
    expected = (
        "## Core\n"
        "- **Another Core Mod** (`another-core`) — status: `testing`, engine: ``, cross-edition: `unknown`. Reason: pending\n"
        "- **Core Mod** (`core-mod`) — status: `testing`, engine: ``, cross-edition: `unknown`. Reason: pending\n"
    )
    assert render_mod_sections(mods) == expected


def test_render_mod_sections_sanitization() -> None:
    mods = [
        {
            "category": "Bad\nCategory",
            "name": "Name\nWith\nNewlines",
            "id": "id`with`backticks",
            "status": "accepted\nstatus",
            "engine": ["bad\nengine", "good`engine"],
            "cross_edition_status": "cross\nedition",
            "decision_reason": "Reason\nwith\n`backticks`",
        }
    ]
    expected = (
        "## Bad Category\n"
        "- **Name With Newlines** (`id'with'backticks`) — status: `accepted status`, engine: `bad engine, good'engine`, "
        "cross-edition: `cross edition`. Reason: Reason with 'backticks'\n"
    )
    assert render_mod_sections(mods) == expected
