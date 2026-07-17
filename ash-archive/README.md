# Ash Archive Control Project

This directory contains the Python tooling, control metadata, generated planning views, and
edition documentation for Ash Archive. The repository plans two sibling Wabbajack editions:

- **Pilgrim Edition** targets OpenMW.
- **Sleeper Edition** targets classic Morrowind + MCP + MGE XE + MWSE.

## Current state

Neither edition is installable or playable, no final load order exists, and no end-to-end
install result is recorded. Repository validation proves structural consistency only; it
does not prove mod compatibility or release readiness.

## Control-data model

The repository separates shared provenance from edition decisions:

1. `shared/sourced-mods.control.meta` records candidate identity, source facts, evidence,
   uncertainty, and candidate-review state.
2. An edition manifest entry may point to a canonical candidate with `source_reference`.
3. Edition manifests retain engine, plugin, dependency, conflict, patch, testing, and
   load-order fields.
4. `editions/*/MODLIST.md` renders a planning view from edition manifests.

A source reference is not promotion, acceptance, compatibility evidence, or an instruction
to copy unknown version/archive data. See
[`shared/sourced-mod-workflow.md`](shared/sourced-mod-workflow.md) and
[`shared/mod-meta-schema.md`](shared/mod-meta-schema.md).

## Automated checks

From this directory, install Python 3.11 development dependencies and run the CI-equivalent
suite:

```bash
python -m pip install -e ".[dev]"

python tools/lint_repo.py
python tools/validate_manifests.py
python tools/check_duplicate_mods.py
python tools/compare_editions.py
python tools/generate_modlist_markdown.py --check
pytest
```

Continuous integration runs those checks on pull requests and pushes to `main`.
`python tools/summarize_sourced_mods.py` is an optional read-only intake report.

## Generated files

Only the sections between `GENERATED-CONTENT` markers in the two edition `MODLIST.md` files
are generated. After a manifest change, run:

```bash
python tools/generate_modlist_markdown.py
python tools/generate_modlist_markdown.py --check
```

Review both diffs. Do not edit generated sections manually.

## Manual and human-review work

Automation cannot decide whether to accept or reject a mod, establish compatibility from
playtesting, choose cross-edition parity, set a final load order, approve a design-bible
exception, or declare a release ready. Unknown source, package, version, archive, licensing,
and game-behavior facts remain blocked until evidence is recorded.

## Navigation

- [`PROJECT-BIBLE.md`](PROJECT-BIBLE.md) — design constraints
- [`ROADMAP.md`](ROADMAP.md) — phase gates
- [`FOLLOW-UP-TASKS.md`](FOLLOW-UP-TASKS.md) — active blockers and next work
- [`shared/sourced-mod-workflow.md`](shared/sourced-mod-workflow.md) — candidate and promotion lifecycle
- [`editions/openmw/README.md`](editions/openmw/README.md) — Pilgrim scope
- [`editions/mwse/README.md`](editions/mwse/README.md) — Sleeper scope
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — contribution and validation rules
