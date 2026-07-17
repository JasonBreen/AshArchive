---
name: ash-archive-lint-manifests
description: Reproduce and mechanically repair Ash Archive manifest, schema, YAML, naming, ordering, and control-metadata lint failures. Use when validation or tests fail for `.control.meta` files; do not use when a fix requires new provenance, compatibility evidence, or design judgment.
---

# Lint Ash Archive Manifests

## Canonical Policy

Read `.agents/presets/manifest-lint-agent.yaml` completely before acting. Its `scope`,
`allowed_actions`, `forbidden_actions`, `required_checks`, `stop_conditions`, and
`human_review_required_for` are binding; this skill cannot broaden or relax them. Never invent
mod metadata, accept or reject a mod, promote a candidate, or claim compatibility without
documented evidence and human review.

## Workflow

1. Read `AGENT-RULES.md`, `ash-archive/PROJECT-BIBLE.md`,
   `ash-archive/LOCAL-AGENT-PRESETS.md`, `.agents/presets/manifest-lint-agent.yaml`,
   `ash-archive/shared/mod-meta-schema.md`, and `ash-archive/shared/naming-policy.md` completely.
2. From `ash-archive/`, reproduce the failure with `python tools/validate_manifests.py` or the
   exact failing test before editing.
3. Make the smallest mechanical correction directly implied by repository evidence. Preserve
   rejected records and all reasoning.
4. Run `python tools/lint_repo.py`, `python tools/validate_manifests.py`, and
   `pytest tests/test_validation.py tests/test_control_meta_conventions.py tests/test_meta_filename_conventions.py`.
5. Regenerate public modlists only when a manifest change affects generated output.
6. Report the original failure category, files changed, and before/after results.

## Stop Conditions

Stop when a value is not unambiguous, a failure exposes a policy decision, or the proposed fix
would invent source metadata, review notes, or compatibility evidence.
