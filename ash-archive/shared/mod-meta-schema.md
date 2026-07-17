# Control Metadata and Manifest Schema

Ash Archive uses YAML `.control.meta` files as internal control data. They are not native
MO2 download sidecars. This document describes field ownership and the contracts enforced by
repository tools; the Python validators remain the executable specification.

## Metadata layers

| File family | Top-level shape | Responsibility |
|---|---|---|
| `shared/sourced-mods.control.meta` | `sourced_candidates:` list | Canonical candidate identity, provenance, source evidence, uncertainty, and candidate-review state. |
| `editions/*/manifests/mods.control.meta` | `mods:` list | Edition-specific selection, engine, plugin, patch, test, conflict, dependency, and ordering data. |
| `shared/source-triage.control.meta` | `source_triage:` mapping | Blocking identity, package, and distribution questions from imported inventory. |
| `shared/source-package-meta.control.meta` | `multi_package_sources:` list | Parent source pages and child package evidence. |
| `editions/*/MODLIST.md` | generated Markdown section | Derived planning view; not canonical metadata. |

The repository-root [`modlist.txt`](../../modlist.txt) is an inventory snapshot, not an
edition manifest or a complete MO2 download-sidecar source.

## Canonical source records

Each sourced candidate has a stable lowercase kebab-case `id`. The source layer owns:

- `source_type`, `source_url`, `source_confidence`, and `evidence_notes`;
- candidate identity and thematic/risk notes;
- `candidate_status`, review fields, intended editions, compatibility status, and promotion target;
- `related_manifest_ids`, the reverse links to edition entries.

Candidate status values are `candidate`, `under-review`, `promoted`, `rejected`, and
`superseded`. Source confidence and compatibility are separate: a source can be verified
while game compatibility still needs testing.

## Edition manifest records

Edition entries require an ID, name, category, edition, cross-edition status, manifest
status, non-empty engine list, source/package fields, plugin/dependency/conflict/order lists,
patch and testing notes, decision reason, and positive integer priority.

- IDs use lowercase kebab-case.
- `edition` is `openmw` or `mwse` and must match the containing edition.
- Engine values must be supported by that edition.
- Priorities are unique within each category.
- `requires`, `conflicts`, `load_after`, and `load_before` reference IDs in the same manifest.
- Planned records may retain blank or explicit placeholder source, URL, version, archive,
  plugin, patch, and testing facts.
- `testing` and `accepted` require positive, non-placeholder test evidence, a non-placeholder
  `reviewed_by` list, and an ISO `last_reviewed` date in `YYYY-MM-DD` form. When linked, the
  canonical candidate must use `source_confidence: verified`.
- `accepted` also requires `source_reference`, a promoted canonical candidate whose
  `promotion_target` includes the entry's edition, and compatible evidence for that edition.
- `rejected`, `needs-patch`, and `deprecated` require non-placeholder decision rationale;
  rejection additionally requires named human review and a review date.

Edition manifest status values are `planned`, `testing`, `accepted`, `rejected`,
`needs-patch`, and `deprecated`. They are independent of candidate status.

## `source_reference`

An edition entry may set optional `source_reference` to a canonical sourced-candidate ID.
Validation checks that the source exists, names and intended editions agree, the candidate is
not rejected or superseded, and `related_manifest_ids` links back.

Planning and testing provenance links are independent of `promotion_target`. That field is
enforced for acceptance, when a promoted candidate must target the accepting edition.

The source record is canonical for source type, source URL, and source evidence. If a linked
manifest repeats a non-placeholder source type or URL, it must agree with the canonical
record. Linking does not:

- change `candidate_status` or edition `status`;
- prove compatibility or testing;
- accept or promote the mod;
- copy unknown versions, archives, plugins, or edition-specific behavior.

See [`sourced-mod-workflow.md`](sourced-mod-workflow.md) for the lifecycle.

## Generated Markdown

`tools/generate_modlist_markdown.py` replaces only content between the
`GENERATED-CONTENT` markers in each edition `MODLIST.md`. Use the normal command to refresh
output and `--check` to compare without writing. Manual introductions remain outside the
markers.
