# Roadmap

## Current state (April 2026)
- Repository foundation is in place: dual-edition structure, schema-backed manifests, baseline docs, and validation/generation tooling.
- Project remains **planning/scaffold**, not yet an installable or fully playable Wabbajack list.

## Phase 0 - Scaffold (completed)
**Goal:** establish guardrails before content scaling.

Completed outcomes:
- Shared and per-edition manifest layout defined.
- Validation and consistency tooling established.
- Baseline documentation created for setup, policy, and testing flow.

## Phase 1 - Sourcing (active)
**Goal:** build trustworthy candidate pools with traceable provenance.

In-scope work:
- Expand `shared/sourced-mods.control.meta` with verified metadata and source links.
- Keep triage and package metadata synchronized (`shared/source-triage.control.meta`, `shared/source-package-meta.control.meta`).
- Track rejected options with retained reasoning.

Exit criteria:
- Candidate pools are sufficiently populated across major categories for both editions.
- Validation passes with no structural issues.
- Source provenance and decision notes are present for all active candidates.

## Phase 2 - Evaluation
**Goal:** convert sourced candidates into evidence-based accept/reject decisions.

In-scope work:
- Evaluate by category and test route using the shared rubric.
- Record compatibility notes, conflicts, and mitigation paths.
- Promote tested entries into edition manifests; document rejections with rationale.

Exit criteria:
- Core categories have evaluated coverage for both editions.
- Major conflicts are either resolved or explicitly deferred with notes.
- Accepted entries include compatibility evidence.

## Phase 3 - Edition hardening
**Goal:** stabilize each edition as a coherent, testable package.

In-scope work:
- Lock edition-level load-order policy enforcement.
- Finalize patch strategy and external tool requirements.
- Run repeated validation and checklist cycles for regression control.

Exit criteria:
- Both editions have internally consistent manifests and patch plans.
- Known issues are documented with severity and workarounds.
- Release checklists are actionable and reproducible.

## Phase 4 - Wabbajack release preparation
**Goal:** ship installable builds with clear support boundaries.

In-scope work:
- Freeze manifests for release candidates.
- Produce final modlist exports and installer-facing documentation.
- Perform end-to-end install tests and capture support notes.

Exit criteria:
- Install flow succeeds for each edition using documented steps.
- Release notes and known issues are published.
- Versioned release artifacts are ready for distribution.
