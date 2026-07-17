# Sourced Mod Workflow

`shared/sourced-mods.control.meta` is the canonical candidate intake and provenance layer.
It is not an accepted-mod list and is not a native MO2 download sidecar.

## 1. Candidate intake

For each candidate, record a stable ID and name, primary source type and URL when known,
source confidence, evidence notes, intended editions, thematic fit, compatibility status,
risk, engine uncertainty, promotion target, and review fields. Leave unknown facts empty or
explicitly unverified; never reconstruct a version, archive, plugin, or URL.

The file uses one top-level `sourced_candidates:` list. Do not replace it with bucket-grouped
shapes.

## 2. Candidate state machine

Allowed candidate-review paths are:

- `candidate` -> `under-review` -> `promoted`
- `candidate` or `under-review` -> `rejected`
- `candidate` or `under-review` -> `superseded`

Human review is required for promotion, rejection, and supersession. Retain the evidence,
rationale, a non-placeholder `reviewed_by` list, and an ISO `last_reviewed` date where validation
requires a completed review.

## 3. Provenance link to edition planning

An existing or new edition planning entry may set `source_reference` to a sourced-candidate
ID when identity and intended edition agree. Add the manifest ID to the source record's
`related_manifest_ids` reverse link.

This relationship can exist while the source remains `candidate` and the edition entry
remains `planned`. It means only that canonical provenance is connected. It does not promote,
accept, test, or prove compatibility, and it does not require unknown version/archive fields
to be copied into the manifest.

Canonical source records own source type, URL, and evidence. Edition manifests own engine
behavior, plugins, requirements, conflicts, patches, test results, and load-order relations.

## 4. Edition state machine

Edition status is independent of candidate status:

- `planned` records intent and may retain honest placeholders.
- `testing` requires recorded package/version and positive test evidence, a non-placeholder
  `reviewed_by` list, and `last_reviewed` in `YYYY-MM-DD` form. A linked canonical candidate
  must have `source_confidence: verified`.
- `accepted` requires `source_reference`, human review, a promoted canonical candidate,
  whose `promotion_target` includes the edition, compatible evidence for that edition, and
  complete edition-specific review notes.
- `needs-patch`, `rejected`, and `deprecated` describe edition decisions and must retain
  non-placeholder rationale. Rejection also requires named human review and a review date.

Changing one state machine never changes the other implicitly.

## 5. Evaluation and promotion

Use [`mod-evaluation-rubric.md`](mod-evaluation-rubric.md) and edition-specific test routes.
Record what was tested, configuration, result, reviewer, and unresolved risk separately for
Pilgrim and Sleeper. Upstream tags may inform planning but are not in-game evidence.

Promotion into one edition does not require parity in the other. Preserve engine-native
implementations and explain intentional differences.

## 6. Unknown-origin and package gates

`source-triage.control.meta` tracks unresolved imported inventory entries. While its gate is
open, affected records remain unverified until identity, source, package, and licensing
questions are resolved.

Use `source-package-meta.control.meta` when one source page distributes multiple packages.
Keep shared parent provenance separate from child variant, artifact, plugin, edition, and
version evidence. A local imported path is snapshot evidence, not a portable acquisition instruction.

## 7. Validation and generation

From `ash-archive/`, run:

```bash
python tools/validate_manifests.py
python tools/check_duplicate_mods.py
python tools/compare_editions.py
python tools/generate_modlist_markdown.py
python tools/generate_modlist_markdown.py --check
pytest
```

Review generated diffs. The public modlists are planning views and do not replace source or
manifest evidence.
