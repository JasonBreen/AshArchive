# AGENT RULES

These rules apply to AI assistants (Codex, Copilot, Claude, and similar agents) contributing to this repository.

## Required workflow

1. Work on a dedicated branch and submit changes through a pull request.
2. Keep PRs small, focused, and reviewable.
3. Limit scope to the requested task; do not bundle unrelated feature work.
4. When uncertain, document uncertainty explicitly instead of guessing.
5. Run relevant validation commands before opening or updating a PR.

## Repository direction and design constraints

1. Preserve the two-edition model:
   - **Ash Archive: Pilgrim Edition** (OpenMW)
   - **Ash Archive: Sleeper Edition** (classic Morrowind + MCP + MGE XE + MWSE)
2. Do not collapse both editions into one shared load order.
3. Preserve Morrowind-native psychological horror direction.
4. Preserve the **evidence before explanation** principle.
5. Do not remove or weaken constraints in `ash-archive/PROJECT-BIBLE.md`.

## Data integrity and evidence standards

1. Do not invent URLs, versions, archive names, or test results.
2. Do not invent mod URLs.
3. Do not claim compatibility has been tested unless repository documentation already records that evidence.
4. Do not mark mods as `accepted` without review notes and compatibility evidence.
5. Do not delete reasoning from rejected-mod records.
6. Avoid editing generated sections manually; use repository generation tools.
7. Do not overwrite generated sections outside generation tooling.

## Content boundaries

1. No direct horror-franchise crossover content.
2. No Skyrimification, anime face replacers, or generic jump-scare design.
3. Do not add convenience fast travel without explicit design review.
4. Do not add survival systems without clear configuration and testing notes.

## Validation commands (run when relevant)

From `ash-archive/`:

```bash
python tools/validate_manifests.py
python tools/generate_modlist_markdown.py
python tools/compare_editions.py
python tools/check_duplicate_mods.py
pytest
```

If a command is not run, state why in the PR.
