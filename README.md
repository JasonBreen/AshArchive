# Ash Archive

**Ash Archive** is a dual-edition Morrowind Wabbajack project built around psychological horror native to Vvardenfell. The repository is a planning and control system for two sibling editions that share a thesis and evaluation standards while using engine-specific implementations.

| Edition | Engine | Identity |
|---|---|---|
| **Pilgrim Edition** | OpenMW | Stable, atmospheric, long-play pilgrimage horror — *The island remembers.* |
| **Sleeper Edition** | Classic Morrowind + MCP + MGE XE + MWSE | Script-heavy, reactive dream horror — *The dream notices you.* |

## Project status

| Area | Status |
|---|---|
| Development phase | **Phase 1 — Sourcing** |
| Public Wabbajack installer | **Not available** |
| Playable release | **No** |
| Final load order and patch plan | **Not defined** |
| Compatibility evidence | Candidate-level and incomplete; hands-on evaluation remains required |
| Repository automation | Lint, tests, manifest integrity, generated-output, drift, and duplicate checks run on pull requests to `main` |

The checked-in manifests and generated `MODLIST.md` files are planning artifacts. A status such as `planned` or `testing` records control-repository state; it does not mean that a public build has been installed or playtested end to end.

See the [roadmap](ash-archive/ROADMAP.md) and [Phase 1 follow-up checklist](ash-archive/FOLLOW-UP-TASKS.md) for the work that remains.

## Design pillars

- **The Island Remembers** — Vvardenfell is already haunted by prophecy, reincarnation, and suppressed history.
- **The Dream is Geological** — dread accumulates in strata, not moments.
- **Reincarnation is Body Horror** — the Nerevarine arc is treated as violation, not triumph.
- **Dagoth Ur is Intimate, Not Loud** — the antagonist functions as contamination, not spectacle.
- **The Tribunal Are the Beautiful Crime Scene** — divinity operates as a cover-up.
- **Evidence Before Explanation** — logs, notes, shrines, and rumours foreshadow; nothing is explained twice.

Horror must emerge from Morrowind's own lore and systems: no horror-franchise crossovers, generic jump scares, or Skyrimification.

## What the repository contains

- Schema-backed `.control.meta` manifests for each edition.
- Shared candidate intake, source-triage, and multi-package provenance records.
- Generated modlist previews derived from the edition manifests.
- Validation, comparison, duplicate-detection, generation, and repository-lint tooling.
- Eight runner-neutral maintenance presets, matching project-scoped Codex agents, and matching reusable repository skills.
- Pull-request checks for repository configuration, tests, manifest validity, generated-output drift, edition drift, and duplicate entries.

Internal `.control.meta` files contain YAML-formatted control data. They are not Mod Organizer 2 download sidecars. Native MO2 `.meta` files must come from verified source artifacts; see [the metadata distinction](ash-archive/shared/mo2-download-meta-sidecars.md).

## Developer setup

Requirements:

- Python 3.11 or newer
- PyYAML at runtime
- pytest, ruff, and yamllint for development

From `ash-archive/`:

```bash
python -m pip install --editable ".[dev]"
```

## Validation and generation

Run commands from `ash-archive/`:

```bash
# Lint Python, YAML control metadata, agent TOML, and repository skills
python tools/lint_repo.py

# Validate both edition manifests and shared schemas
python tools/validate_manifests.py

# Regenerate the derived edition modlists
python tools/generate_modlist_markdown.py

# Review intentional and unexplained edition differences
python tools/compare_editions.py

# Find duplicate IDs and likely accidental duplicate names
python tools/check_duplicate_mods.py

# Summarize candidate intake records
python tools/summarize_sourced_mods.py

# Run the test suite
pytest
```

Do not hand-edit generated sections in edition `MODLIST.md` files.

## Repository map

```text
AshArchive/
├── .agents/
│   ├── presets/              # Canonical runner-neutral maintenance policies
│   └── skills/               # Reusable repository workflows
├── .codex/agents/            # Runnable project-scoped Codex translations
├── .github/workflows/        # Pre-merge repository and archive-integrity checks
├── ash-archive/
│   ├── editions/
│   │   ├── openmw/           # Pilgrim Edition manifests and documentation
│   │   └── mwse/             # Sleeper Edition manifests and documentation
│   ├── shared/               # Categories, sourcing, provenance, and design rules
│   ├── tools/                # Validation and generation scripts
│   ├── tests/                # Tooling, schema, agent, and skill tests
│   ├── PROJECT-BIBLE.md
│   ├── ROADMAP.md
│   ├── FOLLOW-UP-TASKS.md
│   └── CHANGELOG.md
├── AGENTS.md
├── AGENT-RULES.md
├── CONTRIBUTING.md
└── README.md
```

## Documentation

- [Project Bible](ash-archive/PROJECT-BIBLE.md) — thesis, dual-edition philosophy, and non-negotiable atmosphere rules
- [Roadmap](ash-archive/ROADMAP.md) — phase goals, gates, and current development state
- [Follow-up Tasks](ash-archive/FOLLOW-UP-TASKS.md) — immediate Phase 1 sourcing and Phase 2 preparation work
- [Pilgrim Edition](ash-archive/editions/openmw/README.md) — OpenMW identity, artifacts, and documentation
- [Sleeper Edition](ash-archive/editions/mwse/README.md) — MWSE identity, artifacts, and documentation
- [Changelog](ash-archive/CHANGELOG.md) — repository-level change history
- [Local Agent Presets](ash-archive/LOCAL-AGENT-PRESETS.md) — automation scopes, stop conditions, and human-review gates
- [Contributing](CONTRIBUTING.md) — setup, branch, validation, metadata, and PR conventions
- [Agent Rules](AGENT-RULES.md) — mandatory rules for automated contributors
- [Security Policy](SECURITY.md)

## License

See [LICENSE.md](ash-archive/LICENSE.md).
