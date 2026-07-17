# Ash Archive

**Ash Archive** is a planning and control repository for a dual-edition Morrowind
Wabbajack project built around psychological horror native to Vvardenfell. The project
lives under [`ash-archive/`](ash-archive/) and is designed as two sibling editions that
share aesthetic pillars while using engine-specific implementations.

## Editions

| Edition | Engine target | Design emphasis |
|---|---|---|
| **Ash Archive: Pilgrim Edition** | OpenMW | Long-play stability, distance, documents, tomb architecture, and environmental pressure. |
| **Ash Archive: Sleeper Edition** | Classic Morrowind + MCP + MGE XE + MWSE | Reactive dream contamination, identity fracture, and configurable scripted dread. |

The editions are not interchangeable load orders. Shared candidate provenance does not
imply identical inclusion, behavior, patches, or acceptance in both editions.

## Current status

> **Planning and scaffold only.** Neither edition is installable or playable, no final
> load order exists, and the repository contains no completed end-to-end install test.

The descriptions above are design targets, not compatibility or stability claims. See the
[`ROADMAP.md`](ash-archive/ROADMAP.md) for phase gates and
[`FOLLOW-UP-TASKS.md`](ash-archive/FOLLOW-UP-TASKS.md) for unresolved work.

## Design direction

The project treats Vvardenfell as haunted by prophecy, reincarnation, and suppressed
history. Its core rule is **evidence before explanation**: documents, spaces, rumors, and
repetition should foreshadow dread before explicit revelation. Horror must emerge from
Morrowind's own systems and lore; direct franchise crossovers, generic jump scares,
Skyrimification, and convenience changes that erase pilgrimage friction are out of scope.

The complete, non-negotiable constraints live in the
[`PROJECT-BIBLE.md`](ash-archive/PROJECT-BIBLE.md).

## Repository structure

```text
AshArchive/
├── .agents/presets/           # Canonical runner-neutral local-agent presets
├── .agents/skills/            # Repo-scoped reusable workflows
├── .codex/agents/             # Runnable Codex translations of the presets
├── .github/workflows/         # Continuous integration
├── ash-archive/               # Python project and Ash Archive control data
│   ├── editions/openmw/       # Pilgrim manifests, generated modlist, and docs
│   ├── editions/mwse/         # Sleeper manifests, generated modlist, and docs
│   ├── shared/                # Canonical sourcing data and shared policies
│   ├── tools/                 # Validation, comparison, and generation scripts
│   └── tests/                 # Tooling and policy regression tests
├── modlist.txt                # Imported source inventory snapshot
├── CONTRIBUTING.md
└── README.md
```

YAML `.control.meta` files are internal project metadata. They are not native Mod
Organizer 2 download sidecar `.meta` files and must not be synthesized as such. See
[`MO2 Download Sidecars vs Internal Metadata`](ash-archive/shared/mo2-download-meta-sidecars.md).

## Metadata flow

[`shared/sourced-mods.control.meta`](ash-archive/shared/sourced-mods.control.meta) is the
canonical provenance layer for candidate source type, source URL, and source evidence. An
edition entry may use `source_reference` to point to one of those candidate IDs.

That link is provenance-only. It does **not** promote the candidate, accept the mod, prove
compatibility, or copy unknown versions and archive names into an edition manifest. Edition
manifests continue to own engine behavior, plugins, requirements, conflicts, patches,
testing notes, and load-order relationships. The full lifecycle and its two independent
status systems are documented in the
[`Sourced Mod Workflow`](ash-archive/shared/sourced-mod-workflow.md).

## Setup and local checks

Python 3.11 or newer is required. From `ash-archive/`:

```bash
python -m pip install -e ".[dev]"

python tools/lint_repo.py
python tools/validate_manifests.py
python tools/check_duplicate_mods.py
python tools/compare_editions.py
python tools/generate_modlist_markdown.py --check
pytest
```

`python tools/summarize_sourced_mods.py` is an optional read-only candidate report; it is
not a release or compatibility check.

To intentionally refresh generated modlists after a manifest change, run
`python tools/generate_modlist_markdown.py`, review both diffs, and then rerun with
`--check`. Only the content between `GENERATED-CONTENT` markers in
`editions/*/MODLIST.md` is generated; do not edit those sections by hand.

## Continuous integration

The [`Repository checks`](.github/workflows/pr-repository-checks.yml) and
[`Archive integrity`](.github/workflows/pr-archive-integrity.yml) workflows run on pull
requests and pushes to `main`. They use Python 3.11 to run repository lint, manifest and
source-reference validation, duplicate scanning, edition comparison, the read-only
generated-file check, and the test suite. Passing CI validates repository structure and
consistency only; it is not evidence of an installable list or in-game compatibility.

## Documentation

- [`ash-archive/README.md`](ash-archive/README.md) — control-data model, automation boundaries, and contributor navigation
- [`Project Bible`](ash-archive/PROJECT-BIBLE.md) — project thesis and design constraints
- [`Roadmap`](ash-archive/ROADMAP.md) — development phases and release gates
- [`Sourced Mod Workflow`](ash-archive/shared/sourced-mod-workflow.md) — candidate intake, source links, evaluation, and promotion
- [`Control Metadata Schema`](ash-archive/shared/mod-meta-schema.md) — field ownership and validation rules
- [`Pilgrim Edition`](ash-archive/editions/openmw/README.md) — OpenMW scope and documentation
- [`Sleeper Edition`](ash-archive/editions/mwse/README.md) — MWSE scope and documentation
- [`Local Agent Presets`](ash-archive/LOCAL-AGENT-PRESETS.md) — conservative maintenance agents and review gates

See [`CONTRIBUTING.md`](CONTRIBUTING.md) before changing manifests, tools, or planning
documents.

## Security

The project has no released installer or supported runtime version. Repository-tooling
security guidance is in [`SECURITY.md`](SECURITY.md).

## License status

Licensing requires maintainer review. The repository-root [`LICENSE`](LICENSE) contains
CC0 1.0 text, while [`ash-archive/LICENSE.md`](ash-archive/LICENSE.md) contains incomplete,
conflicting MIT text. This documentation does not choose between them; do not treat the
nested file as an authoritative grant until the conflict is resolved.
