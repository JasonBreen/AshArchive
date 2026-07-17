# Ash Archive control project

This directory contains the planning, metadata, documentation, and validation tooling for the dual-edition Ash Archive Morrowind Wabbajack project.

## Editions

- **Pilgrim Edition** — OpenMW; atmospheric, long-play pilgrimage horror. *The island remembers.*
- **Sleeper Edition** — classic Morrowind with MCP, MGE XE, and MWSE; reactive dream horror. *The dream notices you.*

The editions share design pillars and evidence standards, but they do not share a forced load order or artificial feature parity.

## Current state

The project is in **Phase 1 — Sourcing**. The control repository is operational, but neither edition is an installable or playable release. Manifests contain planned and evaluation-stage records, generated modlists are previews, and end-to-end installation evidence does not yet exist.

Immediate work is tracked in [FOLLOW-UP-TASKS.md](FOLLOW-UP-TASKS.md). Phase gates and release criteria are defined in [ROADMAP.md](ROADMAP.md).

## Setup

From this directory:

```bash
python -m pip install --editable ".[dev]"
```

## Common commands

```bash
python tools/lint_repo.py
python tools/validate_manifests.py
python tools/generate_modlist_markdown.py
python tools/compare_editions.py
python tools/check_duplicate_mods.py
python tools/summarize_sourced_mods.py
pytest
```

`MODLIST.md` generated sections must be updated through `tools/generate_modlist_markdown.py`, not edited manually.

## Working model

- `editions/openmw/` and `editions/mwse/` hold edition-specific manifests and docs.
- `shared/` holds categories, candidate intake, source triage, multi-package provenance, and cross-edition policy.
- `.control.meta` files are YAML-formatted internal metadata, not MO2 download sidecars.
- `tools/` and `tests/` enforce schemas, naming, derived output, and repository automation consistency.
- `../.agents/presets/` is the canonical policy layer for recurring automation.
- `../.codex/agents/` and `../.agents/skills/` provide runnable translations and workflows governed by those presets.
- Pull requests to `main` run repository and archive-integrity workflows before merge.

## Start here

- [Project Bible](PROJECT-BIBLE.md)
- [Roadmap](ROADMAP.md)
- [Follow-up Tasks](FOLLOW-UP-TASKS.md)
- [Repository Changelog](CHANGELOG.md)
- [Pilgrim Edition](editions/openmw/README.md)
- [Sleeper Edition](editions/mwse/README.md)
- [Local Agent Presets](LOCAL-AGENT-PRESETS.md)
- [Contributing guide](../CONTRIBUTING.md)
- [Agent rules](../AGENT-RULES.md)
