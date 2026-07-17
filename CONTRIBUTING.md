# Contributing to Ash Archive

Ash Archive is a planning/control repository for two sibling Morrowind editions:

- **Pilgrim Edition** targets OpenMW.
- **Sleeper Edition** targets classic Morrowind + MCP + MGE XE + MWSE.

Neither edition is currently installable or playable. Do not present planned entries,
repository validation, upstream documentation, or a source link as in-game test evidence.

## Before changing files

Read [`AGENT-RULES.md`](AGENT-RULES.md), the
[`PROJECT-BIBLE.md`](ash-archive/PROJECT-BIBLE.md), and the documentation for the affected
edition or shared subsystem. Work on a focused branch, keep the pull request reviewable,
and preserve intentional differences between the editions.

## Branch and commit conventions

Use a descriptive branch with an appropriate prefix such as `codex/`, `docs/`, `tooling/`,
`manifests/`, `wabbajack/`, or `ci/`.

Use concise commit prefixes where helpful: `docs:`, `tools:`, `manifests:`, `shared:`,
`openmw:`, `mwse:`, `tests:`, or `ci:`.

## Install development dependencies

From `ash-archive/`:

```bash
python -m pip install -e ".[dev]"
```

Python 3.11 or newer is required.

## Local validation

The full CI-equivalent suite is:

```bash
python tools/lint_repo.py
python tools/validate_manifests.py
python tools/check_duplicate_mods.py
python tools/compare_editions.py
python tools/generate_modlist_markdown.py --check
pytest
```

Run commands from `ash-archive/`. A genuinely scope-limited change may justify a subset,
but the pull request must list every skipped check and the reason. The optional
`python tools/summarize_sourced_mods.py` command prints a candidate overview and is not a
validation or release-readiness result.

Continuous integration runs the full suite on pull requests and pushes to `main`. These
checks establish structural consistency, not gameplay compatibility, installability, or
release readiness.

## Generated modlists

`editions/openmw/MODLIST.md` and `editions/mwse/MODLIST.md` contain manual introductions
and generated sections delimited by `GENERATED-CONTENT` markers. Never hand-edit content
between those markers.

After a manifest change that affects public output:

1. Run `python tools/generate_modlist_markdown.py`.
2. Review both edition diffs, including unexpected removals or status changes.
3. Run `python tools/generate_modlist_markdown.py --check` to confirm the committed view is current.

## Metadata ownership

Internal `.control.meta` files are YAML project metadata, not Mod Organizer 2 download
sidecars. The main metadata layers have different responsibilities:

| Layer | Canonical responsibility |
|---|---|
| `shared/sourced-mods.control.meta` | Candidate identity, source type, source URL, provenance evidence, source confidence, and candidate review state. |
| `editions/*/manifests/mods.control.meta` | Edition choice, engine behavior, plugins, dependencies, conflicts, patches, testing evidence, and load-order relationships. |
| `editions/*/MODLIST.md` | Generated public planning view; never the source of truth. |

See the [`control metadata schema`](ash-archive/shared/mod-meta-schema.md) for field rules.

## Source references and the two state systems

An edition manifest entry may set `source_reference` to the ID of a canonical candidate in
`shared/sourced-mods.control.meta`. A link may be added to an existing `planned` edition
placeholder when identity and provenance match. The link does not fill unknown version or
archive data and does not change either status automatically.

Candidate intake uses `candidate_status` (`candidate`, `under-review`, `promoted`,
`rejected`, or `superseded`). Edition manifests separately use `status` (`planned`,
`testing`, `accepted`, `rejected`, `needs-patch`, or `deprecated`). Promotion and edition
acceptance remain human-review decisions, and `testing`/`accepted` require recorded evidence.
Follow the [`Sourced Mod Workflow`](ash-archive/shared/sourced-mod-workflow.md).

## Manifest changes

When editing an edition manifest:

1. Keep OpenMW and MWSE as sibling implementations, not forced parity.
2. Use a category from `shared/categories.control.meta`.
3. Keep IDs lowercase kebab-case and priorities unique within a category.
4. Use only engine values supported by that edition.
5. Reference existing IDs in requirements, conflicts, and load-order fields.
6. Leave unknown source, version, archive, plugin, and compatibility facts explicitly unknown.
7. Do not set `testing` or `accepted` without the evidence required by validation and human review.
8. Preserve rejection reasoning.

## Source research

When updating a canonical source record:

1. Prefer current primary sources and record what the evidence actually establishes.
2. Distinguish source confidence from compatibility evidence.
3. Do not invent URLs, IDs, versions, archive names, plugin names, or redistribution terms.
4. Keep unresolved identity, licensing, or package questions blocked or unverified.
5. Do not promote or accept a candidate merely because its source URL is verified.

## Documentation changes

Keep status language tied to repository evidence. Placeholder pages must say what is blocked
and what evidence is needed; an empty known-issues page must not imply that no issues exist.
Preserve the dual-edition model and the design constraints in the project bible.

## Design-bible exceptions

If a proposal conflicts with the project bible, add a clearly labeled **Design-Bible
Exception Request** to the pull request. Identify the exact rule, rationale, alternatives,
and risk. A maintainer must review the exception; do not silently weaken the rule in prose or
metadata.

## Pull request expectations

Describe what changed, why it changed, affected editions, validation results, skipped checks,
and remaining uncertainty. Explicitly separate repository/tooling results from source facts
and from in-game evidence. Do not mix unrelated work.
