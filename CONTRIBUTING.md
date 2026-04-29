# Contributing to TheDreamIsTheDoor / Ash Archive

Thank you for contributing.

This repository is a planning/control repo for **Ash Archive**, organized under `ash-archive/`, with two sibling editions:

- **Pilgrim Edition** (OpenMW)
- **Sleeper Edition** (classic Morrowind + MCP + MGE XE + MWSE)

The project is scaffold/planning-first. Do not present unverified compatibility claims as tested facts.

## Repository layout

- `ash-archive/editions/openmw/` — Pilgrim edition docs and manifests
- `ash-archive/editions/mwse/` — Sleeper edition docs and manifests
- `ash-archive/shared/` — shared categories, design rules, sourcing metadata
- `ash-archive/tools/` — validation and markdown generation tooling
- `ash-archive/tests/` — Python tests for tooling and schema checks
- `ash-archive/PROJECT-BIBLE.md` — core project thesis and non-negotiable design constraints

## Branch naming conventions

Use focused branches with one of these prefixes:

- `codex/`
- `copilot/`
- `docs/`
- `tooling/`
- `manifests/`
- `wabbajack/`
- `ci/`

Examples:
- `docs/update-openmw-install-assumptions`
- `tooling/manifest-error-improvements`
- `manifests/mwse-status-transition-notes`

## Commit message style

Use concise prefix-based commit messages:

- `docs:`
- `tools:`
- `manifests:`
- `shared:`
- `openmw:`
- `mwse:`
- `tests:`
- `ci:`

Examples:
- `docs: add governance guidance for PR scope`
- `tools: improve duplicate detection messaging`
- `shared: add sourced-mod verification fields`

## Pull request expectations

1. Keep PRs small and reviewable.
2. Explain **what changed**, **why**, and **what did not change**.
3. Include edition impact (Shared/OpenMW/MWSE/Tooling/Docs-only).
4. Include validation results or a clear reason for any skipped checks.
5. Do not mix unrelated changes in one PR.

## Validation commands

Run relevant checks from `ash-archive/`:

```bash
python tools/validate_manifests.py
python tools/generate_modlist_markdown.py
python tools/compare_editions.py
python tools/check_duplicate_mods.py
pytest
```

Use a subset only when truly scope-limited; state what was run.

## Manifest change expectations

When editing manifests:

1. Keep OpenMW and MWSE as sibling implementations, not forced parity.
2. Preserve category integrity against `shared/categories.meta`.
3. Preserve cross-edition status intent and explicit rationale.
4. Avoid speculative metadata.
5. Do not mark compatibility as tested without documented evidence.

## Mod sourcing expectations

When updating sourcing records:

1. Record evidence and confidence explicitly.
2. Distinguish candidate vs accepted status clearly.
3. Do not invent URLs, archive names, or version identifiers.
4. Do not mark mods accepted without review/testing notes.


## Sourced-mod candidate workflow

Use `ash-archive/shared/sourced-mod-workflow.md` when triaging or promoting sourced candidates.
Treat `shared/sourced-mods.meta` as candidate intake metadata, not an accepted-mod manifest.

## Documentation expectations

1. Keep docs aligned with current repo state (planning/scaffold where applicable).
2. Avoid language that implies release-ready installer state unless true.
3. Preserve project horror direction: Morrowind-native, evidence-first, no crossover IP content.

## Documenting uncertainty

When facts are incomplete:

- Use explicit uncertainty wording (for example: "unverified", "needs confirmation", "TBD").
- Add what evidence is missing and what test/check would confirm it.
- Never replace unknowns with invented details.

## Handling OpenMW vs MWSE differences

1. Prefer edition-appropriate solutions over artificial parity.
2. Explain when behavior intentionally differs between editions.
3. Do not collapse both editions into a shared load order.

## Proposing design-bible exceptions

If a change appears to conflict with `ash-archive/PROJECT-BIBLE.md`:

1. Open a PR with a clearly labeled **Design-Bible Exception Request** section.
2. Explain the exact rule affected, rationale, alternatives considered, and risk.
3. Do not merge exception-like changes without human maintainer review.

## Additional agent guidance

AI agents should also follow `AGENT-RULES.md`.
