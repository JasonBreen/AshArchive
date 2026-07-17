# Contributing to Ash Archive

Ash Archive is a planning and control repository for two sibling Morrowind Wabbajack editions:

- **Pilgrim Edition** — OpenMW
- **Sleeper Edition** — classic Morrowind with MCP, MGE XE, and MWSE

The project is in Phase 1 sourcing. Keep compatibility, installability, and release claims evidence-based; neither edition is currently a playable release.

## Required reading

Before editing:

1. Read [AGENT-RULES.md](AGENT-RULES.md) if an AI assistant is involved.
2. Read [ash-archive/PROJECT-BIBLE.md](ash-archive/PROJECT-BIBLE.md) for design constraints.
3. Read the relevant edition or shared-subsystem documentation.
4. For recurring automated work, select the narrowest preset in [ash-archive/LOCAL-AGENT-PRESETS.md](ash-archive/LOCAL-AGENT-PRESETS.md).

## Developer setup

Use Python 3.11 or newer. From `ash-archive/`:

```bash
python -m pip install --editable ".[dev]"
```

## Repository layout

- `ash-archive/editions/openmw/` — Pilgrim Edition manifests, generated preview, and docs
- `ash-archive/editions/mwse/` — Sleeper Edition manifests, generated preview, MO2 planning, and docs
- `ash-archive/shared/` — categories, sourcing metadata, provenance, and shared policy
- `ash-archive/tools/` — validation, generation, comparison, and lint tooling
- `ash-archive/tests/` — schema, tooling, agent, skill, and convention tests
- `.agents/presets/` — canonical runner-neutral automation policy
- `.codex/agents/` — project-scoped Codex translations
- `.agents/skills/` — reusable repository workflows

## Branch and commit conventions

Use a focused branch with one of these prefixes:

- `agent/`
- `codex/`
- `copilot/`
- `docs/`
- `tooling/`
- `manifests/`
- `wabbajack/`
- `ci/`

Examples:

- `docs/sync-phase-one-status`
- `tooling/improve-manifest-errors`
- `manifests/mwse-evaluation-notes`

Use a concise, descriptive commit message. Prefixes such as `docs:`, `tools:`, `manifests:`, `shared:`, `openmw:`, `mwse:`, `tests:`, and `ci:` are encouraged.

## Pull request expectations

1. Keep the PR focused and reviewable.
2. Explain what changed, why it changed, and what was deliberately left unchanged.
3. Identify edition impact: shared, Pilgrim, Sleeper, tooling, automation, or docs-only.
4. Separate recorded facts from recommendations and unresolved assumptions.
5. Include exact validation results and explain skipped checks.
6. Update the appropriate changelog when the change is meaningful to maintainers or future release notes.
7. Do not combine content promotion, tooling refactors, and unrelated documentation cleanup in one PR.

Pull requests to `main` run two automated workflows:

- Repository checks install development dependencies, lint repository configuration, and run the test suite.
- Archive-integrity checks validate manifests, verify generated modlists, compare editions, and scan for duplicates.

These checks protect repository consistency; they do not prove game compatibility or release readiness.

## Validation commands

Run relevant checks from `ash-archive/`:

```bash
python tools/lint_repo.py
python tools/validate_manifests.py
python tools/generate_modlist_markdown.py
python tools/compare_editions.py
python tools/check_duplicate_mods.py
python tools/summarize_sourced_mods.py
pytest
```

After generating modlists, inspect the diff and confirm that only expected generated sections changed.

## Manifest and generated-file rules

Internal control metadata uses YAML-formatted `.control.meta` files. These are not Mod Organizer 2 download sidecars and must not be represented as native sidecars.

When editing manifests:

1. Preserve Pilgrim and Sleeper as sibling implementations, not forced copies.
2. Preserve category integrity against `shared/categories.control.meta`.
3. Preserve explicit cross-edition status and rationale.
4. Do not invent source, version, archive, hash, requirement, or compatibility data.
5. Do not mark compatibility as tested without recorded evidence.
6. Regenerate `MODLIST.md` through the generator; never hand-edit generated sections.

## Sourced-mod workflow

Use [ash-archive/shared/sourced-mod-workflow.md](ash-archive/shared/sourced-mod-workflow.md) when triaging or promoting candidates. Treat `shared/sourced-mods.control.meta` as intake metadata, not an accepted-mod manifest.

- Record evidence and confidence explicitly.
- Distinguish candidate, accepted, rejected, and deferred states.
- Preserve rejected records and their reasoning.
- Do not promote a candidate without review and compatibility evidence.
- Keep multi-package source records synchronized when child archives differ from the parent source version.

## Documentation rules

- Keep the README, roadmap, follow-up checklist, edition docs, and changelogs aligned.
- State the current planning phase and avoid implying an installer exists before Phase 4 criteria are met.
- Label unknown information as `unverified`, `needs-testing`, `planned`, `blocked`, or `TBD` as appropriate.
- Explain what evidence or test would resolve an uncertainty.
- Preserve Morrowind-native psychological horror, evidence-before-explanation, and the two-edition model.

## Design-bible exceptions

If a proposal conflicts with `ash-archive/PROJECT-BIBLE.md`, add a clearly labeled **Design-Bible Exception Request** to the PR. Identify the affected rule, rationale, alternatives, and risk. Human maintainer approval is required before merge.
