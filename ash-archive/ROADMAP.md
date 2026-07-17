# Roadmap

## Current state

- The dual-edition directory and manifest structure is established.
- Pull requests and pushes to `main` are checked with Python 3.11 repository lint,
  manifest/source-reference validation, duplicate scanning, edition comparison,
  deterministic generated-modlist checking, and tests.
- Shared sourced candidates can be linked to edition planning entries without duplicating
  canonical provenance or implying promotion.
- Most installer, load-order, performance, post-install, and in-game test documentation is
  still blocked on real builds and recorded evidence.
- The project remains a planning/control scaffold, not an installable or playable Wabbajack list.

## Phase 0 - Repository foundation (completed)

**Goal:** establish guardrails before content scaling.

Completed outcomes:

- Shared and per-edition control-data layouts exist.
- Structural validation, deterministic generation checks, and CI are in place.
- Agent and contribution guardrails preserve evidence standards and edition separation.
- Documentation shells identify missing install, test, and release evidence without claiming it exists.

Phase 0 completion means the planning repository is maintainable; it does not mean either
edition has been assembled or tested.

## Phase 1 - Sourcing (active)

**Goal:** build trustworthy candidate pools with traceable provenance.

In-scope work:

- Expand `shared/sourced-mods.control.meta` across underrepresented categories.
- Resolve blockers in `shared/source-triage.control.meta` and maintain package relationships
  in `shared/source-package-meta.control.meta`.
- Link matching edition planning entries with optional `source_reference` values while
  leaving unknown edition-specific fields unknown.
- Retain rejected and superseded records with their reasoning.

Exit criteria:

- Candidate pools are sufficiently populated across major categories for both editions.
- Validation passes with no structural or source-reference issues.
- Source provenance and decision notes are present for all active candidates.
- Blocking identity, package, and distribution questions are either resolved or explicitly deferred.

## Phase 2 - Evaluation

**Goal:** turn sourced candidates into evidence-based, human-reviewed edition decisions.

In-scope work:

- Move candidate records through `candidate` and `under-review` using the shared rubric.
- Test edition behavior by category and repeatable route.
- Record conflicts, mitigation paths, and edition-specific behavior.
- Promote candidates and advance edition status only when each action's separate evidence
  and human-review requirements are met.

Exit criteria:

- Core categories have evaluated coverage for both editions.
- Major conflicts are resolved or explicitly deferred with notes.
- Promoted candidates and accepted edition entries have the required review and compatibility evidence.

## Phase 3 - Edition hardening

**Goal:** stabilize each edition as an independent, coherent, testable package.

In-scope work:

- Establish and test edition-specific load-order policy.
- Finalize patch strategy, external tools, and reproducible setup requirements.
- Run repeated install, performance, and test-route cycles and record regressions.

Exit criteria:

- Both editions have internally consistent manifests and patch plans.
- Known issues are documented with severity, evidence, and workarounds where available.
- Installation, post-install, performance, and testing instructions are reproducible.
- Release checklists describe verified evidence rather than placeholder intent.

## Phase 4 - Wabbajack release preparation

**Goal:** prepare installable builds with explicit support boundaries.

In-scope work:

- Freeze human-approved release-candidate manifests.
- Produce installer-facing documentation and release artifacts.
- Perform clean end-to-end install tests for each edition.
- Resolve or explicitly document licensing, distribution, and support boundaries.

Exit criteria:

- The documented install flow succeeds independently for each edition.
- Release notes, known issues, support boundaries, and checksums/artifacts are published.
- A human reviewer approves release readiness for each edition.
