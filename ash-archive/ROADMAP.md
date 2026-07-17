# Roadmap

## Current state — July 2026

- **Active phase:** Phase 1 — Sourcing.
- The dual-edition control structure, metadata schemas, generated modlist pipeline, validation tooling, repository lint, agent policy, and pre-merge checks are in place.
- Shared candidate intake and source-triage records exist, but category coverage, provenance cleanup, and compatibility evaluation remain incomplete.
- The project is **not** an installable Wabbajack release, has no final load order, and has no end-to-end playtest record.

Immediate Phase 1 work is tracked in [FOLLOW-UP-TASKS.md](FOLLOW-UP-TASKS.md).

## Phase 0 — Scaffold (completed)

**Goal:** establish structure and guardrails before content scaling.

Completed outcomes:

- Shared and per-edition manifest layout defined.
- Internal metadata standardized on YAML-formatted `.control.meta` files and explicitly separated from MO2 download sidecars.
- Validation, generation, comparison, duplicate detection, and repository lint tooling established.
- Baseline project, edition, contributor, sourcing, metadata, and testing documentation created.
- Runner-neutral maintenance presets, runnable project-scoped Codex agents, and reusable repository skills synchronized under automated tests.
- Pull-request workflows added for lint, tests, manifest validity, generated-output freshness, edition drift, and duplicate checks.

## Phase 1 — Sourcing (active)

**Goal:** build trustworthy candidate pools with traceable provenance while preserving edition-specific direction.

In-scope work:

- Expand `shared/sourced-mods.control.meta` across underrepresented major categories.
- Resolve blockers in `shared/source-triage.control.meta`, including official-plugin policy and unidentified or non-reproducible packages.
- Keep `shared/source-package-meta.control.meta` synchronized for sources that provide multiple installable packages.
- Replace placeholder source, version, archive, and requirement fields only when evidence exists.
- Define initial evaluation batches and test routes without promoting untested candidates.

Exit criteria:

- Candidate pools cover the major categories needed by both editions.
- Active candidates include source provenance, confidence, decision notes, and an explicit compatibility state.
- Blocking source-triage questions are resolved or deliberately deferred with recorded rationale.
- Validation, generated-output, edition-comparison, duplicate, lint, and test checks pass for the milestone branch.

## Phase 2 — Evaluation

**Goal:** convert sourced candidates into evidence-based accept, reject, or defer decisions.

In-scope work:

- Evaluate candidates by category, engine, and test route using the shared rubric.
- Record compatibility behavior, conflicts, performance considerations, and mitigation paths.
- Preserve rejected candidates and their reasoning.
- Promote entries into edition manifests only after human review of recorded evidence.

Exit criteria:

- Core categories have evaluated coverage for both editions.
- Major conflicts are resolved, mitigated, or explicitly deferred.
- Accepted entries have reproducible source and compatibility evidence.
- Intentional OpenMW/MWSE differences are documented rather than flattened into parity.

## Phase 3 — Edition hardening

**Goal:** stabilize each edition as a coherent, testable package.

In-scope work:

- Establish and enforce edition-level load-order policy.
- Finalize patch strategy and external tool requirements.
- Replace planning placeholders with verified configuration and support documentation.
- Run repeated install, route, performance, and regression passes.

Exit criteria:

- Each edition has internally consistent manifests, load-order policy, and patch plans.
- Installation and post-install procedures are reproducible.
- Known issues are documented with severity, affected scope, and workarounds where available.
- Release checklists are actionable and backed by recorded results.

## Phase 4 — Wabbajack release preparation

**Goal:** ship installable builds with clear support boundaries.

In-scope work:

- Freeze manifests for release candidates.
- Build Wabbajack artifacts and final installer-facing documentation.
- Perform clean-machine end-to-end installation tests for both editions.
- Publish release notes, known issues, prerequisites, and support expectations.

Exit criteria:

- Each documented install flow succeeds from a clean environment.
- Generated artifacts match frozen manifests and verified source metadata.
- Release notes and known issues are complete.
- A human maintainer approves each edition for distribution.
